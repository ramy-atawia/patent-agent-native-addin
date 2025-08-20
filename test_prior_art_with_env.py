#!/usr/bin/env python3
"""
Test prior art search with proper environment loading
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from prior_art_search import PatentsViewAPI

def test_with_real_api():
    """Test with the real API key"""
    print("Testing Prior Art Search with Real API Key...")
    print("=" * 50)
    
    # Verify API key is loaded
    api_key = os.getenv("PATENTSVIEW_API_KEY")
    if api_key:
        print(f"✓ API Key loaded: {api_key[:10]}...")
    else:
        print("✗ No API key found!")
        return
    
    # Initialize API client
    api_client = PatentsViewAPI(api_key=api_key)
    print("✓ PatentsViewAPI initialized with API key")
    
    # Test search
    search_query = "artificial intelligence"
    print(f"\nSearching for: '{search_query}'")
    
    try:
        results = api_client.search_patents(search_query, max_results=3)
        print(f"✓ Search successful!")
        print(f"  Found {len(results)} patents")
        
        # Show first result details
        if results:
            first_patent = results[0]
            print(f"\nFirst Result:")
            print(f"  Patent ID: {first_patent.get('patent_id', 'N/A')}")
            print(f"  Title: {first_patent.get('patent_title', 'N/A')[:100]}...")
            print(f"  Grant Date: {first_patent.get('patent_date', 'N/A')}")
        
    except Exception as e:
        print(f"✗ Search failed: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    test_with_real_api()
