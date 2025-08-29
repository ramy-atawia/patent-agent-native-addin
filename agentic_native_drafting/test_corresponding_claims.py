#!/usr/bin/env python3
"""
Test script to verify that ContentDraftingTool properly uses conversation history
to understand "corresponding method claims" requests.
"""

import asyncio
import json
from src.tools.claim_drafting_tool import ContentDraftingTool
from src.utils.response_standardizer import create_thought_event, create_results_event

async def test_corresponding_claims():
    """Test that the tool understands 'corresponding method claims' from conversation history"""
    
    print("🔍 CORRESPONDING CLAIMS TEST")
    print("=" * 60)
    print("This test verifies that ContentDraftingTool properly uses")
    print("conversation history to understand follow-up requests.")
    print("=" * 60)
    
    # Create the tool
    tool = ContentDraftingTool()
    
    # Simulate the conversation history from the user's example
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
    input_text = "draft corresponding method claims"
    
    # Document content (empty for this test)
    document_content = {}
    
    print(f"\n🧪 TESTING CORRESPONDING METHOD CLAIMS")
    print("=" * 60)
    print(f"📤 Input: {input_text}")
    print(f"📤 Conversation History: {len(conversation_history)} entries")
    print(f"📤 Previous Claims: {len(conversation_history[1]['content'].split('Claim')) - 1} claims")
    
    try:
        # Execute the tool
        event_count = 0
        results_event = None
        
        async for event in tool.run(
            input_text, 
            {}, 
            conversation_history, 
            document_content
        ):
            event_count += 1
            print(f"\n📥 Event {event_count}: {event.get('event', 'unknown')}")
            
            if event.get('event') == 'thoughts':
                print(f"   💭 {event.get('content', '')}")
            elif event.get('event') == 'results':
                results_event = event
                print(f"   ✅ RESULTS: {event.get('response', '')[:200]}...")
            elif event.get('event') == 'error':
                print(f"   ❌ ERROR: {event.get('error', '')}")
        
        # Evaluate the results
        print(f"\n🏆 FINAL EVALUATION:")
        
        if results_event:
            response = results_event.get('response', '')
            
            # Check if the response contains method claims
            if 'method' in response.lower():
                print("   ✅ SUCCESS: Generated method claims")
            else:
                print("   ❌ FAILURE: No method claims generated")
            
            # Check if it references the previous system claims
            if 'carrier aggregation' in response.lower():
                print("   ✅ SUCCESS: Maintains context of carrier aggregation")
            else:
                print("   ❌ FAILURE: Lost context of carrier aggregation")
            
            # Check if it's generic or specific
            if 'patent claim' in response.lower() and 'invention' in response.lower():
                print("   ❌ FAILURE: Generated generic patent drafting claims instead of specific method claims")
            else:
                print("   ✅ SUCCESS: Generated specific method claims, not generic ones")
            
            print(f"\n📋 FULL RESPONSE:")
            print(response)
            
        else:
            print("   ❌ FAILURE: No results event generated")
            
    except Exception as e:
        print(f"💥 Tool execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_corresponding_claims())
