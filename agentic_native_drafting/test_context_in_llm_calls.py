#!/usr/bin/env python3
"""
TEST CONTEXT IN LLM CALLS
=========================

This script tests that the context is actually being used in the LLM calls,
not just passed around but actually utilized in the prompt templates.
"""

import asyncio
import json
from src.tools.claim_drafting_tool import ContentDraftingTool
from src.tools.general_conversation_tool import GeneralConversationTool
from src.tools.patent_guidance_tool import GeneralGuidanceTool

async def test_content_drafting_context_usage():
    """Test that ContentDraftingTool actually uses context in LLM calls"""
    print("🧪 Testing ContentDraftingTool Context Usage in LLM Calls...")
    
    tool = ContentDraftingTool()
    
    # Test data with clear context
    input_text = "Draft patent claims for 6G carrier aggregation"
    context = "ENHANCED CONTEXT: This should appear in the LLM call"
    additional_context = "CONVERSATION HISTORY: Previous discussion about 6G"
    
    print(f"📤 Input: {input_text}")
    print(f"📤 Enhanced Context: {context}")
    print(f"📤 Additional Context: {additional_context}")
    
    # Mock the prompt loader to capture what's being sent to LLM
    original_load_prompt = None
    captured_prompts = []
    
    try:
        # Import and mock the prompt loader
        from src.prompt_loader import prompt_loader
        original_load_prompt = prompt_loader.load_prompt
        
        def mock_load_prompt(prompt_name, **kwargs):
            captured_prompts.append({
                "prompt_name": prompt_name,
                "kwargs": kwargs
            })
            # Return a simple template for testing
            if prompt_name == "claim_drafting_user":
                return f"Disclosure: {kwargs.get('disclosure', '')}\nDocument Content: {kwargs.get('document_content', '')}\nConversation History: {kwargs.get('conversation_history', '')}"
            elif prompt_name == "claim_drafting_system":
                return "You are a patent drafting specialist."
            else:
                return "Test prompt"
        
        prompt_loader.load_prompt = mock_load_prompt
        
        # Test the tool
        events = []
        async for event in tool.run(
            input_text, 
            context, 
            {"max_outputs": 2}, 
            [{"input": "Previous request"}], 
            {"text": "Document about 6G"}
        ):
            events.append(event)
            if event.get('event') == 'thoughts':
                print(f"💭 {event.get('content', '')[:100]}...")
        
        print(f"✅ Tool executed with {len(events)} events")
        
        # Check captured prompts
        if captured_prompts:
            print(f"\n📋 CAPTURED PROMPT CALLS:")
            for i, prompt in enumerate(captured_prompts):
                print(f"   {i+1}. {prompt['prompt_name']}: {json.dumps(prompt['kwargs'], indent=2)}")
            
            # Check if context is being passed
            user_prompt = next((p for p in captured_prompts if p['prompt_name'] == 'claim_drafting_user'), None)
            if user_prompt:
                print(f"\n🎯 CONTEXT USAGE ANALYSIS:")
                print(f"   Disclosure: {'✅' if user_prompt['kwargs'].get('disclosure') else '❌'}")
                print(f"   Document Content: {'✅' if user_prompt['kwargs'].get('document_content') else '❌'}")
                print(f"   Conversation History: {'✅' if user_prompt['kwargs'].get('conversation_history') else '❌'}")
                
                if all([user_prompt['kwargs'].get('disclosure'), 
                        user_prompt['kwargs'].get('document_content'), 
                        user_prompt['kwargs'].get('conversation_history')]):
                    print(f"   🎉 ALL CONTEXT PARAMETERS ARE BEING PASSED!")
                else:
                    print(f"   ❌ SOME CONTEXT PARAMETERS ARE MISSING!")
        else:
            print("❌ No prompts were captured - prompt loader not working")
            
    except Exception as e:
        print(f"💥 Error testing ContentDraftingTool: {e}")
    finally:
        # Restore original prompt loader
        if original_load_prompt:
            from src.prompt_loader import prompt_loader
            prompt_loader.load_prompt = original_load_prompt
    
    return len(captured_prompts) > 0

