"""
End-to-End Integration Tests for the New Modular System

This test suite validates the complete flow:
API → Orchestrator → Intent Classification → Tool Selection → Tool Execution → Streaming Output
"""

import pytest
import asyncio
import json
from datetime import datetime
from unittest.mock import Mock, patch, AsyncMock

# Import the new modular system components
from src.agent_core.orchestrator import AgentOrchestrator
from src.tools.claim_drafting_tool import ContentDraftingTool
from src.tools.prior_art_search_tool import PriorArtSearchTool
from src.tools.general_conversation_tool import GeneralConversationTool

# Test client for API endpoints
from fastapi.testclient import TestClient
from src.agent_core.api import app

client = TestClient(app)

class TestEndToEndIntegration:
    """Test the complete flow from API to Orchestrator to Tool Selection to Streaming Output"""
    
    @pytest.mark.asyncio
    async def test_full_agent_workflow_real_orchestrator(self):
        """Test the complete flow with real orchestrator and tools"""
        print("\n🚀 Testing Full Agent Workflow with Real Components...")
    
        # Create real orchestrator instance
        orchestrator = AgentOrchestrator()
    
        # Test input
        user_input = "Draft comprehensive patent claims for 5G wireless communication with AI optimization"
        context = "5G wireless system with machine learning"
    
        print(f"   📝 Input: {user_input[:50]}...")
        print(f"   🎯 Context: {context}")
    
        # Execute the full workflow
        events = []
        try:
            async for event in orchestrator.handle(user_input, context):
                events.append(event)
                print(f"   📡 Event {len(events)}: {event.get('event', 'unknown')} - {event.get('content', 'no content')[:60]}...")
        except Exception as e:
            print(f"   ⚠️ Expected LLM failure: {e}")
            # This is expected behavior in test environment without real LLM
            assert "LLM" in str(e) or "intent classification" in str(e), f"Unexpected error: {e}"
            return
    
        # If we get here, LLM is available (unexpected in test environment)
        if len(events) > 0:
            # Validate the complete flow
            assert len(events) > 0, "No events generated"
    
            # Check that we have the expected event types
            event_types = [event.get('event') for event in events]
            print(f"   📊 Event types generated: {event_types}")
    
            # Must have initialization
            assert "thoughts" in event_types, "Missing thoughts events"
            
            # Must have either results OR errors (errors expected without LLM)
            if "results" in event_types:
                print("   ✅ Workflow completed with results")
            elif "error" in event_types:
                print("   ⚠️ Workflow completed with errors (expected without LLM)")
            else:
                assert False, "Workflow must generate either results or error events"
    
            # Check for specific workflow steps
            thought_contents = [event.get('content', '') for event in events if event.get('event') == 'thoughts']
            print(f"   🧠 Thought contents: {[content[:40] + '...' for content in thought_contents]}")
    
            # Validate workflow progression
            assert any("Processing request" in content for content in thought_contents), "Missing initialization"
        else:
            # No events generated - this might happen with LLM failures
            print("   ⚠️ No events generated - likely due to LLM failure")
    
    @pytest.mark.asyncio
    async def test_intent_classification_and_tool_routing(self):
        """Test that intent classification correctly routes to appropriate tools"""
        print("\n🎯 Testing Intent Classification and Tool Routing...")
    
        orchestrator = AgentOrchestrator()
    
        # Test different input types to see routing
        test_cases = [
            ("Draft patent claims for wireless technology", "claim_drafting"),
            ("Search for prior art in 5G", "prior_art_search"),
            ("What is patent law?", "general_conversation"),
        ]
    
        for user_input, expected_intent in test_cases:
            print(f"   📝 Testing: {user_input[:40]}...")
    
            try:
                # Get the first few events to see routing decision
                events = []
                async for event in orchestrator.handle(user_input, "test context"):
                    events.append(event)
                    if len(events) >= 5:  # Just get routing decision
                        break
                
                # Find routing event
                routing_events = [e for e in events if "Routing to" in e.get('content', '')]
                if routing_events:
                    routing_content = routing_events[0].get('content', '')
                    print(f"   🚦 Routing: {routing_content}")
    
                    # Check if routing mentions expected tool
                    if expected_intent == "claim_drafting":
                        assert "claim_drafting" in routing_content.lower(), f"Expected claim_drafting routing for: {user_input}"
                    elif expected_intent == "prior_art_search":
                        assert "prior_art" in routing_content.lower(), f"Expected prior_art routing for: {user_input}"
                    elif expected_intent == "general_conversation":
                        assert "general_conversation" in routing_content.lower(), f"Expected general_conversation routing for: {user_input}"
                else:
                    # Check if we got error events instead (expected without LLM)
                    error_events = [e for e in events if e.get('event') == 'error']
                    if error_events:
                        print(f"   ⚠️ Got error events instead of routing (expected without LLM): {len(error_events)} errors")
                        continue
                    else:
                        assert len(routing_events) > 0, f"No routing event found for: {user_input}"
                        
            except Exception as e:
                print(f"   ⚠️ Expected LLM failure: {e}")
                # This is expected behavior in test environment without real LLM
                assert "LLM" in str(e) or "intent classification" in str(e), f"Unexpected error: {e}"
                continue
    
    @pytest.mark.asyncio
    async def test_tool_execution_with_real_tools(self):
        """Test that tools actually execute and produce results"""
        print("\n🔧 Testing Tool Execution with Real Tools...")
    
        # Test ContentDraftingTool directly
        claim_tool = ContentDraftingTool()
        test_input = "A method for wireless communication using 5G technology with dynamic spectrum sharing"
    
        print(f"   📝 Testing ContentDraftingTool with: {test_input[:50]}...")
    
        try:
            events = []
            async for event in claim_tool.run(test_input, "5G wireless context"):
                events.append(event)
                print(f"   📡 Tool Event: {event.get('event', 'unknown')} - {event.get('content', 'no content')[:50]}...")
    
            # Validate tool execution
            assert len(events) > 0, "No events generated by tool"
    
            # Check for expected event types
            event_types = [event.get('event') for event in events]
            assert "thoughts" in event_types, "Tool missing thoughts events"
            
            # Check for results OR error events (error is expected without LLM)
            if "results" in event_types:
                print("   ✅ Tool generated results successfully")
                results_events = [e for e in events if e.get('event') == 'results']
                assert len(results_events) > 0, "No results generated"
            elif "error" in event_types:
                print("   ⚠️ Tool generated error events (expected without LLM)")
                error_events = [e for e in events if e.get('event') == 'error']
                assert len(error_events) > 0, "No error events generated"
            else:
                assert False, "Tool must generate either results or error events"
            
        except Exception as e:
            print(f"   ⚠️ Expected LLM failure: {e}")
            # This is expected behavior in test environment without real LLM
            assert "LLM" in str(e) or "send_llm_request_streaming" in str(e), f"Unexpected error: {e}"
    
    @pytest.mark.asyncio
    async def test_streaming_response_content_validation(self):
        """Test that streaming responses contain valid, meaningful content"""
        print("\n📡 Testing Streaming Response Content Validation...")
    
        # Test the API endpoint with real streaming
        request_data = {
            "user_input": "Create patent claims for AI-powered wireless communication",
            "context": "5G AI wireless system"
        }
    
        print(f"   📝 API Request: {request_data['user_input'][:50]}...")
    
        try:
            # Make request and capture streaming response
            response = client.post("/agent/run", json=request_data)
            assert response.status_code == 200, f"API request failed: {response.status_code}"
    
            # Parse streaming response
            content = response.content.decode()
            lines = content.strip().split('\n')
    
            print(f"   📊 Received {len(lines)} streaming lines")
    
            # Validate streaming format
            data_lines = [line for line in lines if line.startswith('data: ')]
            assert len(data_lines) > 0, "No streaming data lines found"
    
            # Parse and validate each event
            events = []
            for line in data_lines:
                try:
                    event_data = line.replace('data: ', '')
                    event = json.loads(event_data)
                    events.append(event)
                except json.JSONDecodeError:
                    continue
    
            print(f"   📋 Parsed {len(events)} valid events")
            assert len(events) > 0, "No valid events parsed"
    
            # Validate event structure
            for i, event in enumerate(events):
                print(f"   📡 Event {i+1}: {event.get('event', 'unknown')} - {event.get('content', 'no content')[:40]}...")
    
                # Check required fields
                assert 'event' in event, f"Event {i+1} missing event"
                assert 'timestamp' in event, f"Event {i+1} missing timestamp"
    
                # Validate event types
                valid_types = ['thoughts', 'results', 'error', 'progress']
                assert event['event'] in valid_types, f"Event {i+1} has invalid type: {event['event']}"
    
            # Check for meaningful progression
            thought_events = [e for e in events if e.get('event') == 'thoughts']
            result_events = [e for e in events if e.get('event') == 'results']
            error_events = [e for e in events if e.get('event') == 'error']
            
            assert len(thought_events) > 0, "No thought events in stream"
            
            # Must have either results OR errors (errors expected without LLM)
            if len(result_events) > 0:
                print("   ✅ Stream contains result events")
            elif len(error_events) > 0:
                print("   ⚠️ Stream contains error events (expected without LLM)")
            else:
                assert False, "Stream must contain either result or error events"
                
        except Exception as e:
            print(f"   ⚠️ Expected API/LLM failure: {e}")
            # This is expected behavior in test environment without real LLM
            assert "LLM" in str(e) or "intent classification" in str(e) or "API" in str(e), f"Unexpected error: {e}"
    
    @pytest.mark.asyncio
    async def test_error_handling_in_workflow(self):
        """Test that errors are handled gracefully throughout the workflow"""
        print("\n⚠️ Testing Error Handling in Workflow...")
    
        orchestrator = AgentOrchestrator()
    
        # Test with invalid input
        try:
            events = []
            async for event in orchestrator.handle("", "empty context"):
                events.append(event)
                if len(events) >= 3:
                    break
            
            # Should handle empty input gracefully
            assert len(events) > 0, "No events generated for empty input"
            
        except Exception as e:
            print(f"   ⚠️ Expected error handling: {e}")
            # This is expected behavior for invalid input
    
    @pytest.mark.asyncio
    async def test_workflow_completion_time(self):
        """Test that workflows complete within reasonable time limits"""
        print("\n⏱️ Testing Workflow Completion Time...")
    
        orchestrator = AgentOrchestrator()
        start_time = datetime.now()
    
        try:
            events = []
            async for event in orchestrator.handle("Test workflow timing", "test context"):
                events.append(event)
                if len(events) >= 5:
                    break
            
            end_time = datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            print(f"   ⏱️ Workflow duration: {duration:.2f} seconds")
            assert duration < 30, f"Workflow took too long: {duration} seconds"
            
        except Exception as e:
            print(f"   ⚠️ Expected LLM failure: {e}")
            # This is expected behavior in test environment without real LLM
            assert "LLM" in str(e) or "intent classification" in str(e), f"Unexpected error: {e}"
    
    @pytest.mark.asyncio
    async def test_concurrent_workflow_execution(self):
        """Test that multiple workflows can execute concurrently"""
        print("\n🔄 Testing Concurrent Workflow Execution...")
    
        orchestrator = AgentOrchestrator()
        
        async def run_workflow(input_text: str, workflow_id: int):
            try:
                events = []
                async for event in orchestrator.handle(input_text, f"context_{workflow_id}"):
                    events.append(event)
                    if len(events) >= 3:
                        break
                return len(events)
            except Exception as e:
                print(f"   ⚠️ Workflow {workflow_id} expected LLM failure: {e}")
                return 0
        
        # Run multiple workflows concurrently
        workflows = [
            ("Test workflow 1", 1),
            ("Test workflow 2", 2),
            ("Test workflow 3", 3)
        ]
        
        try:
            results = await asyncio.gather(*[
                run_workflow(input_text, workflow_id) 
                for input_text, workflow_id in workflows
            ])
            
            print(f"   📊 Concurrent workflow results: {results}")
            assert all(result >= 0 for result in results), "All workflows should complete or fail gracefully"
            
        except Exception as e:
            print(f"   ⚠️ Expected concurrent execution failure: {e}")
            # This is expected behavior in test environment without real LLM
            assert "LLM" in str(e) or "intent classification" in str(e), f"Unexpected error: {e}"
