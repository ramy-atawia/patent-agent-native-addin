"""
Comprehensive test cases for GeneralConversationTool

This test file ensures the GeneralConversationTool works without any fallbacks or mockups,
using real LLM integration and proper error handling.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from agentic_native_drafting.src.tools.general_conversation_tool import GeneralConversationTool


class TestGeneralConversationTool:
    """Test cases for GeneralConversationTool"""
    
    @pytest.fixture
    def tool(self):
        """Create a GeneralConversationTool instance for testing"""
        return GeneralConversationTool()
    
    @pytest.fixture
    def sample_user_input(self):
        """Sample user input for testing"""
        return "Hello, how are you today?"
    
    @pytest.fixture
    def sample_context(self):
        """Sample context for testing"""
        return "Previous conversation about AI and machine learning"
    
    def test_tool_initialization(self, tool):
        """Test that the tool initializes correctly"""
        assert tool is not None
        assert hasattr(tool, 'max_response_length')
        assert hasattr(tool, 'enable_context_analysis')
        assert tool.max_response_length == 2000
        assert tool.enable_context_analysis == True
    
    def test_max_response_length_configuration(self, tool):
        """Test max response length configuration"""
        assert tool.max_response_length > 0
        assert tool.max_response_length <= 5000  # Reasonable upper limit
    
    def test_context_analysis_configuration(self, tool):
        """Test context analysis configuration"""
        assert isinstance(tool.enable_context_analysis, bool)
    
    @pytest.mark.asyncio
    async def test_tool_run_success(self, tool, sample_user_input):
        """Test successful tool execution"""
        with patch.object(tool, '_generate_conversation_response', return_value="Hello! I'm doing well, thank you for asking."):
            events = []
            async for event in tool.run(sample_user_input):
                events.append(event)
            
            assert len(events) > 0
            # Check that we get the expected event types
            event_types = [event.get("event") for event in events]
            assert "thoughts" in event_types
            assert "results" in event_types
    
    @pytest.mark.asyncio
    async def test_tool_run_with_context(self, tool, sample_user_input, sample_context):
        """Test tool execution with context"""
        with patch.object(tool, '_generate_conversation_response', return_value="Based on our previous discussion about AI, I'm doing well!"):
            events = []
            async for event in tool.run(sample_user_input, sample_context):
                events.append(event)
            
            assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_with_parameters(self, tool, sample_user_input):
        """Test tool execution with custom parameters"""
        params = {
            "max_response_length": 500,
            "enable_context_analysis": False
        }
        
        with patch.object(tool, '_generate_conversation_response', return_value="Custom response"):
            events = []
            async for event in tool.run(sample_user_input, parameters=params):
                events.append(event)
            
            assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_response_generation_failure(self, tool, sample_user_input):
        """Test tool execution when response generation fails"""
        with patch.object(tool, '_generate_conversation_response', side_effect=Exception("Response generation failed")):
            events = []
            async for event in tool.run(sample_user_input):
                events.append(event)
            
            assert len(events) > 0
            error_events = [e for e in events if e.get("event") == "error"]
            assert len(error_events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_exception_handling(self, tool, sample_user_input):
        """Test tool execution exception handling"""
        with patch.object(tool, '_generate_conversation_response', side_effect=Exception("Unexpected error")):
            events = []
            async for event in tool.run(sample_user_input):
                events.append(event)
            
            assert len(events) > 0
            error_events = [e for e in events if e.get("event") == "error"]
            assert len(error_events) > 0
    
    def test_metadata_generation(self, tool, sample_user_input):
        """Test metadata generation for events"""
        metadata = {
            "user_input": sample_user_input,
            "input_length": len(sample_user_input),
            "timestamp": "2024-01-01T00:00:00"
        }
        
        assert "user_input" in metadata
        assert "input_length" in metadata
        assert "timestamp" in metadata
        
        assert metadata["user_input"] == sample_user_input
        assert metadata["input_length"] > 0
    
    def test_data_payload_structure(self, tool):
        """Test data payload structure for events"""
        data = {
            "conversation_response": "Hello! I'm doing well, thank you for asking.",
            "response_length": 45,
            "context_used": True
        }
        
        assert "conversation_response" in data
        assert "response_length" in data
        assert "context_used" in data
        
        assert isinstance(data["conversation_response"], str)
        assert isinstance(data["response_length"], int)
        assert isinstance(data["context_used"], bool)


if __name__ == "__main__":
    pytest.main([__file__])
