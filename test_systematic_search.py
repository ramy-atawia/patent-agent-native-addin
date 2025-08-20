#!/usr/bin/env python3
"""
Systematic PatentsView API Search Testing
Testing different query strategies for "Dynamic spectrum sharing" patents
"""

import os
import json
import time
from typing import Dict, List, Any
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SystematicPatentsViewTester:
    def __init__(self):
        self.api_key = os.getenv('PATENTSVIEW_API_KEY')
        if not self.api_key:
            raise ValueError("PATENTSVIEW_API_KEY not found in environment")
        
        self.base_url = "https://search.patentsview.org"
        self.endpoint = "api/v1/patent"
        self.headers = {
            "X-Api-Key": self.api_key,
            "Content-Type": "application/json"
        }
        
    def _rate_limit(self):
        """Rate limiting for API calls"""
        time.sleep(1.5)
    
    def test_query_strategy(self, strategy_name: str, query: Dict, description: str) -> Dict[str, Any]:
        """Test a specific query strategy and return results"""
        print(f"\n{'='*60}")
        print(f"Testing: {strategy_name}")
        print(f"Description: {description}")
        print(f"Query: {json.dumps(query, indent=2)}")
        print(f"{'='*60}")
        
        self._rate_limit()
        
        try:
            payload = {
                "f": ["patent_id", "patent_title", "patent_abstract", "patent_date"],
                "o": {"size": 20},
                "q": query,
                "s": [{"patent_date": "desc"}]
            }
            
            response = httpx.post(
                f"{self.base_url}/{self.endpoint}",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if not data.get("error"):
                    patents = data.get("patents", [])
                    total_hits = data.get("total_hits", 0)
                    
                    print(f"✅ SUCCESS: Found {len(patents)} patents (total: {total_hits})")
                    
                    # Show first few results
                    for i, patent in enumerate(patents[:5]):
                        title = patent.get("patent_title", "No title")
                        abstract = patent.get("patent_abstract", "No abstract")
                        print(f"\n{i+1}. {patent.get('patent_id', 'No ID')}")
                        print(f"   Title: {title[:100]}{'...' if len(title) > 100 else ''}")
                        print(f"   Abstract: {abstract[:150]}{'...' if len(abstract) > 150 else ''}")
                    
                    return {
                        "success": True,
                        "total_hits": total_hits,
                        "patents": patents,
                        "query": query
                    }
                else:
                    print(f"❌ API Error: {data}")
                    return {"success": False, "error": "API returned error", "data": data}
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
                return {"success": False, "error": f"HTTP {response.status_code}", "response": response.text}
                
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def run_systematic_tests(self):
        """Run all systematic search strategies"""
        print("🚀 Starting Systematic PatentsView API Search Testing")
        print(f"Target Query: 'Dynamic spectrum sharing'")
        print(f"API Key: {self.api_key[:10]}...{self.api_key[-10:]}")
        
        # Strategy 1: Simple text search (baseline)
        strategies = [
            {
                "name": "Simple Text Search (Baseline)",
                "query": {"_text_any": {"patent_title": "Dynamic spectrum sharing"}},
                "description": "Basic text search across patent titles"
            },
            {
                "name": "AND Logic with _and operator",
                "query": {
                    "_and": [
                        {"_text_any": {"patent_title": "dynamic"}},
                        {"_text_any": {"patent_title": "spectrum"}},
                        {"_text_any": {"patent_title": "sharing"}}
                    ]
                },
                "description": "Using _and operator to require all three words"
            },
            {
                "name": "Phrase Search with _text_any",
                "query": {"_text_any": {"patent_title": "dynamic spectrum sharing"}},
                "description": "Exact phrase search in title"
            },
            {
                "name": "Abstract + Title Combined",
                "query": {
                    "_and": [
                        {"_text_any": {"patent_title": "spectrum"}},
                        {"_text_any": {"patent_abstract": "dynamic sharing"}}
                    ]
                },
                "description": "Spectrum in title AND dynamic sharing in abstract"
            },
            {
                "name": "Telecommunications Context",
                "query": {
                    "_and": [
                        {"_text_any": {"patent_title": "spectrum"}},
                        {"_text_any": {"patent_title": "sharing"}},
                        {"_text_any": {"patent_abstract": "telecommunications"}}
                    ]
                },
                "description": "Spectrum + sharing in title AND telecommunications in abstract"
            },
            {
                "name": "Wireless Communication Focus",
                "query": {
                    "_and": [
                        {"_text_any": {"patent_title": "spectrum"}},
                        {"_text_any": {"patent_title": "sharing"}},
                        {"_text_any": {"patent_abstract": "wireless"}}
                    ]
                },
                "description": "Spectrum + sharing in title AND wireless in abstract"
            },
            {
                "name": "Mobile Network Context",
                "query": {
                    "_and": [
                        {"_text_any": {"patent_title": "spectrum"}},
                        {"_text_any": {"patent_title": "sharing"}},
                        {"_text_any": {"patent_abstract": "mobile network"}}
                    ]
                },
                "description": "Spectrum + sharing in title AND mobile network in abstract"
            },
            {
                "name": "5G/6G Context",
                "query": {
                    "_and": [
                        {"_text_any": {"patent_title": "spectrum"}},
                        {"_text_any": {"patent_title": "sharing"}},
                        {"_text_any": {"patent_abstract": "5G"}}
                    ]
                },
                "description": "Spectrum + sharing in title AND 5G in abstract"
            },
            {
                "name": "Base Station Context",
                "query": {
                    "_and": [
                        {"_text_any": {"patent_title": "spectrum"}},
                        {"_text_any": {"patent_title": "sharing"}},
                        {"_text_any": {"patent_abstract": "base station"}}
                    ]
                },
                "description": "Spectrum + sharing in title AND base station in abstract"
            },
            {
                "name": "Radio Frequency Context",
                "query": {
                    "_and": [
                        {"_text_any": {"patent_title": "spectrum"}},
                        {"_text_any": {"patent_title": "sharing"}},
                        {"_text_any": {"patent_abstract": "radio frequency"}}
                    ]
                },
                "description": "Spectrum + sharing in title AND radio frequency in abstract"
            }
        ]
        
        results = []
        for strategy in strategies:
            result = self.test_query_strategy(
                strategy["name"], 
                strategy["query"], 
                strategy["description"]
            )
            results.append({
                "strategy": strategy["name"],
                "result": result
            })
            
            # Brief pause between tests
            time.sleep(0.5)
        
        # Summary report
        print(f"\n{'='*80}")
        print("📊 SYSTEMATIC SEARCH SUMMARY REPORT")
        print(f"{'='*80}")
        
        successful_strategies = [r for r in results if r["result"]["success"]]
        failed_strategies = [r for r in results if not r["result"]["success"]]
        
        print(f"✅ Successful Strategies: {len(successful_strategies)}")
        print(f"❌ Failed Strategies: {len(failed_strategies)}")
        
        if successful_strategies:
            print(f"\n🏆 BEST RESULTS:")
            for strategy in successful_strategies:
                result = strategy["result"]
                print(f"  • {strategy['strategy']}: {result['total_hits']} total hits")
        
        if failed_strategies:
            print(f"\n💥 FAILED STRATEGIES:")
            for strategy in failed_strategies:
                print(f"  • {strategy['strategy']}: {strategy['result']['error']}")
        
        return results

if __name__ == "__main__":
    try:
        tester = SystematicPatentsViewTester()
        results = tester.run_systematic_tests()
        
        # Save results to file
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"systematic_search_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\n💾 Results saved to: {filename}")
        
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        import traceback
        traceback.print_exc()
