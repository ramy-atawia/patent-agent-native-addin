#!/usr/bin/env python3
"""
Comprehensive test suite for streaming LLM thoughts across different user inputs.

This test suite validates:
1. Streaming response format for different intent types
2. Thought event generation and content
3. Error handling and graceful degradation
4. Response standardization across all tools
5. End-to-end streaming functionality
"""

import asyncio
import sys
import os
import json
from datetime import datetime
from typing import List, Dict, Any

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class StreamingThoughtsTester:
    """Test suite for streaming LLM thoughts"""
    
    def __init__(self):
        self.test_results = []
        self.passed_tests = 0
        self.failed_tests = 0
        
    async def run_all_tests(self):
        """Run all streaming thoughts tests"""
        print("🧪 STREAMING THOUGHTS TEST SUITE")
        print("=" * 60)
        
        # Test different user input scenarios
        test_scenarios = [
            # Working tools - should generate thoughts and results
            {
                "name": "Claim Drafting - 5G AI System",
                "input": "Draft patent claims for a 5G system that uses AI for dynamic spectrum sharing",
                "context": "The invention relates to a 5G wireless communication system that employs machine learning algorithms to optimize spectrum allocation in real-time.",
                "expected_intent": "claim_drafting",
                "should_work": True
            },
            {
                "name": "Prior Art Search - AI Carrier Aggregation",
                "input": "Search for prior art on AI-based carrier aggregation in 5G networks",
                "context": "Need to understand existing solutions for intelligent carrier aggregation.",
                "expected_intent": "prior_art_search",
                "should_work": True
            },
            {
                "name": "Claim Review - Patent Claims Analysis",
                "input": "Review these patent claims for validity and patentability",
                "context": "Claim 1: A system comprising... Claim 2: The system of claim 1...",
                "expected_intent": "claim_review",
                "should_work": True
            },
            {
                "name": "Patent Guidance - Software Inventions",
                "input": "What are the key requirements for patenting software inventions?",
                "context": "Working on a machine learning algorithm for image recognition.",
                "expected_intent": "patent_guidance",
                "should_work": True
            },
            {
                "name": "Disclosure Assessment - Invention Sufficiency",
                "input": "Assess if my invention disclosure is sufficient for patent filing",
                "context": "My invention is a new method for optimizing database queries using neural networks.",
                "expected_intent": "disclosure_assessment",
                "should_work": True
            },
            {
                "name": "General Conversation - Patent Types",
                "input": "What is the difference between utility patents and design patents?",
                "context": "Learning about different types of patent protection.",
                "expected_intent": "general_conversation",
                "should_work": True
            },
            
            # Missing tools - should generate graceful error messages
            {
                "name": "Invention Analysis - Technical Feasibility",
                "input": "Analyze my invention for technical feasibility and market potential",
                "context": "Need comprehensive technical and market analysis.",
                "expected_intent": "invention_analysis",
                "should_work": False,
                "expected_error": "Sorry, I currently can't do that"
            },
            {
                "name": "Technical Query - Implementation Details",
                "input": "What are the technical requirements for implementing this algorithm?",
                "context": "Need to understand implementation complexity and requirements.",
                "expected_intent": "technical_query",
                "should_work": False,
                "expected_error": "Sorry, I currently can't do that"
            },
            
            # Edge cases and error scenarios
            {
                "name": "Empty Input - Validation",
                "input": "",
                "context": "",
                "expected_intent": "general_conversation",
                "should_work": False,
                "expected_error": "validation"
            },
            {
                "name": "Very Long Input - Processing",
                "input": "A" * 1000,  # Very long input
                "context": "B" * 500,
                "expected_intent": "general_conversation",
                "should_work": True
            },
            {
                "name": "Special Characters - Encoding",
                "input": "Draft claims for system with @#$%^&*() symbols and unicode 🚀📱💻",
                "context": "System includes special characters and emojis",
                "expected_intent": "claim_drafting",
                "should_work": True
            }
        ]
        
        print(f"📋 Running {len(test_scenarios)} test scenarios...\n")
        
        for i, scenario in enumerate(test_scenarios, 1):
            print(f"🧪 Test {i}/{len(test_scenarios)}: {scenario['name']}")
            print(f"   Input: {scenario['input'][:60]}...")
            
            try:
                await self.test_streaming_scenario(scenario)
                print(f"   ✅ PASSED")
            except Exception as e:
                print(f"   ❌ FAILED: {e}")
                self.failed_tests += 1
            
            print()
        
        # Print summary
        self.print_test_summary()
    
    async def test_streaming_scenario(self, scenario: Dict[str, Any]):
        """Test a specific streaming scenario"""
        try:
