# Development Guide

Comprehensive guide for setting up, configuring, and developing the Agentic Native Drafting Service.

## 🚀 Quick Start

### **Prerequisites**
- Python 3.8+
- pip or conda package manager
- Azure OpenAI account and API key
- Git for version control

### **Installation Steps**
```bash
# 1. Clone the repository
git clone <repository-url>
cd agentic-native-drafting

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env with your Azure OpenAI credentials

# 5. Start the development server
uvicorn agentic_native_drafting.main:app --host 127.0.0.1 --port 8001 --reload
```

---

## 🔧 Development Environment Setup

### **1. Python Environment**

#### **Virtual Environment**
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On macOS/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate

# Verify activation
which python  # Should point to .venv/bin/python
pip list      # Should show minimal packages
```

#### **Python Version Management**
```bash
# Check Python version
python --version  # Should be 3.8+

# If using pyenv
pyenv install 3.11.0
pyenv local 3.11.0
pyenv virtualenv 3.11.0 agentic-drafting
pyenv activate agentic-drafting
```

### **2. Dependencies Installation**

#### **Core Dependencies**
```bash
# Install from requirements.txt
pip install -r requirements.txt

# Or install individually
pip install fastapi
pip install uvicorn[standard]
pip install httpx
pip install python-dotenv
pip install pydantic
```

#### **Development Dependencies**
```bash
# Install development tools
pip install pytest
pip install pytest-asyncio
pip install black
pip install flake8
pip install mypy

# Or install all dev dependencies
pip install -r requirements-dev.txt
```

### **3. Environment Configuration**

#### **Environment Variables**
```bash
# .env file
AZURE_OPENAI_ENDPOINT=https://{deployment}.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview

# Optional: Development settings
DEBUG=true
LOG_LEVEL=INFO
PORT=8001
HOST=127.0.0.1
```

#### **Azure OpenAI Setup**
1. **Create Azure OpenAI Resource**:
   - Go to Azure Portal
   - Create "Azure OpenAI" resource
   - Choose region and pricing tier

2. **Deploy Model**:
   - Go to Azure OpenAI Studio
   - Deploy GPT-4o-mini model
   - Note deployment name

3. **Get API Key**:
   - Go to "Keys and Endpoint" in Azure OpenAI resource
   - Copy key 1 or key 2
   - Copy endpoint URL

4. **Configure .env**:
   ```bash
   AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
   AZURE_OPENAI_API_KEY=your-api-key
   AZURE_OPENAI_DEPLOYMENT_NAME=your-deployment-name
   AZURE_OPENAI_API_VERSION=2024-12-01-preview
   ```

---

## 🏗️ Project Structure

### **Directory Layout**
```
agentic-native-drafting/
├── agentic_native_drafting/          # Main package
│   ├── __init__.py
│   ├── main.py                      # FastAPI application
│   ├── agent.py                     # Core agent logic
│   └── models.py                    # Pydantic data models
├── tests/                           # Test suite
│   ├── regression/                  # Regression tests
│   │   ├── test_confidence_threshold.py
│   │   ├── test_draft_claims_regression.py
│   │   ├── test_review_claims_regression.py
│   │   ├── test_session_regression.py
│   │   └── test_conversation_memory.py
│   └── conftest.py                  # Test configuration
├── docs/                            # Documentation
│   ├── README.md
│   ├── api-reference.md
│   ├── architecture.md
│   ├── functionality.md
│   ├── data-models.md
│   ├── session-management.md
│   ├── llm-integration.md
│   ├── development.md
│   ├── testing.md
│   └── deployment.md
├── cli_chat.py                      # CLI client
├── requirements.txt                  # Production dependencies
├── requirements-dev.txt              # Development dependencies
├── .env                             # Environment variables
├── .gitignore                       # Git ignore rules
└── README.md                        # Project overview
```

### **Key Files Explained**

#### **`agentic_native_drafting/main.py`**
- FastAPI application setup
- API endpoint definitions
- Session management service
- SSE streaming implementation

#### **`agentic_native_drafting/agent.py`**
- Core agent intelligence
- LLM integration
- Intent classification
- Function routing

#### **`agentic_native_drafting/models.py`**
- Pydantic data models
- API request/response schemas
- Data validation rules

---

## 🔄 Development Workflow

### **1. Code Development**

#### **Feature Development Process**
```bash
# 1. Create feature branch
git checkout -b feature/new-feature-name

# 2. Make changes
# Edit relevant files

