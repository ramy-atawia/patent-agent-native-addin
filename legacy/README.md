# Legacy System Files

This folder contains the original, monolithic implementation of the patent drafting system that has been replaced by the new modular, LangChain-compatible agentic framework.

## Files

### `main.py`
- **Purpose**: Original FastAPI application with monolithic structure
- **Status**: DEPRECATED - Replaced by `src/agent_core/api.py`
- **Features**: 
  - Direct tool integration
  - Simple request handling
  - Basic streaming responses

### `agent.py`
- **Purpose**: Original agent implementation with direct tool execution
- **Status**: DEPRECATED - Replaced by `src/agent_core/orchestrator.py`
- **Features**:
  - Intent classification
  - Tool routing
  - Basic conversation memory

## Migration Notes

- **New System**: Use `src/agent_core/` for all new development
- **API Endpoints**: New system maintains backward compatibility
- **Tools**: New system uses modular tool architecture
- **Orchestrator**: New system uses enhanced orchestrator with better memory management

## Rollback Instructions

If rollback is needed:
1. Stop the new system
2. Copy files back to `src/` directory
3. Restart the legacy system
4. Update frontend to point to legacy endpoints

## Preservation Benefits

- **Zero Risk**: No functionality lost during transition
- **Reference Material**: Study original implementation patterns
- **Easy Rollback**: Quick reversion if issues arise
- **Documentation**: Preserves system evolution history

