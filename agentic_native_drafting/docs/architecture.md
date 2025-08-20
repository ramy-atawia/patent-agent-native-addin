# Architecture Overview

Comprehensive system architecture documentation for the Agentic Native Drafting Service.

## 🏗️ System Architecture

### **High-Level Architecture**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client Apps   │    │   FastAPI App    │    │  Azure OpenAI   │
│                 │    │                  │    │                 │
│ • Web Frontend  │◄──►│ • Main Router    │◄──►│ • GPT-4o-mini   │
│ • CLI Client    │    │ • Agent Service  │    │ • Function      │
│ • Mobile App    │    │ • Session Mgmt   │    │   Calling      │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌──────────────────┐
                       │  In-Memory       │
                       │  Session Store   │
                       │                  │
                       │ • Sessions       │
                       │ • Run History    │
                       │ • Context Data   │
                       └──────────────────┘
```

## 🔧 Core Components

### **1. FastAPI Application (`main.py`)**

**Purpose**: Main application entry point and API routing

**Key Responsibilities**:
- HTTP endpoint management
- Request/response handling
- Session orchestration
- SSE streaming setup

**Core Classes**:
```python
class SimplePatentService:
    def __init__(self):
        self._runs: Dict[str, Dict[str, Any]] = {}
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._session_history: Dict[str, str] = {}
```

**Key Methods**:
- `start_run()`: Initialize new patent drafting session
- `stream_run()`: Handle streaming responses with context
- `_add_to_session_history()`: Maintain conversation history
- `_get_session_history()`: Retrieve session context

---

### **2. Agent System (`agent.py`)**

**Purpose**: Core intelligence and decision-making engine

**Key Responsibilities**:
- LLM-based intent classification
- Function routing and execution
- Confidence threshold management
- Patent claim generation and review

**Core Functions**:
```python
async def classify_user_intent(user_input: str, conversation_context: str = "") -> IntentClassification

def draft_claims(disclosure: str, num_claims: int = 3, session_history: str = "") -> List[str]

def review_claims(claims_text: str, session_history: str = "") -> List[ReviewComment]

async def agent_run(user_input: str, conversation_context: str = "") -> AgentResponse
```

**Decision Flow**:
```
User Input → Intent Classification → Confidence Check → Action Execution
                ↓
        [Confidence > 0.7] → Execute Function
                ↓
        [Confidence ≤ 0.7] → Seek Clarification
```

---

### **3. Data Models (`models.py`)**

**Purpose**: Structured data definitions and validation

**Core Models**:
```python
class IntentClassification(BaseModel):
    intent: IntentType
    confidence_score: float
    reasoning: str

class AgentResponse(BaseModel):
    conversation_response: str
    reasoning: str
    review_comments: Optional[List[ReviewComment]] = None
    metadata: Dict[str, Any]

class ReviewComment(BaseModel):
    comment: str
    severity: str
    suggestion: str
```

---

### **4. Session Management System**

**Purpose**: Persistent conversation context and history

**Architecture**:
```
Session (Multiple Runs)
├── Session ID: UUID
├── Started At: Timestamp
├── Topic: Invention Description
├── Runs: List[Run ID]
└── History: Text-based conversation log

Run (Single Interaction)
├── Run ID: UUID
├── Session ID: UUID
├── Disclosure: User Input
├── Status: started/completed
└── Result: Agent Response
```

**Key Features**:
- **Session Isolation**: Separate contexts for different patent projects
- **Context Persistence**: Maintain conversation history across runs
- **History Building**: Accumulate user-agent interactions
- **Context Injection**: Pass relevant history to LLM prompts

---

## 🔄 Data Flow Architecture

### **1. Session Initialization Flow**

```
Client Request → API Router → Service Layer → Session Creation
      ↓              ↓            ↓            ↓
  POST /run    FastAPI Route  start_run()   New Session
      ↓              ↓            ↓            ↓
  Response ←─── JSON ←─── UUIDs ←─── Session Store
```

**Detailed Flow**:
1. Client sends `POST /api/patent/run` with disclosure
2. FastAPI routes to `SimplePatentService.start_run()`
3. Service creates new session or continues existing one
4. Returns `run_id` and `session_id` to client
5. Client uses `run_id` for streaming response

### **2. Agent Processing Flow**

```
User Input → Intent Classification → Confidence Check → Function Execution
    ↓              ↓                    ↓                ↓
Session    LLM Prompt with      Threshold Logic    draft_claims()
Context    History Context      (>0.7: Execute)    review_claims()
    ↓              ↓                    ↓                ↓
History    Intent + Confidence  Action Decision    Response Generation
Update     Score + Reasoning    (Execute/Seek)    with Context
```

**Detailed Flow**:
1. **Input Processing**: Extract user input and session context
2. **Intent Classification**: LLM analyzes input with context
3. **Confidence Assessment**: Check if confidence > 0.7
4. **Action Execution**: Route to appropriate function
5. **Response Generation**: Generate context-aware response
6. **History Update**: Store interaction in session history

### **3. Streaming Response Flow**

```
Agent Response → SSE Events → Client Processing → Final Display
      ↓              ↓              ↓              ↓
  Final Data    Event Stream    Event Handler    UI Update
      ↓              ↓              ↓              ↓
  JSON Format   status,reasoning  JavaScript     User Interface
                tool_call,result  EventSource    Response Display
                final,done
