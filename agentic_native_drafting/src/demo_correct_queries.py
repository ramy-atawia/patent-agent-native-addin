#!/usr/bin/env python3
"""
Demo: Correct vs Incorrect Patent Search Queries
Shows the difference between searching for technology vs searching for reports about technology
"""

import asyncio
from prior_art_search import PatentSearchEngine

async def demo_query_comparison():
    """Demonstrate correct vs incorrect search query usage"""
    
    print("🔍 PATENT SEARCH QUERY DEMONSTRATION")
    print("="*60)
    print()
    
    search_engine = PatentSearchEngine()
    
    # Incorrect query (what the user tried)
    print("❌ INCORRECT QUERY EXAMPLE:")
    print("   Query: 'prior art search report for 5G dynamic spectrum sharing'")
    print("   Problem: Searching for 'report' and 'prior art' instead of the actual technology")
    print("   Result: No patents found (as expected)")
    print()
    
    # Correct query
    print("✅ CORRECT QUERY EXAMPLE:")
    print("   Query: '5G dynamic spectrum sharing'")
    print("   Focus: Actual technology terms that appear in patent titles/abstracts")
    print("   Running search...")
    print()
    
    try:
        # Run the correct search
        search_result = await search_engine.search("5G dynamic spectrum sharing")
        
        print(f"   📊 Results: {len(search_result.patents)} patents found")
        print(f"   🎯 Average relevance: {sum(p.relevance_score for p in search_result.patents) / len(search_result.patents):.3f}")
        print(f"   🔍 Strategies executed: {len(search_result.search_strategies)}")
        print()
        
        if search_result.patents:
            print("   📋 Sample patents found:")
            for i, patent in enumerate(search_result.patents[:3], 1):
                print(f"      {i}. {patent.patent_id}: {patent.title[:60]}...")
                print(f"         Assignee: {patent.assignees[0] if patent.assignees else 'Unknown'}")
                print(f"         Relevance: {patent.relevance_score}")
            print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        print()
    
    print("💡 QUERY BEST PRACTICES:")
    print("   ✅ DO search for:")
    print("      • Technical terms: '5G dynamic spectrum sharing'")
    print("      • Technology names: 'machine learning neural networks'")
    print("      • Industry standards: 'blockchain consensus algorithms'")
    print("      • Component technologies: 'lidar autonomous vehicles'")
    print()
    print("   ❌ DON'T search for:")
    print("      • 'prior art search for [technology]'")
    print("      • 'patent report on [technology]'")
    print("      • 'intellectual property analysis of [technology]'")
    print("      • General legal or procedural terms")
    print()
    
    print("🎯 WHY THIS MATTERS:")
    print("   The system searches actual patent databases for:")
    print("   • Patent titles containing your terms")
    print("   • Patent abstracts describing the technology")
    print("   • Technical claims using your terminology")
    print()
    print("   When you search for 'prior art search report for X',")
    print("   it looks for patents containing those exact words,")
    print("   which rarely appear in actual patent documents.")
    print()

if __name__ == "__main__":
    asyncio.run(demo_query_comparison())
