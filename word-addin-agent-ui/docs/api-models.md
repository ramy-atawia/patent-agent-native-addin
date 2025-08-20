# API Models

## Overview

This document provides comprehensive documentation of all TypeScript interfaces, data structures, request/response schemas, and validation rules used throughout the Patent Drafting Agent Word Add-in.

## Core Data Models

### 1. Chat & Messaging

**ChatMessage Interface**
```typescript
export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: string;
}
```

**Properties**:
- `role`: Identifies the message sender (user or AI assistant)
- `content`: The actual message text content
- `timestamp`: ISO 8601 timestamp of when the message was created

**Usage Examples**:
```typescript
// User message
const userMessage: ChatMessage = {
  role: 'user',
  content: 'Please draft a patent claim for my invention',
  timestamp: new Date().toISOString()
};

// Assistant message
const assistantMessage: ChatMessage = {
  role: 'assistant',
  content: 'I\'ll help you draft a patent claim. Here\'s what I understand...',
  timestamp: new Date().toISOString()
};
```

**ChatRequest Interface**
```typescript
export interface ChatRequest {
  disclosure: string;
  session_id?: string | null;
}
```

**Properties**:
- `disclosure`: The patent disclosure text or user query
- `session_id`: Optional session identifier for conversation continuity

**Usage Examples**:
```typescript
const request: ChatRequest = {
  disclosure: 'A method for processing data using machine learning algorithms',
  session_id: 'session_12345'
};
```

### 2. API Responses

**RunResponse Interface**
```typescript
export interface RunResponse {
  run_id: string;
  session_id: string;
}
```

**Properties**:
- `run_id`: Unique identifier for the current AI processing run
- `session_id`: Session identifier for tracking and continuity

**Usage Examples**:
```typescript
const runResponse: RunResponse = {
  run_id: 'run_67890',
  session_id: 'session_12345'
};
```

**ChatResponse Interface**
```typescript
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
  };
  session_id?: string;
}
```

**Properties**:
- `response`: The complete AI-generated response text
- `metadata`: AI processing metadata and decisions
- `data`: Optional structured data (e.g., generated claims)
- `session_id`: Session identifier for the response

**Usage Examples**:
```typescript
const chatResponse: ChatResponse = {
  response: 'Based on your disclosure, I recommend the following patent claim...',
  metadata: {
    should_draft_claims: true,
    has_claims: true,
    reasoning: 'The disclosure contains sufficient technical detail for claim drafting'
  },
  data: {
    claims: [
      '1. A method for processing data, comprising: receiving input data...',
      '2. The method of claim 1, further comprising: applying machine learning...'
    ],
    num_claims: 2
  },
  session_id: 'session_12345'
};
```

### 3. Streaming & Events

**StreamEvent Interface**
```typescript
export interface StreamEvent {
  event: 'status' | 'reasoning' | 'tool_call' | 'tool_result' | 'final' | 'done';
  data: any;
}
```

**Event Types**:
- `status`: Processing status updates
- `reasoning`: AI reasoning and decision-making
- `tool_call`: AI tool usage information
- `tool_result`: Results from AI tool operations
- `final`: Final response delivery
- `done`: Stream completion signal

**Usage Examples**:
```typescript
const statusEvent: StreamEvent = {
  event: 'status',
  data: { message: 'Analyzing patent disclosure...', progress: 25 }
};

const reasoningEvent: StreamEvent = {
  event: 'reasoning',
  data: { thought: 'This disclosure appears to be a software invention...' }
};
```

### 4. Document Operations

**DocumentChange Interface**
```typescript
export interface DocumentChange {
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

**Properties**:
- `type`: The type of document operation
- `content`: The content to insert or replace
- `location`: Where in the document to perform the operation
- `target_text`: Text to replace (for replace operations)
- `formatting`: Optional formatting to apply

**Usage Examples**:
```typescript
// Insert operation
const insertChange: DocumentChange = {
  type: 'insert',
  content: 'New patent claim text',
  location: 'end',
  formatting: {
    bold: true,
    italic: false
  }
};

