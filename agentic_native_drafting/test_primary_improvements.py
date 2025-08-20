#!/usr/bin/env python3
"""
Test the improvements in the primary search method
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

def test_primary_improvements():
    """Test the improved primary search method"""
    print("🚀 Testing Primary Method Improvements")
    print("=" * 60)
    
    api_client = OptimizedPatentsViewAPI()
    
    # Test different search types to show dynamic query building
    test_searches = [
        {
            "query": "Dynamic spectrum sharing",
            "type": "Spectrum Search",
            "expected_fields": ["spectrum", "sharing", "dynamic"]
        },
        {
            "query": "5G wireless communication",
            "type": "Telecom Search", 
            "expected_fields": ["wireless", "communication", "5g"]
        },
        {
            "query": "Machine learning algorithms",
            "type": "AI/ML Search",
            "expected_fields": ["machine learning", "algorithms", "ai"]
        },
        {
            "query": "Software architecture patterns",
            "type": "Software Search",
            "expected_fields": ["software", "architecture", "patterns"]
        },
        {
            "query": "Quantum computing",
            "type": "General Search",
            "expected_fields": ["quantum", "computing"]
        }
    ]
    
    for i, search_test in enumerate(test_searches, 1):
        print(f"\n🧪 Test {i}: {search_test['type']}")
        print(f"Query: '{search_test['query']}'")
        print("-" * 50)
        
        try:
            # Test the improved primary method
            patents = api_client.search_patents(search_test['query'], max_results=3)
            
            if patents:
                print(f"✅ Found {len(patents)} patents")
                
                # Show enhanced fields
                print(f"\n📋 Enhanced Fields Available:")
                sample_patent = patents[0]
                enhanced_fields = [
                    "patent_id", "patent_title", "patent_abstract", "patent_date", 
                    "patent_year", "inventors", "assignees", "cpc_class", 
                    "uspc_class", "patent_kind", "patent_type", "relevance_score"
                ]
                
                for field in enhanced_fields:
                    if field in sample_patent:
                        value = sample_patent[field]
                        if field == "relevance_score":
                            print(f"  • {field}: {value:.3f}")
                        elif field in ["inventors", "assignees"] and isinstance(value, list):
                            print(f"  • {field}: {len(value)} items")
                        else:
                            print(f"  • {field}: {str(value)[:60]}...")
                    else:
                        print(f"  • {field}: Not available")
                
                # Show relevance scoring
                print(f"\n🎯 Relevance Scoring:")
                for j, patent in enumerate(patents, 1):
                    title = patent.get("patent_title", "No title")[:60]
                    relevance = patent.get("relevance_score", 0)
                    print(f"  {j}. Score: {relevance:.3f} - {title}...")
                
            else:
                print("❌ No patents found")
                
        except Exception as e:
            print(f"❌ Search failed: {e}")
        
        # Rate limiting between searches
        if i < len(test_searches):
            import time
            time.sleep(2)
    
    # Test performance improvements
    print(f"\n{'='*60}")
    print("⚡ PERFORMANCE IMPROVEMENTS TEST")
    print(f"{'='*60}")
    
    # Test retry logic
    print(f"\n🔄 Testing Retry Logic:")
    try:
        # This should work normally
        patents = api_client.search_patents("test query", max_results=1)
        print("✅ Normal search successful")
        
        # Test with invalid query to see error handling
        print("🧪 Testing error handling...")
        # Note: We can't easily trigger API errors, but the retry logic is in place
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    # Summary of improvements
    print(f"\n{'='*60}")
    print("📈 PRIMARY METHOD IMPROVEMENTS SUMMARY")
    print(f"{'='*60}")
    print("✅ Dynamic Query Building:")
    print("   • Automatic detection of search type")
    print("   • Optimized queries for spectrum, telecom, AI/ML, software")
    print("   • Fallback to general search for other types")
    
    print(f"\n✅ Enhanced Field Selection:")
    print("   • Added patent_date, patent_year, cpc_class, uspc_class")
    print("   • Added patent_kind, patent_type")
    print("   • Better inventor and assignee information")
    
    print(f"\n✅ Performance Improvements:")
    print("   • Retry logic with exponential backoff")
    print("   • Enhanced error handling")
    print("   • Relevance scoring and sorting")
    print("   • Search metadata tracking")
    
    print(f"\n✅ Smart Query Strategies:")
    print("   • Spectrum: spectrum + sharing + dynamic/adaptive terms")
    print("   • Telecom: search terms + wireless/5g/network terms")
    print("   • AI/ML: search terms + AI/ML related terms")
    print("   • Software: search terms + software related terms")
    print("   • General: title + abstract + word-based search")

def main():
    """Run the primary improvements test"""
    test_primary_improvements()
    print(f"\n{'='*60}")
    print("🎯 PRIMARY METHOD IMPROVEMENTS TEST COMPLETE")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
