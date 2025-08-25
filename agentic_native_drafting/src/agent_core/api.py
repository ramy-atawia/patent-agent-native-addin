from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import asyncio
import json
import uuid
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from .orchestrator import AgentOrchestrator

# ============================================================================
# SESSION & RUN MANAGEMENT
# ============================================================================
class SessionManager:
    """Manages conversation sessions and run states"""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
        self.runs: Dict[str, Dict[str, Any]] = {}
        self.max_sessions = 100
        self.max_runs_per_session = 20
    
    def create_session(self, session_id: str = None) -> str:
        """Create a new session or return existing one"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                "session_id": session_id,
                "created_at": datetime.now().isoformat(),
                "runs": [],
                "conversation_history": [],
                "document_content": {}
            }
            
            # Cleanup old sessions if needed
            if len(self.sessions) > self.max_sessions:
                self._cleanup_old_sessions()
        
        return session_id
    
    def create_run(self, session_id: str, user_message: str, conversation_history: List = None, document_content: Dict = None) -> str:
        """Create a new run within a session"""
        # Ensure session exists
        if session_id not in self.sessions:
            session_id = self.create_session(session_id)
        
        # Generate unique run ID
        run_id = str(uuid.uuid4())
        
        # Create run state
        self.runs[run_id] = {
            "run_id": run_id,
            "session_id": session_id,
            "user_message": user_message,  # Store the original message!
            "status": "started",
            "created_at": datetime.now().isoformat(),
            "conversation_history": conversation_history or [],
            "document_content": document_content or {},
            "results": None,
            "error": None
        }
        
        # Add run to session
        self.sessions[session_id]["runs"].append(run_id)
        
        # Cleanup old runs if needed
        if len(self.sessions[session_id]["runs"]) > self.max_runs_per_session:
            self._cleanup_old_runs(session_id)
        
        return run_id
    
    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        """Get run data by ID"""
        return self.runs.get(run_id)
    
    def update_run_status(self, run_id: str, status: str, results: Any = None, error: str = None):
        """Update run status and results"""
        if run_id in self.runs:
            self.runs[run_id]["status"] = status
            if results:
                self.runs[run_id]["results"] = results
            if error:
                self.runs[run_id]["error"] = error
    
    def _cleanup_old_sessions(self):
        """Remove oldest sessions to maintain memory limits"""
        if len(self.sessions) <= self.max_sessions:
            return
        
        # Sort by creation time and remove oldest
        sorted_sessions = sorted(
            self.sessions.items(),
            key=lambda x: x[1]["created_at"]
        )
        
        # Remove oldest sessions
        to_remove = len(self.sessions) - self.max_sessions
        for i in range(to_remove):
            session_id = sorted_sessions[i][0]
            # Remove all runs for this session
            for run_id in self.sessions[session_id]["runs"]:
                if run_id in self.runs:
                    del self.runs[run_id]
            del self.sessions[session_id]
    
    def _cleanup_old_runs(self, session_id: str):
        """Remove oldest runs from a session"""
        if session_id not in self.sessions:
            return
        
        session = self.sessions[session_id]
        if len(session["runs"]) <= self.max_runs_per_session:
            return
        
        # Sort runs by creation time and remove oldest
        sorted_runs = sorted(
            session["runs"],
            key=lambda run_id: self.runs[run_id]["created_at"]
        )
        
        # Remove oldest runs
        to_remove = len(session["runs"]) - self.max_runs_per_session
        for i in range(to_remove):
            run_id = sorted_runs[i]
            if run_id in self.runs:
                del self.runs[run_id]
            session["runs"].remove(run_id)

# Initialize session manager
session_manager = SessionManager()

# Generic request models - no domain-specific fields
class AgentRequest(BaseModel):
    user_input: str
    context: str = ""
    session_id: Optional[str] = None
    use_chain: bool = False
    workflow_type: Optional[str] = None
    # Generic parameters that can be used by any domain
    parameters: Optional[Dict[str, Any]] = {}

# API Compatibility Layer - Old Patent API Models
class PatentChatRequest(BaseModel):
    disclosure: str
    session_id: Optional[str] = None

# Frontend Compatibility Models - Handle actual frontend request format
class FrontendChatRequest(BaseModel):
    user_message: str
    conversation_history: Optional[List[Dict[str, Any]]] = []
    document_content: Optional[Dict[str, Any]] = {}
    session_id: Optional[str] = None

class PatentRunRequest(BaseModel):
    disclosure: str
    session_id: Optional[str] = None

class PatentStreamRequest(BaseModel):
    run_id: str

class ChainRequest(BaseModel):
    chain_name: str
    input_text: str
    context: str = ""
    conversation_history: str = ""
    # Generic parameters that can be used by any domain
    parameters: Optional[Dict[str, Any]] = {}

class ToolRequest(BaseModel):
    tool_name: str
    user_input: str
    context: str = ""
    session_id: Optional[str] = None
    # Generic parameters that can be used by any domain
    parameters: Optional[Dict[str, Any]] = {}

# Initialize FastAPI app
app = FastAPI(
    title="Generic Agent Orchestrator API",
    description="""
    ## AI-Powered Agent Orchestrator with Modular Tools and Chains
    
    This API provides access to a generic agent orchestrator with:
    - Individual AI tools for various domains
    - Workflow chains for complex processes
    - Intent classification and routing
    - Conversation memory and context management
    
    ### Available Endpoints:
    - `/agent/run` - Main agent endpoint with automatic routing
    - `/chain/execute` - Execute specific workflow chains
    - `/tool/execute` - Execute individual tools directly
    - `/orchestrator/status` - Get orchestrator status
    - `/orchestrator/clear-memory` - Clear conversation memory
    
    ### Generic Design:
    - Domain-agnostic: Works with any type of content
    - Configurable: Parameters passed through generic parameter objects
    - Extensible: Easy to add new tools and domains
    """,
    version="2.0.0",
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

# Initialize orchestrator
orchestrator = AgentOrchestrator()

@app.post("/agent/run")
async def run_agent(request: AgentRequest):
    """
    Main agent endpoint that automatically routes requests to appropriate tools or chains.
    
    The orchestrator will:
    1. Classify user intent
    2. Determine if a chain workflow is needed
    3. Execute the appropriate tool or chain
    4. Return streaming results with progress updates
    
    This endpoint is domain-agnostic and works with any type of content.
    """
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Pass generic parameters to orchestrator
        async def generate_response():
            async for event in orchestrator.handle(
                request.user_input, 
                request.context, 
                request.session_id,
                parameters=request.parameters
            ):
                yield f"data: {json.dumps(event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent execution failed: {str(e)}")

@app.post("/chain/execute")
async def execute_chain(request: ChainRequest):
    """
    Execute a specific workflow chain.
    
    This endpoint is domain-agnostic and can handle any type of workflow chain.
    """
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Get the chain from orchestrator
        chain = orchestrator.get_chain(request.chain_name)
        if not chain:
            raise HTTPException(status_code=404, detail=f"Chain '{request.chain_name}' not found")
        
        # Execute chain with generic parameters
        async def generate_response():
            async for event in chain.run(
                request.input_text,
                request.context,
                request.conversation_history,
                parameters=request.parameters
            ):
                yield f"data: {json.dumps(event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chain execution failed: {str(e)}")

@app.post("/tool/execute")
async def execute_tool(request: ToolRequest):
    """
    Execute a specific tool directly.
    
    This endpoint is domain-agnostic and can handle any type of tool.
    """
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Get the tool from orchestrator
        tool = orchestrator.get_tool(request.tool_name)
        if not tool:
            raise HTTPException(status_code=400, detail=f"Tool '{request.tool_name}' not found. Available tools: {list(orchestrator.get_available_tools())}")
        
        # Execute tool with generic parameters
        async def generate_response():
            async for event in tool.run(
                request.user_input,
                request.context,
                parameters=getattr(request, 'parameters', {})
            ):
                yield f"data: {json.dumps(event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Tool execution failed: {str(e)}")

@app.get("/orchestrator/status")
async def get_orchestrator_status():
    """Get the current status of the orchestrator"""
    try:
        status = orchestrator.get_status()
        return {"status": "healthy", "orchestrator": status}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        status = orchestrator.get_status()
        return {"status": "healthy", "orchestrator": status}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.post("/orchestrator/clear-memory")
async def clear_conversation_memory():
    """Clear conversation memory and intent cache"""
    try:
        orchestrator.clear_memory()
        return {"message": "Memory cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to clear memory: {str(e)}")

# ============================================================================
# API COMPATIBILITY LAYER - Old Patent API Endpoints
# ============================================================================
# These endpoints maintain backward compatibility with the existing frontend
# while internally using the new generic orchestrator

@app.post("/api/patent/run")
async def start_patent_run_frontend(request: FrontendChatRequest):
    """
    API Compatibility: Start a patent drafting run with frontend format
    
    This endpoint handles the actual frontend request format while maintaining
    backward compatibility with the existing frontend.
    """
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Create session and run using the session manager
        session_id = session_manager.create_session(request.session_id)
        run_id = session_manager.create_run(
            session_id=session_id,
            user_message=request.user_message,  # Store the message!
            conversation_history=request.conversation_history,
            document_content=request.document_content
        )
        
        # Return the same response format the frontend expects
        return {
            "run_id": run_id,  # ✅ Now returns a unique run_id
            "session_id": session_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Patent run failed: {str(e)}")

@app.post("/api/patent/stream")
async def stream_patent_response_post(request: FrontendChatRequest):
    """
    API Compatibility: Stream patent response with frontend format
    
    This endpoint handles the actual frontend request format while maintaining
    backward compatibility with the existing frontend.
    """
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Convert frontend request to generic agent request
        agent_request = AgentRequest(
            user_input=request.user_message,
            context="patent_streaming",
            session_id=request.session_id,
            parameters={
                "domain": "patent",
                "workflow_type": "patent_streaming",
                "conversation_history": request.conversation_history,
                "document_content": request.document_content
            }
        )
        
        # Use the existing agent streaming logic
        async def generate_response():
            async for event in orchestrator.handle(
                agent_request.user_input, 
                agent_request.context, 
                agent_request.session_id,
                parameters=agent_request.parameters
            ):
                yield f"data: {json.dumps(event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Patent stream failed: {str(e)}")

@app.get("/api/patent/stream")
async def stream_patent_response(run_id: str):
    """
    API Compatibility: Stream patent response using stored run data
    
    This endpoint maintains backward compatibility with the existing frontend
    while internally using the new generic agent orchestrator.
    """
    try:
        # Get the stored run data
        run_data = session_manager.get_run(run_id)
        if not run_data:
            raise HTTPException(status_code=404, detail="Run not found")
        
        # Use the stored user message from the run
        user_input = run_data["user_message"]
        session_id = run_data["session_id"]
        conversation_history = run_data["conversation_history"]
        document_content = run_data["document_content"]
        
        # Update run status to processing
        session_manager.update_run_status(run_id, "processing")
        
        context = "patent_streaming"
        
        # Use the existing agent streaming logic with stored context
        async def generate_response():
            try:
                async for event in orchestrator.handle(
                    user_input, 
                    context, 
                    session_id,
                    parameters={
                        "domain": "patent",
                        "workflow_type": "patent_streaming",
                        "session_id": session_id,
                        "conversation_history": conversation_history,
                        "document_content": document_content
                    }
                ):
                    # Send events in the format the frontend expects
                    if event.get("event") == "results":
                        # Send final response without data: prefix
                        yield f"event: results\ndata: {json.dumps(event, default=str)}\n\n"
                    elif event.get("event") == "thoughts":
                        # Send thoughts without data: prefix
                        yield f"event: thoughts\ndata: {json.dumps(event, default=str)}\n\n"
                    else:
                        # Send other events without data: prefix
                        yield f"event: {event.get('event', 'message')}\ndata: {json.dumps(event, default=str)}\n\n"
                
                # Update run status to completed
                session_manager.update_run_status(run_id, "completed")
                
            except Exception as e:
                # Update run status to error
                session_manager.update_run_status(run_id, "error", error=str(e))
                error_event = {
                    "event": "error",
                    "content": f"Streaming failed: {str(e)}",
                    "error_type": "streaming_error",
                    "metadata": {"run_id": run_id},
                    "timestamp": datetime.now().isoformat()
                }
                yield f"event: error\ndata: {json.dumps(error_event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Patent stream failed: {str(e)}")

@app.post("/api/patent/chat")
async def patent_chat(request: FrontendChatRequest):
    """
    API Compatibility: Patent chat endpoint (maps to /agent/run)
    
    This endpoint maintains backward compatibility with the existing frontend
    while internally using the new generic agent orchestrator.
    """
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Convert patent request to generic agent request
        agent_request = AgentRequest(
            user_input=request.user_message,
            context="patent_chat",
            session_id=request.session_id,
            parameters={
                "domain": "patent",
                "workflow_type": "patent_chat",
                "conversation_history": request.conversation_history,
                "document_content": request.document_content
            }
        )
        
        # Use the existing agent streaming logic
        async def generate_response():
            async for event in orchestrator.handle(
                agent_request.user_input, 
                agent_request.context, 
                agent_request.session_id,
                parameters=agent_request.parameters
            ):
                yield f"data: {json.dumps(event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Patent chat failed: {str(e)}")

@app.post("/chat")
async def legacy_chat(request: FrontendChatRequest):
    """
    API Compatibility: Legacy chat endpoint (maps to /agent/run)
    
    This endpoint maintains backward compatibility with the existing frontend
    while internally using the new generic agent orchestrator.
    """
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Convert legacy request to generic agent request
        agent_request = AgentRequest(
            user_input=request.user_message,
            context="legacy_chat",
            session_id=request.session_id,
            parameters={
                "domain": "general",
                "workflow_type": "chat",
                "conversation_history": request.conversation_history,
                "document_content": request.document_content
            }
        )
        
        # Use the existing agent streaming logic
        async def generate_response():
            async for event in orchestrator.handle(
                agent_request.user_input, 
                agent_request.context, 
                agent_request.session_id,
                parameters=agent_request.parameters
            ):
                yield f"data: {json.dumps(event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legacy chat failed: {str(e)}")

@app.post("/chat/stream")
async def legacy_chat_stream(request: FrontendChatRequest):
    """
    API Compatibility: Legacy chat stream endpoint (maps to /agent/run)
    
    This endpoint maintains backward compatibility with the existing frontend
    while internally using the new generic agent orchestrator.
    """
    try:
        # Generate session ID if not provided
        if not request.session_id:
            request.session_id = str(uuid.uuid4())
        
        # Convert legacy request to generic agent request
        agent_request = AgentRequest(
            user_input=request.user_message,
            context="legacy_chat_stream",
            session_id=request.session_id,
            parameters={
                "domain": "general",
                "workflow_type": "chat_stream",
                "conversation_history": request.conversation_history,
                "document_content": request.document_content
            }
        )
        
        # Use the existing agent streaming logic
        async def generate_response():
            async for event in orchestrator.handle(
                agent_request.user_input, 
                agent_request.context, 
                agent_request.session_id,
                parameters=agent_request.parameters
            ):
                yield f"data: {json.dumps(event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Legacy chat stream failed: {str(e)}")

# Additional compatibility endpoints for document operations
@app.post("/analyze-document")
async def analyze_document(request: dict):
    """
    API Compatibility: Document analysis endpoint
    
    This endpoint maintains backward compatibility with the existing frontend
    while internally using the new generic agent orchestrator.
    """
    try:
        content = request.get("content", "")
        session_id = str(uuid.uuid4())
        
        # Use the existing agent streaming logic for document analysis
        agent_request = AgentRequest(
            user_input=f"Analyze this document: {content}",
            context="document_analysis",
            session_id=session_id,
            parameters={
                "domain": "document",
                "workflow_type": "analysis"
            }
        )
        
        async def generate_response():
            async for event in orchestrator.handle(
                agent_request.user_input, 
                agent_request.context, 
                agent_request.session_id,
                parameters=agent_request.parameters
            ):
                yield f"data: {json.dumps(event, default=str)}\n\n"
        
        return StreamingResponse(
            generate_response(),
            media_type="text/event-stream",  # ✅ Correct SSE format
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Content-Type": "text/event-stream"
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Document analysis failed: {str(e)}")

@app.post("/apply-changes")
async def apply_changes(request: dict):
    """
    API Compatibility: Apply document changes endpoint
    
    This endpoint maintains backward compatibility with the existing frontend
    while internally using the new generic agent orchestrator.
    """
    try:
        changes = request.get("changes", [])
        
        # For now, return success (actual document changes would be handled by frontend)
        return {
            "message": "Changes applied successfully",
            "changes_count": len(changes),
            "status": "success"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Change application failed: {str(e)}")

@app.get("/api/patent/run/{run_id}", tags=["Patent Drafting"])
async def get_patent_run_status(run_id: str):
    """
    Get the status and details of a patent drafting run
    
    This endpoint provides information about the run including:
    - Current status (started, processing, completed, error)
    - User message that initiated the run
    - Results if completed
    - Error details if failed
    """
    try:
        run_data = session_manager.get_run(run_id)
        if not run_data:
            raise HTTPException(status_code=404, detail="Run not found")
        
        return {
            "run_id": run_id,
            "session_id": run_data["session_id"],
            "status": run_data["status"],
            "user_message": run_data["user_message"],
            "created_at": run_data["created_at"],
            "results": run_data.get("results"),
            "error": run_data.get("error"),
            "conversation_history": run_data.get("conversation_history", []),
            "document_content": run_data.get("document_content", {})
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get run status: {str(e)}")

@app.get("/api/sessions", tags=["Session Management"])
async def list_sessions():
    """List all active conversation sessions with their runs"""
    try:
        sessions = []
        for session_id, session_data in session_manager.sessions.items():
            # Get run information for this session
            session_runs = []
            for run_id in session_data["runs"]:
                run_data = session_manager.get_run(run_id)
                if run_data:
                    session_runs.append({
                        "run_id": run_id,
                        "status": run_data["status"],
                        "user_message": run_data["user_message"][:100] + "..." if len(run_data["user_message"]) > 100 else run_data["user_message"],
                        "created_at": run_data["created_at"]
                    })
            
            sessions.append({
                "session_id": session_id,
                "created_at": session_data["created_at"],
                "total_runs": len(session_data["runs"]),
                "runs": session_runs
            })
        
        return {
            "total_sessions": len(sessions),
            "sessions": sessions
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/api/prior-art/search", tags=["Prior Art Search"])
async def search_prior_art(query: str, max_results: int = 20):
    """
    API Compatibility: Prior art search endpoint
    
    This endpoint maintains backward compatibility with the existing frontend
    while internally using the new generic agent orchestrator.
    """
    try:
        # Generate a session ID for this search
        session_id = str(uuid.uuid4())
        
        # Create a run for the search
        run_id = session_manager.create_run(
            session_id=session_id,
            user_message=f"Search for prior art: {query}",
            conversation_history=[],
            document_content={}
        )
        
        # Use the orchestrator to perform the search
        search_results = []
        async for event in orchestrator.handle(
            f"Search for prior art: {query}",
            "prior_art_search",
            session_id,
            parameters={
                "domain": "patent",
                "workflow_type": "prior_art_search",
                "query": query,
                "max_results": max_results
            }
        ):
            if event.get("event") == "results":
                # Extract search results from the event
                if event.get("data", {}).get("content"):
                    search_results = event["data"]["content"]
                break
        
        # Update run status
        session_manager.update_run_status(run_id, "completed", results={"search_results": search_results})
        
        return {
            "query": query,
            "total_results": len(search_results),
            "results": search_results,
            "status": "success",
            "run_id": run_id,
            "session_id": session_id
        }
        
    except Exception as e:
        print(f"❌ Prior art search failed: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Prior art search failed: {str(e)}"
        )

@app.get("/", tags=["System"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Generic Agent Orchestrator API",
        "endpoints": {
            "agent": "/agent/run",
            "chain": "/chain/execute", 
            "tool": "/tool/execute",
            "status": "/orchestrator/status",
            "health": "/health",
            # API Compatibility Layer
            "patent_run": "/api/patent/run",
            "patent_run_status": "/api/patent/run/{run_id}", # Added new endpoint
            "patent_stream_get": "/api/patent/stream",
            "patent_stream_post": "/api/patent/stream (POST)",
            "patent_chat": "/api/patent/chat",
            "legacy_chat": "/chat",
            "legacy_chat_stream": "/chat/stream",
            "analyze_document": "/analyze-document",
            "apply_changes": "/apply-changes",
            "list_sessions": "/api/sessions", # Added new endpoint
            "prior_art_search": "/api/prior-art/search" # Added new endpoint
        },
        "description": "Domain-agnostic AI agent orchestrator with modular tools and chains + API compatibility layer"
    }

# Note: Frontend uses existing /api/patent/* endpoints from main.py
# No need for duplicate frontend endpoints here

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
