#!/usr/bin/env python3
"""
Backend Flow Debug Test
Tests the complete backend flow to see where the conversation history is getting lost.
"""

import asyncio
import json
from datetime import datetime
from src.agent_core.orchestrator import AgentOrchestrator
from src.agent_core.api import session_manager

async def debug_backend_flow():
    """Debug the complete backend flow step by step"""
    
    print("🔍 BACKEND FLOW DEBUG TEST")
    print("=" * 60)
    print("Testing the complete backend flow to identify where")
    print("conversation history is getting lost.")
    print("=" * 60)
    
    # Import the same orchestrator instance that the API uses
    from src.agent_core.api import orchestrator
    
    # Test session ID
    session_id = "debug-session-4g-carrier-aggregation"
    
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
    context = "patent_streaming"
    document_content = {}
    
    print(f"\n🧪 TESTING BACKEND FLOW")
    print("=" * 60)
    print(f"📤 Session ID: {session_id}")
    print(f"📤 User Input: {user_input}")
    print(f"📤 Conversation History: {len(conversation_history)} entries")
    print(f"📤 Document Content: {document_content}")
    
    print(f"\n🔍 STEP 1: Check orchestrator initial state")
    print("=" * 60)
    print(f"📋 Orchestrator memory keys: {list(orchestrator.conversation_memory.keys())}")
    print(f"📋 Orchestrator memory size: {len(orchestrator.conversation_memory)}")
    
    print(f"\n🔍 STEP 2: Set conversation memory (like API does)")
    print("=" * 60)
    orchestrator.conversation_memory[session_id] = {
        "messages": conversation_history,
        "created_at": datetime.now().isoformat()
    }
    print(f"✅ Set memory for session '{session_id}' with {len(conversation_history)} messages")
    print(f"📋 Memory keys after setting: {list(orchestrator.conversation_memory.keys())}")
    print(f"📋 Memory for our session: {len(orchestrator.conversation_memory[session_id]['messages'])} messages")
    
    print(f"\n🔍 STEP 3: Check memory content")
    print("=" * 60)
    session_memory = orchestrator.conversation_memory.get(session_id, {})
    messages = session_memory.get("messages", [])
    print(f"📋 Session memory keys: {list(session_memory.keys())}")
    print(f"📋 Messages count: {len(messages)}")
    if messages:
        print(f"📋 First message role: {messages[0].get('role', 'NO ROLE')}")
        print(f"📋 First message content preview: {messages[0].get('content', 'NO CONTENT')[:100]}...")
    
    print(f"\n🔍 STEP 4: Test orchestrator.handle() call")
    print("=" * 60)
    print(f"🚀 Calling orchestrator.handle() with session_id: {session_id}")
    
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
    asyncio.run(debug_backend_flow())
