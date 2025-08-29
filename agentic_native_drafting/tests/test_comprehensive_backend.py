#!/usr/bin/env python3
"""
Comprehensive test for the entire new backend.
Tests all components to ensure they work without legacy dependencies.
"""

import asyncio
import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

async def test_comprehensive_backend():
    """Test the entire new backend comprehensively"""
    
    print("🧪 COMPREHENSIVE NEW BACKEND TEST")
    print("=" * 60)
    
    # Test 1: Import all components
    print("📦 Test 1: Importing all components")
    print("-" * 40)
    
    try:
        # Test core imports
        from src.utils.llm_client import llm_client, send_llm_request_streaming
        print("✅ LLM client imported")
        
        from src.utils.enums import IntentType
        print("✅ Enums imported")
        
        from src.utils.new_models import SearchConfig, SearchResult
        print("✅ Models imported")
        
        from src.utils.patent_search_utils import EnhancedSearchAPI
        print("✅ Patent search utils imported")
        
        from src.utils.response_standardizer import create_thought_event
        print("✅ Response standardizer imported")
        
        from src.agent_core.orchestrator import AgentOrchestrator
        print("✅ Orchestrator imported")
        
        from src.tools.claim_drafting_tool import ContentDraftingTool
        print("✅ Claim drafting tool imported")
        
        from src.tools.prior_art_search_tool import PriorArtSearchTool
        print("✅ Prior art search tool imported")
        
        from src.tools.general_conversation_tool import GeneralConversationTool
        print("✅ General conversation tool imported")
        
        print("✅ All components imported successfully!")
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print()
    
    # Test 2: Initialize all components
    print("🔧 Test 2: Initializing all components")
    print("-" * 40)
    
    try:
        # Initialize tools
        claim_tool = ContentDraftingTool()
        print("✅ Claim drafting tool initialized")
        
        prior_art_tool = PriorArtSearchTool()
        print("✅ Prior art search tool initialized")
        
        conversation_tool = GeneralConversationTool()
        print("✅ General conversation tool initialized")
        
        # Initialize orchestrator
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrator initialized")
        
        print("✅ All components initialized successfully!")
        
    except Exception as e:
        print(f"❌ Initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print()
    
    # Test 3: Test intent classification
    print("🧠 Test 3: Testing intent classification")
    print("-" * 40)
    
    test_cases = [
        {
            "input": "Draft content for a 5G system",
            "expected_intent": IntentType.CONTENT_DRAFTING,
            "description": "Content drafting request"
        },
        {
            "input": "Search for content on AI carrier aggregation",
            "expected_intent": IntentType.SEARCH,
            "description": "Content search request"
        },
        {
            "input": "What is a patent?",
            "expected_intent": IntentType.GENERAL_CONVERSATION,
            "description": "General conversation request"
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🧪 Test case {i}: {test_case['description']}")
        print(f"   Input: {test_case['input']}")
        
        try:
            events = []
            async for event in orchestrator.handle(test_case['input'], "Test context", f"test_session_{i}"):
                events.append(event)
                
                if event.get('event') == 'thoughts' and event.get('thought_type') == 'routing':
                    content = event.get('content', '')
                    if test_case['expected_intent'].value in content:
                        print(f"   ✅ Correctly routed to {test_case['expected_intent'].value}")
                    else:
                        print(f"   ❌ Incorrect routing: {content}")
                    break
                
                # Limit events for display
                if len(events) >= 5:
                    print(f"   ⚠️  Too many events, stopping at {len(events)}")
                    break
            
            print(f"   📊 Events generated: {len(events)}")
            
        except Exception as e:
            print(f"   ❌ Test case failed: {e}")
    
    print()
    
    # Test 4: Test tool execution
    print("⚙️  Test 4: Testing tool execution")
    print("-" * 40)
    
    try:
        # Test claim drafting tool
        print("🧪 Testing claim drafting tool...")
        claim_events = []
        async for event in claim_tool.run("Draft claims for a 5G system", "5G wireless communication"):
            claim_events.append(event)
            if len(claim_events) >= 3:
                break
        
        if claim_events:
            print(f"   ✅ Claim drafting tool working: {len(claim_events)} events")
        else:
            print("   ❌ Claim drafting tool failed")
        
        # Test prior art search tool
        print("🧪 Testing prior art search tool...")
        search_events = []
        async for event in prior_art_tool.run("Search for 5G patents", "5G technology"):
            search_events.append(event)
            if len(search_events) >= 3:
                break
        
        if search_events:
            print(f"   ✅ Prior art search tool working: {len(search_events)} events")
        else:
            print("   ❌ Prior art search tool failed")
        
        # Test general conversation tool
        print("🧪 Testing general conversation tool...")
        conv_events = []
        async for event in conversation_tool.run("What is a patent?", "Learning about patents"):
            conv_events.append(event)
            if len(conv_events) >= 3:
                break
        
        if conv_events:
            print(f"   ✅ General conversation tool working: {len(conv_events)} events")
        else:
            print("   ❌ General conversation tool failed")
        
    except Exception as e:
        print(f"❌ Tool execution test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print()
    
    # Test 5: Test missing tool handling
    print("🚫 Test 5: Testing missing tool handling")
    print("-" * 40)
    
    try:
        test_input = "Analyze my invention for technical feasibility"
        events = []
        
        async for event in orchestrator.handle(test_input, "Test context", "missing_tool_test"):
            events.append(event)
            
            if event.get('event') == 'error' and 'tool_not_implemented' in event.get('context', ''):
                print("   ✅ Missing tool handled gracefully")
                print(f"   📤 Error message: {event.get('error', '')[:80]}...")
                break
            
            if len(events) >= 5:
                print("   ⚠️  Missing tool handling not working as expected")
                break
        
        print(f"   📊 Events generated: {len(events)}")
        
    except Exception as e:
        print(f"❌ Missing tool test failed: {e}")
    
    print("\n🎯 Comprehensive backend test completed!")

async def main():
    """Main test execution"""
    await test_comprehensive_backend()

if __name__ == "__main__":
    asyncio.run(main())
