#!/usr/bin/env python3
"""
Test LLM Debug Directly

This script directly tests the LLM call to see what's being sent and received,
bypassing the API to get immediate debug output.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.tools.claim_drafting_tool import ContentDraftingTool

async def test_llm_debug_direct():
    """Test the LLM call directly to see debug output"""
    
    print("🔍 TESTING LLM DEBUG DIRECTLY")
    print("=" * 60)
    
    # Test data (same as our scenario)
    test_data = {
        "input_text": "draft the corresponding method claims",
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
        }
    }
    
    print("📋 Test Data:")
    print(f"   Input Text: {test_data['input_text']}")
    print(f"   Conversation History: {len(test_data['conversation_history'])} entries")
    print(f"   Document Content Length: {len(test_data['document_content']['text'])} characters")
    print()
    
    # Create tool instance
    tool = ContentDraftingTool()
    
    print("🔍 Testing tool.run() directly...")
    print("-" * 40)
    
    try:
        # Call the tool directly
        event_count = 0
        async for event in tool.run(
            test_data['input_text'],
            parameters={
                "domain": "patent",
                "workflow_type": "patent_streaming",
                "session_id": "test-session-4g-carrier-aggregation"
            },
            conversation_history=test_data['conversation_history'],
            document_content=test_data['document_content']
        ):
            event_count += 1
            print(f"📥 Event {event_count}: {event.get('event', 'unknown')}")
            
            if event.get("event") == "results":
                print(f"✅ SUCCESS: Got results event")
                print(f"   Response: {event.get('response', 'No response')}")
                if 'data' in event and 'content' in event['data']:
                    print(f"   Content items: {len(event['data']['content'])}")
                    for i, item in enumerate(event['data']['content'][:3]):  # Show first 3
                        print(f"     Item {i+1}: {item.get('content_text', 'No text')[:100]}...")
                break
            elif event_count > 10:  # Prevent infinite loop
                print("⚠️  WARNING: Too many events, stopping")
                break
        
        print(f"✅ Tool execution completed with {event_count} events")
        
    except Exception as e:
        print(f"❌ Tool execution failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_llm_debug_direct())
