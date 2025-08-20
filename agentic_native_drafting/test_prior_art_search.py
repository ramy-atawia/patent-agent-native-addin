#!/usr/bin/env python3
"""
Test script for the optimized prior art search module
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

def test_optimized_module():
    """Test the optimized prior art search module"""
    print("Testing Optimized Prior Art Search Module")
    print("=" * 60)
    
    try:
        from prior_art_search import search_patents, search_prior_art_optimized
        print("✓ Successfully imported optimized module")
    except ImportError as e:
        print(f"✗ Failed to import: {e}")
        return
    
    # Test 1: Simple search function
    print(f"\n" + "="*40)
    print("TEST 1: SIMPLE SEARCH FUNCTION")
    print("="*40)
    
    search_query = "machine learning"
    print(f"Searching for: '{search_query}'")
    
    try:
        result = search_patents(search_query, max_results=3)
        print("✓ Optimized search completed successfully!")
        print(f"\nResults:\n{result}")
        
    except Exception as e:
        print(f"✗ Optimized search failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Detailed search function
    print(f"\n" + "="*40)
    print("TEST 2: DETAILED SEARCH FUNCTION")
    print("="*40)
    
    search_query2 = "artificial intelligence"
    print(f"Searching for: '{search_query2}'")
    
    try:
        result = search_prior_art_optimized(search_query2, max_results=2)
        print("✓ Detailed optimized search completed successfully!")
        print(f"  Query: {result.query}")
        print(f"  Patents found: {result.total_found}")
        print(f"  Timestamp: {result.timestamp}")
        
        if result.patents:
            print(f"\nPatent Details:")
            for i, patent in enumerate(result.patents, 1):
                print(f"\n  {i}. {patent.patent_id}")
                print(f"     Title: {patent.title[:60]}...")
                print(f"     Relevance: {patent.relevance_score:.2f}")
                print(f"     Inventors: {', '.join(patent.inventors[:3])}...")
                print(f"     Assignees: {', '.join(patent.assignees[:2])}...")
        
    except Exception as e:
        print(f"✗ Detailed optimized search failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run the test"""
    test_optimized_module()
    print(f"\n" + "="*60)
    print("OPTIMIZED MODULE TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    main()