// Replace operation
const replaceChange: DocumentChange = {
  type: 'replace',
  content: 'Improved claim text',
  location: 'specific',
  target_text: 'Old claim text'
};
```

**WordFormatting Interface**
```typescript
export interface WordFormatting {
  bold?: boolean;
  italic?: boolean;
  color?: string;
  fontSize?: number;
  fontName?: string;
}
```

**Properties**:
- `bold`: Bold text formatting
- `italic`: Italic text formatting
- `color`: Text color (hex or named color)
- `fontSize`: Font size in points
- `fontName`: Font family name

**Usage Examples**:
```typescript
const formatting: WordFormatting = {
  bold: true,
  color: '#0000FF',
  fontSize: 12,
  fontName: 'Calibri'
};
```

**DocumentContent Interface**
```typescript
export interface DocumentContent {
  text: string;
  paragraphs: string[];
  selection?: {
    text: string;
    start: number;
    end: number;
  };
}
```

**Properties**:
- `text`: Complete document text content
- `paragraphs`: Array of document paragraphs
- `selection`: Optional current text selection information

**Usage Examples**:
```typescript
const docContent: DocumentContent = {
  text: 'Complete document text content...',
  paragraphs: [
    'First paragraph content',
    'Second paragraph content',
    'Third paragraph content'
  ],
  selection: {
    text: 'selected text',
    start: 10,
    end: 25
  }
};
```

## Error Handling Models

### 1. API Error Interface

**ApiError Interface**
```typescript
export interface ApiError {
  message: string;
  code?: string;
  details?: any;
}
```

**Properties**:
- `message`: Human-readable error message
- `code`: Error code for programmatic handling
- `details`: Additional error details and context

**Usage Examples**:
```typescript
const apiError: ApiError = {
  message: 'Authentication failed. Please log in again.',
  code: 'AUTH_401',
  details: {
    token_expiry: '2024-01-15T10:30:00Z',
    required_action: 'refresh_token'
  }
};
```

**Error Types**:
```typescript
// Common error codes
const ErrorCodes = {
  NETWORK_ERROR: 'NETWORK_ERROR',
  AUTHENTICATION_ERROR: 'AUTH_ERROR',
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  SERVER_ERROR: 'SERVER_ERROR',
  UNKNOWN_ERROR: 'UNKNOWN_ERROR'
} as const;
```

### 2. Error Handling Methods

**Error Handling Implementation**
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

## Authentication Models

### 1. User Authentication

**User Interface (from Auth0)**
```typescript
interface User {
  sub: string;
  name?: string;
  given_name?: string;
  family_name?: string;
  nickname?: string;
  picture?: string;
  email?: string;
  email_verified?: boolean;
  updated_at?: string;
}
```

**Properties**:
- `sub`: Unique user identifier
- `name`: Full user name
- `given_name`: First name
- `family_name`: Last name
- `nickname`: User nickname
- `picture`: Profile picture URL
- `email`: User email address
- `email_verified`: Email verification status
- `updated_at`: Last update timestamp

**AuthContextType Interface**
```typescript
interface AuthContextType {
  isAuthenticated: boolean;
  token: string | null;
  user: User | null;
  loginWithRedirect: () => Promise<void>;
  handleRedirectCallback: () => Promise<void>;
  logout: () => void;
  loading: boolean;
  refreshFromStorage: () => void;
}
```

**Properties**:
- `isAuthenticated`: Current authentication status
- `token`: Current authentication token
- `user`: Current user information
- `loginWithRedirect`: Login method
- `handleRedirectCallback`: Handle authentication callback
- `logout`: Logout method
- `loading`: Authentication loading state
- `refreshFromStorage`: Refresh authentication from storage

## Context & State Models

### 1. Conversation Context

**ConversationContextType Interface**
```typescript
interface ConversationContextType {
  messages: ChatMessage[];
  sessionId: string | null;
  addMessage: (message: ChatMessage) => void;
  clearConversation: () => void;
  clearMessages: () => void;
  getConversationHistory: () => ChatMessage[];
  updateSessionId: (sessionId: string) => void;
}
```

**Properties**:
- `messages`: Array of conversation messages
- `sessionId`: Current session identifier
- `addMessage`: Add new message to conversation
- `clearConversation`: Clear entire conversation
- `clearMessages`: Clear messages only
- `getConversationHistory`: Get conversation history
- `updateSessionId`: Update session identifier

### 2. Word.js Hook Models

**UseWordJsReturn Interface**
```typescript
interface UseWordJsReturn {
  isReady: boolean;
  isLoading: boolean;
  error: string | null;
  execute: <T>(operation: () => Promise<T>) => Promise<T | null>;
}
```

**Properties**:
- `isReady`: Word.js ready status
- `isLoading`: Word.js loading status
- `error`: Any error messages
- `execute`: Safe execution method for Word.js operations

## Service Layer Models

### 1. API Service Models

**ApiService Class Structure**
```typescript
class ApiService {
  private api: AxiosInstance;
  private baseURL: string;

