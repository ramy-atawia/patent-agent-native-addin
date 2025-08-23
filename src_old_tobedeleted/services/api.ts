import axios, { AxiosInstance } from 'axios';
import { API_URL } from '../config/environment';
import { getAccessToken } from './authTokenStore';

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
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
  response: string;  // Changed from 'conversation_response' to 'response'
  metadata: {
    should_draft_claims: boolean;
    has_claims: boolean;
    reasoning: string;
  };
  data?: {
    claims?: string[];
    num_claims?: number;
  };
  session_id?: string;
}

// Prior art search types (simplified E2E structure)
export interface PriorArtPatent {
  patent_number: string;
  title: string;
  abstract: string;
  summary: string;
  relevance_score: number;
  grant_date?: string;
  inventors?: string[];
  assignees?: string[];
  cpc_classifications?: string[];
  claims?: string[];
}

export interface PriorArtResults {
  query: string;
  total_found: number;
  patents?: PriorArtPatent[]; // optional; backend now returns a single markdown results string
  overall_summary?: string;
}

export interface PriorArtResponse {
  results: string; // markdown string
  thought_process: string; // markdown string
}

export interface StreamEvent {
  event: 'thoughts' | 'results' | 'done' | 'error';
  data: any;
}

// DocumentChange interface removed - not supported by backend

export interface ApiError {
  message: string;
  code?: string;
  details?: any;
}

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
      // Use in-memory token store (no browser storage in artifact environments)
      const token = getAccessToken();
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });
  }

  private handleApiError(error: any): ApiError {
    if (error.response) {
      // Server responded with error status
      return {
        message: error.response.data?.message || `Server error: ${error.response.status}`,
        code: error.response.status.toString(),
        details: error.response.data
      };
    } else if (error.request) {
      // Request made but no response
      return {
        message: 'No response from server. Please check your connection.',
        code: 'NETWORK_ERROR'
      };
    } else {
      // Something else happened
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
   * Prior art search
   * Returns the simplified { results, thought_process } structure from the backend
   */
  async priorArtSearch(request: Partial<ChatRequest>): Promise<PriorArtResponse> {
    try {
      const response = await this.api.post('/api/patent/prior-art', request);
      return response.data as PriorArtResponse;
    } catch (error) {
      throw this.handleApiError(error);
    }
  }

  /**
   * Stream the agent's response using Server-Sent Events (SSE)
   */
  async chatStream(
    request: ChatRequest,
    onChunk: (chunk: string) => void,
    onComplete: (response: ChatResponse) => void,
    onError: (error: Error) => void,
    signal?: AbortSignal
  ): Promise<void> {
    try {
      // First, start the patent run
      const runResponse = await this.startPatentRun(request);
      
      // Then stream the response
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
            // Track the current event type
            currentEventType = line.slice(7).trim();
            console.log('SSE Event:', currentEventType);
          } else if (line.startsWith('data: ')) {
            const content = line.slice(6); // Remove 'data: ' prefix
            
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
              
              // Handle different event types for real-time streaming
              console.log(`🔍 Processing event: ${currentEventType}`, { parsed, currentEventType });
              
              // ✅ Simplified - just 2 types: thoughts and results!
              if (currentEventType === 'results') {
                // Final results with complete content
                console.log('🎯 Processing results event:', parsed);
                finalResponse = {
                  response: parsed.response,
                  metadata: parsed.metadata || {
                    should_draft_claims: false,
                    has_claims: false,
                    reasoning: ''
                  },
                  data: parsed.data,
                  session_id: runResponse.session_id
                };
                
                // Log the actual metadata from backend for debugging
                console.log('🔍 Backend metadata received:', parsed.metadata);
                console.log('🔍 Final response structure:', finalResponse);
                
                // Stream the final results content
                onChunk(parsed.response);
              } else if (currentEventType === 'error') {
                // Handle errors
                console.log('❌ Processing error event:', parsed);
                onChunk(`❌ Error: ${parsed.error || 'Unknown error occurred'}`);
              } else {
                // Everything else is a "thought" - reasoning, progress, etc.
                console.log(`💭 Processing thought event (${currentEventType}):`, parsed);
                
                // Extract text from different data structures
                const thoughtText = parsed.text || 
                                   parsed.message || 
                                   (parsed.tool ? `Tool: ${parsed.tool}` : '') ||
                                   'Processing...';
                
                onChunk(thoughtText);
              }
            } catch (e) {
              console.warn('Failed to parse streaming data:', e);
            }
          }
        }
      }
    } catch (error) {
      onError(error as Error);
    }
  }

  /**
   * Legacy method for backward compatibility - now uses the patent API
   */
  async chat(request: { message: string; document_content?: string; session_id?: string | null; conversation_history?: ChatMessage[] }): Promise<ChatResponse> {
    // Convert old format to new format
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
    
    const runResponse = await this.startPatentRun(patentRequest);
    
    return new Promise((resolve, reject) => {
      let finalResponse: ChatResponse | null = null;
      
      this.chatStream(
        patentRequest,
        () => {}, // Don't need chunks for non-streaming version
        (response) => {
          finalResponse = response;
          resolve(response);
        },
        (error) => {
          reject(error);
        }
      );
    });
  }

  // Document analysis and changes removed - not supported by backend

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
