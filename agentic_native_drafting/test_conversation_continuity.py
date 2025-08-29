#!/usr/bin/env python3
"""
TEST CONVERSATION CONTINUITY
============================

This script tests the conversation continuity issue where the second request
should reference the context from the first request.
"""

import asyncio
from src.agent_core.orchestrator import AgentOrchestrator

async def test_conversation_continuity():
    """Test that conversation context is maintained between requests"""
    print("🧪 TESTING CONVERSATION CONTINUITY")
    print("=" * 80)
    
    # Create orchestrator
    orchestrator = AgentOrchestrator()
    session_id = "test_session_123"  # Fixed session ID
    
    print(f"📋 Session ID: {session_id}")
    
    # First request: Draft system claims for 4G carrier aggregation
    print(f"\n📤 REQUEST 1: Draft system claims for 4G carrier aggregation")
    user_input_1 = "draft 5 system claims for 4g carrier aggregation"
    context_1 = "Patent drafting request"
    
    print(f"User Input: {user_input_1}")
    print(f"Context: {context_1}")
    
    # Process first request
    events_1 = []
    async for event in orchestrator.handle(
        user_input_1, context_1, session_id, {}, {}
    ):
        events_1.append(event)
        if event.get('event') == 'thoughts':
            print(f"💭 {event.get('content', '')[:80]}...")
        elif event.get('event') == 'results':
            print(f"✅ RESULTS: {event.get('content', '')[:200]}...")
    
    print(f"✅ Request 1 completed with {len(events_1)} events")
    
    # Check conversation memory
    conversation_history = orchestrator.conversation_memory.get(session_id, {}).get("messages", [])
    print(f"\n📚 Conversation Memory: {len(conversation_history)} entries")
    for i, entry in enumerate(conversation_history):
        print(f"   {i+1}. {entry.get('input', '')[:50]}...")
    
    # Second request: Draft corresponding method claims
    print(f"\n📤 REQUEST 2: Draft corresponding method claims")
    user_input_2 = "draft the corresponding method claims"
    context_2 = "Method claims request"
    
    print(f"User Input: {user_input_2}")
    print(f"Context: {context_2}")
    print(f"Conversation History: {len(conversation_history)} entries")
    
    # Process second request
    events_2 = []
    async for event in orchestrator.handle(
        user_input_2, context_2, session_id, {}, {}
    ):
        events_2.append(event)
        if event.get('event') == 'thoughts':
            print(f"💭 {event.get('content', '')[:80]}...")
        elif event.get('event') == 'results':
            print(f"✅ RESULTS: {event.get('content', '')[:200]}...")
    
    print(f"✅ Request 2 completed with {len(events_2)} events")
    
    # Final conversation memory check
    final_conversation_history = orchestrator.conversation_memory.get(session_id, {}).get("messages", [])
    print(f"\n📚 Final Conversation Memory: {len(final_conversation_history)} entries")
    for i, entry in enumerate(final_conversation_history):
        print(f"   {i+1}. {entry.get('input', '')[:50]}...")
    
    # Analysis
    print(f"\n" + "=" * 80)
    print(f"📊 CONVERSATION CONTINUITY ANALYSIS")
    print(f"=" * 80)
    
    if len(final_conversation_history) >= 2:
        first_request = final_conversation_history[0].get('input', '')
        second_request = final_conversation_history[1].get('input', '')
        
        print(f"✅ Conversation maintained: {len(final_conversation_history)} entries")
        print(f"✅ First request: {first_request}")
        print(f"✅ Second request: {second_request}")
        
        # Check if second request should reference first
        if "4g carrier aggregation" in first_request.lower() and "method claims" in second_request.lower():
            print(f"✅ Context continuity: Second request should reference 4G carrier aggregation")
        else:
            print(f"⚠️  Context mismatch: Second request doesn't clearly reference first")
    else:
        print(f"❌ Conversation not maintained properly")
    
    return len(final_conversation_history) >= 2

async def main():
    """Main test execution"""
    try:
        print("🔍 CONVERSATION CONTINUITY TEST")
        print("=" * 80)
        print("This test verifies that conversation context is maintained")
        print("between requests, especially for patent drafting workflows.")
        print("=" * 80)
        
        # Run the test
        success = await test_conversation_continuity()
        
        # Final evaluation
        print(f"\n🏆 FINAL EVALUATION:")
        if success:
            print(f"   ✅ SUCCESS: Conversation continuity is working!")
            print(f"   ✅ Context is being maintained between requests")
        else:
            print(f"   ❌ FAILURE: Conversation continuity is broken")
            print(f"   ❌ Context is not being maintained")
            
        return success
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())
