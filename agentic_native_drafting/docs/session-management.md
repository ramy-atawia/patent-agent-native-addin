# Session Management

Comprehensive guide to session management, context persistence, and conversation history in the Agentic Native Drafting Service.

## 🎯 Overview

The session management system provides persistent conversation context across multiple interactions, enabling multi-turn patent drafting workflows while maintaining session isolation for different projects.

## 🏗️ Session Architecture

### **Core Concepts**

**Session**: A container for multiple related interactions (runs) about a specific patent project
**Run**: A single user-agent interaction within a session
**Context**: The accumulated conversation history that informs future responses

### **Data Structure**

```
Session (Multiple Runs)
├── Session ID: UUID (unique identifier)
├── Started At: ISO timestamp
├── Topic: Brief description of the invention/project
├── Runs: List of run IDs in chronological order
└── History: Text-based conversation log

Run (Single Interaction)
├── Run ID: UUID (unique identifier)
├── Session ID: Parent session reference
├── Disclosure: User input text
├── Status: started/completed
├── Created At: ISO timestamp
└── Result: Final agent response
```

---

## 🔄 Session Lifecycle

### **1. Session Creation**

#### **New Session Flow**
```
Client Request → Service Layer → Session Creation → Response
      ↓              ↓              ↓            ↓
  POST /run    start_run()     New UUIDs    run_id + session_id
      ↓              ↓              ↓            ↓
  disclosure    Validation    Store State   Client receives IDs
```

**Implementation**:
```python
async def start_run(self, disclosure: str, session_id: str = None) -> Dict[str, str]:
    if session_id and session_id in self._sessions:
        # Continue existing session
        run_id = str(uuid.uuid4())
        session = self._sessions[session_id]
        session["runs"].append(run_id)
        print(f"🔄 Continuing session {session_id} with run {run_id}")
    else:
        # Start new session
        session_id = str(uuid.uuid4())
        run_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            "session_id": session_id,
            "started_at": datetime.now().isoformat(),
            "runs": [run_id],
            "topic": disclosure[:100] + "..." if len(disclosure) > 100 else disclosure
        }
        print(f"🆕 Starting new session {session_id} with run {run_id}")
    
    # Create run
    self._runs[run_id] = {
        "run_id": run_id,
        "session_id": session_id,
        "disclosure": disclosure,
        "status": "started",
        "created_at": datetime.now().isoformat()
    }
    
    # Initialize session history if new session
    if session_id not in self._session_history:
        self._session_history[session_id] = ""
    
    return {"run_id": run_id, "session_id": session_id}
```

#### **Session Continuation Flow**
```
Client Request → Service Layer → Session Lookup → Run Creation
      ↓              ↓              ↓            ↓
  POST /run    start_run()     Find Session   Add New Run
      ↓              ↓              ↓            ↓
  session_id    Validation    Verify Exists   Update State
```

**Key Features**:
- **Automatic Detection**: Service detects if `session_id` exists
- **State Preservation**: Maintains all session data and history
- **Run Addition**: Creates new run within existing session
- **Context Continuity**: Preserves conversation history

---

### **2. Session Execution**

#### **Run Processing Flow**
```
Run Start → Context Retrieval → Agent Processing → History Update → Completion
    ↓            ↓              ↓              ↓            ↓
  Extract    Get History    Process with    Store Turn    Mark Complete
  Input      from Session   Context        in History    Update Status
```

**Implementation**:
```python
async def stream_run(self, run_id: str):
    # Get run data and session context
    run_data = self._runs[run_id]
    disclosure = run_data["disclosure"]
    
    # Retrieve session history for context
    session_history = self._get_session_history(run_data["session_id"])
    
    # Process with agent using context
    agent_response = await agent.run(disclosure, session_history)
    
    # Store conversation in session history
    self._add_to_session_history(run_data["session_id"], disclosure, agent_response.conversation_response)
    
    # Update run status
    self._runs[run_id]["status"] = "completed"
    self._runs[run_id]["result"] = agent_response
```

#### **Context Injection Process**
```
Session History → Context Building → Prompt Enhancement → LLM Processing
      ↓              ↓              ↓              ↓
  Raw Text      Format for      Inject into    Generate
  Extraction    LLM Prompt      LLM Prompt     Context-Aware
```

**Context Building**:
```python
def _get_session_history(self, session_id: str) -> str:
    """Get the complete session history for context building"""
    return self._session_history.get(session_id, "")

# Context injection in agent prompts
prompt = f"""
You are an expert patent attorney AI assistant. Analyze this user input and classify their intent.

User Input: {user_input}

Session History:
{conversation_context if conversation_context else "No previous conversation in this session"}

Consider:
- Context from previous conversation in this session
- References to previous claims or responses
- Technical consistency with earlier discussions
"""
```

---

### **3. Session History Management**

#### **History Accumulation**
```
Turn 1: User Input + Agent Response → Store in History
Turn 2: User Input + Agent Response → Append to History
Turn 3: User Input + Agent Response → Append to History
...
Turn N: Complete conversation history available for context
```

