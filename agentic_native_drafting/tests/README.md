# Modular System Test Suite

This directory contains a comprehensive test suite for the modular agentic system, covering unit tests, integration tests, and end-to-end workflow testing.

## 🏗️ Test Structure

```
tests/
├── conftest.py                    # Pytest configuration and fixtures
├── tools/                         # Unit tests for individual tools
│   ├── test_claim_drafting_tool.py
│   ├── test_claim_review_tool.py
│   └── test_prior_art_search_tool.py
├── chains/                        # Unit tests for workflow chains
│   └── test_patent_drafting_chain.py
├── agent_core/                    # Unit tests for core components
│   └── test_orchestrator.py
├── integration/                   # Integration tests
│   └── test_workflow_integration.py
└── README.md                      # This file
```

## 🚀 Quick Start

### Prerequisites

```bash
# Install required testing packages
pip install pytest pytest-asyncio pytest-mock pytest-cov

# Optional: Install additional packages for enhanced testing
pip install pytest-xdist  # For parallel test execution
pip install pytest-html   # For HTML test reports
```

### Running Tests

#### Using the Test Runner Script (Recommended)

```bash
# Quick tests (unit tests only)
python run_tests.py

# Unit tests only
python run_tests.py --type unit

# Integration tests only
python run_tests.py --type integration

# All tests
python run_tests.py --type all

# With verbose output
python run_tests.py --verbose

# With coverage reporting
python run_tests.py --coverage

# Stop on first failure
python run_tests.py --stop
```

#### Using pytest directly

```bash
# Run all tests
python -m pytest

# Run specific test categories
python -m pytest -m unit          # Unit tests only
python -m pytest -m integration   # Integration tests only

# Run specific test files
python -m pytest tests/tools/test_claim_drafting_tool.py

# Run specific test classes
python -m pytest tests/tools/test_claim_drafting_tool.py::TestClaimDraftingTool

# Run specific test methods
python -m pytest tests/tools/test_claim_drafting_tool.py::TestClaimDraftingTool::test_tool_initialization

# With coverage
python -m pytest --cov=src --cov-report=html
```

## 🧪 Test Categories

### 1. Unit Tests (`@pytest.mark.unit`)

**Purpose**: Test individual components in isolation

**Coverage**:
- Tool initialization and configuration
- Input validation and parameter extraction
- Core business logic methods
- Error handling and edge cases
- Response formatting and data structures

**Location**: `tests/tools/`, `tests/chains/`, `tests/agent_core/`

**Example**:
```python
@pytest.mark.unit
def test_tool_initialization(self, tool):
    """Test tool initialization and default values."""
    assert tool.max_claims == 20
    assert tool.max_claim_length == 500
```

### 2. Integration Tests (`@pytest.mark.integration`)

**Purpose**: Test interactions between components

**Coverage**:
- Tool-to-tool data flow
- Chain workflow execution
- Orchestrator routing logic
- Error propagation through workflows
- Conversation memory persistence

**Location**: `tests/integration/`

**Example**:
```python
@pytest.mark.integration
async def test_tool_to_tool_data_flow(self, sample_disclosure):
    """Test data flow between tools in a chain."""
    # Test that data flows correctly between drafting and review tools
```

### 3. Mock Tests (`@pytest.mark.mock`)

**Purpose**: Test components with mocked external dependencies

**Coverage**:
- LLM API calls
- External API interactions
- Database operations
- File system operations

**Example**:
```python
@pytest.mark.mock
@patch('tools.claim_drafting_tool.send_llm_request_streaming')
async def test_draft_claims_with_llm_success(self, mock_llm, tool, sample_disclosure):
    """Test LLM-based claim drafting with successful response."""
```

## 🔧 Test Fixtures

The test suite provides comprehensive fixtures in `conftest.py`:

### Data Fixtures
- `sample_invention_disclosure`: Sample invention disclosure text
- `sample_patent_claims`: Sample patent claims for testing
- `sample_prior_art_context`: Sample prior art context
- `sample_document_context`: Sample document context
- `sample_conversation_history`: Sample conversation history

### Mock Fixtures
- `mock_llm_response`: Mock LLM API responses
- `mock_search_result`: Mock search results
- `mock_disclosure_assessment`: Mock disclosure assessments
- `mock_azure_config`: Mock Azure OpenAI configuration
- `mock_patents_view_config`: Mock PatentsView API configuration

