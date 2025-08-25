"""
Unit tests for ClaimReviewTool.
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from src.tools.claim_review_tool import ClaimReviewTool


class TestClaimReviewTool:
    """Test suite for ClaimReviewTool."""
    
    @pytest.fixture
    def tool(self):
        """Create a ClaimReviewTool instance for testing."""
        return ClaimReviewTool()
    
    @pytest.fixture
    def sample_claims(self):
        """Sample patent claims for testing."""
        return [
            {
                "claim_number": "1",
                "claim_text": "A method for wireless communication comprising monitoring and allocation.",
                "claim_type": "independent"
            },
            {
                "claim_number": "2",
                "claim_text": "The method of claim 1, further comprising optimization.",
                "claim_type": "dependent",
                "dependency": "1"
            }
        ]
    
    @pytest.fixture
    def sample_invention_disclosure(self):
        """Sample invention disclosure for testing."""
        return "A comprehensive method for wireless communication with monitoring and optimization."
    
    @pytest.mark.unit
    def test_tool_initialization(self, tool):
        """Test tool initialization and default values."""
        assert tool.max_claims_per_review == 50
        assert "min_words" in tool.claim_quality_thresholds
        assert "max_words" in tool.claim_quality_thresholds
        assert "min_technical_terms" in tool.claim_quality_thresholds
        assert "max_dependent_depth" in tool.claim_quality_thresholds
    
    @pytest.mark.unit
    def test_validate_inputs_valid(self, tool, sample_claims):
        """Test input validation with valid data."""
        # Should not raise any exceptions
        tool._validate_inputs(sample_claims)
    
    @pytest.mark.unit
    def test_validate_inputs_empty_claims(self, tool):
        """Test input validation with empty claims list."""
        with pytest.raises(ValueError, match="Claims list cannot be empty"):
            tool._validate_inputs([])
    
    @pytest.mark.unit
    def test_validate_inputs_none_claims(self, tool):
        """Test input validation with None claims."""
        with pytest.raises(ValueError, match="Claims list cannot be empty"):
            tool._validate_inputs(None)
    
    @pytest.mark.unit
    def test_validate_inputs_exceeds_max(self, tool):
        """Test input validation when claims exceed maximum."""
        # Create claims list that exceeds the maximum
        many_claims = [{"claim_text": f"Claim {i}", "claim_type": "independent"} for i in range(60)]
        
        # Should truncate without raising an exception
        tool._validate_inputs(many_claims)
    
    @pytest.mark.unit
    def test_extract_technical_terms(self, tool):
        """Test technical term extraction."""
        claim_text = "A method for wireless communication using 5G networks with dynamic allocation."
        terms = tool._extract_technical_terms(claim_text)
        
        assert len(terms) > 0
        assert "method" in terms
        assert "wireless" in terms
        assert "communication" in terms
        assert "networks" in terms
        assert "allocation" in terms
    
    @pytest.mark.unit
    def test_extract_technical_terms_no_terms(self, tool):
        """Test technical term extraction with no technical terms."""
        claim_text = "This is a simple text without technical terminology."
        terms = tool._extract_technical_terms(claim_text)
        
        assert len(terms) == 0
    
    @pytest.mark.unit
    def test_identify_technical_areas(self, tool):
        """Test technical area identification."""
        claim_text = "A method for data processing using algorithms and computation."
        areas = tool._identify_technical_areas(claim_text)
        
        assert "Process/Method" in areas
        assert "Algorithm/Computation" in areas
    
    @pytest.mark.unit
    def test_identify_technical_areas_system(self, tool):
        """Test technical area identification for system claims."""
        claim_text = "A system for network communication comprising transmitters and receivers."
        areas = tool._identify_technical_areas(claim_text)
        
        assert "System/Apparatus" in areas
        assert "Network/Communication" in areas
    
    @pytest.mark.unit
    def test_calculate_claim_quality_score(self, tool):
        """Test claim quality score calculation."""
        score = tool._calculate_claim_quality_score(
            word_count=50,  # Good range
            char_count=300,
            technical_terms=4,  # Good number
            claim_type="independent",
            invention_disclosure="Some disclosure"
        )
        
        assert 0.0 <= score <= 1.0
        assert score > 0.7  # Should be a good score
    
    @pytest.mark.unit
    def test_calculate_claim_quality_score_poor(self, tool):
        """Test claim quality score calculation for poor claims."""
        score = tool._calculate_claim_quality_score(
            word_count=3,  # Too short
            char_count=20,
            technical_terms=0,  # No technical terms
            claim_type="dependent",
            invention_disclosure=""
        )
        
        assert 0.0 <= score <= 1.0
        assert score < 0.5  # Should be a poor score
    
    @pytest.mark.unit
    def test_identify_claim_issues(self, tool):
        """Test claim issue identification."""
        issues = tool._identify_claim_issues(
            claim_text="A method for wireless communication.",
            word_count=8,
            technical_terms=2,
            claim_type="independent"
        )
        
        # Should identify some issues
        assert isinstance(issues, list)
    
    @pytest.mark.unit
    def test_identify_claim_issues_too_short(self, tool):
        """Test claim issue identification for too short claims."""
        issues = tool._identify_claim_issues(
            claim_text="A method.",
            word_count=2,
            technical_terms=1,
            claim_type="independent"
        )
        
        assert any("too short" in issue.lower() for issue in issues)
    
    @pytest.mark.unit
    def test_identify_claim_issues_too_long(self, tool):
        """Test claim issue identification for too long claims."""
        long_text = "A very long claim text. " * 20  # Will exceed max_words
        issues = tool._identify_claim_issues(
            claim_text=long_text,
            word_count=200,
            technical_terms=5,
            claim_type="independent"
        )
        
        assert any("too long" in issue.lower() for issue in issues)
    
    @pytest.mark.unit
    def test_identify_claim_issues_no_period(self, tool):
        """Test claim issue identification for claims without period."""
        issues = tool._identify_claim_issues(
            claim_text="A method for wireless communication",
            word_count=8,
            technical_terms=2,
            claim_type="independent"
        )
        
        assert any("period" in issue.lower() for issue in issues)
    
    @pytest.mark.unit
    def test_analyze_claim_structure(self, tool):
        """Test claim structure analysis."""
        claim_text = "A method for wireless communication comprising monitoring and allocation."
        structure = tool._analyze_claim_structure(claim_text)
        
        assert "preamble" in structure
        assert "transition" in structure
        assert "body" in structure
        assert "clauses" in structure
    
    @pytest.mark.unit
    def test_analyze_claim_structure_with_wherein(self, tool):
        """Test claim structure analysis with wherein clauses."""
        claim_text = "A method comprising step A, wherein step A includes monitoring, wherein monitoring is continuous."
        structure = tool._analyze_claim_structure(claim_text)
        
        assert len(structure["clauses"]) == 2
        assert "wherein" in structure["clauses"][0]
        assert "wherein" in structure["clauses"][1]
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_assess_patentability_sufficient_disclosure(self, tool, sample_claims, sample_invention_disclosure):
        """Test patentability assessment with sufficient disclosure."""
        assessment = await tool._assess_patentability(sample_claims, "", sample_invention_disclosure)
        
        assert "novelty" in assessment
        assert "non_obviousness" in assessment
        assert "utility" in assessment
        assert "enablement" in assessment
        assert "written_description" in assessment
        assert "overall_patentability" in assessment
        assert "risk_factors" in assessment
        assert "prior_art_concerns" in assessment
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_assess_patentability_insufficient_disclosure(self, tool, sample_claims):
        """Test patentability assessment with insufficient disclosure."""
        short_disclosure = "A method."
        assessment = await tool._assess_patentability(sample_claims, "", short_disclosure)
        
        assert assessment["enablement"] == "insufficient"
        assert assessment["written_description"] == "insufficient"
        assert len(assessment["risk_factors"]) > 0
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_assess_patentability_with_prior_art(self, tool, sample_claims, sample_invention_disclosure):
        """Test patentability assessment with prior art context."""
        prior_art = "Similar technology exists in US Patent 9,123,456."
        assessment = await tool._assess_patentability(sample_claims, prior_art, sample_invention_disclosure)
        
        assert assessment["novelty"] == "requires_analysis"
        assert len(assessment["prior_art_concerns"]) > 0
    
    @pytest.mark.unit
    def test_generate_recommendations(self, tool):
        """Test recommendation generation."""
        claim_analysis = {
            "overall_quality_score": 0.6,
            "claim_quality_scores": [
                {"claim_number": "1", "score": 0.4}
            ]
        }
        
        patentability_assessment = {
            "enablement": "insufficient",
            "novelty": "requires_analysis"
        }
        
        focus_areas = ["wireless", "5G"]
        
        recommendations = tool._generate_recommendations(
            claim_analysis, patentability_assessment, focus_areas
        )
        
        assert "claim_quality" in recommendations
        assert "patentability" in recommendations
        assert "structure" in recommendations
        assert "technical_coverage" in recommendations
    
    @pytest.mark.unit
    def test_assess_risks(self, tool):
        """Test risk assessment."""
        claim_analysis = {
            "overall_quality_score": 0.3
        }
        
        patentability_assessment = {
            "overall_patentability": "unlikely_patentable"
        }
        
        risks = tool._assess_risks(claim_analysis, patentability_assessment)
        
        assert "high_risk" in risks
        assert "medium_risk" in risks
        assert "low_risk" in risks
        assert "risk_score" in risks
        assert 0.0 <= risks["risk_score"] <= 1.0
    
    @pytest.mark.unit
    def test_format_response(self, tool, sample_claims):
        """Test response formatting."""
        claim_analysis = {
            "total_claims": 2,
            "overall_quality_score": 0.8
        }
        
        patentability_assessment = {
            "overall_patentability": "likely_patentable"
        }
        
        recommendations = {
            "claim_quality": ["Good quality"],
            "patentability": ["Sufficient disclosure"]
        }
        
        risk_assessment = {
            "risk_score": 0.2
        }
        
        response = tool._format_response(
            sample_claims, claim_analysis, patentability_assessment,
            recommendations, risk_assessment, "comprehensive", "USPTO"
        )
        
        assert response["status"] == "success"
        assert response["review_type"] == "comprehensive"
        assert response["patent_office"] == "USPTO"
        assert "metadata" in response
        assert "summary" in response
        assert "detailed_analysis" in response
        assert "recommendations" in response
        assert "next_steps" in response
    
    @pytest.mark.unit
    def test_generate_next_steps(self, tool):
        """Test next steps generation."""
        recommendations = {
            "patentability": ["Conduct prior art search"],
            "claim_quality": ["Improve claim structure"]
        }
        
        risk_assessment = {
            "high_risk": ["Critical issue"]
        }
        
        next_steps = tool._generate_next_steps(recommendations, risk_assessment)
        
        assert len(next_steps) > 0
        assert any("high-risk" in step.lower() for step in next_steps)
        assert any("prior art" in step.lower() for step in next_steps)
    
    @pytest.mark.unit
    def test_format_error_response(self, tool, sample_claims):
        """Test error response formatting."""
        error_message = "Something went wrong"
        response = tool._format_error_response(sample_claims, error_message)
        
        assert response["status"] == "error"
        assert response["error"]["message"] == error_message
        assert response["error"]["error_type"] == "claim_review_error"
        assert "timestamp" in response["error"]
        assert "metadata" in response
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_run_success(self, tool, sample_claims, sample_invention_disclosure):
        """Test successful tool execution."""
        result = await tool.run(
            sample_claims, 
            prior_art_context="", 
            invention_disclosure=sample_invention_disclosure
        )
        
        assert result["status"] == "success"
        assert "summary" in result
        assert "detailed_analysis" in result
        assert "recommendations" in result
        assert "next_steps" in result
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_run_empty_claims(self, tool):
        """Test tool execution with empty claims."""
        result = await tool.run([], "", "")
        
        assert result["status"] == "error"
        assert "empty" in result["error"]["message"]
    
    @pytest.mark.asyncio
    @pytest.mark.mock
    async def test_run_exceeds_max_claims(self, tool):
        """Test tool execution with claims exceeding maximum."""
        many_claims = [{"claim_text": f"Claim {i}", "claim_type": "independent"} for i in range(60)]
        
        result = await tool.run(many_claims, "", "")
        
        assert result["status"] == "success"
        # Should truncate to max_claims_per_review
        assert len(result["detailed_analysis"]["claim_analysis"]["total_claims"]) <= tool.max_claims_per_review
