from src.interfaces import Tool
from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
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
        
    async def run(self, user_input: str, context: str = "", parameters: Optional[Dict[str, Any]] = None, conversation_history: Optional[List[Dict[str, Any]]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Process general conversation requests.
        
        Args:
            user_input: The user's input text
            context: Additional context or conversation history
            parameters: Generic parameters that can be used by any domain
        
        Yields:
            Streaming events in standardized format
        """
        try:
            # Extract parameters with defaults
            params = parameters or {}
            max_length = params.get('max_response_length', self.max_response_length)
            enable_analysis = params.get('enable_context_analysis', self.enable_context_analysis)
            
            logger.info(f"Processing general conversation request: {user_input[:100]}...")
            
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
            response = await self._generate_conversation_response(user_input, context, max_length, params)
            
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
            from src import prompt_loader
            from src.utils.llm_client import send_llm_request_streaming
            
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
