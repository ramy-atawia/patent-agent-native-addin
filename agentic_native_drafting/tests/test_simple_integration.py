#!/usr/bin/env python3
"""
Test with simple working query to verify integration
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.prior_art_search import EnhancedPatentsViewAPI, PatentSearchConfig, SearchStrategy

async def test_simple_integration():
    """Test with a simple working query"""
    try:
        print("🔍 Testing simple patent API integration...")
        
        config = PatentSearchConfig()
        
        # Create a simple strategy that we know works
        simple_strategy = SearchStrategy(
            name="Simple Wireless Test",
            description="Simple test with known working query",
            query={"patent_title": "wireless"},
            expected_results=5
        )
        
        async with EnhancedPatentsViewAPI(config) as api:
            results = await api.search_patents_async(simple_strategy)
            
            print(f"✅ Found {len(results)} patents")
            
            for i, patent in enumerate(results[:3]):
                print(f"{i+1}. {patent.get('patent_id')}: {patent.get('patent_title', '')[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_simple_integration())