# 3. Test changes
python -m pytest tests/ -v

# 4. Run linting
black agentic_native_drafting/
flake8 agentic_native_drafting/

# 5. Commit changes
git add .
git commit -m "feat: add new feature description"

# 6. Push and create PR
git push origin feature/new-feature-name
# Create Pull Request on GitHub
```

#### **Code Style Guidelines**
```python
# Use type hints
def draft_claims(disclosure: str, num_claims: int = 3) -> List[str]:
    """Draft patent claims based on disclosure."""
    pass

# Use docstrings
async def classify_user_intent(user_input: str, conversation_context: str = "") -> IntentClassification:
    """
    Use LLM to classify user intent with confidence scores.
    
    Args:
        user_input: The user's input text
        conversation_context: Session history context
        
    Returns:
        IntentClassification with intent, confidence, and reasoning
        
    Raises:
        RuntimeError: If LLM doesn't return function call
    """
    pass

# Use meaningful variable names
session_history = get_session_history(session_id)  # Good
sh = get_session_history(sid)                     # Bad

# Use constants for magic numbers
CONFIDENCE_THRESHOLD = 0.7
MAX_CLAIMS = 20
```

### **2. Testing Strategy**

#### **Test Types**
```python
# Unit tests - test individual functions
def test_draft_claims_basic():
    """Test basic claim drafting functionality."""
    claims = draft_claims("Test invention", 3)
    assert len(claims) == 3
    assert all(isinstance(claim, str) for claim in claims)

# Integration tests - test component interactions
async def test_agent_run_with_session():
    """Test agent run with session context."""
    # Test setup
    # Test execution
    # Test verification

# Regression tests - protect existing functionality
def test_confidence_threshold_regression():
    """Ensure confidence threshold system still works."""
    # Test high confidence scenarios
    # Test low confidence scenarios
    # Test edge cases
```

#### **Running Tests**
```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/regression/test_confidence_threshold.py

# Run with verbose output
python -m pytest -v

# Run with coverage
python -m pytest --cov=agentic_native_drafting

# Run specific test function
python -m pytest tests/regression/test_confidence_threshold.py::test_high_confidence_execution
```

### **3. Code Quality**

#### **Linting and Formatting**
```bash
# Format code with Black
black agentic_native_drafting/
black tests/

# Check code style with flake8
flake8 agentic_native_drafting/
flake8 tests/

# Type checking with mypy
mypy agentic_native_drafting/

# Run all quality checks
make quality-check
```

#### **Pre-commit Hooks**
```bash
# Install pre-commit
pip install pre-commit

# Install git hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

---

## 🧪 Testing Framework

### **1. Test Configuration**

#### **`tests/conftest.py`**
```python
import pytest
import asyncio
from httpx import AsyncClient
from agentic_native_drafting.main import app

@pytest.fixture
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
async def client():
    """Create a test client for the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def sample_invention():
    """Sample invention description for testing."""
    return "I have invented a quantum computing system that uses AI to optimize qubit entanglement patterns."

@pytest.fixture
def sample_claims():
    """Sample patent claims for testing."""
    return [
        "1. A quantum computing system comprising...",
        "2. The system of claim 1, wherein...",
        "3. The system of claim 1, wherein..."
    ]
```

### **2. Test Utilities**

#### **Test Helpers**
```python
# tests/utils/test_helpers.py
import json
from typing import Dict, Any

def create_test_session(client: AsyncClient, disclosure: str) -> Dict[str, str]:
    """Create a test session and return session/run IDs."""
    response = client.post("/api/patent/run", json={"disclosure": disclosure})
    assert response.status_code == 200
    return response.json()

def stream_test_response(client: AsyncClient, run_id: str) -> Dict[str, Any]:
    """Stream a test response and return final data."""
    response = client.get(f"/api/patent/stream?run_id={run_id}")
    assert response.status_code == 200
    
    # Parse SSE response
    events = {}
    current_event = None
    current_data = []
    
    for line in response.text.split('\n'):
        if line.startswith('event: '):
            if current_event and current_data:
                events[current_event] = json.loads(''.join(current_data))
            current_event = line[7:].strip()
            current_data = []
        elif line.startswith('data: '):
            current_data.append(line[6:].strip())
    
    if current_event and current_data:
        events[current_event] = json.loads(''.join(current_data))
    
    return events

def assert_high_confidence_response(response: Dict[str, Any]):
    """Assert that response indicates high confidence execution."""
    assert "final" in response
    final_data = response["final"]
    
    # Check metadata
    assert final_data.get("metadata", {}).get("confidence", 0) > 0.7
    assert "reasoning" in final_data
    
    # Check response content
    assert "response" in final_data
    assert len(final_data["response"]) > 0
```