**Implementation**:
```python
def _add_to_session_history(self, session_id: str, user_input: str, agent_response: str):
    """Add conversation to session-level history"""
    if session_id in self._session_history:
        conversation_entry = f"User: {user_input}\nAgent: {agent_response}\n---\n"
        self._session_history[session_id] += conversation_entry
```

**History Format**:
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

## 🔒 Session Isolation

### **Multi-Project Management**

#### **Independent Sessions**
```
Session A: Quantum Computing Project
├── Session ID: 5aaf0c73-1761-4c24-aea1-b96b6c03b661
├── Topic: "Quantum computing system with AI optimization"
├── Runs: [run_1, run_2, run_3]
└── History: Quantum computing specific conversations

Session B: Blockchain Project
├── Session ID: 3eea8805-4eff-4063-831f-78893b175e7f
├── Topic: "Blockchain system for supply chain tracking"
├── Runs: [run_4, run_5]
└── History: Blockchain specific conversations
```

**Isolation Benefits**:
- ✅ **Context Separation**: No cross-contamination between projects
- ✅ **Independent History**: Each session maintains its own conversation log
- ✅ **Project Focus**: Users can work on multiple inventions simultaneously
- ✅ **Clean State**: New sessions start with fresh context

#### **Session Switching**
```
User: "Draft claims for my quantum computer" → Session A
User: "Now draft claims for my blockchain system" → Session B
User: "Review those quantum claims" → Session A (with full context)
User: "How does this compare to my blockchain claims?" → Session B (with full context)
```

---

## 🧠 Context Awareness

### **Intelligent Context Usage**

#### **Context Injection Strategies**

**1. Intent Classification Context**:
```python
# Include session history in intent classification
prompt = f"""
Session History:
{conversation_context if conversation_context else "No previous conversation in this session"}

Consider:
- Context from previous conversation in this session
- References to previous claims or responses
- Technical consistency with earlier discussions
"""
```

**2. Function Execution Context**:
```python
# Pass context to claim drafting
def draft_claims(disclosure: str, num_claims: int = 3, session_history: str = "") -> List[str]:
    context_prompt = ""
    if session_history:
        context_prompt = f"""
Session History:
{session_history}
Use this context to ensure consistency with any previously discussed inventions or claims."""
```

**3. Claim Review Context**:
```python
# Pass context to claim review
def review_claims(claims_text: str, session_history: str = "") -> List[ReviewComment]:
    context_prompt = ""
    if session_history:
        context_prompt = f"""
Session Context:
{session_history}
Use this context to understand what was previously discussed and provide more relevant feedback."""
```

#### **Context-Aware Responses**

**Example 1: Claim Reference Understanding**:
```
Previous Context: "User drafted claims for 5G AI system"
Current Request: "Review those claims"

Agent Response: "I've reviewed your 5G AI carrier aggregation claims and found..."
[Agent automatically understands "those claims" refers to the 5G AI system claims]
```

**Example 2: Technical Consistency**:
```
Previous Context: "User described quantum computing with neural networks"
Current Request: "Draft additional claims"

Agent Response: "Based on your quantum computing system with neural networks, here are additional claims..."
[Agent maintains technical consistency with the described invention]
```

---

## 📊 Session Analytics

### **Session Information Endpoints**

#### **List All Sessions**
```http
GET /api/sessions
```

**Response**:
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

#### **Session Debug Information**
```http
GET /api/debug/session/{session_id}
```

**Response**:
```json
{
  "session_id": "6e8ab42e-2ada-4c23-9fca-25a0ef81544f",
  "started_at": "2024-08-17T01:08:15.123456",
  "topic": "AI-powered quantum computing system...",
  "runs": ["run_id_1", "run_id_2"],
  "session_history": "User: Input text\nAgent: Response text\n---\n..."
}
```

### **Session Metrics**

**Key Performance Indicators**:
- **Session Count**: Total active sessions
- **Session Duration**: Time from creation to last activity
- **Run Frequency**: Average runs per session
- **Context Length**: Size of session history
- **Session Topics**: Distribution of invention types

---

## 🔧 Session Management Operations

### **Core Operations**

#### **1. Session Creation**
```python
# Create new session
response = await client.post("/api/patent/run", json={
    "disclosure": "Draft claims for my invention"
})

session_id = response.json()["session_id"]
run_id = response.json()["run_id"]
```

#### **2. Session Continuation**
```python
# Continue existing session
response = await client.post("/api/patent/run", json={
    "disclosure": "Review those claims",
    "session_id": session_id
})

new_run_id = response.json()["run_id"]
# session_id remains the same
```

#### **3. Session Monitoring**
```python
# List all sessions
sessions = await client.get("/api/sessions")
active_sessions = sessions.json()["sessions"]

# Get session details
session_info = await client.get(f"/api/debug/session/{session_id}")
session_data = session_info.json()
```

### **Advanced Operations**

