#!/usr/bin/env python3
"""
COMPREHENSIVE REALISTIC TEST
============================

This script simulates a realistic user workflow to test the context integration:
1. User starts with initial request
2. Builds conversation history
3. Adds document content
4. Makes follow-up requests that should use context
5. Evaluates the quality and context awareness of responses
"""

import asyncio
import json
import time
from datetime import datetime
from src.agent_core.orchestrator import AgentOrchestrator
from src.tools.prior_art_search_tool import PriorArtSearchTool
from src.tools.claim_drafting_tool import ContentDraftingTool

class RealisticWorkflowTester:
    """Test realistic user workflow with context integration"""
    
    def __init__(self):
        self.orchestrator = AgentOrchestrator()
        self.session_id = f"realistic_test_{int(time.time())}"
        self.conversation_history = []
        self.document_content = {
            "text": "",
            "paragraphs": [],
            "session_id": self.session_id
        }
        self.test_results = []
        
    def add_conversation_entry(self, role: str, content: str):
        """Add entry to conversation history"""
        entry = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        }
        self.conversation_history.append(entry)
        
    def update_document_content(self, text: str, paragraphs: list = None):
        """Update document content"""
        self.document_content["text"] = text
        if paragraphs:
            self.document_content["paragraphs"] = paragraphs
        self.document_content["session_id"] = self.session_id
        
    async def test_workflow_step(self, step_name: str, user_input: str, expected_context_usage: dict):
        """Test a single workflow step and evaluate context usage"""
        print(f"\n{'='*80}")
        print(f"🧪 TESTING STEP: {step_name}")
        print(f"{'='*80}")
        
        print(f"📤 User Input: {user_input}")
        print(f"📤 Conversation History: {len(self.conversation_history)} entries")
        print(f"📤 Document Content: {len(self.document_content['text'])} characters")
        
        # Test with orchestrator
        start_time = time.time()
        events = []
        
        try:
            async for event in self.orchestrator.handle(
                user_input,
                f"Step: {step_name}",
                self.session_id,
                {"workflow_step": step_name},
                self.document_content
            ):
                events.append(event)
                
                # Display events in real-time
                event_type = event.get('event', 'unknown')
                content = event.get('content', 'no content')
                
                if event_type == 'thoughts':
                    print(f"💭 {content[:100]}{'...' if len(content) > 100 else ''}")
                elif event_type == 'results':
                    print(f"✅ RESULTS: {content[:200]}{'...' if len(content) > 200 else ''}")
                elif event_type == 'error':
                    print(f"❌ ERROR: {content}")
                    
        except Exception as e:
            print(f"💥 Error in workflow step: {e}")
            events = []
            
        execution_time = time.time() - start_time
        
        # Evaluate context usage
        context_analysis = self._analyze_context_usage(events, expected_context_usage)
        
        # Store test result
        test_result = {
            "step_name": step_name,
            "user_input": user_input,
            "execution_time": execution_time,
            "events_count": len(events),
            "context_analysis": context_analysis,
            "success": len(events) > 0 and not any(e.get('event') == 'error' for e in events)
        }
        
        self.test_results.append(test_result)
        
        # Display step results
        print(f"\n📊 STEP RESULTS:")
        print(f"   Execution Time: {execution_time:.2f}s")
        print(f"   Events Generated: {len(events)}")
        print(f"   Context Usage: {context_analysis['overall_score']}/100")
        print(f"   Success: {'✅ PASS' if test_result['success'] else '❌ FAIL'}")
        
        return test_result
    
    def _analyze_context_usage(self, events: list, expected_context: dict) -> dict:
        """Analyze how well the system used available context"""
        analysis = {
            "conversation_history_used": False,
            "document_content_used": False,
            "context_awareness": 0,
            "overall_score": 0
        }
        
        # Check if conversation history was referenced
        for event in events:
            content = event.get('content', '').lower()
            if any(phrase in content for phrase in ['previous', 'earlier', 'conversation', 'history']):
                analysis["conversation_history_used"] = True
                
        # Check if document content was referenced
        for event in events:
            content = event.get('content', '').lower()
            if any(phrase in content for phrase in ['document', 'content', 'existing', 'current']):
                analysis["document_content_used"] = True
        
        # Calculate context awareness score
        context_indicators = 0
        if analysis["conversation_history_used"]:
            context_indicators += 1
        if analysis["document_content_used"]:
            context_indicators += 1
            
        analysis["context_awareness"] = context_indicators
        analysis["overall_score"] = (context_indicators / 2) * 100
        
        return analysis
    
    def generate_final_report(self):
        """Generate comprehensive test report"""
        print(f"\n{'='*80}")
        print(f"📊 COMPREHENSIVE TEST REPORT")
        print(f"{'='*80}")
        
        # Overall statistics
        total_steps = len(self.test_results)
        successful_steps = sum(1 for r in self.test_results if r['success'])
        avg_context_score = sum(r['context_analysis']['overall_score'] for r in self.test_results) / total_steps
        avg_execution_time = sum(r['execution_time'] for r in self.test_results) / total_steps
        
        print(f"📈 OVERALL STATISTICS:")
        print(f"   Total Steps: {total_steps}")
        print(f"   Successful Steps: {successful_steps}/{total_steps}")
        print(f"   Success Rate: {(successful_steps/total_steps)*100:.1f}%")
        print(f"   Average Context Score: {avg_context_score:.1f}/100")
        print(f"   Average Execution Time: {avg_execution_time:.2f}s")
        
        # Step-by-step breakdown
        print(f"\n🔍 STEP-BY-STEP BREAKDOWN:")
        for i, result in enumerate(self.test_results, 1):
            status = "✅ PASS" if result['success'] else "❌ FAIL"
            context_score = result['context_analysis']['overall_score']
            print(f"   {i}. {result['step_name']}: {status} (Context: {context_score:.0f}/100)")
        
        # Context usage analysis
        print(f"\n🎯 CONTEXT USAGE ANALYSIS:")
        conversation_usage = sum(1 for r in self.test_results if r['context_analysis']['conversation_history_used'])
        document_usage = sum(1 for r in self.test_results if r['context_analysis']['document_content_used'])
        
        print(f"   Conversation History Used: {conversation_usage}/{total_steps} steps")
        print(f"   Document Content Used: {document_usage}/{total_steps} steps")
        print(f"   Overall Context Utilization: {((conversation_usage + document_usage)/(total_steps*2))*100:.1f}%")
        
        # Recommendations
        print(f"\n💡 RECOMMENDATIONS:")
        if avg_context_score >= 80:
            print(f"   🎉 EXCELLENT: Context integration is working perfectly!")
        elif avg_context_score >= 60:
            print(f"   ✅ GOOD: Context integration is working well with room for improvement")
        elif avg_context_score >= 40:
            print(f"   ⚠️  FAIR: Context integration needs some improvements")
        else:
            print(f"   ❌ POOR: Context integration needs significant work")
            
        if avg_context_score < 80:
            print(f"   🔧 Consider enhancing prompt templates to better utilize context")
            print(f"   🔧 Review context building methods for optimization")
            
        return {
            "total_steps": total_steps,
            "success_rate": (successful_steps/total_steps)*100,
            "avg_context_score": avg_context_score,
            "avg_execution_time": avg_execution_time,
            "context_utilization": ((conversation_usage + document_usage)/(total_steps*2))*100
        }

