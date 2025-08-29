from typing import AsyncGenerator, Dict, Any, List, Optional
import logging
import os
from datetime import datetime
import asyncio
from dotenv import load_dotenv

# Load environment variables from .env file
# The .env file is in the agentic_native_drafting directory
import pathlib
env_path = pathlib.Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

# Import only the tools that are actually used in routing
try:
    from src.tools.claim_drafting_tool import ContentDraftingTool
    from src.tools.claim_review_tool import ContentReviewTool
    from src.tools.patent_guidance_tool import GeneralGuidanceTool
    from src.tools.prior_art_search_tool import PriorArtSearchTool
    from src.tools.general_conversation_tool import GeneralConversationTool

    # Import self-contained components
    from src.utils.enums import IntentType

    # Import response standardizer
    from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
except ImportError:
    # Fallback for when running from src directory
    from ..tools.claim_drafting_tool import ContentDraftingTool
    from ..tools.claim_review_tool import ContentReviewTool
    from ..tools.patent_guidance_tool import GeneralGuidanceTool
    from ..tools.prior_art_search_tool import PriorArtSearchTool
    from ..tools.general_conversation_tool import GeneralConversationTool

    # Import self-contained components
    from ..utils.enums import IntentType

    # Import response standardizer
    from ..utils.response_standardizer import create_thought_event, create_results_event, create_error_event

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
            "ContentDraftingTool": ContentDraftingTool(),
            "ContentReviewTool": ContentReviewTool(),
            "GeneralGuidanceTool": GeneralGuidanceTool(),
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
        parameters: Optional[Dict[str, Any]] = None,
        document_content: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Main entry point for handling user requests.
        
        Args:
            user_input: The user's input text
            context: Additional context or requirements
            session_id: Unique session identifier for conversation memory
            parameters: Generic parameters that can be used by any domain
            document_content: Document content for context-aware processing
        
        Yields:
            Streaming events in standardized format
        """
        try:
            print(f"🔍 ORCHESTRATOR DEBUG: handle() called with:")
            print(f"   user_input: {user_input}")
            print(f"   context: {context}")
            print(f"   session_id: {session_id}")
            print(f"   parameters: {parameters}")
            print(f"   document_content: {document_content}")
            print(f"🔍 ORCHESTRATOR DEBUG: Current memory keys: {list(self.conversation_memory.keys())}")
            
            # Initialize session if not provided
            if not session_id:
                session_id = f"session_{datetime.now().timestamp()}"
                print(f"🔍 ORCHESTRATOR DEBUG: Generated new session_id: {session_id}")
            
            # Update conversation memory
            print(f"🔍 ORCHESTRATOR DEBUG: About to call _update_conversation_memory")
            self._update_conversation_memory(session_id, user_input, context)
            
            # Enhance context with document content if available
            enhanced_context = self._build_enhanced_context(context, document_content, session_id)
            
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
            
            intent_type, confidence = await self._get_llm_based_intent(user_input, enhanced_context)
            
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
                print(f"🔍 ORCHESTRATOR DEBUG: About to get conversation history for session: {session_id}")
                conversation_history = self.conversation_memory.get(session_id, {}).get("messages", [])
                print(f"🔍 ORCHESTRATOR DEBUG: Using session_id: '{session_id}'")
                print(f"🔍 ORCHESTRATOR DEBUG: Memory keys available: {list(self.conversation_memory.keys())}")
                print(f"🔍 ORCHESTRATOR DEBUG: Found conversation history: {len(conversation_history)} messages")
                if conversation_history:
                    print(f"🔍 ORCHESTRATOR DEBUG: First message preview: {conversation_history[0].get('content', 'NO CONTENT')[:100]}...")
                    print(f"🔍 ORCHESTRATOR DEBUG: First message keys: {list(conversation_history[0].keys())}")
                else:
                    print(f"🔍 ORCHESTRATOR DEBUG: No conversation history found for session '{session_id}'")
                
                print(f"🔍 ORCHESTRATOR DEBUG: About to call _execute_tool with conversation_history length: {len(conversation_history)}")
                async for event in self._execute_tool(tool_name, user_input, enhanced_context, parameters, conversation_history, document_content):
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
                
                async for event in self._execute_tool("GeneralConversationTool", user_input, enhanced_context, parameters, conversation_history, document_content):
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
            "content_drafting": "ContentDraftingTool",
            "content_review": "ContentReviewTool", 
            "search": "PriorArtSearchTool",
            "guidance": "GeneralGuidanceTool",
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
        conversation_history: Optional[List[Dict[str, Any]]] = None,
        document_content: Optional[Dict[str, Any]] = None
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
            
            # Execute tool with generic parameters, conversation history, and document content
            async for event in tool.run(user_input, parameters=parameters or {}, conversation_history=conversation_history or [], document_content=document_content):
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
            try:
                from src.utils.llm_client import send_llm_request_streaming
                from src.prompt_loader import prompt_loader
            except ImportError:
                from ..utils.llm_client import send_llm_request_streaming
                from ..prompt_loader import prompt_loader
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
        """Update conversation memory using API format (role/content)"""
        if session_id not in self.conversation_memory:
            self.conversation_memory[session_id] = {
                "messages": [],
                "last_updated": datetime.now().isoformat()
            }
        
        # Only append if this is a new message (don't overwrite existing conversation history)
        # Check if this exact message already exists to avoid duplicates
        existing_messages = self.conversation_memory[session_id]["messages"]
        message_exists = any(
            msg.get("content") == user_input and msg.get("role") == "user" 
            for msg in existing_messages
        )
        
        if not message_exists:
            self.conversation_memory[session_id]["messages"].append({
                "role": "user",
                "content": user_input,
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
    
    def _build_enhanced_context(self, context: str, document_content: Optional[Dict[str, Any]], session_id: str) -> str:
        """Build enhanced context by combining user context, document content, and conversation history"""
        print(f"🔍 ORCHESTRATOR DEBUG: _build_enhanced_context called with:")
        print(f"   context: {context}")
        print(f"   session_id: {session_id}")
        print(f"   document_content: {document_content}")
        
        context_parts = [context] if context else []
        
        # Add document content context
        if document_content:
            doc_context = self._build_document_context(document_content)
            if doc_context:
                context_parts.append(f"DOCUMENT CONTEXT:\n{doc_context}")
                print(f"🔍 ORCHESTRATOR DEBUG: Added document context: {len(doc_context)} chars")
        
        # Add conversation history context
        print(f"🔍 ORCHESTRATOR DEBUG: About to get conversation history for context building")
        conversation_history = self.conversation_memory.get(session_id, {}).get("messages", [])
        print(f"🔍 ORCHESTRATOR DEBUG: Found conversation history: {len(conversation_history)} messages")
        
        if conversation_history:
            history_context = self._build_conversation_context(conversation_history)
            if history_context:
                context_parts.append(f"CONVERSATION HISTORY:\n{history_context}")
                print(f"🔍 ORCHESTRATOR DEBUG: Added conversation history context: {len(history_context)} chars")
            else:
                print(f"🔍 ORCHESTRATOR DEBUG: No history context generated")
        else:
            print(f"🔍 ORCHESTRATOR DEBUG: No conversation history found for context building")
        
        final_context = "\n\n".join(context_parts)
        print(f"🔍 ORCHESTRATOR DEBUG: Final enhanced context length: {len(final_context)} chars")
        return final_context
    
    def _build_document_context(self, document_content: Dict[str, Any]) -> str:
        """Build context from document content"""
        context_parts = []
        
        if document_content.get("text"):
            # Extract key information from document
            doc_text = document_content["text"]
            # Limit to first 500 characters to avoid overwhelming context
            context_parts.append(f"Document content: {doc_text[:500]}{'...' if len(doc_text) > 500 else ''}")
        
        if document_content.get("paragraphs"):
            # Use paragraph structure
            context_parts.append(f"Document structure: {len(document_content['paragraphs'])} paragraphs")
        
        if document_content.get("session_id"):
            context_parts.append(f"Document session: {document_content['session_id']}")
        
        return "\n".join(context_parts)
    
    def _build_conversation_context(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Build context from conversation history using unified API format (role/content)"""
        print(f"🔍 ORCHESTRATOR DEBUG: _build_conversation_context called with {len(conversation_history)} entries")
        
        if not conversation_history:
            print(f"🔍 ORCHESTRATOR DEBUG: No conversation history provided")
            return ""
        
        # Take last 5 entries to avoid overwhelming context
        recent_history = conversation_history[-5:]
        context_parts = []
        
        print(f"🔍 ORCHESTRATOR DEBUG: Processing {len(recent_history)} recent entries")
        
        for i, entry in enumerate(recent_history):
            print(f"🔍 ORCHESTRATOR DEBUG: Processing entry {i+1}: {list(entry.keys())}")
            
            # Handle unified API format (role/content)
            if entry.get("role") and entry.get("content"):
                role = entry["role"]
                content = entry["content"]
                print(f"🔍 ORCHESTRATOR DEBUG: Processing API format entry with role: {role}")
                
                if role == "user":
                    context_parts.append(f"USER REQUEST {i+1}: {content[:200]}{'...' if len(content) > 200 else ''}")
                    print(f"🔍 ORCHESTRATOR DEBUG: Added user request context")
                elif role == "assistant":
                    # Look for patent claims in assistant responses
                    if "Generated Patent Claims:" in content:
                        claims_start = content.find("Generated Patent Claims:")
                        claims_section = content[claims_start:]
                        claims_text = claims_section.replace("Generated Patent Claims:", "PREVIOUSLY GENERATED CLAIMS:")
                        context_parts.append(f"ASSISTANT RESPONSE {i+1}: {claims_text[:800]}...")
                        print(f"🔍 ORCHESTRATOR DEBUG: Added assistant response with patent claims")
                    else:
                        context_parts.append(f"ASSISTANT RESPONSE {i+1}: {content[:300]}...")
                        print(f"🔍 ORCHESTRATOR DEBUG: Added assistant response without patent claims")
                else:
                    print(f"🔍 ORCHESTRATOR DEBUG: Unknown role: {role}")
            else:
                print(f"🔍 ORCHESTRATOR DEBUG: Entry {i+1} missing role or content field: {list(entry.keys())}")
        
        final_context = "\n".join(context_parts)
        print(f"🔍 ORCHESTRATOR DEBUG: Generated conversation context: {len(final_context)} chars")
        return final_context
