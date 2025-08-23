#!/usr/bin/env python3
"""
Direct Prior Art API Test
Tests the simplified prior art search directly via the /api/prior-art/search endpoint.
"""

import asyncio
import httpx
import json
import time
import os
from datetime import datetime
from pathlib import Path

# Test configuration
BACKEND_URL = "http://localhost:8000"
TEST_QUERIES = [
    "5G dynamic spectrum sharing",
    "AI for carrier aggregation"
]

class DirectPriorArtTester:
    """Test class for direct prior art API testing"""
    
    def __init__(self, backend_url: str = BACKEND_URL):
        self.backend_url = backend_url.rstrip('/')
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
                    data = response.json()
                    print("✅ Backend is healthy and accessible")
                    print(f"🔧 Service: {data.get('service', 'Unknown')}")
                    print(f"📋 Features: {', '.join(data.get('features', []))}")
                    return True
                else:
                    print(f"⚠️ Backend returned status {response.status_code}")
                    return False
        except Exception as e:
            print(f"❌ Backend not accessible: {e}")
            print("💡 Make sure the backend is running with:")
            print("   cd /Users/Mariam/agentic-native-drafting/agentic_native_drafting")
            print("   python -m uvicorn src.main:app --reload --port 8000")
            return False
    
    async def search_prior_art(self, query: str, max_results: int = 20) -> dict:
        """Call the direct prior art search API"""
        try:
            print(f"\n🔍 Searching: '{query}'")
            print(f"📊 Max results: {max_results}")
            
            params = {
                "query": query,
                "max_results": max_results
            }
            
            start_time = time.time()
            
            async with httpx.AsyncClient(timeout=300.0) as client:  # 5 min timeout
                response = await client.get(
                    f"{self.backend_url}/api/prior-art/search",
                    params=params
                )
                
                end_time = time.time()
                duration = end_time - start_time
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Extract key information
                    total_results = data.get("total_results", 0)
                    report = data.get("report", "")
                    results = data.get("results", [])
                    
                    print(f"✅ Search completed in {duration:.1f} seconds")
                    print(f"📈 Found {total_results} patents")
                    print(f"📄 Report length: {len(report)} characters")
                    
                    return {
                        "success": True,
                        "query": query,
                        "duration_seconds": duration,
                        "total_results": total_results,
                        "report": report,
                        "results": results,
                        "timestamp": datetime.now().isoformat(),
                        "raw_response": data
                    }
                else:
                    print(f"❌ Search failed with status {response.status_code}")
                    print(f"Response: {response.text}")
                    return {
                        "success": False,
                        "query": query,
                        "duration_seconds": duration,
                        "error": f"HTTP {response.status_code}: {response.text}",
                        "timestamp": datetime.now().isoformat()
                    }
                    
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return {
                "success": False,
                "query": query,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    async def save_report(self, result: dict, test_index: int) -> str:
        """Save the patent report to a file"""
        try:
            query = result["query"]
            
            # Create filename from query
            safe_query = "".join(c for c in query if c.isalnum() or c in (' ', '-', '_')).rstrip()
            safe_query = safe_query.replace(' ', '_')[:50]
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"direct_api_report_{test_index}_{safe_query}_{timestamp}.md"
            filepath = self.reports_dir / filename
            
            # Extract report content
            report = result.get("report", "No report generated")
            
            # Create comprehensive report file
            report_content = f"""# Direct Prior Art API Test Report

## Test Information
- **Query**: {query}
- **Test Index**: {test_index}
- **Timestamp**: {result.get('timestamp', 'Unknown')}
- **Duration**: {result.get('duration_seconds', 0):.1f} seconds
- **Total Results**: {result.get('total_results', 0)}
- **Backend URL**: {self.backend_url}

## Search Results Summary
{f"Found {result.get('total_results', 0)} relevant patents" if result.get('success') else f"Search failed: {result.get('error', 'Unknown error')}"}

## Patent Analysis Report
{report}

## Raw API Response
```json
{json.dumps(result.get('raw_response', {}), indent=2)}
```

---
Generated by Direct Prior Art API Tester
"""
            
            # Write to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            print(f"💾 Report saved: {filepath}")
            return str(filepath)
            
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
            return None
    
    async def run_all_tests(self) -> list:
        """Run all test queries"""
        print(f"\n🧪 Running {len(TEST_QUERIES)} direct API tests...")
        
        for i, query in enumerate(TEST_QUERIES, 1):
            print(f"\n{'='*60}")
            print(f"🔍 TEST {i}/{len(TEST_QUERIES)}: {query}")
            print(f"{'='*60}")
            
            # Run search
            result = await self.search_prior_art(query)
            result["test_index"] = i
            
            # Save report if successful
            if result["success"]:
                report_path = await self.save_report(result, i)
                result["report_path"] = report_path
                print(f"✅ Test {i} completed successfully")
            else:
                print(f"❌ Test {i} failed")
            
            self.test_results.append(result)
            
            # Brief pause between tests
            if i < len(TEST_QUERIES) - 1:
                print("\n⏳ Waiting 10 seconds before next test...")
                await asyncio.sleep(10)
        
        return self.test_results
    
    async def generate_summary_report(self):
        """Generate a summary report of all tests"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            summary_file = self.reports_dir / f"direct_api_summary_{timestamp}.md"
            
            successful_tests = [r for r in self.test_results if r["success"]]
            failed_tests = [r for r in self.test_results if not r["success"]]
            
            # Calculate average duration for successful tests
            avg_duration = 0
            if successful_tests:
                avg_duration = sum(r.get("duration_seconds", 0) for r in successful_tests) / len(successful_tests)
            
            summary_content = f"""# Direct Prior Art API Test Summary

## Overview
- **Total Tests**: {len(self.test_results)}
- **Successful**: {len(successful_tests)}
- **Failed**: {len(failed_tests)}
- **Success Rate**: {len(successful_tests)/len(self.test_results)*100:.1f}%
- **Average Duration**: {avg_duration:.1f} seconds
- **Test Date**: {datetime.now().isoformat()}
- **Backend URL**: {self.backend_url}

## Test Results

"""
            
            for i, result in enumerate(self.test_results, 1):
                status = "✅ PASSED" if result["success"] else "❌ FAILED"
                duration = result.get("duration_seconds", 0)
                total_results = result.get("total_results", 0)
                
                summary_content += f"""### Test {i}: {status}
- **Query**: {result["query"]}
- **Duration**: {duration:.1f} seconds
- **Patents Found**: {total_results}
- **Report Path**: {result.get("report_path", "Not saved")}
"""
                
                if not result["success"]:
                    summary_content += f"- **Error**: {result.get('error', 'Unknown error')}\n"
                
                summary_content += "\n"
            
            # Add performance analysis
            if successful_tests:
                summary_content += "## Performance Analysis\n\n"
                durations = [r.get("duration_seconds", 0) for r in successful_tests]
                patent_counts = [r.get("total_results", 0) for r in successful_tests]
                
                summary_content += f"- **Fastest Search**: {min(durations):.1f} seconds\n"
                summary_content += f"- **Slowest Search**: {max(durations):.1f} seconds\n"
                summary_content += f"- **Total Patents Found**: {sum(patent_counts)}\n"
                summary_content += f"- **Average Patents per Query**: {sum(patent_counts)/len(patent_counts):.1f}\n\n"
            
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
## API Endpoint Used
`GET /api/prior-art/search?query={query}&max_results={max_results}`

## Notes
- Reports are saved in the `test_reports/` directory
- Each test includes the full patent analysis report
- Backend must be running for tests to pass
- Tests use the simplified patent search engine

---
Generated by Direct Prior Art API Tester
"""
            
            with open(summary_file, 'w', encoding='utf-8') as f:
                f.write(summary_content)
            
            print(f"\n📊 Summary report saved: {summary_file}")
            
        except Exception as e:
            print(f"❌ Failed to generate summary: {e}")
    
    async def run_full_test(self):
        """Run the complete test suite"""
        print("🚀 Starting Direct Prior Art API Test Suite")
        print(f"🎯 Backend URL: {self.backend_url}")
        print(f"📝 Test Queries: {len(TEST_QUERIES)}")
        
        # 1. Check backend health
        if not await self.test_backend_health():
            print("❌ Cannot continue without backend access")
            return False
        
        # 2. Run all tests
        results = await self.run_all_tests()
        
        # 3. Generate summary
        await self.generate_summary_report()
        
        # 4. Print final results
        successful = len([r for r in results if r["success"]])
        total = len(results)
        total_patents = sum(r.get("total_results", 0) for r in results if r["success"])
        
        print(f"\n{'='*60}")
        print("🏁 DIRECT API TEST SUITE COMPLETED")
        print(f"{'='*60}")
        print(f"✅ Successful: {successful}/{total}")
        print(f"❌ Failed: {total-successful}/{total}")
        print(f"📊 Success Rate: {successful/total*100:.1f}%")
        print(f"🎯 Total Patents Found: {total_patents}")
        print(f"📁 Reports Directory: {self.reports_dir.absolute()}")
        
        return successful == total

async def main():
    """Main test function"""
    # Check if custom backend URL provided
    backend_url = os.getenv("BACKEND_URL", BACKEND_URL)
    
    print(f"Direct Prior Art API Test Suite")
    print(f"Backend URL: {backend_url}")
    
    tester = DirectPriorArtTester(backend_url)
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
