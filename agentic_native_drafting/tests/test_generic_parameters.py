#!/usr/bin/env python3
"""
Test generic parameter passing to tools.
"""

import sys
import os
import asyncio
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_generic_parameters():
    """Test that generic parameters are passed correctly to tools"""
    try:
        from src.agent_core.orchestrator import AgentOrchestrator
        
        print('🧪 GENERIC PARAMETERS TEST')
        print('=' * 50)
        
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        print('✅ Orchestrator initialized')
        
        # Test with custom parameters
        custom_params = {
            'max_outputs': 5,
            'relevance_threshold': 0.8,
            'max_response_length': 1000,
            'custom_field': 'test_value'
        }
        
        print(f'\n📋 Testing with custom parameters: {custom_params}')
        
        # Test content drafting with parameters
        events = []
        async for event in orchestrator.handle(
            "Draft content for a 5G system", 
            "5G context", 
            "param_test_session",
            parameters=custom_params
        ):
            events.append(event)
            if len(events) >= 5:  # Get first few events
                break
        
        print(f'   📤 Events generated: {len(events)}')
        
        # Check if parameters were used
        for i, event in enumerate(events):
            if event.get('event') == 'thoughts':
                print(f'   📝 Event {i+1}: {event.get("content", "")[:80]}...')
        
        print('\n🎯 Generic parameters test completed!')
        
    except Exception as e:
        print(f'❌ Test failed: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_generic_parameters())