  constructor() {
    this.baseURL = API_URL;
    this.api = axios.create({
      baseURL: this.baseURL,
      timeout: 30000,
    });
  }

  // Methods
  async startPatentRun(request: ChatRequest): Promise<RunResponse>;
  async chatStream(request: ChatRequest, ...): Promise<void>;
  async chat(request: {...}): Promise<ChatResponse>;
  async getDocumentAnalysis(documentContent: string): Promise<any>;
  async applyDocumentChanges(changes: DocumentChange[]): Promise<void>;
  async healthCheck(): Promise<boolean>;
  async getBackendStatus(): Promise<any>;
  async getSessions(): Promise<any>;
  async getSessionDetails(sessionId: string): Promise<any>;
}
```

### 2. Document Service Models

**DocumentService Class Structure**
```typescript
class DocumentService {
  async getDocumentContent(): Promise<DocumentContent>;
  async getSelection(): Promise<DocumentContent['selection']>;
  async insertText(text: string, formatting?: WordFormatting): Promise<void>;
  async replaceText(text: string, formatting?: WordFormatting): Promise<void>;
  async deleteText(): Promise<void>;
  async applyFormatting(formatting: WordFormatting): Promise<void>;
  async getDocumentInfo(): Promise<any>;
  async saveDocument(): Promise<void>;
}
```

## Validation Rules

### 1. Input Validation

**Chat Request Validation**
```typescript
const validateChatRequest = (request: ChatRequest): boolean => {
  // Disclosure must not be empty
  if (!request.disclosure || request.disclosure.trim().length === 0) {
    return false;
  }

  // Disclosure must not exceed maximum length
  if (request.disclosure.length > 10000) {
    return false;
  }

  // Session ID must be valid format if provided
  if (request.session_id && !/^[a-zA-Z0-9_-]+$/.test(request.session_id)) {
    return false;
  }

  return true;
};
```

**Document Change Validation**
```typescript
const validateDocumentChange = (change: DocumentChange): boolean => {
  // Type must be valid
  if (!['insert', 'replace', 'delete'].includes(change.type)) {
    return false;
  }

  // Content must not be empty for insert/replace
  if (['insert', 'replace'].includes(change.type) && 
      (!change.content || change.content.trim().length === 0)) {
    return false;
  }

  // Location must be valid
  if (!['start', 'end', 'specific'].includes(change.location)) {
    return false;
  }

  // Target text required for replace operations
  if (change.type === 'replace' && !change.target_text) {
    return false;
  }

  return true;
};
```

### 2. Type Guards

**Type Guard Functions**
```typescript
// Check if object is ChatMessage
export const isChatMessage = (obj: any): obj is ChatMessage => {
  return obj && 
         typeof obj.role === 'string' && 
         ['user', 'assistant'].includes(obj.role) &&
         typeof obj.content === 'string';
};

