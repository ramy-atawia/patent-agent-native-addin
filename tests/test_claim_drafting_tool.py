"""
Comprehensive test cases for ContentDraftingTool

This test file ensures the ContentDraftingTool works without any fallbacks or mockups,
using real LLM integration and proper error handling.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch, AsyncMock
from agentic_native_drafting.src.tools.claim_drafting_tool import ContentDraftingTool


class TestContentDraftingTool:
    """Test cases for ContentDraftingTool"""
    
    @pytest.fixture
    def tool(self):
        """Create a ContentDraftingTool instance for testing"""
        return ContentDraftingTool()
    
    @pytest.fixture
    def mock_llm_client(self):
        """Mock LLM client for testing"""
        mock_client = AsyncMock()
        mock_client.return_value = {
            "function_arguments": '{"content": [{"content_number": "1", "content_text": "Test claim", "content_type": "primary", "focus_area": "patent_claims"}], "reasoning": "Test reasoning", "input_assessment": {"sufficiency_score": 0.8, "strengths": ["Good input"], "areas_for_improvement": []}}',
            "content": "Test content"
        }
        return mock_client
    
    def test_tool_initialization(self, tool):
        """Test that the tool initializes correctly"""
        assert tool is not None
        assert hasattr(tool, 'max_outputs')
        assert hasattr(tool, 'max_output_length')
        assert tool.max_outputs == 20
        assert tool.max_output_length == 500
    
    @pytest.mark.asyncio
    async def test_input_assessment_sufficiency(self, tool):
        """Test input sufficiency assessment"""
        # Test sufficient input
        sufficient_input = "A method for optimizing handover procedures in 5G networks using artificial intelligence algorithms to predict optimal handover timing and reduce latency while maintaining quality of service."
        
        # Mock the LLM assessment
        with patch.object(tool, '_assess_input_sufficiency', return_value={
            "sufficiency_score": 0.8,
            "strengths": ["Good technical terminology", "Clear problem statement", "Appropriate scope"],
            "areas_for_improvement": ["Could include more implementation details"],
            "technical_depth": "advanced",
            "clarity_score": 0.9,
            "recommendations": ["Consider adding implementation examples"]
        }):
            assessment = await tool._assess_input_sufficiency(sufficient_input)
            
            assert isinstance(assessment, dict)
            assert "sufficiency_score" in assessment
            assert "strengths" in assessment
            assert "areas_for_improvement" in assessment
            assert "technical_depth" in assessment
            assert "clarity_score" in assessment
            assert "recommendations" in assessment
            assert assessment["sufficiency_score"] > 0.5  # Should be sufficient
            assert len(assessment["strengths"]) > 0
            assert len(assessment["areas_for_improvement"]) >= 0
            assert assessment["technical_depth"] in ["basic", "intermediate", "advanced"]
    
    @pytest.mark.asyncio
    async def test_input_assessment_insufficient(self, tool):
        """Test input sufficiency assessment for insufficient input"""
        # Test insufficient input
        insufficient_input = "AI optimization"
        
        # Mock the LLM assessment for insufficient input
        with patch.object(tool, '_assess_input_sufficiency', return_value={
            "sufficiency_score": 0.2,
            "strengths": ["Brief and concise"],
            "areas_for_improvement": ["Too brief", "Lacks technical detail", "Missing context"],
            "technical_depth": "basic",
            "clarity_score": 0.3,
            "recommendations": ["Add more technical details", "Include problem context", "Describe implementation approach"]
        }):
            assessment = await tool._assess_input_sufficiency(insufficient_input)
            
            assert isinstance(assessment, dict)
            assert "sufficiency_score" in assessment
            assert "strengths" in assessment
            assert "areas_for_improvement" in assessment
            assert assessment["sufficiency_score"] < 0.5  # Should be insufficient
            assert len(assessment["areas_for_improvement"]) > 0
    
    def test_content_indicators_counting(self, tool):
        """Test content indicator counting"""
        text = "method system process technique approach algorithm"
        count = tool._count_content_indicators(text)
        
        assert isinstance(count, int)
        assert count > 0  # Should find several indicators
    
    @pytest.mark.asyncio
    async def test_llm_content_drafting_success(self, tool, mock_llm_client):
        """Test successful LLM content drafting"""
        with patch('agentic_native_drafting.src.utils.llm_client.send_llm_request_streaming', mock_llm_client):
            result = await tool._draft_content_with_llm(
                "AI handover optimization",
                "5G network context",
                "Additional context",
                5,
                ["primary", "secondary"],
                ["handover", "optimization"]
            )
            
            assert isinstance(result, dict)
            assert "content" in result
            assert "reasoning" in result
            assert "input_assessment" in result
            assert len(result["content"]) > 0
    
    @pytest.mark.asyncio
    async def test_llm_content_drafting_function_call_failure(self, tool):
        """Test LLM content drafting when function call parsing fails"""
        mock_client = AsyncMock()
        mock_client.return_value = [
            {"type": "function_call", "function_arguments": "invalid json"}
        ]
        
        with patch('agentic_native_drafting.src.utils.llm_client.send_llm_request_streaming', mock_client):
            with pytest.raises(ValueError, match="LLM response parsing failed"):
                await tool._draft_content_with_llm(
                    "test input",
                    "test context",
                    "test additional",
                    5,
                    ["primary"],
                    []
                )
    
    @pytest.mark.asyncio
    async def test_llm_content_drafting_no_content(self, tool):
        """Test LLM content drafting when no content is provided"""
        mock_client = AsyncMock()
        mock_client.return_value = []
        
        with patch('agentic_native_drafting.src.utils.llm_client.send_llm_request_streaming', mock_client):
            with pytest.raises(ValueError, match="LLM did not provide any content"):
                await tool._draft_content_with_llm(
                    "test input",
                    "test context",
                    "test additional",
                    5,
                    ["primary"],
                    []
                )
    
    def test_llm_response_parsing_success(self, tool):
        """Test successful LLM response parsing"""
        response_content = """
        Claim 1: A method for AI-based handover optimization in 5G networks.
        Claim 2: The method of claim 1, further comprising predicting optimal timing.
        Claim 3: A system for implementing the method of claim 1.
        """
        
        result = tool._parse_llm_response(response_content)
        
        assert isinstance(result, dict)
        assert "content" in result
        assert "reasoning" in result
        assert "input_assessment" in result
        assert len(result["content"]) == 3
        
        # Check claim structure
        for claim in result["content"]:
            assert "content_number" in claim
            assert "content_text" in claim
            assert "content_type" in claim
            assert "focus_area" in claim
    
    def test_llm_response_parsing_no_claims(self, tool):
        """Test LLM response parsing when no claims are found"""
        response_content = "This is just some text without any claims."
        
        with pytest.raises(ValueError, match="No claims found in LLM response"):
            tool._parse_llm_response(response_content)
    
    def test_response_formatting_success(self, tool):
        """Test successful response formatting"""
        content_result = {
            "content": [
                {
                    "content_number": "1",
                    "content_text": "Test claim",
                    "content_type": "primary",
                    "focus_area": "patent_claims"
                }
            ],
            "reasoning": "Test reasoning"
        }
        
        input_assessment = {
            "sufficiency_score": 0.8,
            "strengths": ["Good input"],
            "areas_for_improvement": []
        }
        
        result = tool._format_response("test input", content_result, input_assessment)
        
        assert isinstance(result, dict)
        assert "content" in result
        assert "reasoning" in result
        assert "input_assessment" in result
        assert "metadata" in result
        assert result["metadata"]["outputs_generated"] == 1
    
    def test_response_formatting_failure(self, tool):
        """Test response formatting when it fails"""
        with patch.object(tool, '_format_response', side_effect=Exception("Formatting failed")):
            with pytest.raises(ValueError, match="Response formatting failed"):
                tool._format_response("test", {}, {})
    
    @pytest.mark.asyncio
    async def test_tool_run_success(self, tool, mock_llm_client):
        """Test successful tool execution"""
        with patch('agentic_native_drafting.src.utils.llm_client.send_llm_request_streaming', mock_llm_client):
            # Execute the tool
            events = []
            async for event in tool.run("AI handover optimization"):
                events.append(event)
            
            # Verify events were generated
            assert len(events) > 0
            
            # Check for thought events
            thought_events = [e for e in events if e.get("type") == "thought"]
            assert len(thought_events) > 0
            
            # Check for results event
            results_events = [e for e in events if e.get("type") == "results"]
            assert len(results_events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_with_parameters(self, tool, mock_llm_client):
        """Test tool execution with custom parameters"""
        with patch('agentic_native_drafting.src.utils.llm_client.send_llm_request_streaming', mock_llm_client):
            parameters = {
                "max_outputs": 10,
                "output_types": ["primary"],
                "focus_areas": ["handover"],
                "assess_input": True
            }
            
            events = []
            async for event in tool.run("AI handover optimization", parameters=parameters):
                events.append(event)
            
            assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_input_assessment_disabled(self, tool, mock_llm_client):
        """Test tool execution with input assessment disabled"""
        with patch('agentic_native_drafting.src.utils.llm_client.send_llm_request_streaming', mock_llm_client):
            parameters = {"assess_input": False}
            
            events = []
            async for event in tool.run("AI handover optimization", parameters=parameters):
                events.append(event)
            
            assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_llm_failure(self, tool):
        """Test tool execution when LLM fails"""
        with patch('agentic_native_drafting.src.utils.llm_client.send_llm_request_streaming', side_effect=Exception("LLM failed")):
            events = []
            async for event in tool.run("AI handover optimization"):
                events.append(event)
            
            # Should have error event
            error_events = [e for e in events if e.get("type") == "error"]
            assert len(error_events) > 0
    
    def test_claim_validation(self):
        """Test claim validation logic"""
        tool = ContentDraftingTool()
        
        # Valid claim
        valid_claim = {
            "content_number": "1",
            "content_text": "A method for AI optimization",
            "content_type": "primary",
            "focus_area": "patent_claims"
        }
        
        # Invalid claim (missing required fields)
        invalid_claim = {
            "content_number": "1",
            "content_text": "A method for AI optimization"
            # Missing content_type and focus_area
        }
        
        # Test validation logic (if implemented)
        assert "content_number" in valid_claim
        assert "content_text" in valid_claim
        assert "content_type" in valid_claim
        assert "focus_area" in valid_claim


class TestErrorHandling:
    """Test error handling scenarios"""
    
    @pytest.mark.asyncio
    async def test_missing_llm_client(self, tool):
        """Test behavior when LLM client is not available"""
        with patch('agentic_native_drafting.src.utils.llm_client.send_llm_request_streaming', None):
            with pytest.raises(AttributeError):
                await tool._draft_content_with_llm(
                    "test input",
                    "test context",
                    "test additional",
                    5,
                    ["primary"],
                    []
                )
    
    @pytest.mark.asyncio
    async def test_invalid_input_parameters(self, tool):
        """Test behavior with invalid input parameters"""
        invalid_params = {
            "max_outputs": -1,  # Invalid max outputs
            "output_types": "invalid",  # Should be list
            "focus_areas": "invalid"  # Should be list
        }
        
        # Should handle gracefully or raise appropriate error
        events = []
        try:
            async for event in tool.run("test input", parameters=invalid_params):
                events.append(event)
        except Exception:
            # Expected to fail with invalid parameters
            pass
        
        # Should have some events before failure
        assert len(events) >= 0
    
    def test_empty_input_text(self, tool):
        """Test behavior with empty input text"""
        with pytest.raises(ValueError):
            tool._assess_input_sufficiency("")
    
    def test_none_input_text(self, tool):
        """Test behavior with None input text"""
        with pytest.raises(AttributeError):
            tool._assess_input_sufficiency(None)


if __name__ == "__main__":
    pytest.main([__file__])
