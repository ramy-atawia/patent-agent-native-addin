#!/usr/bin/env python3
"""
Test different query strategies for "Dynamic spectrum sharing" 
to find the most effective PatentsView API approach
"""

import os
import sys
import time
import json
from pathlib import Path
from dotenv import load_dotenv
from typing import Dict, List, Any

# Load environment variables
load_dotenv()

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from prior_art_search import OptimizedPatentsViewAPI

class QueryStrategyTester:
    """Test different query strategies for spectrum sharing patents"""
    
    def __init__(self):
        self.api_client = OptimizedPatentsViewAPI()
        self.test_results = []
        
    def test_query_strategy(self, strategy_name: str, query_payload: Dict, description: str) -> Dict[str, Any]:
        """Test a specific query strategy"""
        print(f"\n{'='*60}")
        print(f"Testing: {strategy_name}")
        print(f"Description: {description}")
        print(f"{'='*60}")
        
        try:
            # Rate limit before request
            time.sleep(1.5)
            
            # Make the API call
            response = self.api_client.session.post(
                f"{self.api_client.base_url}/patent/",
                json=query_payload,
                headers={"Content-Type": "application/json", "X-Api-Key": self.api_client.api_key or ""}
            )
            
            if response.status_code == 200:
                data = response.json()
                patents = data.get("patents", [])
                total_hits = data.get("total_hits", 0)
                
                print(f"✅ Success! Found {len(patents)} patents, {total_hits} total matches")
                
                # Analyze results
                result_analysis = self.analyze_results(patents, strategy_name)
                
                return {
                    "strategy": strategy_name,
                    "success": True,
                    "patents_found": len(patents),
                    "total_hits": total_hits,
                    "query_payload": query_payload,
                    "results": patents[:3],  # First 3 for analysis
                    "analysis": result_analysis
                }
                
            else:
                print(f"❌ Failed with status {response.status_code}")
                return {
                    "strategy": strategy_name,
                    "success": False,
                    "error": f"HTTP {response.status_code}",
                    "query_payload": query_payload
                }
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return {
                "strategy": strategy_name,
                "success": False,
                "error": str(e),
                "query_payload": query_payload
            }
    
    def analyze_results(self, patents: List[Dict], strategy_name: str) -> Dict[str, Any]:
        """Analyze the relevance of returned patents"""
        if not patents:
            return {"relevance_score": 0, "relevant_count": 0, "notes": "No patents found"}
        
        relevant_keywords = [
            "spectrum", "sharing", "dynamic", "adaptive", "intelligent",
            "wireless", "communication", "network", "frequency", "bandwidth",
            "allocation", "management", "optimization", "efficiency"
        ]
        
        relevant_count = 0
        total_score = 0
        
        for patent in patents:
            title = patent.get("patent_title", "").lower()
            abstract = patent.get("patent_abstract", "").lower()
            combined_text = f"{title} {abstract}"
            
            # Count relevant keywords
            keyword_matches = sum(1 for keyword in relevant_keywords if keyword in combined_text)
            relevance_score = min(keyword_matches / len(relevant_keywords), 1.0)
            
            if relevance_score > 0.3:  # Threshold for relevance
                relevant_count += 1
            
            total_score += relevance_score
        
        avg_relevance = total_score / len(patents) if patents else 0
        
        return {
            "relevance_score": round(avg_relevance, 3),
            "relevant_count": relevant_count,
            "total_patents": len(patents),
            "notes": f"Found {relevant_count} relevant patents out of {len(patents)}"
        }
    
    def run_all_strategies(self):
        """Test all query strategies"""
        print("🚀 Testing Query Strategies for 'Dynamic Spectrum Sharing'")
        print("=" * 80)
        
        # Define all query strategies to test
        strategies = [
            {
                "name": "Simple Text Search",
                "payload": {
                    "f": ["patent_id", "patent_title", "patent_abstract", "inventors", "assignees"],
                    "o": {"size": 5},
                    "q": {"patent_title": "Dynamic spectrum sharing"}
                },
                "description": "Basic search on patent title only"
            },
            {
                "name": "Multiple Field Search",
                "payload": {
                    "f": ["patent_id", "patent_title", "patent_abstract", "inventors", "assignees"],
                    "o": {"size": 5},
                    "q": {
                        "_or": [
                            {"patent_title": "Dynamic spectrum sharing"},
                            {"patent_abstract": "Dynamic spectrum sharing"},
                            {"patent_title": "spectrum sharing"},
                            {"patent_abstract": "spectrum sharing"}
                        ]
                    }
                },
                "description": "Search across title and abstract with variations"
            },
            {
                "name": "Broader Telecommunications Search",
                "payload": {
                    "f": ["patent_id", "patent_title", "patent_abstract", "inventors", "assignees"],
                    "o": {"size": 5},
                    "q": {
                        "_and": [
                            {"_text_any": {"patent_title": "spectrum"}},
                            {"_text_any": {"patent_title": "sharing"}},
                            {"_or": [
                                {"patent_title": "dynamic"},
                                {"patent_title": "adaptive"},
                                {"patent_title": "intelligent"}
                            ]}
                        ]
                    }
                },
                "description": "Complex boolean logic with spectrum + sharing + dynamic/adaptive"
            },
            {
                "name": "Current Implementation (_text_any)",
                "payload": {
                    "f": ["patent_id", "patent_title", "patent_abstract", "inventors", "assignees"],
                    "o": {"size": 5},
                    "q": {
                        "_text_any": {
                            "patent_title": "Dynamic spectrum sharing"
                        }
                    }
                },
                "description": "Your current _text_any approach"
            },
            {
                "name": "Wildcard Search",
                "payload": {
                    "f": ["patent_id", "patent_title", "patent_abstract", "inventors", "assignees"],
                    "o": {"size": 5},
                    "q": {
                        "patent_title": {
                            "_wildcard": "*spectrum*sharing*"
                        }
                    }
                },
                "description": "Wildcard search for spectrum and sharing"
            },
            {
                "name": "Recent Patents Search",
                "payload": {
                    "f": ["patent_id", "patent_title", "patent_abstract", "inventors", "assignees"],
                    "o": {"size": 5},
                    "q": {
                        "_and": [
                            {"patent_year": {"_gte": "2015"}},
                            {"_text_any": {"patent_title": "spectrum sharing"}}
                        ]
                    }
                },
                "description": "Recent patents (2015+) with spectrum sharing"
            },
            {
                "name": "Simplified OR Search",
                "payload": {
                    "f": ["patent_id", "patent_title", "patent_abstract", "inventors", "assignees"],
                    "o": {"size": 5},
                    "q": {
                        "_or": [
                            {"patent_title": "spectrum sharing"},
                            {"patent_title": "dynamic spectrum"},
                            {"patent_title": "adaptive spectrum"}
                        ]
                    }
                },
                "description": "Simple OR logic for related terms"
            }
        ]
        
        # Test each strategy
        for strategy in strategies:
            result = self.test_query_strategy(
                strategy["name"], 
                strategy["payload"], 
                strategy["description"]
            )
            self.test_results.append(result)
            
            # Show sample results if successful
            if result.get("success") and result.get("results"):
                print(f"\n📋 Sample Results:")
                for i, patent in enumerate(result["results"][:2], 1):
                    title = patent.get("patent_title", "No title")[:80]
                    print(f"  {i}. {patent.get('patent_id', 'No ID')} - {title}...")
            
            print(f"\n📊 Analysis: {result.get('analysis', {}).get('notes', 'No analysis')}")
            
            # Wait between requests
            time.sleep(2)
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate comprehensive summary of all test results"""
        print(f"\n{'='*80}")
        print("📊 QUERY STRATEGY TEST SUMMARY")
        print(f"{'='*80}")
        
        successful_strategies = [r for r in self.test_results if r.get("success")]
        failed_strategies = [r for r in self.test_results if not r.get("success")]
        
        print(f"✅ Successful Strategies: {len(successful_strategies)}")
        print(f"❌ Failed Strategies: {len(failed_strategies)}")
        
        if successful_strategies:
            print(f"\n🏆 TOP PERFORMING STRATEGIES:")
            # Sort by relevance score
            sorted_strategies = sorted(
                successful_strategies, 
                key=lambda x: x.get("analysis", {}).get("relevance_score", 0), 
                reverse=True
            )
            
            for i, strategy in enumerate(sorted_strategies[:3], 1):
                analysis = strategy.get("analysis", {})
                print(f"\n{i}. {strategy['strategy']}")
                print(f"   📈 Relevance Score: {analysis.get('relevance_score', 0):.3f}")
                print(f"   🔍 Patents Found: {strategy.get('patents_found', 0)}")
                print(f"   🎯 Relevant Patents: {analysis.get('relevant_count', 0)}")
                print(f"   📝 Notes: {analysis.get('notes', 'No notes')}")
        
        if failed_strategies:
            print(f"\n❌ FAILED STRATEGIES:")
            for strategy in failed_strategies:
                print(f"   • {strategy['strategy']}: {strategy.get('error', 'Unknown error')}")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if successful_strategies:
            best_strategy = sorted_strategies[0]
            print(f"   1. Use '{best_strategy['strategy']}' as primary search method")
            print(f"   2. Consider '{sorted_strategies[1]['strategy']}' as backup")
            print(f"   3. Avoid failed strategies: {', '.join([s['strategy'] for s in failed_strategies])}")
        else:
            print("   No successful strategies found. Check API configuration and query syntax.")

def main():
    """Run the query strategy tests"""
    try:
        tester = QueryStrategyTester()
        tester.run_all_strategies()
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
