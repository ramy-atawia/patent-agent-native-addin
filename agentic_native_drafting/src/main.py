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

from .agent import agent
from .models import AgentResponse

class StreamEventType(str, Enum):
    """Types of streaming events"""
    INTENT_ANALYSIS = "intent_analysis"
    INTENT_CLASSIFIED = "intent_classified" 
    CLAIMS_DRAFTING_START = "claims_drafting_start"
    CLAIMS_PROGRESS = "claims_progress"
    CLAIMS_COMPLETE = "claims_complete"
    PRIOR_ART_START = "prior_art_start"
    PRIOR_ART_PROGRESS = "prior_art_progress"
    PRIOR_ART_COMPLETE = "prior_art_complete"
    ERROR = "error"
    COMPLETE = "complete"

def create_sse_event(event_type: StreamEventType, data: Dict[str, Any]) -> str:
    """Create a Server-Sent Event formatted message"""
    return f"event: {event_type.value}\ndata: {json.dumps(data)}\n\n"

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
    title="Novitai Patent Drafting API",
    description="""
    ## AI-Powered Patent Drafting and Prior Art Research API
    
    This API provides comprehensive patent drafting assistance powered by Azure OpenAI.
    It offers intelligent patent claim generation, prior art research, and real-time 
    streaming responses for an interactive user experience.
    
    ### Key Features
    - **AI-Powered Patent Drafting**: Generate professional patent claims using advanced LLM
    - **Prior Art Research**: Intelligent search and analysis of existing patents  
    - **Real-time Streaming**: Server-sent events for live response streaming
    - **Session Management**: Conversation context and history tracking
    - **Document Integration**: Support for Word document content analysis
    
    ### Usage
    1. Start a patent drafting run with `/api/patent/run`
    2. Stream real-time results with `/api/patent/stream`
    3. All requests (prior art + claims) go through the unified streaming pipeline
    4. Manage sessions with `/api/sessions`
    """,
    version="1.0.0",
    terms_of_service="https://novitai.com/terms",
    contact={
        "name": "Novitai API Support",
        "url": "https://novitai.com/support",
        "email": "api-support@novitai.com",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "http://localhost:8000", "description": "Development server"},
        {"url": "https://api.novitai.com", "description": "Production server"},
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SimplePatentService:
    def __init__(self):
        self._runs: Dict[str, Dict[str, Any]] = {}
        self._sessions: Dict[str, Dict[str, Any]] = {}  # Session management
        self._session_history: Dict[str, str] = {}      # Session-level history

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

    def _add_to_session_history(self, session_id: str, user_input: str, agent_response: str):
        """Add conversation to session-level history"""
        if session_id in self._session_history:
            conversation_entry = f"User: {user_input}\nAgent: {agent_response}\n---\n"
            self._session_history[session_id] += conversation_entry
        else:
            # Initialize session history if it doesn't exist
            self._session_history[session_id] = f"User: {user_input}\nAgent: {agent_response}\n---\n"

    def _get_session_history(self, session_id: str) -> str:
        """Get the complete session history for context building"""
        history = self._session_history.get(session_id, "")
        if history:
            # Truncate very long histories to prevent context overflow
            max_length = 8000  # Reasonable limit for LLM context
            if len(history) > max_length:
                # Keep the most recent conversations (last 8000 chars)
                history = "..." + history[-max_length:]
                print(f"⚠️  Session history truncated for session {session_id} (was {len(self._session_history[session_id])} chars)")
        return history

    async def get_run_details(self, run_id: str) -> Dict[str, Any]:
        """Get run details"""
        if run_id not in self._runs:
            raise HTTPException(status_code=404, detail="Run not found")
        return self._runs[run_id]

    async def stream_run(self, run_id: str):
        """Stream patent drafting run with true step-by-step streaming"""
        try:
            if run_id not in self._runs:
                yield create_sse_event(StreamEventType.ERROR, {'error': 'Run not found'})
                yield create_sse_event(StreamEventType.COMPLETE, {})
                return
                
            run_data = self._runs[run_id]
            disclosure = run_data["disclosure"]
            self._runs[run_id]["status"] = "processing"
            
            try:
                session_history = self._get_session_history(run_data["session_id"])
                if session_history:
                    print(f"🔍 Using session context ({len(session_history)} chars) for run {run_id}")
                else:
                    print(f"🆕 No session context available for run {run_id}")
                
                # Use the new streaming agent method
                async for event in agent.run_streaming(disclosure, session_history):
                    event_type = event.get('type', 'unknown')
                    
                    if event_type == 'intent_analysis':
                        yield create_sse_event(StreamEventType.INTENT_ANALYSIS, {
                            'text': event.get('message', 'Analyzing request...'),
                            'user_input': event.get('user_input', disclosure[:100] + "...")
                        })
                        
                    elif event_type == 'intent_classified':
                        yield create_sse_event(StreamEventType.INTENT_CLASSIFIED, {
                            'text': event.get('reasoning', 'Intent classified'),
                            'intent_type': event.get('intent', 'unknown'),
                            'confidence': event.get('confidence_score', 0.0)
                        })
                        
                    elif event_type == 'low_confidence':
                        yield create_sse_event(StreamEventType.ERROR, {
                            'error': event.get('message', 'Low confidence - needs clarification'),
                            'confidence': event.get('confidence', 0.0)
                        })
                        return
                        
                    elif event_type == 'claims_drafting_start':
                        yield create_sse_event(StreamEventType.CLAIMS_DRAFTING_START, {
                            'text': event.get('message', 'Starting claims drafting...'),
                            'disclosure_length': event.get('disclosure_length', len(disclosure))
                        })
                        
                    elif event_type == 'claims_progress':
                        yield create_sse_event(StreamEventType.CLAIMS_PROGRESS, {
                            'text': event.get('message', 'Processing...'),
                            'stage': event.get('stage', 'unknown')
                        })
                        
                    elif event_type == 'claim_generated':
                        yield create_sse_event(StreamEventType.CLAIMS_PROGRESS, {
                            'claim_number': event.get('claim_number', 0),
                            'text': event.get('text', ''),
                            'total_claims': event.get('total_claims', 0)
                        })
                        
                    elif event_type == 'claims_complete':
                        yield create_sse_event(StreamEventType.CLAIMS_COMPLETE, {
                            'text': event.get('message', 'Claims complete'),
                            'num_claims': event.get('num_claims', 0),
                            'claims': event.get('claims', [])
                        })
                        
                    elif event_type == 'prior_art_start':
                        yield create_sse_event(StreamEventType.PRIOR_ART_START, {
                            'text': event.get('message', 'Starting prior art search...')
                        })
                        
                    elif event_type == 'prior_art_progress':
                        yield create_sse_event(StreamEventType.PRIOR_ART_PROGRESS, {
                            'text': event.get('message', 'Searching...'),
                            'stage': event.get('stage', 'unknown')
                        })
                        
                    elif event_type == 'prior_art_complete':
                        yield create_sse_event(StreamEventType.PRIOR_ART_COMPLETE, {
                            'text': event.get('message', 'Prior art search complete'),
                            'results': event.get('results', ''),
                            'patents_found': event.get('patents_found', 0)
                        })
                        
                    elif event_type == 'review_start':
                        yield create_sse_event(StreamEventType.CLAIMS_PROGRESS, {
                            'text': event.get('message', 'Starting review...'),
                            'stage': 'review_start'
                        })
                        
                    elif event_type == 'review_progress':
                        yield create_sse_event(StreamEventType.CLAIMS_PROGRESS, {
                            'text': event.get('message', 'Reviewing...'),
                            'stage': event.get('stage', 'unknown')
                        })
                        
                    elif event_type == 'review_complete':
                        yield create_sse_event(StreamEventType.CLAIMS_COMPLETE, {
                            'text': event.get('message', 'Review complete'),
                            'review_comments': event.get('review_comments', [])
                        })
                        
                    elif event_type == 'processing':
                        yield create_sse_event(StreamEventType.CLAIMS_PROGRESS, {
                            'text': event.get('message', 'Processing...'),
                            'stage': 'processing'
                        })
                        
                    elif event_type == 'complete':
                        # Final completion
                        final_data = {
                            "response": event.get('response', 'Process completed'),
                            "metadata": {
                                "should_draft_claims": event_type in ['claims_complete', 'claim_generated'],
                                "has_claims": event_type == 'claims_complete',
                                "reasoning": event.get('message', 'Process completed')
                            }
                        }
                        
                        if event_type == 'claims_complete' and event.get('claims'):
                            final_data["data"] = {
                                "claims": event.get('claims', []),
                                "num_claims": event.get('num_claims', 0)
                            }
                        
                        self._runs[run_id]["status"] = "completed"
                        self._add_to_session_history(run_data["session_id"], disclosure, final_data["response"])
                        print(f"💾 Updated session history for session {run_data['session_id']}")
                        
                        yield create_sse_event(StreamEventType.COMPLETE, final_data)
                        
                    elif event_type == 'error':
                        yield create_sse_event(StreamEventType.ERROR, {
                            'error': event.get('error', 'Unknown error'),
                            'message': event.get('message', 'Error occurred')
                        })
                        return
                
            except Exception as e:
                print(f"❌ Agent execution failed: {e}")
                fallback_response = {
                    "response": "I encountered an issue processing your request. Please try again or provide more details about your invention.",
                    "metadata": {"error": str(e), "should_draft_claims": False, "has_claims": False}
                }
                self._runs[run_id]["status"] = "error"
                self._runs[run_id]["error"] = str(e)
                yield create_sse_event(StreamEventType.ERROR, {'error': str(e)})
                yield create_sse_event(StreamEventType.COMPLETE, fallback_response)
                
        except Exception as e:
            print(f"❌ Stream execution failed: {e}")
            yield create_sse_event(StreamEventType.ERROR, {'error': str(e)})
            yield create_sse_event(StreamEventType.COMPLETE, {})


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

    def _add_to_session_history(self, session_id: str, user_input: str, agent_response: str):
        """Add conversation to session-level history"""
        if session_id in self._session_history:
            conversation_entry = f"User: {user_input}\nAgent: {agent_response}\n---\n"
            self._session_history[session_id] += conversation_entry
        else:
            # Initialize session history if it doesn't exist
            self._session_history[session_id] = f"User: {user_input}\nAgent: {agent_response}\n---\n"

    def _get_session_history(self, session_id: str) -> str:
        """Get the complete session history for context building"""
        history = self._session_history.get(session_id, "")
        if history:
            # Truncate very long histories to prevent context overflow
            max_length = 8000  # Reasonable limit for LLM context
            if len(history) > max_length:
                # Keep the most recent conversations (last 8000 chars)
                history = "..." + history[-max_length:]
                print(f"⚠️  Session history truncated for session {session_id} (was {len(self._session_history[session_id])} chars)")
        return history

    async def get_run_details(self, run_id: str) -> Dict[str, Any]:
        """Get run details"""
        if run_id not in self._runs:
            raise HTTPException(status_code=404, detail="Run not found")
        
        return self._runs[run_id]

    async def stream_run(self, run_id: str):
        """Stream patent drafting run"""
        try:
            if run_id not in self._runs:
                yield f"event: error\ndata: {json.dumps({'error': 'Run not found'})}\n\n"
                yield "event: done\ndata: {}\n\n"
                return
            
            run_data = self._runs[run_id]
            disclosure = run_data["disclosure"]
            
            # Update status
            self._runs[run_id]["status"] = "processing"
            
            yield f"event: status\ndata: {json.dumps({'status': 'processing', 'message': 'Analyzing your request...'})}\n\n"
            await asyncio.sleep(1)
            
            # Use the agent with session history context
            try:
                # Get session history for context building BEFORE calling agent
                session_history = self._get_session_history(run_data["session_id"])
                
                # Log session context for debugging
                if session_history:
                    print(f"🔍 Using session context ({len(session_history)} chars) for run {run_id}")
                else:
                    print(f"🆕 No session context available for run {run_id}")
                
                # Pass session history to agent
                agent_response = await agent.run(disclosure, session_history)
                
                # Stream reasoning
                yield f"event: reasoning\ndata: {json.dumps({'text': agent_response.reasoning})}\n\n"
                await asyncio.sleep(1)
                
                # Add search progress events for prior art requests
                if "prior art" in agent_response.reasoning.lower() or "search" in agent_response.reasoning.lower():
                    yield f"event: search_progress\ndata: {json.dumps({'step': 'searching', 'message': 'Searching patent databases...'})}\n\n"
                    await asyncio.sleep(0.5)
                    yield f"event: search_progress\ndata: {json.dumps({'step': 'analyzing', 'message': 'Analyzing search results...'})}\n\n"
                    await asyncio.sleep(0.5)
                
                # Add report drafting progress events
                if "report" in agent_response.reasoning.lower() or "analysis" in agent_response.reasoning.lower():
                    yield f"event: report_progress\ndata: {json.dumps({'step': 'structuring', 'message': 'Structuring the report...'})}\n\n"
                    await asyncio.sleep(0.5)
                    yield f"event: report_progress\ndata: {json.dumps({'step': 'formatting', 'message': 'Formatting content...'})}\n\n"
                    await asyncio.sleep(0.5)
                
                if agent_response.should_draft_claims:
                    yield f"event: tool_call\ndata: {json.dumps({'tool': 'draft_claims', 'num_claims': len(agent_response.claims or [])})}\n\n"
                    await asyncio.sleep(1)
                    
                    yield f"event: tool_result\ndata: {json.dumps({'tool': 'draft_claims', 'success': True, 'claims_generated': len(agent_response.claims or [])})}\n\n"
                    await asyncio.sleep(1)
                
                # Prepare final response
                final_data = {
                    "response": agent_response.conversation_response,
                    "metadata": {
                        "should_draft_claims": agent_response.should_draft_claims,
                        "has_claims": bool(agent_response.claims),
                        "reasoning": agent_response.reasoning
                    }
                }
                
                if agent_response.claims:
                    final_data["data"] = {
                        "claims": agent_response.claims,
                        "num_claims": len(agent_response.claims)
                    }
                
                # Update run status first
                self._runs[run_id]["status"] = "completed"
                self._runs[run_id]["result"] = agent_response
                
                # Store conversation in session history AFTER successful completion
                self._add_to_session_history(run_data["session_id"], disclosure, agent_response.conversation_response)
                print(f"💾 Updated session history for session {run_data['session_id']}")
                
                yield f"event: results\ndata: {json.dumps(final_data)}\n\n"
                await asyncio.sleep(0.5)
                yield "event: done\ndata: {}\n\n"
                
            except Exception as e:
                print(f"❌ Agent execution failed: {e}")
                
                fallback_response = {
                    "response": "I encountered an issue processing your request. Please try again or provide more details about your invention.",
                    "metadata": {
                        "error": str(e),
                        "should_draft_claims": False,
                        "has_claims": False
                    }
                }
                
                self._runs[run_id]["status"] = "error"
                self._runs[run_id]["error"] = str(e)
                
                yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
                yield f"event: results\ndata: {json.dumps(fallback_response)}\n\n"
                yield "event: done\ndata: {}\n\n"
                
        except Exception as e:
            print(f"❌ Stream execution failed: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
            yield "event: done\ndata: {}\n\n"

# Initialize service
service = SimplePatentService()

@app.post("/api/patent/run", tags=["Patent Drafting"])
async def start_run(request: RunRequest):
    """
    Start a new patent drafting run.
    
    Initiates a new patent drafting session or continues an existing one.
    This endpoint accepts user input and document content to generate patent claims
    and professional responses using AI.
    
    - **user_message**: Natural language description of the invention
    - **document_content**: Optional Word document content for context
    - **conversation_history**: Previous messages for context
    - **session_id**: Optional ID to continue existing session
    
    Returns a unique run_id for streaming the response.
    """
    try:
        # Prefer user_message if provided, otherwise fall back to legacy disclosure
        disclosure = request.user_message or request.disclosure or ""
        session_id = request.session_id
        
        if not disclosure:
            raise HTTPException(status_code=400, detail="Disclosure or user_message is required")
        
        result = await service.start_run(disclosure, session_id)
        # store raw request for traceability
        try:
            service._runs[result["run_id"]]["raw_request"] = request.dict()
        except Exception:
            pass
        return result
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error starting run: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Prior art endpoint removed - now handled through streaming pipeline
# All requests (prior art + claims) go through /api/patent/run + /api/patent/stream

@app.get("/api/patent/run/{run_id}", tags=["Patent Drafting"])
async def get_run_details(run_id: str):
    """
    Get detailed information about a patent drafting run.
    
    Retrieves the complete run information including status, results,
    and any generated patent claims.
    """
    try:
        return await service.get_run_details(run_id)
    except Exception as e:
        print(f"❌ Error getting run details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patent/stream", tags=["Patent Drafting"])
async def stream_run(run_id: str):
    """
    Stream patent drafting results in real-time.
    
    Uses Server-Sent Events (SSE) to provide live updates as the AI
    processes the patent drafting request. Events include status updates,
    reasoning, tool calls, and final results.
    
    Event types: thoughts, results, done, error
    """
    async def event_generator():
        try:
            async for event in service.stream_run(run_id):
                yield event
        except Exception as e:
            print(f"❌ Stream error: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
            yield "event: done\ndata: {}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "*"
        }
    )

