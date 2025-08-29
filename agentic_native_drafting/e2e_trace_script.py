#!/usr/bin/env python3
"""
COMPREHENSIVE E2E TRACE SCRIPT
==============================

This script demonstrates and stores the complete end-to-end flow of a user request
through the Agentic Native Drafting system, from frontend initiation to backend response.

The script traces:
1. Frontend request initiation
2. Backend API reception
3. Orchestrator processing
4. Tool execution
5. Response streaming back
6. Frontend reception and display

Usage:
    python e2e_trace_script.py
"""

import asyncio
import json
import logging
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.agent_core.orchestrator import AgentOrchestrator
from src.tools.claim_drafting_tool import ContentDraftingTool
from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class E2ETraceRecorder:
    """Records and stores the complete E2E flow for analysis"""
    
    def __init__(self):
        self.trace_data = {
            "session_id": f"e2e_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "flow_phases": [],
            "api_calls": [],
            "llm_calls": [],
            "tool_executions": [],
            "streaming_events": [],
            "performance_metrics": {},
            "error_logs": [],
            "success_indicators": []
        }
        
    def record_phase(self, phase_name: str, description: str, data: Dict[str, Any] = None):
        """Record a phase in the E2E flow"""
        phase = {
            "phase": phase_name,
            "timestamp": datetime.now().isoformat(),
            "description": description,
            "data": data or {}
        }
        self.trace_data["flow_phases"].append(phase)
        logger.info(f"📋 PHASE: {phase_name} - {description}")
        
    def record_api_call(self, method: str, endpoint: str, request_data: Dict[str, Any], response_data: Dict[str, Any]):
        """Record an API call"""
        api_call = {
            "timestamp": datetime.now().isoformat(),
            "method": method,
            "endpoint": endpoint,
            "request": request_data,
            "response": response_data
        }
        self.trace_data["api_calls"].append(api_call)
        logger.info(f"🌐 API CALL: {method} {endpoint}")
        
    def record_llm_call(self, purpose: str, input_data: Dict[str, Any], output_data: Dict[str, Any], duration: float):
        """Record an LLM call"""
        llm_call = {
            "timestamp": datetime.now().isoformat(),
            "purpose": purpose,
            "input": input_data,
            "output": output_data,
            "duration_seconds": duration
        }
        self.trace_data["llm_calls"].append(llm_call)
        logger.info(f"🤖 LLM CALL: {purpose} ({duration:.2f}s)")
        
    def record_tool_execution(self, tool_name: str, input_data: Dict[str, Any], output_data: Dict[str, Any], duration: float):
        """Record a tool execution"""
        tool_exec = {
            "timestamp": datetime.now().isoformat(),
            "tool": tool_name,
            "input": input_data,
            "output": output_data,
            "duration_seconds": duration
        }
        self.trace_data["tool_executions"].append(tool_exec)
        logger.info(f"🛠️ TOOL EXECUTION: {tool_name} ({duration:.2f}s)")
        
    def record_streaming_event(self, event_type: str, event_data: Dict[str, Any]):
        """Record a streaming event"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "event_type": event_type,
            "event_data": event_data
        }
        self.trace_data["streaming_events"].append(event)
        logger.info(f"📡 STREAMING EVENT: {event_type}")
        
    def record_error(self, error_type: str, error_message: str, context: str = ""):
        """Record an error"""
        error = {
            "timestamp": datetime.now().isoformat(),
            "error_type": error_type,
            "error_message": error_message,
            "context": context
        }
        self.trace_data["error_logs"].append(error)
        logger.error(f"❌ ERROR: {error_type} - {error_message}")
        
    def record_success(self, indicator: str, details: str = ""):
        """Record a success indicator"""
        success = {
            "timestamp": datetime.now().isoformat(),
            "indicator": indicator,
            "details": details
        }
        self.trace_data["success_indicators"].append(success)
        logger.info(f"✅ SUCCESS: {indicator} - {details}")
        
    def save_trace(self, filename: str = None):
        """Save the trace data to a JSON file"""
        if filename is None:
            filename = f"e2e_trace_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            
        trace_file = Path(__file__).parent / "test_reports" / filename
        
        # Ensure test_reports directory exists
        trace_file.parent.mkdir(exist_ok=True)
        
        with open(trace_file, 'w') as f:
            json.dump(self.trace_data, f, indent=2, default=str)
            
        logger.info(f"💾 Trace saved to: {trace_file}")
        return str(trace_file)

class MockFrontend:
    """Simulates frontend behavior for E2E testing"""
    
    def __init__(self, trace_recorder: E2ETraceRecorder):
        self.trace_recorder = trace_recorder
        self.base_url = "http://localhost:8000"
        
    async def simulate_user_request(self, user_message: str, document_content: str = "", conversation_history: List[Dict] = None):
        """Simulate a user making a request from the frontend"""
        self.trace_recorder.record_phase(
            "frontend_initiation",
            "User submits message in Word Add-in",
            {
                "user_message": user_message,
                "document_content": document_content,
                "conversation_history_length": len(conversation_history) if conversation_history else 0
            }
        )
        
        # Simulate the request object that would be sent
        request = {
            "user_message": user_message,
            "conversation_history": conversation_history or [],
            "document_content": {"text": document_content},
            "session_id": f"frontend_session_{int(time.time())}"
        }
        
        self.trace_recorder.record_phase(
            "frontend_request_formation",
            "Frontend forms ChatRequest object",
            {"request_object": request}
        )
        
        return request

class MockBackendAPI:
    """Simulates backend API behavior for E2E testing"""
    
    def __init__(self, trace_recorder: E2ETraceRecorder):
        self.trace_recorder = trace_recorder
        
    async def simulate_start_patent_run(self, request: Dict[str, Any]):
        """Simulate the /api/patent/run endpoint"""
        start_time = time.time()
        
        self.trace_recorder.record_phase(
            "backend_api_reception",
            "Backend receives POST /api/patent/run",
            {"endpoint": "/api/patent/run", "request_data": request}
        )
        
        # Simulate session creation
        session_id = request.get("session_id", f"session_{int(time.time())}")
        run_id = f"run_{int(time.time())}"
        
        # Simulate the response
        response = {
            "run_id": run_id,
            "session_id": session_id
        }
        
        duration = time.time() - start_time
        
        self.trace_recorder.record_api_call(
            "POST",
            "/api/patent/run",
            request,
            response
        )
        
        self.trace_recorder.record_phase(
            "session_creation",
            "Session manager creates run",
            {
                "session_id": session_id,
                "run_id": run_id,
                "duration_seconds": duration
            }
        )
        
        return response
        
    async def simulate_stream_patent_response(self, run_id: str, user_input: str, context: str = "patent_streaming"):
        """Simulate the /api/patent/stream endpoint"""
        self.trace_recorder.record_phase(
            "streaming_initiation",
            "Frontend makes GET /api/patent/stream",
            {
                "endpoint": "/api/patent/stream",
                "run_id": run_id,
                "user_input": user_input,
                "context": context
            }
        )
        
        return {
            "run_id": run_id,
            "user_input": user_input,
            "context": context
        }

class MockOrchestrator:
    """Simulates orchestrator behavior for E2E testing"""
    
    def __init__(self, trace_recorder: E2ETraceRecorder):
        self.trace_recorder = trace_recorder
        self.orchestrator = AgentOrchestrator()
        
    async def simulate_handle_request(self, user_input: str, context: str, session_id: str, parameters: Dict[str, Any]):
        """Simulate the orchestrator.handle() method"""
        start_time = time.time()
        
        self.trace_recorder.record_phase(
            "orchestrator_processing",
            "Orchestrator.handle() method called",
            {
                "user_input": user_input,
                "context": context,
                "session_id": session_id,
                "parameters": parameters
            }
        )
        
        # Simulate conversation memory update
        self.trace_recorder.record_phase(
            "conversation_memory_update",
            "Update conversation memory",
            {"session_id": session_id, "input_length": len(user_input)}
        )
        
        # Simulate initialization event
        init_event = create_thought_event(
            content=f"Processing request: {user_input[:100]}...",
            thought_type="initialization",
            metadata={"session_id": session_id, "input_length": len(user_input)}
        )
        self.trace_recorder.record_streaming_event("initialization", init_event)
        
        # Simulate intent analysis
        self.trace_recorder.record_phase(
            "intent_analysis_start",
            "Analyzing user intent...",
            {"thought_type": "intent_analysis"}
        )
        
        intent_event = create_thought_event(
            content="Analyzing user intent...",
            thought_type="intent_analysis"
        )
        self.trace_recorder.record_streaming_event("intent_analysis", intent_event)
        
        # Simulate LLM-based intent classification
        intent_start_time = time.time()
        intent_type, confidence = await self._simulate_llm_intent_classification(user_input, context)
        intent_duration = time.time() - intent_start_time
        
        self.trace_recorder.record_llm_call(
            "intent_classification",
            {"user_input": user_input, "context": context},
            {"intent_type": intent_type, "confidence": confidence},
            intent_duration
        )
        
        self.trace_recorder.record_phase(
            "intent_classification_complete",
            f"Intent classified as: {intent_type} (confidence: {confidence})",
            {"intent_type": intent_type, "confidence": confidence}
        )
        
        # Simulate tool routing
        tool_name = self._get_tool_name_for_intent(intent_type)
        
        routing_event = create_thought_event(
            content=f"Routing to {tool_name}...",
            thought_type="routing",
            metadata={"intent": intent_type, "confidence": confidence}
        )
        self.trace_recorder.record_streaming_event("routing", routing_event)
        
        self.trace_recorder.record_phase(
            "tool_routing",
            f"Routing to {tool_name}",
            {"intent_type": intent_type, "tool_name": tool_name}
        )
        
        # Simulate tool execution
        tool_exec_event = create_thought_event(
            content=f"Executing {tool_name}...",
            thought_type="tool_execution",
            metadata={"tool": tool_name}
        )
        self.trace_recorder.record_streaming_event("tool_execution", tool_exec_event)
        
        # Execute the actual tool
        tool_start_time = time.time()
        tool_output = await self._execute_tool(tool_name, user_input, context, parameters)
        tool_duration = time.time() - tool_start_time
        
        self.trace_recorder.record_tool_execution(
            tool_name,
            {"user_input": user_input, "context": context, "parameters": parameters},
            tool_output,
            tool_duration
        )
        
        # Simulate final results
        results_event = create_results_event(
            response=f"Successfully processed request using {tool_name}",
            metadata={"tool": tool_name, "intent": intent_type},
            data=tool_output
        )
        self.trace_recorder.record_streaming_event("results", results_event)
        
        total_duration = time.time() - start_time
        
        self.trace_recorder.record_phase(
            "orchestrator_completion",
            "Orchestrator processing completed",
            {"total_duration_seconds": total_duration}
        )
        
        # Return all events for streaming simulation
        return [
            init_event,
            intent_event,
            routing_event,
            tool_exec_event,
            results_event
        ]
        
    async def _simulate_llm_intent_classification(self, user_input: str, context: str) -> tuple[str, float]:
        """Simulate LLM-based intent classification"""
        # Simulate the intent classification logic
        if "draft" in user_input.lower() or "claim" in user_input.lower():
            return "content_drafting", 0.95
        elif "review" in user_input.lower() or "analyze" in user_input.lower():
            return "content_review", 0.90
        elif "search" in user_input.lower() or "prior art" in user_input.lower():
            return "search", 0.85
        elif "guidance" in user_input.lower() or "help" in user_input.lower():
            return "guidance", 0.80
        else:
            return "general_conversation", 0.70
            
    def _get_tool_name_for_intent(self, intent_type: str) -> str:
        """Map intent types to tool names"""
        intent_to_tool = {
            "content_drafting": "ContentDraftingTool",
            "content_review": "ContentReviewTool",
            "search": "PriorArtSearchTool",
            "guidance": "GeneralGuidanceTool",
            "analysis": "GeneralConversationTool",
            "query": "GeneralConversationTool",
            "general_conversation": "GeneralConversationTool"
        }
        return intent_to_tool.get(intent_type, "GeneralConversationTool")
        
    async def _execute_tool(self, tool_name: str, user_input: str, context: str, parameters: Dict[str, Any]):
        """Execute the specified tool"""
        try:
            if tool_name == "ContentDraftingTool":
                tool = ContentDraftingTool()
                # Simulate tool execution
                output = {
                    "content": [
                        {
                            "content_number": "1",
                            "content_text": f"Generated content based on: {user_input[:50]}...",
                            "content_type": "primary",
                            "dependency": None,
                            "focus_area": "general"
                        }
                    ],
                    "reasoning": f"Content drafted based on user input: {user_input}",
                    "metadata": {
                        "input_length": len(user_input),
                        "outputs_generated": 1
                    }
                }
                return output
            else:
                return {"message": f"Tool {tool_name} executed successfully", "input": user_input}
                
        except Exception as e:
            self.trace_recorder.record_error("tool_execution", str(e), f"Tool: {tool_name}")
            return {"error": str(e)}

class MockFrontendReception:
    """Simulates frontend reception and processing of streaming events"""
    
    def __init__(self, trace_recorder: E2ETraceRecorder):
        self.trace_recorder = trace_recorder
        
    async def simulate_receive_streaming_events(self, events: List[Dict[str, Any]], session_id: str):
        """Simulate frontend receiving and processing streaming events"""
        self.trace_recorder.record_phase(
            "frontend_reception",
            "Frontend receives streaming events",
            {"session_id": session_id, "event_count": len(events)}
        )
        
        for i, event in enumerate(events):
            event_type = event.get("event", "unknown")
            
            self.trace_recorder.record_phase(
                "event_processing",
                f"Processing event {i+1}: {event_type}",
                {"event_number": i+1, "event_type": event_type, "event_data": event}
            )
            
            # Simulate frontend processing logic
            if event_type == "thoughts":
                self._simulate_thought_processing(event)
            elif event_type == "results":
                self._simulate_results_processing(event)
            elif event_type == "error":
                self._simulate_error_processing(event)
                
        self.trace_recorder.record_phase(
            "frontend_completion",
            "Frontend processing completed",
            {"total_events_processed": len(events)}
        )
        
    def _simulate_thought_processing(self, event: Dict[str, Any]):
        """Simulate processing of thought events"""
        thought_type = event.get("metadata", {}).get("thought_type", "unknown")
        self.trace_recorder.record_streaming_event(f"thought_{thought_type}", event)
        
    def _simulate_results_processing(self, event: Dict[str, Any]):
        """Simulate processing of results events"""
        self.trace_recorder.record_streaming_event("results_processing", event)
        
    def _simulate_error_processing(self, event: Dict[str, Any]):
        """Simulate processing of error events"""
        self.trace_recorder.record_error("frontend_error", event.get("content", ""), "frontend_processing")

async def run_complete_e2e_trace():
    """Run the complete E2E trace simulation"""
    print("🚀 STARTING COMPLETE E2E TRACE SIMULATION")
    print("=" * 60)
    
    # Initialize trace recorder
    trace_recorder = E2ETraceRecorder()
    
    # Initialize mock components
    frontend = MockFrontend(trace_recorder)
    backend_api = MockBackendAPI(trace_recorder)
    orchestrator = MockOrchestrator(trace_recorder)
    frontend_reception = MockFrontendReception(trace_recorder)
    
    try:
        # PHASE 1: Frontend Initiation
        print("\n📱 PHASE 1: FRONTEND INITIATION")
        print("-" * 40)
        
        user_message = "I want to draft patent claims for a wireless communication system"
        document_content = "This invention relates to optimizing handover in wireless communication systems..."
        conversation_history = [
            {"role": "user", "content": "Hello, I need help with patent drafting"},
            {"role": "assistant", "content": "I'd be happy to help you with patent drafting. What would you like to work on?"}
        ]
        
        request = await frontend.simulate_user_request(user_message, document_content, conversation_history)
        
        # PHASE 2: Backend API Reception
        print("\n🌐 PHASE 2: BACKEND API RECEPTION")
        print("-" * 40)
        
        run_response = await backend_api.simulate_start_patent_run(request)
        
        # PHASE 3: Streaming Response Initiation
        print("\n🔄 PHASE 3: STREAMING RESPONSE INITIATION")
        print("-" * 40)
        
        stream_data = await backend_api.simulate_stream_patent_response(
            run_response["run_id"],
            request["user_message"]
        )
        
        # PHASE 4: Orchestrator Processing
        print("\n🎯 PHASE 4: ORCHESTRATOR PROCESSING")
        print("-" * 40)
        
        parameters = {
            "domain": "patent",
            "workflow_type": "patent_streaming",
            "session_id": run_response["session_id"],
            "conversation_history": conversation_history,
            "document_content": {"text": document_content}
        }
        
        events = await orchestrator.simulate_handle_request(
            request["user_message"],
            "patent_streaming",
            run_response["session_id"],
            parameters
        )
        
        # PHASE 5: Frontend Reception
        print("\n📱 PHASE 5: FRONTEND RECEPTION")
        print("-" * 40)
        
        await frontend_reception.simulate_receive_streaming_events(events, run_response["session_id"])
        
        # Record final success
        trace_recorder.record_success("e2e_trace_completed", "All phases completed successfully")
        
        # Calculate performance metrics
        total_events = len(events)
        total_api_calls = len(trace_recorder.trace_data["api_calls"])
        total_llm_calls = len(trace_recorder.trace_data["llm_calls"])
        total_tool_executions = len(trace_recorder.trace_data["tool_executions"])
        
        trace_recorder.trace_data["performance_metrics"] = {
            "total_events_processed": total_events,
            "total_api_calls": total_api_calls,
            "total_llm_calls": total_llm_calls,
            "total_tool_executions": total_tool_executions,
            "success_rate": 100.0 if not trace_recorder.trace_data["error_logs"] else 0.0
        }
        
        print("\n🎉 E2E TRACE COMPLETED SUCCESSFULLY!")
        print(f"📊 Total Events: {total_events}")
        print(f"🌐 API Calls: {total_api_calls}")
        print(f"🤖 LLM Calls: {total_llm_calls}")
        print(f"🛠️ Tool Executions: {total_tool_executions}")
        
        # Save trace data
        trace_file = trace_recorder.save_trace()
        print(f"💾 Trace data saved to: {trace_file}")
        
        return trace_recorder.trace_data
        
    except Exception as e:
        trace_recorder.record_error("e2e_trace_failed", str(e), "main_execution")
        print(f"❌ E2E TRACE FAILED: {e}")
        return None

def print_trace_summary(trace_data: Dict[str, Any]):
    """Print a summary of the trace data"""
    if not trace_data:
        print("❌ No trace data available")
        return
        
    print("\n" + "=" * 60)
    print("📋 E2E TRACE SUMMARY")
    print("=" * 60)
    
    print(f"🆔 Session ID: {trace_data.get('session_id', 'N/A')}")
    print(f"⏰ Timestamp: {trace_data.get('timestamp', 'N/A')}")
    
    print(f"\n📊 PERFORMANCE METRICS:")
    metrics = trace_data.get('performance_metrics', {})
    for key, value in metrics.items():
        print(f"   {key}: {value}")
    
    print(f"\n🔄 FLOW PHASES ({len(trace_data.get('flow_phases', []))}):")
    for phase in trace_data.get('flow_phases', []):
        print(f"   • {phase['phase']}: {phase['description']}")
    
    print(f"\n🌐 API CALLS ({len(trace_data.get('api_calls', []))}):")
    for call in trace_data.get('api_calls', []):
        print(f"   • {call['method']} {call['endpoint']}")
    
    print(f"\n🤖 LLM CALLS ({len(trace_data.get('llm_calls', []))}):")
    for call in trace_data.get('llm_calls', []):
        print(f"   • {call['purpose']} ({call['duration_seconds']:.2f}s)")
    
    print(f"\n🛠️ TOOL EXECUTIONS ({len(trace_data.get('tool_executions', []))}):")
    for exec in trace_data.get('tool_executions', []):
        print(f"   • {exec['tool']} ({exec['duration_seconds']:.2f}s)")
    
    print(f"\n📡 STREAMING EVENTS ({len(trace_data.get('streaming_events', []))}):")
    for event in trace_data.get('streaming_events', []):
        print(f"   • {event['event_type']}")
    
    if trace_data.get('error_logs'):
        print(f"\n❌ ERRORS ({len(trace_data['error_logs'])}):")
        for error in trace_data['error_logs']:
            print(f"   • {error['error_type']}: {error['error_message']}")
    
    if trace_data.get('success_indicators'):
        print(f"\n✅ SUCCESS INDICATORS ({len(trace_data['success_indicators'])}):")
        for success in trace_data['success_indicators']:
            print(f"   • {success['indicator']}: {success['details']}")

if __name__ == "__main__":
    print("🔍 AGENTIC NATIVE DRAFTING - E2E TRACE SCRIPT")
    print("=" * 60)
    print("This script will trace a complete user request through the system")
    print("from frontend initiation to backend response and back to frontend.")
    print()
    
    try:
        # Run the complete E2E trace
        trace_data = asyncio.run(run_complete_e2e_trace())
        
        # Print summary
        print_trace_summary(trace_data)
        
        print("\n🎯 E2E TRACE SCRIPT COMPLETED!")
        print("Check the generated JSON file for detailed trace data.")
        
    except KeyboardInterrupt:
        print("\n⏹️ E2E trace interrupted by user")
    except Exception as e:
        print(f"\n💥 Unexpected error during E2E trace: {e}")
        import traceback
        traceback.print_exc()
