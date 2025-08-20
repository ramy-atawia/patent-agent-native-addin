# Agentic Native Drafting Service Documentation

Welcome to the comprehensive documentation for the **Agentic Native Drafting Service** - an intelligent patent drafting system powered by Large Language Models (LLMs) with advanced session management and context awareness.

## 📚 Documentation Structure

### **Core Documentation**
- **[API Reference](api-reference.md)** - Complete API endpoints, request/response formats, and examples
- **[Architecture Overview](architecture.md)** - System design, components, and data flow
- **[Functionality Guide](functionality.md)** - Core features, capabilities, and use cases

### **Technical Documentation**
- **[Data Models](data-models.md)** - Pydantic models, schemas, and data structures
- **[Session Management](session-management.md)** - Session lifecycle, context persistence, and history
- **[LLM Integration](llm-integration.md)** - Azure OpenAI integration, prompts, and intent classification

### **Development & Testing**
- **[Development Guide](development.md)** - Setup, configuration, and development workflow
- **[Testing Guide](testing.md)** - Test suite, regression testing, and quality assurance
- **[Deployment Guide](deployment.md)** - Production deployment and environment configuration

## 🚀 Quick Start

### **Service Overview**
The Agentic Native Drafting Service is a FastAPI-based backend that provides:

- **Intelligent Patent Drafting**: AI-powered generation of USPTO-compliant patent claims
- **Smart Claim Review**: Automated analysis and feedback on existing patent claims
- **Session Management**: Persistent conversation context across multiple interactions
- **LLM-Based Intent Classification**: Dynamic understanding of user requests
- **Confidence-Based Decision Making**: Intelligent routing based on confidence scores

### **Key Features**
- ✅ **Multi-turn Conversations**: Maintain context across patent drafting sessions
- ✅ **Intent Recognition**: Automatically classify user requests (draft, review, guidance)
- ✅ **Quality Assessment**: LLM-powered evaluation of patent claim quality
- ✅ **Session Isolation**: Separate contexts for different patent projects
- ✅ **Real-time Streaming**: Server-Sent Events (SSE) for live response updates

### **Technology Stack**
- **Backend**: FastAPI (Python)
- **LLM Provider**: Azure OpenAI (GPT-4o-mini)
- **Data Models**: Pydantic
- **Session Storage**: In-memory with persistent history
- **API Communication**: HTTP/HTTPS with SSE streaming

## 🔗 Quick Links

- **API Base URL**: `http://127.0.0.1:8000`
- **Health Check**: `GET /`
- **Main Endpoint**: `POST /api/patent/run`
- **Streaming**: `GET /api/patent/stream?run_id={run_id}`
- **Session Management**: `GET /api/sessions`

## 📖 Getting Started

1. **Read the [Architecture Overview](architecture.md)** to understand the system design
2. **Check the [API Reference](api-reference.md)** for endpoint details
3. **Review [Functionality Guide](functionality.md)** for use cases and examples
4. **Follow [Development Guide](development.md)** for setup and development

## 🤝 Contributing

This documentation is maintained alongside the codebase. When making changes:

1. Update the relevant documentation files
2. Ensure examples match current API behavior
3. Update diagrams and flowcharts if architecture changes
4. Test documentation examples against the current implementation

## 📞 Support

For questions about the documentation or system:

- Check the [Development Guide](development.md) for common issues
- Review the [Testing Guide](testing.md) for validation steps
- Examine the [Architecture Overview](architecture.md) for system understanding

---

**Last Updated**: August 17, 2024  
**Version**: 1.0  
**Status**: Production Ready ✅
