#!/usr/bin/env python3
"""
TEST LLM CLIENT DIRECT
======================

This script tests the LLM client directly to see what's happening
with the responses.
"""

import asyncio
from src.utils.llm_client import send_llm_request_streaming

async def test_llm_client_direct():
    """Test the LLM client directly"""
    print("🧪 TESTING LLM CLIENT DIRECTLY")
    print("=" * 80)
    
    # Simple test messages
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Generate a simple response."
        },
        {
            "role": "user",
            "content": "Say hello and provide a short response."
        }
    ]
    
    print(f"📤 Sending messages to LLM...")
    print(f"System: {messages[0]['content']}")
    print(f"User: {messages[1]['content']}")
    
    # Test the LLM client
    response_content = ""
    function_arguments = ""
    
    try:
        async for chunk in send_llm_request_streaming(messages, functions=None):
            print(f"📥 Received chunk: {chunk}")
            
            if chunk.get("type") == "content_chunk":
                response_content += chunk.get("content", "")
                print(f"   Content chunk: {chunk.get('content', '')}")
            elif chunk.get("type") == "function_call":
                print(f"   Function call: {chunk.get('function_name', 'unknown')}")
            elif chunk.get("type") == "completion":
                function_arguments = chunk.get("function_arguments", "")
                print(f"   Completion: {chunk}")
                break
        
        print(f"\n📊 FINAL RESULTS:")
        print(f"Response content length: {len(response_content)}")
        print(f"Response content: {response_content}")
        print(f"Function arguments: {function_arguments}")
        
        if response_content:
            print(f"✅ SUCCESS: LLM generated content")
        else:
            print(f"❌ FAILURE: LLM generated no content")
            
        return len(response_content) > 0
        
    except Exception as e:
        print(f"💥 LLM client test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test execution"""
    try:
        print("🔍 LLM CLIENT DIRECT TEST")
        print("=" * 80)
        print("This test verifies that the LLM client is working")
        print("and generating responses.")
        print("=" * 80)
        
        # Run the test
        success = await test_llm_client_direct()
        
        # Final evaluation
        print(f"\n🏆 FINAL EVALUATION:")
        if success:
            print(f"   ✅ SUCCESS: LLM client is working")
        else:
            print(f"   ❌ FAILURE: LLM client is not working")
            
        return success
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())
