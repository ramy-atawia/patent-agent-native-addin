from src.interfaces import Tool
from src.utils.response_standardizer import create_thought_event, create_results_event, create_error_event
from typing import Dict, Any, List, Optional, AsyncGenerator
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class ClaimDraftingTool(Tool):
    """
    Generic content drafting tool that can work with any domain.
    
    This tool provides:
    - Content drafting based on input and context
    - Multiple output types and formats
    - Content validation and formatting
    - Integration with content assessment
    """
    
    def __init__(self):
        self.max_outputs = 20
        self.max_output_length = 500  # characters per output
        
    async def run(self, input_text: str, context: str = "", parameters: Optional[Dict[str, Any]] = None, conversation_history: Optional[List[Dict[str, Any]]] = None) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Draft content based on input and context.
        
        Args:
            input_text: The main input text
            context: Additional context or requirements
            parameters: Generic parameters that can be used by any domain
        
        Yields:
            Streaming events in standardized format
        """
        try:
            # Extract parameters with defaults
            params = parameters or {}
            max_outputs = params.get('max_outputs', self.max_outputs)
            output_types = params.get('output_types', ["primary", "secondary"])
            focus_areas = params.get('focus_areas', [])
            additional_context = params.get('additional_context', "")
            
            logger.info(f"Starting content drafting for input of length {len(input_text)}")
            logger.info(f"Parameters: max_outputs={max_outputs}, output_types={output_types}")
            
            # Yield progress event
            yield create_thought_event(
                content=f"Starting content drafting process for {len(input_text)} character input",
                thought_type="initialization",
                metadata={"input_length": len(input_text), "max_outputs": max_outputs}
            )
            
            # Optional: Assess input sufficiency first
            input_assessment = None
            if params.get('assess_input', True):
                yield create_thought_event(
                    content="Assessing input sufficiency for content drafting...",
                    thought_type="assessment"
                )
                
                input_assessment = self._assess_input_sufficiency(input_text)
                
                if input_assessment.get("sufficiency_score", 0.0) < 0.5:
                    yield create_thought_event(
                        content=f"Input sufficiency score is low ({input_assessment.get('sufficiency_score', 0.0):.2f}). Consider enhancing the input.",
                        thought_type="warning",
                        metadata={"sufficiency_score": input_assessment.get("sufficiency_score", 0.0)}
                    )
                else:
                    yield create_thought_event(
                        content=f"Input sufficiency score: {input_assessment.get('sufficiency_score', 0.0):.2f} - Good for content drafting",
                        thought_type="assessment_complete",
                        metadata={"sufficiency_score": input_assessment.get("sufficiency_score", 0.0)}
                    )
            
            # Draft content using LLM
            yield create_thought_event(
                content="Drafting content using LLM analysis...",
                thought_type="drafting"
            )
            
            content_result = await self._draft_content_with_llm(
                input_text, context, additional_context,
                max_outputs, output_types, focus_areas
            )
            
            # Validate and format content
            yield create_thought_event(
                content="Validating and formatting drafted content...",
                thought_type="validation"
            )
            
            if content_result and content_result.get("content"):
                # Format the response
                response = self._format_response(input_text, content_result, input_assessment)
                
                yield create_results_event(
                    response=f"Successfully drafted {len(content_result.get('content', []))} content items",
                    metadata={"input_length": len(input_text), "outputs_generated": len(content_result.get('content', []))},
                    data=response
                )
            else:
                yield create_error_event(
                    error="Content drafting failed - no valid content generated",
                    context="content_drafting_failed"
                )
                
        except Exception as e:
            logger.error(f"Content drafting failed: {e}")
            yield create_error_event(
                error=f"Content drafting failed: {str(e)}",
                context="content_drafting_error"
            )
    
    def _assess_input_sufficiency(self, input_text: str) -> Dict[str, Any]:
        """Assess whether the input is sufficient for content drafting"""
        try:
            # Simple heuristic assessment
            word_count = len(input_text.split())
            content_indicators = self._count_content_indicators(input_text)
            
            assessment = {
                "word_count": word_count,
                "content_indicators_count": content_indicators,
                "sufficiency_score": min(1.0, (word_count / 100) * (content_indicators / 10)),
                "recommendations": []
            }
            
            if word_count < 50:
                assessment["recommendations"].append("Consider adding more detailed description")
            if content_indicators < 5:
                assessment["recommendations"].append("Include more descriptive content")
            if assessment["sufficiency_score"] < 0.5:
                assessment["recommendations"].append("Input may be insufficient for comprehensive content drafting")
            
            return assessment
            
        except Exception as e:
            logger.warning(f"Input assessment failed: {e}")
            return {"error": "Assessment failed", "sufficiency_score": 0.5}
    
    def _count_content_indicators(self, text: str) -> int:
        """Count content indicators in the text (simple heuristic)"""
        content_indicators = [
            "method", "system", "process", "technique", "approach",
            "algorithm", "protocol", "interface", "component", "module",
            "data", "information", "content", "structure", "format",
            "analysis", "evaluation", "assessment", "review", "summary"
        ]
        
        text_lower = text.lower()
        count = sum(1 for term in content_indicators if term in text_lower)
        return count
    
    async def _draft_content_with_llm(
        self, 
        input_text: str, 
        context: str, 
        additional_context: str,
        max_outputs: int,
        output_types: List[str],
        focus_areas: List[str]
    ) -> Dict[str, Any]:
        """Draft content using LLM integration"""
        try:
            from src import prompt_loader
            from src.utils.llm_client import send_llm_request_streaming
            
            # Prepare the prompt
            drafting_messages = [
                {
                    "role": "system",
                    "content": prompt_loader.load_prompt("claims_generation_system")
                },
                {
                    "role": "user",
                    "content": prompt_loader.load_prompt(
                        "claims_generation_user",
                        disclosure=input_text,
                        document_content=context,
                        conversation_history=additional_context,
                        analysis_content="",
                        max_claims=max_outputs,
                        claim_types=", ".join(output_types),
                        focus_areas=", ".join(focus_areas) if focus_areas else "General",
                        prior_art_context=""
                    )
                }
            ]
            
            # Define function schema for structured output
            functions = [
                {
                    "type": "function",
                    "function": {
                        "name": "draft_content",
                        "description": "Draft content based on input and context",
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
                                            "content_type": {"type": "string", "enum": ["primary", "secondary"]},
                                            "dependency": {"type": "string"},
                                            "focus_area": {"type": "string"}
                                        },
                                        "required": ["content_number", "content_text", "content_type"]
                                    }
                                },
                                "reasoning": {
                                    "type": "string",
                                    "description": "Explanation of the drafting approach"
                                },
                                "input_assessment": {
                                    "type": "object",
                                    "properties": {
                                        "sufficiency_score": {"type": "number"},
                                        "strengths": {"type": "array", "items": {"type": "string"}},
                                        "areas_for_improvement": {"type": "array", "items": {"type": "string"}}
                                    }
                                }
                            },
                            "required": ["content", "reasoning"]
                        }
                    }
                }
            ]
            
            # Call LLM for content drafting
            response_content = ""
            function_arguments = ""
            
            async for chunk in send_llm_request_streaming(drafting_messages, functions=functions):
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
                    result = json.loads(function_arguments)
                    return result
                except json.JSONDecodeError:
                    logger.warning("Failed to parse function arguments, using fallback")
            
            # Fallback to response content analysis
            return {
                "content": [
                    {
                        "content_number": "1",
                        "content_text": response_content[:200] + "..." if len(response_content) > 200 else response_content,
                        "content_type": "primary",
                        "focus_area": "general"
                    }
                ],
                "reasoning": "Generated from LLM response content",
                "input_assessment": {
                    "sufficiency_score": 0.7,
                    "strengths": ["LLM-generated content"],
                    "areas_for_improvement": ["Consider using function calling for structured output"]
                }
            }
            
        except Exception as e:
            logger.error(f"LLM content drafting failed: {e}")
            raise e
    
    def _format_response(self, input_text: str, content_result: Dict[str, Any], input_assessment: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Format the response generically"""
        try:
            response = {
                "content": content_result.get("content", []),
                "reasoning": content_result.get("reasoning", "Content drafted based on input"),
                "input_assessment": input_assessment or {},
                "metadata": {
                    "input_length": len(input_text),
                    "outputs_generated": len(content_result.get("content", [])),
                    "timestamp": datetime.now().isoformat()
                }
            }
            
            return response
            
        except Exception as e:
            logger.error(f"Response formatting failed: {e}")
            return {
                "error": f"Response formatting failed: {str(e)}",
                "content": [],
                "metadata": {"timestamp": datetime.now().isoformat()}
            }

