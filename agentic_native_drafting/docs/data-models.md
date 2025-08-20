# Data Models

Complete documentation of all data structures, Pydantic models, and schemas used in the Agentic Native Drafting Service.

## 📋 Model Overview

The system uses Pydantic models for:
- **Data Validation**: Automatic type checking and validation
- **API Serialization**: JSON request/response handling
- **Type Safety**: IntelliSense and error prevention
- **Documentation**: Self-documenting API schemas

## 🏗️ Core Data Models

### **1. Intent Classification Models**

#### **IntentType Enum**
```python
class IntentType(str, Enum):
    CLAIM_DRAFTING = "claim_drafting"
    CLAIM_REVIEW = "claim_review"
    PATENT_GUIDANCE = "patent_guidance"
    INVENTION_ANALYSIS = "invention_analysis"
    TECHNICAL_QUERY = "technical_query"
    GENERAL_CONVERSATION = "general_conversation"
```

**Purpose**: Defines the six supported user intent types for routing requests to appropriate functions.

**Usage Examples**:
```python
# Intent classification
intent = IntentType.CLAIM_DRAFTING  # "claim_drafting"
intent = IntentType.CLAIM_REVIEW    # "claim_review"

# Validation
if intent == IntentType.CLAIM_DRAFTING:
    # Route to claim drafting function
    pass
```

#### **IntentClassification Model**
```python
class IntentClassification(BaseModel):
    intent: IntentType
    confidence_score: float
    reasoning: str
```

**Fields**:
- `intent`: The classified intent type (IntentType enum)
- `confidence_score`: LLM confidence in classification (0.0 to 1.0)
- `reasoning`: LLM's explanation for the classification

**Example Instance**:
```python
classification = IntentClassification(
    intent=IntentType.CLAIM_DRAFTING,
    confidence_score=0.95,
    reasoning="User explicitly requests drafting patent claims for their AI invention"
)
```

**Validation Rules**:
- `confidence_score`: Must be between 0.0 and 1.0
- `reasoning`: Must be non-empty string
- `intent`: Must be valid IntentType enum value

---

### **2. Agent Response Models**

#### **AgentResponse Model**
```python
class AgentResponse(BaseModel):
    conversation_response: str
    reasoning: str
    review_comments: Optional[List[ReviewComment]] = None
    metadata: Dict[str, Any]
```

**Fields**:
- `conversation_response`: The main response text to the user
- `reasoning`: LLM's reasoning for the chosen action
- `review_comments`: Optional list of review feedback (for claim review)
- `metadata`: Additional response data (claims, confidence, etc.)

**Example Instance**:
```python
response = AgentResponse(
    conversation_response="I've drafted 3 patent claims for your invention...",
    reasoning="Executing claim_drafting (confidence: 0.95)",
    review_comments=None,
    metadata={
        "should_draft_claims": True,
        "has_claims": True,
        "confidence": 0.95
    }
)
```

**Usage Patterns**:
```python
# For claim drafting
draft_response = AgentResponse(
    conversation_response="Generated claims...",
    reasoning="Executing claim_drafting",
    metadata={"has_claims": True, "num_claims": 3}
)

# For claim review
review_response = AgentResponse(
    conversation_response="Review completed...",
    reasoning="Executing claim_review",
    review_comments=[ReviewComment(...)],
    metadata={"review_count": 2}
)
```

---

### **3. Review Comment Models**

#### **ReviewComment Model**
```python
class ReviewComment(BaseModel):
    comment: str
    severity: str
    suggestion: str
```

**Fields**:
- `comment`: Description of the issue found
- `severity`: Issue severity level (minor/major/critical)
- `suggestion`: Recommended improvement action

**Example Instance**:
```python
comment = ReviewComment(
    comment="Claim 1 lacks specific technical details about ML algorithm",
    severity="major",
    suggestion="Add algorithm parameters and training methodology"
)
```

**Severity Levels**:
- **🟢 MINOR**: Small improvements, formatting issues
- **🟡 MAJOR**: Significant issues affecting claim quality
- **🔴 CRITICAL**: Serious compliance or patentability issues

**Usage in Review**:
```python
review_comments = [
    ReviewComment(
        comment="Claim structure follows proper dependency format",
        severity="minor",
        suggestion="Consider adding more specific technical details"
    ),
    ReviewComment(
        comment="May violate 35 USC 101 patentable subject matter",
        severity="critical",
        suggestion="Add concrete technical implementation details"
    )
]
```

---

### **4. Function Call Models**

#### **FunctionCall Model**
```python
class FunctionCall(BaseModel):
    name: str
    arguments: Dict[str, Any]
```

**Fields**:
- `name`: Name of the function to call
- `arguments`: Dictionary of function parameters

**Example Instance**:
```python
function_call = FunctionCall(
    name="draft_claims",
    arguments={
        "disclosure": "AI-powered quantum computing system",
        "num_claims": 3,
        "session_history": "Previous conversation context..."
    }
)
```

