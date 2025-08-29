try:
            from src.interfaces import Tool
            from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
except ImportError:
    from agentic_native_drafting.src.interfaces import Tool
    from agentic_native_drafting.src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
from typing import Dict, Any, Optional, AsyncGenerator, List
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class GeneralConversationTool(Tool):
    """
    Generic conversation tool that can handle any type of user input.
    
    This tool provides:
    - General conversation capabilities
    - Context-aware responses
    - Multi-domain knowledge
    - Helpful guidance and explanations
    """
    
    def __init__(self):
        self.max_response_length = 2000
        self.enable_context_analysis = True
        
    async def run(self, user_input: str, context: str = "", parameters: Optional[Dict[str, Any]] = None, conversation_history: Optional[List[Dict[str, Any]]] = None, document_content: Optional[Dict[str, Any]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process general conversation requests.
        
        Args:
            user_input: The user's input text
            context: Additional context or conversation history
            parameters: Generic parameters that can be used by any domain
            conversation_history: Previous conversation context
            document_content: Document content for context-aware responses
        
        Yields:
            Streaming events in standardized format
        """
        try:
            # Extract parameters with defaults
            params = parameters or {}
            max_length = params.get('max_response_length', self.max_response_length)
            enable_analysis = params.get('enable_context_analysis', self.enable_context_analysis)
            
            # Process context from conversation history and document content
            enhanced_context = self._build_enhanced_conversation_context(user_input, context, conversation_history, document_content)
            
            logger.info(f"Processing general conversation request: {user_input[:100]}...")
            logger.info(f"Enhanced context: {enhanced_context[:200]}...")
            
            # Yield initialization event
            yield create_thought_event(
                content=f"Processing general conversation request: {user_input[:100]}...",
                thought_type="initialization"
            )
            
            # Analyze user input and context if enabled
            if enable_analysis:
                yield create_thought_event(
                    content="Analyzing user input and generating response...",
                    thought_type="processing"
                )
            
            # Generate response using LLM
            response = await self._generate_conversation_response(user_input, enhanced_context, max_length, params)
            
            if response:
                # Create metadata
                metadata = {
                    "input_length": len(user_input),
                    "context_length": len(context),
                    "response_length": len(response),
                    "timestamp": datetime.now().isoformat()
                }
                
                # Create data payload
                data = {
                    "response": response,
                    "reasoning": "Generated through general conversation analysis",
                    "input": user_input,
                    "context": context
                }
                
                # Yield results event
                yield create_results_event(
                    response=response,
                    metadata=metadata,
                    data=data
                )
            else:
                yield create_error_event(
                    error="Failed to generate conversation response",
                    context="conversation_generation_failed"
                )
                
        except Exception as e:
            logger.error(f"General conversation failed: {e}")
            yield create_error_event(
                error=f"General conversation failed: {str(e)}",
                context="conversation_error"
            )
    
    async def _generate_conversation_response(
        self, 
        user_input: str, 
        context: str, 
        max_length: int,
        parameters: Dict[str, Any]
    ) -> str:
        """Generate conversation response using LLM"""
        try:
            from ..prompt_loader import prompt_loader
            from ..utils.llm_client import send_llm_request_streaming
            
            # Prepare conversation messages
            conversation_messages = [
                {
                    "role": "system",
                    "content": prompt_loader.load_prompt("general_conversation_system")
                },
                {
                    "role": "user",
                    "content": prompt_loader.load_prompt(
                        "general_conversation_user",
                        user_input=user_input,
                        context=context
                    )
                }
            ]
            
            # Generate response
            response_content = ""
            
            async for chunk in send_llm_request_streaming(conversation_messages, max_tokens=max_length):
                if chunk.get("type") == "content_chunk":
                    response_content += chunk.get("content", "")
                elif chunk.get("type") == "completion":
                    break
            
            # Truncate if too long
            if len(response_content) > max_length:
                response_content = response_content[:max_length-3] + "..."
            
            return response_content
            
        except Exception as e:
            logger.error(f"LLM conversation generation failed: {e}")
            raise e
    
    def _build_enhanced_conversation_context(self, user_input: str, context: str, conversation_history: Optional[List[Dict[str, Any]]], document_content: Optional[Dict[str, Any]]) -> str:
        """Build enhanced conversation context from conversation history and document content"""
        context_parts = [f"User input: {user_input}"]
        
        if context:
            context_parts.append(f"Additional context: {context}")
        
        # Add conversation history context
        if conversation_history:
            history_context = self._build_conversation_context(conversation_history)
            if history_context:
                context_parts.append(f"CONVERSATION HISTORY:\n{history_context}")
        
        # Add document content context
        if document_content:
            doc_context = self._build_document_context(document_content)
            if doc_context:
                context_parts.append(f"DOCUMENT CONTENT:\n{doc_context}")
        
        return "\n\n".join(context_parts)
    
    def _build_conversation_context(self, conversation_history: List[Dict[str, Any]]) -> str:
        """Build context from conversation history"""
        if not conversation_history:
            return ""
        
        # Take last 3 entries to avoid overwhelming context
        recent_history = conversation_history[-3:]
        context_parts = []
        
        for i, entry in enumerate(recent_history):
            if entry.get("input"):
                context_parts.append(f"Previous request {i+1}: {entry['input'][:150]}{'...' if len(entry['input']) > 150 else ''}")
            elif entry.get("content"):
                context_parts.append(f"Previous response {i+1}: {entry['content'][:150]}{'...' if len(entry['content']) > 150 else ''}")
        
        return "\n".join(context_parts)
    
    def _build_document_context(self, document_content: Dict[str, Any]) -> str:
        """Build context from document content"""
        context_parts = []
        
        if document_content.get("text"):
            # Extract key information from document
            doc_text = document_content["text"]
            # Limit to first 300 characters to avoid overwhelming context
            context_parts.append(f"Document content: {doc_text[:300]}{'...' if len(doc_text) > 300 else ''}")
        
        if document_content.get("paragraphs"):
            # Use paragraph structure
            context_parts.append(f"Document structure: {len(document_content['paragraphs'])} paragraphs")
        
        if document_content.get("session_id"):
            context_parts.append(f"Document session: {document_content['session_id']}")
        
        return "\n".join(context_parts)
