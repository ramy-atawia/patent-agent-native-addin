import uuid
import asyncio
import json
import os
from typing import Dict, Any
from datetime import datetime

from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from .agent import agent
from .models import AgentResponse

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

app = FastAPI()

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
            try:
                session_history = self._get_session_history(run_data["session_id"])
                if session_history:
                    print(f"🔍 Using session context ({len(session_history)} chars) for run {run_id}")
                else:
                    print(f"🆕 No session context available for run {run_id}")
                agent_response = await agent.run(disclosure, session_history)
                yield f"event: reasoning\ndata: {json.dumps({'text': agent_response.reasoning})}\n\n"
                await asyncio.sleep(1)
                if agent_response.should_draft_claims:
                    yield f"event: tool_call\ndata: {json.dumps({'tool': 'draft_claims', 'num_claims': len(agent_response.claims or [])})}\n\n"
                    await asyncio.sleep(1)
                    yield f"event: tool_result\ndata: {json.dumps({'tool': 'draft_claims', 'success': True, 'claims_generated': len(agent_response.claims or [])})}\n\n"
                    await asyncio.sleep(1)
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
                self._runs[run_id]["status"] = "completed"
                self._runs[run_id]["result"] = agent_response
                self._add_to_session_history(run_data["session_id"], disclosure, agent_response.conversation_response)
                print(f"💾 Updated session history for session {run_data['session_id']}")
                yield f"event: final\ndata: {json.dumps(final_data)}\n\n"
                await asyncio.sleep(0.5)
                yield "event: done\ndata: {}\n\n"
            except Exception as e:
                print(f"❌ Agent execution failed: {e}")
                fallback_response = {
                    "response": "I encountered an issue processing your request. Please try again or provide more details about your invention.",
                    "metadata": {"error": str(e), "should_draft_claims": False, "has_claims": False}
                }
                self._runs[run_id]["status"] = "error"
                self._runs[run_id]["error"] = str(e)
                yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
                yield f"event: final\ndata: {json.dumps(fallback_response)}\n\n"
                yield "event: done\ndata: {}\n\n"
        except Exception as e:
            print(f"❌ Stream execution failed: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
            yield "event: done\ndata: {}\n\n"


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
                
                # Stream tool execution if claims were drafted
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
                
                yield f"event: final\ndata: {json.dumps(final_data)}\n\n"
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
                yield f"event: final\ndata: {json.dumps(fallback_response)}\n\n"
                yield "event: done\ndata: {}\n\n"
                
        except Exception as e:
            print(f"❌ Stream execution failed: {e}")
            yield f"event: error\ndata: {json.dumps({'error': str(e)})}\n\n"
            yield "event: done\ndata: {}\n\n"

# Initialize service
service = SimplePatentService()

@app.post("/api/patent/run")
async def start_run(request: RunRequest):
    """Start a new patent drafting run. Accepts labeled fields from UI."""
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


@app.post("/api/patent/prior-art")
async def prior_art_search_endpoint(request: RunRequest):
    """Endpoint to trigger prior art search using user_message or disclosure"""
    try:
        search_query = request.user_message or request.disclosure or ""
        if not search_query:
            raise HTTPException(status_code=400, detail="user_message or disclosure is required for prior art search")

        # Import here to avoid startup cost if not used
        from .prior_art_search import search_prior_art_optimized, format_optimized_results

        result = search_prior_art_optimized(search_query, max_results=10)
        # Format the result for API response
        formatted_results = format_optimized_results(result)
        
        # Create API response structure
        api_response = {
            "results": formatted_results,
            "thought_process": f"Prior art search completed for: {search_query}",
            "query": search_query,
            "total_found": result.total_found,
            "timestamp": result.timestamp,
            "patents": [patent.patent_id for patent in result.patents]
        }
        return api_response
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Prior art endpoint failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patent/run/{run_id}")
async def get_run_details(run_id: str):
    """Get run details"""
    try:
        return await service.get_run_details(run_id)
    except Exception as e:
        print(f"❌ Error getting run details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/patent/stream")
async def stream_run(run_id: str):
    """Stream a patent drafting run"""
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

@app.get("/api/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables"""
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

@app.get("/api/sessions")
async def list_sessions():
    """List all active sessions"""
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

@app.get("/api/debug/session/{session_id}")
async def debug_session(session_id: str):
    """Debug endpoint to see session history"""
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

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": "Simple Patent Drafting Service",
        "version": "1.0",
        "functions": ["draft_claims", "general_conversation"],
        "status": "operational"
    }