### **3. Test Categories**

#### **Regression Tests**
```python
# tests/regression/test_confidence_threshold.py
class ConfidenceThresholdTester:
    """Test suite for confidence threshold system."""
    
    def __init__(self, base_url: str = "http://127.0.0.1:8001"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def test_high_confidence_execution(self):
        """Test that high confidence requests execute properly."""
        # Test implementation
        
    async def test_low_confidence_clarification(self):
        """Test that low confidence requests seek clarification."""
        # Test implementation
```

#### **Integration Tests**
```python
# tests/integration/test_end_to_end.py
async def test_complete_patent_workflow():
    """Test complete patent drafting workflow."""
    # 1. Start session
    # 2. Draft claims
    # 3. Review claims
    # 4. Improve claims
    # 5. Final review
```

---

## 🔍 Debugging & Troubleshooting

### **1. Common Issues**

#### **Azure OpenAI Connection Issues**
```bash
# Check environment variables
echo $AZURE_OPENAI_ENDPOINT
echo $AZURE_OPENAI_API_KEY
echo $AZURE_OPENAI_DEPLOYMENT_NAME

# Test connection manually
curl -X POST "https://your-endpoint.openai.azure.com/openai/deployments/your-deployment/chat/completions?api-version=2024-12-01-preview" \
  -H "Content-Type: application/json" \
  -H "api-key: your-api-key" \
  -d '{"messages":[{"role":"user","content":"Hello"}],"model":"gpt-4o-mini"}'
```

#### **Session Management Issues**
```bash
# Check session state
curl "http://127.0.0.1:8001/api/sessions"

# Debug specific session
curl "http://127.0.0.1:8001/api/debug/session/{session_id}"

# Check server logs
tail -f server.log
```

### **2. Debug Tools**

#### **Logging Configuration**
```python
# agentic_native_drafting/main.py
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('server.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use logger in code
logger.info("Starting new session: %s", session_id)
logger.error("Error processing request: %s", str(e))
```

#### **Debug Endpoints**
```python
# Add debug endpoints for development
@app.get("/api/debug/state")
async def debug_state():
    """Debug endpoint to see current service state."""
    return {
        "sessions": len(service._sessions),
        "runs": len(service._runs),
        "memory_usage": "TODO: Add memory monitoring"
    }

@app.get("/api/debug/health")
async def debug_health():
    """Debug endpoint to check system health."""
    try:
        # Test Azure OpenAI connection
        test_response = await test_azure_connection()
        return {"status": "healthy", "azure_openai": test_response}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

---

## 🚀 Performance Optimization

### **1. Profiling Tools**

#### **Performance Monitoring**
```python
import time
import functools

def timing_decorator(func):
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result
    return wrapper

# Use decorator
@timing_decorator
async def classify_user_intent(user_input: str, conversation_context: str = "") -> IntentClassification:
    # Function implementation
    pass
```

#### **Memory Profiling**
```python
import psutil
import os

