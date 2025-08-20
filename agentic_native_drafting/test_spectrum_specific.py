#!/usr/bin/env python3
"""
Test the new spectrum-specific search capabilities
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

from prior_art_search import OptimizedPatentsViewAPI, search_prior_art_optimized

def test_spectrum_search():
    """Test the new spectrum search capabilities"""
    print("🔍 Testing New Spectrum Search Capabilities")
    print("=" * 60)
    
    api_client = OptimizedPatentsViewAPI()
    
    # Test 1: Direct spectrum search method
    print("\n🧪 Test 1: Direct Spectrum Search Method")
    print("-" * 40)
    
    try:
        spectrum_patents = api_client.search_spectrum_patents("Dynamic spectrum sharing", max_results=5)
        print(f"✅ Found {len(spectrum_patents)} spectrum patents")
        
        if spectrum_patents:
            print("\n📋 Sample Spectrum Patents:")
            for i, patent in enumerate(spectrum_patents[:3], 1):
                title = patent.get("patent_title", "No title")[:80]
                print(f"  {i}. {patent.get('patent_id', 'No ID')} - {title}...")
        else:
            print("❌ No spectrum patents found")
            
    except Exception as e:
        print(f"❌ Spectrum search failed: {e}")
    
    # Test 2: Advanced search with auto-detection
    print("\n🧪 Test 2: Advanced Search with Auto-Detection")
    print("-" * 40)
    
    try:
        advanced_patents = api_client.search_patents_advanced("Dynamic spectrum sharing", max_results=5)
        print(f"✅ Found {len(advanced_patents)} patents with advanced search")
        
        if advanced_patents:
            print("\n📋 Sample Advanced Search Results:")
            for i, patent in enumerate(advanced_patents[:3], 1):
                title = patent.get("patent_title", "No title")[:80]
                print(f"  {i}. {patent.get('patent_id', 'No ID')} - {title}...")
        else:
            print("❌ No patents found with advanced search")
            
    except Exception as e:
        print(f"❌ Advanced search failed: {e}")
    
    # Test 3: Full optimized search with claims
    print("\n🧪 Test 3: Full Optimized Search with Claims")
    print("-" * 40)
    
    try:
        result = search_prior_art_optimized("Dynamic spectrum sharing", max_results=3)
        print(f"✅ Found {result.total_found} patents with full search")
        
        if result.patents:
            print("\n📋 Full Search Results:")
            for i, patent in enumerate(result.patents, 1):
                print(f"\n  {i}. {patent.patent_id} - {patent.title[:60]}...")
                print(f"     Relevance: {patent.relevance_score:.2f}")
                print(f"     Claims: {len(patent.claims)} found")
                print(f"     Inventors: {', '.join(patent.inventors[:2])}...")
        else:
            print("❌ No patents found with full search")
            
    except Exception as e:
        print(f"❌ Full search failed: {e}")
    
    # Test 4: Compare with old method
    print("\n🧪 Test 4: Compare with Old Search Method")
    print("-" * 40)
    
    try:
        old_patents = api_client.search_patents("Dynamic spectrum sharing", max_results=5)
        print(f"✅ Old method found {len(old_patents)} patents")
        
        if old_patents:
            print("\n📋 Old Method Results:")
            for i, patent in enumerate(old_patents[:3], 1):
                title = patent.get("patent_title", "No title")[:80]
                print(f"  {i}. {patent.get('patent_id', 'No ID')} - {title}...")
        else:
            print("❌ Old method found no patents")
            
    except Exception as e:
        print(f"❌ Old method failed: {e}")

def main():
    """Run the spectrum search tests"""
    test_spectrum_search()
    print(f"\n{'='*60}")
    print("🎯 SPECTRUM SEARCH TEST COMPLETE")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
