#!/usr/bin/env python3
"""
Test script to verify session memory and context access with the new session management system
"""

import asyncio
import httpx
import json
import time
import pytest

@pytest.mark.asyncio
async def test_session_memory():
    """Test if the agent can access session context and previous claims"""
    
    base_url = "http://127.0.0.1:8000"
    session_id = None
    
    async with httpx.AsyncClient() as client:
        
        # Step 1: Start a session and generate claims
        print("🆕 Step 1: Starting session and generating claims...")
        
        response = await client.post(f"{base_url}/api/patent/run", json={
            "user_message": "Please draft patent claims for my 5G AI carrier aggregation system that uses machine learning to dynamically select and combine multiple frequency carriers based on real-time network conditions.",
            "conversation_history": [],
            "document_content": {"text": ""}
        })
        
        if response.status_code != 200:
            print(f"❌ Failed to start session: {response.status_code}")
            return
            
        run_data = response.json()
        run_id = run_data.get('run_id')
        session_id = run_data.get('session_id')
        
        print(f"✅ Session started: {session_id}")
        print(f"✅ Run ID: {run_id}")
        
        # Step 2: Stream the response to get claims
        print("\n🔄 Step 2: Streaming response to get generated claims...")
        
        async with client.stream('GET', f"{base_url}/api/patent/stream", params={'run_id': run_id}, timeout=120.0) as stream_response:
            claims = []
            current_event = None
            current_data = []
            in_data_section = False
            
            async for line in stream_response.aiter_lines():
                line = line.strip()
                
                if line.startswith("event: "):
                    # Process previous event if we have one
                    if current_event and current_data:
                        if current_event == "final":
                            try:
                                combined_data = "".join(current_data)
                                print(f"🔍 Debug: Event {current_event}, data lines: {len(current_data)}")
                                print(f"🔍 Debug: Combined data: {combined_data}")
                                data = json.loads(combined_data)
                                if 'data' in data and 'claims' in data['data']:
                                    claims = data['data']['claims']
                                    print(f"✅ Generated {len(claims)} claims")
                                    for i, claim in enumerate(claims[:2], 1):
                                        print(f"   {i}. {claim[:100]}...")
                                    break
                            except json.JSONDecodeError as e:
                                print(f"⚠️  JSON parse error: {e}")
                                print(f"⚠️  Raw data: {combined_data[:200]}...")
                                print(f"🔍 Debug: All data lines: {current_data}")
                    
                    # Start new event
                    current_event = line[7:].strip()
                    current_data = []
                    in_data_section = False
                    
                elif line.startswith("data: "):
                    data_str = line[6:].strip()
                    if data_str:
                        current_data.append(data_str)
                    in_data_section = True
                elif in_data_section:  # Capture all lines while in data section
                    current_data.append(line)
                elif line == "" and in_data_section:
                    # Empty line within data section - continue accumulating
                    current_data.append(line)
                elif line == "" and not in_data_section:
                    # Empty line outside data section - end of event
                    if current_event and current_data:
                        if current_event == "final":
                            try:
                                combined_data = "".join(current_data)
                                print(f"🔍 Debug: Event {current_event}, data lines: {len(current_data)}")
                                print(f"🔍 Debug: Combined data: {combined_data}")
                                data = json.loads(combined_data)
                                if 'data' in data and 'claims' in data['data']:
                                    claims = data['data']['claims']
                                    print(f"✅ Generated {len(claims)} claims")
                                    for i, claim in enumerate(claims[:2], 1):
                                        print(f"   {i}. {claim[:100]}...")
                                    break
                            except json.JSONDecodeError as e:
                                print(f"⚠️  JSON parse error: {e}")
                                print(f"⚠️  Raw data: {combined_data[:200]}...")
                                print(f"🔍 Debug: All data lines: {current_data}")
        
        if not claims:
            print("❌ No claims generated, cannot test session memory")
            return
        
        # Step 3: Continue the same session to test context access
        print(f"\n🔄 Step 3: Continuing session {session_id} to test context access...")
        
        response = await client.post(f"{base_url}/api/patent/run", json={
            "user_message": "How many claims did you generate for my 5G AI system?",
            "conversation_history": [],
            "document_content": {"text": ""},
            "session_id": session_id
        })
        
        if response.status_code != 200:
            print(f"❌ Failed to continue session: {response.status_code}")
            return
            
        run_data = response.json()
        continue_run_id = run_data.get('run_id')
        continue_session_id = run_data.get('session_id')
        
        print(f"✅ Continued session: {continue_session_id}")
        print(f"✅ New Run ID: {continue_run_id}")
        
        # Verify we're using the same session
        if continue_session_id != session_id:
            print("❌ Session ID mismatch - context not being shared")
            return
        else:
            print("✅ Same session ID - context should be shared")
        
        # Step 4: Stream the continued session response
        print("\n🔄 Step 4: Streaming continued session response...")
        
        async with client.stream('GET', f"{base_url}/api/patent/stream", params={'run_id': continue_run_id}, timeout=120.0) as stream_response:
            context_response = ""
            current_event = None
            current_data = []
            
            async for line in stream_response.aiter_lines():
                line = line.strip()
                
                if line.startswith("event: "):
                    # Process previous event if we have one
                    if current_event and current_data:
                        if current_event == "final":
                            try:
                                combined_data = "".join(current_data)
                                data = json.loads(combined_data)
                                context_response = data.get('response', '')
                                print(f"✅ Context response: {context_response[:200]}...")
                                break
                            except json.JSONDecodeError as e:
                                print(f"⚠️  JSON parse error: {e}")
                    
                    # Start new event
                    current_event = line[7:].strip()
                    current_data = []
                    
                elif line.startswith("data: "):
                    data_str = line[6:].strip()
                    if data_str:
                        current_data.append(data_str)
        
        # Step 5: Analyze context awareness
        print("\n🔍 Step 5: Analyzing context awareness...")
        
        # Check if response shows awareness of the 5G AI system
        context_keywords = ['5g', 'ai', 'carrier', 'frequency', 'machine learning']
        context_awareness = any(keyword in context_response.lower() for keyword in context_keywords)
        
        if context_awareness:
            print("✅ Response shows context awareness of the 5G AI system")
            print("✅ Session memory is working correctly!")
        else:
            print("❌ Response lacks context awareness")
            print("❌ Session memory may not be working")
        
        # Step 6: Check session information
        print(f"\n🔍 Step 6: Checking session information for {session_id}...")
        
        try:
            session_response = await client.get(f"{base_url}/api/debug/session/{session_id}")
            if session_response.status_code == 200:
                session_data = session_response.json()
                runs = session_data.get('runs', [])
                history_length = len(session_data.get('session_history', ''))
                topic = session_data.get('topic', 'N/A')
                
                print(f"✅ Session runs: {len(runs)}")
                print(f"✅ Session history: {history_length} characters")
                print(f"✅ Session topic: {topic}")
                
                if len(runs) >= 2:
                    print("✅ Session contains multiple runs - context sharing working!")
                else:
                    print("⚠️  Session has fewer runs than expected")
            else:
                print(f"❌ Failed to get session info: {session_response.status_code}")
        except Exception as e:
            print(f"❌ Error getting session info: {e}")
        
        print("\n🎉 Session memory test completed!")

async def main():
    """Main test runner"""
    print("🚀 Testing Session Memory and Context Access")
    print("=" * 50)
    await test_session_memory()

if __name__ == "__main__":
    asyncio.run(main())
