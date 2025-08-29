#!/usr/bin/env python3
"""
Test Real API Data

This script tests with the exact real API data to confirm the
conversation history mismatch issue.
"""

import asyncio
import sys
import os
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.agent_core.api import orchestrator

async def test_real_api_data():
    """Test with the exact real API data to confirm the issue"""
    
    print("🔍 TESTING WITH REAL API DATA")
    print("=" * 60)
    
    # EXACT data from your real API call
    real_api_data = {
        "user_message": "draft the  corresponding method claims",
        "conversation_history": [
            {
                "role": "user",
                "content": "draft the  corresponding method claims",
                "timestamp": "2025-08-28T01:59:11.994Z"
            },
            {
                "role": "assistant",
                "content": "Successfully drafted 5 content items\n\n**Generated Patent Claims:**\n\n**Claim 1** (primary):\nA method for enhancing the performance of a machine learning model, comprising: collecting a dataset comprising labeled training data; preprocessing the dataset to remove noise and irrelevant features; training the machine learning model on the preprocessed dataset; evaluating the performance of the trained model using a validation dataset; and iteratively refining the model based on the evaluation results until a desired performance threshold is achieved.\n\n**Claim 2** (secondary):\nThe method of claim 1, wherein the preprocessing step includes normalization of the data and feature selection based on statistical significance.\n\n**Claim 3** (secondary):\nThe method of claim 1, further comprising the step of deploying the trained model to a production environment after achieving the desired performance threshold.\n\n**Claim 4** (secondary):\nThe method of claim 1, wherein the machine learning model is selected from the group consisting of decision trees, neural networks, and support vector machines.\n\n**Claim 5** (secondary):\nThe method of claim 1, wherein the evaluation of the model's performance includes metrics selected from the group consisting of accuracy, precision, recall, and F1 score.\n",
                "timestamp": "2025-08-28T01:59:24.551Z",
                "thoughts": ["Processing request: draft the  corresponding method claims...", "Analyzing user intent...", "Routing to ContentDraftingTool...", "Executing ContentDraftingTool...", "Starting content drafting process for 38 character input", "Assessing input sufficiency for content drafting...", "Input sufficiency score is low (0.40). Consider enhancing the input.", "Drafting content using LLM analysis..."],
                "thoughtsExpanded": True
            },
            {
                "role": "user",
                "content": "draft the  corresponding method claims",
                "timestamp": "2025-08-28T03:43:04.281Z"
            },
            {
                "role": "assistant",
                "content": "Successfully drafted 5 content items\n\n**Generated Patent Claims:**\n\n**Claim 1** (primary):\nA method for enhancing the performance of a machine learning model, comprising: collecting a dataset comprising labeled training data; preprocessing the dataset to remove noise and irrelevant features; training the machine learning model on the preprocessed dataset; evaluating the performance of the trained model using a validation dataset; and iteratively refining the model based on the evaluation results until a desired performance threshold is achieved.\n\n**Claim 2** (secondary):\nThe method of claim 1, wherein the preprocessing step includes normalization of the data and feature selection based on statistical significance.\n\n**Claim 3** (secondary):\nThe method of claim 1, further comprising the step of deploying the trained model to a production environment after achieving the desired performance threshold.\n\n**Claim 4** (secondary):\nThe method of claim 1, wherein the machine learning model is selected from the group consisting of decision trees, neural networks, and support vector machines.\n\n**Claim 5** (secondary):\nThe method of claim 1, wherein the evaluation of the model's performance includes metrics selected from the group consisting of accuracy, precision, recall, and F1 score.\n",
                "timestamp": "2025-08-28T03:43:11.893Z",
                "thoughts": ["Processing request: draft the  corresponding method claims...", "Analyzing user intent...", "Routing to ContentDraftingTool...", "Executing ContentDraftingTool...", "Starting content drafting process for 38 character input", "Assessing input sufficiency for content drafting...", "Input sufficiency score is low (0.40). Consider enhancing the input.", "Drafting content using LLM analysis..."],
                "thoughtsExpanded": True
            }
        ],
        "document_content": {
            "text": "Successfully drafted 5 content items\rGenerated Patent Claims:\rClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\rClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\rClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\rClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\rClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.\r\r",
            "paragraphs": ["Successfully drafted 5 content items\rGenerated Patent Claims:\rClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\rClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\rClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\rClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\rClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.\r\r"],
            "session_id": "06f74125-f6ad-48a9-bc32-5db0ff1697a5"
        },
        "session_id": "06f74125-f6ad-48a9-bc32-5db0ff1697a5"
    }
    
    print("📋 REAL API DATA ANALYSIS:")
    print(f"   User Message: {real_api_data['user_message']}")
    print(f"   Conversation History: {len(real_api_data['conversation_history'])} entries")
    print(f"   Document Content Length: {len(real_api_data['document_content']['text'])} characters")
    print(f"   Session ID: {real_api_data['session_id']}")
    print()
    
    # Analyze the conversation history
    print("🔍 CONVERSATION HISTORY ANALYSIS:")
    print("-" * 40)
    
    for i, entry in enumerate(real_api_data['conversation_history']):
        role = entry.get('role', 'unknown')
        content = entry.get('content', '')
        timestamp = entry.get('timestamp', 'unknown')
        
        print(f"Entry {i+1} ({role}):")
        print(f"  Timestamp: {timestamp}")
        
        if role == "user":
            print(f"  Content: {content}")
        elif role == "assistant":
            # Check what type of claims this contains
            if "machine learning" in content.lower() or "ml model" in content.lower():
                print(f"  ❌ CONTAINS: Machine Learning Claims")
            elif "4g" in content.lower() or "carrier aggregation" in content.lower():
                print(f"  ✅ CONTAINS: 4G Carrier Aggregation Claims")
            else:
                print(f"  ❓ CONTAINS: Unknown/Generic Claims")
            
            # Show first 100 chars
            print(f"  Preview: {content[:100]}...")
        print()
    
    # Analyze the document content
    print("🔍 DOCUMENT CONTENT ANALYSIS:")
    print("-" * 40)
    
    doc_text = real_api_data['document_content']['text']
    if "4g" in doc_text.lower() or "carrier aggregation" in doc_text.lower():
        print("✅ CONTAINS: 4G Carrier Aggregation Claims")
    else:
        print("❌ DOES NOT CONTAIN: 4G Carrier Aggregation Claims")
    
    print(f"Content Preview: {doc_text[:200]}...")
    print()
    
    # Now test with this real data
    print("🔍 TESTING WITH REAL API DATA:")
    print("-" * 40)
    
    # Extract variables exactly as the API does
    user_input = real_api_data["user_message"]
    session_id = real_api_data["session_id"]
    conversation_history = real_api_data["conversation_history"]
    document_content = real_api_data["document_content"]
    context = "patent_streaming"
    
    # Set orchestrator memory exactly as the API does
    orchestrator.conversation_memory[session_id] = {
        "messages": conversation_history,
        "created_at": datetime.now().isoformat()
    }
    
    print(f"✅ Set memory for session '{session_id}' with {len(conversation_history)} messages")
    
    # Call orchestrator.handle exactly as the API does
    event_count = 0
    results_event = None
    
    try:
        async for event in orchestrator.handle(
            user_input, 
            context, 
            session_id,
            parameters={
                "domain": "patent",
                "workflow_type": "patent_streaming",
                "session_id": session_id
            },
            document_content=document_content
        ):
            event_count += 1
            print(f"📥 Event {event_count}: {event.get('event', 'unknown')}")
            
            if event.get("event") == "results":
                results_event = event
                print(f"✅ SUCCESS: Got results event")
                print(f"   Response: {event.get('response', 'No response')}")
                if 'data' in event and 'content' in event['data']:
                    print(f"   Content items: {len(event['data']['content'])}")
                    for i, item in enumerate(event['data']['content'][:3]):  # Show first 3
                        print(f"     Item {i+1}: {item.get('content_text', 'No text')[:100]}...")
                break
            elif event_count > 15:  # Prevent infinite loop
                print("⚠️  WARNING: Too many events, stopping")
                break
        
        print(f"✅ Orchestrator execution completed with {event_count} events")
        
    except Exception as e:
        print(f"❌ Orchestrator execution failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Final analysis
    print("🔍 FINAL ANALYSIS:")
    print("-" * 40)
    
    if results_event:
        print("✅ TEST COMPLETED SUCCESSFULLY")
        
        # Check if we got the right type of claims
        if 'data' in results_event and 'content' in results_event['data']:
            content_items = results_event['data']['content']
            print(f"   Generated {len(content_items)} content items")
            
            # Check if any contain 4G carrier aggregation
            has_4g_context = any(
                "4g" in item.get('content_text', '').lower() or 
                "carrier aggregation" in item.get('content_text', '').lower()
                for item in content_items
            )
            
            if has_4g_context:
                print("   ✅ SUCCESS: Generated claims contain 4G carrier aggregation context")
                print("   This means the issue is NOT in the backend code!")
            else:
                print("   ❌ FAILURE: Generated claims do NOT contain 4G carrier aggregation context")
                print("   This confirms the conversation history mismatch issue!")
                
                # Check what we actually got
                print("   Generated claims contain:")
                for i, item in enumerate(content_items[:2]):
                    content_text = item.get('content_text', '')
                    if "machine learning" in content_text.lower():
                        print(f"     Item {i+1}: Machine Learning Claims ✅ (Expected behavior)")
                    elif "4g" in content_text.lower():
                        print(f"     Item {i+1}: 4G Claims ❌ (Unexpected - should be ML)")
                    else:
                        print(f"     Item {i+1}: Generic Claims ❓")
    else:
        print("❌ TEST FAILED")
        print("   No results event received")
    
    print()
    print("✅ Real API data test completed")

if __name__ == "__main__":
    asyncio.run(test_real_api_data())
