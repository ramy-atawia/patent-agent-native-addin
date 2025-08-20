#!/usr/bin/env python3
"""
Simple CLI Chat Interface for Patent Drafting Agent
Works with the simplified agent system
"""

import asyncio
import json
import httpx
import sys
from typing import Optional

class SimpleCLIChat:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self.conversation_id: Optional[str] = None
        
    async def test_connection(self) -> bool:
        """Test if the server is running"""
        try:
            response = await self.client.get(f"{self.base_url}/")
            if response.status_code == 200:
                print("✅ Server connection successful!")
                return True
            else:
                print(f"❌ Server responded with status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Cannot connect to server: {e}")
            return False
    
    async def start_conversation(self, user_input: str, session_id: str = None) -> str:
        """Start a new conversation or continue existing session"""
        try:
            # Send labeled payload compatible with UI: user_message, conversation_history, document_content
            payload = {"user_message": user_input}
            if session_id:
                payload["session_id"] = session_id
                print(f"🔄 Continuing session: {session_id}")
            
            response = await self.client.post(
                f"{self.base_url}/api/patent/run",
                json=payload
            )
            
            if response.status_code == 200:
                result = response.json()
                run_id = result.get("run_id")
                new_session_id = result.get("session_id")
                
                if session_id:
                    print(f"✅ Continued session {session_id} with run {run_id}")
                else:
                    print(f"🆕 Started new session {new_session_id} with run {run_id}")
                
                return run_id
            else:
                print(f"❌ Failed to start run: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error starting conversation: {e}")
            return None

    async def continue_session(self, user_input: str, session_id: str) -> str:
        """Continue an existing session"""
        return await self.start_conversation(user_input, session_id)

    async def list_sessions(self) -> list:
        """List all active sessions"""
        try:
            response = await self.client.get(f"{self.base_url}/api/sessions")
            if response.status_code == 200:
                data = response.json()
                return data.get("sessions", [])
            else:
                print(f"❌ Failed to list sessions: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ Error listing sessions: {e}")
            return []
    
    async def stream_response(self, run_id: str) -> dict:
        """Stream the response and collect all events"""
        try:
            response = await self.client.get(
                f"{self.base_url}/api/patent/stream",
                params={"run_id": run_id}
            )
            
            if response.status_code != 200:
                print(f"❌ Stream failed: {response.status_code}")
                return {}
            
            # Parse SSE response - handle multiline data properly
            events = {}
            content = response.text
            
            lines = content.split('\n')
            i = 0
            while i < len(lines):
                line = lines[i].strip()
                
                if line.startswith('event:'):
                    event_type = line.split(':', 1)[1].strip()
                    
                    # Look for the corresponding data
                    data_lines = []
                    i += 1
                    while i < len(lines) and not lines[i].strip().startswith('event:'):
                        if lines[i].strip().startswith('data:'):
                            data_content = lines[i].split(':', 1)[1].strip()
                            data_lines.append(data_content)
                        i += 1
                    
                    # Combine multiline data
                    if data_lines:
                        combined_data = '\n'.join(data_lines)
                        try:
                            if combined_data == "{}":
                                events[event_type] = {}
                            else:
                                data = json.loads(combined_data)
                                events[event_type] = data
                        except json.JSONDecodeError as e:
                            print(f"⚠️  JSON parse error for {event_type}: {e}")
                            print(f"⚠️  Raw data: {combined_data[:100]}...")
                            events[event_type] = combined_data
                else:
                    i += 1
            
            print(f"🔍 Debug: Parsed events: {list(events.keys())}")
            return events
            
        except Exception as e:
            print(f"❌ Error streaming response: {e}")
            return {}
    
    async def chat(self, user_input: str):
        """Main chat function"""
        print(f"\n🤖 Processing: {user_input[:100]}{'...' if len(user_input) > 100 else ''}")
        print("=" * 80)
        
        # Start conversation
        run_id = await self.start_conversation(user_input)
        if not run_id:
            return
        
        # Stream response
        events = await self.stream_response(run_id)
        
        # Display results
        if 'final' in events:
            final_data = events['final']
            response = final_data.get('response', 'No response received')
            metadata = final_data.get('metadata', {})
            
            print(f"\n📝 Response:")
            print(response)
            
            if metadata.get('should_draft_claims') and 'data' in final_data:
                claims = final_data['data'].get('claims', [])
                print(f"\n🔍 Generated {len(claims)} claims:")
                for i, claim in enumerate(claims, 1):
                    print(f"  {i}. {claim}")
            
            if metadata.get('reasoning'):
                print(f"\n💭 Reasoning: {metadata['reasoning']}")
                
        elif 'error' in events:
            error_data = events['error']
            print(f"❌ Error: {error_data}")
        else:
            print("⚠️  No final response received")
            print(f"Available events: {list(events.keys())}")
        
        print("=" * 80)
    
    async def interactive_chat(self):
        """Interactive chat loop"""
        print("🚀 Simple Patent Drafting Chat")
        print("Type 'quit' to exit, 'help' for commands")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() == 'help':
                    self.show_help()
                    continue
                elif user_input.lower() == 'status':
                    await self.show_status()
                    continue
                elif not user_input:
                    continue
                
                await self.chat(user_input)
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Unexpected error: {e}")
    
    def show_help(self):
        """Show available commands"""
        print("\n📚 Available Commands:")
        print("  help     - Show this help message")
        print("  status   - Check server status")
        print("  quit     - Exit the chat")
        print("\n💡 Examples:")
        print("  'I have invented a 5G AI system for dynamic spectrum sharing'")
        print("  'Can you help me understand patent claims?'")
        print("  'What makes a good invention disclosure?'")
    
    async def show_status(self):
        """Check server status"""
        try:
            response = await self.client.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"\n🟢 Server Status: {data.get('status', 'unknown')}")
                print(f"   Service: {data.get('service', 'unknown')}")
                print(f"   Version: {data.get('version', 'unknown')}")
                print(f"   Functions: {', '.join(data.get('functions', []))}")
            else:
                print(f"🔴 Server Status: Error {response.status_code}")
        except Exception as e:
            print(f"🔴 Server Status: Cannot connect - {e}")
    
    async def close(self):
        """Close the client"""
        await self.client.aclose()

async def main():
    """Main function"""
    chat = SimpleCLIChat()
    
    try:
        # Test connection first
        if not await chat.test_connection():
            print("❌ Cannot connect to server. Make sure it's running on http://127.0.0.1:8001")
            return
        
        # Start interactive chat
        await chat.interactive_chat()
        
    finally:
        await chat.close()

if __name__ == "__main__":
    asyncio.run(main())
