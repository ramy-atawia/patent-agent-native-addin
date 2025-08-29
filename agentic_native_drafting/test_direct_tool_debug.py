#!/usr/bin/env python3
"""
Direct Tool Debug Test
Tests the ContentDraftingTool directly with the exact same data
to see if the issue is in the tool or the API flow.
"""

import asyncio
import json
from src.tools.claim_drafting_tool import ContentDraftingTool

async def test_direct_tool_debug():
    """Test the ContentDraftingTool directly with the exact same data"""
    
    print("🔍 DIRECT TOOL DEBUG TEST")
    print("=" * 60)
    print("Testing ContentDraftingTool directly with the exact same data")
    print("to isolate whether the issue is in the tool or the API flow.")
    print("=" * 60)
    
    # Create the tool
    tool = ContentDraftingTool()
    
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
    input_text = "draft the corresponding method claims"
    
    # Document content (empty for this test)
    document_content = {}
    
    print(f"\n🧪 TESTING DIRECT TOOL CALL")
    print("=" * 60)
    print(f"📤 Input: {input_text}")
    print(f"📤 Conversation History: {len(conversation_history)} entries")
    print(f"📤 First message: {conversation_history[0]['content'][:100]}...")
    print(f"📤 Second message: {conversation_history[1]['content'][:100]}...")
    
    print(f"\n🔍 DEBUGGING TOOL EXECUTION")
    print("=" * 60)
    
    try:
        # Call the tool directly
        event_count = 0
        results_event = None
        
        print(f"📞 Calling tool.run() with:")
        print(f"   input_text: {input_text}")
        print(f"   parameters: {{}}")
        print(f"   conversation_history: {len(conversation_history)} entries")
        print(f"   document_content: {document_content}")
        
        async for event in tool.run(
            input_text, 
            {}, 
            conversation_history, 
            document_content
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
            
            # Check if it's specific to the invention or generic
            if 'patent claim' in response_text.lower() and 'invention' in response_text.lower():
                print("❌ FAILURE: Generated generic patent drafting claims")
            else:
                print("✅ SUCCESS: Generated specific method claims for the invention")
            
            # Count the claims generated
            claim_count = response_text.count('Claim')
            print(f"📊 Claims Generated: {claim_count}")
            
            print(f"\n📋 FULL TOOL RESPONSE:")
            print(response_text)
            
        else:
            print("❌ FAILURE: No results event generated")
            
    except Exception as e:
        print(f"💥 Tool execution failed: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🎯 TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_direct_tool_debug())
