#!/usr/bin/env python3
"""
Simple test script for streaming LLM thoughts across different user inputs.

This script tests the streaming response format and thought generation
for various user scenarios.
"""

import asyncio
import sys
import os
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_streaming_thoughts():
    """Test streaming thoughts for different user inputs"""
    
    print("🧪 STREAMING THOUGHTS TEST")
    print("=" * 50)
    
    try:
        from src.agent_core.orchestrator import AgentOrchestrator
        
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrator initialized successfully")
        
        # Test scenarios
        test_cases = [
            {
                "name": "Claim Drafting",
                "input": "Draft patent claims for a 5G AI system",
                "description": "Should generate thoughts and results"
            },
            {
                "name": "Prior Art Search", 
                "input": "Search for prior art on AI carrier aggregation",
                "description": "Should generate thoughts and results"
            },
            {
                "name": "Missing Tool (Invention Analysis)",
                "input": "Analyze my invention for technical feasibility",
                "description": "Should generate graceful error message"
            },
            {
                "name": "General Conversation",
                "input": "What is a patent?",
                "description": "Should generate thoughts and results"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: {test_case['name']}")
            print(f"   Input: {test_case['input']}")
            print(f"   Expected: {test_case['description']}")
            print("   " + "-" * 40)
            
            # Execute the test case
            events = []
            try:
                async for event in orchestrator.handle(
                    test_case['input'], 
                    "Test context", 
                    f"test_session_{i}"
                ):
                    events.append(event)
                    
                    # Print the event
                    event_type = event.get('event', 'unknown')
                    if event_type == 'thoughts':
                        content = event.get('content', '')[:80]
                        thought_type = event.get('thought_type', 'unknown')
                        print(f"   📤 {event_type.upper()}: [{thought_type}] {content}...")
                    elif event_type == 'results':
                        response = event.get('response', '')[:80]
                        print(f"   📤 {event_type.upper()}: {response}...")
                    elif event_type == 'error':
                        error = event.get('error', '')[:80]
                        context = event.get('context', 'unknown')
                        print(f"   📤 {event_type.upper()}: [{context}] {error}...")
                    else:
                        print(f"   📤 {event_type.upper()}: {event}")
                    
                    # Limit events for display
                    if len(events) >= 8:
                        print(f"   ... (showing first 8 events)")
                        break
                
                # Summary
                event_types = [e.get('event', 'unknown') for e in events]
                thought_count = event_types.count('thoughts')
                result_count = event_types.count('results')
                error_count = event_types.count('error')
                
                print(f"   📊 Events: {thought_count} thoughts, {result_count} results, {error_count} errors")
                
                if error_count > 0 and 'graceful' in test_case['description'].lower():
                    print("   ✅ PASSED: Graceful error handling working")
                elif result_count > 0 and 'thoughts and results' in test_case['description'].lower():
                    print("   ✅ PASSED: Thoughts and results generated")
                else:
                    print("   ⚠️  UNEXPECTED: Check the response pattern")
                    
            except Exception as e:
                print(f"   ❌ ERROR: {e}")
            
            print()
        
        print("🎯 Streaming thoughts test completed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_specific_tool_streaming():
    """Test streaming for a specific tool in detail"""
    
    print("\n🔍 DETAILED TOOL STREAMING TEST")
    print("=" * 50)
    
    try:
        from src.agent_core.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        
        # Test a specific tool
        test_input = "Draft 3 patent claims for a machine learning algorithm that optimizes database queries"
        test_context = "The algorithm uses neural networks to predict query execution time and optimize database performance."
        
        print(f"🧪 Testing: {test_input}")
        print(f"   Context: {test_context}")
        print("   " + "-" * 50)
        
        events = []
        async for event in orchestrator.handle(test_input, test_context, "detailed_test_session"):
            events.append(event)
            
            # Detailed event analysis
            event_type = event.get('event', 'unknown')
            timestamp = event.get('timestamp', '')
            metadata = event.get('metadata', {})
            
            print(f"📤 Event {len(events)}: {event_type.upper()}")
            print(f"   Timestamp: {timestamp}")
            
            if event_type == 'thoughts':
                content = event.get('content', '')
                thought_type = event.get('thought_type', 'unknown')
                print(f"   Type: {thought_type}")
                print(f"   Content: {content}")
                
                if metadata:
                    print(f"   Metadata: {metadata}")
                    
            elif event_type == 'results':
                response = event.get('response', '')
                data = event.get('data', {})
                print(f"   Response: {response}")
                
                if data:
                    print(f"   Data keys: {list(data.keys())}")
                    
            elif event_type == 'error':
                error = event.get('error', '')
                context = event.get('context', 'unknown')
                print(f"   Context: {context}")
                print(f"   Error: {error}")
            
            print()
            
            # Limit for display
            if len(events) >= 10:
                print("   ... (showing first 10 events)")
                break
        
        # Analysis
        print("📊 STREAMING ANALYSIS:")
        event_types = [e.get('event', 'unknown') for e in events]
        thought_types = [e.get('thought_type', '') for e in events if e.get('event') == 'thoughts']
        
        print(f"   Total events: {len(events)}")
        print(f"   Event distribution: {dict(zip(set(event_types), [event_types.count(t) for t in set(event_types)]))}")
        print(f"   Thought progression: {thought_types}")
        
        # Validate streaming format
        print("\n🔍 VALIDATION:")
        
        # Check timestamps
        timestamps = [e.get('timestamp') for e in events if e.get('timestamp')]
        if timestamps:
            try:
                [datetime.fromisoformat(ts.replace('Z', '+00:00')) for ts in timestamps]
                print("   ✅ Timestamps: Valid ISO format")
            except:
                print("   ❌ Timestamps: Invalid format")
        else:
            print("   ⚠️  Timestamps: Missing")
        
        # Check metadata
        metadata_count = sum(1 for e in events if e.get('metadata'))
        print(f"   📋 Metadata: {metadata_count}/{len(events)} events have metadata")
        
        # Check content quality
        thought_events = [e for e in events if e.get('event') == 'thoughts']
        content_lengths = [len(e.get('content', '')) for e in thought_events]
        if content_lengths:
            avg_length = sum(content_lengths) / len(content_lengths)
            print(f"   📝 Content: Average thought length: {avg_length:.1f} characters")
        
        print("\n🎯 Detailed test completed!")
        
    except Exception as e:
        print(f"❌ Detailed test failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test execution"""
    await test_streaming_thoughts()
    await test_specific_tool_streaming()

if __name__ == "__main__":
    asyncio.run(main())
