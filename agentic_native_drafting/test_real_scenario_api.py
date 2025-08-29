#!/usr/bin/env python3
"""
Real Scenario API Test
Tests the exact scenario provided by the user:
- Document content with 4G carrier aggregation system claims
- User query: "draft the corresponding method claims"
- Calls actual API and stores output
"""

import asyncio
import json
import httpx
import time
from datetime import datetime

async def test_real_scenario_api():
    """Test the real scenario with actual API call"""
    
    print("🔍 REAL SCENARIO API TEST")
    print("=" * 60)
    print("Testing the exact scenario provided by the user:")
    print("- Document content with 4G carrier aggregation claims")
    print("- User query: 'draft the corresponding method claims'")
    print("- Calling actual API endpoint")
    print("=" * 60)
    
    # The exact document content from the user's scenario
    document_content = {
        "text": "Successfully drafted 5 content items\n\nGenerated Patent Claims:\n\nClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\n\nClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\n\nClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\n\nClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\n\nClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.",
        "paragraphs": [
            "Successfully drafted 5 content items",
            "Generated Patent Claims:",
            "Claim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.",
            "Claim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.",
            "Claim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.",
            "Claim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.",
            "Claim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process."
        ],
        "session_id": "test-session-4g-carrier-aggregation"
    }
    
    # The exact user query from the scenario
    user_message = "draft the corresponding method claims"
    
    # Conversation history to provide context
    conversation_history = [
        {
            "role": "user",
            "content": "draft 5 system claims for 4g carrier aggregation",
            "timestamp": "2025-08-27T21:40:00.000Z"
        },
        {
            "role": "assistant",
            "content": "Successfully drafted 5 content items\n\nGenerated Patent Claims:\n\nClaim 1 (primary): A system for 4G carrier aggregation, comprising: a first communication module configured to connect to a first carrier network; a second communication module configured to connect to a second carrier network; and a control unit configured to manage the aggregation of data from the first and second carrier networks to provide a combined data throughput to a user device.\n\nClaim 2 (secondary): The system of claim 1, wherein the control unit is further configured to dynamically adjust the data allocation between the first and second carrier networks based on real-time network conditions.\n\nClaim 3 (secondary): The system of claim 1, wherein the first and second communication modules support different frequency bands for the first and second carrier networks, respectively.\n\nClaim 4 (secondary): The system of claim 1, further comprising a user interface for displaying the status of the carrier aggregation and the data throughput from the first and second carrier networks.\n\nClaim 5 (secondary): The system of claim 1, wherein the control unit is configured to prioritize data traffic based on user-defined preferences and application requirements during the carrier aggregation process.",
            "timestamp": "2025-08-27T21:43:00.000Z"
        }
    ]
    
    # Prepare the API request payload
    api_payload = {
        "user_message": user_message,
        "conversation_history": conversation_history,
        "document_content": document_content,
        "session_id": "test-session-4g-carrier-aggregation"
    }
    
    print(f"\n📤 API REQUEST DETAILS:")
    print(f"User Message: {user_message}")
    print(f"Document Content Length: {len(document_content['text'])} characters")
    print(f"Conversation History: {len(conversation_history)} entries")
    print(f"Session ID: {document_content['session_id']}")
    
    print(f"\n📋 DOCUMENT CONTENT PREVIEW:")
    print(f"Claims Found: {len(document_content['paragraphs']) - 2} patent claims")
    print(f"First Claim: {document_content['paragraphs'][2][:100]}...")
    
    print(f"\n🚀 CALLING API ENDPOINT...")
    print("=" * 60)
    
    try:
        # Call the actual API endpoint using the correct frontend flow
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Step 1: Start a patent run (POST /api/patent/run)
            print("📤 Step 1: Starting patent run...")
            run_response = await client.post(
                "http://localhost:8001/api/patent/run",
                json=api_payload,
                headers={"Content-Type": "application/json"}
            )
            
            if run_response.status_code != 200:
                raise Exception(f"Patent run failed: {run_response.status_code}")
            
            run_data = run_response.json()
            run_id = run_data["run_id"]
            session_id = run_data["session_id"]
            print(f"✅ Patent run started: run_id={run_id}, session_id={session_id}")
            
            # Step 2: Stream the response (GET /api/patent/stream?run_id=X)
            print("📤 Step 2: Streaming response...")
            response = await client.get(
                f"http://localhost:8001/api/patent/stream?run_id={run_id}",
                headers={"Accept": "text/event-stream"}
            )
            
            if response.status_code == 200:
                print("✅ API call successful (200)")
                
                # Process streaming response
                print(f"\n📥 PROCESSING STREAMING RESPONSE...")
                print("=" * 60)
                
                events = []
                full_response = ""
                results_event = None
                
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]  # Remove "data: " prefix
                        if data.strip() == "[DONE]":
                            break
                        
                        try:
                            event = json.loads(data)
                            events.append(event)
                            
                            event_type = event.get('event', 'unknown')
                            print(f"📥 Event: {event_type}")
                            
                            if event_type == 'thoughts':
                                content = event.get('content', '')
                                print(f"   💭 {content[:100]}{'...' if len(content) > 100 else ''}")
                            elif event_type == 'results':
                                results_event = event
                                response_text = event.get('response', '')
                                full_response = response_text
                                print(f"   ✅ RESULTS: {response_text[:200]}...")
                            elif event_type == 'error':
                                error_msg = event.get('error', '')
                                print(f"   ❌ ERROR: {error_msg}")
                            
                        except json.JSONDecodeError as e:
                            print(f"   ⚠️  JSON parse error: {e}")
                            continue
                
                # Store the complete output
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = f"real_scenario_output_{timestamp}.json"
                
                output_data = {
                    "test_info": {
                        "scenario": "4G Carrier Aggregation - Corresponding Method Claims",
                        "timestamp": datetime.now().isoformat(),
                        "user_message": user_message,
                        "document_content": document_content,
                        "conversation_history": conversation_history
                    },
                    "api_response": {
                        "status_code": response.status_code,
                        "total_events": len(events),
                        "events": events,
                        "full_response": full_response,
                        "results_event": results_event
                    }
                }
                
                with open(output_filename, 'w') as f:
                    json.dump(output_data, f, indent=2)
                
                print(f"\n💾 OUTPUT STORED TO: {output_filename}")
                
                # Analyze the results
                print(f"\n🏆 RESULTS ANALYSIS:")
                print("=" * 60)
                
                if results_event:
                    response_text = results_event.get('response', '')
                    
                    # Check if method claims were generated
                    if 'method' in response_text.lower():
                        print("✅ SUCCESS: Generated method claims")
                    else:
                        print("❌ FAILURE: No method claims generated")
                    
                    # Check if it maintains 4G carrier aggregation context
                    if 'carrier aggregation' in response_text.lower() or '4g' in response_text.lower():
                        print("✅ SUCCESS: Maintains 4G carrier aggregation context")
                    else:
                        print("❌ FAILURE: Lost 4G carrier aggregation context")
                    
                    # Check if it's specific to the invention or generic
                    if 'patent claim' in response_text.lower() and 'invention' in response_text.lower():
                        print("❌ FAILURE: Generated generic patent drafting claims")
                    else:
                        print("✅ SUCCESS: Generated specific method claims for the invention")
                    
                    # Count the claims generated
                    claim_count = response_text.count('Claim')
                    print(f"📊 Claims Generated: {claim_count}")
                    
                    print(f"\n📋 FULL API RESPONSE:")
                    print(response_text)
                    
                else:
                    print("❌ FAILURE: No results event in API response")
                    print(f"Events received: {[e.get('event') for e in events]}")
                
            else:
                print(f"❌ API call failed with status code: {response.status_code}")
                print(f"Response: {response.text}")
                
    except Exception as e:
        print(f"💥 Error calling API: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\n🎯 TEST COMPLETED")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(test_real_scenario_api())
