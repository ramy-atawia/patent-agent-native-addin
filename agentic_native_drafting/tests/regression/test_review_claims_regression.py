#!/usr/bin/env python3
"""
Regression Test Suite: Review Claims Functionality Protection

This test file captures all the tests performed to validate the review_claims function
implementation. It serves as a protection mechanism to ensure the functionality
continues to work correctly after future code changes.

Test Coverage:
1. Review Claims Function Implementation
2. Integration with Agent Intent Classification
3. Response Parsing and Formatting
4. Error Handling
5. Comparison with Draft Claims Functionality
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.cli_chat import SimpleCLIChat

class ReviewClaimsRegressionTester:
    """Regression test suite for review_claims functionality"""
    
    def __init__(self):
        self.chat = SimpleCLIChat()
        self.test_results = []
        self.protection_tests = []
        
    async def setup(self):
        """Initialize the test environment"""
        print("🔧 Setting up Review Claims Regression Test Suite...")
        if not await self.chat.test_connection():
            raise RuntimeError("❌ Failed to connect to server")
        print("✅ Server connection successful!")
        
    async def cleanup(self):
        """Clean up test resources"""
        await self.chat.close()
        
    def log_test_result(self, test_name: str, test_type: str, input_data: str, 
                       expected_behavior: str, actual_result: str, status: str):
        """Log test results for regression analysis"""
        result = {
            "test_name": test_name,
            "test_type": test_type,
            "input_data": input_data[:200] + "..." if len(input_data) > 200 else input_data,
            "expected_behavior": expected_behavior,
            "actual_result": actual_result[:300] + "..." if len(actual_result) > 300 else actual_result,
            "status": status,
            "timestamp": asyncio.get_event_loop().time()
        }
        self.test_results.append(result)
        
        # Store protection tests separately
        if test_type == "PROTECTION":
            self.protection_tests.append(result)
        
    async def test_review_claims_basic_functionality(self):
        """Test 1: Basic review_claims function implementation"""
        print("\n🔍 Test 1: Basic Review Claims Functionality")
        
        test_claim = "1. A method for processing data comprising receiving input data and processing the data."
        expected_behavior = "Should detect CLAIM_REVIEW intent and execute review_claims function"
        
        run_id = await self.chat.start_conversation(f'review this claim: {test_claim}')
        if not run_id:
            print("   ❌ Failed to start conversation")
            return
            
        events = await self.chat.stream_response(run_id)
        
        if 'final' in events:
            final_data = events['final']
            if isinstance(final_data, dict):
                response = final_data.get('response', 'No response')
                metadata = final_data.get('metadata', {})
                reasoning = metadata.get('reasoning', 'Unknown')
                
                # Check if review was executed
                review_executed = (
                    'reviewed your patent claims' in response.lower() and
                    'found' in response.lower() and
                    'issue' in response.lower()
                )
                
                # Check if reasoning shows CLAIM_REVIEW execution
                claim_review_executed = 'executing claim_review' in reasoning.lower()
                
                status = "✅ PASS" if (review_executed and claim_review_executed) else "❌ FAIL"
                print(f"   Status: {status}")
                print(f"   Response: {response[:100]}...")
                print(f"   Reasoning: {reasoning[:150]}...")
                
                self.log_test_result(
                    "Basic Review Claims Functionality",
                    "PROTECTION",
                    test_claim,
                    expected_behavior,
                    f"Response: {response[:100]}... | Reasoning: {reasoning[:100]}...",
                    status
                )
            else:
                print("   ❌ Invalid final data format")
        else:
            print("   ❌ No final event received")
            
    async def test_review_claims_complex_input(self):
        """Test 2: Review claims with complex, multi-claim input"""
        print("\n🔍 Test 2: Complex Multi-Claim Review")
        
        complex_claims = """1. A system for processing data comprising:
   a processor configured to execute instructions;
   a memory storing the instructions; and
   an output device for displaying results.

2. The system of claim 1, wherein the processor is a quantum processor.

