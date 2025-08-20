import axios, { AxiosInstance } from 'axios';
import { API_URL } from '../config/environment';
import { getAccessToken } from './authTokenStore';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
  thoughts?: string[]; // AI thinking process and tool usage
}

export interface ChatRequest {
  user_message: string;
  conversation_history: ChatMessage[];
  document_content: {
    text: string;
    paragraphs?: string[];
    selection?: any;
  };
  session_id?: string | null;
}

export interface RunResponse {
  run_id: string;
  session_id: string;
}

export interface ChatResponse {
  response: string;
  metadata: {
    should_draft_claims: boolean;
    has_claims: boolean;
    reasoning: string;
  };
  data?: {
    claims?: string[];
    num_claims?: number;
    review_comments?: Array<{
      comment: string;
      severity: string;
    }>;
  };
  session_id?: string;
}

export interface StreamEvent {
  event: string;
  data: any;
}

export interface ApiError {
  message: string;
  code?: string;
  details?: any;
}

// Event types that match your backend
export type EventType = 
  | 'intent_analysis'
  | 'intent_classified'
  | 'claims_drafting_start'
  | 'claims_progress'
  | 'claims_complete'
  | 'prior_art_start'
  | 'prior_art_progress'
  | 'prior_art_complete'
  | 'review_start'
  | 'review_progress'
  | 'review_complete'
  | 'processing'
  | 'complete'
  | 'error'
  | 'low_confidence';

class ApiService {
  private api: AxiosInstance;
  private baseURL: string;

