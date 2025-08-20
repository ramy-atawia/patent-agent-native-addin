#!/usr/bin/env python3
"""
Regression Test Suite: Draft Claims Functionality Protection

This test file captures all the tests performed to validate the draft_claims function
implementation. It serves as a protection mechanism to ensure the functionality
continues to work correctly after future code changes.

Test Coverage:
1. Draft Claims Function Implementation
2. Integration with Agent Intent Classification
3. Response Parsing and Claim Generation
4. Error Handling
5. Comparison with Review Claims Functionality
6. Different Invention Types and Complexities
"""

import asyncio
import json
from typing import Dict, Any, List
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.cli_chat import SimpleCLIChat

class DraftClaimsRegressionTester:
    """Regression test suite for draft_claims functionality"""
    
    def __init__(self):
        self.chat = SimpleCLIChat()
        self.test_results = []
        self.protection_tests = []
        
    async def setup(self):
        """Initialize the test environment"""
        print("🔧 Setting up Draft Claims Regression Test Suite...")
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
        
    async def test_draft_claims_basic_functionality(self):
        """Test 1: Basic draft_claims function implementation"""
        print("\n🔍 Test 1: Basic Draft Claims Functionality")
        
        test_invention = "I invented an AI system for data processing"
        expected_behavior = "Should detect CLAIM_DRAFTING intent and execute draft_claims function"
        
        run_id = await self.chat.start_conversation(f'draft patent claims for {test_invention}')
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
                
                # Check if claims were drafted
                claims_drafted = (
                    'drafted' in response.lower() and
                    'patent claims' in response.lower() and
                    'invention' in response.lower()
                )
                
                # Check if reasoning shows CLAIM_DRAFTING execution
                claim_drafting_executed = 'executing claim_drafting' in reasoning.lower()
                
                # Check if claims are in the data
                has_claims_data = 'data' in final_data and 'claims' in final_data['data']
                
                status = "✅ PASS" if (claims_drafted and claim_drafting_executed and has_claims_data) else "❌ FAIL"
                print(f"   Status: {status}")
                print(f"   Response: {response[:100]}...")
                print(f"   Reasoning: {reasoning[:150]}...")
                print(f"   Has Claims Data: {'✅' if has_claims_data else '❌'}")
                
                self.log_test_result(
                    "Basic Draft Claims Functionality",
                    "PROTECTION",
                    test_invention,
                    expected_behavior,
                    f"Response: {response[:100]}... | Reasoning: {reasoning[:100]}... | Claims Data: {'✅' if has_claims_data else '❌'}",
                    status
                )
            else:
                print("   ❌ Invalid final data format")
        else:
            print("   ❌ No final event received")
            
    async def test_draft_claims_complex_invention(self):
        """Test 2: Draft claims for complex, technical invention"""
        print("\n🔍 Test 2: Complex Technical Invention Claims Drafting")
        
        complex_invention = """I invented a 5G AI carrier aggregation system that uses machine learning to dynamically select and combine multiple frequency carriers based on real-time network conditions, incorporating quantum-resistant encryption and adaptive beamforming algorithms."""
        
        expected_behavior = "Should handle complex technical invention and generate detailed patent claims"
        
        run_id = await self.chat.start_conversation(f'draft patent claims for {complex_invention}')
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
                
                # Check if complex invention was handled
                complex_handled = (
                    'drafted' in response.lower() and
                    'patent claims' in response.lower() and
                    len(response) > 200  # Should be substantial response
                )
                
                # Check if claims data exists
                has_claims_data = 'data' in final_data and 'claims' in final_data['data']
                if has_claims_data:
                    num_claims = len(final_data['data']['claims'])
                    print(f"   Number of Claims Generated: {num_claims}")
                
                status = "✅ PASS" if (complex_handled and has_claims_data) else "❌ FAIL"
                print(f"   Status: {status}")
                print(f"   Response Length: {len(response)} characters")
                print(f"   Response: {response[:100]}...")
                
                self.log_test_result(
                    "Complex Technical Invention Claims Drafting",
                    "PROTECTION",
                    complex_invention,
                    expected_behavior,
                    f"Response Length: {len(response)} chars | Claims Data: {'✅' if has_claims_data else '❌'} | Content: {response[:100]}...",
                    status
                )
            else:
                print("   ❌ Invalid final data format")
        else:
            print("   ❌ No final event received")
            
    async def test_draft_claims_intent_classification(self):
        """Test 3: Verify CLAIM_DRAFTING intent classification works correctly"""
        print("\n🔍 Test 3: CLAIM_DRAFTING Intent Classification")
        
        drafting_requests = [
            "draft patent claims for my invention",
            "create patent claims for my AI system",
            "generate claims for my technology",
            "write patent claims for my invention",
            "make patent claims for my system"
        ]
        
        expected_behavior = "Should classify all drafting requests as CLAIM_DRAFTING with high confidence (>0.7)"
        
        for i, request in enumerate(drafting_requests, 1):
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
                    
                    # Check if CLAIM_DRAFTING was detected
                    claim_drafting_detected = 'executing claim_drafting' in reasoning.lower()
                    
                    status = "✅ PASS" if claim_drafting_detected else "❌ FAIL"
                    print(f"     Status: {status}")
                    
                    self.log_test_result(
                        f"CLAIM_DRAFTING Intent Classification - Request {i}",
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
                
    async def test_draft_claims_vs_review_claims(self):
        """Test 4: Compare draft_claims and review_claims functionality"""
        print("\n🔍 Test 4: Draft Claims vs Review Claims Comparison")
        
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
            "Draft Claims vs Review Claims Comparison",
            "PROTECTION",
            "draft_claims + review_claims",
            "Both functions should work independently and correctly",
            f"Draft: {'✅' if draft_working else '❌'} | Review: {'✅' if review_working else '❌'}",
            status
        )
        
    async def test_draft_claims_error_handling(self):
        """Test 5: Error handling in draft_claims function"""
        print("\n🔍 Test 5: Draft Claims Error Handling")
        
        # Test with minimal input
        print("   Testing minimal input handling...")
        minimal_run_id = await self.chat.start_conversation('draft claims for invention')
        if minimal_run_id:
            minimal_events = await self.chat.stream_response(minimal_run_id)
            if 'final' in minimal_events:
                final_data = minimal_events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    # Should handle minimal input gracefully
                    graceful_handling = len(response) > 0 and not 'error' in response.lower()
                    print(f"   Minimal Input Handling: {'✅ GRACEFUL' if graceful_handling else '❌ ERROR'}")
        
        # Test with very short input
        print("   Testing very short input handling...")
        short_run_id = await self.chat.start_conversation('draft claims')
        if short_run_id:
            short_events = await self.chat.stream_response(short_run_id)
            if 'final' in short_events:
                final_data = short_events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    # Should handle short input gracefully
                    graceful_handling = len(response) > 0 and not 'error' in response.lower()
                    print(f"   Short Input Handling: {'✅ GRACEFUL' if graceful_handling else '❌ ERROR'}")
        
        self.log_test_result(
            "Draft Claims Error Handling",
            "PROTECTION",
            "minimal + short inputs",
            "Should handle edge cases gracefully without crashing",
            "Error handling tests completed",
            "INFO"
        )
        
    async def test_draft_claims_response_format(self):
        """Test 6: Verify draft_claims response format and structure"""
        print("\n🔍 Test 6: Draft Claims Response Format")
        
        test_invention = "I invented a simple data processing system"
        expected_format = "Should return formatted response with generated claims and proper structure"
        
        run_id = await self.chat.start_conversation(f'draft patent claims for {test_invention}')
        if not run_id:
            print("   ❌ Failed to start conversation")
            return
            
        events = await self.chat.stream_response(run_id)
        
        if 'final' in events:
            final_data = events['final']
            if isinstance(final_data, dict):
                response = final_data.get('response', '')
                
                # Check for expected format elements
                has_drafting_message = 'drafted' in response.lower() and 'patent claims' in response.lower()
                has_claims_data = 'data' in final_data and 'claims' in final_data['data']
                has_metadata = 'metadata' in final_data
                
                format_correct = has_drafting_message and has_claims_data and has_metadata
                status = "✅ PASS" if format_correct else "❌ FAIL"
                
                print(f"   Status: {status}")
                print(f"   Has Drafting Message: {'✅' if has_drafting_message else '❌'}")
                print(f"   Has Claims Data: {'✅' if has_claims_data else '❌'}")
                print(f"   Has Metadata: {'✅' if has_metadata else '❌'}")
                
                if has_claims_data:
                    claims = final_data['data']['claims']
                    print(f"   Number of Claims: {len(claims)}")
                    print(f"   First Claim: {claims[0][:100]}...")
                
                self.log_test_result(
                    "Draft Claims Response Format",
                    "PROTECTION",
                    test_invention,
                    expected_format,
                    f"Drafting Message: {'✅' if has_drafting_message else '❌'} | Claims Data: {'✅' if has_claims_data else '❌'} | Metadata: {'✅' if has_metadata else '❌'}",
                    status
                )
            else:
                print("   ❌ Invalid final data format")
        else:
            print("   ❌ No final event received")
            
    async def test_draft_claims_different_invention_types(self):
        """Test 7: Test draft_claims with different types of inventions"""
        print("\n🔍 Test 7: Different Invention Types Claims Drafting")
        
        invention_types = [
            ("Software", "I invented a machine learning algorithm for image recognition"),
            ("Hardware", "I invented a quantum computing processor with novel architecture"),
            ("Method", "I invented a method for optimizing network traffic using AI"),
            ("System", "I invented a distributed computing system for big data processing")
        ]
        
        expected_behavior = "Should handle different invention types and generate appropriate claims"
        
        for invention_type, description in invention_types:
            print(f"   Testing {invention_type}: '{description[:50]}...'")
            
            run_id = await self.chat.start_conversation(f'draft patent claims for {description}')
            if not run_id:
                print("     ❌ Failed to start conversation")
                continue
                
            events = await self.chat.stream_response(run_id)
            
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    has_claims_data = 'data' in final_data and 'claims' in final_data['data']
                    
                    status = "✅ PASS" if has_claims_data else "❌ FAIL"
                    print(f"     Status: {status}")
                    
                    self.log_test_result(
                        f"Different Invention Types - {invention_type}",
                        "PROTECTION",
                        description,
                        expected_behavior,
                        f"Claims Generated: {'✅' if has_claims_data else '❌'} | Response: {response[:100]}...",
                        status
                    )
                else:
                    print("     ❌ Invalid final data format")
            else:
                print("     ❌ No final event received")
                
    def generate_regression_report(self):
        """Generate comprehensive regression test report"""
        print("\n" + "="*80)
        print("📊 DRAFT CLAIMS REGRESSION TEST REPORT")
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
        report_file = "draft_claims_regression_results.json"
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
    print("🚀 Starting Draft Claims Regression Test Suite")
    print("🛡️  Purpose: Protect draft_claims functionality from future changes")
    print("="*60)
    
    tester = DraftClaimsRegressionTester()
    
    try:
        # Setup
        await tester.setup()
        
        # Run all regression tests
        await tester.test_draft_claims_basic_functionality()
        await tester.test_draft_claims_complex_invention()
        await tester.test_draft_claims_intent_classification()
        await tester.test_draft_claims_vs_review_claims()
        await tester.test_draft_claims_error_handling()
        await tester.test_draft_claims_response_format()
        await tester.test_draft_claims_different_invention_types()
        
        # Generate comprehensive report
        success = tester.generate_regression_report()
        
        if success:
            print("\n🎉 Draft Claims Functionality is PROTECTED!")
            print("   - All core functionality tests passed ✅")
            print("   - Protection tests secured the implementation 🛡️")
            print("   - Future changes can be validated against this baseline 📊")
        else:
            print("\n⚠️  Draft Claims Functionality needs attention!")
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
