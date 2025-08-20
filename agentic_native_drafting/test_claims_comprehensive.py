#!/usr/bin/env python3
"""
Comprehensive test to find spectrum patents with available claims
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add src to path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from prior_art_search import OptimizedPatentsViewAPI

def test_claims_availability():
    """Test claims availability across multiple spectrum patents"""
    print("🔍 Comprehensive Claims Availability Test")
    print("=" * 60)
    
    api_client = OptimizedPatentsViewAPI()
    
    # Test with multiple spectrum patents to find ones with claims
    print(f"\n🧪 Testing Multiple Spectrum Patents for Claims")
    print("-" * 50)
    
    try:
        # Search for more spectrum patents
        spectrum_patents = api_client.search_spectrum_patents("Dynamic spectrum sharing", max_results=10)
        
        if not spectrum_patents:
            print("❌ No spectrum patents found")
            return
        
        print(f"Found {len(spectrum_patents)} spectrum patents to test")
        
        patents_with_claims = []
        patents_without_claims = []
        
        for i, patent in enumerate(spectrum_patents, 1):
            patent_id = patent.get("patent_id", "")
            title = patent.get("patent_title", "No title")[:80]
            
            print(f"\n  {i}. Testing Patent {patent_id}: {title}...")
            
            # Get claims for this patent
            claims = api_client.get_patent_claims(patent_id)
            
            if claims:
                print(f"     ✅ Has {len(claims)} claims")
                patents_with_claims.append({
                    "patent_id": patent_id,
                    "title": title,
                    "claim_count": len(claims)
                })
                
                # Show first claim preview
                first_claim = claims[0][:100] + "..." if len(claims[0]) > 100 else claims[0]
                print(f"     📝 First claim: {first_claim}")
            else:
                print(f"     ❌ No claims available")
                patents_without_claims.append({
                    "patent_id": patent_id,
                    "title": title
                })
            
            # Rate limiting between requests
            if i < len(spectrum_patents):
                import time
                time.sleep(1.5)
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 CLAIMS AVAILABILITY SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Patents WITH claims: {len(patents_with_claims)}")
        print(f"❌ Patents WITHOUT claims: {len(patents_without_claims)}")
        
        if patents_with_claims:
            print(f"\n🏆 PATENTS WITH CLAIMS:")
            for patent in patents_with_claims:
                print(f"  • {patent['patent_id']}: {patent['title']} ({patent['claim_count']} claims)")
        
        if patents_without_claims:
            print(f"\n⚠️  PATENTS WITHOUT CLAIMS:")
            for patent in patents_without_claims:
                print(f"  • {patent['patent_id']}: {patent['title']}")
        
        # Test a specific patent with claims if we found any
        if patents_with_claims:
            print(f"\n🧪 DETAILED CLAIMS TEST")
            print("-" * 40)
            
            test_patent = patents_with_claims[0]
            print(f"Testing detailed claims for: {test_patent['patent_id']}")
            
            claims = api_client.get_patent_claims(test_patent['patent_id'])
            
            print(f"\n📋 ALL CLAIMS FOR PATENT {test_patent['patent_id']}:")
            for i, claim in enumerate(claims, 1):
                print(f"\n  {i}. {claim}")
                if i >= 3:  # Show first 3 claims in full
                    print(f"  ... and {len(claims) - 3} more claims")
                    break
        
    except Exception as e:
        print(f"❌ Comprehensive test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run the comprehensive claims test"""
    test_claims_availability()
    print(f"\n{'='*60}")
    print("🎯 COMPREHENSIVE CLAIMS TEST COMPLETE")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