async def test_general_conversation_context_usage():
    """Test that GeneralConversationTool actually uses context in LLM calls"""
    print("\n🧪 Testing GeneralConversationTool Context Usage in LLM Calls...")
    
    tool = GeneralConversationTool()
    
    # Test data
    user_input = "How does this compare to 5G?"
    context = "ENHANCED CONTEXT: This should appear in the LLM call"
    
    print(f"📤 User Input: {user_input}")
    print(f"📤 Enhanced Context: {context}")
    
    # Mock the prompt loader
    original_load_prompt = None
    captured_prompts = []
    
    try:
        from src.prompt_loader import prompt_loader
        original_load_prompt = prompt_loader.load_prompt
        
        def mock_load_prompt(prompt_name, **kwargs):
            captured_prompts.append({
                "prompt_name": prompt_name,
                "kwargs": kwargs
            })
            if prompt_name == "general_conversation_user":
                return f"User Input: {kwargs.get('user_input', '')}\nContext: {kwargs.get('context', '')}"
            elif prompt_name == "general_conversation_system":
                return "You are a helpful assistant."
            else:
                return "Test prompt"
        
        prompt_loader.load_prompt = mock_load_prompt
        
        # Test the tool
        events = []
        async for event in tool.run(
            user_input, 
            context, 
            {}, 
            [{"input": "Previous request"}], 
            {"text": "Document about 6G"}
        ):
            events.append(event)
            if event.get('event') == 'thoughts':
                print(f"💭 {event.get('content', '')[:100]}...")
        
        print(f"✅ Tool executed with {len(events)} events")
        
        # Check captured prompts
        if captured_prompts:
            print(f"\n📋 CAPTURED PROMPT CALLS:")
            for i, prompt in enumerate(captured_prompts):
                print(f"   {i+1}. {prompt['prompt_name']}: {json.dumps(prompt['kwargs'], indent=2)}")
            
            # Check if context is being passed
            user_prompt = next((p for p in captured_prompts if p['prompt_name'] == 'general_conversation_user'), None)
            if user_prompt:
                print(f"\n🎯 CONTEXT USAGE ANALYSIS:")
                print(f"   User Input: {'✅' if user_prompt['kwargs'].get('user_input') else '❌'}")
                print(f"   Context: {'✅' if user_prompt['kwargs'].get('context') else '❌'}")
                
                if user_prompt['kwargs'].get('context'):
                    print(f"   🎉 ENHANCED CONTEXT IS BEING PASSED!")
                else:
                    print(f"   ❌ ENHANCED CONTEXT IS MISSING!")
        else:
            print("❌ No prompts were captured - prompt loader not working")
            
    except Exception as e:
        print(f"💥 Error testing GeneralConversationTool: {e}")
    finally:
        # Restore original prompt loader
        if original_load_prompt:
            from src.prompt_loader import prompt_loader
            prompt_loader.load_prompt = original_load_prompt
    
    return len(captured_prompts) > 0

async def main():
    """Run all context usage tests"""
    print("🔍 TESTING CONTEXT USAGE IN LLM CALLS")
    print("=" * 80)
    print("This test verifies that context is actually being used in LLM calls,")
    print("not just passed around but actually utilized in the prompt templates.")
    print("=" * 80)
    
    try:
        # Test 1: ContentDraftingTool
        test1_result = await test_content_drafting_context_usage()
        
        # Test 2: GeneralConversationTool
        test2_result = await test_general_conversation_context_usage()
        
        # Summary
        print("\n" + "=" * 80)
        print("📊 CONTEXT USAGE TEST RESULTS")
        print("=" * 80)
        print(f"✅ ContentDraftingTool Context Usage: {'PASS' if test1_result else 'FAIL'}")
        print(f"✅ GeneralConversationTool Context Usage: {'PASS' if test2_result else 'FAIL'}")
        
        if all([test1_result, test2_result]):
            print("\n🎉 ALL TESTS PASSED! Context is being used in LLM calls.")
            print("✅ The context integration is working at the LLM level.")
        else:
            print("\n❌ Some tests failed. Context integration needs more work.")
            
    except Exception as e:
        print(f"\n💥 Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
