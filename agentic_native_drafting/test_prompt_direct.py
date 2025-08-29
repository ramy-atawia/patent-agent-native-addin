#!/usr/bin/env python3
"""
Test Prompt Template Directly

This script tests the prompt template directly to see what's being sent to the LLM
and identify why the context is being ignored.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src import prompt_loader

def test_prompt_template():
    """Test the prompt template directly"""
    
    print("🔍 TESTING PROMPT TEMPLATE DIRECTLY")
    print("=" * 60)
    
    # Test data (same as our scenario)
    test_data = {
        "input_text": "draft the corresponding method claims",
        "conversation_history": [
            {
                "role": "user",
                "content": "draft 5 system claims for 4g carrier aggregation",
                "timestamp": "2025-08-27T21:40:00.000Z"
            },
            {
                "role": "assistant", 
                "content": "Successfully drafted 5 content items\rGenerated Patent Claims:\rClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\rClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\rClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\rClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\rClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.",
                "timestamp": "2025-08-27T21:43:00.000Z"
            }
        ],
        "document_content": {
            "text": "Successfully drafted 5 content items\rGenerated Patent Claims:\rClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\rClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\rClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\rClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\rClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.",
            "paragraphs": [],
            "session_id": "test-session-4g-carrier-aggregation"
        }
    }
    
    print("📋 Test Data:")
    print(f"   Input Text: {test_data['input_text']}")
    print(f"   Conversation History: {len(test_data['conversation_history'])} entries")
    print(f"   Document Content Length: {len(test_data['document_content']['text'])} characters")
    print()
    
    # Test 1: Load the prompt template
    print("🧪 TEST 1: Load Prompt Template")
    print("-" * 40)
    
    try:
        # Load the prompt template with variables
        formatted_prompt = prompt_loader.load_prompt(
            "claim_drafting_user",
            disclosure=test_data['input_text'],
            document_content=test_data['document_content']['text'],
            conversation_history=str(test_data['conversation_history'])
        )
        print(f"✅ Prompt template loaded and formatted successfully")
        print(f"   Formatted prompt length: {len(formatted_prompt)} characters")
        print()
        
        # Show the full formatted prompt
        print("📝 FULL FORMATTED PROMPT:")
        print("=" * 60)
        print(formatted_prompt)
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Failed to load prompt template: {e}")
        return
    

    
    # Test 3: Check if context is properly included
    print()
    print("🧪 TEST 3: Context Inclusion Check")
    print("-" * 40)
    
    formatted_prompt_lower = formatted_prompt.lower()
    
    # Check for key context elements
    context_checks = {
        "4g carrier aggregation": "4g carrier aggregation" in formatted_prompt_lower,
        "carrier network": "carrier network" in formatted_prompt_lower,
        "communication module": "communication module" in formatted_prompt_lower,
        "data throughput": "data throughput" in formatted_prompt_lower,
        "system claims": "system claims" in formatted_prompt_lower,
        "method claims": "method claims" in formatted_prompt_lower,
        "corresponding": "corresponding" in formatted_prompt_lower
    }
    
    print("🔍 Context Elements Check:")
    for element, found in context_checks.items():
        status = "✅ FOUND" if found else "❌ MISSING"
        print(f"   {element}: {status}")
    
    # Summary
    found_count = sum(context_checks.values())
    total_count = len(context_checks)
    
    print(f"\n📊 Context Coverage: {found_count}/{total_count} elements found")
    
    if found_count == total_count:
        print("✅ ALL context elements are present in the prompt!")
    else:
        print("⚠️  Some context elements are missing from the prompt")
        print("   This could explain why the LLM is generating generic claims")

if __name__ == "__main__":
    test_prompt_template()
