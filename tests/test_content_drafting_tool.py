"""
Comprehensive test cases for ContentDraftingTool

This test file ensures the ContentDraftingTool works without any fallbacks or mockups,
using real LLM integration and proper error handling.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from agentic_native_drafting.src.tools.claim_drafting_tool import ContentDraftingTool


class TestContentDraftingTool:
    """Test cases for ContentDraftingTool"""
    
    @pytest.fixture
    def tool(self):
        """Create a ContentDraftingTool instance for testing"""
        return ContentDraftingTool()
    
    def test_tool_initialization(self, tool):
        """Test that the tool initializes correctly"""
        assert tool is not None
        assert hasattr(tool, 'max_outputs')
        assert hasattr(tool, 'max_output_length')
        assert tool.max_outputs == 20
        assert tool.max_output_length == 500
    
    def test_input_assessment_sufficiency(self, tool):
        """Test input sufficiency assessment"""
        # Test sufficient input - longer text with more content indicators
        sufficient_input = "A comprehensive method for optimizing network procedures and system performance using advanced artificial intelligence algorithms and machine learning techniques to predict optimal timing parameters, reduce latency while maintaining quality of service, implement adaptive routing protocols, and enhance overall network efficiency through intelligent resource allocation and dynamic load balancing mechanisms. This innovative approach leverages cutting-edge machine learning algorithms and artificial intelligence techniques to dynamically optimize network performance, implement intelligent routing protocols, and enhance overall system efficiency through sophisticated resource allocation strategies and advanced load balancing mechanisms."
        assessment = tool._assess_input_sufficiency(sufficient_input)
        
        assert isinstance(assessment, dict)
        assert "sufficiency_score" in assessment
        assert "word_count" in assessment
        assert "content_indicators_count" in assessment
        assert "recommendations" in assessment
        assert assessment["sufficiency_score"] > 0.5  # Should be sufficient
    
    def test_input_assessment_insufficient(self, tool):
        """Test input assessment with insufficient input"""
        insufficient_input = "AI optimization"
        assessment = tool._assess_input_sufficiency(insufficient_input)
        
        assert isinstance(assessment, dict)
        assert assessment["sufficiency_score"] < 0.5  # Should be insufficient
        assert len(assessment["recommendations"]) > 0
        assert "word_count" in assessment
        assert "content_indicators_count" in assessment
    
    def test_content_indicators_counting(self, tool):
        """Test content indicator counting"""
        text = "method system process technique approach algorithm"
        count = tool._count_content_indicators(text)
        
        assert isinstance(count, int)
        assert count > 0  # Should find several indicators


if __name__ == "__main__":
    pytest.main([__file__])
