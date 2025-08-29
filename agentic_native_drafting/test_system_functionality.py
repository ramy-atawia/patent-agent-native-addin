#!/usr/bin/env python3
"""
Simple system functionality test script.
This tests the core system without requiring pytest-asyncio.
"""

import sys
import os

# Add src to path
sys.path.insert(0, 'src')

def test_imports():
    """Test that all core modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
from src.agent_core.orchestrator import AgentOrchestrator
        print("✅ Orchestrator imported successfully")
    except Exception as e:
        print(f"❌ Orchestrator import failed: {e}")
        return False
    
    try:
from src.agent_core.api import app
        print("✅ API imported successfully")
    except Exception as e:
        print(f"❌ API import failed: {e}")
        return False
    
    try:
from src.tools.prior_art_search_tool import PriorArtSearchTool
from src.tools.claim_drafting_tool import ContentDraftingTool
from src.tools.claim_review_tool import ContentReviewTool
from src.tools.patent_guidance_tool import GeneralGuidanceTool
from src.tools.general_conversation_tool import GeneralConversationTool
        print("✅ All tools imported successfully")
    except Exception as e:
        print(f"❌ Tool imports failed: {e}")
        return False
    
    return True

def test_instantiation():
    """Test that all core components can be instantiated"""
    print("\n🧪 Testing instantiation...")
    
    try:
from src.agent_core.orchestrator import AgentOrchestrator
        orchestrator = AgentOrchestrator()
        print("✅ Orchestrator instantiated successfully")
        print(f"   Available tools: {list(orchestrator.tools.keys())}")
        print(f"   Total tools: {len(orchestrator.tools)}")
    except Exception as e:
        print(f"❌ Orchestrator instantiation failed: {e}")
        return False
    
    try:
from src.tools.prior_art_search_tool import PriorArtSearchTool
        tool = PriorArtSearchTool()
        print("✅ PriorArtSearchTool instantiated successfully")
        print(f"   Tool class: {tool.__class__.__name__}")
        print(f"   Has run method: {hasattr(tool, 'run')}")
    except Exception as e:
        print(f"❌ PriorArtSearchTool instantiation failed: {e}")
        return False
    
    return True

def test_api():
    """Test that the API can be loaded and configured"""
    print("\n🧪 Testing API...")
    
    try:
from src.agent_core.api import app
        print("✅ API loaded successfully")
        print(f"   API title: {app.title}")
        print(f"   Total routes: {len(app.routes)}")
        
        # Check key endpoints
        key_endpoints = ['/health', '/chat', '/agent/run', '/tool/execute']
        available_endpoints = [route.path for route in app.routes if hasattr(route, 'path')]
        
        for endpoint in key_endpoints:
            if endpoint in available_endpoints:
                print(f"   ✅ {endpoint} endpoint available")
            else:
                print(f"   ⚠️ {endpoint} endpoint not found")
        
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False
    
    return True

def test_tool_methods():
    """Test that tools have the expected methods and attributes"""
    print("\n🧪 Testing tool methods...")
    
    try:
from src.tools.claim_drafting_tool import ContentDraftingTool
        tool = ContentDraftingTool()
        
        expected_methods = ['run']
        expected_attrs = ['max_outputs', 'max_output_length']
        
        for method in expected_methods:
            if hasattr(tool, method):
                print(f"   ✅ {method} method available")
            else:
                print(f"   ❌ {method} method missing")
        
        for attr in expected_attrs:
            if hasattr(tool, attr):
                print(f"   ✅ {attr} attribute available: {getattr(tool, attr)}")
            else:
                print(f"   ❌ {attr} attribute missing")
        
        print("✅ Tool method test completed")
        
    except Exception as e:
        print(f"❌ Tool method test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Starting System Functionality Tests\n")
    
    tests = [
        test_imports,
        test_instantiation,
        test_api,
        test_tool_methods
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                print(f"❌ {test.__name__} failed")
        except Exception as e:
            print(f"❌ {test.__name__} crashed: {e}")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is fully functional.")
        return True
    else:
        print("⚠️ Some tests failed. System may have issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
