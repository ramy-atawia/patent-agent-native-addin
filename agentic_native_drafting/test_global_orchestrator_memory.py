#!/usr/bin/env python3
"""
Test Global Orchestrator Memory State

This script inspects the global orchestrator's memory state to identify
why the API flow differs from direct tool calls.
"""

import asyncio
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent_core.api import orchestrator

def inspect_global_orchestrator_memory():
    """Inspect the global orchestrator's memory state"""
    
    print("🔍 INSPECTING GLOBAL ORCHESTRATOR MEMORY")
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
    
    # Inspect global orchestrator state
    print("🔍 GLOBAL ORCHESTRATOR STATE:")
    print(f"   Type: {type(orchestrator)}")
    print(f"   ID: {id(orchestrator)}")
    print(f"   Memory Keys: {list(orchestrator.conversation_memory.keys())}")
    print(f"   Memory Size: {len(orchestrator.conversation_memory)}")
    print()
    
    # Check if our test session exists in global memory
    test_session_id = "test-session-4g-carrier-aggregation"
    if test_session_id in orchestrator.conversation_memory:
        print(f"✅ Test session '{test_session_id}' found in global memory")
        session_data = orchestrator.conversation_memory[test_session_id]
        print(f"   Messages: {len(session_data.get('messages', []))}")
        print(f"   Last Updated: {session_data.get('last_updated', 'N/A')}")
        
        if session_data.get('messages'):
            print("   Message Preview:")
            for i, msg in enumerate(session_data['messages'][:3]):
                print(f"     {i+1}. Role: {msg.get('role', 'N/A')}, Content: {msg.get('content', 'N/A')[:100]}...")
    else:
        print(f"❌ Test session '{test_session_id}' NOT found in global memory")
    
    print()
    
    # Check other sessions in global memory
    other_sessions = [k for k in orchestrator.conversation_memory.keys() if k != test_session_id]
    if other_sessions:
        print("🔍 OTHER SESSIONS IN GLOBAL MEMORY:")
        for session_id in other_sessions[:5]:  # Show first 5
            session_data = orchestrator.conversation_memory[session_id]
            print(f"   Session: {session_id}")
            print(f"     Messages: {len(session_data.get('messages', []))}")
            print(f"     Last Updated: {session_data.get('last_updated', 'N/A')}")
            if session_data.get('messages'):
                first_msg = session_data['messages'][0]
                print(f"     First Message: {first_msg.get('role', 'N/A')} - {first_msg.get('content', 'N/A')[:100]}...")
            print()
    
    # Test setting memory in global orchestrator
    print("🔍 TESTING MEMORY SETTING IN GLOBAL ORCHESTRATOR:")
    print(f"   About to set memory for session: {test_session_id}")
    
    # Set the memory exactly as the API would
    orchestrator.conversation_memory[test_session_id] = {
        "messages": test_data['conversation_history'],
        "created_at": "2025-08-27T23:45:00.000Z"
    }
    
    print(f"   ✅ Memory set successfully")
    print(f"   Memory keys after setting: {list(orchestrator.conversation_memory.keys())}")
    print(f"   Test session messages: {len(orchestrator.conversation_memory[test_session_id]['messages'])}")
    
    # Verify the data was stored correctly
    stored_messages = orchestrator.conversation_memory[test_session_id]["messages"]
    print(f"   First stored message: {stored_messages[0].get('role', 'N/A')} - {stored_messages[0].get('content', 'N/A')[:100]}...")
    print(f"   Second stored message: {stored_messages[1].get('role', 'N/A')} - {stored_messages[1].get('content', 'N/A')[:100]}...")
    
    print()
    
    # Test context building with global orchestrator
    print("🔍 TESTING CONTEXT BUILDING WITH GLOBAL ORCHESTRATOR:")
    enhanced_context = orchestrator._build_enhanced_context(
        context="patent_streaming",
        document_content=test_data['document_content'],
        session_id=test_session_id
    )
    
    print(f"   Enhanced context length: {len(enhanced_context)} characters")
    print(f"   Enhanced context preview: {enhanced_context[:500]}...")
    
    print()
    
    # Test conversation history retrieval
    print("🔍 TESTING CONVERSATION HISTORY RETRIEVAL:")
    retrieved_history = orchestrator.conversation_memory.get(test_session_id, {}).get("messages", [])
    print(f"   Retrieved history length: {len(retrieved_history)}")
    if retrieved_history:
        print(f"   First entry keys: {list(retrieved_history[0].keys())}")
        print(f"   First entry role: {retrieved_history[0].get('role', 'N/A')}")
        print(f"   First entry content preview: {retrieved_history[0].get('content', 'N/A')[:100]}...")
    
    print()
    print("✅ Global orchestrator memory inspection completed")

if __name__ == "__main__":
    inspect_global_orchestrator_memory()
