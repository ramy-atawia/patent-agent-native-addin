#!/usr/bin/env python3
"""
Test Claims Retrieval from PatentsView API
Tests the claims retrieval functionality to ensure it works properly.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the src directory to Python path
src_dir = Path(__file__).parent.parent / "src"
sys.path.insert(0, str(src_dir))

from prior_art_search import EnhancedPatentsViewAPI, PatentSearchConfig, PatentClaim


async def test_claims_retrieval():
    """Test claims retrieval from PatentsView API"""
    
    print("🔍 Testing Claims Retrieval from PatentsView API")
    print("=" * 60)
    
    # Test configuration
    config = PatentSearchConfig()
    
    # Test patent IDs - using patents from 5G DSS prior art report
    test_patents = [
        "12192952",  # Efficient positioning enhancement for dynamic spectrum sharing - QUALCOMM
        "12063645",  # Scheduling restriction enhancements for LTE and 5G NR DSS - Apple Inc.
        "11888610",  # Method and apparatus for positioning with LTE-NR DSS - QUALCOMM
        "11044693",  # Efficient positioning enhancement for dynamic spectrum sharing - QUALCOMM
        "11943204"   # Method and systems for DSS with spectrum management firewall - RIVADA NETWORKS
    ]
    
    successful_tests = 0
    total_tests = len(test_patents)
    
    async with EnhancedPatentsViewAPI(config) as api:
        for i, patent_id in enumerate(test_patents, 1):
            print(f"\n{i}. Testing patent: {patent_id}")
            print("-" * 40)
            
            try:
                # Retrieve claims for this patent
                claims = await api.get_patent_claims_async(patent_id)
                
                if claims:
                    print(f"✅ SUCCESS: Found {len(claims)} claims")
                    
                    # Show details of first few claims
                    for j, claim in enumerate(claims[:3], 1):
                        print(f"   Claim {claim.claim_number} ({claim.claim_type}):")
                        claim_preview = claim.claim_text[:100] + "..." if len(claim.claim_text) > 100 else claim.claim_text
                        print(f"   Text: {claim_preview}")
                        if claim.dependency:
                            print(f"   Depends on: {claim.dependency}")
                        print()
                    
                    if len(claims) > 3:
                        print(f"   ... and {len(claims) - 3} more claims")
                    
                    # Analyze claim types
                    independent_claims = [c for c in claims if c.claim_type == "independent"]
                    dependent_claims = [c for c in claims if c.claim_type == "dependent"]
                    
                    print(f"   📊 Claim Analysis:")
                    print(f"      - Independent claims: {len(independent_claims)}")
                    print(f"      - Dependent claims: {len(dependent_claims)}")
                    print(f"      - Total claims: {len(claims)}")
                    
                    successful_tests += 1
                    
                else:
                    print(f"⚠️  No claims found for patent {patent_id}")
                    print("   This could mean:")
                    print("   - Patent doesn't exist")
                    print("   - Patent has no claims in PatentsView")
                    print("   - API issue")
                
            except Exception as e:
                print(f"❌ ERROR retrieving claims for {patent_id}: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print(f"Total tests: {total_tests}")
    print(f"Successful: {successful_tests}")
    print(f"Failed: {total_tests - successful_tests}")
    print(f"Success rate: {(successful_tests/total_tests)*100:.1f}%")
    
    if successful_tests > 0:
        print("\n✅ Claims retrieval is working!")
        return True
    else:
        print("\n❌ Claims retrieval failed for all test patents")
        return False


async def test_specific_known_patent():
    """Test with a specific known patent that should have claims"""
    
    print("\n" + "=" * 60)
    print("🎯 Testing Specific Known Patent")
    print("=" * 60)
    
    # Test with known patents from the 5G DSS prior art report
    known_patent = "7450947"  # Method and apparatus for dynamic spectrum sharing - Motorola (foundational patent)
    
    config = PatentSearchConfig()
    
    async with EnhancedPatentsViewAPI(config) as api:
        try:
            print(f"Testing patent: {known_patent}")
            claims = await api.get_patent_claims_async(known_patent)
            
            if claims:
                print(f"✅ Found {len(claims)} claims")
                
                # Detailed analysis
                print("\n📋 DETAILED CLAIM ANALYSIS:")
                for claim in claims[:5]:  # Show first 5 claims
                    print(f"\nClaim {claim.claim_number} ({claim.claim_type}):")
                    print(f"Text: {claim.claim_text[:200]}...")
                    if claim.dependency:
                        print(f"Depends on claim: {claim.dependency}")
                    if claim.is_exemplary:
                        print("Marked as exemplary")
                
                return True
            else:
                print(f"❌ No claims found for {known_patent}")
                
                # Try alternative patent numbers from the report
                alternative_patents = [
                    "11832111",  # Dynamic spectrum sharing between 4G and 5G - QUALCOMM
                    "10849180",  # Dynamic spectrum sharing in 4G and 5G - T-Mobile
                    "11882626",  # Selecting antenna configurations - Sprint Spectrum
                    "11864005"   # Optimized carrier combination selection - T-Mobile Innovations
                ]
                
                for alt_patent in alternative_patents:
                    print(f"\nTrying alternative patent: {alt_patent}")
                    alt_claims = await api.get_patent_claims_async(alt_patent)
                    if alt_claims:
                        print(f"✅ Found {len(alt_claims)} claims for {alt_patent}")
                        
                        # Show some details for the successful patent
                        print(f"\n📋 Sample claims from {alt_patent}:")
                        for claim in alt_claims[:3]:
                            print(f"   Claim {claim.claim_number}: {claim.claim_text[:100]}...")
                        
                        return True
                
                return False
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return False


async def test_claims_parsing():
    """Test the claims parsing logic with mock data"""
    
    print("\n" + "=" * 60)
    print("🔧 Testing Claims Parsing Logic")
    print("=" * 60)
    
    config = PatentSearchConfig()
    api = EnhancedPatentsViewAPI(config)
    
    # Mock claims data as it would come from PatentsView API
    mock_claims_data = [
        {
            "claim_sequence": 0,
            "claim_number": "1",
            "claim_text": "A method for wireless communication comprising: receiving a signal; processing the signal; and transmitting a response.",
            "claim_dependent": "",
            "exemplary": ""
        },
        {
            "claim_sequence": 1,
            "claim_number": "2", 
            "claim_text": "The method of claim 1, wherein the signal is a 5G signal.",
            "claim_dependent": "1",
            "exemplary": ""
        },
        {
            "claim_sequence": 2,
            "claim_number": "3",
            "claim_text": "The method of claim 1, wherein the processing includes decoding.",
            "claim_dependent": "1", 
            "exemplary": "true"
        }
    ]
    
    try:
        # Test the parsing function
        parsed_claims = api._parse_claims(mock_claims_data)
        
        print(f"✅ Parsed {len(parsed_claims)} claims from mock data")
        
        for claim in parsed_claims:
            print(f"\nClaim {claim.claim_number} ({claim.claim_type}):")
            print(f"Text: {claim.claim_text[:100]}...")
            if claim.dependency:
                print(f"Depends on: {claim.dependency}")
            if claim.is_exemplary:
                print("Marked as exemplary")
        
        # Verify parsing correctness
        assert len(parsed_claims) == 3, "Should parse 3 claims"
        assert parsed_claims[0].claim_type == "independent", "Claim 1 should be independent"
        assert parsed_claims[1].claim_type == "dependent", "Claim 2 should be dependent"
        assert parsed_claims[1].dependency == "1", "Claim 2 should depend on claim 1"
        assert parsed_claims[2].is_exemplary == True, "Claim 3 should be exemplary"
        
        print("\n✅ All parsing tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Parsing test failed: {e}")
        return False


async def main():
    """Run all claims retrieval tests"""
    
    print("🧪 CLAIMS RETRIEVAL TEST SUITE")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: General claims retrieval
    try:
        if await test_claims_retrieval():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test 1 failed: {e}")
    
    # Test 2: Specific known patent
    try:
        if await test_specific_known_patent():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test 2 failed: {e}")
    
    # Test 3: Claims parsing logic
    try:
        if await test_claims_parsing():
            tests_passed += 1
    except Exception as e:
        print(f"❌ Test 3 failed: {e}")
    
    # Final summary
    print("\n" + "🏁 FINAL TEST RESULTS " + "🏁")
    print("=" * 60)
    print(f"Tests passed: {tests_passed}/{total_tests}")
    print(f"Success rate: {(tests_passed/total_tests)*100:.1f}%")
    
    if tests_passed == total_tests:
        print("\n🎉 ALL TESTS PASSED! Claims retrieval is working properly.")
        return True
    elif tests_passed > 0:
        print(f"\n⚠️  {tests_passed} out of {total_tests} tests passed. Some issues detected.")
        return False
    else:
        print("\n❌ ALL TESTS FAILED! Claims retrieval needs investigation.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
