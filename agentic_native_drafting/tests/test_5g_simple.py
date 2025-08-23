#!/usr/bin/env python3
"""
Quick test script for 5G search with enhanced patent search system
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from prior_art_search import PatentSearchEngine

async def test_5g_search():
    """Test the enhanced patent search system with 5G query"""
    try:
        print("🔍 Testing 5G patent search...")
        
        # Initialize search engine
        engine = PatentSearchEngine()
        
        # Perform search
        search_result = await engine.search("5G", max_results=5)
        
        print(f"✅ Search completed: {len(search_result.patents)} patents found")
        print(f"📊 Strategies executed: {len(search_result.search_strategies)}")
        
        # Generate report
        print("\n📋 Generating report...")
        report = await engine.generate_report(search_result)
        
        print(f"✅ Report generated: {len(report)} characters")
        
        # Show report excerpt
        print("\n" + "="*80)
        print("📄 REPORT EXCERPT:")
        print("="*80)
        print(report[:1000] + "..." if len(report) > 1000 else report)
        
        # Check for specific patent references
        print("\n🔍 CHECKING FOR SPECIFIC PATENT REFERENCES:")
        if "US12" in report and ":" in report:
            print("✅ Found specific patent ID and title references")
        else:
            print("❌ Generic patent references detected")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_5g_search())
