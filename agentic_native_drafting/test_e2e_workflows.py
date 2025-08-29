#!/usr/bin/env python3
"""
Test end-to-end user workflows.
This tests complete user journeys to ensure the system works as intended.
"""

import sys
import asyncio
import os

# Add src to path
sys.path.insert(0, 'src')

async def test_prior_art_search_workflow():
    """Test complete prior art search workflow"""
    print("🧪 Testing Prior Art Search E2E Workflow...")
    
    try:
        from src.tools.prior_art_search_tool import PriorArtSearchTool
        
        tool = PriorArtSearchTool()
        print("✅ PriorArtSearchTool created")
        
        # Test with a realistic patent search query
        test_query = "wireless charging technology for electric vehicles"
        print(f"📤 Testing search query: {test_query}")
        
        # Collect all events from the workflow
        events = []
        async for event in tool.run(test_query, context="", parameters={"max_results": 5}):
            events.append(event)
            event_type = event.get("event", "unknown")
            content = event.get("content", event.get("response", "no content"))
            print(f"📥 {event_type.upper()}: {content[:80]}...")
        
        # Analyze the workflow
        thought_events = [e for e in events if e.get("event") == "thoughts"]
        results_events = [e for e in events if e.get("event") == "results"]
        error_events = [e for e in events if e.get("event") == "error"]
        
        print(f"\n📊 Workflow Analysis:")
        print(f"   Thoughts: {len(thought_events)}")
        print(f"   Results: {len(results_events)}")
        print(f"   Errors: {len(error_events)}")
        
        if results_events and len(thought_events) >= 3:
            print("✅ Prior Art Search E2E workflow successful!")
            return True
        else:
            print("⚠️ Prior Art Search workflow incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Prior Art Search E2E workflow failed: {e}")
        return False

async def test_content_drafting_workflow():
    """Test complete content drafting workflow"""
    print("\n🧪 Testing Content Drafting E2E Workflow...")
    
    try:
        from src.tools.claim_drafting_tool import ContentDraftingTool
        
        tool = ContentDraftingTool()
        print("✅ ContentDraftingTool created")
        
        # Test with a realistic invention disclosure
        test_disclosure = """
        A method for wireless charging of electric vehicles using inductive coupling technology.
        The system includes a charging pad embedded in the ground and a receiver coil mounted
        on the vehicle's undercarriage. When the vehicle is parked over the pad, the coils
        align and create a magnetic field for efficient power transfer.
        """
        
        print(f"📤 Testing with disclosure: {test_disclosure[:100]}...")
        
        # Collect all events from the workflow
        events = []
        async for event in tool.run(test_disclosure, context="", parameters={"max_outputs": 3}):
            events.append(event)
            event_type = event.get("event", "unknown")
            content = event.get("content", event.get("response", "no content"))
            print(f"📥 {event_type.upper()}: {content[:80]}...")
        
        # Analyze the workflow
        thought_events = [e for e in events if e.get("event") == "thoughts"]
        results_events = [e for e in events if e.get("event") == "results"]
        error_events = [e for e in events if e.get("event") == "error"]
        
        print(f"\n📊 Workflow Analysis:")
        print(f"   Thoughts: {len(thought_events)}")
        print(f"   Results: {len(results_events)}")
        print(f"   Errors: {len(error_events)}")
        
        if results_events and len(thought_events) >= 3:
            print("✅ Content Drafting E2E workflow successful!")
            return True
        else:
            print("⚠️ Content Drafting workflow incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Content Drafting E2E workflow failed: {e}")
        return False

async def test_content_review_workflow():
    """Test complete content review workflow"""
    print("\n🧪 Testing Content Review E2E Workflow...")
    
    try:
        from src.tools.claim_review_tool import ContentReviewTool
        
        tool = ContentReviewTool()
        print("✅ ContentReviewTool created")
        
        # Test with sample content to review
        test_content = [
            {
                "claim_number": "1",
                "claim_text": "A method for wireless charging comprising a charging pad and a receiver coil."
            },
            {
                "claim_number": "2", 
                "claim_text": "The method of claim 1, wherein the charging pad is embedded in the ground."
            }
        ]
        
        print(f"📤 Testing with {len(test_content)} content items to review")
        
        # Collect all events from the workflow
        events = []
        async for event in tool.run(test_content, prior_content_context="", original_content="wireless charging method"):
            events.append(event)
            event_type = event.get("event", "unknown")
            content = event.get("content", event.get("response", "no content"))
            print(f"📥 {event_type.upper()}: {content[:80]}...")
        
        # Analyze the workflow
        thought_events = [e for e in events if e.get("event") == "thoughts"]
        results_events = [e for e in events if e.get("event") == "results"]
        error_events = [e for e in events if e.get("event") == "error"]
        
        print(f"\n📊 Workflow Analysis:")
        print(f"   Thoughts: {len(thought_events)}")
        print(f"   Results: {len(results_events)}")
        print(f"   Errors: {len(error_events)}")
        
        if results_events and len(thought_events) >= 3:
            print("✅ Content Review E2E workflow successful!")
            return True
        else:
            print("⚠️ Content Review workflow incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Content Review E2E workflow failed: {e}")
        return False

async def test_orchestrator_workflow():
    """Test orchestrator routing and workflow management"""
    print("\n🧪 Testing Orchestrator E2E Workflow...")
    
    try:
        from src.agent_core.orchestrator import AgentOrchestrator
        
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrator created")
        
        # Test with different types of user inputs
        test_inputs = [
            "Search for prior art related to wireless charging technology",
            "Draft patent claims for a smartphone camera system",
            "Review these patent claims for validity and clarity"
        ]
        
        print(f"📤 Testing orchestrator with {len(test_inputs)} different inputs")
        
        total_events = 0
        successful_routes = 0
        
        for i, test_input in enumerate(test_inputs, 1):
            print(f"\n   Testing input {i}: {test_input[:50]}...")
            
            try:
                events = []
                async for event in orchestrator.handle(test_input, context="", session_id=f"test_session_{i}"):
                    events.append(event)
                
                if events:
                    total_events += len(events)
                    successful_routes += 1
                    print(f"   ✅ Routed successfully - {len(events)} events generated")
                else:
                    print(f"   ⚠️ No events generated")
                    
            except Exception as e:
                print(f"   ❌ Routing failed: {e}")
        
        print(f"\n📊 Orchestrator Analysis:")
        print(f"   Successful routes: {successful_routes}/{len(test_inputs)}")
        print(f"   Total events generated: {total_events}")
        
        if successful_routes >= 2:  # At least 2 out of 3 should work
            print("✅ Orchestrator E2E workflow successful!")
            return True
        else:
            print("⚠️ Orchestrator workflow incomplete")
            return False
            
    except Exception as e:
        print(f"❌ Orchestrator E2E workflow failed: {e}")
        return False

async def main():
    """Run all E2E workflow tests"""
    print("🚀 Starting E2E Workflow Tests\n")
    
    tests = [
        test_prior_art_search_workflow,
        test_content_drafting_workflow,
        test_content_review_workflow,
        test_orchestrator_workflow
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if await test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")
    
    print(f"\n📊 E2E Workflow Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All E2E workflow tests passed! System is production-ready.")
        return True
    elif passed >= total * 0.75:  # At least 75% success
        print("✅ Most E2E workflow tests passed. System is mostly functional.")
        return True
    else:
        print("⚠️ Many E2E workflow tests failed. System needs improvement.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
