# 🚀 Patent Drafting System

A sophisticated, LLM-driven agentic system for patent drafting that combines intelligent planning, dynamic tool execution, and comprehensive testing infrastructure.

## 🎯 **What This System Does**

The Patent Drafting System is an intelligent AI agent that:

- **Analyzes User Intent**: Uses LLM-based intent detection to understand patent drafting requests
- **Plans Dynamically**: Generates custom workflows based on user input rather than hardcoded paths
- **Executes Tools**: Dynamically selects and executes appropriate tools (draft_claims, review_claims, etc.)
- **Maintains Context**: Remembers conversation history and user intent across multiple interactions
- **Reflects Automatically**: Performs quality validation and reflection before output
- **Streams Responses**: Provides real-time streaming of agent reasoning and tool execution

## 🏗️ **Architecture Overview**

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   CLI Chat      │    │   FastAPI        │    │   Azure OpenAI  │
│   Interface     │◄──►│   Server         │◄──►│   LLM Service   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Agentic        │
                       │   Orchestrator   │
                       │   (LLM Planner)  │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   Tool Suite     │
                       │   • draft_claims │
                       │   • review_claims│
                       │   • conversation │
                       │   • reflection   │
                       └──────────────────┘
```

## 🚀 **Quick Start**

### **1. Setup Environment**
```bash
# Clone the repository
git clone <repository-url>
cd agentic-native-drafting

# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### **2. Configure Azure OpenAI**
Create a `.env` file in the root directory:
```bash
AZURE_OPENAI_API_KEY=your_api_key
AZURE_OPENAI_ENDPOINT=your_endpoint
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment
```

### **3. Start the Server**
```bash
./run.sh
```

### **4. Use the CLI Chat**
```bash
python3 cli_chat.py
```

## 🧪 **Testing Infrastructure**

The system includes a comprehensive, professionally organized testing suite:

### **Run All Tests**
```bash
python3 run_tests.py
```

### **Run Specific Test Categories**
```bash
# From the tests directory
python3 scripts/run_category.py --category functional
python3 scripts/run_category.py --category performance
python3 scripts/run_category.py --category integration
```

### **Test Structure**
```
tests/
├── functional/          # Core functionality tests
├── performance/         # Performance and load tests
├── integration/         # System integration tests
├── scripts/            # Test execution scripts
├── config/             # Test configuration
├── data/               # Test results and archives
└── logs/               # Execution logs
```

## 🔧 **Key Features**

### **Intelligent Intent Detection**
- **LLM-Based**: No hardcoded keyword matching
- **Context-Aware**: Considers conversation history
- **Dynamic Planning**: Generates custom workflows on-the-fly

### **Tool Execution**
- **draft_claims**: Generate patent claims based on invention description
- **review_claims**: Review and improve existing claims
- **conversation_query**: Intelligent conversation analysis and summarization
- **reflection_validator**: Automatic quality validation and improvement

### **Conversation Memory**
- **Persistent Context**: Remembers user intent across messages
- **Tool Results**: Stores detailed outputs for future reference
- **Smart Retrieval**: LLM-powered conversation querying

### **Real-Time Streaming**
- **Server-Sent Events**: Real-time response streaming
- **Progress Visibility**: See agent reasoning and tool execution
- **Interactive Experience**: Responsive user interface

## 📁 **Project Structure**

```
agentic-native-drafting/
├── agentic_native_drafting/    # Core system code
│   ├── agent.py                # LLM agent and tools
│   ├── main.py                 # FastAPI server
│   └── models.py               # Data models
├── tests/                      # Comprehensive test suite
│   ├── functional/             # Functionality tests
│   ├── performance/            # Performance tests
│   ├── integration/            # Integration tests
│   ├── scripts/                # Test runners
│   └── config/                 # Test configuration
├── cli_chat.py                 # Command-line interface
├── run.sh                      # Server startup script
├── run_tests.py                # Test suite launcher
└── README.md                   # This file
```

## 🎮 **Usage Examples**

