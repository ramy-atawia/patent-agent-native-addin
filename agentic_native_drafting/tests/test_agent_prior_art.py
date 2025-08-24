#!/usr/bin/env python3
"""
Test Agent Prior Art Search Integration
Tests the full agent workflow via HTTP requests to the backend for prior art search functionality.
"""

import asyncio
import httpx
import json
import time
import os
from datetime import datetime
from pathlib import Path

# Test configuration
BACKEND_URL = "http://localhost:8000"  # Default backend URL
TEST_QUERIES = [
    "i need prior art search for 5G dynamic spectrum sharing",
    "i need prior art search for AI for carrier aggregation"
]

class AgentPriorArtTester:
    """Test class for agent prior art search functionality"""
    
    def __init__(self, backend_url: str = BACKEND_URL):
        self.backend_url = backend_url.rstrip('/')
        self.session_id = None
        self.test_results = []
        
        # Create reports directory
        self.reports_dir = Path("test_reports")
        self.reports_dir.mkdir(exist_ok=True)
        
    async def test_backend_health(self) -> bool:
        """Test if backend is available"""
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{self.backend_url}/")
                if response.status_code == 200:
                    print("✅ Backend is healthy and accessible")
                    return True
                else:
                    print(f"⚠️ Backend returned status {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Backend not accessible: {e}")
            print("💡 Make sure the backend is running with: `python -m uvicorn main:app --reload --port 8000`")
            return False
    
    async def start_session(self) -> str:
        """Start a new agent session - for patent API we'll generate our own session ID"""
        try:
            # For the patent API, we generate our own session ID
            session_id = f"test_session_{int(time.time())}"
            print(f"✅ Generated session ID: {session_id}")
            return session_id
        except Exception as e:
            print(f"❌ Session creation failed: {e}")
            return None
    
    async def send_message_via_patent_api(self, message: str) -> dict:
        """Send a message via the patent drafting API which should route to agent"""
        try:
            print(f"\n📤 Sending via patent API: '{message}'")
            
            payload = {
                "user_message": message,
                "disclosure": message,  # Also include as disclosure
                "session_id": self.session_id
            }
            
            async with httpx.AsyncClient(timeout=300.0) as client:  # 5 min timeout for patent search
                response = await client.post(
                    f"{self.backend_url}/api/patent/run",
                    json=payload,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    print(f"📥 Patent API response received - Run ID: {data.get('run_id')}")
                    
                    # Now stream the results to get the actual patent report
                    run_id = data.get('run_id')
                    if run_id:
                        stream_response = await self.get_streaming_results(run_id)
                        return {
                            "success": True,
                            "response": stream_response.get("final_response", ""),
                            "data": {**data, **stream_response},
                            "timestamp": datetime.now().isoformat()
                        }
                    else:
                        return {
                            "success": True,
                            "response": data,
                            "data": data,
                            "timestamp": datetime.now().isoformat()
                        }
                else:
                    print(f"❌ Patent API request failed: {response.status_code}")
                    print(f"Response: {response.text}")
                    return {
                        "success": False,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "timestamp": datetime.now().isoformat()
                    }
                    
        except Exception as e:
            print(f"❌ Patent API request failed: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def get_streaming_results(self, run_id: str) -> dict:
        """Get the streaming results from a run"""
        try:
            print(f"🔄 Streaming results for run {run_id}...")
            
            async with httpx.AsyncClient(timeout=300.0) as client:
                async with client.stream(
                    'GET',
                    f"{self.backend_url}/api/patent/stream?run_id={run_id}",
                    headers={"Accept": "text/event-stream"}
                ) as response:
                    if response.status_code != 200:
                        return {"error": f"Stream failed: {response.status_code}"}
                    
                    events_received = 0
                    final_response = ""
                    all_events = []
                    debug_events = []  # For debugging
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            try:
                                event_data = json.loads(line[6:])  # Remove "data: " prefix
                                events_received += 1
                                all_events.append(event_data)
                                debug_events.append(event_data)  # Store for debugging
                                
                                event_type = event_data.get("type", event_data.get("event_type", "unknown"))
                                print(f"📨 Event {events_received}: {event_type}")
                                
                                # Look for the final response in completion events
                                if event_type in ["complete", "completion", "results", "RESULTS", "COMPLETION"]:
                                    response_content = event_data.get("response", event_data.get("data", {}).get("response", ""))
                                    if response_content and len(response_content) > len(final_response):
                                        final_response = response_content
                                        print(f"🎯 Found final response: {len(response_content)} characters")
                                        
                                # Also check for any response content in any event type
                                elif "response" in event_data:
                                    response_content = event_data.get("response", "")
                                    if response_content and len(response_content) > len(final_response):
                                        final_response = response_content
                                        print(f"📄 Found response content: {len(response_content)} characters")
                                        
                            except json.JSONDecodeError as e:
                                print(f"⚠️ Failed to parse event: {e}")
                                continue
                    
                    print(f"✅ Streaming completed - {events_received} events received")
                    print(f"📄 Final response length: {len(final_response)} characters")
                    
                    # Debug: Print first few events to see structure
                    if debug_events and len(final_response) == 0:
                        print("🔍 DEBUG: First few events:")
                        for i, event in enumerate(debug_events[:3]):
                            print(f"   Event {i+1}: {json.dumps(event, indent=2)[:200]}...")
                    
                    return {
                        "final_response": final_response,
                        "events_received": events_received,
                        "all_events": all_events,
                        "debug_events": debug_events[:5] if len(final_response) == 0 else []  # Include debug info if no response
                    }
                    
        except Exception as e:
            print(f"❌ Streaming failed: {e}")
            return {"error": str(e)}
    
    async def save_report(self, query: str, response_data: dict, test_index: int) -> str:
        """Save the patent report to a file"""
        try:
            # Create filename from query
            safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_query = safe_query.replace(' ', '_')[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"prior_art_report_{test_index}_{safe_query}_{timestamp}.md"
            filepath = self.reports_dir / filename
            
            # Extract the actual patent report content from streaming response
            final_response = response_data.get("response", "")
            events_received = response_data.get("data", {}).get("events_received", 0)
            
            # Create comprehensive report file
            report_content = f"""# Prior Art Search Test Report

## Test Information
- **Query**: {query}
- **Test Index**: {test_index}
- **Timestamp**: {response_data.get('timestamp', 'Unknown')}
- **Session ID**: {self.session_id}
- **Backend URL**: {self.backend_url}
- **Events Received**: {events_received}

## Agent Prior Art Search Results

{final_response if final_response else "No final response received from agent"}

## Raw Response Metadata
```json
{json.dumps({k: v for k, v in response_data.get('data', {}).items() if k != 'all_events'}, indent=2)}
```

---
Generated by Agent Prior Art Tester
"""
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"💾 Report saved: {filepath}")
            print(f"📄 Report content length: {len(final_response)} characters")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
            return None
    
    async def run_test_queries(self) -> list:
        """Run all test queries and collect results"""
        print(f"\n🧪 Running {len(TEST_QUERIES)} test queries...")
        
        for i, query in enumerate(TEST_QUERIES, 1):
            print(f"\n{'='*60}")
            print(f"🔍 TEST {i}/{len(TEST_QUERIES)}: {query}")
            print(f"{'='*60}")
            
            start_time = time.time()
            
            # Send query to agent via patent API
            result = await self.send_message_via_patent_api(query)
            
            end_time = time.time()
            duration = end_time - start_time
            
            # Add timing and test info
            result["query"] = query
            result["test_index"] = i
            result["duration_seconds"] = duration
            
            print(f"⏱️ Query completed in {duration:.1f} seconds")
            
            # Save report if successful
            if result["success"]:
                report_path = await self.save_report(query, result, i)
                result["report_path"] = report_path
                print(f"✅ Test {i} completed successfully")
            else:
                print(f"❌ Test {i} failed")
            
            self.test_results.append(result)
            
            # Brief pause between tests
            if i < len(TEST_QUERIES):
                print("\n⏳ Waiting 5 seconds before next test...")
                await asyncio.sleep(5)
        
        return self.test_results
    
    async def generate_summary_report(self):
        """Generate a summary report of all tests"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_file = self.reports_dir / f"test_summary_{timestamp}.md"
            
            successful_tests = [r for r in self.test_results if r["success"]]
            failed_tests = [r for r in self.test_results if not r["success"]]
            
            summary_content = f"""# Agent Prior Art Search Test Summary

## Overview
- **Total Tests**: {len(self.test_results)}
- **Successful**: {len(successful_tests)}
- **Failed**: {len(failed_tests)}
- **Success Rate**: {len(successful_tests)/len(self.test_results)*100:.1f}%
- **Test Date**: {datetime.now().isoformat()}
- **Backend URL**: {self.backend_url}
- **Session ID**: {self.session_id}

## Test Results

"""
            
            for i, result in enumerate(self.test_results, 1):
                status = "✅ PASSED" if result["success"] else "❌ FAILED"
                duration = result.get("duration_seconds", 0)
                
                summary_content += f"""### Test {i}: {status}
- **Query**: {result["query"]}
- **Duration**: {duration:.1f} seconds
- **Report Path**: {result.get("report_path", "Not saved")}
"""
                
                if not result["success"]:
                    summary_content += f"- **Error**: {result.get('error', 'Unknown error')}\n"
                
                summary_content += "\n"
            
            # Add failed tests details
            if failed_tests:
                summary_content += "## Failed Test Details\n\n"
                for i, result in enumerate(failed_tests, 1):
                    summary_content += f"""### Failed Test {i}
- **Query**: {result["query"]}
- **Error**: {result.get("error", "Unknown error")}
- **Timestamp**: {result.get("timestamp", "Unknown")}

"""
            
            summary_content += """
## Notes
- Reports are saved in the `test_reports/` directory
- Each test includes the full agent response and raw data
- Backend must be running for tests to pass

---
Generated by Agent Prior Art Tester
"""
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            print(f"\n📊 Summary report saved: {summary_file}")
            
        except Exception as e:
            print(f"❌ Failed to generate summary: {e}")
    
    async def run_full_test(self):
        """Run the complete test suite"""
        print("🚀 Starting Agent Prior Art Search Integration Test")
        print(f"🎯 Backend URL: {self.backend_url}")
        print(f"📝 Test Queries: {len(TEST_QUERIES)}")
        
        # 1. Check backend health
        if not await self.test_backend_health():
            print("❌ Cannot continue without backend access")
            return False
        
        # 2. Start session
        self.session_id = await self.start_session()
        if not self.session_id:
            print("❌ Cannot continue without session")
            return False
        
        # 3. Run test queries
        results = await self.run_test_queries()
        
        # 4. Generate summary
        await self.generate_summary_report()
        
        # 5. Print final results
        successful = len([r for r in results if r["success"]])
        total = len(results)
        
        print(f"\n{'='*60}")
        print("🏁 TEST SUITE COMPLETED")
        print(f"{'='*60}")
        print(f"✅ Successful: {successful}/{total}")
        print(f"❌ Failed: {total-successful}/{total}")
        print(f"📊 Success Rate: {successful/total*100:.1f}%")
        print(f"📁 Reports Directory: {self.reports_dir.absolute()}")
        
        return successful == total

async def main():
    """Main test function"""
    # Check if custom backend URL provided
    backend_url = os.getenv("BACKEND_URL", BACKEND_URL)
    
    print(f"Agent Prior Art Search Integration Test")
    print(f"Backend URL: {backend_url}")
    
    tester = AgentPriorArtTester(backend_url)
    success = await tester.run_full_test()
    
    if success:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n💥 Some tests failed!")
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        exit(exit_code)
    except KeyboardInterrupt:
        print("\n⛔ Test interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n💥 Test suite failed with error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
