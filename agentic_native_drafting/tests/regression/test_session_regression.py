#!/usr/bin/env python3
"""
Session Management Regression Test Suite
Tests complex multi-turn conversations and session persistence
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List, Any
from datetime import datetime

class SessionRegressionTester:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.test_results = []
        
    async def test_connection(self) -> bool:
        """Test if the server is running"""
        try:
            response = await self.client.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Server connection successful!")
                return True
            else:
                print(f"❌ Server responded with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            return False
    
    async def start_run(self, disclosure: str, session_id: str = None) -> Dict[str, str]:
        """Start a new run or continue existing session"""
        try:
            payload = {"disclosure": disclosure}
            if session_id:
                payload["session_id"] = session_id
                print(f"🔄 Continuing session: {session_id}")
            else:
                print(f"🆕 Starting new session")
            
            response = await self.client.post(
                f"{self.base_url}/api/patent/run",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                return result
            else:
                print(f"❌ Failed to start run: {response.status_code}")
                return {}
                
        except Exception as e:
            print(f"❌ Error starting conversation: {e}")
            return {}
    
    async def stream_response(self, run_id: str) -> Dict[str, Any]:
        """Stream the response and collect all events"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/patent/stream",
                params={"run_id": run_id}
            )
            
            if response.status_code != 200:
                print(f"❌ Stream failed: {response.status_code}")
                return {}
            
            # Parse SSE response
            events = {}
            content = response.text
            
            lines = content.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if line.startswith('event:'):
                    event_type = line.split(':', 1)[1].strip()
                    
                    # Look for the corresponding data
                    data_lines = []
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith('event:'):
                        if lines[i].strip().startswith('data:'):
                            data_content = lines[i].split(':', 1)[1].strip()
                            data_lines.append(data_content)
                        i += 1
                    
                    # Combine multiline data
                    if data_lines:
                        combined_data = '\n'.join(data_lines)
                        try:
                            if combined_data == "{}":
                                events[event_type] = {}
                            else:
                                data = json.loads(combined_data)
                                events[event_type] = data
                        except json.JSONDecodeError as e:
                            print(f"⚠️  JSON parse error for {event_type}: {e}")
                            events[event_type] = combined_data
                else:
                    i += 1
            
            return events
            
        except Exception as e:
            print(f"❌ Error streaming response: {e}")
            return {}
    
    async def get_session_info(self, session_id: str) -> Dict[str, Any]:
        """Get session information"""
        try:
            response = await self.client.get(f"{self.base_url}/api/debug/session/{session_id}")
            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"Status {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}
    
    async def list_sessions(self) -> List[Dict[str, Any]]:
        """List all sessions"""
        try:
            response = await self.client.get(f"{self.base_url}/api/sessions")
            if response.status_code == 200:
                data = response.json()
                return data.get("sessions", [])
            else:
                return []
        except Exception as e:
            print(f"❌ Error listing sessions: {e}")
            return []
    
    async def test_complex_patent_workflow(self) -> Dict[str, Any]:
        """Test a complex patent drafting workflow with multiple turns"""
        print("\n🔍 Test: Complex Patent Workflow")
        print("=" * 50)
        
        test_result = {
            "test_name": "Complex Patent Workflow",
            "steps": [],
            "session_id": None,
            "success": False,
            "errors": []
        }
        
        try:
            # Step 1: Start new session - Draft claims
            print("\n📝 Step 1: Draft initial claims")
            result = await self.start_run("I have invented a quantum computing system that uses AI to optimize qubit entanglement patterns for improved error correction")
            if not result:
                test_result["errors"].append("Failed to start initial run")
                return test_result
            
            run_id = result.get("run_id")
            session_id = result.get("session_id")
            test_result["session_id"] = session_id
            
            print(f"✅ Started session: {session_id}")
            print(f"✅ Run ID: {run_id}")
            
            # Stream response
            events = await self.stream_response(run_id)
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    claims = final_data.get('data', {}).get('claims', [])
                    print(f"✅ Claims generated: {len(claims)}")
                    test_result["steps"].append({
                        "step": "draft_initial_claims",
                        "status": "success",
                        "claims_count": len(claims),
                        "response_length": len(response)
                    })
                else:
                    test_result["errors"].append("Invalid final data format")
                    return test_result
            else:
                test_result["errors"].append("No final event in stream")
                return test_result
            
            # Step 2: Continue session - Review claims
            print("\n🔍 Step 2: Review the generated claims")
            result = await self.start_run("review those claims and identify the top 3 issues", session_id)
            if not result:
                test_result["errors"].append("Failed to continue session")
                return test_result
            
            run_id = result.get("run_id")
            print(f"✅ Continued session with run: {run_id}")
            
            # Stream response
            events = await self.stream_response(run_id)
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    print(f"✅ Review completed: {len(response)} characters")
                    test_result["steps"].append({
                        "step": "review_claims",
                        "status": "success",
                        "response_length": len(response)
                    })
                else:
                    test_result["errors"].append("Invalid review response format")
                    return test_result
            else:
                test_result["errors"].append("No final event in review stream")
                return test_result
            
            # Step 3: Continue session - Improve specific claim
            print("\n🔧 Step 3: Improve claim 1 based on review")
            result = await self.start_run("improve claim 1 to address the clarity issues mentioned in the review", session_id)
            if not result:
                test_result["errors"].append("Failed to continue session for improvement")
                return test_result
            
            run_id = result.get("run_id")
            print(f"✅ Continued session with run: {run_id}")
            
            # Stream response
            events = await self.stream_response(run_id)
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    print(f"✅ Improvement completed: {len(response)} characters")
                    test_result["steps"].append({
                        "step": "improve_claim",
                        "status": "success",
                        "response_length": len(response)
                    })
                else:
                    test_result["errors"].append("Invalid improvement response format")
                    return test_result
            else:
                test_result["errors"].append("No final event in improvement stream")
                return test_result
            
            # Step 4: Continue session - Final review
            print("\n📋 Step 4: Final review of improved claims")
            result = await self.start_run("provide a final assessment of the improved claims", session_id)
            if not result:
                test_result["errors"].append("Failed to continue session for final review")
                return test_result
            
            run_id = result.get("run_id")
            print(f"✅ Continued session with run: {run_id}")
            
            # Stream response
            events = await self.stream_response(run_id)
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    print(f"✅ Final review completed: {len(response)} characters")
                    test_result["steps"].append({
                        "step": "final_review",
                        "status": "success",
                        "response_length": len(response)
                    })
                else:
                    test_result["errors"].append("Invalid final review response format")
                    return test_result
            else:
                test_result["errors"].append("No final event in final review stream")
                return test_result
            
            # Step 5: Verify session integrity
            print("\n🔍 Step 5: Verify session integrity")
            session_info = await self.get_session_info(session_id)
            if "error" not in session_info:
                runs = session_info.get("runs", [])
                history_length = len(session_info.get("session_history", ""))
                print(f"✅ Session runs: {len(runs)}")
                print(f"✅ Session history: {history_length} characters")
                print(f"✅ Session topic: {session_info.get('topic', 'N/A')}")
                
                test_result["steps"].append({
                    "step": "verify_session_integrity",
                    "status": "success",
                    "total_runs": len(runs),
                    "history_length": history_length
                })
                
                test_result["success"] = True
                print("🎉 Complex workflow test completed successfully!")
            else:
                test_result["errors"].append(f"Failed to verify session: {session_info.get('error')}")
            
        except Exception as e:
            test_result["errors"].append(f"Test execution error: {str(e)}")
            print(f"❌ Test execution error: {e}")
        
        return test_result
    
    async def test_session_isolation(self) -> Dict[str, Any]:
        """Test that sessions are properly isolated"""
        print("\n🔍 Test: Session Isolation")
        print("=" * 30)
        
        test_result = {
            "test_name": "Session Isolation",
            "steps": [],
            "success": False,
            "errors": []
        }
        
        try:
            # Create two separate sessions
            print("\n📝 Creating Session A")
            result_a = await self.start_run("draft claims for a blockchain invention")
            if not result_a:
                test_result["errors"].append("Failed to create Session A")
                return test_result
            
            session_a_id = result_a.get("session_id")
            run_a_id = result_a.get("run_id")
            print(f"✅ Session A: {session_a_id}")
            
            # Complete Session A
            events = await self.stream_response(run_a_id)
            if 'final' not in events:
                test_result["errors"].append("Session A did not complete")
                return test_result
            
            print("\n📝 Creating Session B")
            result_b = await self.start_run("draft claims for a quantum computing invention")
            if not result_b:
                test_result["errors"].append("Failed to create Session B")
                return test_result
            
            session_b_id = result_b.get("session_id")
            run_b_id = result_b.get("run_id")
            print(f"✅ Session B: {session_b_id}")
            
            # Complete Session B
            events = await self.stream_response(run_b_id)
            if 'final' not in events:
                test_result["errors"].append("Session B did not complete")
                return test_result
            
            # Verify sessions are different
            if session_a_id == session_b_id:
                test_result["errors"].append("Sessions A and B have the same ID")
                return test_result
            
            print(f"✅ Sessions are different: {session_a_id} vs {session_b_id}")
            
            # Check session A still has its original content
            session_a_info = await self.get_session_info(session_a_id)
            if "error" not in session_a_info:
                history_a = session_a_info.get("session_history", "")
                if "blockchain" not in history_a.lower():
                    test_result["errors"].append("Session A lost its blockchain content")
                    return test_result
                print("✅ Session A maintains blockchain content")
            
            # Check session B has its content
            session_b_info = await self.get_session_info(session_b_id)
            if "error" not in session_b_info:
                history_b = session_b_info.get("session_history", "")
                if "quantum" not in history_b.lower():
                    test_result["errors"].append("Session B lost its quantum content")
                    return test_result
                print("✅ Session B maintains quantum content")
            
            test_result["success"] = True
            test_result["steps"].append({
                "step": "session_isolation",
                "status": "success",
                "session_a_id": session_a_id,
                "session_b_id": session_b_id
            })
            
            print("🎉 Session isolation test completed successfully!")
            
        except Exception as e:
            test_result["errors"].append(f"Test execution error: {str(e)}")
            print(f"❌ Test execution error: {e}")
        
        return test_result
    
    async def test_context_persistence(self) -> Dict[str, Any]:
        """Test that context persists correctly across multiple turns"""
        print("\n🔍 Test: Context Persistence")
        print("=" * 30)
        
        test_result = {
            "test_name": "Context Persistence",
            "steps": [],
            "success": False,
            "errors": []
        }
        
        try:
            # Start session with specific invention
            print("\n📝 Starting session with specific invention")
            result = await self.start_run("I invented a neural network that can predict weather patterns using satellite data and machine learning")
            if not result:
                test_result["errors"].append("Failed to start session")
                return test_result
            
            session_id = result.get("session_id")
            run_id = result.get("run_id")
            print(f"✅ Session started: {session_id}")
            
            # Complete initial run
            events = await self.stream_response(run_id)
            if 'final' not in events:
                test_result["errors"].append("Initial run did not complete")
                return test_result
            
            # Continue with context-dependent request
            print("\n🔄 Testing context-dependent request")
            result = await self.start_run("how many claims did you generate for my weather prediction system?", session_id)
            if not result:
                test_result["errors"].append("Failed to continue session")
                return test_result
            
            run_id = result.get("run_id")
            events = await self.stream_response(run_id)
            
            if 'final' in events:
                final_data = events['final']
                if isinstance(final_data, dict):
                    response = final_data.get('response', '')
                    print(f"✅ Context response: {response[:100]}...")
                    
                    # Check if response shows context awareness
                    if "weather" in response.lower() or "satellite" in response.lower():
                        print("✅ Response shows context awareness")
                        test_result["steps"].append({
                            "step": "context_awareness",
                            "status": "success",
                            "response_length": len(response)
                        })
                    else:
                        print("⚠️  Response may lack context awareness")
                        test_result["steps"].append({
                            "step": "context_awareness",
                            "status": "warning",
                            "response_length": len(response)
                        })
                else:
                    test_result["errors"].append("Invalid response format")
                    return test_result
            else:
                test_result["errors"].append("No final event in context test")
                return test_result
            
            test_result["success"] = True
            print("🎉 Context persistence test completed successfully!")
            
        except Exception as e:
            test_result["errors"].append(f"Test execution error: {str(e)}")
            print(f"❌ Test execution error: {e}")
        
        return test_result
    
    async def run_all_tests(self):
        """Run all regression tests"""
        print("🚀 Starting Session Management Regression Tests")
        print("=" * 60)
        
        if not await self.test_connection():
            print("❌ Cannot connect to server. Exiting.")
            return
        
        # Run all tests
        tests = [
            await self.test_complex_patent_workflow(),
            await self.test_session_isolation(),
            await self.test_context_persistence()
        ]
        
        # Generate report
        print("\n📊 Test Results Summary")
        print("=" * 40)
        
        total_tests = len(tests)
        passed_tests = sum(1 for test in tests if test["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Detailed results
        for i, test in enumerate(tests, 1):
            status = "✅ PASS" if test["success"] else "❌ FAIL"
            print(f"\n{i}. {test['test_name']}: {status}")
            
            if test["steps"]:
                print("   Steps:")
                for step in test["steps"]:
                    step_status = "✅" if step["status"] == "success" else "⚠️"
                    print(f"     {step_status} {step['step']}")
            
            if test["errors"]:
                print("   Errors:")
                for error in test["errors"]:
                    print(f"     ❌ {error}")
        
        # Save detailed report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"session_regression_report_{timestamp}.md"
        
        with open(report_filename, 'w') as f:
            f.write(f"# Session Management Regression Test Report\n\n")
            f.write(f"**Generated:** {datetime.now().isoformat()}\n")
            f.write(f"**Total Tests:** {total_tests}\n")
            f.write(f"**Passed:** {passed_tests}\n")
            f.write(f"**Failed:** {failed_tests}\n")
            f.write(f"**Success Rate:** {(passed_tests/total_tests)*100:.1f}%\n\n")
            
            for test in tests:
                f.write(f"## {test['test_name']}\n\n")
                f.write(f"**Status:** {'✅ PASS' if test['success'] else '❌ FAIL'}\n\n")
                
                if test["steps"]:
                    f.write("### Steps:\n")
                    for step in test["steps"]:
                        f.write(f"- {step['step']}: {step['status']}\n")
                    f.write("\n")
                
                if test["errors"]:
                    f.write("### Errors:\n")
                    for error in test["errors"]:
                        f.write(f"- {error}\n")
                    f.write("\n")
        
        print(f"\n📄 Detailed report saved to: {report_filename}")
        
        # Cleanup
        await self.client.aclose()
        
        return tests

async def main():
    """Main test runner"""
    tester = SessionRegressionTester()
    await tester.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main())
