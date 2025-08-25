"""
Pytest configuration and fixtures for the modular system tests.
"""

import pytest
import asyncio
import sys
import os
from unittest.mock import Mock, AsyncMock, patch
from typing import Dict, Any, List

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Test data fixtures
@pytest.fixture
def sample_invention_disclosure():
    """Sample invention disclosure for testing"""
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
def sample_patent_claims():
    """Sample patent claims for testing"""
    return [
        {
            "claim_number": "1",
            "claim_text": "A method for dynamic spectrum sharing in wireless networks, comprising: monitoring network conditions in real-time; allocating spectrum resources based on demand; and coordinating between multiple operators.",
            "claim_type": "independent",
            "technical_focus": "Dynamic spectrum allocation"
        },
        {
            "claim_number": "2",
            "claim_text": "The method of claim 1, further comprising optimizing quality of service based on user requirements.",
            "claim_type": "dependent",
            "dependency": "1",
            "technical_focus": "QoS optimization"
        },
        {
            "claim_number": "3",
            "claim_text": "The method of claim 1, wherein the monitoring includes analyzing traffic patterns and congestion levels.",
            "claim_type": "dependent",
            "dependency": "1",
            "technical_focus": "Traffic analysis"
        }
    ]

@pytest.fixture
def sample_prior_art_context():
    """Sample prior art context for testing"""
    return """
    Known prior art includes:
    - US Patent 9,123,456: Basic spectrum sharing methods
    - US Patent 8,987,654: Network monitoring systems
    - US Patent 9,456,789: Multi-operator coordination
    
    However, none disclose the specific combination of real-time monitoring,
    dynamic allocation, and multi-operator coordination as claimed.
    """

@pytest.fixture
def sample_document_context():
    """Sample document context for testing"""
    return """
    This invention relates to wireless communications and specifically to
    spectrum sharing in 5G networks. The background includes current
    spectrum allocation challenges and the need for more efficient utilization.
    """

@pytest.fixture
def sample_conversation_history():
    """Sample conversation history for testing"""
    return """
    User: I need help drafting patent claims for my spectrum sharing invention.
    Assistant: I can help you draft claims. What are the key technical features?
    User: The main features are real-time monitoring and dynamic allocation.
    Assistant: Great! Let me help you draft comprehensive claims.
    """

@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing"""
    return {
        "claims": [
            {
                "claim_number": "1",
                "claim_text": "A method for dynamic spectrum sharing in wireless networks.",
                "claim_type": "independent",
                "technical_focus": "Spectrum sharing"
            }
        ],
        "reasoning": "Based on the disclosure, this independent claim covers the core invention.",
        "claim_strategy": "Broad independent claim with specific dependent claims",
        "technical_areas_covered": ["Wireless communications", "Spectrum management"]
    }

@pytest.fixture
def mock_search_result():
    """Mock search result for testing"""
    return {
        "query": "dynamic spectrum sharing 5G",
        "total_patents_found": 3,
        "average_relevance_score": 0.75,
        "patents": [
            {
                "patent_id": "US1234567",
                "title": "Dynamic Spectrum Sharing Method",
                "relevance_score": 0.85,
                "claims_count": 15
            },
            {
                "patent_id": "US2345678",
                "title": "5G Network Optimization",
                "relevance_score": 0.72,
                "claims_count": 12
            }
        ]
    }

@pytest.fixture
def mock_disclosure_assessment():
    """Mock disclosure assessment for testing"""
    return {
        "word_count": 150,
        "technical_terms_count": 8,
        "sufficiency_score": 0.8,
        "recommendations": [
            "Consider adding more implementation details",
            "Include specific algorithm descriptions"
        ]
    }

# Async test fixtures
@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

# Mock configurations
@pytest.fixture
def mock_azure_config():
    """Mock Azure OpenAI configuration"""
    return {
        "endpoint": "https://mock-azure.openai.azure.com",
        "api_key": "mock-api-key",
        "deployment_name": "mock-deployment",
        "api_version": "2024-02-15-preview"
    }

@pytest.fixture
def mock_patents_view_config():
    """Mock PatentsView API configuration"""
    return {
        "patents_view_api_key": "mock-patentsview-key",
        "timeout": 30.0,
        "min_request_interval": 1.5
    }

# Test utilities
class MockLLMStream:
    """Mock LLM streaming response"""
    
    def __init__(self, responses: List[Dict[str, Any]]):
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

@pytest.fixture
def mock_llm_stream():
    """Create a mock LLM stream"""
    def _create_stream(responses: List[Dict[str, Any]]):
        return MockLLMStream(responses)
    return _create_stream

# Environment setup
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Setup test environment variables"""
    # Mock environment variables for testing
    with patch.dict(os.environ, {
        'AZURE_OPENAI_ENDPOINT': 'https://mock-azure.openai.azure.com',
        'AZURE_OPENAI_API_KEY': 'mock-api-key',
        'AZURE_OPENAI_DEPLOYMENT_NAME': 'mock-deployment',
        'AZURE_OPENAI_API_VERSION': '2024-02-15-preview',
        'PATENTSVIEW_API_KEY': 'mock-patentsview-key'
    }):
        yield

# Test markers
def pytest_configure(config):
    """Configure pytest with custom markers"""
    config.addinivalue_line(
        "markers", "unit: mark test as a unit test"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as an integration test"
    )
    config.addinivalue_line(
        "markers", "e2e: mark test as an end-to-end test"
    )
    config.addinivalue_line(
        "markers", "slow: mark test as slow running"
    )
    config.addinivalue_line(
        "markers", "mock: mark test as using mocks"
    )
