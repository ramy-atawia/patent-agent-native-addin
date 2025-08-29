#!/usr/bin/env python3
"""
TEST CONTENT DRAFTING TOOL DIRECT
=================================

This script tests the ContentDraftingTool directly to see what's happening.
"""

import asyncio
import logging
from src.tools.claim_drafting_tool import ContentDraftingTool

# Set up logging to see all messages
logging.basicConfig(level=logging.INFO)

async def test_content_drafting_tool_direct():
    """Test the ContentDraftingTool directly"""
    print("🧪 TESTING CONTENT DRAFTING TOOL DIRECTLY")
    print("=" * 80)
    
    # Create tool
    tool = ContentDraftingTool()
    
    # Test data
    input_text = "draft 5 system claims for 4g carrier aggregation"
    context = "Patent drafting request for 4G technology"
    conversation_history = [
        {"input": "previous request", "context": "previous context"}
    ]
    document_content = {"text": "Document about 4G technology"}
    
    print(f"📤 Input: {input_text}")
    print(f"📤 Context: {context}")
    print(f"📤 Conversation History: {len(conversation_history)} entries")
    print(f"📤 Document Content: {len(document_content['text'])} characters")
    
    # Test the tool
    events = []
    try:
        async for event in tool.run(
            input_text, 
            {}, 
            conversation_history, 
            document_content
        ):
            events.append(event)
            print(f"📥 Event: {event}")
            
            if event.get('event') == 'thoughts':
                print(f"   💭 {event.get('content', '')}")
            elif event.get('event') == 'results':
                print(f"   ✅ RESULTS: {event.get('content', '')}")
            elif event.get('event') == 'error':
                print(f"   ❌ ERROR: {event.get('error', '')}")
    
    except Exception as e:
        print(f"💥 Tool execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"✅ Tool executed with {len(events)} events")
    
    # Check results
    results_event = next((e for e in events if e.get('event') == 'results'), None)
    if results_event:
        content = results_event.get('content', '')
        print(f"✅ SUCCESS: Results generated")
        print(f"   Content: {content[:200]}...")
    else:
        print(f"❌ FAILURE: No results event generated")
    
    return len(events) > 0

async def main():
    """Main test execution"""
    try:
        print("🔍 CONTENT DRAFTING TOOL DIRECT TEST")
        print("=" * 80)
        print("This test verifies that the ContentDraftingTool")
        print("is working correctly when called directly.")
        print("=" * 80)
        
        # Run the test
        success = await test_content_drafting_tool_direct()
        
        # Final evaluation
        print(f"\n🏆 FINAL EVALUATION:")
        if success:
            print(f"   ✅ SUCCESS: ContentDraftingTool is working")
        else:
            print(f"   ❌ FAILURE: ContentDraftingTool is broken")
            
        return success
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())
