#!/usr/bin/env python3
"""
Enhanced query generation for DSS with manual query refinement
"""

import asyncio
from prior_art_search import PatentSearchEngine

async def test_enhanced_dss_search():
    """Test enhanced DSS search with manual query improvements"""
    try:
        print("🔍 Testing Enhanced DSS Search with Improved Queries...")
        
        # Initialize search engine
        engine = PatentSearchEngine()
        
        # Perform search with enhanced query
        search_result = await engine.search("5G dynamic spectrum sharing DSS", max_results=20)
        
        print(f"✅ Search completed: {len(search_result.patents)} patents found")
        print(f"📊 Strategies executed: {len(search_result.search_strategies)}")
        
        # Show patent IDs and titles found
        print("\n📋 PATENTS FOUND:")
        print("="*80)
        for i, patent in enumerate(search_result.patents, 1):
            print(f"{i}. {patent.patent_id}: {patent.title}")
            print(f"   Assignee: {', '.join(patent.assignees)}")
            print(f"   Relevance: {patent.relevance_score:.2f}")
            print(f"   Source: {patent.source_strategy}")
            print()
        
        # Generate brief report
        print("📄 GENERATING BRIEF REPORT...")
        report = await engine.generate_report(search_result)
        
        # Show report excerpt focusing on patent references
        print("="*80)
        print("REPORT EXCERPT - Patent References:")
        print("="*80)
        
        # Extract lines that mention specific patent IDs
        report_lines = report.split('\n')
        patent_references = []
        for line in report_lines:
            if 'US12' in line and ':' in line:
                patent_references.append(line.strip())
        
        if patent_references:
            print("✅ SPECIFIC PATENT REFERENCES FOUND:")
            for ref in patent_references[:20]:  # Show first 20
                print(f"  • {ref}")
        else:
            print("❌ No specific patent references found in report")
        
        return search_result
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(test_enhanced_dss_search())
