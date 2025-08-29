#!/usr/bin/env python3
"""
Test session memory and conversation history functionality.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_session_memory():
    """Test that session memory is working correctly"""
    try:
        from src.agent_core.orchestrator import AgentOrchestrator
        
        print('🧪 SESSION MEMORY TEST')
        print('=' * 50)
        
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        print('✅ Orchestrator initialized')
        
        # Test session 1
        session1 = "test_session_1"
        print(f'\n📝 Testing session: {session1}')
        
        # First message
        events1 = []
        async for event in orchestrator.handle("Hello, I need help with patent drafting", "Patent context", session1):
            events1.append(event)
            if len(events1) >= 3:  # Just get first few events
                break
        
        print(f'   📤 First message events: {len(events1)}')
        
        # Check memory
        memory1 = orchestrator.conversation_memory.get(session1, {})
        print(f'   💾 Memory after first message: {len(memory1.get("messages", []))} messages')
        
        # Second message in same session
        events2 = []
        async for event in orchestrator.handle("Can you explain what a patent claim is?", "Patent context", session1):
            events2.append(event)
            if len(events2) >= 3:  # Just get first few events
                break
        
        print(f'   📤 Second message events: {len(events2)}')
        
        # Check memory again
        memory2 = orchestrator.conversation_memory.get(session1, {})
        print(f'   💾 Memory after second message: {len(memory2.get("messages", []))} messages')
        
        # Test session 2 (different session)
        session2 = "test_session_2"
        print(f'\n📝 Testing different session: {session2}')
        
        events3 = []
        async for event in orchestrator.handle("What is machine learning?", "ML context", session2):
            events3.append(event)
            if len(events3) >= 3:  # Just get first few events
                break
        
        print(f'   📤 New session events: {len(events3)}')
        
        # Check both sessions
        memory1_final = orchestrator.conversation_memory.get(session1, {})
        memory2_final = orchestrator.conversation_memory.get(session2, {})
        
        print(f'   💾 Session 1 memory: {len(memory1_final.get("messages", []))} messages')
        print(f'   💾 Session 2 memory: {len(memory2_final.get("messages", []))} messages')
        
        # Test memory clearing
        print(f'\n🧹 Testing memory clearing...')
        orchestrator.clear_memory()
        
        memory_after_clear = orchestrator.conversation_memory
        print(f'   💾 Memory after clearing: {len(memory_after_clear)} sessions')
        
        print('\n🎯 Session memory test completed!')
        
    except Exception as e:
        print(f'❌ Test failed: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_session_memory())
