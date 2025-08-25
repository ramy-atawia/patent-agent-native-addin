"""
Integration tests for the complete modular system workflow.
"""

import pytest
import asyncio
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from src.agent_core.orchestrator import AgentOrchestrator
from src.chains.patent_drafting_chain import PatentDraftingChain
from src.tools.claim_drafting_tool import ClaimDraftingTool
from src.tools.claim_review_tool import ClaimReviewTool


class TestWorkflowIntegration:
    """Integration tests for complete workflow execution."""
    
    @pytest.fixture
    def orchestrator(self):
        """Create an AgentOrchestrator instance for testing."""
        return AgentOrchestrator()
    
    @pytest.fixture
    def patent_chain(self):
        """Create a PatentDraftingChain instance for testing."""
        return PatentDraftingChain()
    
    @pytest.fixture
    def sample_disclosure(self):
        """Sample invention disclosure for testing."""
        return """
        A method for dynamic spectrum sharing in 5G networks that enables 
        multiple operators to efficiently utilize available spectrum resources 
        through intelligent allocation algorithms and real-time monitoring.
        
        The system includes:
        - Dynamic spectrum allocation engine
        - Real-time network condition monitoring
        - Multi-operator coordination protocols
        - Quality of service optimization
        """
    
    @pytest.fixture
    def sample_context(self):
        """Sample document context for testing."""
        return "This invention relates to wireless communications and specifically to spectrum sharing in 5G networks."
    
    @pytest.fixture
    def sample_conversation_history(self):
        """Sample conversation history for testing."""
        return "User: I need help with patent drafting. Assistant: I can help you with that."
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_complete_patent_drafting_workflow(self, orchestrator, patent_chain, sample_disclosure, sample_context, sample_conversation_history):
        """Test the complete patent drafting workflow from start to finish."""
        # Mock the intent classification
        with patch.object(orchestrator, '_classify_intent') as mock_classify:
            mock_classify.return_value = {
                "intent": "claim_drafting",
                "confidence": 0.9
            }
            
            # Mock the tools to return realistic responses
            with patch.object(patent_chain, 'disclosure_tool') as mock_disclosure:
                mock_disclosure.run.return_value = {
                    "status": "success",
                    "assessment": {
                        "sufficiency_score": 0.85,
                        "word_count": 120,
                        "technical_terms_count": 12,
                        "recommendations": ["Add more implementation details"]
                    }
                }
                
                with patch.object(patent_chain, 'claim_drafting_tool') as mock_drafting:
                    mock_drafting.run.return_value = {
                        "status": "success",
                        "claims": [
                            {
                                "claim_number": "1",
                                "claim_text": "A method for dynamic spectrum sharing in wireless networks, comprising: monitoring network conditions in real-time; allocating spectrum resources based on demand; and coordinating between multiple operators.",
                                "claim_type": "independent",
                                "word_count": 25,
                                "character_count": 180
                            },
                            {
                                "claim_number": "2",
                                "claim_text": "The method of claim 1, further comprising optimizing quality of service based on user requirements.",
                                "claim_type": "dependent",
                                "dependency": "1",
                                "word_count": 15,
                                "character_count": 120
                            }
                        ],
                        "claims_generated": 2,
                        "reasoning": "Generated comprehensive claims covering the core invention and key dependent features."
                    }
                    
                    with patch.object(patent_chain, 'claim_review_tool') as mock_review:
                        mock_review.run.return_value = {
                            "status": "success",
                            "summary": {
                                "total_claims": 2,
                                "overall_quality_score": 0.82,
                                "independent_claims": 1,
                                "dependent_claims": 1
                            },
                            "detailed_analysis": {
                                "claim_analysis": {
                                    "claim_quality_scores": [
                                        {"claim_number": "1", "score": 0.85},
                                        {"claim_number": "2", "score": 0.78}
                                    ]
                                },
                                "patentability_assessment": {
                                    "novelty": "likely_novel",
                                    "non_obviousness": "requires_analysis",
                                    "utility": "clearly_useful",
                                    "enablement": "sufficient",
                                    "written_description": "sufficient",
                                    "overall_patentability": "likely_patentable"
                                }
                            },
                            "recommendations": {
                                "claim_quality": ["Consider adding more specific technical details"],
                                "patentability": ["Conduct prior art search for novelty analysis"]
                            },
                            "next_steps": ["File provisional application", "Conduct prior art search"]
                        }
                        
                        # Execute the complete workflow
                        events = []
                        async for event in patent_chain.execute(
                            sample_disclosure, 
                            sample_context, 
                            sample_conversation_history
                        ):
                            events.append(event)
                        
                        # Verify the complete workflow execution
                        assert len(events) > 0
                        
                        # Check for all major workflow steps
                        workflow_steps = [event.get("step", "") for event in events]
                        assert any("disclosure_assessment" in step for step in workflow_steps)
                        assert any("claim_drafting" in step for step in workflow_steps)
                        assert any("claim_review" in step for step in workflow_steps)
                        
                        # Check for final result
                        final_events = [e for e in events if e.get("type") == "workflow_completed"]
                        assert len(final_events) > 0
                        
                        final_result = final_events[0].get("result", {})
                        assert "workflow_summary" in final_result
                        assert "disclosure_assessment" in final_result
                        assert "drafted_claims" in final_result
                        assert "claim_review" in final_result
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_orchestrator_to_chain_workflow(self, orchestrator, sample_disclosure, sample_context):
        """Test the complete flow from orchestrator to chain execution."""
        # Mock intent classification
        with patch.object(orchestrator, '_classify_intent') as mock_classify:
            mock_classify.return_value = {
                "intent": "claim_drafting",
                "confidence": 0.9
            }
            
            # Mock chain workflow detection
            with patch.object(orchestrator, '_is_chain_workflow') as mock_detect:
                mock_detect.return_value = True
                
                # Mock chain execution
                with patch.object(orchestrator, '_execute_chain_workflow') as mock_execute:
                    mock_execute.return_value = [
                        {"type": "chain_started", "step": "chain_workflow_started"},
                        {"type": "chain_result", "result": {"status": "success"}}
                    ]
                    
                    # Execute through orchestrator
                    events = []
                    async for event in orchestrator.handle(
                        sample_disclosure, 
                        sample_context, 
                        use_chain=True
                    ):
                        events.append(event)
                    
                    # Verify orchestrator properly routed to chain
                    assert len(events) > 0
                    assert any("intent_classified" in event.get("step", "") for event in events)
                    assert any("chain_workflow" in event.get("step", "") for event in events)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_tool_to_tool_data_flow(self, sample_disclosure):
        """Test data flow between tools in a chain."""
        # Create tool instances
        drafting_tool = ClaimDraftingTool()
        review_tool = ClaimReviewTool()
        
        # Mock the drafting tool to return realistic claims
        with patch.object(drafting_tool, '_draft_claims_with_llm') as mock_llm:
            mock_llm.return_value = {
                "claims": [
                    {
                        "claim_text": "A method for wireless communication.",
                        "claim_type": "independent"
                    }
                ],
                "reasoning": "Generated claim based on disclosure"
            }
            
            # Execute drafting tool
            drafting_result = await drafting_tool.run(
                sample_disclosure,
                document_context="Test context",
                conversation_history="Test history"
            )
            
            assert drafting_result["status"] == "success"
            assert "claims" in drafting_result
            
            # Use the drafted claims in the review tool
            drafted_claims = drafting_result["claims"]
            review_result = await review_tool.run(
                drafted_claims,
                prior_art_context="",
                invention_disclosure=sample_disclosure
            )
            
            assert review_result["status"] == "success"
            assert "summary" in review_result
            assert "detailed_analysis" in review_result
            
            # Verify data consistency between tools
            assert review_result["detailed_analysis"]["claim_analysis"]["total_claims"] == len(drafted_claims)
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_error_propagation_through_workflow(self, patent_chain, sample_disclosure, sample_context, sample_conversation_history):
        """Test how errors propagate through the workflow."""
        # Mock disclosure tool to fail
        with patch.object(patent_chain, 'disclosure_tool') as mock_disclosure:
            mock_disclosure.run.side_effect = Exception("Disclosure assessment failed")
            
            # Mock other tools to succeed
            with patch.object(patent_chain, 'claim_drafting_tool') as mock_drafting:
                mock_drafting.run.return_value = {"status": "success", "claims": []}
                
                with patch.object(patent_chain, 'claim_review_tool') as mock_review:
                    mock_review.run.return_value = {"status": "success"}
                    
                    # Execute workflow
                    events = []
                    async for event in patent_chain.execute(
                        sample_disclosure, 
                        sample_context, 
                        sample_conversation_history
                    ):
                        events.append(event)
                    
                    # Verify error handling
                    assert len(events) > 0
                    
                    # Should have error events
                    error_events = [e for e in events if "error" in e.get("type", "")]
                    assert len(error_events) > 0
                    
                    # Should still have final result with error information
                    final_events = [e for e in events if e.get("type") == "workflow_completed"]
                    if final_events:
                        final_result = final_events[0].get("result", {})
                        assert "workflow_summary" in final_result
                        assert final_result["workflow_summary"].get("errors", 0) > 0
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_conversation_memory_persistence(self, orchestrator, sample_disclosure, sample_context):
        """Test that conversation memory persists across multiple requests."""
        session_id = "test_session_123"
        
        # First request
        with patch.object(orchestrator, '_classify_intent') as mock_classify:
            mock_classify.return_value = {"intent": "claim_drafting", "confidence": 0.8}
            
            with patch.object(orchestrator, '_execute_single_tool') as mock_execute:
                mock_execute.return_value = [{"type": "tool_result"}]
                
                events1 = []
                async for event in orchestrator.handle(sample_disclosure, sample_context, session_id=session_id):
                    events1.append(event)
                
                # Second request
                events2 = []
                async for event in orchestrator.handle("Follow up question", sample_context, session_id=session_id):
                    events2.append(event)
                
                # Verify conversation memory was maintained
                assert session_id in orchestrator.conversation_memory
                memory = orchestrator.conversation_memory[session_id]
                assert len(memory) == 2
                
                # First entry should be the original request
                assert memory[0]["user_input"] == sample_disclosure
                # Second entry should be the follow-up
                assert memory[1]["user_input"] == "Follow up question"
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_workflow_with_iterative_improvement(self, patent_chain, sample_disclosure, sample_context, sample_conversation_history):
        """Test workflow with iterative improvement enabled."""
        # Mock tools to return results that would trigger improvement
        with patch.object(patent_chain, 'disclosure_tool') as mock_disclosure:
            mock_disclosure.run.return_value = {
                "status": "success",
                "assessment": {"sufficiency_score": 0.8}
            }
            
            with patch.object(patent_chain, 'claim_drafting_tool') as mock_drafting:
                mock_drafting.run.return_value = {
                    "status": "success",
                    "claims": [{"claim_text": "A method.", "claim_type": "independent"}],
                    "claims_generated": 1
                }
                
                with patch.object(patent_chain, 'claim_review_tool') as mock_review:
                    # First review returns low quality score
                    mock_review.run.return_value = {
                        "status": "success",
                        "summary": {"overall_quality_score": 0.4},  # Below threshold
                        "recommendations": {
                            "claim_quality": ["Improve claim structure"],
                            "patentability": ["Add more technical details"]
                        }
                    }
                    
                    # Execute with iterative improvement
                    events = []
                    async for event in patent_chain.execute(
                        sample_disclosure, 
                        sample_context, 
                        sample_conversation_history,
                        enable_iterative_improvement=True
                    ):
                        events.append(event)
                    
                    # Verify improvement process
                    assert len(events) > 0
                    
                    # Should have improvement events
                    improvement_events = [e for e in events if "improvement" in e.get("step", "")]
                    assert len(improvement_events) > 0
                    
                    # Check final result includes iterations
                    final_events = [e for e in events if e.get("type") == "workflow_completed"]
                    if final_events:
                        final_result = final_events[0].get("result", {})
                        assert "iterative_improvements" in final_result
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_workflow_performance_metrics(self, patent_chain, sample_disclosure, sample_context, sample_conversation_history):
        """Test that workflow provides performance metrics."""
        # Mock all tools to succeed
        with patch.object(patent_chain, 'disclosure_tool') as mock_disclosure:
            mock_disclosure.run.return_value = {"status": "success", "assessment": {"sufficiency_score": 0.8}}
            
            with patch.object(patent_chain, 'claim_drafting_tool') as mock_drafting:
                mock_drafting.run.return_value = {"status": "success", "claims": [], "claims_generated": 0}
                
                with patch.object(patent_chain, 'claim_review_tool') as mock_review:
                    mock_review.run.return_value = {"status": "success"}
                    
                    # Execute workflow
                    start_time = asyncio.get_event_loop().time()
                    events = []
                    async for event in patent_chain.execute(
                        sample_disclosure, 
                        sample_context, 
                        sample_conversation_history
                    ):
                        events.append(event)
                    end_time = asyncio.get_event_loop().time()
                    
                    # Verify performance metrics
                    assert len(events) > 0
                    
                    # Check for timing information in final result
                    final_events = [e for e in events if e.get("type") == "workflow_completed"]
                    if final_events:
                        final_result = final_events[0].get("result", {})
                        workflow_summary = final_result.get("workflow_summary", {})
                        
                        assert "start_time" in workflow_summary
                        assert "end_time" in workflow_summary
                        assert "total_duration" in workflow_summary
                        
                        # Verify duration is reasonable
                        duration = workflow_summary["total_duration"]
                        assert duration > 0
                        assert duration < (end_time - start_time) + 1.0  # Allow some overhead
    
    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_workflow_with_different_disclosure_types(self, patent_chain, sample_context, sample_conversation_history):
        """Test workflow with different types of invention disclosures."""
        # Test with short disclosure
        short_disclosure = "A method for wireless communication."
        
        with patch.object(patent_chain, 'disclosure_tool') as mock_disclosure:
            mock_disclosure.run.return_value = {
                "status": "success",
                "assessment": {"sufficiency_score": 0.3}  # Low score for short disclosure
            }
            
            with patch.object(patent_chain, 'claim_drafting_tool') as mock_drafting:
                mock_drafting.run.return_value = {"status": "success", "claims": [], "claims_generated": 0}
                
                with patch.object(patent_chain, 'claim_review_tool') as mock_review:
                    mock_review.run.return_value = {"status": "success"}
                    
                    events = []
                    async for event in patent_chain.execute(
                        short_disclosure, 
                        sample_context, 
                        sample_conversation_history
                    ):
                        events.append(event)
                    
                    # Verify workflow handles short disclosure
                    assert len(events) > 0
                    
                    # Check that disclosure assessment reflects the short nature
                    disclosure_events = [e for e in events if "disclosure_assessment" in e.get("step", "")]
                    if disclosure_events:
                        assessment = disclosure_events[0].get("result", {})
                        assert assessment.get("assessment", {}).get("sufficiency_score", 1.0) < 0.5
        
        # Test with very long disclosure
        long_disclosure = "A comprehensive method for wireless communication. " * 50
        
        with patch.object(patent_chain, 'disclosure_tool') as mock_disclosure:
            mock_disclosure.run.return_value = {
                "status": "success",
                "assessment": {"sufficiency_score": 0.9}  # High score for comprehensive disclosure
            }
            
            with patch.object(patent_chain, 'claim_drafting_tool') as mock_drafting:
                mock_drafting.run.return_value = {"status": "success", "claims": [], "claims_generated": 0}
                
                with patch.object(patent_chain, 'claim_review_tool') as mock_review:
                    mock_review.run.return_value = {"status": "success"}
                    
                    events = []
                    async for event in patent_chain.execute(
                        long_disclosure, 
                        sample_context, 
                        sample_conversation_history
                    ):
                        events.append(event)
                    
                    # Verify workflow handles long disclosure
                    assert len(events) > 0
                    
                    # Check that disclosure assessment reflects the comprehensive nature
                    disclosure_events = [e for e in events if "disclosure_assessment" in e.get("step", "")]
                    if disclosure_events:
                        assessment = disclosure_events[0].get("result", {})
                        assert assessment.get("assessment", {}).get("sufficiency_score", 0.0) > 0.7
