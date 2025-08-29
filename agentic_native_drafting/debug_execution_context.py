#!/usr/bin/env python3
"""
Debug Execution Context Differences

This script compares the execution context between:
1. Direct orchestrator calls (working)
2. API endpoint calls (failing)

The goal is to identify the subtle execution difference that causes
the API to fail while direct calls work perfectly.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent_core.orchestrator import AgentOrchestrator
from src.agent_core.api import orchestrator, session_manager
from src.tools.claim_drafting_tool import ContentDraftingTool

async def debug_execution_context():
    """Compare execution contexts between direct calls and API calls"""
    
    print("🔍 DEBUG: Execution Context Comparison")
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
    # TEST 1: Direct Orchestrator Call (Working)
    # ============================================================================
    print("🧪 TEST 1: Direct Orchestrator Call (Working)")
    print("-" * 50)
    
    # Create a fresh orchestrator instance (not the API's global one)
    fresh_orchestrator = AgentOrchestrator()
    
    print("🔍 Creating fresh orchestrator instance...")
    print(f"   Fresh orchestrator ID: {id(fresh_orchestrator)}")
    print(f"   Fresh orchestrator memory keys: {list(fresh_orchestrator.conversation_memory.keys())}")
    
    # Set memory manually (same as API does)
    fresh_orchestrator.conversation_memory[test_data['session_id']] = {
        "messages": test_data['conversation_history'],
        "created_at": datetime.now().isoformat()
    }
    
    print(f"🔍 Set memory for session '{test_data['session_id']}'")
    print(f"   Memory keys after setting: {list(fresh_orchestrator.conversation_memory.keys())}")
    print(f"   Memory content preview: {fresh_orchestrator.conversation_memory[test_data['session_id']]['messages'][0]['content'][:100]}...")
    
    # Call orchestrator directly
    print("🔍 Calling fresh orchestrator.handle() directly...")
    try:
        event_count = 0
        async for event in fresh_orchestrator.handle(
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
            if event.get("event") == "results":
                print(f"✅ SUCCESS: Got results event with {len(event.get('data', {}).get('content', ''))} characters")
                print(f"   Content preview: {event.get('data', {}).get('content', '')[:200]}...")
                break
            elif event_count > 10:  # Prevent infinite loop
                print("⚠️  WARNING: Too many events, stopping")
                break
        
        print(f"✅ Direct call completed successfully with {event_count} events")
        
    except Exception as e:
        print(f"❌ Direct call failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # ============================================================================
    # TEST 2: API's Global Orchestrator Call (Should Work)
    # ============================================================================
    print("🧪 TEST 2: API's Global Orchestrator Call (Should Work)")
    print("-" * 50)
    
    print(f"🔍 Using API's global orchestrator instance...")
    print(f"   Global orchestrator ID: {id(orchestrator)}")
    print(f"   Global orchestrator memory keys: {list(orchestrator.conversation_memory.keys())}")
    
    # Clear any existing memory for this session
    if test_data['session_id'] in orchestrator.conversation_memory:
        del orchestrator.conversation_memory[test_data['session_id']]
        print(f"🔍 Cleared existing memory for session '{test_data['session_id']}'")
    
    # Set memory manually (same as API does)
    orchestrator.conversation_memory[test_data['session_id']] = {
        "messages": test_data['conversation_history'],
        "created_at": datetime.now().isoformat()
    }
    
    print(f"🔍 Set memory for session '{test_data['session_id']}'")
    print(f"   Memory keys after setting: {list(orchestrator.conversation_memory.keys())}")
    print(f"   Memory content preview: {orchestrator.conversation_memory[test_data['session_id']]['messages'][0]['content'][:100]}...")
    
    # Call orchestrator directly using the API's global instance
    print("🔍 Calling API's global orchestrator.handle() directly...")
    try:
        event_count = 0
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
            if event.get("event") == "results":
                print(f"✅ SUCCESS: Got results event with {len(event.get('data', {}).get('content', ''))} characters")
                print(f"   Content preview: {event.get('data', {}).get('content', '')[:200]}...")
                break
            elif event_count > 10:  # Prevent infinite loop
                print("⚠️  WARNING: Too many events, stopping")
                break
        
        print(f"✅ Global orchestrator call completed successfully with {event_count} events")
        
    except Exception as e:
        print(f"❌ Global orchestrator call failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # ============================================================================
    # TEST 3: Simulate API Session Manager Flow
    # ============================================================================
    print("🧪 TEST 3: Simulate API Session Manager Flow")
    print("-" * 50)
    
    # Create session and run using session manager (same as API does)
    print("🔍 Creating session and run using session manager...")
    
    session_id = session_manager.create_session(test_data['session_id'])
    print(f"   Created session: {session_id}")
    
    run_id = session_manager.create_run(
        session_id=session_id,
        user_message=test_data['user_message'],
        conversation_history=test_data['conversation_history'],
        document_content=test_data['document_content']
    )
    print(f"   Created run: {run_id}")
    
    # Retrieve run data (same as API does)
    run_data = session_manager.get_run(run_id)
    print(f"   Retrieved run data:")
    print(f"     user_message: {run_data['user_message']}")
    print(f"     conversation_history_length: {len(run_data['conversation_history'])}")
    print(f"     document_content_keys: {list(run_data['document_content'].keys())}")
    
    # Extract data (same as API does)
    user_input = run_data["user_message"]
    session_id = run_data["session_id"]
    conversation_history = run_data["conversation_history"]
    document_content = run_data["document_content"]
    
    print(f"   Extracted data:")
    print(f"     user_input: {user_input}")
    print(f"     session_id: {session_id}")
    print(f"     conversation_history_length: {len(conversation_history)}")
    print(f"     document_content_keys: {list(document_content.keys())}")
    
    # Set orchestrator memory (same as API does)
    print("🔍 Setting orchestrator memory...")
    if conversation_history:
        orchestrator.conversation_memory[session_id] = {
            "messages": conversation_history,
            "created_at": datetime.now().isoformat()
        }
        print(f"   Set memory for session '{session_id}' with {len(conversation_history)} messages")
        print(f"   Memory keys after setting: {list(orchestrator.conversation_memory.keys())}")
    
    # Call orchestrator (same as API does)
    print("🔍 Calling orchestrator.handle() with extracted data...")
    try:
        event_count = 0
        async for event in orchestrator.handle(
            user_input,
            "patent_streaming",
            session_id,
            parameters={
                "domain": "patent",
                "workflow_type": "patent_streaming",
                "session_id": session_id
            },
            document_content=document_content
        ):
            event_count += 1
            if event.get("event") == "results":
                print(f"✅ SUCCESS: Got results event with {len(event.get('data', {}).get('content', ''))} characters")
                print(f"   Content preview: {event.get('data', {}).get('content', '')[:200]}...")
                break
            elif event_count > 10:  # Prevent infinite loop
                print("⚠️  WARNING: Too many events, stopping")
                break
        
        print(f"✅ Session manager flow completed successfully with {event_count} events")
        
    except Exception as e:
        print(f"❌ Session manager flow failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # ============================================================================
    # ANALYSIS: Compare Execution Contexts
    # ============================================================================
    print("🔍 EXECUTION CONTEXT ANALYSIS")
    print("=" * 60)
    
    print("✅ What's Working:")
    print("   1. Direct orchestrator calls (fresh instance)")
    print("   2. Direct orchestrator calls (API's global instance)")
    print("   3. Session manager flow simulation")
    
    print("\n🚨 What's Failing:")
    print("   - API endpoint calls (despite identical data and flow)")
    
    print("\n🔍 Potential Execution Context Differences:")
    print("   1. FastAPI request/response cycle")
    print("   2. Async context isolation")
    print("   3. Memory cleanup during API execution")
    print("   4. Streaming response effects")
    print("   5. Request middleware interference")
    
    print("\n🎯 Next Investigation:")
    print("   - Compare FastAPI request context vs direct call context")
    print("   - Check for memory cleanup during streaming")
    print("   - Investigate async context differences")

if __name__ == "__main__":
    asyncio.run(debug_execution_context())
