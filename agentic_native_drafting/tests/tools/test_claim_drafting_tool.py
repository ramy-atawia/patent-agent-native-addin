"""
Unit tests for ContentDraftingTool.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from src.tools.claim_drafting_tool import ContentDraftingTool


class TestContentDraftingTool:
    """Test suite for ContentDraftingTool."""
    
    @pytest.fixture
    def tool(self):
        """Create a ContentDraftingTool instance for testing."""
        return ContentDraftingTool()
    
    @pytest.fixture
    def sample_disclosure(self):
        """Sample invention disclosure for testing."""
        return "A method for dynamic spectrum sharing in 5G networks."
    
    @pytest.mark.unit
    def test_tool_initialization(self, tool):
        """Test tool initialization and default values."""
        assert tool.max_claims == 20
        assert tool.max_claim_length == 500
        assert isinstance(tool, ContentDraftingTool)
    
    @pytest.mark.unit
    def test_validate_inputs_valid(self, tool, sample_disclosure):
        """Test input validation with valid data."""
        # Should not raise any exceptions
        tool._validate_inputs(sample_disclosure)
    
    @pytest.mark.unit
    def test_validate_inputs_empty_disclosure(self, tool):
        """Test input validation with empty disclosure."""
        with pytest.raises(ValueError, match="Disclosure text cannot be empty"):
            tool._validate_inputs("")
    
    @pytest.mark.unit
    def test_validate_inputs_none_disclosure(self, tool):
        """Test input validation with None disclosure."""
        with pytest.raises(ValueError, match="Disclosure text cannot be empty"):
            tool._validate_inputs(None)
    
    @pytest.mark.unit
    def test_validate_inputs_whitespace_disclosure(self, tool):
        """Test input validation with whitespace-only disclosure."""
        with pytest.raises(ValueError, match="Disclosure text cannot be empty"):
            tool._validate_inputs("   \n\t   ")
    
    @pytest.mark.unit
    def test_extract_parameters_defaults(self, tool):
        """Test parameter extraction with default values."""
        kwargs = {}
        params = tool._extract_parameters(kwargs)
        
        assert params["max_claims"] == 20
        assert params["claim_types"] == ["independent", "dependent"]
        assert params["focus_areas"] == []
        assert params["prior_art_context"] == ""
        assert params["assess_disclosure"] is True
    
    @pytest.mark.unit
    def test_extract_parameters_custom(self, tool):
        """Test parameter extraction with custom values."""
        kwargs = {
            "max_claims": 10,
            "claim_types": ["independent"],
            "focus_areas": ["wireless", "5G"],
            "prior_art_context": "Some prior art",
            "assess_disclosure": False
        }
        params = tool._extract_parameters(kwargs)
        
        assert params["max_claims"] == 10
        assert params["claim_types"] == ["independent"]
        assert params["focus_areas"] == ["wireless", "5G"]
        assert params["prior_art_context"] == "Some prior art"
        assert params["assess_disclosure"] is False
    
    @pytest.mark.unit
    def test_extract_parameters_max_claims_limit(self, tool):
        """Test that max_claims is limited to tool maximum."""
        kwargs = {"max_claims": 50}
        params = tool._extract_parameters(kwargs)
        
        assert params["max_claims"] == 20  # Should be limited to tool maximum
    
    @pytest.mark.unit
    def test_assess_disclosure_sufficiency(self, tool, sample_disclosure):
        """Test disclosure sufficiency assessment."""
        assessment = tool._assess_disclosure_sufficiency(sample_disclosure)
        
        assert "word_count" in assessment
        assert "technical_terms_count" in assessment
        assert "sufficiency_score" in assessment
        assert "recommendations" in assessment
        assert isinstance(assessment["sufficiency_score"], float)
        assert 0.0 <= assessment["sufficiency_score"] <= 1.0
    
    @pytest.mark.unit
    def test_count_technical_terms(self, tool):
        """Test technical term counting."""
        text = "A method for wireless communication using 5G networks with dynamic allocation."
        count = tool._count_technical_terms(text)
        
        assert count > 0
        assert isinstance(count, int)
    
    @pytest.mark.unit
    def test_count_technical_terms_no_terms(self, tool):
        """Test technical term counting with no technical terms."""
        text = "This is a simple text without technical terminology."
        count = tool._count_technical_terms(text)
        
        assert count == 0
    
    @pytest.mark.unit
    def test_generate_fallback_claims(self, tool, sample_disclosure):
        """Test fallback claim generation."""
        claims = tool._generate_fallback_claims(sample_disclosure, 5, ["independent", "dependent"])
        
        assert isinstance(claims, dict)
        assert "claims" in claims
        assert "reasoning" in claims
        assert "claim_strategy" in claims
        assert "technical_areas_covered" in claims
        
        # Should generate at least one independent claim
        independent_claims = [c for c in claims["claims"] if c["claim_type"] == "independent"]
        assert len(independent_claims) > 0
    
    @pytest.mark.unit
    def test_generate_fallback_claims_only_independent(self, tool, sample_disclosure):
        """Test fallback claim generation with only independent claims."""
        claims = tool._generate_fallback_claims(sample_disclosure, 3, ["independent"])
        
        assert all(c["claim_type"] == "independent" for c in claims["claims"])
        assert len(claims["claims"]) == 1
    
    @pytest.mark.unit
    def test_validate_and_format_claims(self, tool):
        """Test claim validation and formatting."""
        raw_claims = [
            {
                "claim_text": "A method for wireless communication.",
                "claim_type": "independent"
            },
            {
                "claim_text": "The method of claim 1, further comprising optimization.",
                "claim_type": "dependent",
                "dependency": "1"
            }
        ]
        
        formatted_claims = tool._validate_and_format_claims(raw_claims)
        
        assert len(formatted_claims) == 2
        for claim in formatted_claims:
            assert "claim_number" in claim
            assert "claim_text" in claim
            assert "claim_type" in claim
            assert "word_count" in claim
            assert "character_count" in claim
    
    @pytest.mark.unit
    def test_validate_and_format_claims_invalid(self, tool):
        """Test claim validation with invalid claims."""
        raw_claims = [
            {
                "claim_text": "",  # Invalid: empty text
                "claim_type": "independent"
            },
            {
                "claim_type": "dependent"  # Invalid: missing text
            },
            {
                "claim_text": "Valid claim text.",
                "claim_type": "independent"
            }
        ]
        
        formatted_claims = tool._validate_and_format_claims(raw_claims)
        
        # Should only include valid claims
        assert len(formatted_claims) == 1
        assert formatted_claims[0]["claim_text"] == "Valid claim text."
    
    @pytest.mark.unit
    def test_validate_and_format_claims_length_limit(self, tool):
        """Test claim length validation."""
        # Create a claim that exceeds the length limit
        long_text = "A very long claim text. " * 30  # Will exceed 500 characters
        raw_claims = [
            {
                "claim_text": long_text,
                "claim_type": "independent"
            }
        ]
        
        formatted_claims = tool._validate_and_format_claims(raw_claims)
        
        assert len(formatted_claims) == 1
        assert len(formatted_claims[0]["claim_text"]) <= tool.max_claim_length
        assert formatted_claims[0]["claim_text"].endswith("...")
    
    @pytest.mark.unit
    def test_format_response_success(self, tool, sample_disclosure):
        """Test response formatting for successful execution."""
        claims = [
            {
                "claim_number": "1",
                "claim_text": "A method for wireless communication.",
                "claim_type": "independent",
                "word_count": 8,
                "character_count": 40
            }
        ]
        
        response = tool._format_response(
            sample_disclosure, claims, "Good reasoning", 
            {"sufficiency_score": 0.8}, "context", "history"
        )
        
        assert response["status"] == "success"
        assert response["disclosure_length"] == len(sample_disclosure)
        assert response["claims_generated"] == 1
        assert "metadata" in response
        assert "claims" in response
        assert "reasoning" in response
        assert "disclosure_assessment" in response
        assert "claim_statistics" in response
    
    @pytest.mark.unit
    def test_format_response_no_claims(self, tool, sample_disclosure):
        """Test response formatting when no claims are generated."""
        response = tool._format_response(
            sample_disclosure, [], "No claims generated", 
            {"sufficiency_score": 0.5}, "context", "history"
        )
        
        assert response["status"] == "success"
        assert response["claims_generated"] == 0
        assert "claim_statistics" not in response
    
    @pytest.mark.unit
    def test_format_error_response(self, tool, sample_disclosure):
        """Test error response formatting."""
        error_message = "Something went wrong"
        response = tool._format_error_response(sample_disclosure, error_message)
        
        assert response["status"] == "error"
        assert response["error"]["message"] == error_message
        assert response["error"]["error_type"] == "claim_drafting_error"
        assert "timestamp" in response["error"]
        assert "metadata" in response
    
    @pytest.mark.unit
    def test_review_claims(self, tool):
        """Test claim review functionality."""
        claims = [
            {
                "claim_type": "independent",
                "word_count": 15
            },
            {
                "claim_type": "dependent",
                "word_count": 12
            }
        ]
        
        review = tool.review_claims_sync(claims)
        
        assert review["status"] == "success"
        assert review["analysis"]["total_claims"] == 2
        assert review["analysis"]["independent_claims"] == 1
        assert review["analysis"]["dependent_claims"] == 1
        assert "recommendations" in review["analysis"]
    
    @pytest.mark.unit
    def test_review_claims_empty(self, tool):
        """Test claim review with empty claims list."""
        review = tool.review_claims_sync([])
        
        assert review["status"] == "error"
        assert "No claims to review" in review["message"]
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.agent.send_llm_request_streaming')
    async def test_draft_claims_with_llm_success(self, mock_llm, tool, sample_disclosure, mock_llm_response):
        """Test LLM-based claim drafting with successful response."""
        # Mock the LLM response
        mock_llm.return_value = MockLLMStream([
            {"type": "completion", "function_arguments": '{"claims": [{"claim_number": "1", "claim_text": "A method.", "claim_type": "independent"}], "reasoning": "Good reasoning"}'}
        ])
        
        result = await tool._draft_claims_with_llm(
            sample_disclosure, "context", "history", 5, ["independent"], [], ""
        )
        
        assert result is not None
        assert "claims" in result
        assert "reasoning" in result
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    @patch('src.agent.send_llm_request_streaming')
    async def test_draft_claims_with_llm_failure(self, mock_llm, tool, sample_disclosure):
        """Test LLM-based claim drafting with LLM failure."""
        # Mock LLM failure
        mock_llm.side_effect = Exception("LLM call failed")
        
        result = await tool._draft_claims_with_llm(
            sample_disclosure, "context", "history", 5, ["independent"], [], ""
        )
        
        # Should fall back to fallback claims
        assert result is not None
        assert "claims" in result
        assert "reasoning" in result


class MockLLMStream:
    """Mock LLM streaming response for testing."""
    
    def __init__(self, responses):
        self.responses = responses
        self.index = 0
    
    def __aiter__(self):
        return self
    
    async def __anext__(self):
        if self.index >= len(self.responses):
            raise StopAsyncIteration
        
        response = self.responses[self.index]
        self.index += 1
        return response
