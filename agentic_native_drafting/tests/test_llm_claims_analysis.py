#!/usr/bin/env python3
"""
Test LLM-based claims analysis functionality
"""

import asyncio
import pytest
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.prior_art_search import PatentSearchConfig, SimplifiedReportGenerator
from src.models import PatentClaim

@pytest.mark.asyncio
async def test_llm_claims_analysis():
    """Test the new LLM-based claims analysis function"""
    print("🧪 Testing LLM-based Claims Analysis")
    print("=" * 50)
    
    # Configure for testing
    config = PatentSearchConfig(
        azure_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o-mini"),
        timeout=120.0
    )
    
    # Create sample patent claims for testing
    sample_claims = [
        PatentClaim(
            claim_number="1",
            claim_text="A method for dynamic spectrum sharing in wireless communication networks, comprising: establishing a primary connection between a base station and user equipment; monitoring spectrum availability across multiple frequency bands; dynamically allocating spectrum resources based on detected interference levels; and coordinating spectrum sharing between different network technologies.",
            claim_type="independent"
        ),
        PatentClaim(
            claim_number="2", 
            claim_text="The method of claim 1, wherein the monitoring comprises continuously scanning predetermined frequency ranges and measuring signal strength indicators.",
            claim_type="dependent",
            dependency="1"
        ),
        PatentClaim(
            claim_number="3",
            claim_text="The method of claim 1, wherein the coordinating comprises exchanging scheduling information between LTE and 5G NR network entities.",
            claim_type="dependent", 
            dependency="1"
        )
    ]
    
    patent_title = "Dynamic Spectrum Sharing Method and Apparatus for 5G Networks"
    search_query = "5G dynamic spectrum sharing technology"
    
    # Test the LLM claims analysis
    generator = SimplifiedReportGenerator(config)
    
    try:
        print(f"📋 Testing with patent: {patent_title}")
        print(f"🔍 Search context: {search_query}")
        print(f"📊 Sample claims: {len(sample_claims)} claims")
        print()
        
        print("🤖 Analyzing claims with LLM...")
        analysis = await generator._analyze_claims_with_llm(
            sample_claims, 
            patent_title, 
            search_query
        )
        
        print("✅ LLM Analysis completed!")
        print()
        print("📋 CLAIMS ANALYSIS RESULTS:")
        print("-" * 40)
        
        for key, value in analysis.items():
            print(f"{key.replace('_', ' ').title()}: {value}")
        
        print()
        print("🎯 Key Insights:")
        print(f"• Technical Scope: {analysis.get('technical_scope', 'N/A')}")
        print(f"• Blocking Potential: {analysis.get('blocking_potential', 'N/A')}")
        print(f"• Claim Breadth: {analysis.get('claim_breadth', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Starting LLM-based claims analysis test...")
    success = asyncio.run(test_llm_claims_analysis())
    
    if success:
        print("\n🎉 Test PASSED - LLM claims analysis working!")
    else:
        print("\n💥 Test FAILED - Issues with LLM claims analysis")
    
    sys.exit(0 if success else 1)
