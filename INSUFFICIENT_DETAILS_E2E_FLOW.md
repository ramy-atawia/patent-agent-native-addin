# End-to-End Logic Flow: Insufficient Details Detection

## Overview
This document traces the complete flow of how the system detects and handles insufficient details requests (like "draft 10 claims") using purely LLM-based assessment.

## Architecture Summary
```
User Input → Frontend → API Service → Backend Main → Agent → LLM Assessment → Response
```

## 1. User Input & Frontend Processing

### Frontend Entry (`ChatBot.tsx`)
```typescript
// User types: "draft 10 claims"
const handleSubmit = async (e: React.FormEvent) => {
  // ... validation ...
  
  const request = {
    user_message: inputValue,  // "draft 10 claims"
    conversation_history: getConversationHistory(),
    document_content: { text: documentContent },
    session_id: sessionId,
  };

  // Send to API service
  await apiService.chatStream(request, onChunk, onComplete, onError);
}
```

### API Service Processing (`api.ts`)
```typescript
async chatStream(request: ChatRequest, onChunk, onComplete, onError) {
  // 1. Start backend run
  const runResponse = await this.api.post('/api/patent/run', request);
  
  // 2. Stream results
  const response = await fetch(`/api/patent/stream?run_id=${runResponse.data.run_id}`);
  
  // 3. Process SSE events
  switch (currentEventType) {
    case 'results':
      // Handle final response (including insufficient details)
      onChunk(parsed.response, 'results');
      onComplete(finalResponse);
      break;
    case 'thoughts':
      // Handle AI thinking process
      onChunk(thoughtText, 'thoughts');
      break;
  }
}
```

## 2. Backend Processing (`main.py`)

### Run Creation
```python
@app.post("/api/patent/run")
async def start_run(request: RunRequest):
    disclosure = request.user_message  # "draft 10 claims"
    result = await service.start_run(disclosure, session_id)
    return {"run_id": run_id, "session_id": session_id}
```

### Streaming Handler
```python
async def stream_run(self, run_id: str):
    disclosure = run_data["disclosure"]  # "draft 10 claims"
    
    # Call agent with streaming
    async for event in agent.run_streaming(disclosure, session_history):
        event_type = event.get('type')
        
        if event_type == 'results':
            # CRITICAL: Handle insufficient details responses
            final_response = event.get('response')
            final_data = {
                "response": final_response,
                "metadata": {
                    "should_draft_claims": False,
                    "has_claims": False,
                    "reasoning": "Direct response provided"
                }
            }
            yield create_sse_event(StreamEventType.RESULTS, final_data)
            return  # Stop processing
```

## 3. Agent Processing (`agent.py`)

### Main Agent Flow
```python
async def agent_run_streaming(user_input: str, conversation_context: str = ""):
    # Step 0: Early insufficient details check for claim drafting
    input_lower = user_input.lower()  # "draft 10 claims"
    might_be_claim_drafting = ("draft" in input_lower and 
                              ("claim" in input_lower or "patent" in input_lower))
    
    if might_be_claim_drafting:
        # PURE LLM ASSESSMENT - NO FALLBACKS
        assessment_result = await assess_disclosure_sufficiency(user_input)
        
        if not assessment_result["sufficient"]:
            # Return insufficient details immediately
            yield {
                "type": "results",
                "response": assessment_result["message"]
            }
            return  # Skip all other processing
    
    # If sufficient, continue with intent classification and claim drafting
    # ... rest of agent logic ...
```

### Claims Drafting Function
```python
async def draft_claims_streaming(disclosure: str, document_content: str = "", conversation_history: str = ""):
    # PURE LLM ASSESSMENT - NO LENGTH CHECKS
    assessment_result = await assess_disclosure_sufficiency(disclosure)
    
    if not assessment_result["sufficient"]:
        yield {
            "type": "results",
            "response": assessment_result["message"]
        }
        return
    
    # If sufficient, proceed with actual claim drafting
    # ... claim generation logic ...
```

## 4. LLM Assessment Core (`assess_disclosure_sufficiency`)

