#!/usr/bin/env python3
"""
Quick test to see the full report output from enhanced DSS search
"""

import asyncio
from prior_art_search import PatentSearchEngine

async def test_report_output():
    print("🔍 Testing Enhanced DSS Report Output...")
    
    search_engine = PatentSearchEngine()
    
    # Run search and get full report
    report = await search_engine.search("5G dynamic spectrum sharing DSS")
    
    print("\n📄 FULL REPORT:")
    print("="*80)
    print(report)
    print("="*80)
    
    # Save report to file for review
    with open('enhanced_dss_report.md', 'w') as f:
        f.write(report)
    
    print(f"\n✅ Report saved to: enhanced_dss_report.md")
    print(f"📊 Report length: {len(report)} characters")

if __name__ == "__main__":
    asyncio.run(test_report_output())
