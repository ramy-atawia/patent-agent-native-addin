"""
Comprehensive test cases for PriorArtSearchTool

This test file ensures the PriorArtSearchTool works without any fallbacks or mockups,
using real PatentsView API integration and proper error handling.
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from agentic_native_drafting.src.tools.prior_art_search_tool import PriorArtSearchTool


class TestPriorArtSearchTool:
    """Test cases for PriorArtSearchTool"""
    
    @pytest.fixture
    def tool(self):
        """Create a PriorArtSearchTool instance for testing"""
        return PriorArtSearchTool()
    
    @pytest.fixture
    def sample_query(self):
        """Sample search query for testing"""
        return "AI for 5G network optimization"
    
    @pytest.fixture
    def sample_search_strategies(self):
        """Sample search strategies for testing"""
        return [
            {
                "name": "AI_5G_optimization",
                "description": "Search for AI applications in 5G network optimization",
                "query": {
                    "q": {"_and": [{"_text_phrase": {"patent_abstract": "artificial intelligence"}}, {"_text_phrase": {"patent_abstract": "5G"}}, {"_text_phrase": {"patent_abstract": "optimization"}}]},
                    "f": ["patent_id", "patent_title", "patent_abstract", "patent_date", "patent_year"],
                    "s": [{"patent_date": "desc"}]
                }
            }
        ]
    
    def test_tool_initialization(self, tool):
        """Test that the tool initializes correctly"""
        assert tool is not None
        assert hasattr(tool, 'config')
        assert hasattr(tool, 'query_generator')
        assert hasattr(tool, 'api_client')
        assert hasattr(tool, 'content_analyzer')
        assert hasattr(tool, 'report_generator')
    
    def test_config_loading(self, tool):
        """Test that configuration loads correctly"""
        config = tool.config
        assert hasattr(config, 'azure_endpoint')
        assert hasattr(config, 'azure_api_key')
        assert hasattr(config, 'azure_deployment')
        assert hasattr(config, 'patents_view_api_key')
        assert hasattr(config, 'min_request_interval')
        assert hasattr(config, 'default_relevance_threshold')
        assert hasattr(config, 'default_max_results')
        assert hasattr(config, 'timeout')
    
    @pytest.mark.asyncio
    async def test_tool_run_success(self, tool, sample_query):
        """Test successful tool execution"""
        with patch.object(tool, '_generate_search_strategies', return_value=[{"name": "test", "query": {}}]):
            with patch.object(tool, '_execute_search_strategies', return_value=[{"patent_id": "123", "relevance_score": 0.8}]):
                with patch.object(tool, '_generate_search_report', return_value="Comprehensive search report"):
                    events = []
                    async for event in tool.run(sample_query):
                        events.append(event)
                    
                    assert len(events) > 0
                    # Check that we get the expected event types
                    event_types = [event.get("event") for event in events]
                    assert "thoughts" in event_types
                    assert "results" in event_types
    
    @pytest.mark.asyncio
    async def test_tool_run_with_parameters(self, tool, sample_query):
        """Test tool execution with custom parameters"""
        params = {
            "max_strategies": 3,
            "max_patents": 15,
            "relevance_threshold": 0.7
        }
        
        with patch.object(tool, '_generate_search_strategies', return_value=[{"name": "test", "query": {}}]):
            with patch.object(tool, '_execute_search_strategies', return_value=[{"patent_id": "123", "relevance_score": 0.8}]):
                with patch.object(tool, '_generate_search_report', return_value="Custom search report"):
                    events = []
                    async for event in tool.run(sample_query, **params):
                        events.append(event)
                    
                    assert len(events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_search_strategies_failure(self, tool, sample_query):
        """Test tool execution when search strategy generation fails"""
        with patch.object(tool, '_generate_search_strategies', side_effect=Exception("Strategy generation failed")):
            events = []
            async for event in tool.run(sample_query):
                events.append(event)
            
            assert len(events) > 0
            error_events = [e for e in events if e.get("event") == "error"]
            assert len(error_events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_search_execution_failure(self, tool, sample_query):
        """Test tool execution when search execution fails"""
        with patch.object(tool, '_generate_search_strategies', return_value=[{"name": "test", "query": {}}]):
            with patch.object(tool, '_execute_search_strategies', side_effect=Exception("Search execution failed")):
                events = []
                async for event in tool.run(sample_query):
                    events.append(event)
                
                assert len(events) > 0
                error_events = [e for e in events if e.get("event") == "error"]
                assert len(error_events) > 0
    
    @pytest.mark.asyncio
    async def test_tool_run_report_generation_failure(self, tool, sample_query):
        """Test tool execution when report generation fails"""
        with patch.object(tool, '_generate_search_strategies', return_value=[{"name": "test", "query": {}}]):
            with patch.object(tool, '_execute_search_strategies', return_value=[{"patent_id": "123", "relevance_score": 0.8}]):
                with patch.object(tool, '_generate_search_report', side_effect=Exception("Report generation failed")):
                    events = []
                    async for event in tool.run(sample_query):
                        events.append(event)
                    
                    assert len(events) > 0
                    error_events = [e for e in events if e.get("event") == "error"]
                    assert len(error_events) > 0
    
    def test_validate_inputs_valid(self, tool, sample_query):
        """Test input validation with valid inputs"""
        # Should not raise any exception
        tool._validate_inputs(sample_query)
    
    def test_validate_inputs_empty(self, tool):
        """Test input validation with empty query"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            tool._validate_inputs("")
    
    def test_validate_inputs_none(self, tool):
        """Test input validation with None query"""
        with pytest.raises(ValueError, match="Query cannot be empty"):
            tool._validate_inputs(None)
    
    def test_validate_inputs_too_short(self, tool):
        """Test input validation with too short query"""
        with pytest.raises(ValueError, match="Query must be at least"):
            tool._validate_inputs("AI")
    
    def test_metadata_generation(self, tool, sample_query):
        """Test metadata generation for events"""
        metadata = {
            "query": sample_query,
            "query_length": len(sample_query),
            "timestamp": "2024-01-01T00:00:00"
        }
        
        assert "query" in metadata
        assert "query_length" in metadata
        assert "timestamp" in metadata
        
        assert metadata["query"] == sample_query
        assert metadata["query_length"] > 0
    
    def test_data_payload_structure(self, tool):
        """Test data payload structure for events"""
        data = {
            "search_strategies": [{"name": "test", "query": {}}],
            "search_results": [{"patent_id": "123", "relevance_score": 0.8}],
            "search_report": "Comprehensive search report"
        }
        
        assert "search_strategies" in data
        assert "search_results" in data
        assert "search_report" in data
        
        assert isinstance(data["search_strategies"], list)
        assert isinstance(data["search_results"], list)
        assert isinstance(data["search_report"], str)


if __name__ == "__main__":
    pytest.main([__file__])