### Utility Fixtures
- `mock_llm_stream`: Mock streaming LLM responses
- `event_loop`: Async test event loop

## 📊 Test Coverage

### Tools Coverage
- **ClaimDraftingTool**: Input validation, parameter extraction, disclosure assessment, claim generation, response formatting
- **ClaimReviewTool**: Claim analysis, quality scoring, patentability assessment, recommendations generation
- **PriorArtSearchTool**: Search execution, result processing, relevance scoring

### Chains Coverage
- **PatentDraftingChain**: Workflow execution, step coordination, iterative improvement, error handling

### Agent Core Coverage
- **AgentOrchestrator**: Intent classification, tool routing, chain selection, conversation memory, caching

## 🚨 Error Handling Tests

The test suite extensively tests error scenarios:

### Input Validation Errors
- Empty or invalid inputs
- Parameter out of range
- Missing required fields

### External Service Failures
- LLM API failures
- Network timeouts
- Invalid responses

### Workflow Errors
- Tool execution failures
- Chain workflow errors
- Data consistency issues

## 🔄 Async Testing

Many components use async/await patterns. The test suite handles this with:

- `@pytest.mark.asyncio` decorator for async test methods
- `event_loop` fixture for async test setup
- Proper mocking of async operations
- Testing of streaming responses

## 📈 Performance Testing

The test suite includes performance validation:

- Workflow execution timing
- Memory usage patterns
- Response time validation
- Resource consumption monitoring

## 🧹 Test Cleanup

Tests automatically clean up after themselves:

- Temporary data removal
- Mock restoration
- Memory cleanup
- Cache clearing

## 🔍 Debugging Tests

### Verbose Output
```bash
python run_tests.py --verbose
python -m pytest -v
```

### Stop on First Failure
```bash
python run_tests.py --stop
python -m pytest -x
```

### Detailed Traceback
```bash
python -m pytest --tb=long
```

### Test Discovery
```bash
python -m pytest --collect-only
```

## 📝 Adding New Tests

### 1. Create Test File
```python
# tests/tools/test_new_tool.py
import pytest
from tools.new_tool import NewTool

class TestNewTool:
    @pytest.fixture
    def tool(self):
        return NewTool()
    
    @pytest.mark.unit
    def test_initialization(self, tool):
        assert tool is not None
```

### 2. Add Test Markers
```python
@pytest.mark.unit          # Unit test
@pytest.mark.integration   # Integration test
@pytest.mark.mock          # Uses mocks
@pytest.mark.asyncio       # Async test
```

### 3. Use Appropriate Fixtures
```python
def test_with_sample_data(self, sample_invention_disclosure):
    # Use existing fixtures
    pass

@pytest.fixture
def custom_fixture(self):
    # Create custom fixtures when needed
    return "custom_data"
```

## 🎯 Best Practices

### Test Naming
- Use descriptive test names that explain the scenario
- Follow the pattern: `test_[scenario]_[expected_behavior]`

### Test Structure
- Arrange: Set up test data and mocks
- Act: Execute the method under test
- Assert: Verify the expected outcomes

### Mocking
- Mock external dependencies, not internal logic
- Use `@patch` decorator for clean mock management
- Verify mock calls when testing interactions

### Error Testing
- Test both success and failure scenarios
- Verify error messages and types
- Test edge cases and boundary conditions

## 📚 Additional Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [Pytest-Asyncio](https://pytest-asyncio.readthedocs.io/)
- [Python Mock Library](https://docs.python.org/3/library/unittest.mock.html)
- [Test-Driven Development](https://en.wikipedia.org/wiki/Test-driven_development)

## 🤝 Contributing

When adding new tests:

1. Follow the existing test patterns
2. Add appropriate markers
3. Use existing fixtures when possible
4. Ensure tests are isolated and repeatable
5. Add comprehensive error case coverage
6. Update this documentation if needed

## 📊 Test Reports

### HTML Reports
```bash
python run_tests.py --coverage
# Open htmlcov/index.html in your browser
```

### XML Reports
```bash
python -m pytest --cov=src --cov-report=xml
# Useful for CI/CD integration
```

### Coverage Reports
```bash
python -m pytest --cov=src --cov-report=term-missing
# Shows which lines are not covered by tests
```
