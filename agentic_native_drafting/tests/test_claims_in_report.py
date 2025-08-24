#!/usr/bin/env python3
"""
Quick test to verify claims are being properly included in reports
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from prior_art_search import SimplifiedPatentSearchEngine

async def test_claims_in_report():
    """Test that claims are properly included in the search report"""
    
    print("🔍 Testing Claims Integration in Full Search Report")
    print("=" * 60)
    
    # Initialize search engine
    engine = SimplifiedPatentSearchEngine()
    
    # Use a simple query that should find patents with claims
    query = "dynamic spectrum sharing"
    
    print(f"Running search for: '{query}'")
    print("This will test the full workflow including claims retrieval...")
    
    try:
        # Perform the full search (this should include claims retrieval)
        search_result = await engine.search(query, max_results=3)
        
        print(f"\n✅ Search completed!")
        print(f"📊 Found {len(search_result.patents)} patents")
        
        # Check each patent for claims
        total_claims = 0
        patents_with_claims = 0
        
        for i, patent in enumerate(search_result.patents, 1):
            claims_count = len(patent.claims)
            total_claims += claims_count
            
            if claims_count > 0:
                patents_with_claims += 1
                
            print(f"\n{i}. Patent {patent.patent_id}:")
            print(f"   Title: {patent.title[:80]}...")
            print(f"   Claims: {claims_count}")
            print(f"   Relevance: {patent.relevance_score:.3f}")
            
            if claims_count > 0:
                # Show claim types
                independent = [c for c in patent.claims if c.claim_type == "independent"]
                dependent = [c for c in patent.claims if c.claim_type == "dependent"]
                print(f"   - Independent: {len(independent)}")
                print(f"   - Dependent: {len(dependent)}")
                
                # Show first claim preview
                if patent.claims:
                    first_claim = patent.claims[0]
                    print(f"   First claim: {first_claim.claim_text[:100]}...")
            else:
                print("   ⚠️  NO CLAIMS FOUND!")
        
        print(f"\n📊 CLAIMS SUMMARY:")
        print(f"   Total patents: {len(search_result.patents)}")
        print(f"   Patents with claims: {patents_with_claims}")
        print(f"   Total claims retrieved: {total_claims}")
        print(f"   Success rate: {(patents_with_claims/len(search_result.patents)*100):.1f}%")
        
        # Generate report and check if claims are included
        print(f"\n📄 Generating report...")
        report = await engine.generate_report(search_result)
        
        # Check if report contains claim information
        claims_in_report = "Claim " in report and len([line for line in report.split('\n') if 'Claim ' in line]) > 5
        
        print(f"✅ Report generated: {len(report)} characters")
        print(f"📋 Claims in report: {'✅ YES' if claims_in_report else '❌ NO'}")
        
        if claims_in_report:
            # Count claim references in report
            claim_lines = [line for line in report.split('\n') if 'Claim ' in line]
            print(f"   Found {len(claim_lines)} claim references in report")
        
        # Show a sample of the report
        print(f"\n📄 REPORT SAMPLE:")
        print("=" * 60)
        report_lines = report.split('\n')
        for line in report_lines[50:70]:  # Show middle section
            if line.strip():
                print(line)
        print("=" * 60)
        
        return patents_with_claims > 0 and claims_in_report
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    success = await test_claims_in_report()
    
    if success:
        print("\n🎉 SUCCESS: Claims are being properly retrieved and included in reports!")
    else:
        print("\n❌ FAILURE: Claims are not being properly included in reports.")
    
    return success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