  constructor() {
    this.baseURL = API_URL;
    this.api = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
    });

    // Add request interceptor for authentication
    this.api.interceptors.request.use((config) => {
      const token = getAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  private handleApiError(error: any): ApiError {
    if (error.response) {
      return {
        message: error.response.data?.message || `Server error: ${error.response.status}`,
        code: error.response.status.toString(),
        details: error.response.data
      };
    } else if (error.request) {
      return {
        message: 'No response from server. Please check your connection.',
        code: 'NETWORK_ERROR'
      };
    } else {
      return {
        message: error.message || 'An unexpected error occurred',
        code: 'UNKNOWN_ERROR'
      };
    }
  }

  /**
   * Start a new patent drafting run
   */
  async startPatentRun(request: ChatRequest): Promise<RunResponse> {
    try {
      const response = await this.api.post('/api/patent/run', request);
      return response.data;
    } catch (error) {
      throw this.handleApiError(error);
    }
  }

  /**
   * Stream the agent's response using Server-Sent Events (SSE)
   * Updated to properly handle the backend's streaming events
   */
  async chatStream(
    request: ChatRequest,
    onChunk: (chunk: string, eventType?: string) => void,
    onComplete: (response: ChatResponse) => void,
    onError: (error: Error) => void,
    signal?: AbortSignal
  ): Promise<void> {
    try {
      console.log('🚀 API SERVICE: chatStream called with request:', request);
      
      // First, start the patent run
      console.log('🚀 API SERVICE: Starting patent run...');
      const runResponse = await this.startPatentRun(request);
      console.log('🚀 API SERVICE: Patent run started:', runResponse);
      
      // Then stream the response using the new streaming endpoint
      const response = await fetch(`${this.baseURL}/api/patent/stream?run_id=${runResponse.run_id}`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${getAccessToken() || ''}`,
        },
        signal,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const reader = response.body?.getReader();
      if (!reader) {
        throw new Error('No response body reader available');
      }

      let buffer = '';
      const decoder = new TextDecoder();
      let finalResponse: ChatResponse | null = null;
      let currentEventType = '';

      while (true) {
        if (signal?.aborted) {
          throw new Error('Stream aborted by client');
        }

        const { done, value } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const lines = buffer.split('\n');
        buffer = lines.pop() || '';

        for (const line of lines) {
          if (line.startsWith('event: ')) {
            currentEventType = line.slice(7).trim();
            console.log('📡 SSE Event:', currentEventType);
          } else if (line.startsWith('data: ')) {
            const content = line.slice(6).trim();
            
            if (content === '{}') {
              // Stream complete
              if (finalResponse) {
                finalResponse.session_id = runResponse.session_id;
                onComplete(finalResponse);
              }
              return;
            }
            
            try {
              const parsed = JSON.parse(content);
              console.log(`🔍 Processing event: ${currentEventType}`, parsed);
              
              // Handle the streaming events based on your backend implementation
              switch (currentEventType) {
                case 'intent_analysis':
                  onChunk(parsed.text || parsed.message || 'Analyzing your request...', 'intent_analysis');
                  break;
                  
                case 'intent_classified':
                  onChunk(parsed.text || `Intent: ${parsed.intent_type} (${Math.round((parsed.confidence || 0) * 100)}% confidence)`, 'intent_classified');
                  break;
                  
                case 'claims_drafting_start':
                  onChunk(parsed.text || 'Starting patent claims drafting...', 'claims_drafting_start');
                  break;
                  
                case 'claims_progress':
                  // Handle different stages of claims progress
                  if (parsed.stage === 'analysis') {
                    onChunk(parsed.text || 'Analyzing invention disclosure...', 'claims_progress');
                  } else if (parsed.stage === 'feature_identification') {
                    onChunk(parsed.text || 'Identifying key inventive features...', 'claims_progress');
                  } else if (parsed.stage === 'drafting') {
                    onChunk(parsed.text || 'Drafting comprehensive patent claims...', 'claims_progress');
                  } else if (parsed.claim_number) {
                    // Show the actual claim text, not just "Generated claim X of Y"
                    const claimText = parsed.text || `Claim ${parsed.claim_number} of ${parsed.total_claims}`;
                    onChunk(claimText, 'claims_progress');
                  } else {
                    onChunk(parsed.text || 'Processing claims...', 'claims_progress');
                  }
                  break;
                  
                case 'claim_generated':
                  // Handle individual claim generation events
                  const claimText = parsed.text || `Claim ${parsed.claim_number} of ${parsed.total_claims}`;
                  onChunk(claimText, 'claim_generated');
                  break;
                  
                case 'claims_complete':
                  const claimsMsg = parsed.num_claims ? 
                    `Successfully drafted ${parsed.num_claims} patent claims` : 
                    'Patent claims completed';
                  onChunk(parsed.text || claimsMsg, 'claims_complete');
                  break;
                  
                case 'prior_art_start':
                  onChunk(parsed.text || 'Starting prior art search...', 'prior_art_start');
                  break;
                  
                case 'prior_art_progress':
                  if (parsed.stage === 'searching') {
                    onChunk(parsed.text || 'Searching patent databases...', 'prior_art_progress');
                  } else if (parsed.stage === 'analyzing') {
                    onChunk(parsed.text || 'Analyzing search results for relevance...', 'prior_art_progress');
                  } else if (parsed.stage === 'reporting') {
                    onChunk(parsed.text || 'Generating comprehensive prior art report...', 'prior_art_progress');
                  } else {
                    onChunk(parsed.text || 'Processing prior art...', 'prior_art_progress');
                  }
                  break;
                  
                case 'prior_art_complete':
                  const patentsMsg = parsed.patents_found ? 
                    `Prior art search completed - found ${parsed.patents_found} relevant patents` : 
                    'Prior art search completed';
                  onChunk(parsed.text || patentsMsg, 'prior_art_complete');
                  break;
                  
                case 'review_start':
                  onChunk(parsed.text || 'Starting patent claim review...', 'review_start');
                  break;
                  
                case 'review_progress':
                  if (parsed.stage === 'analysis') {
                    onChunk(parsed.text || 'Analyzing claim structure and language...', 'review_progress');
                  } else if (parsed.stage === 'compliance_check') {
                    onChunk(parsed.text || 'Checking USPTO compliance...', 'review_progress');
                  } else {
                    onChunk(parsed.text || 'Reviewing claims...', 'review_progress');
                  }
                  break;
                  
                case 'review_complete':
                  const reviewMsg = parsed.review_comments?.length ? 
                    `Claim review completed - found ${parsed.review_comments.length} issues to address` : 
                    'Claim review completed';
                  onChunk(parsed.text || reviewMsg, 'review_complete');
                  break;
                  
                case 'processing':
                  onChunk(parsed.message || parsed.text || 'Processing your request...', 'processing');
                  break;
                  
                case 'complete':
                  // Final completion with results
                  finalResponse = {
                    response: parsed.response || 'Process completed',
                    metadata: parsed.metadata || {
                      should_draft_claims: false,
                      has_claims: false,
                      reasoning: parsed.message || 'Process completed'
                    },
                    data: parsed.data,
                    session_id: runResponse.session_id
                  };
                  
                  // Handle different types of completions
                  if (parsed.claims) {
                    finalResponse.data = {
                      ...finalResponse.data,
                      claims: parsed.claims,
                      num_claims: parsed.num_claims || parsed.claims.length
                    };
                    finalResponse.metadata.should_draft_claims = true;
                    finalResponse.metadata.has_claims = true;
                  }
                  
                  if (parsed.review_comments) {
                    finalResponse.data = {
                      ...finalResponse.data,
                      review_comments: parsed.review_comments
                    };
                  }
                  
                  console.log('🎯 Final response prepared:', finalResponse);
                  onChunk(parsed.response || 'Process completed', 'complete');
                  break;
                  
                case 'error':
                  const errorMsg = parsed.error || parsed.message || 'An error occurred';
                  onChunk(`❌ ${errorMsg}`, 'error');
                  onError(new Error(errorMsg));
                  return;
                  
                case 'low_confidence':
                  const clarificationMsg = parsed.message || 'I need more information to help you effectively.';
                  onChunk(`❓ ${clarificationMsg}`, 'low_confidence');
                  break;
                  
                // Handle legacy event types for backward compatibility
                case 'status':
                  onChunk(parsed.message || 'Processing...', 'status');
                  break;
                  
                case 'reasoning':
                  onChunk(parsed.text || 'Analyzing...', 'reasoning');
                  break;
                  
                case 'search_progress':
                  if (parsed.step === 'searching') {
                    onChunk('🔍 Searching patent databases...', 'search_progress');
                  } else if (parsed.step === 'analyzing') {
                    onChunk('📊 Analyzing search results...', 'search_progress');
                  } else {
                    onChunk(parsed.message || 'Searching...', 'search_progress');
                  }
                  break;
                  
                case 'report_progress':
                  if (parsed.step === 'structuring') {
                    onChunk('📋 Structuring the report...', 'report_progress');
                  } else if (parsed.step === 'formatting') {
                    onChunk('✨ Formatting content...', 'report_progress');
                  } else {
                    onChunk(parsed.message || 'Generating report...', 'report_progress');
                  }
                  break;
                  
                case 'tool_call':
                  if (parsed.tool === 'draft_claims') {
                    onChunk(`🛠️ Drafting ${parsed.num_claims || 'patent'} claims...`, 'tool_call');
                  } else {
                    onChunk(`🛠️ Using ${parsed.tool || 'tool'}...`, 'tool_call');
                  }
                  break;
                  
                case 'tool_result':
                  if (parsed.tool === 'draft_claims' && parsed.success) {
                    onChunk(`✅ Generated ${parsed.claims_generated || 'patent'} claims`, 'tool_result');
                  } else {
                    onChunk('✅ Tool execution completed', 'tool_result');
                  }
                  break;
                  
                case 'results':
                  // Legacy results event
                  finalResponse = {
                    response: parsed.response || 'Process completed',
                    metadata: parsed.metadata || {
                      should_draft_claims: false,
                      has_claims: false,
                      reasoning: 'Process completed'
                    },
                    data: parsed.data,
                    session_id: runResponse.session_id
                  };
                  onChunk(parsed.response || 'Results ready', 'results');
                  break;
                  
                case 'done':
                  // Legacy done event
                  if (finalResponse) {
                    finalResponse.session_id = runResponse.session_id;
                    onComplete(finalResponse);
                  }
                  return;
                  
                default:
                  // Handle unknown event types gracefully
                  console.warn('⚠️ Unknown event type:', currentEventType, parsed);
                  
                  if (parsed.text || parsed.message) {
                    onChunk(parsed.text || parsed.message, 'unknown');
                  } else if (parsed.response) {
                    onChunk(parsed.response, 'unknown');
                  }
                  break;
              }
            } catch (parseError) {
              console.warn('Failed to parse streaming data:', parseError);
            }
          }
        }
      }

      // If we reach here without a proper completion, ensure we complete
      if (finalResponse) {
        finalResponse.session_id = runResponse.session_id;
        onComplete(finalResponse);
      }
    } catch (error) {
      console.error('🚨 Stream error:', error);
      onError(error as Error);
    }
  }

  /**
   * Legacy method for backward compatibility
   */
  async chat(request: { 
    message: string; 
    document_content?: string; 
    session_id?: string | null; 
    conversation_history?: ChatMessage[] 
  }): Promise<ChatResponse> {
    const patentRequest: ChatRequest = {
      user_message: request.message,
      conversation_history: request.conversation_history || [],
      document_content: {
        text: request.document_content || '',
        paragraphs: request.document_content ? [request.document_content] : undefined,
        selection: undefined
      },
      session_id: request.session_id
    };
    
    return new Promise((resolve, reject) => {
      let finalResponse: ChatResponse | null = null;
      
      this.chatStream(
        patentRequest,
        () => {}, // Don't need chunks for non-streaming version
        (response) => {
          resolve(response);
        },
        (error) => {
          reject(error);
        }
      );
    });
  }

  /**
   * Check if the backend is healthy and accessible
   */
  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${this.baseURL}/`, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${getAccessToken() || ''}`,
        },
      });
      return response.ok;
    } catch (error) {
      console.warn('Health check failed:', error);
      return false;
    }
  }

  /**
   * Get backend status and version information
   */
  async getBackendStatus(): Promise<any> {
    try {
      const response = await this.api.get('/');
      return response.data;
    } catch (error) {
      console.warn('Failed to get backend status:', error);
      return null;
    }
  }

  /**
   * List all active sessions
   */
  async getSessions(): Promise<any> {
    try {
      const response = await this.api.get('/api/sessions');
      return response.data;
    } catch (error) {
      console.warn('Failed to get sessions:', error);
      return null;
    }
  }

  /**
   * Get detailed information about a specific session
   */
  async getSessionDetails(sessionId: string): Promise<any> {
    try {
      const response = await this.api.get(`/api/debug/session/${sessionId}`);
      return response.data;
    } catch (error) {
      console.warn('Failed to get session details:', error);
      return null;
    }
  }
}

export const apiService = new ApiService();
export default apiService;
