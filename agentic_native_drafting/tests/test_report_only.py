#!/usr/bin/env python3
"""
Test report generation separately to debug the issue
"""

import asyncio
import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.prior_art_search import SimplifiedReportGenerator, PatentSearchConfig, SearchResult, SimplePatentAnalysis, PatentClaim, SearchStrategy
from datetime import datetime

async def test_report_generation():
    """Test report generation with minimal data"""
    try:
        print("🔍 Testing report generation...")
        
        config = PatentSearchConfig()
        generator = SimplifiedReportGenerator(config)
        
        # Create minimal test data
        test_claim = PatentClaim(
            claim_number="1",
            claim_text="A method for wireless communication...",
            claim_type="independent"
        )
        
        test_patent = SimplePatentAnalysis(
            patent_id="12345678",
            title="Test 5G Patent",
            abstract="This patent describes 5G technology...",
            inventors=["John Doe", "Jane Smith"],
            assignees=["Tech Corp"],
            claims=[test_claim],
            relevance_score=0.85
        )
        
        test_strategies = [
            SearchStrategy(name="Test Strategy", description="Test", query={"test": "test"})
        ]
        
        test_result = SearchResult(
            query="5G",
            total_found=1,
            patents=[test_patent],
            search_strategies=test_strategies,
            timestamp=datetime.now().isoformat()
        )
        
        # Test report generation
        report = await generator.generate_report(test_result)
        
        print(f"✅ Report generated: {len(report)} characters")
        print("\nReport preview:")
        print(report[:500] + "..." if len(report) > 500 else report)
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_report_generation())