#### **Session Cleanup**
```python
# Future enhancement: automatic session cleanup
def cleanup_expired_sessions(self, max_age_hours: int = 24):
    """Remove sessions older than specified age"""
    current_time = datetime.now()
    expired_sessions = []
    
    for session_id, session_data in self._sessions.items():
        started_at = datetime.fromisoformat(session_data["started_at"])
        age_hours = (current_time - started_at).total_seconds() / 3600
        
        if age_hours > max_age_hours:
            expired_sessions.append(session_id)
    
    for session_id in expired_sessions:
        self._cleanup_session(session_id)
```

#### **Session Export**
```python
# Future enhancement: export session data
def export_session(self, session_id: str) -> Dict[str, Any]:
    """Export complete session data for backup or analysis"""
    if session_id not in self._sessions:
        raise ValueError("Session not found")
    
    session_data = self._sessions[session_id].copy()
    session_data["history"] = self._session_history.get(session_id, "")
    session_data["runs"] = [
        self._runs[run_id] for run_id in session_data["runs"]
        if run_id in self._runs
    ]
    
    return session_data
```

---

## 🚀 Performance & Scalability

### **Current Implementation**

**Memory Usage**:
- **Session Storage**: ~1KB per session (metadata)
- **History Storage**: ~2-10KB per session (depending on conversation length)
- **Run Storage**: ~0.5KB per run
- **Total Overhead**: ~3-15KB per active session

**Performance Characteristics**:
- ✅ **Fast Access**: In-memory storage for instant retrieval
- ✅ **Low Latency**: No database queries or network calls
- ✅ **Efficient Updates**: Direct dictionary operations
- ✅ **Minimal Overhead**: Lightweight data structures

### **Scalability Considerations**

**Memory Growth**:
```
Active Sessions: Linear growth with user activity
Session History: Linear growth with conversation length
Run Storage: Linear growth with interaction count
Total Memory: O(n) where n = total sessions + total history
```

**Optimization Strategies**:
1. **Session Expiration**: Automatic cleanup of old sessions
2. **History Compression**: Compress long conversation histories
3. **Memory Monitoring**: Track memory usage and implement limits
4. **LRU Eviction**: Remove least recently used sessions when memory is low

---

## 🔮 Future Enhancements

### **Planned Features**

#### **1. Persistent Storage**
```python
# Database integration for session persistence
class SessionDatabase:
    def save_session(self, session_data: Dict[str, Any]):
        # Save to PostgreSQL/MongoDB
        
    def load_session(self, session_id: str) -> Dict[str, Any]:
        # Load from database
        
    def cleanup_sessions(self, max_age: timedelta):
        # Database-level cleanup
```

#### **2. Advanced Context Management**
```python
# Semantic context extraction
class ContextManager:
    def extract_key_concepts(self, session_history: str) -> List[str]:
        # Extract key technical concepts
        
    def build_context_summary(self, session_history: str) -> str:
        # Generate context summary for LLM
        
    def identify_context_changes(self, old_context: str, new_context: str) -> List[str]:
        # Track context evolution
```

#### **3. Session Analytics**
```python
# Advanced session analytics
class SessionAnalytics:
    def analyze_session_patterns(self) -> Dict[str, Any]:
        # Identify common workflow patterns
        
    def predict_session_outcomes(self, session_data: Dict[str, Any]) -> Dict[str, float]:
        # Predict session success probability
        
    def generate_session_insights(self, session_id: str) -> Dict[str, Any]:
        # Provide session-specific insights
```

---

## 📋 Best Practices

### **For Developers**

1. **Session State Management**:
   - Always validate session IDs before use
   - Handle session expiration gracefully
   - Implement proper error handling for missing sessions

2. **Context Injection**:
   - Limit context size to prevent prompt bloat
   - Prioritize recent context over older conversations
   - Implement context summarization for long sessions

3. **Memory Management**:
   - Monitor session memory usage
   - Implement automatic cleanup strategies
   - Set reasonable limits on session count and history size

### **For Users**

1. **Session Continuity**:
   - Use the same session for related requests
   - Reference previous claims and discussions
   - Build upon previous feedback and improvements

2. **Context Clarity**:
   - Provide clear invention descriptions
   - Use consistent terminology
   - Reference specific claims when requesting reviews

3. **Session Organization**:
   - Use separate sessions for different inventions
   - Keep related work within the same session
   - Monitor session topics and run counts

---

## 🔍 Troubleshooting

### **Common Issues**

#### **1. Session Not Found**
**Symptoms**: 404 error when accessing session
**Causes**: Session expired, server restart, invalid session ID
**Solutions**: Create new session, verify session ID format

#### **2. Context Loss**
**Symptoms**: Agent doesn't remember previous claims
**Causes**: Session ID mismatch, history corruption
**Solutions**: Verify session ID, check session debug endpoint

#### **3. Memory Issues**
**Symptoms**: High memory usage, slow performance
**Causes**: Too many active sessions, long histories
**Solutions**: Implement session cleanup, limit history size

### **Debug Commands**

```bash
# Check all sessions
curl "http://127.0.0.1:8001/api/sessions"

# Debug specific session
curl "http://127.0.0.1:8001/api/debug/session/{session_id}"

# Health check
curl "http://127.0.0.1:8001/"
```

---

**Next**: Read the [LLM Integration](llm-integration.md) documentation to understand how the system integrates with Azure OpenAI.
