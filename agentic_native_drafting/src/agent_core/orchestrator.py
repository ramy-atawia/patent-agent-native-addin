from typing import AsyncGenerator, Dict, Any, List, Optional
import logging
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import only the tools that are actually used in routing
from src.tools.claim_drafting_tool import ClaimDraftingTool
from src.tools.claim_review_tool import ClaimReviewTool
from src.tools.patent_guidance_tool import PatentGuidanceTool
from src.tools.prior_art_search_tool import PriorArtSearchTool
from src.tools.general_conversation_tool import GeneralConversationTool

# Import self-contained components
from src.utils.enums import IntentType

# Import response standardizer
from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Generic orchestrator that routes requests to the correct tools and chains.
    
    This orchestrator provides:
    - Intent classification and routing
    - Tool and chain execution
    - Context management and conversation memory
    - Error handling and fallback mechanisms
    - Workflow orchestration for complex tasks
    
    The orchestrator is domain-agnostic and can work with any type of content.
    """
    
    def __init__(self):
        # Generic tool mapping - only tools that are actually used in routing
        self.tools = {
            "ClaimDraftingTool": ClaimDraftingTool(),
            "ClaimReviewTool": ClaimReviewTool(),
            "PatentGuidanceTool": PatentGuidanceTool(),
            "PriorArtSearchTool": PriorArtSearchTool(),
            "GeneralConversationTool": GeneralConversationTool()
        }
        
        # No chains currently used - can be added later as needed
        self.chains = {}
        
        # Conversation memory
        self.conversation_memory = {}
        self.max_memory_size = 100
        
        # Intent classification cache
        self.intent_cache = {}
        self.cache_ttl = 300  # 5 minutes
        
        logger.info("Generic AgentOrchestrator initialized with tools and chains")
    
    async def handle(
        self, 
        user_input: str, 
        context: str = "", 
        session_id: str = None,
        parameters: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Main entry point for handling user requests.
        
        Args:
            user_input: The user's input text
            context: Additional context or requirements
            session_id: Unique session identifier for conversation memory
            parameters: Generic parameters that can be used by any domain
        
        Yields:
            Streaming events in standardized format
        """
        try:
            # Initialize session if not provided
            if not session_id:
                session_id = f"session_{datetime.now().timestamp()}"
            
            # Update conversation memory
            self._update_conversation_memory(session_id, user_input, context)
            
            logger.info(f"Processing request for session {session_id}: {user_input[:100]}...")
            
            # Yield initialization event
            yield create_thought_event(
                content=f"Processing request: {user_input[:100]}...",
                thought_type="initialization",
                metadata={"session_id": session_id, "input_length": len(user_input)}
            )
            
            # Step 1: Classify intent
            yield create_thought_event(
                content="Analyzing user intent...",
                thought_type="intent_analysis"
            )
            
            intent_type, confidence = await self._get_llm_based_intent(user_input, context)
            
            # Step 2: Route to appropriate tool or chain
            if intent_type in ["content_drafting", "content_review", "search", "guidance", "analysis", "query", "general_conversation"]:
                # Route to specific tool
                tool_name = self._get_tool_name_for_intent(intent_type)
                yield create_thought_event(
                    content=f"Routing to {tool_name}...",
                    thought_type="routing",
                    metadata={"intent": intent_type, "confidence": confidence}
                )
                
                # Execute the tool
                yield create_thought_event(
                    content=f"Executing {tool_name}...",
                    thought_type="tool_execution",
                    metadata={"tool": tool_name}
                )
                
                # Get conversation history for context
                conversation_history = self.conversation_memory.get(session_id, {}).get("messages", [])
                
                async for event in self._execute_tool(tool_name, user_input, context, parameters, conversation_history):
                    yield event
                    
            elif intent_type in ["analysis", "query"]:
                # Handle unimplemented tools gracefully
                yield create_thought_event(
                    content=f"Tool {intent_type} is not yet available...",
                    thought_type="tool_unavailable"
                )
                
                yield create_error_event(
                    error="Sorry, I currently can't do that. This feature is not yet implemented.",
                    context="tool_not_implemented"
                )
                
            else:
                # Default to general conversation
                yield create_thought_event(
                    content="Routing to general conversation tool...",
                    thought_type="routing",
                    metadata={"intent": "general_conversation", "confidence": 0.5}
                )
                
                # Get conversation history for context
                conversation_history = self.conversation_memory.get(session_id, {}).get("messages", [])
                
                async for event in self._execute_tool("GeneralConversationTool", user_input, context, parameters, conversation_history):
                    yield event
                    
        except Exception as e:
            logger.error(f"Error in orchestrator handle: {e}")
            yield create_error_event(
                error=f"Orchestrator error: {str(e)}",
                context="orchestrator_error"
            )
    
    def _get_tool_name_for_intent(self, intent_type: str) -> str:
        """Map intent types to tool names generically"""
        intent_to_tool = {
            "content_drafting": "ClaimDraftingTool",
            "content_review": "ClaimReviewTool", 
            "search": "PriorArtSearchTool",
            "guidance": "PatentGuidanceTool",
            "analysis": "GeneralConversationTool",    # Added mapping for analysis
            "query": "GeneralConversationTool",       # Added mapping for query
            "general_conversation": "GeneralConversationTool"
        }
        return intent_to_tool.get(intent_type, "GeneralConversationTool")
    
    async def _execute_tool(
        self, 
        tool_name: str, 
        user_input: str, 
        context: str,
        parameters: Optional[Dict[str, Any]] = None,
        conversation_history: Optional[List[Dict[str, Any]]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """Execute a specific tool with generic parameters"""
        try:
            tool = self.tools.get(tool_name)
            if not tool:
                yield create_error_event(
                    error=f"Tool {tool_name} not found",
                    context="tool_not_found"
                )
                return
            
            # Execute tool with generic parameters and conversation history
            async for event in tool.run(user_input, context, parameters=parameters or {}, conversation_history=conversation_history or []):
                yield event
                
        except Exception as e:
            logger.error(f"Tool execution failed for {tool_name}: {e}")
            yield create_error_event(
                error=f"Tool execution failed for {tool_name}: {str(e)}",
                context="tool_execution_error"
            )
    
    async def _get_llm_based_intent(self, user_input: str, context: str) -> tuple[str, float]:
        """Get intent classification using real LLM analysis"""
        try:
            from src.utils.llm_client import send_llm_request_streaming
            from src import prompt_loader
            import json
            
            # Use generic intent classification prompt
            messages = [
                {
                    "role": "system",
                    "content": prompt_loader.load_prompt("intent_classification_orchestrator_system")
                },
                {
                    "role": "user",
                    "content": prompt_loader.load_prompt(
                        "intent_classification_orchestrator_user",
                        user_input=user_input,
                        context=context
                    )
                }
            ]
            
            # Define function schema for structured output
            functions = [
                {
                    "type": "function",
                    "function": {
                        "name": "classify_intent",
                        "description": "Classify the user's intent based on their input",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "intent": {
                                    "type": "string",
                                    "enum": [
                                        "content_drafting",
                                        "content_review", 
                                        "search",
                                        "guidance",
                                        "analysis",
                                        "query",
                                        "general_conversation"
                                    ],
                                    "description": "The classified intent type"
                                },
                                "confidence": {
                                    "type": "number",
                                    "minimum": 0.0,
                                    "maximum": 1.0,
                                    "description": "Confidence score for the classification"
                                },
                                "reasoning": {
                                    "type": "string",
                                    "description": "Brief explanation of the classification"
                                }
                            },
                            "required": ["intent", "confidence"]
                        }
                    }
                }
            ]
            
            # Get LLM response
            response_content = ""
            function_arguments = ""
            
            async for chunk in send_llm_request_streaming(messages, functions=functions):
                if chunk.get("type") == "content_chunk":
                    response_content += chunk.get("content", "")
                elif chunk.get("type") == "function_call":
                    function_arguments += chunk.get("function_arguments", "")
                elif chunk.get("type") == "completion":
                    function_arguments = chunk.get("function_arguments", "")
                    break
            
            # Parse function call if available
            if function_arguments:
                try:
                    parsed_args = json.loads(function_arguments)
                    intent = parsed_args.get("intent", "general_conversation")
                    confidence = parsed_args.get("confidence", 0.5)
                    return intent, confidence
                except json.JSONDecodeError:
                    logger.warning("Failed to parse function arguments, using fallback")
            
            # Fallback to response content analysis
            if "content" in response_content.lower() and "draft" in response_content.lower():
                return "content_drafting", 0.8
            elif "search" in response_content.lower() and "find" in response_content.lower():
                return "search", 0.8
            elif "guidance" in response_content.lower() or "advice" in response_content.lower():
                return "guidance", 0.7
            elif "analysis" in response_content.lower() or "analyze" in response_content.lower():
                return "analysis", 0.7
            else:
                return "general_conversation", 0.6
                
        except Exception as e:
            logger.error(f"LLM-based intent classification failed: {e}")
            # Return default intent on failure
            return "general_conversation", 0.5
    
    def _update_conversation_memory(self, session_id: str, user_input: str, context: str):
        """Update conversation memory generically"""
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = {
                "messages": [],
                "last_updated": datetime.now().isoformat()
            }
        
        self.conversation_memory[session_id]["messages"].append({
            "input": user_input,
            "context": context,
            "timestamp": datetime.now().isoformat()
        })
        
        # Limit memory size
        if len(self.conversation_memory[session_id]["messages"]) > self.max_memory_size:
            self.conversation_memory[session_id]["messages"] = self.conversation_memory[session_id]["messages"][-self.max_memory_size:]
        
        self.conversation_memory[session_id]["last_updated"] = datetime.now().isoformat()
    
    def get_status(self) -> Dict[str, Any]:
        """Get orchestrator status generically"""
        return {
            "status": "operational",
            "tools_available": list(self.tools.keys()),
            "chains_available": list(self.chains.keys()),
            "active_sessions": len(self.conversation_memory),
            "memory_size": sum(len(session["messages"]) for session in self.conversation_memory.values()),
            "timestamp": datetime.now().isoformat()
        }
    
    def clear_memory(self):
        """Clear conversation memory generically"""
        self.conversation_memory.clear()
        self.intent_cache.clear()
        logger.info("Conversation memory and intent cache cleared")
    
    def get_tool(self, tool_name: str):
        """Get a specific tool by name"""
        return self.tools.get(tool_name)
    
    def get_chain(self, chain_name: str):
        """Get a specific chain by name"""
        return self.chains.get(chain_name)
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return list(self.tools.keys())
