#!/usr/bin/env python3
"""
Test the simplified patent search system
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from prior_art_search_simplified import SimplifiedPatentSearchEngine

async def test_simplified_search():
    """Test the simplified patent search system"""
    try:
        print("🔍 Testing SIMPLIFIED 5G patent search...")
        
        # Initialize simplified search engine
        engine = SimplifiedPatentSearchEngine()
        
        # Perform search
        search_result = await engine.search("5G", max_results=3)
        
        print(f"✅ Search completed: {len(search_result.patents)} patents found")
        print(f"📊 Strategies executed: {len(search_result.search_strategies)}")
        
        # Show patent summaries
        print("\n📋 PATENT SUMMARIES:")
        for i, patent in enumerate(search_result.patents, 1):
            print(f"{i}. {patent.title[:80]}...")
            print(f"   Relevance: {patent.relevance_score:.3f}")
            print(f"   Assignees: {', '.join(patent.assignees[:2])}")
            print(f"   Claims: {len(patent.claims)}")
            print()
        
        # Generate simplified report
        print("📋 Generating SIMPLIFIED report...")
        report = await engine.generate_report(search_result)
        
        print(f"✅ Report generated: {len(report)} characters")
        
        # Show report excerpt
        print("\n" + "="*80)
        print("📄 SIMPLIFIED REPORT EXCERPT:")
        print("="*80)
        print(report[:1500] + "..." if len(report) > 1500 else report)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_simplified_search())
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}")