```

**Event Sequence**:
1. **status**: Processing status update
2. **reasoning**: LLM reasoning and confidence
3. **tool_call**: Function being called
4. **tool_result**: Function execution result
5. **final**: Complete response with metadata
6. **done**: Stream completion signal

---

## 🧠 LLM Integration Architecture

### **Azure OpenAI Integration**

**Configuration**:
```python
# Environment Variables
AZURE_OPENAI_ENDPOINT = "https://{deployment}.cognitiveservices.azure.com/"
AZURE_OPENAI_API_KEY = "your-api-key"
AZURE_OPENAI_DEPLOYMENT_NAME = "gpt-4o-mini"
AZURE_OPENAI_API_VERSION = "2024-12-01-preview"
```

**Integration Points**:
- **Intent Classification**: Dynamic user intent understanding
- **Patent Drafting**: USPTO-compliant claim generation
- **Claim Review**: Quality assessment and feedback
- **Context Understanding**: Session history interpretation

**Prompt Engineering**:
```python
# Intent Classification Prompt
prompt = f"""
You are an expert patent attorney AI assistant. Analyze this user input and classify their intent.

User Input: {user_input}

Session History:
{conversation_context if conversation_context else "No previous conversation in this session"}

Available intent types:
1. claim_drafting - User wants patent claims drafted
2. claim_review - User wants existing claims reviewed
3. patent_guidance - User needs general patent advice
4. invention_analysis - User wants invention analyzed
5. technical_query - User has technical questions
6. general_conversation - General chat or greetings

Consider:
- Explicit keywords in the user's request
- Technical complexity of the input
- Context from previous conversation in this session
- Professional patent terminology
"""
```

---

## 🗄️ Data Storage Architecture

### **In-Memory Storage**

**Session Store**:
```python
_sessions: Dict[str, Dict[str, Any]] = {
    "session_id": {
        "session_id": "uuid",
        "started_at": "2024-08-17T01:08:15.123456",
        "runs": ["run_id_1", "run_id_2"],
        "topic": "Invention description..."
    }
}
```

**Run Store**:
```python
_runs: Dict[str, Dict[str, Any]] = {
    "run_id": {
        "run_id": "uuid",
        "session_id": "session_uuid",
        "disclosure": "User input text",
        "status": "started/completed",
        "created_at": "timestamp",
        "result": "AgentResponse object"
    }
}
```

**History Store**:
```python
_session_history: Dict[str, str] = {
    "session_id": "User: Input text\nAgent: Response text\n---\nUser: Next input..."
}
```

### **Data Persistence Strategy**

**Current Implementation**:
- In-memory storage for active sessions
- Session data lost on server restart
- Fast access and low latency

**Future Considerations**:
- Database persistence (PostgreSQL/MongoDB)
- Redis for session caching
- File-based backup system
- Session archival and cleanup

---

## 🔒 Security & Performance

### **Security Features**

**Input Validation**:
- Pydantic model validation
- Request parameter sanitization
- Session ID validation
- Rate limiting considerations

**API Security**:
- HTTP/HTTPS communication
- JSON payload validation
- Error message sanitization
- Session isolation enforcement

### **Performance Optimizations**

**Streaming Architecture**:
- Server-Sent Events for real-time updates
- Non-blocking async operations
- Efficient memory management
- Connection pooling

**Caching Strategy**:
- In-memory session storage
- LLM response caching (future)
- Session context optimization
- Request deduplication

---

## 🔄 System Interactions

### **Component Communication**

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Client    │    │   FastAPI   │    │    Agent    │
│             │◄──►│   Router    │◄──►│   System    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                    │
                          ▼                    ▼
                   ┌─────────────┐    ┌─────────────┐
                   │  Session    │    │  Azure      │
                   │  Service    │    │  OpenAI     │
                   └─────────────┘    └─────────────┘
```

### **Data Flow Patterns**

**Request Pattern**:
```
Client → FastAPI → Service → Agent → LLM → Response → Client
```

**Session Pattern**:
```
Start → Continue → Continue → ... → Complete
  ↓         ↓         ↓              ↓
New      Context   Context      Final Result
Session  Aware    Aware        with History
```

---

## 🚀 Scalability Considerations

### **Current Architecture Strengths**

✅ **Stateless API Design**: Easy horizontal scaling  
✅ **Async Processing**: Non-blocking operations  
✅ **Session Isolation**: Independent conversation contexts  
✅ **Modular Components**: Clear separation of concerns  

### **Future Scaling Strategies**

🔄 **Horizontal Scaling**:
- Multiple FastAPI instances
- Load balancer distribution
- Shared session storage (Redis/Database)

🔄 **Performance Optimization**:
- LLM response caching
- Session data compression
- Background task processing
- Connection pooling

🔄 **Monitoring & Observability**:
- Metrics collection
- Performance monitoring
- Error tracking
- Usage analytics

---

## 📊 System Metrics

### **Key Performance Indicators**

- **Response Time**: Intent classification latency
- **Throughput**: Requests per second
- **Session Duration**: Average session length
- **Success Rate**: Successful intent classifications
- **Error Rate**: Failed requests and exceptions

### **Monitoring Points**

- API endpoint response times
- LLM integration latency
- Session storage performance
- Memory usage patterns
- Error frequency and types

---

## 🔮 Future Architecture Evolution

### **Planned Enhancements**

1. **Database Integration**: Persistent session storage
2. **Microservices**: Service decomposition
3. **Event Streaming**: Kafka/RabbitMQ integration
4. **Containerization**: Docker/Kubernetes deployment
5. **API Gateway**: Centralized routing and security

### **Architecture Principles**

- **Modularity**: Clear component boundaries
- **Scalability**: Horizontal scaling capability
- **Maintainability**: Clean code and documentation
- **Reliability**: Error handling and recovery
- **Performance**: Efficient data processing

---

**Next**: Read the [Functionality Guide](functionality.md) to understand the system's capabilities and use cases.
