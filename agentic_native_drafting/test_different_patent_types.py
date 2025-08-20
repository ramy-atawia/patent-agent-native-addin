#!/usr/bin/env python3
"""
Test different patent types to find ones with available claims
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from prior_art_search import OptimizedPatentsViewAPI

def test_different_patent_types():
    """Test different patent types for claims availability"""
    print("🔍 Testing Different Patent Types for Claims")
    print("=" * 60)
    
    api_client = OptimizedPatentsViewAPI()
    
    # Test different search queries to find patents with claims
    test_queries = [
        "machine learning",
        "artificial intelligence", 
        "wireless communication",
        "5G network",
        "blockchain",
        "quantum computing"
    ]
    
    results_summary = {}
    
    for query in test_queries:
        print(f"\n🧪 Testing: '{query}'")
        print("-" * 40)
        
        try:
            # Search for patents
            patents = api_client.search_patents(query, max_results=3)
            
            if not patents:
                print(f"❌ No patents found for '{query}'")
                results_summary[query] = {"found": 0, "with_claims": 0}
                continue
            
            print(f"✅ Found {len(patents)} patents")
            
            patents_with_claims = 0
            
            for i, patent in enumerate(patents, 1):
                patent_id = patent.get("patent_id", "")
                title = patent.get("patent_title", "No title")[:60]
                
                print(f"  {i}. Testing {patent_id}: {title}...")
                
                # Get claims for this patent
                claims = api_client.get_patent_claims(patent_id)
                
                if claims:
                    print(f"     ✅ Has {len(claims)} claims")
                    patents_with_claims += 1
                else:
                    print(f"     ❌ No claims")
                
                # Rate limiting between requests
                if i < len(patents):
                    import time
                    time.sleep(1.5)
            
            results_summary[query] = {
                "found": len(patents),
                "with_claims": patents_with_claims
            }
            
        except Exception as e:
            print(f"❌ Test failed: {e}")
            results_summary[query] = {"found": 0, "with_claims": 0, "error": str(e)}
    
    # Summary
    print(f"\n{'='*60}")
    print("📊 CLAIMS AVAILABILITY BY PATENT TYPE")
    print(f"{'='*60}")
    
    for query, result in results_summary.items():
        if "error" in result:
            print(f"❌ {query}: {result['error']}")
        else:
            success_rate = (result['with_claims'] / result['found'] * 100) if result['found'] > 0 else 0
            print(f"✅ {query}: {result['with_claims']}/{result['found']} patents have claims ({success_rate:.1f}%)")
    
    # Find best performing query
    best_query = None
    best_rate = 0
    
    for query, result in results_summary.items():
        if "error" not in result and result['found'] > 0:
            rate = result['with_claims'] / result['found']
            if rate > best_rate:
                best_rate = rate
                best_query = query
    
    if best_query:
        print(f"\n🏆 BEST PERFORMING QUERY: '{best_query}' ({best_rate*100:.1f}% success rate)")
        
        # Test the best query with more patents
        print(f"\n🧪 DETAILED TEST OF BEST QUERY: '{best_query}'")
        print("-" * 50)
        
        try:
            best_patents = api_client.search_patents(best_query, max_results=5)
            
            if best_patents:
                print(f"Testing {len(best_patents)} patents from best query...")
                
                for i, patent in enumerate(best_patents, 1):
                    patent_id = patent.get("patent_id", "")
                    title = patent.get("patent_title", "No title")[:80]
                    
                    print(f"\n  {i}. {patent_id}: {title}...")
                    
                    claims = api_client.get_patent_claims(patent_id)
                    
                    if claims:
                        print(f"     ✅ Claims: {len(claims)} found")
                        # Show first claim
                        first_claim = claims[0][:150] + "..." if len(claims[0]) > 150 else claims[0]
                        print(f"     📝 First claim: {first_claim}")
                    else:
                        print(f"     ❌ No claims")
                    
                    if i < len(best_patents):
                        import time
                        time.sleep(1.5)
        
        except Exception as e:
            print(f"❌ Detailed test failed: {e}")

def main():
    """Run the different patent types test"""
    test_different_patent_types()
    print(f"\n{'='*60}")
    print("🎯 DIFFERENT PATENT TYPES TEST COMPLETE")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
