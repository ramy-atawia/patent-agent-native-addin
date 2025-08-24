#!/usr/bin/env python3
"""
Test the updated prior_art_search.py module with extracted prompts
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent / "src"
sys.path.insert(0, str(src_dir))

from prior_art_search import SimplifiedPatentSearchEngine

async def test_updated_prior_art_search():
    """Test the updated patent search system with external prompts"""
    
    print("🔍 Testing Updated Prior Art Search System")
    print("=" * 50)
    
    try:
        # Test 1: Initialize the engine (tests prompt loading)
        print("1️⃣ Initializing search engine...")
        engine = SimplifiedPatentSearchEngine()
        print("   ✅ Engine initialized successfully")
        
        # Test 2: Test search strategy generation (tests first prompt)
        print("\n2️⃣ Testing search strategy generation...")
        strategies = await engine.query_generator.generate_search_strategies("wireless communication")
        print(f"   ✅ Generated {len(strategies)} search strategies")
        for i, strategy in enumerate(strategies, 1):
            print(f"   📋 Strategy {i}: {strategy.name}")
        
        # Test 3: Test relevance analysis (tests second prompt)
        print("\n3️⃣ Testing patent relevance analysis...")
        mock_patent = {
            "patent_title": "Wireless Communication System",
            "patent_abstract": "A system for wireless data transmission using advanced modulation techniques."
        }
        relevance_score = await engine.analyzer.check_relevance(mock_patent, "wireless communication")
        print(f"   ✅ Relevance analysis completed: score = {relevance_score:.2f}")
        
        # Test 4: Full search with limited results (tests integration)
        print("\n4️⃣ Testing full search integration...")
        search_result = await engine.search("wireless communication", max_results=2)
        print(f"   ✅ Search completed: {search_result.total_found} patents found")
        print(f"   📊 Search strategies used: {len(search_result.search_strategies)}")
        
        # Test 5: Report generation (tests third prompt)
        if search_result.patents:
            print("\n5️⃣ Testing report generation...")
            report = await engine.generate_report(search_result)
            print(f"   ✅ Report generated: {len(report)} characters")
            print(f"   📄 Report starts with: {report[:60]}...")
        else:
            print("\n5️⃣ Skipping report generation (no patents found)")
        
        print("\n🎉 All tests passed! The updated prior art search system is working correctly.")
        print("✅ Prompt extraction successful - functionality maintained")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    success = await test_updated_prior_art_search()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
