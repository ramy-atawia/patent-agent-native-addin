#!/usr/bin/env python3
"""
Test for orchestrator only - no legacy dependencies.
"""

import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_orchestrator_only():
    """Test only the orchestrator without other imports"""
    
    print("🧪 ORCHESTRATOR ONLY TEST")
    print("=" * 40)
    
    try:
        # Test 1: Import orchestrator
        print("📦 Testing orchestrator import...")
        from src.agent_core.orchestrator import AgentOrchestrator
        print("✅ Orchestrator imported successfully")
        
        # Test 2: Initialize orchestrator
        print("\n🔧 Testing orchestrator initialization...")
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrator initialized successfully")
        
        # Test 3: Test intent classification
        print("\n🧠 Testing intent classification...")
        test_input = "Draft patent claims for a 5G system"
        test_context = "5G wireless communication system"
        
        print(f"📤 Testing with: {test_input}")
        
        events = []
        async for event in orchestrator.handle(test_input, test_context, "test_session"):
            events.append(event)
            
            event_type = event.get('event', 'unknown')
            if event_type == 'thoughts':
                content = event.get('content', '')[:80]
                thought_type = event.get('thought_type', 'unknown')
                print(f"   📤 {event_type.upper()}: [{thought_type}] {content}...")
            elif event_type == 'error':
                error = event.get('error', '')[:80]
                context = event.get('context', 'unknown')
                print(f"   📤 {event_type.upper()}: [{context}] {error}...")
            else:
                print(f"   📤 {event_type.upper()}: {event}")
            
            # Limit for display
            if len(events) >= 5:
                print("   ... (showing first 5 events)")
                break
        
        print(f"📊 Total events: {len(events)}")
        
        print("\n🎯 Orchestrator test completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test execution"""
    await test_orchestrator_only()

if __name__ == "__main__":
    asyncio.run(main())
