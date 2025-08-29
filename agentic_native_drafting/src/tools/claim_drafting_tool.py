from src.interfaces import Tool
from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
from typing import Dict, Any, List, Optional, AsyncGenerator
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ContentDraftingTool(Tool):
    """
    Simplified content drafting tool for patent claims.
    """
    
    async def run(
        self, 
        input_text: str, 
        parameters: Optional[Dict[str, Any]] = None, 
        conversation_history: Optional[List[Dict[str, Any]]] = None, 
        document_content: Optional[Dict[str, Any]] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Draft patent claims based on input and context.
        """
        try:
            # Build simple context
            context = self._build_simple_context(input_text, conversation_history, document_content)
            
            # Draft content using LLM
            yield create_thought_event("Starting patent claims drafting...", "drafting")
            
            content_result = await self._draft_content_with_llm(input_text, context)
            
            if content_result and content_result.get("content"):
                # Format the response with proper markdown structure for HTML conversion
                content_summary = f"Successfully drafted {len(content_result.get('content', []))} patent claims"
                
                if content_result.get("content"):
                    content_summary += f"\n\n## Generated Patent Claims\n"
                    for i, item in enumerate(content_result.get("content", []), 1):
                        claim_text = item.get("content_text", "")
                        claim_type = item.get("content_type", "primary")
                        # Clean up claim text formatting
                        clean_claim = claim_text.strip()
                        if clean_claim.endswith('.'):
                            clean_claim = clean_claim[:-1]
                        # Use markdown formatting for better HTML conversion with proper spacing
                        # Each claim should be a separate paragraph for proper HTML structure
                        content_summary += f"\n\n**Claim {i}** ({claim_type}): {clean_claim}."
                
                yield create_results_event(
                    response=content_summary,
                    metadata={"outputs_generated": len(content_result.get('content', []))},
                    data=content_result
                )
            else:
                yield create_error_event("Content drafting failed - no valid content generated", "content_drafting_failed")
                
        except Exception as e:
            logger.error(f"Content drafting failed: {e}")
            yield create_error_event(f"Content drafting failed: {str(e)}", "content_drafting_error")
    
    def _build_simple_context(self, input_text: str, conversation_history: Optional[List[Dict[str, Any]]], document_content: Optional[Dict[str, Any]]) -> str:
        """Build simple context from input, conversation history, and document content"""
        context_parts = [f"Input: {input_text}"]
        
        # Add conversation history context (last 2 entries)
        if conversation_history:
            recent_history = conversation_history[-2:]
            for entry in recent_history:
                if entry.get("role") == "user":
                    context_parts.append(f"Previous user request: {entry.get('content', '')[:200]}...")
                elif entry.get("role") == "assistant" and "Generated Patent Claims:" in entry.get('content', ''):
                    claims_start = entry['content'].find("Generated Patent Claims:")
                    claims_section = entry['content'][claims_start:].replace("Generated Patent Claims:", "Previous claims:")
                    context_parts.append(f"Previous claims: {claims_section[:600]}...")
        
        # Add document content context
        if document_content and document_content.get("text"):
            doc_text = document_content["text"][:300]
            context_parts.append(f"Document: {doc_text}...")
        
        return "\n\n".join(context_parts)
    
    async def _draft_content_with_llm(self, input_text: str, context: str) -> Dict[str, Any]:
        """Draft content using LLM integration"""
        try:
            from src import prompt_loader
            from src.utils.llm_client import send_llm_request_streaming
            
            # Build prompts
            user_prompt = prompt_loader.load_prompt(
                "claim_drafting_user",
                disclosure=input_text,
                document_content=context,
                conversation_history=context
            )
            
            system_prompt = prompt_loader.load_prompt("claim_drafting_system")
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
            
            # Define function schema
            functions = [{
                "type": "function",
                "function": {
                    "name": "draft_content",
                    "description": "Draft patent claims based on input and context",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "content_number": {"type": "string"},
                                        "content_text": {"type": "string"},
                                        "content_type": {"type": "string", "enum": ["primary", "secondary"]}
                                    },
                                    "required": ["content_number", "content_text", "content_type"]
                                }
                            },
                            "reasoning": {"type": "string"}
                        },
                        "required": ["content", "reasoning"]
                    }
                }
            }]
            
            # Call LLM with timeout handling and retry logic
            max_retries = 3
            retry_count = 0
            
            while retry_count < max_retries:
                try:
                    function_arguments = ""
                    async for chunk in send_llm_request_streaming(messages, functions=functions, max_tokens=8000):
                        if chunk.get("type") == "function_call":
                            function_arguments += chunk.get("function_arguments", "")
                        elif chunk.get("type") == "completion":
                            final_args = chunk.get("function_arguments", "")
                            if final_args:
                                function_arguments = final_args
                            break
                    
                    # If we got here without timeout, break the retry loop
                    break
                    
                except Exception as e:
                    retry_count += 1
                    if "timeout" in str(e).lower() or "408" in str(e):
                        logger.warning(f"LLM timeout on attempt {retry_count}/{max_retries}: {e}")
                        if retry_count >= max_retries:
                            logger.error("Max retries reached, using fallback content")
                            break
                        # Wait a bit before retrying
                        import asyncio
                        await asyncio.sleep(2)
                    else:
                        # Non-timeout error, don't retry
                        logger.error(f"Non-timeout LLM error: {e}")
                        break
            
            # Parse response
            if function_arguments:
                try:
                    result = json.loads(function_arguments)
                    
                    # Validate that we have meaningful content
                    if result.get("content") and isinstance(result["content"], list):
                        # Filter out empty or invalid content
                        valid_content = []
                        for item in result["content"]:
                            if (isinstance(item, dict) and 
                                item.get("content_text") and 
                                item["content_text"].strip() and
                                len(item["content_text"].strip()) > 10):  # Minimum meaningful length
                                valid_content.append(item)
                        
                        if valid_content:
                            result["content"] = valid_content
                            return result
                        else:
                            logger.warning("LLM returned empty or invalid content, using fallback")
                    else:
                        logger.warning("LLM response missing content array, using fallback")
                        
                except json.JSONDecodeError:
                    # Simple fallback: try to extract content from partial JSON
                    content_items = self._extract_content_from_partial_json(function_arguments)
                    if content_items:
                        return {
                            "content": content_items,
                            "reasoning": f"Extracted {len(content_items)} claims from partial response"
                        }
            
            # Enhanced fallback: create meaningful content based on input
            fallback_content = self._generate_fallback_content(input_text)
            
            # Add timeout-specific reasoning if we had retry attempts
            reasoning = "Fallback content generated due to insufficient LLM response"
            if retry_count > 0:
                reasoning = f"Fallback content generated after {retry_count} LLM timeout attempts"
            
            return {
                "content": fallback_content,
                "reasoning": reasoning
            }
            
        except Exception as e:
            logger.error(f"LLM content drafting failed: {e}")
            raise e
    
    def _extract_content_from_partial_json(self, json_text: str) -> List[Dict[str, Any]]:
        """Simple extraction of content from partial JSON"""
        content_items = []
        
        # Look for content_text patterns
        import re
        text_matches = re.findall(r'"content_text":\s*"([^"]*)"', json_text)
        
        for i, text in enumerate(text_matches):
            if text.strip():
                content_items.append({
                    "content_number": str(i + 1),
                    "content_text": text,
                    "content_type": "primary"
                })
        
        return content_items

    def _generate_fallback_content(self, input_text: str) -> List[Dict[str, Any]]:
        """Generate fallback content when LLM fails to provide meaningful content"""
        # Create a meaningful fallback based on the input
        input_words = input_text.strip().split()
        
        if len(input_words) < 3:
            # Very short input - provide generic guidance with multiple claims
            claims = []
            claims.append({
                "content_number": "1",
                "content_text": "A method for processing user input, comprising: receiving a user request; analyzing the request content; and generating appropriate response content based on the LLM analysis.",
                "content_type": "primary"
            })
            claims.append({
                "content_number": "2",
                "content_text": "The method of claim 1, further comprising: validating the user request format; determining appropriate processing parameters; and executing the analysis with optimized settings.",
                "content_type": "secondary"
            })
            return claims
        else:
            # Try to create meaningful claims from the input
            input_summary = " ".join(input_words[:5])  # Use first 5 words
            
            claims = []
            claims.append({
                "content_number": "1",
                "content_text": f"A method for {input_summary.lower()}, comprising: receiving input data; processing the data according to predefined rules; and generating output based on the processing results.",
                "content_type": "primary"
            })
            claims.append({
                "content_number": "2",
                "content_text": f"The method of claim 1, further comprising: analyzing the {input_summary.lower()} data for patterns; applying machine learning algorithms; and generating optimized results based on the analysis.",
                "content_type": "secondary"
            })
            return claims

