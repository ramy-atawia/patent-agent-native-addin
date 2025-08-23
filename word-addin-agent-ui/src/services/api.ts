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

// Ultra-simplified event types - just what we actually need
export type EventType = 
  | 'thoughts'              // All AI thinking/reasoning/progress → Small streaming bubbles
  | 'results'               // Final results/completion → Large final bubble
  | 'error';                // Error states → Error handling

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
              
              // Simplified event handling - just thoughts and results
              switch (currentEventType) {
                case 'results':
                  // Final completion with results (new simplified backend)
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
                  onChunk(parsed.response || 'Process completed', 'results');
                  onComplete(finalResponse);
                  return;
                
                case 'complete':
                  // Legacy support for old backend events
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
                  onChunk(parsed.response || 'Process completed', 'results');
                  onComplete(finalResponse);
                  return;
                  
                case 'error':
                  const errorMsg = parsed.error || parsed.message || 'An error occurred';
                  onChunk(`❌ ${errorMsg}`, 'error');
                  onError(new Error(errorMsg));
                  return;
                  
                case 'low_confidence':
                  const clarificationMsg = parsed.message || 'I need more information to help you effectively.';
                  onChunk(`❓ ${clarificationMsg}`, 'low_confidence');
                  break;
                  
                default:
                  // Everything else is a "thought" - reasoning, progress, analysis, etc.
                  console.log(`� Processing thought event (${currentEventType}):`, parsed);
                  
                  // Extract the meaningful text content
                  const thoughtText = parsed.text || 
                                    parsed.content || 
                                    parsed.message || 
                                    `${currentEventType}: Processing...`;
                  
                  onChunk(thoughtText, 'thoughts');
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
