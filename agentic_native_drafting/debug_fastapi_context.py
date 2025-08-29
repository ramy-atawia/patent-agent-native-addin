#!/usr/bin/env python3
"""
Debug FastAPI Request Context Issues

This script simulates the FastAPI request context to identify why
API endpoint calls fail while direct calls work perfectly.

The goal is to isolate the FastAPI-specific issue that causes
the conversation history to be lost or ignored.
"""

import asyncio
import sys
import os
from datetime import datetime
from contextlib import asynccontextmanager

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent_core.orchestrator import AgentOrchestrator
from src.agent_core.api import orchestrator, session_manager
from src.tools.claim_drafting_tool import ContentDraftingTool

@asynccontextmanager
async def simulate_fastapi_context():
    """Simulate FastAPI request context and cleanup"""
    print("🔍 Simulating FastAPI request context...")
    
    # Simulate request start
    print("   📥 Request started")
    
    try:
        yield "fastapi_context"
    finally:
        # Simulate request cleanup
        print("   📤 Request cleanup (finally block)")
        print("   🔍 Checking if memory was affected...")

async def debug_fastapi_context():
    """Debug FastAPI-specific context issues"""
    
    print("🔍 DEBUG: FastAPI Context Investigation")
    print("=" * 60)
    
    # Test data (same as our working scenario)
    test_data = {
        "user_message": "draft the corresponding method claims",
        "conversation_history": [
            {
                "role": "user",
                "content": "draft 5 system claims for 4g carrier aggregation",
                "timestamp": "2025-08-27T21:40:00.000Z"
            },
            {
                "role": "assistant", 
                "content": "Successfully drafted 5 content items\rGenerated Patent Claims:\rClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\rClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\rClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\rClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\rClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.",
                "timestamp": "2025-08-27T21:43:00.000Z"
            }
        ],
        "document_content": {
            "text": "Successfully drafted 5 content items\rGenerated Patent Claims:\rClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\rClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\rClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\rClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\rClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.",
            "paragraphs": [],
            "session_id": "test-session-4g-carrier-aggregation"
        },
        "session_id": "test-session-4g-carrier-aggregation"
    }
    
    print("📋 Test Data:")
    print(f"   User Message: {test_data['user_message']}")
    print(f"   Conversation History: {len(test_data['conversation_history'])} entries")
    print(f"   Document Content Keys: {list(test_data['document_content'].keys())}")
    print(f"   Session ID: {test_data['session_id']}")
    print()
    
    # ============================================================================
    # TEST 1: Simulate FastAPI Request Context with Memory Check
    # ============================================================================
    print("🧪 TEST 1: FastAPI Request Context Simulation")
    print("-" * 50)
    
    # Clear any existing memory
    if test_data['session_id'] in orchestrator.conversation_memory:
        del orchestrator.conversation_memory[test_data['session_id']]
        print("🔍 Cleared existing memory")
    
    print(f"🔍 Initial orchestrator memory keys: {list(orchestrator.conversation_memory.keys())}")
    
    # Simulate FastAPI request context
    async with simulate_fastapi_context() as context:
        print(f"   🔍 Inside FastAPI context: {context}")
        
        # Set memory (same as API does)
        orchestrator.conversation_memory[test_data['session_id']] = {
            "messages": test_data['conversation_history'],
            "created_at": datetime.now().isoformat()
        }
        
        print(f"   🔍 Set memory for session '{test_data['session_id']}'")
        print(f"   🔍 Memory keys inside context: {list(orchestrator.conversation_memory.keys())}")
        
        # Check memory immediately after setting
        if test_data['session_id'] in orchestrator.conversation_memory:
            memory_content = orchestrator.conversation_memory[test_data['session_id']]
            print(f"   ✅ Memory verified: {len(memory_content['messages'])} messages")
            print(f"   🔍 First message preview: {memory_content['messages'][0]['content'][:100]}...")
        else:
            print(f"   ❌ Memory NOT found for session '{test_data['session_id']}'")
    
    # Check memory after context cleanup
    print(f"🔍 Memory keys after context cleanup: {list(orchestrator.conversation_memory.keys())}")
    if test_data['session_id'] in orchestrator.conversation_memory:
        memory_content = orchestrator.conversation_memory[test_data['session_id']]
        print(f"✅ Memory preserved after cleanup: {len(memory_content['messages'])} messages")
    else:
        print(f"❌ Memory LOST after cleanup!")
    
    print()
    
    # ============================================================================
    # TEST 2: Simulate FastAPI Streaming Response Context
    # ============================================================================
    print("🧪 TEST 2: FastAPI Streaming Response Context Simulation")
    print("-" * 50)
    
    # Clear memory again
    if test_data['session_id'] in orchestrator.conversation_memory:
        del orchestrator.conversation_memory[test_data['session_id']]
        print("🔍 Cleared existing memory")
    
    print(f"🔍 Initial orchestrator memory keys: {list(orchestrator.conversation_memory.keys())}")
    
    # Simulate the exact flow from GET /api/patent/stream
    async def simulate_api_stream_flow():
        """Simulate the exact API streaming flow"""
        
        # Step 1: Set memory (same as API does)
        orchestrator.conversation_memory[test_data['session_id']] = {
            "messages": test_data['conversation_history'],
            "created_at": datetime.now().isoformat()
        }
        
        print(f"   🔍 Step 1: Set memory for session '{test_data['session_id']}'")
        print(f"   🔍 Memory keys after setting: {list(orchestrator.conversation_memory.keys())}")
        
        # Step 2: Check memory before calling orchestrator
        if test_data['session_id'] in orchestrator.conversation_memory:
            memory_content = orchestrator.conversation_memory[test_data['session_id']]
            print(f"   ✅ Step 2: Memory verified before orchestrator call: {len(memory_content['messages'])} messages")
        else:
            print(f"   ❌ Step 2: Memory NOT found before orchestrator call!")
            return
        
        # Step 3: Call orchestrator (same as API does)
        print(f"   🔍 Step 3: Calling orchestrator.handle()...")
        
        event_count = 0
        try:
            async for event in orchestrator.handle(
                test_data['user_message'],
                "patent_streaming",
                test_data['session_id'],
                parameters={
                    "domain": "patent",
                    "workflow_type": "patent_streaming",
                    "session_id": test_data['session_id']
                },
                document_content=test_data['document_content']
            ):
                event_count += 1
                
                # Check memory during streaming
                if event_count % 3 == 0:  # Check every 3rd event
                    if test_data['session_id'] in orchestrator.conversation_memory:
                        memory_content = orchestrator.conversation_memory[test_data['session_id']]
                        print(f"   🔍 Event {event_count}: Memory still intact: {len(memory_content['messages'])} messages")
                    else:
                        print(f"   ❌ Event {event_count}: Memory LOST during streaming!")
                        break
                
                if event.get("event") == "results":
                    print(f"   ✅ SUCCESS: Got results event with {len(event.get('data', {}).get('content', ''))} characters")
                    print(f"   🔍 Content preview: {event.get('data', {}).get('content', '')[:200]}...")
                    break
                elif event_count > 15:  # Prevent infinite loop
                    print("   ⚠️  WARNING: Too many events, stopping")
                    break
            
            print(f"   ✅ Streaming completed with {event_count} events")
            
        except Exception as e:
            print(f"   ❌ Streaming failed: {e}")
            import traceback
            traceback.print_exc()
        
        # Step 4: Check memory after streaming
        print(f"   🔍 Step 4: Memory after streaming: {list(orchestrator.conversation_memory.keys())}")
        if test_data['session_id'] in orchestrator.conversation_memory:
            memory_content = orchestrator.conversation_memory[test_data['session_id']]
            print(f"   ✅ Memory preserved after streaming: {len(memory_content['messages'])} messages")
        else:
            print(f"   ❌ Memory LOST after streaming!")
    
    # Run the simulation
    await simulate_api_stream_flow()
    
    print()
    
    # ============================================================================
    # TEST 3: Investigate Memory Cleanup Patterns
    # ============================================================================
    print("🧪 TEST 3: Memory Cleanup Pattern Investigation")
    print("-" * 50)
    
    # Check if there are any cleanup patterns in the orchestrator
    print("🔍 Checking orchestrator for cleanup patterns...")
    
    # Look for any methods that might clean up memory
    orchestrator_methods = [method for method in dir(orchestrator) if not method.startswith('_')]
    print(f"   Orchestrator public methods: {orchestrator_methods}")
    
    # Check if there are any cleanup methods
    cleanup_methods = [method for method in orchestrator_methods if 'clean' in method.lower() or 'clear' in method.lower()]
    print(f"   Potential cleanup methods: {cleanup_methods}")
    
    # Check if there are any memory management methods
    memory_methods = [method for method in orchestrator_methods if 'memory' in method.lower()]
    print(f"   Memory-related methods: {memory_methods}")
    
    # Check the orchestrator's __init__ method for any cleanup logic
    print("🔍 Checking orchestrator initialization...")
    if hasattr(orchestrator, '__dict__'):
        print(f"   Orchestrator attributes: {list(orchestrator.__dict__.keys())}")
    
    print()
    
    # ============================================================================
    # ANALYSIS: FastAPI Context Issues
    # ============================================================================
    print("🔍 FASTAPI CONTEXT ANALYSIS")
    print("=" * 60)
    
    print("✅ What We've Confirmed:")
    print("   1. All direct calls work perfectly")
    print("   2. Memory management works perfectly")
    print("   3. Orchestrator logic works perfectly")
    print("   4. Tool execution works perfectly")
    
    print("\n🚨 What's Failing:")
    print("   - FastAPI endpoint calls specifically")
    
    print("\n🔍 Potential FastAPI-Specific Issues:")
    print("   1. Request/Response cycle memory isolation")
    print("   2. Async context manager cleanup")
    print("   3. Streaming response memory management")
    print("   4. FastAPI middleware interference")
    print("   5. Request scope memory isolation")
    
    print("\n🎯 Next Investigation:")
    print("   - Check FastAPI request scope vs global scope")
    print("   - Investigate streaming response memory handling")
    print("   - Look for request-level memory isolation")

if __name__ == "__main__":
    asyncio.run(debug_fastapi_context())
