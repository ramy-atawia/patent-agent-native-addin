#!/usr/bin/env python3
"""
Debug script to inspect generated search queries
"""

import asyncio
from prior_art_search import QueryGenerator, PatentSearchConfig

async def debug_queries():
    """Debug the query generation process"""
    try:
        print("🔍 Debugging 5G Dynamic Spectrum Sharing query generation...")
        
        # Initialize query generator
        config = PatentSearchConfig()
        generator = QueryGenerator(config)
        
        # Generate strategies
        query = "5G dynamic spectrum sharing"
        strategies = await generator.generate_search_strategies(query)
        
        print(f"✅ Generated {len(strategies)} strategies:")
        print("="*80)
        
        for i, strategy in enumerate(strategies, 1):
            print(f"\n🎯 STRATEGY {i}: {strategy.name}")
            print(f"   Description: {strategy.description}")
            print(f"   Technical Focus: {strategy.technical_focus}")
            print(f"   Coverage Scope: {strategy.coverage_scope}")
            print(f"   Expected Results: {strategy.expected_results}")
            print(f"   Query Structure:")
            import json
            print(json.dumps(strategy.query, indent=6))
            print("-" * 60)
        
        return strategies
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        return []

if __name__ == "__main__":
    asyncio.run(debug_queries())