def log_memory_usage():
    """Log current memory usage."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    print(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")

# Use in key functions
async def start_run(self, disclosure: str, session_id: str = None) -> Dict[str, str]:
    log_memory_usage()
    # Function implementation
    log_memory_usage()
```

### **2. Optimization Strategies**

#### **Async Optimization**
```python
# Use asyncio.gather for concurrent operations
async def process_multiple_requests(requests: List[str]):
    """Process multiple requests concurrently."""
    tasks = [process_single_request(req) for req in requests]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

# Use connection pooling
async def create_http_client():
    """Create HTTP client with connection pooling."""
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=10)
    return httpx.AsyncClient(limits=limits)
```

---

## 📚 Documentation Development

### **1. Code Documentation**

#### **Docstring Standards**
```python
def draft_claims(disclosure: str, num_claims: int = 3, session_history: str = "") -> List[str]:
    """
    Draft patent claims based on invention disclosure and session history.
    
    This function generates USPTO-compliant patent claims using LLM integration.
    It considers session context to maintain consistency with previous discussions.
    
    Args:
        disclosure: Description of the invention to draft claims for
        num_claims: Number of claims to generate (default: 3)
        session_history: Session conversation history for context (default: "")
        
    Returns:
        List of patent claim strings
        
    Raises:
        ValueError: If disclosure is empty or invalid
        RuntimeError: If LLM request fails
        
    Example:
        >>> claims = draft_claims("AI-powered quantum computing system", 3)
        >>> print(f"Generated {len(claims)} claims")
        Generated 3 claims
    """
    pass
```

#### **Type Hints**
```python
from typing import List, Dict, Any, Optional, Union
from pydantic import BaseModel

def process_claims(
    claims: List[str],
    options: Optional[Dict[str, Any]] = None,
    context: Union[str, Dict[str, str]] = ""
) -> Dict[str, Any]:
    """Process patent claims with various options."""
    pass
```

### **2. API Documentation**

#### **OpenAPI/Swagger**
```python
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Agentic Native Drafting Service",
    description="AI-powered patent drafting system with session management",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

def custom_openapi():
    """Customize OpenAPI schema."""
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title="Agentic Native Drafting Service",
        version="1.0.0",
        description="AI-powered patent drafting system",
        routes=app.routes,
    )
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
```

---

## 🔧 Development Tools

### **1. IDE Configuration**

#### **VS Code Settings**
```json
// .vscode/settings.json
{
    "python.defaultInterpreterPath": "./.venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"],
    "python.testing.unittestEnabled": false,
    "python.testing.nosetestsEnabled": false,
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
        "source.organizeImports": true
    }
}
```

#### **VS Code Extensions**
- Python (Microsoft)
- Pylance
- Black Formatter
- Flake8
- Pytest
- GitLens

### **2. Development Scripts**

#### **Makefile**
```makefile
# Makefile
.PHONY: install test lint format clean run dev

install:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	python -m pytest tests/ -v

lint:
	flake8 agentic_native_drafting/ tests/
	mypy agentic_native_drafting/

format:
	black agentic_native_drafting/ tests/

quality-check: lint format test

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache/
	rm -rf .coverage

run:
	uvicorn agentic_native_drafting.main:app --host 127.0.0.1 --port 8001

dev:
	uvicorn agentic_native_drafting.main:app --host 127.0.0.1 --port 8001 --reload
```

#### **Development Scripts**
```bash
#!/bin/bash
# scripts/dev-setup.sh

echo "Setting up development environment..."

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run initial tests
python -m pytest tests/ -v

echo "Development environment setup complete!"
```

---

## 🔮 Future Development

### **1. Planned Features**

#### **Database Integration**
```python
# Future: SQLAlchemy integration
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Session(Base):
    __tablename__ = "sessions"
    
    session_id = Column(String, primary_key=True)
    started_at = Column(DateTime)
    topic = Column(Text)
    history = Column(Text)
```

#### **Microservices Architecture**
```python
# Future: Service decomposition
class PatentDraftingService:
    """Microservice for patent drafting."""
    pass

class SessionManagementService:
    """Microservice for session management."""
    pass

class LLMIntegrationService:
    """Microservice for LLM integration."""
    pass
```

### **2. Development Roadmap**

#### **Phase 1: Core Features** ✅
- Basic patent drafting
- Session management
- LLM integration
- Confidence threshold system

#### **Phase 2: Advanced Features** 🔄
- Database persistence
- User authentication
- Advanced analytics
- Performance optimization

#### **Phase 3: Enterprise Features** 📋
- Multi-tenant support
- API rate limiting
- Advanced security
- Monitoring and alerting

---

## 📋 Best Practices

### **1. Code Quality**

1. **Write Tests First**: Use TDD approach for new features
2. **Keep Functions Small**: Single responsibility principle
3. **Use Type Hints**: Improve code clarity and catch errors
4. **Document Everything**: Clear docstrings and comments
5. **Follow PEP 8**: Consistent Python style

### **2. Development Process**

1. **Feature Branches**: Work on features in separate branches
2. **Code Review**: Require PR reviews for all changes
3. **Continuous Testing**: Run tests on every commit
4. **Regular Refactoring**: Keep code clean and maintainable
5. **Performance Monitoring**: Track key metrics

### **3. Security**

1. **Environment Variables**: Never commit secrets
2. **Input Validation**: Validate all user inputs
3. **Rate Limiting**: Prevent API abuse
4. **Error Handling**: Don't expose sensitive information
5. **Regular Updates**: Keep dependencies updated

---

**Next**: Read the [Testing Guide](testing.md) to understand the testing strategy and test suite.