### **Basic Patent Drafting**
```
User: I have an invention for a smart home security system
Agent: I understand you want to draft patent claims for a smart home security system. 
      To proceed effectively, I'll need more technical details about your invention.
      Could you describe the key components, how they work together, and what makes 
      your system unique?

User: It uses AI to detect unusual patterns and automatically adjusts security settings
Agent: Excellent! I'll draft comprehensive patent claims for your AI-powered smart 
      home security system. Let me generate claims that capture the AI pattern 
      detection and automatic security adjustment features.
```

### **Conversation Query**
```
User: Show me all the claims we discussed
Agent: Based on our conversation, here are all the claims we've generated:

      Claim 1: A smart home security system comprising an AI module configured to 
      detect unusual patterns in security data and automatically adjust security 
      settings based on detected patterns...

      [Additional claims with full text...]
```

## 🔍 **Advanced Features**

### **Dynamic Workflow Generation**
The system doesn't use hardcoded workflows. Instead, the LLM agent:
1. **Analyzes** user input and conversation context
2. **Plans** the optimal sequence of tools to execute
3. **Executes** tools dynamically based on the plan
4. **Reflects** on results to ensure quality

### **Automatic Reflection**
Every tool execution involving claims automatically triggers:
1. **Quality Validation**: Ensures claims meet patent standards
2. **Improvement Attempts**: Tries to enhance failed validations
3. **Final Reflection**: Confirms quality before user output

### **Context Utilization**
The system maintains rich conversation context including:
- **User Messages**: All user inputs and clarifications
- **Assistant Responses**: Agent reasoning and tool outputs
- **Tool Results**: Detailed outputs from all executed tools
- **Derived Information**: Summaries and context updates

## 🚀 **Development & Extension**

### **Adding New Tools**
1. Define the tool function in `agent.py`
2. Add tool description to the LLM prompt
3. Update the orchestrator to handle the new tool
4. Add tests for the new functionality

### **Customizing Behavior**
- **Agent Conservatism**: Adjust in `analyze_intent_with_llm` prompt
- **Tool Selection**: Modify tool descriptions and examples
- **Context Handling**: Customize conversation memory behavior

## 📊 **Performance & Reliability**

### **Test Coverage**
- **26 Functional Tests**: Core functionality validation
- **Performance Tests**: Streaming and multi-scenario testing
- **Integration Tests**: End-to-end conversation simulation
- **Continuous Validation**: Automated quality assurance

### **Error Handling**
- **Graceful Degradation**: Fallback responses for failures
- **Retry Logic**: Automatic retry for transient issues
- **Detailed Logging**: Comprehensive error tracking
- **User Feedback**: Clear error messages and guidance

## 🤝 **Contributing**

1. **Fork** the repository
2. **Create** a feature branch
3. **Implement** your changes
4. **Add** tests for new functionality
5. **Run** the test suite
6. **Submit** a pull request

## 📚 **Documentation**

- **This README**: Project overview and quick start
- **Test Documentation**: Comprehensive testing guides
- **Code Comments**: Inline documentation and examples
- **API Documentation**: FastAPI auto-generated docs at `/docs`

## 🐛 **Troubleshooting**

### **Common Issues**

#### **Server Won't Start**
```bash
# Check if port 8001 is in use
lsof -i :8001

# Kill existing processes
pkill -f "uvicorn.*8001"

# Restart server
./run.sh
```

#### **Tests Fail**
```bash
# Check server status
curl http://127.0.0.1:8001/docs

# Verify environment
source .venv/bin/activate
pip list | grep httpx

# Run tests with verbose output
python3 tests/scripts/run_category.py --category functional --verbose
```

#### **LLM Errors**
- Verify Azure OpenAI credentials in `.env`
- Check API endpoint and deployment name
- Ensure sufficient API quota and rate limits

## 📄 **License**

[Add your license information here]

---

**Need Help?** Check the test documentation, run the test suite, or examine the code comments for detailed guidance.
