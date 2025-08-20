#!/usr/bin/env python3
"""
Search for telecommunications spectrum sharing patents with better targeting
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def search_telecom_spectrum_patents():
    """Search for telecommunications spectrum sharing patents"""
    print("🔍 Searching for TELECOMMUNICATIONS spectrum sharing patents...")
    print("=" * 70)
    
    try:
        # Add src to path
        src_path = Path(__file__).parent / "src"
        sys.path.insert(0, str(src_path))
        
        from prior_art_search import OptimizedPatentsViewAPI
        
        api_client = OptimizedPatentsViewAPI()
        
        # Try more specific telecommunications-focused searches
        search_strategies = [
            {
                "name": "Telecommunications + spectrum",
                "query": "telecommunications spectrum sharing",
                "description": "Looking for telecom patents with spectrum sharing"
            },
            {
                "name": "Mobile network spectrum",
                "query": "mobile network spectrum sharing",
                "description": "Mobile network and spectrum sharing"
            },
            {
                "name": "Radio frequency spectrum",
                "query": "radio frequency spectrum sharing",
                "description": "RF spectrum sharing patents"
            },
            {
                "name": "Wireless communication spectrum",
                "query": "wireless communication spectrum sharing",
                "description": "Wireless comm and spectrum sharing"
            },
            {
                "name": "Base station spectrum",
                "query": "base station spectrum sharing",
                "description": "Base station and spectrum sharing"
            }
        ]
        
        for strategy in search_strategies:
            print(f"\n{'='*70}")
            print(f"Strategy: {strategy['name']}")
            print(f"Query: '{strategy['query']}'")
            print(f"Description: {strategy['description']}")
            print(f"{'='*70}")
            
            patent_data = api_client.search_patents(strategy['query'], max_results=15)
            
            if patent_data:
                print(f"✓ Found {len(patent_data)} patents")
                print("\n📋 PATENT NUMBERS & TITLES:")
                print("-" * 60)
                
                # Filter for more relevant patents
                relevant_count = 0
                for i, patent in enumerate(patent_data, 1):
                    patent_id = patent.get("patent_id", "")
                    title = patent.get("patent_title", "")
                    
                    # Check if title seems relevant to telecommunications
                    title_lower = title.lower()
                    telecom_keywords = ['wireless', 'radio', 'frequency', 'spectrum', 'mobile', 'network', 'communication', 'base station', 'antenna', 'signal']
                    
                    is_relevant = any(keyword in title_lower for keyword in telecom_keywords)
                    
                    if is_relevant:
                        relevant_count += 1
                        print(f"{relevant_count:2d}. {patent_id} - RELEVANT")
                        print(f"    Title: {title}")
                        print()
                    else:
                        print(f"    {patent_id} - {title[:60]}...")
                
                print(f"\n📊 SUMMARY:")
                print(f"  Total found: {len(patent_data)}")
                print(f"  Relevant to telecom: {relevant_count}")
                
                # Show just the relevant numbers
                if relevant_count > 0:
                    print(f"\n🔢 RELEVANT PATENT NUMBERS:")
                    print("-" * 30)
                    relevant_patents = []
                    for patent in patent_data:
                        title_lower = patent.get("patent_title", "").lower()
                        telecom_keywords = ['wireless', 'radio', 'frequency', 'spectrum', 'mobile', 'network', 'communication', 'base station', 'antenna', 'signal']
                        if any(keyword in title_lower for keyword in telecom_keywords):
                            relevant_patents.append(patent.get("patent_id", ""))
                    
                    for number in relevant_patents:
                        print(number)
                else:
                    print("❌ No relevant telecommunications patents found")
                    
            else:
                print("❌ No patents found")
            
            print(f"\n" + "-"*60)
            
            # Rate limiting between searches
            import time
            time.sleep(2)
            
    except Exception as e:
        print(f"✗ Search failed: {e}")
        import traceback
        traceback.print_exc()

def main():
    """Run the search"""
    search_telecom_spectrum_patents()

if __name__ == "__main__":
    main()
