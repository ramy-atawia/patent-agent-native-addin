#!/usr/bin/env python3
"""
Test optimized report generation with timeout fixes and payload reduction
"""

import asyncio
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from prior_art_search import PatentSearchConfig, PatentSearchEngine

async def test_optimized_report():
    """Test the optimized report generation with real patents from logs"""
    print("🧪 Testing Optimized Prior Art Search Report Generation")
    print("=" * 60)
    
    # Configure for testing with timeout fixes
    config = PatentSearchConfig(
        patents_view_api_key=os.getenv("PATENTSVIEW_API_KEY", "demo"),
        azure_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        default_max_results=5,  # Reduced for testing efficiency
        default_relevance_threshold=0.6,
        timeout=120.0  # New timeout setting
    )
    
    search_engine = PatentSearchEngine(config)
    
    # Test with 5G dynamic spectrum sharing query (string query)
    test_query = "5G dynamic spectrum sharing technology for carrier aggregation and interference mitigation"
    
    print(f"📋 Query: {test_query}")
    print(f"📊 Max patents: {config.default_max_results}")
    print(f"⏰ Timeout: {config.timeout}s")
    print()
    
    try:
        print("🔍 Starting prior art search...")
        search_result = await search_engine.search(test_query)
        
        print("✅ Search completed successfully!")
        print(f"📊 Patents found: {len(search_result.patents)}")
        print()
        
        # Generate report
        print("📄 Generating comprehensive report...")
        report = await search_engine.generate_report(search_result)
        
        print("✅ Report generated successfully!")
        print(f"📄 Report length: {len(report)} characters")
        print()
        
        # Check if report contains claims information
        if "claim" in report.lower():
            print("✅ Report contains claims information")
        else:
            print("❌ Report does NOT contain claims information")
        
        # Check if report contains patent numbers
        patent_count = report.count("Patent")
        print(f"📊 Patent references in report: {patent_count}")
        
        # Check for timeout error messages
        if "timeout" in report.lower() or "error" in report.lower():
            print("⚠️  Report contains timeout/error messages")
        else:
            print("✅ Report appears clean (no timeout/error messages)")
        
        print()
        print("📋 REPORT PREVIEW (first 500 chars):")
        print("-" * 50)
        print(report[:500])
        if len(report) > 500:
            print("...")
        print("-" * 50)
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting optimized report generation test...")
    success = asyncio.run(test_optimized_report())
    
    if success:
        print("\n🎉 Test PASSED - Optimized report generation working!")
    else:
        print("\n💥 Test FAILED - Issues remain")
    
    sys.exit(0 if success else 1)
