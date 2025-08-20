# API Reference

## Overview

The Patent Drafting Agent integrates with a backend AI service that provides patent drafting capabilities through RESTful APIs and Server-Sent Events (SSE) for real-time streaming responses.

## Base Configuration

### Environment Variables
```typescript
// src/config/environment.ts
export const API_URL = env.API_URL; // Default: http://localhost:8000
export const NODE_ENV = env.NODE_ENV; // 'development' | 'production'
```

### API Endpoints
- **Base URL**: `http://localhost:8000` (development) / `https://your-production-api.com` (production)
- **Protocol**: HTTPS required for production, HTTP allowed for local development
- **Authentication**: Bearer token authentication required for all endpoints

## Core API Service

### ApiService Class

The main API service class handles all backend communication with built-in authentication, error handling, and retry logic.

#### Constructor
```typescript
class ApiService {
  private api: AxiosInstance;
  private baseURL: string;
  
  constructor() {
    this.baseURL = API_URL;
    this.api = axios.create({
      baseURL: this.baseURL,
      timeout: 30000, // 30 second timeout
    });
  }
}
```

#### Authentication Interceptor
```typescript
// Automatic token injection for all requests
this.api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem('auth0_access_token') || 
                sessionStorage.getItem('auth_token') || 
                localStorage.getItem('auth_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

## Patent Drafting API

### Start Patent Run

**Endpoint**: `POST /api/patent/run`

**Purpose**: Initiates a new patent drafting session with the AI backend.

**Request**:
```typescript
interface ChatRequest {
  disclosure: string;        // Patent disclosure text
  session_id?: string | null; // Optional session ID for continuity
}
```

**Response**:
```typescript
interface RunResponse {
  run_id: string;      // Unique identifier for this run
  session_id: string;  // Session identifier for tracking
}
```

**Example**:
```typescript
const runResponse = await apiService.startPatentRun({
  disclosure: "A method for processing data...",
  session_id: "existing-session-123"
});
```

### Stream Patent Response

**Endpoint**: `GET /api/patent/stream?run_id={run_id}`

**Purpose**: Streams real-time AI responses using Server-Sent Events (SSE).

**Parameters**:
- `run_id`: The run ID returned from `startPatentRun`

**Response Format**: Server-Sent Events with JSON payloads

**Event Types**:
```typescript
interface StreamEvent {
  event: 'status' | 'reasoning' | 'tool_call' | 'tool_result' | 'final' | 'done';
  data: any;
}
```

**Usage**:
```typescript
await apiService.chatStream(
  request,
  (chunk: string) => {
    // Handle streaming chunks
    setStreamingResponse(chunk);
  },
  (response: ChatResponse) => {
    // Handle complete response
    addMessage(response);
  },
  (error: Error) => {
    // Handle errors
    console.error('Stream error:', error);
  },
  abortController.signal
);
```

## Data Models

### Chat Message
```typescript
interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}
```

### Chat Response
```typescript
interface ChatResponse {
  response: string;                    // AI-generated response
  metadata: {
    should_draft_claims: boolean;      // Whether to generate patent claims
    has_claims: boolean;               // Whether claims were generated
    reasoning: string;                 // AI reasoning for the response
  };
  data?: {
    claims?: string[];                 // Generated patent claims
    num_claims?: number;               // Number of claims generated
  };
  session_id?: string;                 // Session identifier
}
```

### Document Changes
```typescript
interface DocumentChange {
  type: 'insert' | 'replace' | 'delete';
  content: string;
  location: 'start' | 'end' | 'specific';
  target_text?: string;
  formatting?: {
    bold?: boolean;
    italic?: boolean;
    color?: string;
  };
}
```

## Error Handling

### ApiError Interface
```typescript
interface ApiError {
  message: string;      // Human-readable error message
  code?: string;        // Error code for programmatic handling
  details?: any;        // Additional error details
}
```

### Error Types
- **Server Errors**: HTTP 4xx/5xx responses with detailed error messages
- **Network Errors**: Connection failures, timeouts, and network issues
- **Authentication Errors**: Invalid or expired tokens
- **Validation Errors**: Invalid request data or parameters

### Error Handling Methods
```typescript
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
```

## Streaming Implementation

### Server-Sent Events Processing
```typescript
async chatStream(
  request: ChatRequest,
  onChunk: (chunk: string) => void,
  onComplete: (response: ChatResponse) => void,
  onError: (error: Error) => void,
  signal?: AbortSignal
): Promise<void>
```

**Features**:
- Real-time streaming of AI responses
- Abort controller support for cancellation
- Automatic error handling and recovery
- Efficient buffer management for large responses

**Stream Processing**:
1. Parse incoming SSE data
2. Handle different event types
3. Accumulate response chunks
4. Trigger completion callback
5. Handle errors gracefully

## Session Management

### Session Endpoints

#### List Sessions
**Endpoint**: `GET /api/sessions`

**Purpose**: Retrieve all active sessions for the authenticated user.

#### Get Session Details
**Endpoint**: `GET /api/debug/session/{sessionId}`

**Purpose**: Get detailed information about a specific session.

### Session Persistence
- Sessions are maintained across browser sessions
- Session IDs are automatically managed by the backend
- Conversation history is preserved within sessions

## Health Check & Status

### Health Check
**Endpoint**: `GET /`

**Purpose**: Verify backend availability and health status.

**Response**: HTTP 200 OK if healthy

### Backend Status
**Endpoint**: `GET /`

**Purpose**: Get backend version and status information.

## Rate Limiting & Quotas

### Current Limitations
- No explicit rate limiting implemented
- Backend may enforce limits based on user tier
- Streaming connections have timeout limits (30 seconds)

### Best Practices
- Implement exponential backoff for retries
- Cache responses when appropriate
- Monitor API usage and implement client-side throttling

## Security Considerations

### Authentication
- All API calls require valid JWT tokens
- Tokens are automatically refreshed via Auth0
- Session-based authentication for long-running operations

### Data Privacy
- All communication uses HTTPS in production
- Sensitive data is not logged or stored locally
- User data is handled according to privacy policies

### CORS Configuration
- Backend must allow requests from the add-in domain
- Credentials are included in all requests
- Preflight requests are handled automatically

## Testing & Development

### Development Mode
- Local development uses HTTP endpoints
- CORS is relaxed for local development
- Mock responses can be enabled for testing

### Testing Endpoints
- Health check endpoint for connectivity testing
- Session endpoints for debugging
- Error simulation endpoints for testing error handling

## Future API Enhancements

### Planned Features
- **WebSocket Support**: Real-time bidirectional communication
- **Batch Operations**: Multiple patent operations in single request
- **File Upload**: Direct document upload and analysis
- **Collaboration**: Multi-user editing and review features

### API Versioning
- Current version: v1 (implicit)
- Future versions will use explicit versioning
- Backward compatibility will be maintained

---

*This API reference covers the current implementation. For the latest updates and additional endpoints, refer to the backend API documentation.*