async def run_realistic_workflow():
    """Run the complete realistic workflow test"""
    print("🚀 STARTING COMPREHENSIVE REALISTIC WORKFLOW TEST")
    print("=" * 80)
    
    tester = RealisticWorkflowTester()
    
    # Step 1: Initial greeting and setup
    print("\n👋 STEP 1: Initial Setup")
    tester.add_conversation_entry("user", "Hello, I'm working on a patent for 6G carrier aggregation technology")
    tester.add_conversation_entry("assistant", "Hello! I can help you with patent work for 6G carrier aggregation technology. What would you like to do first?")
    
    await tester.test_workflow_step(
        "Initial Greeting",
        "Hello, I'm working on a patent for 6G carrier aggregation technology",
        {"conversation_history": True, "document_content": False}
    )
    
    # Step 2: Document content creation
    print("\n📄 STEP 2: Document Content Creation")
    document_text = """
    Patent Disclosure: 6G Carrier Aggregation System
    
    This invention relates to a novel approach for carrier aggregation in 6G wireless networks. 
    The system utilizes artificial intelligence to dynamically allocate and manage multiple 
    carrier frequencies for optimal network performance.
    
    Key Features:
    1. AI-powered carrier selection algorithm
    2. Dynamic frequency allocation based on network conditions
    3. Real-time optimization of carrier combinations
    4. Intelligent load balancing across multiple carriers
    5. Adaptive modulation and coding schemes
    """
    
    tester.update_document_content(document_text, [
        "6G carrier aggregation overview",
        "AI-powered carrier selection",
        "Dynamic frequency allocation",
        "Real-time optimization",
        "Load balancing and modulation"
    ])
    
    await tester.test_workflow_step(
        "Document Analysis",
        "Analyze this patent disclosure and identify key technical concepts",
        {"conversation_history": True, "document_content": True}
    )
    
    # Step 3: Prior art search with context
    print("\n🔍 STEP 3: Prior Art Search with Context")
    tester.add_conversation_entry("user", "I need to search for prior art related to AI in carrier aggregation")
    tester.add_conversation_entry("assistant", "I'll help you search for prior art related to AI in carrier aggregation. Let me search the patent databases.")
    
    await tester.test_workflow_step(
        "Prior Art Search",
        "Find prior art patents related to AI-powered carrier aggregation in wireless networks",
        {"conversation_history": True, "document_content": True}
    )
    
    # Step 4: Content drafting with context
    print("\n✍️ STEP 4: Content Drafting with Context")
    tester.add_conversation_entry("user", "Based on the prior art search, draft improved patent claims")
    tester.add_conversation_entry("assistant", "I'll draft improved patent claims based on the prior art analysis and your disclosure.")
    
    await tester.test_workflow_step(
        "Content Drafting",
        "Draft improved patent claims that address the gaps identified in prior art",
        {"conversation_history": True, "document_content": True}
    )
    
    # Step 5: Follow-up request using conversation context
    print("\n🔄 STEP 5: Follow-up Request Using Context")
    await tester.test_workflow_step(
        "Follow-up Context Usage",
        "Can you refine the first claim to be more specific about the AI algorithm?",
        {"conversation_history": True, "document_content": True}
    )
    
    # Step 6: Document-aware request
    print("\n📋 STEP 6: Document-Aware Request")
    await tester.test_workflow_step(
        "Document Context Usage",
        "How does this compare to existing 5G carrier aggregation approaches?",
        {"conversation_history": True, "document_content": True}
    )
    
    # Step 7: Complex multi-context request
    print("\n🧠 STEP 7: Complex Multi-Context Request")
    await tester.test_workflow_step(
        "Multi-Context Integration",
        "Based on our conversation and the document content, what are the most innovative aspects of this invention?",
        {"conversation_history": True, "document_content": True}
    )
    
    # Generate final report
    final_report = tester.generate_final_report()
    
    # Save detailed results
    with open("realistic_workflow_test_results.json", "w") as f:
        json.dump({
            "test_summary": final_report,
            "detailed_results": tester.test_results,
            "conversation_history": tester.conversation_history,
            "document_content": tester.document_content,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: realistic_workflow_test_results.json")
    
    return final_report

async def main():
    """Main test execution"""
    try:
        print("🔍 COMPREHENSIVE REALISTIC WORKFLOW TEST")
        print("=" * 80)
        print("This test simulates a real user workflow to evaluate context integration:")
        print("1. Initial conversation setup")
        print("2. Document content creation and analysis")
        print("3. Prior art search with context")
        print("4. Content drafting using conversation and document context")
        print("5. Follow-up requests that should leverage context")
        print("6. Complex multi-context integration")
        print("=" * 80)
        
        # Run the workflow test
        results = await run_realistic_workflow()
        
        # Final evaluation
        print(f"\n🏆 FINAL EVALUATION:")
        if results["context_utilization"] >= 80:
            print(f"   🎉 OUTSTANDING: Context integration is working excellently!")
        elif results["context_utilization"] >= 60:
            print(f"   ✅ GOOD: Context integration is working well")
        elif results["context_utilization"] >= 40:
            print(f"   ⚠️  FAIR: Context integration needs improvement")
        else:
            print(f"   ❌ POOR: Context integration needs significant work")
            
        print(f"\n📊 Key Metrics:")
        print(f"   Context Utilization: {results['context_utilization']:.1f}%")
        print(f"   Success Rate: {results['success_rate']:.1f}%")
        print(f"   Average Context Score: {results['avg_context_score']:.1f}/100")
        
        return results
        
    except Exception as e:
        print(f"\n💥 Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    asyncio.run(main())
