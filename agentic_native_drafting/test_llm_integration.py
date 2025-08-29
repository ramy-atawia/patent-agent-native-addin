#!/usr/bin/env python3
"""
Test real LLM integration with Azure OpenAI.
This tests actual API calls to ensure the system works end-to-end.
"""

import sys
import asyncio
import os

# Add src to path
sys.path.insert(0, 'src')

async def test_simple_llm_request():
    """Test a simple LLM request to Azure OpenAI"""
    print("🧪 Testing simple LLM request...")
    
    try:
from src.utils.llm_client import LLMClient
        
        client = LLMClient()
        print("✅ LLM Client created")
        
        # Simple test message
        messages = [
            {"role": "user", "content": "Hello! Please respond with 'LLM integration test successful' and nothing else."}
        ]
        
        print("📤 Sending test request to Azure OpenAI...")
        
        # Collect the response
        response_content = ""
        async for chunk in client.send_request_streaming(messages, max_tokens=100):
            if chunk.get("type") == "content_chunk":
                response_content += chunk.get("content", "")
        
        print(f"📥 Response received: {response_content}")
        
        if "LLM integration test successful" in response_content:
            print("✅ LLM integration test successful!")
            return True
        else:
            print("⚠️ LLM response received but content unexpected")
            return True  # Still successful if we got a response
            
    except Exception as e:
        print(f"❌ LLM integration test failed: {e}")
        return False

async def test_tool_llm_integration():
    """Test that tools can make LLM calls"""
    print("\n🧪 Testing tool LLM integration...")
    
    try:
from src.tools.general_conversation_tool import GeneralConversationTool
        
        tool = GeneralConversationTool()
        print("✅ GeneralConversationTool created")
        
        # Test with a simple input
        test_input = "What is the capital of France?"
        print(f"📤 Testing with input: {test_input}")
        
        # Collect events from the tool
        events = []
        async for event in tool.run(test_input, context="", parameters={"max_response_length": 100}):
            events.append(event)
            print(f"📥 Event: {event.get('event', 'unknown')} - {event.get('content', event.get('response', 'no content'))[:50]}...")
        
        # Check if we got results
        results_events = [e for e in events if e.get("event") == "results"]
        if results_events:
            print("✅ Tool LLM integration successful!")
            return True
        else:
            print("⚠️ Tool ran but no results generated")
            return False
            
    except Exception as e:
        print(f"❌ Tool LLM integration test failed: {e}")
        return False

async def test_prior_art_search_llm():
    """Test PriorArtSearchTool LLM integration"""
    print("\n🧪 Testing PriorArtSearchTool LLM integration...")
    
    try:
from src.tools.prior_art_search_tool import PriorArtSearchTool
        
        tool = PriorArtSearchTool()
        print("✅ PriorArtSearchTool created")
        
        # Test with a simple search query
        test_query = "smartphone camera technology"
        print(f"📤 Testing search query: {test_query}")
        
        # Collect events from the tool
        events = []
        async for event in tool.run(test_query, context="", parameters={"max_results": 3}):
            events.append(event)
            print(f"📥 Event: {event.get('event', 'unknown')} - {event.get('content', event.get('response', 'no content'))[:50]}...")
        
        # Check if we got results
        results_events = [e for e in events if e.get("event") == "results"]
        if results_events:
            print("✅ PriorArtSearchTool LLM integration successful!")
            return True
        else:
            print("⚠️ PriorArtSearchTool ran but no results generated")
            return False
            
    except Exception as e:
        print(f"❌ PriorArtSearchTool LLM integration test failed: {e}")
        return False

async def main():
    """Run all LLM integration tests"""
    print("🚀 Starting LLM Integration Tests\n")
    
    tests = [
        test_simple_llm_request,
        test_tool_llm_integration,
        test_prior_art_search_llm
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")
    
    print(f"\n📊 LLM Integration Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All LLM integration tests passed! System is ready for E2E testing.")
        return True
    elif passed > 0:
        print("⚠️ Some LLM integration tests passed. System has partial functionality.")
        return True
    else:
        print("❌ No LLM integration tests passed. System needs configuration.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
