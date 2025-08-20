# Novitai Patent Drafting API Documentation

## 🚀 **Quick Start**

### **Access Interactive API Documentation**

1. **Start the backend server:**
   ```bash
   cd agentic_native_drafting
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uvicorn src.main:app --reload --port 8000
   ```

2. **Open interactive Swagger UI:**
   ```
   http://localhost:8000/docs
   ```

3. **Alternative ReDoc documentation:**
   ```
   http://localhost:8000/redoc
   ```

4. **OpenAPI JSON schema:**
   ```
   http://localhost:8000/openapi.json
   ```

## 📖 **Documentation Files**

### **1. Interactive Documentation (FastAPI Auto-Generated)**
- **Swagger UI**: `http://localhost:8000/docs` - Interactive API testing interface
- **ReDoc**: `http://localhost:8000/redoc` - Clean, readable documentation
- **OpenAPI JSON**: `http://localhost:8000/openapi.json` - Machine-readable schema

### **2. Static Documentation**
- **swagger.yaml**: Complete OpenAPI 3.0 specification with examples
- **This file**: Human-readable API overview and usage guide

## 🔗 **API Endpoints Overview**

### **Core Patent Drafting**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/patent/run` | Start patent drafting run |
| `GET` | `/api/patent/stream` | Stream real-time results |
| `GET` | `/api/patent/run/{run_id}` | Get run details |

### **Prior Art Research**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/patent/prior-art` | Search prior art |

### **Session Management**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/sessions` | List all sessions |

### **System & Debug**
| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Health check |
| `GET` | `/api/debug/env` | Environment check (dev only) |
| `GET` | `/api/debug/session/{id}` | Session debug (dev only) |

## 🛠 **Usage Examples**

### **1. Basic Patent Drafting Workflow**

```javascript
// Step 1: Start a patent drafting run
const runResponse = await fetch('http://localhost:8000/api/patent/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_message: "Help me draft claims for a 5G beamforming optimization system",
    document_content: {
      text: "Our invention relates to adaptive beamforming in 5G networks..."
    }
  })
});

const { run_id, session_id } = await runResponse.json();
console.log('Run started:', run_id);

// Step 2: Stream the results
const eventSource = new EventSource(`http://localhost:8000/api/patent/stream?run_id=${run_id}`);

eventSource.onmessage = (event) => {
  if (event.type === 'final') {
    const data = JSON.parse(event.data);
    console.log('Final response:', data.response);
    console.log('Generated claims:', data.data?.claims);
  }
};

// Step 3: Get complete run details
const detailsResponse = await fetch(`http://localhost:8000/api/patent/run/${run_id}`);
const runDetails = await detailsResponse.json();
console.log('Complete run details:', runDetails);
```

### **2. Prior Art Search**

```javascript
const priorArtResponse = await fetch('http://localhost:8000/api/patent/prior-art', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_message: "Find prior art for wireless mesh networking protocols"
  })
});

const results = await priorArtResponse.json();
console.log('Total patents found:', results.total_found);
console.log('Formatted report (markdown):', results.results);
console.log('Patent IDs:', results.patents);
```

### **3. Session Management**

```javascript
// List all active sessions
const sessionsResponse = await fetch('http://localhost:8000/api/sessions');
const sessions = await sessionsResponse.json();
console.log('Active sessions:', sessions.total_sessions);

// Continue existing session
const continueResponse = await fetch('http://localhost:8000/api/patent/run', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    user_message: "Can you refine those claims we discussed earlier?",
    session_id: "existing-session-uuid-123"
  })
});
```

## 📊 **Server-Sent Events (SSE) Stream Format**

The `/api/patent/stream` endpoint returns Server-Sent Events with the following format:

```
event: status
data: {"status": "processing", "message": "Analyzing your request..."}

event: reasoning
data: {"text": "Based on your 5G invention description, I'll draft comprehensive claims..."}

event: tool_call
data: {"tool": "draft_claims", "num_claims": 3}

event: tool_result
data: {"tool": "draft_claims", "success": true, "claims_generated": 3}

event: final
data: {"response": "Here are your patent claims...", "metadata": {...}, "data": {...}}

event: done
data: {}
```

### **Event Types:**
- **status**: Processing status updates
- **reasoning**: AI reasoning and thought process
- **tool_call**: When AI decides to use tools (e.g., draft claims)
- **tool_result**: Results from tool execution
- **final**: Complete response with claims/analysis
- **done**: Stream completion marker
- **error**: Error notifications

## 🔧 **Integration Tips**

### **Frontend Integration**
```typescript
// TypeScript interfaces for type safety
interface ChatRequest {
  user_message: string;
  conversation_history?: ConversationTurn[];
  document_content?: DocumentContent;
  session_id?: string;
}

interface RunResponse {
  run_id: string;
  session_id: string;
}

interface PriorArtResponse {
  results: string;  // Markdown formatted
  thought_process: string;
  query: string;
  total_found: number;
  timestamp: string;
  patents: string[];
}
```

### **Error Handling**
```javascript
try {
  const response = await fetch('/api/patent/run', { /* ... */ });
  if (!response.ok) {
    const error = await response.json();
    console.error('API Error:', error.detail);
  }
} catch (error) {
  console.error('Network Error:', error.message);
}
```

### **Authentication (Future)**
```javascript
// When authentication is implemented
const headers = {
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${yourJwtToken}`
};
```

## 🚨 **Important Notes**

### **Development vs Production**
- **Debug endpoints** (`/api/debug/*`) should not be exposed in production
- **CORS** is currently set to allow all origins - restrict in production
- **Rate limiting** is not implemented - add for production use

### **Data Models**
All request/response schemas are defined in the OpenAPI specification:
- `RunRequest`: Patent drafting request structure
- `ConversationTurn`: Individual message format
- `DocumentContent`: Word document content structure
- `PriorArtResponse`: Prior art search results

### **Performance Considerations**
- **Streaming responses** reduce perceived latency
- **Session management** maintains conversation context
- **Document content** is processed efficiently
- **Prior art search** may take 10-30 seconds for comprehensive results

## 📱 **Testing with Swagger UI**

1. **Navigate to** `http://localhost:8000/docs`
2. **Expand any endpoint** to see parameters and schemas
3. **Click "Try it out"** to test interactively
4. **Fill in parameters** and click "Execute"
5. **View real responses** with examples and schemas

## 🔍 **Troubleshooting**

### **Common Issues**
1. **"Run not found"**: Ensure run_id from `/api/patent/run` is correct
2. **"Environment validation failed"**: Check Azure OpenAI configuration
3. **CORS errors**: Verify server is running and accessible
4. **SSE connection issues**: Check browser SSE support and network

### **Debug Endpoints**
- **GET /api/debug/env**: Check environment variables
- **GET /api/debug/session/{id}**: Inspect session state
- **GET /api/sessions**: List all active sessions

---

**For more detailed information, refer to the interactive documentation at `http://localhost:8000/docs` when the server is running!**
