#!/usr/bin/env python3
"""
Simple test for LLM client only - no orchestrator imports.
"""

import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.getcwd(), 'src'))

async def test_llm_client_only():
    """Test only the LLM client without other imports"""
    
    print("🧪 LLM CLIENT ONLY TEST")
    print("=" * 40)
    
    try:
        # Test 1: Import LLM client
        print("📦 Testing LLM client import...")
from src.utils.llm_client import llm_client, send_llm_request_streaming
        print("✅ LLM client imported successfully")
        
        # Test 2: Check configuration
        print("\n📋 Testing configuration...")
        print(f"   Endpoint: {llm_client.endpoint}")
        print(f"   Deployment: {llm_client.deployment_name}")
        print(f"   API Version: {llm_client.api_version}")
        print(f"   API Key: {llm_client.api_key[:8]}...{llm_client.api_key[-4:]}")
        print("✅ Configuration loaded successfully")
        
        # Test 3: Simple LLM request
        print("\n📤 Testing simple LLM request...")
        messages = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Respond with 'Hello, I am working!'"
            },
            {
                "role": "user", 
                "content": "Say hello"
            }
        ]
        
        response_chunks = []
        async for chunk in send_llm_request_streaming(messages, max_tokens=100):
            response_chunks.append(chunk)
            print(f"   📥 Chunk: {chunk}")
            
            # Limit for display
            if len(response_chunks) >= 5:
                print("   ... (showing first 5 chunks)")
                break
        
        if response_chunks:
            print(f"✅ LLM request successful! Received {len(response_chunks)} chunks")
        else:
            print("⚠️  No response chunks received")
            
        print("\n🎯 LLM client test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test execution"""
    await test_llm_client_only()

if __name__ == "__main__":
    asyncio.run(main())
