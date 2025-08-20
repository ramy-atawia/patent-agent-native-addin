# API Reference

Complete API documentation for the Agentic Native Drafting Service.

## 🔗 Base Information

- **Base URL**: `http://127.0.0.1:8000`
- **API Version**: 1.0
- **Content Type**: `application/json`
- **Streaming**: Server-Sent Events (SSE)

## 📋 API Endpoints

### **Health Check**

#### `GET /`
Returns service status and available functions.

**Response:**
```json
{
  "service": "Simple Patent Drafting Service",
  "version": "1.0",
  "functions": ["draft_claims", "general_conversation"],
  "status": "operational"
}
```

---

### **Patent Drafting**

#### `POST /api/patent/run`
Start a new patent drafting run or continue an existing session.

**Request Body:**
```json
{
  "disclosure": "string (required)",
  "session_id": "string (optional)"
}
```

**Parameters:**
- `disclosure` (required): Description of the invention or user request
- `session_id` (optional): Existing session ID to continue

**Response:**
```json
{
  "run_id": "uuid-string",
  "session_id": "uuid-string"
}
```

**Example Request:**
```bash
curl -X POST "http://127.0.0.1:8000/api/patent/run" \
  -H "Content-Type: application/json" \
  -d '{
    "disclosure": "Please draft patent claims for my AI-powered quantum computing system",
    "session_id": "optional-existing-session-id"
  }'
```

**Example Response:**
```json
{
  "run_id": "a12997b6-61f7-4a23-ac63-32435740877a",
  "session_id": "6e8ab42e-2ada-4c23-9fca-25a0ef81544f"
}
```

---

### **Streaming Response**

#### `GET /api/patent/stream?run_id={run_id}`
Stream the agent's response using Server-Sent Events (SSE).

**Parameters:**
- `run_id` (required): The run ID from the `/api/patent/run` endpoint

**Response Format:**
```
event: status
data: {"status": "processing", "message": "Analyzing your request..."}

event: reasoning
data: {"reasoning": "Executing claim_drafting (confidence: 0.95)..."}

event: tool_call
data: {"tool": "draft_claims", "parameters": {...}}

event: tool_result
data: {"result": "Generated 3 patent claims..."}

event: final
data: {"response": "I've drafted 3 patent claims...", "metadata": {...}}

event: done
data: {}
```

**Example Usage:**
```javascript
const eventSource = new EventSource('/api/patent/stream?run_id=a12997b6-61f7-4a23-ac63-32435740877a');

eventSource.onmessage = function(event) {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

eventSource.addEventListener('status', function(event) {
  console.log('Status:', JSON.parse(event.data));
});

eventSource.addEventListener('final', function(event) {
  const data = JSON.parse(event.data);
  console.log('Final response:', data.response);
  eventSource.close();
});
```

---

### **Session Management**

#### `GET /api/sessions`
List all active sessions.

**Response:**
```json
{
  "total_sessions": 3,
  "sessions": [
    {
      "session_id": "6e8ab42e-2ada-4c23-9fca-25a0ef81544f",
      "started_at": "2024-08-17T01:08:15.123456",
      "topic": "AI-powered quantum computing system...",
      "total_runs": 2,
      "last_run": "a12997b6-61f7-4a23-ac63-32435740877a"
    }
  ]
}
```

---

### **Debug & Development**

#### `GET /api/debug/session/{session_id}`
Get detailed information about a specific session.

**Parameters:**
- `session_id` (path): The session ID to inspect

**Response:**
```json
{
  "session_id": "6e8ab42e-2ada-4c23-9fca-25a0ef81544f",
  "started_at": "2024-08-17T01:08:15.123456",
  "topic": "AI-powered quantum computing system...",
  "runs": [
    "a12997b6-61f7-4a23-ac63-32435740877a",
    "b234c8d7-72g8-5b34-bd74-43546851988b"
  ],
  "session_history": "User: Please draft patent claims...\nAgent: I've drafted 3 patent claims...\n---\nUser: Review those claims...\nAgent: I've reviewed your claims..."
}
```

---

## 🔄 Data Flow

### **Complete Workflow Example**

1. **Start Session**
   ```bash
   POST /api/patent/run
   {
     "disclosure": "Draft claims for my blockchain invention"
   }
   ```

2. **Get Response**
   ```bash
   GET /api/patent/stream?run_id={run_id}
   ```

3. **Continue Session**
   ```bash
   POST /api/patent/run
   {
     "disclosure": "Review those claims",
     "session_id": "{session_id}"
   }
   ```

4. **Monitor Sessions**
   ```bash
   GET /api/sessions
   GET /api/debug/session/{session_id}
   ```

---

## 📊 Response Metadata

### **Final Response Structure**
```json
{
  "response": "string",
  "metadata": {
    "should_draft_claims": "boolean",
    "has_claims": "boolean",
    "reasoning": "string"
  },
  "data": {
    "claims": ["array of claim strings"],
    "num_claims": "number"
  }
}
```

### **Metadata Fields**
- `should_draft_claims`: Whether the system should generate claims
- `has_claims`: Whether the response contains patent claims
- `reasoning`: LLM's reasoning for the chosen action
- `data.claims`: Array of generated patent claims
- `data.num_claims`: Number of claims generated

---

## ⚠️ Error Handling

### **HTTP Status Codes**
- `200 OK`: Request successful
- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### **Error Response Format**
```json
{
  "detail": "Error description"
}
```

### **Common Error Scenarios**
- Missing `disclosure` parameter
- Invalid `session_id`
- Server startup issues
- LLM service unavailability

---

## 🚀 Best Practices

### **Request Optimization**
1. **Clear Descriptions**: Provide detailed invention descriptions
2. **Session Continuity**: Use `session_id` for multi-turn conversations
3. **Explicit Intent**: Use clear language for drafting/review requests

### **Response Handling**
1. **Stream Processing**: Handle SSE events sequentially
2. **Error Recovery**: Implement retry logic for failed requests
3. **Session Management**: Track session IDs for context continuity

### **Performance Tips**
1. **Connection Reuse**: Maintain HTTP connections when possible
2. **Event Handling**: Process streaming events efficiently
3. **Memory Management**: Close unused event sources

---

## 🔧 Testing

### **Test Endpoints**
```bash
# Health check
curl "http://127.0.0.1:8000/"

# Start session
curl -X POST "http://127.0.0.1:8000/api/patent/run" \
  -H "Content-Type: application/json" \
  -d '{"disclosure": "Test invention"}'

# List sessions
curl "http://127.0.0.1:8000/api/sessions"
```

### **Integration Testing**
Use the provided test suites in `tests/regression/` for comprehensive testing:
- `test_confidence_threshold.py`
- `test_draft_claims_regression.py`
- `test_review_claims_regression.py`
- `test_session_regression.py`
- `test_conversation_memory.py`

---

## 📝 Changelog

### **Version 1.0 (August 17, 2024)**
- ✅ Initial API implementation
- ✅ Session management system
- ✅ LLM-based intent classification
- ✅ Confidence threshold system
- ✅ Comprehensive test suite
- ✅ Production-ready deployment

---

**Next**: Read the [Architecture Overview](architecture.md) to understand the system design.