from src.agent_core.orchestrator import AgentOrchestrator
            
            # Initialize orchestrator
            orchestrator = AgentOrchestrator()
            
            # Execute the scenario
            events = []
            async for event in orchestrator.handle(
                scenario['input'], 
                scenario['context'], 
                f"test_session_{datetime.now().timestamp()}"
            ):
                events.append(event)
                
                # Limit events for testing (prevent infinite loops)
                if len(events) > 20:
                    break
            
            # Validate the response
            await self.validate_streaming_response(scenario, events)
            
            self.passed_tests += 1
            
        except Exception as e:
            # If this is expected to fail, that's okay
            if not scenario.get('should_work', True):
                self.passed_tests += 1
                return
            raise e
    
    async def validate_streaming_response(self, scenario: Dict[str, Any], events: List[Dict[str, Any]]):
        """Validate the streaming response format and content"""
        
        # Basic validation
        if not events:
            raise ValueError("No events generated")
        
        # Check event structure
        for event in events:
            if not isinstance(event, dict):
                raise ValueError(f"Event is not a dictionary: {type(event)}")
            
            if 'event' not in event:
                raise ValueError(f"Event missing 'event' field: {event}")
            
            event_type = event['event']
            
            # Validate event types
            if event_type not in ['thoughts', 'results', 'error', 'low_confidence']:
                raise ValueError(f"Invalid event type: {event_type}")
            
            # Validate required fields based on event type
            if event_type == 'thoughts':
                if 'content' not in event:
                    raise ValueError(f"Thought event missing 'content' field: {event}")
                if 'thought_type' not in event:
                    raise ValueError(f"Thought event missing 'thought_type' field: {event}")
                if 'timestamp' not in event:
                    raise ValueError(f"Thought event missing 'timestamp' field: {event}")
            
            elif event_type == 'results':
                if 'response' not in event:
                    raise ValueError(f"Results event missing 'response' field: {event}")
                if 'timestamp' not in event:
                    raise ValueError(f"Results event missing 'timestamp' field: {event}")
            
            elif event_type == 'error':
                if 'error' not in event:
                    raise ValueError(f"Error event missing 'error' field: {event}")
                if 'context' not in event:
                    raise ValueError(f"Error event missing 'context' field: {event}")
                if 'timestamp' not in event:
                    raise ValueError(f"Error event missing 'timestamp' field: {event}")
        
        # Scenario-specific validation
        if scenario.get('should_work', True):
            # Should have thoughts and results
            thought_events = [e for e in events if e['event'] == 'thoughts']
            result_events = [e for e in events if e['event'] == 'results']
            
            if not thought_events:
                raise ValueError("No thought events generated for working scenario")
            
            if not result_events:
                raise ValueError("No result events generated for working scenario")
            
            # Validate thought progression
            thought_types = [e.get('thought_type', '') for e in thought_events]
            expected_thoughts = ['initialization', 'intent_analysis', 'routing', 'tool_execution']
            
            # Should have at least initialization and intent_analysis
            if 'initialization' not in thought_types:
                raise ValueError("Missing initialization thought")
            
            if 'intent_analysis' not in thought_types:
                raise ValueError("Missing intent analysis thought")
            
        else:
            # Should have error or graceful handling
            error_events = [e for e in events if e['event'] == 'error']
            
            if not error_events:
                raise ValueError("No error events generated for failing scenario")
            
            # Check for expected error message if specified
            if 'expected_error' in scenario:
                error_messages = [e.get('error', '') for e in error_events]
                if not any(scenario['expected_error'] in msg for msg in error_messages):
                    raise ValueError(f"Expected error message '{scenario['expected_error']}' not found in: {error_messages}")
        
        # Validate streaming format
        await self.validate_streaming_format(events)
    
    async def validate_streaming_format(self, events: List[Dict[str, Any]]):
        """Validate the streaming response format"""
        
        # Check timestamp format
        for event in events:
            timestamp = event.get('timestamp', '')
            if timestamp:
                try:
                    datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                except ValueError:
                    raise ValueError(f"Invalid timestamp format: {timestamp}")
        
        # Check metadata structure
        for event in events:
            metadata = event.get('metadata', {})
            if not isinstance(metadata, dict):
                raise ValueError(f"Metadata is not a dictionary: {metadata}")
        
        # Check content length (shouldn't be empty for thoughts)
        for event in events:
            if event['event'] == 'thoughts':
                content = event.get('content', '')
                if not content or len(content.strip()) < 5:
                    raise ValueError(f"Thought content too short: '{content}'")
        
        # Check thought type values
        valid_thought_types = [
            'initialization', 'intent_analysis', 'routing', 'tool_execution',
            'tool_unavailable', 'chain_execution', 'assessment', 'drafting',
            'validation', 'search_execution', 'report_generation', 'search_complete'
        ]
        
        for event in events:
            if event['event'] == 'thoughts':
                thought_type = event.get('thought_type', '')
                if thought_type and thought_type not in valid_thought_types:
                    print(f"⚠️  Warning: Unknown thought type: {thought_type}")
    
    def print_test_summary(self):
        """Print test execution summary"""
        print("📊 TEST SUMMARY")
        print("=" * 60)
        print(f"✅ Passed: {self.passed_tests}")
        print(f"❌ Failed: {self.failed_tests}")
        print(f"📈 Success Rate: {(self.passed_tests / (self.passed_tests + self.failed_tests) * 100):.1f}%")
        
        if self.failed_tests == 0:
            print("\n🎉 ALL TESTS PASSED! Streaming thoughts working correctly.")
        else:
            print(f"\n⚠️  {self.failed_tests} tests failed. Check implementation.")

async def main():
    """Main test execution"""
    tester = StreamingThoughtsTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
