# Integration Guide: Word Add-in with Backend Services

This guide explains how the Patent Drafting Agent Word Add-in integrates with the backend services in the `agentic-native-drafting` project.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Word Document                           │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Office.js API                           │   │
│  │  • Document content extraction                          │   │
│  │  • Text insertion and formatting                       │   │
│  │  • Track changes management                            │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Word Add-in (React)                        │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Frontend Components                     │   │
│  │  • ChatBot: AI conversation interface                  │   │
│  │  • DocumentPanel: Document analysis tools              │   │
│  │  • MessageBubble: Individual chat messages             │   │
│  │  • InsertButton: Document insertion controls           │   │
│  └─────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Services Layer                          │   │
│  │  • API Service: Backend communication                  │   │
│  │  • Document Service: Word operations                   │   │
│  │  • Context Providers: State management                 │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Backend API (FastAPI)                      │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                 Patent Agent                            │   │
│  │  • LLM Integration (Azure OpenAI)                      │   │
│  │  • Patent claim generation                              │   │
│  │  • Document analysis                                    │   │
│  │  • Conversation management                              │   │
│  └─────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

## API Integration Points

### 1. Chat Endpoint (`/chat`)

**Purpose**: Handle regular chat requests with the patent agent

**Request Format**:
```typescript
interface ChatRequest {
  message: string;                    // User's message
  document_content?: string;          // Current document content
  session_id?: string;               // Conversation session ID
  conversation_history?: ChatMessage[]; // Previous messages
}
```

**Response Format**:
```typescript
interface ChatResponse {
  conversation_response: string;       // AI response
  reasoning: string;                  // AI reasoning
  should_draft_claims: boolean;       // Whether to generate claims
  claims?: string[];                  // Generated patent claims
  review_comments?: ReviewComment[];  // Document review feedback
  structured_claims?: PatentClaim[];  // Structured claim data
}
```

### 2. Streaming Endpoint (`/chat/stream`)

**Purpose**: Provide real-time streaming responses for better UX

**Implementation**: Uses Server-Sent Events (SSE) for live streaming

**Stream Format**:
```
data: {"conversation_response": "Partial response..."}
data: {"conversation_response": "More content..."}
data: [DONE]
```

### 3. Document Analysis (`/analyze-document`)

**Purpose**: Analyze document content for patent-related insights

**Request Format**:
```typescript
{
  content: string;  // Document text content
}
```

### 4. Change Application (`/apply-changes`)

**Purpose**: Apply AI-suggested changes to the document

**Request Format**:
```typescript
{
  changes: DocumentChange[];  // Array of document modifications
}
```

## Data Flow

### 1. User Input → Backend Processing

```
User types message in ChatBot
    ↓
ChatBot extracts document content via DocumentService
    ↓
API request sent to backend with:
  - User message
  - Document content
  - Session ID
  - Conversation history
    ↓
Backend processes with LLM
    ↓
Response streamed back to frontend
```

### 2. AI Response → Document Integration

```
AI response received in ChatBot
    ↓
User clicks "Insert to Document"
    ↓
InsertButton triggers DocumentService
    ↓
DocumentService uses Office.js to:
  - Insert text at cursor/end
  - Apply formatting
  - Enable track changes
    ↓
Content appears in Word document
```

### 3. Session Management

```
Conversation starts
    ↓
Session ID generated by backend
    ↓
Frontend stores session ID in ConversationContext
    ↓
Subsequent requests include session ID
    ↓
Backend maintains conversation state
    ↓
Session persists until cleared
```

## Key Integration Features

### 1. Real-time Streaming

- **Frontend**: Uses `fetch` API with streaming response handling
- **Backend**: FastAPI streaming responses with SSE
- **Benefits**: Immediate feedback, better user experience

### 2. Document Context Awareness

- **Content Extraction**: Real-time document content reading
- **Context Preservation**: Document state maintained across requests
- **Smart Insertion**: Context-aware text placement

### 3. Authentication Integration

- **Bearer Token**: Stored in localStorage
- **Automatic Inclusion**: Added to all API requests
- **Session Persistence**: Maintains login state

### 4. Error Handling

- **Network Errors**: Graceful fallback with user feedback
- **API Errors**: Structured error responses
- **Office.js Errors**: Document operation error handling

## Configuration

### Environment Variables

```bash
# Backend API URL
REACT_APP_API_URL=http://localhost:8000

# Development settings
NODE_ENV=development
HTTPS=true
```

### Backend Requirements

Ensure the backend has these endpoints available:
- `POST /chat` - Regular chat
- `POST /chat/stream` - Streaming chat
- `POST /analyze-document` - Document analysis
- `POST /apply-changes` - Document modifications

## Testing Integration

### 1. Backend Connectivity

```bash
# Test if backend is running
curl http://localhost:8000/health

# Test chat endpoint
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello"}'
```

### 2. Frontend Development

```bash
# Start development server
npm run dev-server

# Start Word with add-in
npm start
```

### 3. Integration Testing

```bash
# Run tests
npm test

# Run tests with coverage
npm run test:coverage
```

## Troubleshooting

### Common Issues

1. **Backend Connection Failed**
   - Check if backend is running on correct port
   - Verify CORS settings in backend
   - Check network connectivity

2. **Office.js Not Loading**
   - Ensure add-in is properly sideloaded
   - Check manifest.xml configuration
   - Verify HTTPS requirements

3. **Streaming Not Working**
   - Check backend streaming implementation
   - Verify SSE support in browser
   - Check network proxy settings

### Debug Mode

Enable debugging in the add-in:

```typescript
// In browser console
Office.context.document.settings.set('Office.Debug', true);
```

## Performance Considerations

### 1. Memory Management

- **Conversation History**: Limited to prevent memory bloat
- **Document Content**: Chunked processing for large documents
- **Streaming**: Efficient handling of long responses

### 2. Network Optimization

- **Request Batching**: Multiple operations in single request
- **Caching**: Session data and document content caching
- **Compression**: Gzip compression for API responses

### 3. Office.js Optimization

- **Batch Operations**: Group multiple document changes
- **Async Processing**: Non-blocking document operations
- **Error Recovery**: Graceful handling of Office.js failures

## Security Considerations

### 1. Authentication

- **Token Storage**: Secure localStorage usage
- **Token Expiry**: Automatic token refresh
- **HTTPS Only**: Secure communication requirement

### 2. Data Privacy

- **Document Content**: Only sent when necessary
- **User Data**: Minimal data collection
- **API Security**: Rate limiting and validation

### 3. Office.js Security

- **Permissions**: Minimal required permissions
- **Content Validation**: Sanitize user inputs
- **Error Handling**: No sensitive data in error messages

## Future Enhancements

### 1. Advanced Features

- **Real-time Collaboration**: Multiple users editing
- **Version Control**: Document change tracking
- **AI Training**: User feedback integration

### 2. Performance Improvements

- **WebSocket Support**: Bidirectional communication
- **Offline Mode**: Local processing capabilities
- **Caching Strategy**: Intelligent data caching

### 3. Integration Extensions

- **Other Office Apps**: Excel, PowerPoint support
- **Cloud Storage**: OneDrive, SharePoint integration
- **Third-party APIs**: Patent office integrations
