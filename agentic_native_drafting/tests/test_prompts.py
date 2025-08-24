#!/usr/bin/env python3
"""
Test script to verify prompt extraction is working correctly
"""

import sys
import os
from pathlib import Path

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from prompt_loader import prompt_loader


def test_prompt_loading():
    """Test that all prompts can be loaded and formatted"""
    
    print("🔍 Testing Prompt Loading System")
    print("=" * 50)
    
    # Test 1: List available prompts
    prompts = prompt_loader.list_available_prompts()
    print(f"✅ Found {len(prompts)} prompts: {prompts}")
    
    # Test 2: Search strategy generation prompt
    try:
        search_prompt = prompt_loader.load_prompt(
            "search_strategy_generation", 
            user_query="5G dynamic spectrum sharing"
        )
        print(f"✅ Search strategy prompt loaded: {len(search_prompt)} characters")
        assert "5G dynamic spectrum sharing" in search_prompt
        print("   ✓ Variable substitution working")
    except Exception as e:
        print(f"❌ Search strategy prompt failed: {e}")
        return False
    
    # Test 3: Relevance analysis prompt
    try:
        relevance_prompt = prompt_loader.load_prompt(
            "patent_relevance_analysis",
            search_query="wireless communication",
            title="Method for wireless data transmission",
            abstract="A system for transmitting data wirelessly..."
        )
        print(f"✅ Relevance analysis prompt loaded: {len(relevance_prompt)} characters")
        assert "wireless communication" in relevance_prompt
        assert "Method for wireless data transmission" in relevance_prompt
        print("   ✓ Multiple variable substitution working")
    except Exception as e:
        print(f"❌ Relevance analysis prompt failed: {e}")
        return False
    
    # Test 4: Report generation prompt
    try:
        report_prompt = prompt_loader.load_prompt(
            "comprehensive_report_generation",
            query="AI patent search",
            total_patents=5,
            patent_inventory='[{"patent_id": "US123456", "title": "Test Patent"}]'
        )
        print(f"✅ Report generation prompt loaded: {len(report_prompt)} characters")
        assert "AI patent search" in report_prompt
        assert "5" in report_prompt
        print("   ✓ Mixed data type substitution working")
    except Exception as e:
        print(f"❌ Report generation prompt failed: {e}")
        return False
    
    # Test 5: Error handling for missing variables
    try:
        prompt_loader.load_prompt("search_strategy_generation")  # Missing user_query
        print("❌ Should have failed with missing variable")
        return False
    except ValueError as e:
        print("✅ Error handling working: Missing variable detected")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False
    
    print("\n🎉 All tests passed! Prompt extraction system is working correctly.")
    print("\n📁 Prompt files location:", prompt_loader.prompts_dir)
    print("📝 Edit prompts directly in the .txt files - no code changes needed!")
    
    return True


if __name__ == "__main__":
    success = test_prompt_loading()
    sys.exit(0 if success else 1)