// Check if object is ChatResponse
export const isChatResponse = (obj: any): obj is ChatResponse => {
  return obj && 
         typeof obj.response === 'string' &&
         obj.metadata &&
         typeof obj.metadata.should_draft_claims === 'boolean' &&
         typeof obj.metadata.has_claims === 'boolean' &&
         typeof obj.metadata.reasoning === 'string';
};

// Check if object is ApiError
export const isApiError = (obj: any): obj is ApiError => {
  return obj && typeof obj.message === 'string';
};
```

## Data Transformation Models

### 1. Request Transformation

**Legacy to New Format Conversion**
```typescript
const convertLegacyRequest = (legacyRequest: {
  message: string;
  document_content?: string;
  session_id?: string | null;
  conversation_history?: ChatMessage[];
}): ChatRequest => {
  let disclosure = legacyRequest.message;
  
  // Add document content if available
  if (legacyRequest.document_content) {
    disclosure += `\n\nDocument context: ${legacyRequest.document_content}`;
  }
  
  // Add conversation history if available
  if (legacyRequest.conversation_history && legacyRequest.conversation_history.length > 0) {
    const historyContext = legacyRequest.conversation_history
      .map(msg => `${msg.role}: ${msg.content}`)
      .join('\n');
    disclosure += `\n\nConversation history:\n${historyContext}`;
  }
  
  return {
    disclosure,
    session_id: legacyRequest.session_id
  };
};
```

### 2. Response Transformation

**Stream Response Processing**
```typescript
const processStreamResponse = (parsed: any, runResponse: RunResponse): ChatResponse => {
  return {
    response: parsed.response,
    metadata: parsed.metadata || {
      should_draft_claims: false,
      has_claims: false,
      reasoning: ''
    },
    data: parsed.data,
    session_id: runResponse.session_id
  };
};
```

## Future Model Extensions

### 1. Enhanced Patent Models

**Patent Claim Models**
```typescript
interface PatentClaim {
  claimNumber: number;
  claimText: string;
  claimType: 'independent' | 'dependent';
  dependency?: string;
  scope: 'broad' | 'narrow' | 'medium';
  validity: 'strong' | 'moderate' | 'weak';
}

interface PatentSpecification {
  title: string;
  abstract: string;
  background: string;
  summary: string;
  detailedDescription: string;
  claims: PatentClaim[];
  drawings: string[];
}
```

**Patent Analysis Models**
```typescript
interface PatentAnalysis {
  novelty: 'novel' | 'not_novel' | 'uncertain';
  obviousness: 'non_obvious' | 'obvious' | 'uncertain';
  enablement: 'enabled' | 'not_enabled' | 'uncertain';
  writtenDescription: 'adequate' | 'inadequate' | 'uncertain';
  recommendations: string[];
  priorArt: string[];
}
```

### 2. Collaboration Models

**User Collaboration Models**
```typescript
interface CollaborationSession {
  sessionId: string;
  participants: User[];
  documentId: string;
  permissions: CollaborationPermissions;
  changes: DocumentChange[];
  comments: Comment[];
}

interface Comment {
  id: string;
  author: User;
  content: string;
  timestamp: string;
  location: DocumentLocation;
  replies: Comment[];
}
```

## Model Usage Guidelines

### 1. Best Practices

**Interface Usage**
- Always use interfaces for data contracts
- Prefer composition over inheritance
- Use optional properties for non-required fields
- Provide default values where appropriate

**Type Safety**
- Use strict TypeScript configuration
- Implement proper type guards
- Validate data at runtime
- Handle undefined/null cases gracefully

**Performance Considerations**
- Use efficient data structures
- Minimize object creation
- Implement proper cleanup
- Monitor memory usage

### 2. Migration Guidelines

**Version Compatibility**
- Maintain backward compatibility
- Use versioned interfaces
- Implement migration functions
- Provide deprecation warnings

**Breaking Changes**
- Document all breaking changes
- Provide migration guides
- Maintain multiple versions
- Gradual rollout strategy

---

*These API models provide a comprehensive foundation for the Patent Drafting Agent Word Add-in. They ensure type safety, data consistency, and maintainable code structure.*
