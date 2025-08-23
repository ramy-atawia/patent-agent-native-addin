#!/usr/bin/env python3
"""Test specific query that's failing"""

import asyncio
import httpx
import json
from dotenv import load_dotenv
import os

load_dotenv()

async def test_specific_query():
    """Test the actual query that's failing"""
    api_key = os.getenv("PATENTSVIEW_API_KEY")
    
    # This is the actual query from strategy 1
    payload = {
        "q": {
            "_and": [
                {
                    "_text_phrase": {
                        "patent_title": "dynamic spectrum sharing"
                    }
                },
                {
                    "_text_phrase": {
                        "patent_abstract": "5G"
                    }
                }
            ]
        },
        "f": [
            "patent_id",
            "patent_title", 
            "patent_abstract",
            "patent_date",
            "patent_year",
            "inventors",
            "assignees"
        ],
        "s": [{"patent_date": "desc"}],
        "o": {"size": 20}
    }
    
    headers = {"Content-Type": "application/json"}
    if api_key:
        headers["X-Api-Key"] = api_key
        print(f"Using API key: {api_key[:10]}...")
    
    url = "https://search.patentsview.org/api/v1/patent/"
    
    print("Testing query:")
    print(json.dumps(payload, indent=2))
    print()
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                patents = data.get("patents", [])
                print(f"Found {len(patents)} patents")
                for patent in patents[:3]:
                    print(f"- {patent.get('patent_id')}: {patent.get('patent_title', '')[:60]}...")
            else:
                print(f"Error response: {response.text}")
                
        except Exception as e:
            print(f"Request failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_specific_query())