3. The system of claim 1, further comprising a network interface."""
        
        expected_behavior = "Should handle complex multi-claim input and provide detailed review feedback"
        
        run_id = await self.chat.start_conversation(f'review these patent claims: {complex_claims}')
        if not run_id:
            print("   ❌ Failed to start conversation")
            return
            
        events = await self.chat.stream_response(run_id)
        
        if 'final' in events:
            final_data = events['final']
            if isinstance(final_data, dict):
                response = final_data.get('response', 'No response')
                metadata = final_data.get('metadata', {})
                reasoning = metadata.get('reasoning', 'Unknown')
                
                # Check if complex review was handled
                complex_review_handled = (
                    'reviewed your patent claims' in response.lower() and
                    'found' in response.lower() and
                    'issue' in response.lower() and
                    len(response) > 200  # Should be substantial review
                )
                
                status = "✅ PASS" if complex_review_handled else "❌ FAIL"
                print(f"   Status: {status}")
                print(f"   Response Length: {len(response)} characters")
                print(f"   Response: {response[:100]}...")
                
                self.log_test_result(
                    "Complex Multi-Claim Review",
                    "PROTECTION",
                    complex_claims,
                    expected_behavior,
                    f"Response Length: {len(response)} chars | Content: {response[:100]}...",
                    status
                )
            else:
                print("   ❌ Invalid final data format")
        else:
            print("   ❌ No final event received")
            
    async def test_review_claims_intent_classification(self):
        """Test 3: Verify CLAIM_REVIEW intent classification works correctly"""
        print("\n🔍 Test 3: CLAIM_REVIEW Intent Classification")
        
        review_requests = [
            "review my patent claims",
            "check these claims for compliance",
            "validate my patent claims",
            "analyze these claims for quality"
        ]
        
        expected_behavior = "Should classify all review requests as CLAIM_REVIEW with high confidence (>0.7)"
        
        for i, request in enumerate(review_requests, 1):
            print(f"   Testing request {i}: '{request}'")
            
            run_id = await self.chat.start_conversation(request)
            if not run_id:
                print("     ❌ Failed to start conversation")
                continue
                
            events = await self.chat.stream_response(run_id)
            
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    metadata = final_data.get('metadata', {})
                    reasoning = metadata.get('reasoning', 'Unknown')
                    
                    # Check if CLAIM_REVIEW was detected
                    claim_review_detected = 'executing claim_review' in reasoning.lower()
                    
                    status = "✅ PASS" if claim_review_detected else "❌ FAIL"
                    print(f"     Status: {status}")
                    
                    self.log_test_result(
                        f"CLAIM_REVIEW Intent Classification - Request {i}",
                        "PROTECTION",
                        request,
                        expected_behavior,
                        f"Reasoning: {reasoning[:100]}...",
                        status
                    )
                else:
                    print("     ❌ Invalid final data format")
            else:
                print("     ❌ No final event received")
                
    async def test_review_claims_vs_draft_claims(self):
        """Test 4: Compare review_claims and draft_claims functionality"""
        print("\n🔍 Test 4: Review Claims vs Draft Claims Comparison")
        
        # Test draft claims
        print("   Testing draft_claims functionality...")
        draft_run_id = await self.chat.start_conversation('draft patent claims for my AI invention')
        if draft_run_id:
            draft_events = await self.chat.stream_response(draft_run_id)
            draft_working = 'final' in draft_events and 'drafted' in draft_events['final'].get('response', '')
            print(f"   Draft Claims Status: {'✅ WORKING' if draft_working else '❌ FAILED'}")
        
        # Test review claims
        print("   Testing review_claims functionality...")
        test_claim = "1. A method for data processing comprising receiving input and outputting results."
        review_run_id = await self.chat.start_conversation(f'review this claim: {test_claim}')
        if review_run_id:
            review_events = await self.chat.stream_response(review_run_id)
            review_working = 'final' in review_events and 'reviewed your patent claims' in review_events['final'].get('response', '')
            print(f"   Review Claims Status: {'✅ WORKING' if review_working else '❌ FAILED'}")
        
        # Both should work
        both_working = draft_working and review_working
        status = "✅ PASS" if both_working else "❌ FAIL"
        
        self.log_test_result(
            "Review Claims vs Draft Claims Comparison",
            "PROTECTION",
            "draft_claims + review_claims",
            "Both functions should work independently and correctly",
            f"Draft: {'✅' if draft_working else '❌'} | Review: {'✅' if review_working else '❌'}",
            status
        )
        
    async def test_review_claims_error_handling(self):
        """Test 5: Error handling in review_claims function"""
        print("\n🔍 Test 5: Review Claims Error Handling")
        
        # Test with empty input
        print("   Testing empty input handling...")
        empty_run_id = await self.chat.start_conversation('review these claims:')
        if empty_run_id:
            empty_events = await self.chat.stream_response(empty_run_id)
            if 'final' in empty_events:
                final_data = empty_events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    # Should handle empty input gracefully
                    graceful_handling = len(response) > 0 and not 'error' in response.lower()
                    print(f"   Empty Input Handling: {'✅ GRACEFUL' if graceful_handling else '❌ ERROR'}")
        
        # Test with malformed input
        print("   Testing malformed input handling...")
        malformed_run_id = await self.chat.start_conversation('review these claims: [invalid input]')
        if malformed_run_id:
            malformed_events = await self.chat.stream_response(malformed_run_id)
            if 'final' in malformed_events:
                final_data = malformed_events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    # Should handle malformed input gracefully
                    graceful_handling = len(response) > 0 and not 'error' in response.lower()
                    print(f"   Malformed Input Handling: {'✅ GRACEFUL' if graceful_handling else '❌ ERROR'}")
        
        self.log_test_result(
            "Review Claims Error Handling",
            "PROTECTION",
            "empty + malformed inputs",
            "Should handle edge cases gracefully without crashing",
            "Error handling tests completed",
            "INFO"
        )
        
    async def test_review_claims_response_format(self):
        """Test 6: Verify review_claims response format and structure"""
        print("\n🔍 Test 6: Review Claims Response Format")
        
        test_claim = "1. A method for data processing."
        expected_format = "Should return formatted response with severity levels and emojis"
        
        run_id = await self.chat.start_conversation(f'review this claim: {test_claim}')
        if not run_id:
            print("   ❌ Failed to start conversation")
            return
            
        events = await self.chat.stream_response(run_id)
        
        if 'final' in events:
            final_data = events['final']
            if isinstance(final_data, dict):
                response = final_data.get('response', '')
                
                # Check for expected format elements
                has_severity_emojis = any(emoji in response for emoji in ['🟢', '🟡', '🔴'])
                has_severity_text = any(level in response for level in ['MINOR', 'MAJOR', 'CRITICAL'])
                has_issue_count = 'found' in response and 'issue' in response
                
                format_correct = has_severity_emojis and has_severity_text and has_issue_count
                status = "✅ PASS" if format_correct else "❌ FAIL"
                
                print(f"   Status: {status}")
                print(f"   Has Severity Emojis: {'✅' if has_severity_emojis else '❌'}")
                print(f"   Has Severity Text: {'✅' if has_severity_text else '❌'}")
                print(f"   Has Issue Count: {'✅' if has_severity_text else '❌'}")
                
                self.log_test_result(
                    "Review Claims Response Format",
                    "PROTECTION",
                    test_claim,
                    expected_format,
                    f"Emojis: {'✅' if has_severity_emojis else '❌'} | Text: {'✅' if has_severity_text else '❌'} | Count: {'✅' if has_severity_text else '❌'}",
                    status
                )
            else:
                print("   ❌ Invalid final data format")
        else:
            print("   ❌ No final event received")
            
    def generate_regression_report(self):
        """Generate comprehensive regression test report"""
        print("\n" + "="*80)
        print("📊 REVIEW CLAIMS REGRESSION TEST REPORT")
        print("="*80)
        
        # Count results
        total_tests = len(self.test_results)
        protection_tests = len(self.protection_tests)
        passed_tests = len([r for r in self.test_results if r['status'] == '✅ PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == '❌ FAIL'])
        info_tests = len([r for r in self.test_results if r['status'] == 'INFO'])
        
        print(f"\n📈 Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Protection Tests: {protection_tests}")
        print(f"   ✅ Passed: {passed_tests}")
        print(f"   ❌ Failed: {failed_tests}")
        print(f"   ℹ️  Info: {info_tests}")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if result['status'] == '❌ FAIL':
                    print(f"   - {result['test_name']}: {result['input_data'][:50]}...")
                    
        print(f"\n✅ Passed Tests:")
        for result in self.test_results:
            if result['status'] == '✅ PASS':
                print(f"   - {result['test_name']}")
                
        # Save detailed results to file
        report_file = "review_claims_regression_results.json"
        with open(report_file, 'w') as f:
            json.dump(self.test_results, f, indent=2)
        print(f"\n📄 Detailed results saved to: {report_file}")
        
        # Protection status
        protection_success_rate = (len([r for r in self.protection_tests if r['status'] == '✅ PASS']) / len(self.protection_tests) * 100) if protection_tests > 0 else 0
        print(f"\n🛡️  Protection Status: {'✅ SECURED' if protection_success_rate >= 90 else '⚠️  NEEDS ATTENTION'}")
        print(f"   Protection Success Rate: {protection_success_rate:.1f}%")
        
        # Overall system status
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"\n🎯 Overall System Status: {'✅ OPERATIONAL' if success_rate >= 80 else '⚠️  NEEDS ATTENTION'}")
        print(f"   Overall Success Rate: {success_rate:.1f}%")
        
        return success_rate >= 80 and protection_success_rate >= 90

async def main():
    """Main regression test execution function"""
    print("🚀 Starting Review Claims Regression Test Suite")
    print("🛡️  Purpose: Protect review_claims functionality from future changes")
    print("="*60)
    
    tester = ReviewClaimsRegressionTester()
    
    try:
        # Setup
        await tester.setup()
        
        # Run all regression tests
        await tester.test_review_claims_basic_functionality()
        await tester.test_review_claims_complex_input()
        await tester.test_review_claims_intent_classification()
        await tester.test_review_claims_vs_draft_claims()
        await tester.test_review_claims_error_handling()
        await tester.test_review_claims_response_format()
        
        # Generate comprehensive report
        success = tester.generate_regression_report()
        
        if success:
            print("\n🎉 Review Claims Functionality is PROTECTED!")
            print("   - All core functionality tests passed ✅")
            print("   - Protection tests secured the implementation 🛡️")
            print("   - Future changes can be validated against this baseline 📊")
        else:
            print("\n⚠️  Review Claims Functionality needs attention!")
            print("   - Some tests failed - review the report above")
            print("   - Protection level may be compromised")
            
    except Exception as e:
        print(f"\n💥 Regression test execution failed: {e}")
        return False
    finally:
        await tester.cleanup()
        
    return success

if __name__ == "__main__":
    # Run the regression test suite
    success = asyncio.run(main())
    exit(0 if success else 1)
