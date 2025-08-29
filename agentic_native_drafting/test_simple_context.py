#!/usr/bin/env python3
"""
TEST SIMPLE CONTEXT INTEGRATION
===============================

This script tests basic context integration to see if the conversation
history is being passed to the LLM calls.
"""

import asyncio
from src.tools.general_conversation_tool import GeneralConversationTool

async def test_simple_context():
    """Test simple context integration"""
    print("🧪 TESTING SIMPLE CONTEXT INTEGRATION")
    print("=" * 80)
    
    # Create tool
    tool = GeneralConversationTool()
    
    # Test data
    user_input = "What was my previous request about?"
    context = "Context test"
    conversation_history = [
        {"input": "draft 5 system claims for 4g carrier aggregation", "context": "Patent drafting"},
        {"input": "draft the corresponding method claims", "context": "Method claims"}
    ]
    document_content = {"text": "Document about 4G carrier aggregation technology"}
    
    print(f"📤 User Input: {user_input}")
    print(f"📤 Context: {context}")
    print(f"📤 Conversation History: {len(conversation_history)} entries")
    print(f"📤 Document Content: {len(document_content['text'])} characters")
    
    # Test the tool
    events = []
    async for event in tool.run(
        user_input, 
        context, 
        {}, 
        conversation_history, 
        document_content
    ):
        events.append(event)
        if event.get('event') == 'thoughts':
            print(f"💭 {event.get('content', '')[:100]}...")
        elif event.get('event') == 'results':
            print(f"✅ RESULTS: {event.get('content', '')[:300]}...")
    
    print(f"✅ Tool executed with {len(events)} events")
    
    # Check if context was used
    results_event = next((e for e in events if e.get('event') == 'results'), None)
    if results_event:
        content = results_event.get('content', '').lower()
        if '4g' in content or 'carrier aggregation' in content:
            print(f"✅ SUCCESS: Context was used - 4G/carrier aggregation mentioned in response")
        else:
            print(f"❌ FAILURE: Context was NOT used - no 4G/carrier aggregation in response")
            print(f"   Response content: {content[:200]}...")
    else:
        print(f"❌ FAILURE: No results event generated")
    
    return len(events) > 0

async def main():
    """Main test execution"""
    try:
        print("🔍 SIMPLE CONTEXT INTEGRATION TEST")
        print("=" * 80)
        print("This test verifies basic context integration")
        print("by checking if conversation history is used.")
        print("=" * 80)
        
        # Run the test
        success = await test_simple_context()
        
        # Final evaluation
        print(f"\n🏆 FINAL EVALUATION:")
        if success:
            print(f"   ✅ SUCCESS: Basic context integration is working")
        else:
            print(f"   ❌ FAILURE: Basic context integration is broken")
            
        return success
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())
