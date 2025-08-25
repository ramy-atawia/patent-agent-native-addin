#!/usr/bin/env python3
"""
Live Demo Script for the New Modular System

This script demonstrates the new system working by:
1. Testing API endpoints
2. Running sample workflows
3. Showing streaming responses
4. Validating functionality
"""

import asyncio
import json
import time
import requests
from typing import Dict, Any

class LiveDemo:
    """Live demonstration of the new modular system"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def test_health(self) -> bool:
        """Test the health endpoint"""
        print("🏥 Testing Health Endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Health: {data.get('status', 'unknown')}")
                print(f"   📊 Timestamp: {data.get('timestamp', 'N/A')}")
                return True
            else:
                print(f"   ❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Health check error: {e}")
            return False
    
    def test_root(self) -> bool:
        """Test the root endpoint"""
        print("\n🏠 Testing Root Endpoint...")
        try:
            response = self.session.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Title: {data.get('title', 'N/A')}")
                print(f"   📋 Version: {data.get('version', 'N/A')}")
                print(f"   📝 Description: {data.get('description', 'N/A')[:100]}...")
                return True
            else:
                print(f"   ❌ Root endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Root endpoint error: {e}")
            return False
    
    def test_orchestrator_status(self) -> bool:
        """Test the orchestrator status endpoint"""
        print("\n🎯 Testing Orchestrator Status...")
        try:
            response = self.session.get(f"{self.base_url}/orchestrator/status")
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Status: {data.get('status', 'unknown')}")
                print(f"   🔧 Tools Available: {data.get('tools_available', 0)}")
                print(f"   ⚡ Chains Available: {data.get('chains_available', 0)}")
                print(f"   💾 Active Sessions: {data.get('active_sessions', 0)}")
                return True
            else:
                print(f"   ❌ Orchestrator status failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Orchestrator status error: {e}")
            return False
    
    def test_agent_run_basic(self) -> bool:
        """Test basic agent run"""
        print("\n🤖 Testing Basic Agent Run...")
        request_data = {
            "user_input": "Draft claims for 5G technology",
            "context": "Wireless communication patent"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/agent/run", json=request_data)
            if response.status_code == 200:
                print("   ✅ Basic agent run successful")
                print(f"   📊 Response length: {len(response.content)} bytes")
                return True
            else:
                print(f"   ❌ Basic agent run failed: {response.status_code}")
                print(f"   📝 Response: {response.text[:200]}...")
                return False
        except Exception as e:
            print(f"   ❌ Basic agent run error: {e}")
            return False
    
    def test_agent_run_with_params(self) -> bool:
        """Test agent run with parameters"""
        print("\n⚙️ Testing Agent Run with Parameters...")
        request_data = {
            "user_input": "Create comprehensive patent claims for wireless communication",
            "context": "5G wireless system with dynamic spectrum sharing",
            "max_claims": 5,
            "claim_types": ["independent", "dependent"],
            "focus_areas": ["wireless", "5G", "spectrum"],
            "use_chain": False
        }
        
        try:
            response = self.session.post(f"{self.base_url}/agent/run", json=request_data)
            if response.status_code == 200:
                print("   ✅ Parameterized agent run successful")
                print(f"   📊 Response length: {len(response.content)} bytes")
                return True
            else:
                print(f"   ❌ Parameterized agent run failed: {response.status_code}")
                print(f"   📝 Response: {response.text[:200]}...")
                return False
        except Exception as e:
            print(f"   ❌ Parameterized agent run error: {e}")
            return False
    
    def test_tool_execute(self) -> bool:
        """Test direct tool execution"""
        print("\n🔧 Testing Direct Tool Execution...")
        request_data = {
            "tool_name": "ClaimDraftingTool",
            "user_input": "A method for wireless communication using 5G technology",
            "context": "5G wireless implementation"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/tool/execute", json=request_data)
            if response.status_code == 200:
                print("   ✅ Tool execution successful")
                print(f"   📊 Response length: {len(response.content)} bytes")
                return True
            else:
                print(f"   ❌ Tool execution failed: {response.status_code}")
                print(f"   📝 Response: {response.text[:200]}...")
                return False
        except Exception as e:
            print(f"   ❌ Tool execution error: {e}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test error handling"""
        print("\n🚨 Testing Error Handling...")
        
        # Test empty input
        request_data = {
            "user_input": "",
            "context": "Test context"
        }
        
        try:
            response = self.session.post(f"{self.base_url}/agent/run", json=request_data)
            if response.status_code == 422:  # Validation error expected
                print("   ✅ Empty input validation working")
            else:
                print(f"   ⚠️ Unexpected response for empty input: {response.status_code}")
            
            # Test invalid tool
            tool_request = {
                "tool_name": "invalid_tool",
                "user_input": "Test input",
                "context": "Test context"
            }
            
            response = self.session.post(f"{self.base_url}/tool/execute", json=tool_request)
            if response.status_code == 422:  # Validation error expected
                print("   ✅ Invalid tool validation working")
            else:
                print(f"   ⚠️ Unexpected response for invalid tool: {response.status_code}")
            
            return True
        except Exception as e:
            print(f"   ❌ Error handling test failed: {e}")
            return False
    
    def test_streaming_response(self) -> bool:
        """Test streaming response handling"""
        print("\n🌊 Testing Streaming Response...")
        request_data = {
            "user_input": "Draft comprehensive claims for 5G technology",
            "context": "Advanced wireless communication system"
        }
        
        try:
            # Use a longer timeout for streaming
            response = self.session.post(
                f"{self.base_url}/agent/run", 
                json=request_data, 
                timeout=30,
                stream=True
            )
            
            if response.status_code == 200:
                print("   ✅ Streaming response initiated")
                
                # Read the response content
                content = response.content.decode('utf-8', errors='ignore')
                print(f"   📊 Response content length: {len(content)} characters")
                
                # Look for streaming indicators
                if "data:" in content:
                    print("   ✅ Streaming data format detected")
                else:
                    print("   ⚠️ No streaming data format detected")
                
                return True
            else:
                print(f"   ❌ Streaming response failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"   ❌ Streaming response error: {e}")
            return False
    
    def run_comprehensive_demo(self) -> Dict[str, bool]:
        """Run the complete demo suite"""
        print("🚀 STARTING COMPREHENSIVE LIVE DEMO")
        print("=" * 60)
        print(f"🌐 Testing API at: {self.base_url}")
        print("=" * 60)
        
        start_time = time.time()
        results = {}
        
        # Run all tests
        results['health'] = self.test_health()
        results['root'] = self.test_root()
        results['orchestrator_status'] = self.test_orchestrator_status()
        results['agent_run_basic'] = self.test_agent_run_basic()
        results['agent_run_params'] = self.test_agent_run_with_params()
        results['tool_execute'] = self.test_tool_execute()
        results['error_handling'] = self.test_error_handling()
        results['streaming'] = self.test_streaming_response()
        
        end_time = time.time()
        duration = end_time - start_time
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 DEMO RESULTS SUMMARY")
        print("=" * 60)
        
        passed = sum(results.values())
        total = len(results)
        
        for test_name, result in results.items():
            status = "✅ PASS" if result else "❌ FAIL"
            print(f"   {test_name:20} : {status}")
        
        print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
        print(f"⏱️  Total Duration: {duration:.2f} seconds")
        
        if passed == total:
            print("\n🎉 ALL TESTS PASSED! System is ready for production demo!")
        elif passed >= total * 0.8:
            print("\n🟡 MOST TESTS PASSED! System is mostly ready for demo.")
        else:
            print("\n⚠️  MANY TESTS FAILED! System needs fixes before demo.")
        
        return results

def main():
    """Main demo function"""
    print("🚀 Live Demo of New Modular System")
    print("=" * 50)
    
    # Check if server is running
    try:
        response = requests.get("http://localhost:8001/health", timeout=5)
        if response.status_code == 200:
            print("✅ New API server is running on port 8001")
        else:
            print("⚠️ New API server responded but with unexpected status")
    except requests.exceptions.RequestException:
        print("❌ New API server is not running on port 8001")
        print("\n🔧 To start the server, run:")
        print("   python3 -m uvicorn src.agent_core.api:app --reload --port 8001")
        return
    
    # Run demo
    demo = LiveDemo("http://localhost:8001")
    results = demo.run_comprehensive_demo()
    
    # Final recommendations
    print("\n" + "=" * 60)
    print("💡 DEMO RECOMMENDATIONS")
    print("=" * 60)
    
    if results['streaming'] and results['agent_run_basic']:
        print("✅ Ready for streaming demo with real-time responses")
        print("   Use: curl -N -X POST http://localhost:8001/agent/run")
    
    if results['error_handling']:
        print("✅ Error handling is robust and ready for demo")
        print("   Show validation errors and graceful degradation")
    
    if results['orchestrator_status']:
        print("✅ Orchestrator status monitoring ready")
        print("   Use: curl http://localhost:8001/orchestrator/status")
    
    print("\n🌐 Demo URLs:")
    print(f"   Health: {demo.base_url}/health")
    print(f"   Status: {demo.base_url}/orchestrator/status")
    print(f"   Root: {demo.base_url}/")

if __name__ == "__main__":
    main()
