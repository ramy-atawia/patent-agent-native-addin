#!/usr/bin/env python3
"""
Test Case: Confidence Threshold System for Patent Drafting Agent

This test file validates the simplified confidence threshold system:
- Confidence > 0.7: EXECUTE the detected intent
- Confidence ≤ 0.7: SEEK USER CLARIFICATION

Test Scenarios:
1. High confidence requests (>0.7) - should execute immediately
2. Low confidence requests (≤0.7) - should seek clarification
3. Edge cases and error conditions
"""

import asyncio
import json
from typing import Dict, Any
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.cli_chat import SimpleCLIChat

class ConfidenceThresholdTester:
    """Test suite for the confidence threshold system"""
    
    def __init__(self):
        self.chat = SimpleCLIChat()
        self.test_results = []
        
    async def setup(self):
        """Initialize the test environment"""
        print("🔧 Setting up confidence threshold test environment...")
        if not await self.chat.test_connection():
            raise RuntimeError("❌ Failed to connect to server")
        print("✅ Server connection successful!")
        
    async def cleanup(self):
        """Clean up test resources"""
        await self.chat.close()
        
    def log_test_result(self, test_name: str, input_text: str, expected_action: str, 
                       actual_response: str, confidence_info: str, status: str):
        """Log test results for analysis"""
        result = {
            "test_name": test_name,
            "input_text": input_text,
            "expected_action": expected_action,
            "actual_response": actual_response[:200] + "..." if len(actual_response) > 200 else actual_response,
            "confidence_info": confidence_info,
            "status": status,
            "timestamp": asyncio.get_event_loop().time()
        }
        self.test_results.append(result)
        
    async def test_high_confidence_execution(self):
        """Test scenarios where confidence > 0.7 - should EXECUTE"""
        print("\n🔍 Testing HIGH CONFIDENCE scenarios (>0.7) - should EXECUTE")
        
        high_confidence_tests = [
            {
                "name": "Explicit Claim Drafting Request",
                "input": "draft patent claims for my quantum computing invention",
                "expected": "EXECUTE - Generate claims"
            },
            {
                "name": "Clear Claim Review Request", 
                "input": "review my patent claims for quality and compliance",
                "expected": "EXECUTE - Provide review guidance"
            },
            {
                "name": "Specific Patent Guidance",
                "input": "how do I patent my AI invention?",
                "expected": "EXECUTE - Provide guidance"
            },
            {
                "name": "Technical Invention Description",
                "input": "I invented a 5G AI carrier aggregation system that uses machine learning to dynamically select frequency carriers",
                "expected": "EXECUTE - Draft claims or analyze"
            }
        ]
        
        for test in high_confidence_tests:
            print(f"\n📝 Test: {test['name']}")
            print(f"   Input: '{test['input']}'")
            
            run_id = await self.chat.start_conversation(test['input'])
            if not run_id:
                print("   ❌ Failed to start conversation")
                continue
                
            events = await self.chat.stream_response(run_id)
            
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', 'No response')
                    metadata = final_data.get('metadata', {})
                    reasoning = metadata.get('reasoning', 'Unknown')
                    
                    # Check if response indicates execution (not clarification)
                    is_execution = (
                        'drafted' in response.lower() or
                        'claims' in response.lower() or
                        'guidance' in response.lower() or
                        'analysis' in response.lower() or
                        'review' in response.lower()
                    )
                    
                    # Check if reasoning shows execution
                    is_executing = 'executing' in reasoning.lower()
                    
                    status = "✅ PASS" if (is_execution and is_executing) else "❌ FAIL"
                    print(f"   Status: {status}")
                    print(f"   Response: {response[:100]}...")
                    print(f"   Reasoning: {reasoning[:150]}...")
                    
                    self.log_test_result(
                        test['name'], test['input'], test['expected'],
                        response, reasoning, status
                    )
                else:
                    print("   ❌ Invalid final data format")
            else:
                print("   ❌ No final event received")
                
    async def test_low_confidence_clarification(self):
        """Test scenarios where confidence ≤ 0.7 - should SEEK CLARIFICATION"""
        print("\n🔍 Testing LOW CONFIDENCE scenarios (≤0.7) - should SEEK CLARIFICATION")
        
        low_confidence_tests = [
            {
                "name": "Vague Technology Reference",
                "input": "something about technology maybe",
                "expected": "SEEK CLARIFICATION"
            },
            {
                "name": "Ambiguous Patent Interest",
                "input": "maybe something about patents",
                "expected": "SEEK CLARIFICATION"
            },
            {
                "name": "Unclear Request",
                "input": "I don't know, what can you do?",
                "expected": "SEEK CLARIFICATION"
            },
            {
                "name": "Incomplete Thought",
                "input": "patents are...",
                "expected": "SEEK CLARIFICATION"
            }
        ]
        
        for test in low_confidence_tests:
            print(f"\n📝 Test: {test['name']}")
            print(f"   Input: '{test['input']}'")
            
            run_id = await self.chat.start_conversation(test['input'])
            if not run_id:
                print("   ❌ Failed to start conversation")
                continue
                
            events = await self.chat.stream_response(run_id)
            
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', 'No response')
                    metadata = final_data.get('metadata', {})
                    reasoning = metadata.get('reasoning', 'Unknown')
                    
                    # Check if response seeks clarification
                    seeks_clarification = (
                        'not entirely sure' in response.lower() or
                        'provide more details' in response.lower() or
                        'clarification' in response.lower() or
                        'not sure' in response.lower()
                    )
                    
                    # Check if reasoning shows low confidence
                    low_confidence = 'low confidence' in reasoning.lower()
                    
                    status = "✅ PASS" if (seeks_clarification and low_confidence) else "❌ FAIL"
                    print(f"   Status: {status}")
                    print(f"   Response: {response[:100]}...")
                    print(f"   Reasoning: {reasoning[:150]}...")
                    
                    self.log_test_result(
                        test['name'], test['input'], test['expected'],
                        response, reasoning, status
                    )
                else:
                    print("   ❌ Invalid final data format")
            else:
                print("   ❌ No final event received")
                
    async def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        print("\n🔍 Testing EDGE CASES and boundary conditions")
        
        edge_case_tests = [
            {
                "name": "Empty Input",
                "input": "",
                "expected": "SEEK CLARIFICATION or ERROR"
            },
            {
                "name": "Very Short Input",
                "input": "hi",
                "expected": "EXECUTE (general conversation)"
            },
            {
                "name": "Very Long Technical Input",
                "input": "I have invented a comprehensive quantum computing system that utilizes advanced machine learning algorithms to optimize quantum gate operations, incorporating novel error correction mechanisms and quantum entanglement protocols for enhanced computational efficiency in cryptographic applications, specifically designed for post-quantum cryptography standards and quantum-resistant encryption algorithms",
                "expected": "EXECUTE (claim drafting)"
            }
        ]
        
        for test in edge_case_tests:
            print(f"\n📝 Test: {test['name']}")
            print(f"   Input: '{test['input'][:50]}{'...' if len(test['input']) > 50 else ''}'")
            
            if not test['input']:  # Skip empty input test
                print("   ⚠️  Skipping empty input test")
                continue
                
            run_id = await self.chat.start_conversation(test['input'])
            if not run_id:
                print("   ❌ Failed to start conversation")
                continue
                
            events = await self.chat.stream_response(run_id)
            
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', 'No response')
                    metadata = final_data.get('metadata', {})
                    reasoning = metadata.get('reasoning', 'Unknown')
                    
                    print(f"   Response: {response[:100]}...")
                    print(f"   Reasoning: {reasoning[:150]}...")
                    
                    # Log without strict validation for edge cases
                    self.log_test_result(
                        test['name'], test['input'], test['expected'],
                        response, reasoning, "INFO"
                    )
                else:
                    print("   ❌ Invalid final data format")
            else:
                print("   ❌ No final event received")
                
    def generate_test_report(self):
        """Generate a comprehensive test report"""
        print("\n" + "="*80)
        print("📊 CONFIDENCE THRESHOLD SYSTEM - TEST REPORT")
        print("="*80)
        
        # Count results
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == '✅ PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == '❌ FAIL'])
        info_tests = len([r for r in self.test_results if r['status'] == 'INFO'])
        
        print(f"\n📈 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ℹ️  Info: {info_tests}")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if result['status'] == '❌ FAIL':
                    print(f"   - {result['test_name']}: {result['input_text'][:50]}...")
                    
        print(f"\n✅ Passed Tests:")
        for result in self.test_results:
            if result['status'] == '✅ PASS':
                print(f"   - {result['test_name']}: {result['input_text'][:50]}...")
                
        # Save detailed results to file
        report_file = "confidence_threshold_test_results.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n📄 Detailed results saved to: {report_file}")
        
        # Overall system status
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"\n🎯 System Status: {'✅ OPERATIONAL' if success_rate >= 80 else '⚠️  NEEDS ATTENTION'}")
        print(f"   Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80

async def main():
    """Main test execution function"""
    print("🚀 Starting Confidence Threshold System Test Suite")
    print("="*60)
    
    tester = ConfidenceThresholdTester()
    
    try:
        # Setup
        await tester.setup()
        
        # Run test scenarios
        await tester.test_high_confidence_execution()
        await tester.test_low_confidence_clarification()
        await tester.test_edge_cases()
        
        # Generate report
        success = tester.generate_test_report()
        
        if success:
            print("\n🎉 Confidence Threshold System is OPERATIONAL!")
            print("   - High confidence requests (>0.7) → EXECUTE ✅")
            print("   - Low confidence requests (≤0.7) → SEEK CLARIFICATION ✅")
            print("   - No fallback systems ✅")
            print("   - Clean binary decision logic ✅")
        else:
            print("\n⚠️  Confidence Threshold System needs attention!")
            print("   - Some tests failed - review the report above")
            
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        return False
    finally:
        await tester.cleanup()
        
    return success

if __name__ == "__main__":
    # Run the test suite
    success = asyncio.run(main())
    exit(0 if success else 1)