**Supported Functions**:
- `draft_claims`: Generate patent claims
- `review_claims`: Review existing claims
- `conversation_query`: Handle general conversation

---

## 🗄️ Session Management Models

### **1. Session Data Structures**

#### **Session Metadata**
```python
# Internal session structure (not Pydantic model)
session_data = {
    "session_id": "uuid-string",
    "started_at": "2024-08-17T01:08:15.123456",
    "runs": ["run_id_1", "run_id_2", "run_id_3"],
    "topic": "AI-powered quantum computing system..."
}
```

**Fields**:
- `session_id`: Unique identifier for the session
- `started_at`: ISO timestamp when session was created
- `runs`: List of run IDs within this session
- `topic`: Brief description of the session topic

#### **Run Data Structure**
```python
# Internal run structure (not Pydantic model)
run_data = {
    "run_id": "uuid-string",
    "session_id": "session_uuid",
    "disclosure": "User input text",
    "status": "started" | "completed",
    "created_at": "timestamp",
    "result": "AgentResponse object"
}
```

**Fields**:
- `run_id`: Unique identifier for the run
- `session_id`: Parent session identifier
- `disclosure`: User's input text
- `status`: Current run status
- `created_at`: ISO timestamp when run was created
- `result`: Final agent response (if completed)

---

### **2. Session History Model**

#### **History Storage Format**
```python
# Internal history structure (not Pydantic model)
session_history = {
    "session_id": "User: Please draft patent claims for my AI invention\nAgent: I've drafted 3 patent claims...\n---\nUser: Review those claims\nAgent: I've reviewed your claims..."
}
```

**Format**:
- Each conversation turn is separated by newlines
- User inputs prefixed with "User: "
- Agent responses prefixed with "Agent: "
- Turns separated by "---" for readability

**Example History**:
```
User: Please draft patent claims for my quantum computing system
Agent: I've drafted 3 patent claims based on your invention:
1. A quantum computing system comprising...
2. The system of claim 1, wherein...
3. The system of claim 1, wherein...
---
User: Review those claims for quality
Agent: I've reviewed your patent claims and found 2 issue(s):
🟡 MAJOR: Claim 1 needs more specific technical details...
🟢 MINOR: Consider adding dependent claims for specific features...
---
User: Improve claim 1 based on your feedback
Agent: Here's an improved version of claim 1 with specific technical details...
```

---

## 🔄 API Request/Response Models

### **1. Patent Run Request**

#### **Start Run Request**
```python
# Request body for POST /api/patent/run
{
    "disclosure": "string (required)",
    "session_id": "string (optional)"
}
```

**Validation Rules**:
- `disclosure`: Required, non-empty string
- `session_id`: Optional, valid UUID format if provided

**Example Request**:
```json
{
    "disclosure": "Please draft patent claims for my blockchain invention that uses AI for supply chain optimization",
    "session_id": "6e8ab42e-2ada-4c23-9fca-25a0ef81544f"
}
```

#### **Start Run Response**
```python
# Response from POST /api/patent/run
{
    "run_id": "uuid-string",
    "session_id": "uuid-string"
}
```

**Example Response**:
```json
{
    "run_id": "a12997b6-61f7-4a23-ac63-32435740877a",
    "session_id": "6e8ab42e-2ada-4c23-9fca-25a0ef81544f"
}
```

---

### **2. Streaming Response Models**

#### **SSE Event Structure**
```python
# Server-Sent Events format
event: {event_type}
data: {json_data}

# Event types and data structures
```

**Event Types**:

1. **Status Event**:
```json
event: status
data: {
    "status": "processing",
    "message": "Analyzing your request..."
}
```

2. **Reasoning Event**:
```json
event: reasoning
data: {
    "reasoning": "Executing claim_drafting (confidence: 0.95)..."
}
```

3. **Tool Call Event**:
```json
event: tool_call
data: {
    "tool": "draft_claims",
    "parameters": {
        "disclosure": "User input...",
        "num_claims": 3
    }
}
```

4. **Tool Result Event**:
```json
event: tool_result
data: {
    "result": "Generated 3 patent claims successfully"
}
```

5. **Final Event**:
```json
event: final
data: {
    "response": "I've drafted 3 patent claims...",
    "metadata": {
        "should_draft_claims": true,
        "has_claims": true,
        "reasoning": "Executing claim_drafting..."
    },
    "data": {
        "claims": ["Claim 1...", "Claim 2...", "Claim 3..."],
        "num_claims": 3
    }
}
```

6. **Done Event**:
```json
event: done
data: {}
```

---

### **3. Session Management Responses**

#### **List Sessions Response**
```python
# Response from GET /api/sessions
{
    "total_sessions": 3,
    "sessions": [
        {
            "session_id": "uuid-string",
            "started_at": "2024-08-17T01:08:15.123456",
            "topic": "AI-powered quantum computing system...",
            "total_runs": 2,
            "last_run": "uuid-string"
        }
    ]
}
```