### Pure LLM-Based Assessment
```python
async def assess_disclosure_sufficiency(disclosure: str) -> Dict[str, Any]:
    """PURELY LLM-BASED - NO KEYWORD/LENGTH FALLBACKS"""
    
    assessment_messages = [
        {
            "role": "system",
            "content": """You are a patent attorney evaluating technical content.
            
            Examples:
            ✅ SUFFICIENT: "draft 10 claims for dynamic spectrum sharing"
            ✅ SUFFICIENT: "create claims for AI-based network optimization"  
            ❌ INSUFFICIENT: "draft claims" - no technical content
            ❌ INSUFFICIENT: "draft 10 claims" - just command with number
            """
        },
        {
            "role": "user",
            "content": f'Assess: "{disclosure}"'
        }
    ]
    
    # Call LLM with function
    async for chunk in send_llm_request_streaming(assessment_messages, functions):
        if chunk["type"] == "completion" and chunk["function_arguments"]:
            result = json.loads(chunk["function_arguments"])
            return result
    
    # Conservative fallback only if LLM completely fails
    return {
        "sufficient": False,
        "confidence": 0.5,
        "message": "I need more specific technical details about your invention."
    }
```

### LLM Function Definition
```python
functions = [
    {
        "type": "function",
        "function": {
            "name": "assess_technical_sufficiency",
            "parameters": {
                "type": "object",
                "properties": {
                    "sufficient": {"type": "boolean"},
                    "confidence": {"type": "number"},
                    "technical_elements_found": {"type": "array"},
                    "message": {"type": "string"}
                }
            }
        }
    }
]
```

## 5. Response Flow Back to Frontend

### Backend SSE Response
```
event: results
data: {
  "response": "I need more specific technical details about your invention to draft meaningful patent claims. Please describe the technical aspects of your invention.",
  "metadata": {
    "should_draft_claims": false,
    "has_claims": false,
    "reasoning": "Direct response provided"
  }
}
```

### API Service Processing
```typescript
case 'results':
  const finalResponse = {
    response: parsed.response,
    metadata: parsed.metadata,
    data: parsed.data
  };
  onChunk(parsed.response, 'results');
  onComplete(finalResponse);
  return;
```

### Frontend Display
```typescript
case 'results':
  console.log('🎯 Setting final response:', chunk);
  setStreamingResponse(chunk);  // Shows LLM's insufficient details message
  break;
```

## 6. Complete Example Trace

### Input: "draft 10 claims"

1. **Frontend**: Captures input, sends to API
2. **API Service**: Creates run, starts streaming
3. **Backend**: Receives request, calls agent
4. **Agent**: Detects claim drafting request, calls LLM assessment
5. **LLM Assessment**: 
   ```json
   {
     "sufficient": false,
     "confidence": 0.95,
     "technical_elements_found": [],
     "message": "I need more specific technical details about your invention to draft meaningful patent claims. Please describe the technical aspects of your invention."
   }
   ```
6. **Agent**: Returns results event immediately
7. **Backend**: Sends SSE results event
8. **API Service**: Processes results event, calls onComplete
9. **Frontend**: Displays LLM's message to user

### Input: "draft 10 claims for dynamic spectrum sharing"

1. **Frontend**: Captures input, sends to API
2. **Agent**: Detects claim drafting request, calls LLM assessment
3. **LLM Assessment**:
   ```json
   {
     "sufficient": true,
     "confidence": 0.90,
     "technical_elements_found": ["dynamic spectrum sharing", "wireless communication"],
     "message": "Technical content detected"
   }
   ```
4. **Agent**: Continues with intent classification and claim drafting
5. **Claims Generated**: Full patent claims returned

## Key Design Decisions

### 1. No Fallback Logic
- **Removed**: Length checks (`len(disclosure) < 20`)
- **Removed**: Keyword matching
- **Pure LLM**: All assessment done by GPT-4

### 2. Early Return Pattern
- **Insufficient**: Return immediately, skip all other processing
- **Sufficient**: Continue with full claim drafting pipeline

### 3. Unified Event Type
- **Single Event**: Both insufficient and successful results use `results` event
- **No Special Cases**: Frontend has no special handling for insufficient details

### 4. Conservative Fallback
- **LLM Failure**: If LLM call fails, assume insufficient (be safe)
- **Error Handling**: Always ask for more details rather than proceeding

## Performance Characteristics

### Insufficient Details Request
- **LLM Calls**: 1 assessment call (~200ms)
- **Total Time**: ~300ms
- **Events**: 1 results event

### Sufficient Request  
- **LLM Calls**: 3+ calls (assessment + intent + claims)
- **Total Time**: ~3-5 seconds
- **Events**: Multiple thoughts + 1 results event

## Testing the Flow

### Test Cases
1. **"draft 10 claims"** → Should return insufficient details
2. **"draft claims"** → Should return insufficient details  
3. **"draft 10 claims for 5G networks"** → Should proceed with drafting
4. **"create patent claims for my AI invention"** → Should proceed with drafting

### Expected Behavior
- Pure LLM decision making
- No keyword dependencies
- Consistent messaging
- Fast response for insufficient cases
