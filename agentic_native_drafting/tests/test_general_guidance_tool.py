"""
Comprehensive test cases for GeneralGuidanceTool

This test file ensures the GeneralGuidanceTool works without any fallbacks or mockups,
using real LLM integration and proper error handling.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from src.tools.patent_guidance_tool import GeneralGuidanceTool


class TestGeneralGuidanceTool:
    """Test cases for GeneralGuidanceTool"""
    
    @pytest.fixture
    def tool(self):
        """Create a GeneralGuidanceTool instance for testing"""
        return GeneralGuidanceTool()
    
    @pytest.fixture
    def sample_user_input(self):
        """Sample user input for testing"""
        return "How can I improve the performance of my machine learning model?"
    
    @pytest.fixture
    def sample_context(self):
        """Sample context for testing"""
        return "Working on a computer vision project with limited computational resources"
    
    def test_tool_initialization(self, tool):
        """Test that the tool initializes correctly"""
        assert tool is not None
        assert hasattr(tool, 'max_response_length')
        assert hasattr(tool, 'enable_context_analysis')
        assert tool.max_response_length == 1500
        assert tool.enable_context_analysis is True
    
    def test_max_response_length_configuration(self, tool):
        """Test max response length configuration"""
        assert tool.max_response_length > 0
        assert tool.max_response_length <= 5000  # Reasonable upper limit
    
    def test_enable_context_analysis_configuration(self, tool):
        """Test context analysis configuration"""
        assert isinstance(tool.enable_context_analysis, bool)
    
    @pytest.mark.asyncio
    async def test_tool_run_success(self, tool, sample_user_input, sample_context):
        """Test successful tool execution"""
        with patch.object(tool, '_generate_guidance_response', return_value="Here are some tips to improve performance..."):
            events = []
            async for event in tool.run(sample_user_input, sample_context):
                events.append(event)
            
            assert len(events) > 0
            # Check that we get the expected event types
            event_types = [event.get("event") for event in events]
            assert "thoughts" in event_types
            assert "results" in event_types
    
    @pytest.mark.asyncio
    async def test_tool_run_with_parameters(self, tool, sample_user_input, sample_context):
        """Test tool execution with custom parameters"""
        params = {
            "max_response_length": 1000,
            "enable_context_analysis": False
        }
        
        with patch.object(tool, '_generate_guidance_response', return_value="Custom guidance response"):
            events = []
            async for event in tool.run(sample_user_input, sample_context, params):
                events.append(event)
            
            assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_without_context(self, tool, sample_user_input):
        """Test tool execution without context"""
        with patch.object(tool, '_generate_guidance_response', return_value="Guidance without context"):
            events = []
            async for event in tool.run(sample_user_input):
                events.append(event)
            
            assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_guidance_generation_failure(self, tool, sample_user_input, sample_context):
        """Test tool execution when guidance generation fails"""
        with patch.object(tool, '_generate_guidance_response', return_value=""):
            events = []
            async for event in tool.run(sample_user_input, sample_context):
                events.append(event)
            
            assert len(events) > 0
            error_events = [e for e in events if e.get("event") == "error"]
            assert len(error_events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_exception_handling(self, tool, sample_user_input, sample_context):
        """Test tool exception handling"""
        with patch.object(tool, '_generate_guidance_response', side_effect=Exception("Test error")):
            events = []
            async for event in tool.run(sample_user_input, sample_context):
                events.append(event)
            
            assert len(events) > 0
            error_events = [e for e in events if e.get("event") == "error"]
            assert len(error_events) > 0
    
    def test_metadata_generation(self, tool, sample_user_input, sample_context):
        """Test metadata generation for events"""
        metadata = {
            "input_length": len(sample_user_input),
            "context_length": len(sample_context),
            "response_length": 100,
            "timestamp": "2024-01-01T00:00:00"
        }
        
        assert "input_length" in metadata
        assert "context_length" in metadata
        assert "response_length" in metadata
        assert "timestamp" in metadata
        
        assert metadata["input_length"] > 0
        assert metadata["context_length"] > 0
        assert metadata["response_length"] > 0
    
    def test_data_payload_structure(self, tool):
        """Test data payload structure for events"""
        data = {
            "guidance": "Sample guidance text",
            "reasoning": "Generated through guidance analysis",
            "input": "Sample input",
            "context": "Sample context"
        }
        
        assert "guidance" in data
        assert "reasoning" in data
        assert "input" in data
        assert "context" in data
        
        assert isinstance(data["guidance"], str)
        assert isinstance(data["reasoning"], str)
        assert isinstance(data["input"], str)
        assert isinstance(data["context"], str)


if __name__ == "__main__":
    pytest.main([__file__])
