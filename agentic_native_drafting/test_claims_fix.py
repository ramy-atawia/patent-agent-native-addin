#!/usr/bin/env python3
"""
Test the fixed claims functionality using the working query structure
from the PatentsView forum
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

def test_claims_functionality():
    """Test the fixed claims functionality"""
    print("🔍 Testing Fixed Claims Functionality")
    print("=" * 60)
    
    api_client = OptimizedPatentsViewAPI()
    
    # Test with the patent ID from the forum example
    test_patent_id = "11540434"  # The working example from the forum
    
    print(f"\n🧪 Test 1: Claims for Patent {test_patent_id} (Forum Example)")
    print("-" * 50)
    
    try:
        claims = api_client.get_patent_claims(test_patent_id)
        
        if claims:
            print(f"✅ Success! Retrieved {len(claims)} claims")
            print(f"\n📋 Claims Preview:")
            for i, claim in enumerate(claims[:3], 1):  # Show first 3 claims
                # Truncate long claims for display
                claim_preview = claim[:150] + "..." if len(claim) > 150 else claim
                print(f"\n  {i}. {claim_preview}")
            
            if len(claims) > 3:
                print(f"\n  ... and {len(claims) - 3} more claims")
        else:
            print("❌ No claims retrieved")
            
    except Exception as e:
        print(f"❌ Claims test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 2: Claims for one of our spectrum patents
    print(f"\n🧪 Test 2: Claims for Spectrum Patent")
    print("-" * 50)
    
    try:
        # First search for a spectrum patent
        spectrum_patents = api_client.search_spectrum_patents("Dynamic spectrum sharing", max_results=1)
        
        if spectrum_patents:
            test_patent = spectrum_patents[0]
            patent_id = test_patent.get("patent_id")
            title = test_patent.get("patent_title", "No title")[:80]
            
            print(f"Testing with patent: {patent_id} - {title}...")
            
            claims = api_client.get_patent_claims(patent_id)
            
            if claims:
                print(f"✅ Success! Retrieved {len(claims)} claims")
                print(f"\n📋 Claims Preview:")
                for i, claim in enumerate(claims[:2], 1):  # Show first 2 claims
                    claim_preview = claim[:150] + "..." if len(claim) > 150 else claim
                    print(f"\n  {i}. {claim_preview}")
            else:
                print("❌ No claims retrieved for spectrum patent")
        else:
            print("❌ No spectrum patents found to test")
            
    except Exception as e:
        print(f"❌ Spectrum patent claims test failed: {e}")
        import traceback
        traceback.print_exc()
    
    # Test 3: Test the exact query structure from the forum
    print(f"\n🧪 Test 3: Exact Forum Query Structure")
    print("-" * 50)
    
    try:
        import httpx
        
        # Use the exact working query from the forum
        payload = {
            "f": [
                "patent_id",
                "claim_sequence", 
                "claim_text",
                "claim_number",
                "claim_dependent",
                "exemplary"
            ],
            "o": {
                "size": 100
            },
            "q": {
                "_and": [
                    {"patent_id": "11540434"}
                ]
            },
            "s": [
                {"patent_id": "asc"}, 
                {"claim_sequence": "asc"}
            ]
        }
        
        headers = {"Content-Type": "application/json"}
        if api_client.api_key:
            headers["X-Api-Key"] = api_client.api_key
        
        response = httpx.post(
            f"{api_client.base_url}/g_claim/",
            json=payload,
            headers=headers
        )
        
        if response.status_code == 200:
            data = response.json()
            claims = data.get("g_claims", [])
            print(f"✅ Forum query successful! Retrieved {len(claims)} claims")
            
            if claims:
                print(f"\n📋 First Claim Preview:")
                first_claim = claims[0]
                claim_text = first_claim.get("claim_text", "")[:200]
                print(f"  Claim {first_claim.get('claim_sequence', 0) + 1}: {claim_text}...")
        else:
            print(f"❌ Forum query failed with status {response.status_code}")
            
    except Exception as e:
        print(f"❌ Forum query test failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run the claims functionality tests"""
    test_claims_functionality()
    print(f"\n{'='*60}")
    print("🎯 CLAIMS FUNCTIONALITY TEST COMPLETE")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