#### **Session Debug Response**
```python
# Response from GET /api/debug/session/{session_id}
{
    "session_id": "uuid-string",
    "started_at": "2024-08-17T01:08:15.123456",
    "topic": "AI-powered quantum computing system...",
    "runs": ["run_id_1", "run_id_2"],
    "session_history": "User: Input text\nAgent: Response text\n---\n..."
}
```

---

## 🔧 Internal Data Structures

### **1. Service State Management**

#### **SimplePatentService State**
```python
class SimplePatentService:
    def __init__(self):
        # Active runs tracking
        self._runs: Dict[str, Dict[str, Any]] = {}
        
        # Session management
        self._sessions: Dict[str, Dict[str, Any]] = {}
        
        # Conversation history
        self._session_history: Dict[str, str] = {}
```

**Data Relationships**:
```
Sessions (1) ←→ (Many) Runs
Sessions (1) ←→ (1) History
Runs (Many) ←→ (1) Sessions
```

**Memory Management**:
- Sessions persist until server restart
- Runs are completed and stored
- History accumulates over time
- No automatic cleanup (future enhancement)

---

### **2. LLM Integration Data**

#### **Prompt Construction**
```python
# Intent classification prompt structure
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
- References to previous claims or responses

Use the classify_user_intent function to provide your analysis.
"""
```

#### **Response Parsing**
```python
# LLM response structure for intent classification
{
    "function_call": {
        "name": "classify_user_intent",
        "arguments": {
            "intent": "claim_drafting",
            "confidence_score": 0.95,
            "reasoning": "User explicitly requests drafting patent claims..."
        }
    }
}
```

---

## 📊 Data Validation & Constraints

### **1. Field Validation Rules**

#### **String Fields**
- `disclosure`: Required, min_length=1, max_length=10000
- `reasoning`: Required, min_length=10, max_length=2000
- `comment`: Required, min_length=10, max_length=1000
- `suggestion`: Required, min_length=10, max_length=1000

#### **Numeric Fields**
- `confidence_score`: Required, ge=0.0, le=1.0
- `num_claims`: Optional, ge=1, le=20

#### **Enum Fields**
- `intent`: Must be valid IntentType enum value
- `severity`: Must be one of ["minor", "major", "critical"]

### **2. Business Logic Validation**

#### **Session Continuity**
- `session_id` must exist in active sessions
- `run_id` must belong to specified session
- Session history must be accessible

#### **Intent Classification**
- Confidence score must be valid probability
- Reasoning must explain classification
- Intent must match available types

#### **Claim Generation**
- Number of claims must be reasonable (1-20)
- Claims must have proper structure
- Technical content must be present

---

## 🔄 Data Flow Patterns

### **1. Request Processing Flow**

```
Client Request → Pydantic Validation → Service Processing → Response Generation
      ↓                ↓                    ↓                    ↓
  JSON Input    Type Checking      Business Logic        JSON Output
      ↓                ↓                    ↓                    ↓
  API Endpoint  Field Validation   Data Processing      SSE Events
```

### **2. Session Data Flow**

```
Session Creation → Run Execution → History Update → Context Injection
      ↓              ↓              ↓              ↓
   New UUID      Process Input   Store Turn      Build Prompt
      ↓              ↓              ↓              ↓
  Store State    Generate      Accumulate      Pass to LLM
                Response      Conversation    for Context
```

### **3. LLM Integration Flow**

```
User Input → Context Building → LLM Prompt → Response Parsing → Validation
     ↓            ↓              ↓            ↓            ↓
  Raw Text    History +      Structured    JSON Parse   Pydantic
              Context        Prompt        Function     Validation
     ↓            ↓              ↓            ↓            ↓
  Processed   Enhanced      LLM Input    Extracted    Validated
   Input      Context       Generation   Data        Response
```

---

## 🚀 Performance Considerations

### **1. Memory Management**

**Current Implementation**:
- In-memory storage for active sessions
- No automatic cleanup or expiration
- Linear growth with session count

**Optimization Strategies**:
- Session timeout and cleanup
- History compression
- Memory usage monitoring
- LRU eviction policies

### **2. Data Serialization**

**JSON Performance**:
- Fast serialization/deserialization
- Compact data representation
- Wide language support
- Streaming compatibility

**Validation Overhead**:
- Pydantic validation on every request
- Type checking and conversion
- Error handling and reporting
- Schema generation for documentation

---

## 🔮 Future Data Model Enhancements

### **1. Planned Additions**

**Database Models**:
- Persistent session storage
- User authentication and authorization
- Audit logging and analytics
- Performance metrics tracking

**Advanced Features**:
- Multi-language support
- Collaborative editing
- Version control for claims
- Prior art integration

### **2. Schema Evolution**

**Backward Compatibility**:
- Optional fields for new features
- Default values for missing data
- Migration strategies for schema changes
- API versioning support

**Extensibility**:
- Plugin architecture for new intent types
- Custom validation rules
- Dynamic field addition
- Schema customization

---

**Next**: Read the [Session Management](session-management.md) documentation to understand how sessions work.
