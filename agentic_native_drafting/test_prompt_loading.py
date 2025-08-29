#!/usr/bin/env python3
"""
TEST PROMPT LOADING
===================

This script tests if the prompt loading is working correctly.
"""

import asyncio
from src import prompt_loader

async def test_prompt_loading():
    """Test prompt loading"""
    print("🧪 TESTING PROMPT LOADING")
    print("=" * 80)
    
    try:
        # Test system prompt
        print("📤 Testing claim_drafting_system prompt...")
        system_prompt = prompt_loader.load_prompt("claim_drafting_system")
        print(f"✅ System prompt loaded: {system_prompt[:100]}...")
        
        # Test user prompt
        print("📤 Testing claim_drafting_user prompt...")
        user_prompt = prompt_loader.load_prompt(
            "claim_drafting_user",
            disclosure="test disclosure",
            document_content="test document",
            conversation_history="test history"
        )
        print(f"✅ User prompt loaded: {user_prompt[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"💥 Prompt loading failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test execution"""
    try:
        print("🔍 PROMPT LOADING TEST")
        print("=" * 80)
        print("This test verifies that prompt loading is working")
        print("correctly.")
        print("=" * 80)
        
        # Run the test
        success = await test_prompt_loading()
        
        # Final evaluation
        print(f"\n🏆 FINAL EVALUATION:")
        if success:
            print(f"   ✅ SUCCESS: Prompt loading is working")
        else:
            print(f"   ❌ FAILURE: Prompt loading is broken")
            
        return success
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(main())
