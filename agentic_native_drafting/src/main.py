import uuid
import asyncio
import json
import os
from typing import Dict, Any
from datetime import datetime
from enum import Enum

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from .agent import agent_with_thoughts
from .models import AgentResponse

class StreamEventType(str, Enum):
    """Ultra-simplified streaming events - just what we actually need"""
    # Core event types
    THOUGHTS = "thoughts"           # All AI thinking/reasoning/progress → Small streaming bubbles  
    RESULTS = "results"             # Final results/completion → Large final bubble
    ERROR = "error"                 # Error states → Error handling

class ThoughtEventData(BaseModel):
    """Structure for thought events"""
    thought_type: str
    content: str
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = {}
    timestamp: str = datetime.now().isoformat()

def create_sse_event(event_type: StreamEventType, data: Dict[str, Any]) -> str:
    """Create a Server-Sent Event formatted message with enhanced data"""
    # Add timestamp to all events
    if "timestamp" not in data:
        data["timestamp"] = datetime.now().isoformat()
    
    return f"event: {event_type.value}\ndata: {json.dumps(data, default=str)}\n\n"

# Validate environment variables
def validate_environment():
    """Validate that required environment variables are loaded"""
    required_vars = [
        "AZURE_OPENAI_ENDPOINT",
        "AZURE_OPENAI_API_KEY", 
        "AZURE_OPENAI_DEPLOYMENT_NAME",
        "AZURE_OPENAI_API_VERSION"
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        return False
    
    print("✅ All required environment variables are loaded")
    return True

if not validate_environment():
    raise RuntimeError("Environment validation failed. Please check your .env file.")

app = FastAPI(
    title="Simplified Patent Drafting API with Streaming Thoughts",
    description="""
    ## AI-Powered Patent Drafting with Simplified Real-time Streaming
    
    This simplified API provides patent drafting assistance with clean, streamlined
    real-time streaming of AI thoughts and final results.
    
    ### Simplified Architecture in v3.0
    - **4 Event Types Only**: thoughts, results, error, low_confidence
    - **Clean Thought Stream**: Only meaningful AI reasoning, no noise
    - **Clear Results**: Final outputs clearly separated from thoughts
    - **Better UX**: Reduced complexity, improved performance
    
    ### Streaming Event Types (Simplified)
    - `thoughts` - All AI reasoning and decision-making content
    - `results` - Final completed results and outputs
    - `error` - Error states and messages
    - `low_confidence` - When AI needs clarification from user
    
    ### Usage
    1. Start a patent drafting run with `/api/patent/run`
    2. Stream real-time results with `/api/patent/stream`
    3. Receive clean thought streams and clear final results
    4. Simple 4-event architecture for easy frontend integration
    """,
    version="3.0.0",
    terms_of_service="https://novitai.com/terms",
    contact={
        "name": "Novitai API Support",
        "url": "https://novitai.com/support",
        "email": "api-support@novitai.com",
    }
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EnhancedPatentService:
    def __init__(self):
        self._runs: Dict[str, Dict[str, Any]] = {}
        self._sessions: Dict[str, Dict[str, Any]] = {}
        self._session_history: Dict[str, str] = {}
        self._performance_metrics: Dict[str, List[float]] = {}

    async def start_run(self, disclosure: str, session_id: str = None) -> Dict[str, str]:
        """Start a new patent drafting run or continue existing session"""
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
        
        # Create run with enhanced metadata
        self._runs[run_id] = {
            "run_id": run_id,
            "session_id": session_id,
            "disclosure": disclosure,
            "status": "started",
            "created_at": datetime.now().isoformat(),
            "metrics": {
                "start_time": datetime.now().timestamp(),
                "events_streamed": 0,
                "thoughts_generated": 0
            }
        }
        
        # Initialize session history if new session
        if session_id not in self._session_history:
            self._session_history[session_id] = ""
        
        return {"run_id": run_id, "session_id": session_id}

    def _add_to_session_history(self, session_id: str, user_input: str, agent_response: str):
        """Add conversation to session-level history"""
        if session_id in self._session_history:
            conversation_entry = f"User: {user_input}\nAgent: {agent_response}\n---\n"
            self._session_history[session_id] += conversation_entry
        else:
            self._session_history[session_id] = f"User: {user_input}\nAgent: {agent_response}\n---\n"

    def _get_session_history(self, session_id: str) -> str:
        """Get the complete session history for context building"""
        history = self._session_history.get(session_id, "")
        if history:
            max_length = 8000
            if len(history) > max_length:
                history = "..." + history[-max_length:]
                print(f"⚠️  Session history truncated for session {session_id}")
        return history

    async def get_run_details(self, run_id: str) -> Dict[str, Any]:
        """Get run details with enhanced metrics"""
        if run_id not in self._runs:
            raise HTTPException(status_code=404, detail="Run not found")
        return self._runs[run_id]

    def _update_run_metrics(self, run_id: str, metric: str, value: Any = None):
        """Update run metrics"""
        if run_id in self._runs:
            if metric == "event_streamed":
                self._runs[run_id]["metrics"]["events_streamed"] += 1
            elif metric == "thought_generated":
                self._runs[run_id]["metrics"]["thoughts_generated"] += 1
            elif metric == "end_time":
                self._runs[run_id]["metrics"]["end_time"] = datetime.now().timestamp()
                start_time = self._runs[run_id]["metrics"]["start_time"]
                self._runs[run_id]["metrics"]["duration_seconds"] = datetime.now().timestamp() - start_time

    async def stream_run(self, run_id: str):
        """Enhanced streaming with LLM decision thoughts"""
        try:
            if run_id not in self._runs:
                yield create_sse_event(StreamEventType.ERROR, {'error': 'Run not found'})
                return
                
            run_data = self._runs[run_id]
            disclosure = run_data["disclosure"]
            self._runs[run_id]["status"] = "processing"
            
            try:
                session_history = self._get_session_history(run_data["session_id"])
                if session_history:
                    print(f"🔍 Using session context ({len(session_history)} chars) for run {run_id}")
                
                # Use the streaming agent with simplified event handling
                final_response = ""
                events_received = 0
                async for event in agent_with_thoughts.run_streaming(disclosure, session_history):
                    event_type = event.get('type', 'unknown')
                    events_received += 1
                    print(f"🔍 Backend received event #{events_received}: {event_type} - {str(event)[:200]}...")  # Debug logging
                    self._update_run_metrics(run_id, "event_streamed")
                    
                    # Ultra-simplified event handling - everything is either a thought or final result
                    if event_type == 'low_confidence':
                        # Treat low confidence as a special thought, not a separate event type
                        self._update_run_metrics(run_id, "thought_generated")
                        clarification_msg = f"❓ {event.get('text', 'I need more information to help you effectively.')}"
                        yield create_sse_event(StreamEventType.THOUGHTS, {
                            'content': clarification_msg,
                            'event_type': 'low_confidence',  # Keep original type for debugging
                            'metadata': {
                                'confidence': event.get('confidence', 0.0),
                                'suggestions': event.get('suggestions', [])
                            }
                        })
                        # Don't return - continue processing, this isn't a terminal event
                        
                    elif event_type == 'complete':
                        # Final completion with results
                        final_response = event.get('response', 'Process completed')
                        print(f"🎯 Emitting RESULTS event with response: {final_response[:100]}...")  # Debug logging
                        
                        final_data = {
                            "response": final_response,
                            "metadata": event.get('metadata', {}),
                            "data": event.get('data', {}),
                            "performance": {
                                "events_streamed": self._runs[run_id]["metrics"]["events_streamed"],
                                "thoughts_generated": self._runs[run_id]["metrics"]["thoughts_generated"]
                            }
                        }
                        
                        self._runs[run_id]["status"] = "completed"
                        self._update_run_metrics(run_id, "end_time")
                        
                        # Add to session history
                        self._add_to_session_history(run_data["session_id"], disclosure, final_response)
                        print(f"💾 Updated session history for session {run_data['session_id']}")
                        
                        yield create_sse_event(StreamEventType.RESULTS, final_data)
                        return  # Important: stop processing after completion
                        
                    elif event_type == 'error':
                        # Handle errors from agent
                        error_msg = event.get('error', 'Unknown error')
                        print(f"❌ Agent error: {error_msg}")
                        yield create_sse_event(StreamEventType.ERROR, {
                            'error': error_msg,
                            'context': 'agent_error',
                            'text': event.get('text', f'Error: {error_msg}')
                        })
                        return
                        
                    else:
                        # Everything else is a "thought" - reasoning, progress, analysis, etc.
                        self._update_run_metrics(run_id, "thought_generated")
                        
                        # Extract and clean meaningful content from any event type
                        raw_content = (
                            event.get('content') or 
                            event.get('text') or 
                            event.get('message') or
                            event.get('reasoning') or  # For intent_classified events
                            ""
                        )
                        
                        # Clean up verbose content for better UX
                        if raw_content and raw_content.strip():
                            # For very long reasoning text, provide a summary instead
                            if len(raw_content) > 200:
                                # Extract the key insight from verbose reasoning
                                if "intent" in event_type.lower() and "classification" in raw_content.lower():
                                    thought_content = f"Analyzing request intent for {event.get('intent', 'unknown')} classification..."
                                elif "claim" in event_type.lower():
                                    thought_content = "Analyzing patent claim requirements and structure..."
                                elif "analysis" in event_type.lower():
                                    thought_content = "Performing technical analysis of the invention..."
                                else:
                                    # Take first meaningful sentence
                                    sentences = raw_content.split('.')
                                    thought_content = sentences[0][:150] + "..." if sentences[0] else f"Processing {event_type}..."
                            else:
                                thought_content = raw_content
                            
                            yield create_sse_event(StreamEventType.THOUGHTS, {
                                'content': thought_content,
                                'event_type': event_type,  # Keep original type for debugging
                                'metadata': event.get('metadata', {})
                            })
                
                # Fallback: If we reach here without a complete event, send a default response
                if events_received > 0:
                    print(f"⚠️ No complete event received after {events_received} events, sending fallback response")
                    fallback_response = {
                        "response": "I've analyzed your request. Please let me know if you need any clarification or have additional questions.",
                        "metadata": {
                            "should_draft_claims": False,
                            "has_claims": False,
                            "reasoning": "Partial processing completed"
                        },
                        "performance": {
                            "events_streamed": self._runs[run_id]["metrics"]["events_streamed"],
                            "thoughts_generated": self._runs[run_id]["metrics"]["thoughts_generated"]
                        }
                    }
                    self._runs[run_id]["status"] = "completed"
                    self._update_run_metrics(run_id, "end_time")
                    yield create_sse_event(StreamEventType.RESULTS, fallback_response)
                
            except Exception as e:
                print(f"❌ Agent execution failed: {e}")
                fallback_response = {
                    "response": "I encountered an issue processing your request. Please try again or provide more details about your invention.",
                    "metadata": {"error": str(e), "should_draft_claims": False, "has_claims": False},
                    "performance": {
                        "events_streamed": self._runs[run_id]["metrics"]["events_streamed"],
                        "thoughts_generated": self._runs[run_id]["metrics"]["thoughts_generated"]
                    }
                }
                self._runs[run_id]["status"] = "error"
                self._runs[run_id]["error"] = str(e)
                yield create_sse_event(StreamEventType.ERROR, {'error': str(e), 'context': 'agent_execution'})
                yield create_sse_event(StreamEventType.RESULTS, fallback_response)
                
        except Exception as e:
            print(f"❌ Stream execution failed: {e}")
            yield create_sse_event(StreamEventType.ERROR, {'error': str(e), 'context': 'stream_execution'})

class ConversationTurn(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class DocumentContentModel(BaseModel):
    text: str
    paragraphs: Optional[List[str]] = None
    selection: Optional[dict] = None

class RunRequest(BaseModel):
    user_message: Optional[str] = None
    conversation_history: Optional[List[ConversationTurn]] = None
    document_content: Optional[DocumentContentModel] = None
    disclosure: Optional[str] = None  # legacy
    session_id: Optional[str] = None
    enable_thoughts: Optional[bool] = True  # NEW: Option to enable/disable thought streaming

# Initialize enhanced service
service = EnhancedPatentService()

@app.post("/api/patent/run", tags=["Patent Drafting"])
async def start_run(request: RunRequest):
    """
    Start a new simplified patent drafting run.
    
    Initiates a new patent drafting session with clean, simplified streaming
    that's easy to integrate and debug.
    
    ### Simplified Features:
    - **Clean Events**: Just 4 event types instead of 18+
    - **Better UX**: Clear separation of thoughts vs results
    - **Easy Integration**: No complex event mapping needed
    
    ### Request Body:
    - **user_message**: Natural language description of the invention
    - **document_content**: Optional Word document content for context
    - **conversation_history**: Previous messages for context
    - **session_id**: Optional ID to continue existing session
    
    Returns a unique run_id for streaming the response.
    """
    try:
        disclosure = request.user_message or request.disclosure or ""
        session_id = request.session_id
        
        if not disclosure:
            raise HTTPException(status_code=400, detail="Disclosure or user_message is required")
        
        result = await service.start_run(disclosure, session_id)
        
        # Store enhanced request metadata
        try:
            service._runs[result["run_id"]]["raw_request"] = {
                **request.dict(),
                "enable_thoughts": request.enable_thoughts
            }
        except Exception:
            pass
            
        return {
            **result,
            "features": {
                "thoughts_enabled": request.enable_thoughts,
                "enhanced_streaming": True,
                "performance_tracking": True
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error starting enhanced run: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patent/run/{run_id}", tags=["Patent Drafting"])
async def get_run_details(run_id: str):
    """
    Get detailed information about a patent drafting run with enhanced metrics.
    
    Retrieves complete run information including status, results, performance
    metrics, and LLM decision thought statistics.
    """
    try:
        return await service.get_run_details(run_id)
    except Exception as e:
        print(f"❌ Error getting run details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patent/stream", tags=["Patent Drafting"])
async def stream_run(run_id: str):
    """
    Stream simplified patent drafting results.
    
    Uses Server-Sent Events (SSE) with a clean, simple architecture:
    - AI thoughts and reasoning in real-time
    - Clear final results with structured data
    - Simple error handling and recovery
    
    ### Simplified Event Types:
    - **thoughts**: All AI thinking, reasoning, progress updates
    - **results**: Final completion with structured data
    - **error**: Error states with helpful context
    - **low_confidence**: When AI needs clarification
    
    ### Usage:
    ```javascript
    const eventSource = new EventSource('/api/patent/stream?run_id=' + runId);
    
    eventSource.addEventListener('thoughts', (event) => {
        const thoughtData = JSON.parse(event.data);
        console.log('AI Thinking:', thoughtData.content);
    });
    
    eventSource.addEventListener('results', (event) => {
        const result = JSON.parse(event.data);
        console.log('Final Result:', result.response);
        // result.data contains claims, metadata, etc.
    });
    ```
    """
    async def event_generator():
        try:
            async for event in service.stream_run(run_id):
                yield event
        except Exception as e:
            print(f"❌ Enhanced stream error: {e}")
            yield create_sse_event(StreamEventType.ERROR, {
                'error': str(e), 
                'context': 'event_generator',
                'timestamp': datetime.now().isoformat()
            })
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*",
            "X-Enhanced-Streaming": "true",
            "X-Thoughts-Enabled": "true"
        }
    )

@app.get("/api/debug/env", tags=["Debug"])
async def debug_env():
    """Check environment variables status with enhanced diagnostics."""
    def mask(val: str):
        if not val:
            return None
        if len(val) <= 8:
            return "***"
        return f"{val[:4]}...{val[-4:]}"

    return {
        "AZURE_OPENAI_ENDPOINT": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "AZURE_OPENAI_API_VERSION": os.getenv("AZURE_OPENAI_API_VERSION"),
        "AZURE_OPENAI_DEPLOYMENT_NAME": os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),
        "AZURE_OPENAI_API_KEY": mask(os.getenv("AZURE_OPENAI_API_KEY")),
        "agent_type": "enhanced_with_thoughts_v2",
        "features": {
            "streaming_thoughts": True,
            "enhanced_events": True,
            "performance_tracking": True,
            "better_error_handling": True
        }
    }

@app.get("/api/sessions", tags=["Session Management"])
async def list_sessions():
    """List all active conversation sessions with enhanced metrics."""
    try:
        sessions = []
        for session_id, session_data in service._sessions.items():
            # Calculate session metrics
            total_thoughts = sum(
                service._runs.get(run_id, {}).get("metrics", {}).get("thoughts_generated", 0)
                for run_id in session_data["runs"]
            )
            
            sessions.append({
                "session_id": session_id,
                "started_at": session_data["started_at"],
                "topic": session_data["topic"],
                "total_runs": len(session_data["runs"]),
                "last_run": session_data["runs"][-1] if session_data["runs"] else None,
                "total_thoughts_generated": total_thoughts
            })
        
        return {
            "total_sessions": len(sessions),
            "sessions": sessions,
            "enhanced_features": True
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/debug/performance", tags=["Debug"])
async def get_performance_metrics():
    """Get system performance metrics and statistics."""
    try:
        total_runs = len(service._runs)
        completed_runs = len([r for r in service._runs.values() if r["status"] == "completed"])
        total_thoughts = sum(
            run.get("metrics", {}).get("thoughts_generated", 0) 
            for run in service._runs.values()
        )
        
        avg_duration = 0
        if completed_runs > 0:
            durations = [
                run.get("metrics", {}).get("duration_seconds", 0)
                for run in service._runs.values()
                if run["status"] == "completed" and run.get("metrics", {}).get("duration_seconds")
            ]
            if durations:
                avg_duration = sum(durations) / len(durations)
        
        return {
            "total_runs": total_runs,
            "completed_runs": completed_runs,
            "error_runs": len([r for r in service._runs.values() if r["status"] == "error"]),
            "total_sessions": len(service._sessions),
            "total_thoughts_generated": total_thoughts,
            "avg_completion_time_seconds": round(avg_duration, 2),
            "avg_thoughts_per_run": round(total_thoughts / max(total_runs, 1), 1)
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/prior-art/search", tags=["Prior Art Search"])
async def search_prior_art(query: str, max_results: int = 20):
    """
    Perform prior art search using the PatentSearchEngine.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to return (default: 20)
    
    Returns:
        Prior art search results with patent information
    """
    try:
        from .prior_art_search import PatentSearchEngine, PatentSearchConfig
        
        # Create search configuration
        config = PatentSearchConfig()
        config.default_max_results = max_results
        
        # Initialize search engine
        search_engine = PatentSearchEngine(config)
        
        # Perform search using the correct method
        search_result = await search_engine.search(
            query=query,
            max_results=max_results
        )
        
        return {
            "query": query,
            "total_results": len(search_result.patents) if hasattr(search_result, 'patents') else 0,
            "results": search_result.patents if hasattr(search_result, 'patents') else [],
            "status": "success",
            "search_result": search_result
        }
        
    except Exception as e:
        print(f"❌ Prior art search failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Prior art search failed: {str(e)}"
        )

@app.get("/", tags=["System"])
async def root():
    """
    Enhanced API health check and service information.
    
    Returns comprehensive service information including new features
    and capabilities for LLM decision thought streaming.
    """
    return {
        "service": "Enhanced Patent Drafting Service with LLM Thoughts",
        "version": "2.0",
        "features": [
            "draft_claims", 
            "general_conversation", 
            "prior_art_search",
            "llm_decision_thoughts",
            "enhanced_streaming", 
            "performance_tracking"
        ],
        "new_capabilities": {
            "thought_streaming": "Real-time LLM decision thoughts",
            "enhanced_events": "More granular streaming events",
            "performance_metrics": "Built-in timing and statistics",
            "better_errors": "Detailed error context and recovery"
        },
        "status": "operational"
    }