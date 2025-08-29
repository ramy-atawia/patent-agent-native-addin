#!/usr/bin/env python3
"""
TEST DETAILED CONTEXT USAGE
===========================

This script tests the detailed context usage to see if the LLM
is actually using the conversation history to generate relevant claims.
"""

import asyncio
import json
from src.agent_core.orchestrator import AgentOrchestrator

async def test_detailed_context_usage():
    """Test detailed context usage in patent claim generation"""
    print("🧪 TESTING DETAILED CONTEXT USAGE")
    print("=" * 80)
    
    # Create orchestrator
    orchestrator = AgentOrchestrator()
    session_id = "detailed_test_session_456"
    
    print(f"📋 Session ID: {session_id}")
    
    # First request: Draft system claims for 4G carrier aggregation
    print(f"\n📤 REQUEST 1: Draft system claims for 4G carrier aggregation")
    user_input_1 = "draft 5 system claims for 4g carrier aggregation"
    context_1 = "Patent drafting request for 4G technology"
    
    print(f"User Input: {user_input_1}")
    print(f"Context: {context_1}")
    
    # Process first request
    events_1 = []
    results_1 = ""
    async for event in orchestrator.handle(
        user_input_1, context_1, session_id, {}, {}
    ):
        events_1.append(event)
        if event.get('event') == 'thoughts':
            print(f"💭 {event.get('content', '')[:80]}...")
        elif event.get('event') == 'results':
            results_1 = event.get('content', '')
            print(f"✅ RESULTS: {results_1[:300]}...")
    
    print(f"✅ Request 1 completed with {len(events_1)} events")
    
    # Check conversation memory
    conversation_history = orchestrator.conversation_memory.get(session_id, {}).get("messages", [])
    print(f"\n📚 Conversation Memory: {len(conversation_history)} entries")
    for i, entry in enumerate(conversation_history):
        print(f"   {i+1}. {entry.get('input', '')[:50]}...")
    
    # Second request: Draft corresponding method claims
    print(f"\n📤 REQUEST 2: Draft corresponding method claims")
    user_input_2 = "draft the corresponding method claims"
    context_2 = "Method claims request - should reference 4G carrier aggregation"
    
    print(f"User Input: {user_input_2}")
    print(f"Context: {context_2}")
    print(f"Conversation History: {len(conversation_history)} entries")
    
    # Process second request
    events_2 = []
    results_2 = ""
    async for event in orchestrator.handle(
        user_input_2, context_2, session_id, {}, {}
    ):
        events_2.append(event)
        if event.get('event') == 'thoughts':
            print(f"💭 {event.get('content', '')[:80]}...")
        elif event.get('event') == 'results':
            results_2 = event.get('content', '')
            print(f"✅ RESULTS: {results_2[:300]}...")
    
    print(f"✅ Request 2 completed with {len(events_2)} events")
    
    # Final conversation memory check
    final_conversation_history = orchestrator.conversation_memory.get(session_id, {}).get("messages", [])
    print(f"\n📚 Final Conversation Memory: {len(final_conversation_history)} entries")
    for i, entry in enumerate(final_conversation_history):
        print(f"   {i+1}. {entry['input'][:50]}...")
    
    # Detailed Analysis
    print(f"\n" + "=" * 80)
    print(f"📊 DETAILED CONTEXT USAGE ANALYSIS")
    print(f"=" * 80)
    
    # Analyze first request results
    print(f"\n🔍 REQUEST 1 ANALYSIS:")
    if "4g" in results_1.lower() or "carrier aggregation" in results_1.lower():
        print(f"   ✅ 4G/Carrier aggregation context detected in results")
    else:
        print(f"   ❌ 4G/Carrier aggregation context NOT detected in results")
    
    if "system" in results_1.lower():
        print(f"   ✅ System claims context detected")
    else:
        print(f"   ❌ System claims context NOT detected")
    
    # Analyze second request results
    print(f"\n🔍 REQUEST 2 ANALYSIS:")
    if "4g" in results_2.lower() or "carrier aggregation" in results_2.lower():
        print(f"   ✅ 4G/Carrier aggregation context maintained in results")
    else:
        print(f"   ❌ 4G/Carrier aggregation context NOT maintained in results")
    
    if "method" in results_2.lower():
        print(f"   ✅ Method claims context detected")
    else:
        print(f"   ❌ Method claims context NOT detected")
    
    # Check for context continuity
    print(f"\n🔍 CONTEXT CONTINUITY ANALYSIS:")
    if ("4g" in results_1.lower() and "4g" in results_2.lower()) or \
       ("carrier aggregation" in results_1.lower() and "carrier aggregation" in results_2.lower()):
        print(f"   ✅ EXCELLENT: Technical context maintained between requests")
        print(f"   ✅ The LLM is using conversation history properly")
    else:
        print(f"   ❌ POOR: Technical context NOT maintained between requests")
        print(f"   ❌ The LLM is NOT using conversation history properly")
    
    # Check for appropriate claim types
    print(f"\n🔍 CLAIM TYPE ANALYSIS:")
    if "system" in results_1.lower() and "method" in results_2.lower():
        print(f"   ✅ EXCELLENT: Correct claim types generated (System → Method)")
    else:
        print(f"   ❌ POOR: Incorrect claim types generated")
    
    return {
        "context_maintained": ("4g" in results_1.lower() and "4g" in results_2.lower()) or \
                             ("carrier aggregation" in results_1.lower() and "carrier aggregation" in results_2.lower()),
        "claim_types_correct": "system" in results_1.lower() and "method" in results_2.lower(),
        "results_1": results_1,
        "results_2": results_2
    }

async def main():
    """Main test execution"""
    try:
        print("🔍 DETAILED CONTEXT USAGE TEST")
        print("=" * 80)
        print("This test verifies that the LLM is actually using")
        print("conversation history to generate contextually relevant claims.")
        print("=" * 80)
        
        # Run the test
        results = await test_detailed_context_usage()
        
        # Final evaluation
        print(f"\n🏆 FINAL EVALUATION:")
        if results["context_maintained"] and results["claim_types_correct"]:
            print(f"   🎉 OUTSTANDING: Context integration is working perfectly!")
            print(f"   ✅ Technical context maintained between requests")
            print(f"   ✅ Correct claim types generated")
            print(f"   ✅ LLM is using conversation history properly")
        elif results["context_maintained"]:
            print(f"   ✅ GOOD: Context is maintained but claim types may be incorrect")
        elif results["claim_types_correct"]:
            print(f"   ⚠️  FAIR: Claim types correct but context not maintained")
        else:
            print(f"   ❌ POOR: Both context and claim types are incorrect")
            print(f"   ❌ LLM is NOT using conversation history properly")
            
        return results
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(main())
