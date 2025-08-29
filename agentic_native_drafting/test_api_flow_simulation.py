#!/usr/bin/env python3
"""
Test API Flow Simulation

This script simulates the exact API flow to identify where the difference
occurs between API calls and direct calls.
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent_core.api import orchestrator

async def simulate_api_flow():
    """Simulate the exact API flow to identify differences"""
    
    print("🔍 SIMULATING EXACT API FLOW")
    print("=" * 60)
    
    # Test data (same as our scenario)
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
    print(f"   Document Content Length: {len(test_data['document_content']['text'])} characters")
    print(f"   Session ID: {test_data['session_id']}")
    print()
    
    # Step 1: Simulate the exact API flow from GET /api/patent/stream
    print("🔍 STEP 1: SIMULATING API FLOW")
    print("-" * 40)
    
    # Extract variables exactly as the API does
    user_input = test_data["user_message"]           # ✅ String
    session_id = test_data["session_id"]             # ✅ String
    conversation_history = test_data["conversation_history"]  # ✅ List[Dict]
    document_content = test_data["document_content"] # ✅ Dict
    context = "patent_streaming"                     # ✅ String (hardcoded in API)
    
    print(f"   Extracted user_input: {user_input}")
    print(f"   Extracted session_id: {session_id}")
    print(f"   Extracted conversation_history length: {len(conversation_history)}")
    print(f"   Extracted document_content keys: {list(document_content.keys())}")
    print(f"   Hardcoded context: {context}")
    print()
    
    # Step 2: Set orchestrator memory exactly as the API does
    print("🔍 STEP 2: SETTING ORCHESTRATOR MEMORY")
    print("-" * 40)
    
    # Clear any existing memory for this session
    if session_id in orchestrator.conversation_memory:
        del orchestrator.conversation_memory[session_id]
        print(f"   ✅ Cleared existing memory for session: {session_id}")
    
    # Set memory exactly as the API does
    orchestrator.conversation_memory[session_id] = {
        "messages": conversation_history,
        "created_at": datetime.now().isoformat()
    }
    print(f"   ✅ Set memory for session '{session_id}' with {len(conversation_history)} messages")
    print(f"   ✅ Memory keys after setting: {list(orchestrator.conversation_memory.keys())}")
    print(f"   ✅ First message preview: {conversation_history[0]['content'][:100]}...")
    print()
    
    # Step 3: Call orchestrator.handle exactly as the API does
    print("🔍 STEP 3: CALLING ORCHESTRATOR.HANDLE")
    print("-" * 40)
    
    print(f"   About to call orchestrator.handle with session_id: '{session_id}'")
    print(f"   Parameters:")
    print(f"     user_input: {user_input}")
    print(f"     context: {context}")
    print(f"     session_id: {session_id}")
    print(f"     document_content: {document_content}")
    print()
    
    # Call orchestrator.handle exactly as the API does
    event_count = 0
    results_event = None
    
    try:
        async for event in orchestrator.handle(
            user_input, 
            context, 
            session_id,
            parameters={
                "domain": "patent",
                "workflow_type": "patent_streaming",
                "session_id": session_id
            },
            document_content=document_content
        ):
            event_count += 1
            print(f"📥 Event {event_count}: {event.get('event', 'unknown')}")
            
            if event.get("event") == "results":
                results_event = event
                print(f"✅ SUCCESS: Got results event")
                print(f"   Response: {event.get('response', 'No response')}")
                if 'data' in event and 'content' in event['data']:
                    print(f"   Content items: {len(event['data']['content'])}")
                    for i, item in enumerate(event['data']['content'][:3]):  # Show first 3
                        print(f"     Item {i+1}: {item.get('content_text', 'No text')[:100]}...")
                break
            elif event_count > 15:  # Prevent infinite loop
                print("⚠️  WARNING: Too many events, stopping")
                break
        
        print(f"✅ Orchestrator execution completed with {event_count} events")
        
    except Exception as e:
        print(f"❌ Orchestrator execution failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Step 4: Analyze the results
    print("🔍 STEP 4: ANALYSIS")
    print("-" * 40)
    
    if results_event:
        print("✅ API FLOW SIMULATION SUCCESSFUL")
        print("   The orchestrator is working correctly in the simulated API flow")
        
        # Check if we got the right type of claims
        if 'data' in results_event and 'content' in results_event['data']:
            content_items = results_event['data']['content']
            print(f"   Generated {len(content_items)} content items")
            
            # Check if any contain 4G carrier aggregation
            has_4g_context = any(
                "4g" in item.get('content_text', '').lower() or 
                "carrier aggregation" in item.get('content_text', '').lower()
                for item in content_items
            )
            
            if has_4g_context:
                print("   ✅ SUCCESS: Generated claims contain 4G carrier aggregation context")
            else:
                print("   ❌ FAILURE: Generated claims do NOT contain 4G carrier aggregation context")
                print("   This matches the API behavior - the issue is elsewhere!")
    else:
        print("❌ API FLOW SIMULATION FAILED")
        print("   No results event received")
    
    print()
    print("✅ API flow simulation completed")

if __name__ == "__main__":
    asyncio.run(simulate_api_flow())
