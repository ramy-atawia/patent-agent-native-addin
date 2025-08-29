#!/usr/bin/env python3
"""
Direct Backend Call Debug Test
Calls the backend functions directly to see debug output in the terminal.
"""

import asyncio
import json
from datetime import datetime
from src.agent_core.api import session_manager, orchestrator

async def debug_direct_backend_call():
    """Debug the backend flow by calling functions directly"""
    
    print("🔍 DIRECT BACKEND DEBUG TEST")
    print("=" * 60)
    print("Calling backend functions directly to see debug output")
    print("=" * 60)
    
    # Test session ID
    session_id = "debug-direct-session-4g-carrier-aggregation"
    
    # The exact conversation history from the user's scenario
    conversation_history = [
        {
            "role": "user",
            "content": "draft 5 system claims for 4g carrier aggregation",
            "timestamp": "2025-08-27T21:40:00.000Z"
        },
        {
            "role": "assistant",
            "content": "Successfully drafted 5 content items\n\nGenerated Patent Claims:\n\nClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\n\nClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\n\nClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\n\nClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\n\nClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.",
            "timestamp": "2025-08-27T21:43:00.000Z"
        }
    ]
    
    # Current request for corresponding method claims
    user_input = "draft the corresponding method claims"
    document_content = {}
    
    print(f"\n🧪 TESTING DIRECT BACKEND CALL")
    print("=" * 60)
    print(f"📤 Session ID: {session_id}")
    print(f"📤 User Input: {user_input}")
    print(f"📤 Conversation History: {len(conversation_history)} entries")
    print(f"📤 Document Content: {document_content}")
    
    print(f"\n🔍 STEP 1: Create session and run (like API does)")
    print("=" * 60)
    
    # Create session and run like the API does
    session_id = session_manager.create_session(session_id)
    print(f"✅ Created session: {session_id}")
    
    run_id = session_manager.create_run(
        session_id=session_id,
        user_message=user_input,
        conversation_history=conversation_history,
        document_content=document_content
    )
    print(f"✅ Created run: {run_id}")
    
    print(f"\n🔍 STEP 2: Get run data (like API does)")
    print("=" * 60)
    
    # Get run data like the API does
    run_data = session_manager.get_run(run_id)
    print(f"📋 Retrieved run data:")
    print(f"   user_message: {run_data['user_message']}")
    print(f"   session_id: {run_data['session_id']}")
    print(f"   conversation_history_length: {len(run_data['conversation_history'])}")
    print(f"   document_content_keys: {list(run_data['document_content'].keys()) if run_data['document_content'] else 'None'}")
    
    print(f"\n🔍 STEP 3: Set orchestrator memory (like API does)")
    print("=" * 60)
    
    # Set orchestrator memory like the API does
    if run_data['conversation_history']:
        orchestrator.conversation_memory[session_id] = {
            "messages": run_data['conversation_history'],
            "created_at": datetime.now().isoformat()
        }
        print(f"✅ Set memory for session '{session_id}' with {len(run_data['conversation_history'])} messages")
        print(f"📋 Memory keys after setting: {list(orchestrator.conversation_memory.keys())}")
        print(f"📋 First message preview: {run_data['conversation_history'][0]['content'][:100]}...")
    else:
        print(f"❌ No conversation history to set")
    
    print(f"\n🔍 STEP 4: Call orchestrator.handle directly")
    print("=" * 60)
    
    # Call orchestrator.handle directly
    context = "patent_streaming"
    
    print(f"🚀 Calling orchestrator.handle with:")
    print(f"   user_input: {user_input}")
    print(f"   context: {context}")
    print(f"   session_id: {session_id}")
    print(f"   document_content: {document_content}")
    
    try:
        event_count = 0
        results_event = None
        
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
            print(f"\n📥 Event {event_count}: {event.get('event', 'unknown')}")
            
            if event.get('event') == 'thoughts':
                content = event.get('content', '')
                print(f"   💭 {content}")
            elif event.get('event') == 'results':
                results_event = event
                response_text = event.get('response', '')
                print(f"   ✅ RESULTS: {response_text[:200]}...")
            elif event.get('event') == 'error':
                error_msg = event.get('error', '')
                print(f"   ❌ ERROR: {error_msg}")
        
        # Analyze the results
        print(f"\n🏆 RESULTS ANALYSIS:")
        print("=" * 60)
        
        if results_event:
            response_text = results_event.get('response', '')
            
            # Check if method claims were generated
            if 'method' in response_text.lower():
                print("✅ SUCCESS: Generated method claims")
            else:
                print("❌ FAILURE: No method claims generated")
            
            # Check if it maintains 4G carrier aggregation context
            if 'carrier aggregation' in response_text.lower() or '4g' in response_text.lower():
                print("✅ SUCCESS: Maintains 4G carrier aggregation context")
            else:
                print("❌ FAILURE: Lost 4G carrier aggregation context")
            
            # Count the claims generated
            claim_count = response_text.count('Claim')
            print(f"📊 Claims Generated: {claim_count}")
            
            print(f"\n📋 FULL ORCHESTRATOR RESPONSE:")
            print(response_text)
            
        else:
            print("❌ FAILURE: No results event generated")
            
    except Exception as e:
        print(f"💥 Orchestrator execution failed: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🎯 TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(debug_direct_backend_call())