@app.get("/api/debug/env", tags=["Debug"])
async def debug_env():
    """
    Check environment variables status.
    
    ⚠️ Development only - returns masked environment variables
    for system diagnostics. Sensitive values are masked for security.
    """
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
        "agent_type": "simple_v1"
    }

@app.get("/api/sessions", tags=["Session Management"])
async def list_sessions():
    """
    List all active conversation sessions.
    
    Returns summary information about all sessions including
    start time, topic, and number of runs.
    """
    try:
        sessions = []
        for session_id, session_data in service._sessions.items():
            sessions.append({
                "session_id": session_id,
                "started_at": session_data["started_at"],
                "topic": session_data["topic"],
                "total_runs": len(session_data["runs"]),
                "last_run": session_data["runs"][-1] if session_data["runs"] else None
            })
        
        return {
            "total_sessions": len(sessions),
            "sessions": sessions
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/debug/session/{session_id}", tags=["Debug"])
async def debug_session(session_id: str):
    """
    Get detailed session debug information.
    
    ⚠️ Development only - provides full session history and metadata
    for debugging purposes. Should not be exposed in production.
    """
    try:
        if session_id not in service._sessions:
            return {"error": "Session not found"}
        
        session_data = service._sessions[session_id]
        session_history = service._get_session_history(session_id)
        
        return {
            "session_id": session_id,
            "started_at": session_data["started_at"],
            "topic": session_data["topic"],
            "runs": session_data["runs"],
            "session_history": session_history,
            "history_length": len(session_history),
            "history_preview": session_history[:200] + "..." if len(session_history) > 200 else session_history
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/", tags=["System"])
async def root():
    """
    API health check and service information.
    
    Returns basic service information and operational status.
    Use this endpoint to verify the API is running and accessible.
    """
    return {
        "service": "Simple Patent Drafting Service",
        "version": "1.0",
        "functions": ["draft_claims", "general_conversation"],
        "status": "operational"
    }