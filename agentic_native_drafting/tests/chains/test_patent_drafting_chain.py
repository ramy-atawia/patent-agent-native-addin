"""
Unit tests for PatentDraftingChain.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from src.chains.patent_drafting_chain import PatentDraftingChain


class TestPatentDraftingChain:
    """Test suite for PatentDraftingChain."""
    
    @pytest.fixture
    def chain(self):
        """Create a PatentDraftingChain instance for testing."""
        return PatentDraftingChain()
    
    @pytest.fixture
    def sample_disclosure(self):
        """Sample invention disclosure for testing."""
        return """
        A method for dynamic spectrum sharing in 5G networks that enables 
        multiple operators to efficiently utilize available spectrum resources 
        through intelligent allocation algorithms and real-time monitoring.
        """
    
    @pytest.fixture
    def sample_context(self):
        """Sample document context for testing."""
        return "This invention relates to wireless communications and 5G networks."
    
    @pytest.fixture
    def sample_conversation_history(self):
        """Sample conversation history for testing."""
        return "User: I need help drafting patent claims."
    
    @pytest.mark.unit
    def test_chain_initialization(self, chain):
        """Test chain initialization and default values."""
        assert chain.max_iterations == 3
        assert chain.quality_threshold == 0.7
        assert chain.enable_iterative_improvement is True
        assert hasattr(chain, 'disclosure_tool')
        assert hasattr(chain, 'claim_drafting_tool')
        assert hasattr(chain, 'claim_review_tool')
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_workflow_status(self, chain):
        """Test workflow status retrieval."""
        status = await chain.get_workflow_status()
        
        assert status["chain_type"] == "PatentDraftingChain"
        assert status["version"] == "1.0.0"
        assert status["max_iterations"] == 3
        assert status["quality_threshold"] == 0.7
        assert "tools_available" in status
        assert "workflow_steps" in status
        assert len(status["workflow_steps"]) == 5
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.chains.patent_drafting_chain.DisclosureAssessmentTool')
    @patch('src.chains.patent_drafting_chain.ClaimDraftingTool')
    @patch('src.chains.patent_drafting_chain.ClaimReviewTool')
    async def test_execute_disclosure_assessment_success(self, mock_review, mock_drafting, mock_disclosure, chain, sample_disclosure):
        """Test successful disclosure assessment step."""
        # Mock disclosure tool
        mock_disclosure_instance = Mock()
        mock_disclosure_instance.run.return_value = {
            "status": "success",
            "assessment": {"sufficiency_score": 0.8}
        }
        mock_disclosure.return_value = mock_disclosure_instance
        
        # Mock other tools
        mock_drafting_instance = Mock()
        mock_drafting_instance.run.return_value = {"status": "success", "claims": []}
        mock_drafting.return_value = mock_drafting_instance
        
        mock_review_instance = Mock()
        mock_review_instance.run.return_value = {"status": "success"}
        mock_review.return_value = mock_review_instance
        
        # Execute chain
        events = []
        async for event in chain.execute(sample_disclosure, sample_context, sample_conversation_history):
            events.append(event)
        
        # Check that disclosure assessment was called
        mock_disclosure_instance.run.assert_called_once()
        
        # Check for disclosure assessment events
        disclosure_events = [e for e in events if "disclosure" in e.get("step", "")]
        assert len(disclosure_events) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.chains.patent_drafting_chain.DisclosureAssessmentTool')
    @patch('src.chains.patent_drafting_chain.ClaimDraftingTool')
    @patch('src.chains.patent_drafting_chain.ClaimReviewTool')
    async def test_execute_disclosure_assessment_failure(self, mock_review, mock_drafting, mock_disclosure, chain, sample_disclosure):
        """Test disclosure assessment failure handling."""
        # Mock disclosure tool failure
        mock_disclosure_instance = Mock()
        mock_disclosure_instance.run.side_effect = Exception("Disclosure tool failed")
        mock_disclosure.return_value = mock_disclosure_instance
        
        # Mock other tools
        mock_drafting_instance = Mock()
        mock_drafting_instance.run.return_value = {"status": "success", "claims": []}
        mock_drafting.return_value = mock_drafting_instance
        
        mock_review_instance = Mock()
        mock_review_instance.run.return_value = {"status": "success"}
        mock_review.return_value = mock_review_instance
        
        # Execute chain
        events = []
        async for event in chain.execute(sample_disclosure, sample_context, sample_conversation_history):
            events.append(event)
        
        # Check for error events
        error_events = [e for e in events if "error" in e.get("step", "")]
        assert len(error_events) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.chains.patent_drafting_chain.DisclosureAssessmentTool')
    @patch('src.chains.patent_drafting_chain.ClaimDraftingTool')
    @patch('src.chains.patent_drafting_chain.ClaimReviewTool')
    async def test_execute_claim_drafting_success(self, mock_review, mock_drafting, mock_disclosure, chain, sample_disclosure):
        """Test successful claim drafting step."""
        # Mock disclosure tool
        mock_disclosure_instance = Mock()
        mock_disclosure_instance.run.return_value = {
            "status": "success",
            "assessment": {"sufficiency_score": 0.8}
        }
        mock_disclosure.return_value = mock_disclosure_instance
        
        # Mock claim drafting tool
        mock_drafting_instance = Mock()
        mock_drafting_instance.run.return_value = {
            "status": "success", 
            "claims": [{"claim_text": "A method for spectrum sharing."}],
            "claims_generated": 1
        }
        mock_drafting.return_value = mock_drafting_instance
        
        # Mock review tool
        mock_review_instance = Mock()
        mock_review_instance.run.return_value = {"status": "success"}
        mock_review.return_value = mock_review_instance
        
        # Execute chain
        events = []
        async for event in chain.execute(sample_disclosure, sample_context, sample_conversation_history):
            events.append(event)
        
        # Check that claim drafting was called
        mock_drafting_instance.run.assert_called_once()
        
        # Check for claim drafting events
        drafting_events = [e for e in events if "drafting" in e.get("step", "")]
        assert len(drafting_events) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.chains.patent_drafting_chain.DisclosureAssessmentTool')
    @patch('src.chains.patent_drafting_chain.ClaimDraftingTool')
    @patch('src.chains.patent_drafting_chain.ClaimReviewTool')
    async def test_execute_claim_review_success(self, mock_review, mock_drafting, mock_disclosure, chain, sample_disclosure):
        """Test successful claim review step."""
        # Mock disclosure tool
        mock_disclosure_instance = Mock()
        mock_disclosure_instance.run.return_value = {
            "status": "success",
            "assessment": {"sufficiency_score": 0.8}
        }
        mock_disclosure.return_value = mock_disclosure_instance
        
        # Mock claim drafting tool
        mock_drafting_instance = Mock()
        mock_drafting_instance.run.return_value = {
            "status": "success", 
            "claims": [{"claim_text": "A method for spectrum sharing."}],
            "claims_generated": 1
        }
        mock_drafting.return_value = mock_drafting_instance
        
        # Mock review tool
        mock_review_instance = Mock()
        mock_review_instance.run.return_value = {
            "status": "success",
            "summary": {"overall_quality_score": 0.8}
        }
        mock_review.return_value = mock_review_instance
        
        # Execute chain
        events = []
        async for event in chain.execute(sample_disclosure, sample_context, sample_conversation_history):
            events.append(event)
        
        # Check that claim review was called
        mock_review_instance.run.assert_called_once()
        
        # Check for claim review events
        review_events = [e for e in events if "review" in e.get("step", "")]
        assert len(review_events) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.chains.patent_drafting_chain.DisclosureAssessmentTool')
    @patch('src.chains.patent_drafting_chain.ClaimDraftingTool')
    @patch('src.chains.patent_drafting_chain.ClaimReviewTool')
    async def test_execute_with_iterative_improvement(self, mock_review, mock_drafting, mock_disclosure, chain, sample_disclosure):
        """Test execution with iterative improvement enabled."""
        # Mock disclosure tool
        mock_disclosure_instance = Mock()
        mock_disclosure_instance.run.return_value = {
            "status": "success",
            "assessment": {"sufficiency_score": 0.8}
        }
        mock_disclosure.return_value = mock_disclosure_instance
        
        # Mock claim drafting tool
        mock_drafting_instance = Mock()
        mock_drafting_instance.run.return_value = {
            "status": "success", 
            "claims": [{"claim_text": "A method for spectrum sharing."}],
            "claims_generated": 1
        }
        mock_drafting.return_value = mock_drafting_instance
        
        # Mock review tool with low quality score to trigger improvement
        mock_review_instance = Mock()
        mock_review_instance.run.return_value = {
            "status": "success",
            "summary": {"overall_quality_score": 0.5},  # Below threshold
            "recommendations": {"claim_quality": ["Improve claim structure"]}
        }
        mock_review.return_value = mock_review_instance
        
        # Execute chain with iterative improvement
        events = []
        async for event in chain.execute(
            sample_disclosure, 
            sample_context, 
            sample_conversation_history,
            enable_iterative_improvement=True
        ):
            events.append(event)
        
        # Check for improvement events
        improvement_events = [e for e in events if "improvement" in e.get("step", "")]
        assert len(improvement_events) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.chains.patent_drafting_chain.DisclosureAssessmentTool')
    @patch('src.chains.patent_drafting_chain.ClaimDraftingTool')
    @patch('src.chains.patent_drafting_chain.ClaimReviewTool')
    async def test_execute_without_iterative_improvement(self, mock_review, mock_drafting, mock_disclosure, chain, sample_disclosure):
        """Test execution without iterative improvement."""
        # Mock all tools
        mock_disclosure_instance = Mock()
        mock_disclosure_instance.run.return_value = {
            "status": "success",
            "assessment": {"sufficiency_score": 0.8}
        }
        mock_disclosure.return_value = mock_disclosure_instance
        
        mock_drafting_instance = Mock()
        mock_drafting_instance.run.return_value = {
            "status": "success", 
            "claims": [{"claim_text": "A method for spectrum sharing."}],
            "claims_generated": 1
        }
        mock_drafting.return_value = mock_drafting_instance
        
        mock_review_instance = Mock()
        mock_review_instance.run.return_value = {
            "status": "success",
            "summary": {"overall_quality_score": 0.5}
        }
        mock_review.return_value = mock_review_instance
        
        # Execute chain without iterative improvement
        events = []
        async for event in chain.execute(
            sample_disclosure, 
            sample_context, 
            sample_conversation_history,
            enable_iterative_improvement=False
        ):
            events.append(event)
        
        # Should not have improvement events
        improvement_events = [e for e in events if "improvement" in e.get("step", "")]
        assert len(improvement_events) == 0
    
    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_yield_progress(self, chain):
        """Test progress event generation."""
        workflow_state = {"step": "test", "data": "test_data"}
        progress_event = await chain._yield_progress("test_step", "Test message", workflow_state)
        
        assert progress_event["type"] == "progress"
        assert progress_event["step"] == "test_step"
        assert progress_event["message"] == "Test message"
        assert progress_event["workflow_state"] == workflow_state
        assert "timestamp" in progress_event
    
    @pytest.mark.unit
    def test_create_improvement_prompt(self, chain):
        """Test improvement prompt creation."""
        claims = [{"claim_number": "1", "claim_text": "A method."}]
        recommendations = {
            "claim_quality": ["Improve structure"],
            "patentability": ["Add details"]
        }
        disclosure = "A method for wireless communication."
        
        prompt = chain._create_improvement_prompt(claims, recommendations, disclosure)
        
        assert "recommendations" in prompt
        assert "Original claims" in prompt
        assert "Invention disclosure context" in prompt
        assert "Please provide improved versions" in prompt
    
    @pytest.mark.unit
    def test_compile_final_result(self, chain, sample_disclosure):
        """Test final result compilation."""
        workflow_state = {
            "start_time": "2024-01-01T00:00:00",
            "end_time": "2024-01-01T01:00:00",
            "disclosure_assessment": {"status": "success"},
            "drafted_claims": {"claims_generated": 2},
            "claim_review": {
                "summary": {"overall_quality_score": 0.8},
                "recommendations": {"claim_quality": ["Good"]},
                "next_steps": ["File application"]
            },
            "iterations": [{"iteration": 1}]
        }
        
        final_result = chain._compile_final_result(workflow_state, sample_disclosure)
        
        assert "workflow_summary" in final_result
        assert "disclosure_assessment" in final_result
        assert "drafted_claims" in final_result
        assert "claim_review" in final_result
        assert "iterative_improvements" in final_result
        assert "recommendations" in final_result
    
    @pytest.mark.unit
    def test_compile_final_result_with_errors(self, chain, sample_disclosure):
        """Test final result compilation with errors."""
        workflow_state = {
            "start_time": "2024-01-01T00:00:00",
            "errors": ["Error 1", "Error 2"]
        }
        
        final_result = chain._compile_final_result(workflow_state, sample_disclosure)
        
        assert "workflow_summary" in final_result
        assert final_result["workflow_summary"]["errors"] == 2
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_perform_iterative_improvement(self, chain, sample_disclosure):
        """Test iterative improvement process."""
        workflow_state = {
            "drafted_claims": {
                "claims": [{"claim_text": "A method.", "claim_type": "independent"}]
            },
            "claim_review": {
                "recommendations": {
                    "claim_quality": ["Improve structure"],
                    "patentability": ["Add details"]
                }
            }
        }
        
        kwargs = {"max_claims": 5}
        
        iterations = await chain._perform_iterative_improvement(
            sample_disclosure, workflow_state, kwargs
        )
        
        # Should return iterations list
        assert isinstance(iterations, list)
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_perform_iterative_improvement_no_claims(self, chain, sample_disclosure):
        """Test iterative improvement with no claims."""
        workflow_state = {
            "drafted_claims": {"claims": []}
        }
        
        kwargs = {"max_claims": 5}
        
        iterations = await chain._perform_iterative_improvement(
            sample_disclosure, workflow_state, kwargs
        )
        
        # Should return empty iterations list
        assert iterations == []
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_perform_iterative_improvement_no_recommendations(self, chain, sample_disclosure):
        """Test iterative improvement with no recommendations."""
        workflow_state = {
            "drafted_claims": {
                "claims": [{"claim_text": "A method.", "claim_type": "independent"}]
            },
            "claim_review": {
                "recommendations": {}
            }
        }
        
        kwargs = {"max_claims": 5}
        
        iterations = await chain._perform_iterative_improvement(
            sample_disclosure, workflow_state, kwargs
        )
        
        # Should return empty iterations list when no recommendations
        assert iterations == []
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_improve_claims(self, chain):
        """Test claim improvement functionality."""
        current_claims = [{"claim_text": "A method.", "claim_type": "independent"}]
        improvement_prompt = "Improve the claims based on recommendations."
        kwargs = {"max_claims": 5}
        
        improved_claims = await chain._improve_claims(
            current_claims, improvement_prompt, kwargs
        )
        
        # For now, should return current claims (no improvement implemented)
        assert improved_claims == current_claims
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_improve_claims_exception(self, chain):
        """Test claim improvement with exception handling."""
        current_claims = [{"claim_text": "A method.", "claim_type": "independent"}]
        improvement_prompt = "Improve the claims based on recommendations."
        kwargs = {"max_claims": 5}
        
        # Mock an exception in the improvement process
        with patch.object(chain, '_improve_claims', side_effect=Exception("Improvement failed")):
            improved_claims = await chain._improve_claims(
                current_claims, improvement_prompt, kwargs
            )
            
            # Should return current claims on failure
            assert improved_claims == current_claims
