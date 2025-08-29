from typing import List, Dict, Optional, Any, AsyncGenerator
import os
import json
import logging
import httpx
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from enum import Enum

from .models import AgentResponse, ReviewComment
from .prior_art_search import PatentSearchEngine, PatentSearchConfig
from .prompt_loader import prompt_loader

# Load environment variables
load_dotenv()

class IntentType(str, Enum):
    """Types of user intent the agent can recognize"""
    CLAIM_DRAFTING = "claim_drafting"
    CLAIM_REVIEW = "claim_review"
    PATENT_GUIDANCE = "patent_guidance"
    INVENTION_ANALYSIS = "invention_analysis"
    TECHNICAL_QUERY = "technical_query"
    GENERAL_CONVERSATION = "general_conversation"
    PRIOR_ART_SEARCH = "prior_art_search"

class IntentClassification(BaseModel):
    """Result of intent classification"""
    intent: IntentType
    confidence_score: float
    reasoning: str
    suggested_actions: List[str]
    requires_context: bool

def get_azure_config():
    """Get Azure OpenAI configuration with validation"""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    
    if not endpoint or not api_key or not deployment_name:
        raise RuntimeError(f"Missing Azure OpenAI config: endpoint={bool(endpoint)}, deployment={bool(deployment_name)}, api_key={bool(api_key)}")
    
    return {
        "endpoint": endpoint.rstrip("/"),
        "api_key": api_key,
        "deployment_name": deployment_name,
        "api_version": api_version
    }

async def send_llm_request_streaming(
    messages: List[Dict], 
    functions: Optional[List[Dict]] = None, 
    max_tokens: int = 4000
) -> AsyncGenerator[Dict, None]:
    """Send streaming request to Azure OpenAI"""
    config = get_azure_config()
    url = f"{config['endpoint']}/openai/deployments/{config['deployment_name']}/chat/completions?api-version={config['api_version']}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": config['api_key']
    }
    
    payload = {
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "temperature": 0.0,
        "stream": True
    }
    
    if functions:
        payload["tools"] = functions
        payload["tool_choice"] = "auto"
    
    async with httpx.AsyncClient(timeout=60) as client:
        async with client.stream("POST", url, headers=headers, json=payload) as response:
            response.raise_for_status()
            
            content_buffer = ""
            function_call_buffer = ""
            
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data_str = line[6:]
                    
                    if data_str.strip() == "[DONE]":
                        break
                    
                    try:
                        data = json.loads(data_str)
                        
                        if "choices" in data and len(data["choices"]) > 0:
                            choice = data["choices"][0]
                            delta = choice.get("delta", {})
                            
                            # Handle content streaming
                            if "content" in delta and delta["content"]:
                                chunk = delta["content"]
                                content_buffer += chunk
                                
                                yield {
                                    "type": "content_chunk",
                                    "content": chunk,
                                    "full_content": content_buffer
                                }
                            
                            # Handle function calls
                            if "tool_calls" in delta:
                                for tool_call in delta["tool_calls"]:
                                    if "function" in tool_call:
                                        func = tool_call["function"]
                                        if "name" in func:
                                            yield {
                                                "type": "function_call",
                                                "function_name": func["name"]
                                            }
                                        if "arguments" in func:
                                            function_call_buffer += func["arguments"]
                                            
                            # Check for completion
                            if choice.get("finish_reason"):
                                yield {
                                    "type": "completion",
                                    "finish_reason": choice["finish_reason"],
                                    "full_content": content_buffer,
                                    "function_arguments": function_call_buffer
                                }
                                break
                                
                    except json.JSONDecodeError:
                        continue

async def classify_user_intent_streaming(user_input: str, conversation_context: str = "") -> AsyncGenerator[Dict, None]:
    """Stream intent classification with two-step approach: analysis then function call"""
    
    # Step 1: Get analysis without function calls
    analysis_messages = [
        {
            "role": "system", 
            "content": prompt_loader.load_prompt("intent_analysis_system")
        },
        {
            "role": "user", 
            "content": prompt_loader.load_prompt("intent_analysis_user", 
                user_input=user_input,
                conversation_context=conversation_context if conversation_context else "No previous conversation"
            )
        }
    ]
    
    # Stream the analysis
    analysis_content = ""
    buffer = ""
    
    async for chunk in send_llm_request_streaming(analysis_messages, max_tokens=300):
        if chunk["type"] == "content_chunk":
            buffer += chunk["content"]
            
            # Send in sentence chunks
            if chunk["content"].endswith(('.', '!', '?', '\n')):
                if buffer.strip():
                    yield {
                        "type": "intent_reasoning",
                        "content": buffer.strip()
                    }
                    analysis_content += buffer
                    buffer = ""
        elif chunk["type"] == "completion":
            if buffer.strip():
                yield {
                    "type": "intent_reasoning", 
                    "content": buffer.strip()
                }
                analysis_content += buffer
    
    # Step 2: Get classification via function call (no streaming)
    classification_messages = [
        {
            "role": "system",
            "content": prompt_loader.load_prompt("intent_classification_system")
        },
        {
            "role": "user",
            "content": prompt_loader.load_prompt("intent_classification_user",
                analysis_content=analysis_content,
                user_input=user_input
            )
        }
    ]
    
    functions = get_intent_classification_functions()
    function_result = None
    
    async for chunk in send_llm_request_streaming(classification_messages, functions, max_tokens=200):
        if chunk["type"] == "completion" and chunk["function_arguments"]:
            try:
                function_result = json.loads(chunk["function_arguments"])
                break
            except json.JSONDecodeError:
                pass
    
    # Send final classification
    if function_result:
        yield {
            "type": "intent_classified",
            "intent": function_result['intent'],
            "confidence": function_result['confidence_score'],
            "reasoning": function_result['reasoning'],
            "suggested_actions": function_result['suggested_actions']
        }
    else:
        # Fallback
        fallback_intent, fallback_confidence = get_fallback_intent(user_input)
        yield {
            "type": "intent_classified",
            "intent": fallback_intent,
            "confidence": fallback_confidence,
            "reasoning": f"Classified based on keywords in request",
            "suggested_actions": [f"Proceed with {fallback_intent}"]
        }

def get_fallback_intent(user_input: str) -> tuple[str, float]:
    """Simple keyword-based fallback classification"""
    input_lower = user_input.lower()
    
    if "draft" in input_lower and ("claim" in input_lower or "patent" in input_lower):
        return "claim_drafting", 0.8
    elif "review" in input_lower and "claim" in input_lower:
        return "claim_review", 0.8
    elif "prior art" in input_lower or ("search" in input_lower and ("patent" in input_lower or "prior" in input_lower)):
        return "prior_art_search", 0.9
    elif "patent" in input_lower or "invention" in input_lower:
        return "patent_guidance", 0.7
    else:
        return "general_conversation", 0.7

def is_template_claim(claim_text: str) -> bool:
    """Check if claim is a template/placeholder"""
    template_indicators = [
        "[describe", "[list", "[insert", "[specify",
        "primary function", "list key components", "describe the method"
    ]
    return any(indicator in claim_text for indicator in template_indicators)

async def assess_disclosure_sufficiency(disclosure: str) -> Dict[str, Any]:
    """Use LLM to assess if disclosure contains sufficient technical content for claim drafting"""
    
    assessment_messages = [
        {
            "role": "system",
            "content": prompt_loader.load_prompt("disclosure_assessment_system")
        },
        {
            "role": "user",
            "content": prompt_loader.load_prompt("disclosure_assessment_user",
                disclosure=disclosure
            )
        }
    ]
    
    functions = [
        {
            "type": "function",
            "function": {
                "name": "assess_technical_sufficiency",
                "description": "Assess if disclosure has sufficient technical content",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "sufficient": {"type": "boolean"},
                        "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                        "technical_elements_found": {"type": "array", "items": {"type": "string"}},
                        "message": {"type": "string"},
                        "requirements": {"type": "array", "items": {"type": "string"}}
                    },
                    "required": ["sufficient", "confidence", "technical_elements_found", "message"]
                }
            }
        }
    ]
    
    try:
        async for chunk in send_llm_request_streaming(assessment_messages, functions, max_tokens=400):
            if chunk["type"] == "completion" and chunk["function_arguments"]:
                try:
                    result = json.loads(chunk["function_arguments"])
                    logging.info(f"LLM assessment result for '{disclosure}': {result}")
                    return result
                except json.JSONDecodeError:
                    pass
        
        # If LLM assessment fails, return conservative result asking for more details
        logging.warning(f"LLM assessment failed for: '{disclosure}' - returning conservative insufficient result")
        return {
            "sufficient": False,
            "confidence": 0.5,
            "technical_elements_found": [],
            "message": "I need more specific technical details about your invention to draft meaningful patent claims. Please describe the technical aspects of your invention.",
            "requirements": [
                "What specific technical problem does your invention solve?",
                "What are the key technical components or processes?",
                "How does your invention work technically?",
                "What makes your technical approach novel or different?"
            ]
        }
            
    except Exception as e:
        logging.error(f"Error in assess_disclosure_sufficiency: {e}")
        # For errors, be conservative and ask for more details
        return {
            "sufficient": False,
            "confidence": 0.5,
            "technical_elements_found": [],
            "message": "I need more specific technical details about your invention to draft meaningful patent claims. Please describe the technical aspects of your invention.",
            "requirements": [
                "What specific technical problem does your invention solve?",
                "What are the key technical components or processes?", 
                "How does your invention work technically?",
                "What makes your technical approach novel or different?"
            ]
        }

async def draft_claims_streaming(disclosure: str, document_content: str = "", conversation_history: str = "") -> AsyncGenerator[Dict, None]:
    """Stream claims drafting with two-step approach: analysis then claims generation"""
    
    # Use LLM to assess if disclosure contains sufficient technical content for claim drafting
    assessment_result = await assess_disclosure_sufficiency(disclosure)
    if not assessment_result["sufficient"]:
        yield {
            "type": "results",
            "response": assessment_result["message"]
        }
        return
    
    context_prompt = ""
    if conversation_history or document_content:
        parts = []
        if conversation_history:
            parts.append(f"Conversation History:\n{conversation_history[:2000]}...")
        if document_content:
            parts.append(f"Document Content:\n{document_content[:2000]}...")
        context_prompt = "\n\n".join(parts)
    
    # Step 1: Get analysis without function calls
    analysis_messages = [
        {
            "role": "system",
            "content": prompt_loader.load_prompt("claims_analysis_system")
        },
        {
            "role": "user", 
            "content": prompt_loader.load_prompt("claims_analysis_user",
                disclosure=disclosure,
                context_prompt=context_prompt
            )
        }
    ]
    
    # Stream the analysis
    analysis_content = ""
    buffer = ""
    
    async for chunk in send_llm_request_streaming(analysis_messages, max_tokens=800):
        if chunk["type"] == "content_chunk":
            buffer += chunk["content"]
            
            # Send in meaningful chunks
            if chunk["content"].endswith(('.', '!', '?', '\n', ':')) and len(buffer.strip()) > 30:
                yield {
                    "type": "drafting_thoughts",
                    "content": buffer.strip()
                }
                analysis_content += buffer
                buffer = ""
        elif chunk["type"] == "completion":
            if buffer.strip():
                yield {
                    "type": "drafting_thoughts",
                    "content": buffer.strip()
                }
                analysis_content += buffer
    
    # Step 2: Generate claims via function call
    claims_messages = [
        {
            "role": "system",
            "content": prompt_loader.load_prompt("claims_generation_system")
        },
        {
            "role": "user",
            "content": prompt_loader.load_prompt("claims_generation_user",
                analysis_content=analysis_content,
                disclosure=disclosure
            )
        }
    ]
    
    functions = get_patent_claim_functions()
    function_result = None
    
    async for chunk in send_llm_request_streaming(claims_messages, functions, max_tokens=2000):
        if chunk["type"] == "completion" and chunk["function_arguments"]:
            try:
                function_result = json.loads(chunk["function_arguments"])
                break
            except json.JSONDecodeError:
                pass
    
    # Send final claims
    if function_result and "claims" in function_result:
        claims = []
        valid_claims = [c for c in function_result['claims'] if not is_template_claim(c['claim_text'])]
        
        if valid_claims:
            for i, claim in enumerate(valid_claims, 1):
                claim_text = f"{claim['claim_number']}. {claim['claim_text']}"
                claims.append(claim_text)
                
                yield {
                    "type": "claim_generated",
                    "claim_number": i,
                    "claim_text": claim_text,
                    "claim_type": claim['claim_type'],
                    "total_claims": len(valid_claims)
                }
            
            yield {
                "type": "claims_complete",
                "claims": claims,
                "num_claims": len(claims),
                "summary": function_result.get('summary', '')
            }
        else:
            yield {
                "type": "error",
                "error": "Could not generate valid claims from the provided invention description",
                "context": "claims_validation"
            }
    else:
        yield {
            "type": "error", 
            "error": "Failed to generate claims via function call",
            "context": "claims_generation"
        }

def get_intent_classification_functions():
    """Define functions for intent classification"""
    return [
        {
            "type": "function",
            "function": {
                "name": "classify_user_intent",
                "description": "Classify the user's intent",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "intent": {
                            "type": "string",
                            "enum": ["claim_drafting", "claim_review", "patent_guidance", "invention_analysis", "technical_query", "general_conversation", "prior_art_search"]
                        },
                        "confidence_score": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0
                        },
                        "reasoning": {"type": "string"},
                        "suggested_actions": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "requires_context": {"type": "boolean"}
                    },
                    "required": ["intent", "confidence_score", "reasoning", "suggested_actions", "requires_context"]
                }
            }
        }
    ]

def get_patent_claim_functions():
    """Define functions for patent claim generation"""
    return [
        {
            "type": "function",
            "function": {
                "name": "draft_patent_claims",
                "description": "Generate patent claims",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "claims": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "claim_number": {"type": "integer"},
                                    "claim_text": {"type": "string"},
                                    "claim_type": {
                                        "type": "string",
                                        "enum": ["independent", "dependent"]
                                    },
                                    "dependency": {"type": "string"}
                                },
                                "required": ["claim_number", "claim_text", "claim_type"]
                            }
                        },
                        "summary": {"type": "string"}
                    },
                    "required": ["claims", "summary"]
                }
            }
        }
    ]

async def agent_run_streaming(user_input: str, conversation_context: str = "") -> AsyncGenerator[Dict[str, Any], None]:
    """Main streaming agent with clean separation of concerns"""
    try:
        # Step 0: Early check for claim drafting requests with insufficient details
        # This prevents unnecessary intent classification for obvious insufficient requests
        input_lower = user_input.lower()
        might_be_claim_drafting = ("draft" in input_lower and ("claim" in input_lower or "patent" in input_lower))
        
        if might_be_claim_drafting:
            # Do a quick assessment to avoid running intent classification for insufficient requests
            logging.info(f"Detected potential claim drafting request: '{user_input}'")
            assessment_result = await assess_disclosure_sufficiency(user_input)
            logging.info(f"Assessment result: {assessment_result}")
            if not assessment_result["sufficient"]:
                # Skip intent classification entirely and return insufficient details immediately
                logging.info("Returning insufficient details immediately")
                yield {
                    "type": "results",
                    "response": assessment_result["message"]
                }
                return
            else:
                logging.info("Assessment passed, continuing to intent classification")
        
        # Step 1: Stream intent classification (only if we haven't already returned insufficient details)
        intent_classification = None
        async for event in classify_user_intent_streaming(user_input, conversation_context):
            yield event
            if event.get("type") == "intent_classified":
                intent_classification = IntentClassification(
                    intent=IntentType(event["intent"]),
                    confidence_score=event["confidence"],
                    reasoning=event["reasoning"],
                    suggested_actions=event["suggested_actions"],
                    requires_context=True
                )
        
        if not intent_classification:
            fallback_intent, fallback_confidence = get_fallback_intent(user_input)
            intent_classification = IntentClassification(
                intent=IntentType(fallback_intent),
                confidence_score=fallback_confidence,
                reasoning="Fallback classification",
                suggested_actions=[f"Proceed with {fallback_intent}"],
                requires_context=False
            )
        
        # Step 2: Handle low confidence
        if intent_classification.confidence_score <= 0.5:
            yield {
                "type": "low_confidence",
                "text": "I need more information to help you effectively. Could you provide more details?",
                "confidence": intent_classification.confidence_score,
                "suggestions": intent_classification.suggested_actions
            }
            return
        
        # Step 3: Execute based on intent
        if intent_classification.intent == IntentType.CLAIM_DRAFTING:
            claims = []
            
            async for event in draft_claims_streaming(user_input, "", conversation_context):
                yield event
                if event.get("type") == "claims_complete":
                    claims = event.get("claims", [])
                elif event.get("type") == "results":
                    # This could be either claims or insufficient details - just pass it through
                    return

            # Only send completion if we actually got claims
            if claims:
                response_text = f"I've drafted {len(claims)} patent claims based on your invention:\n\n" + "\n\n".join(claims)
                yield {
                    "type": "complete",
                    "response": response_text,
                    "metadata": {
                        "should_draft_claims": True,
                        "has_claims": True,
                        "reasoning": f"Executed {intent_classification.intent.value} successfully"
                    },
                    "data": {
                        "claims": claims,
                        "num_claims": len(claims)
                    }
                }
            
        elif intent_classification.intent == IntentType.PRIOR_ART_SEARCH:
            # Prior art search implementation
            search_terms = user_input.replace("prior art search results for", "").replace("search prior art", "").replace("find prior art", "").strip()
            if not search_terms:
                search_terms = user_input
            
            yield {
                "type": "search_progress",
                "content": f"🔍 Performing prior art search for: {search_terms}"
            }
            
            try:
                config = PatentSearchConfig()
                config.default_relevance_threshold = 0.2
                engine = PatentSearchEngine(config)
                
                search_result = await engine.search(search_terms, max_results=20, relevance_threshold=0.2)
                formatted_results = await engine.generate_report(search_result)
                
                yield {
                    "type": "complete",
                    "response": formatted_results,
                    "metadata": {
                        "should_draft_claims": False,
                        "has_claims": False,
                        "reasoning": "Completed prior art search"
                    }
                }
                
            except Exception as e:
                fallback_msg = f"""# Prior Art Search for '{search_terms}'

**⚠️ Enhanced Search Temporarily Unavailable**

I've identified your request for prior art search on **{search_terms}**. However, the full patent database search functionality is currently unavailable.

## Recommendations:
1. Visit [Google Patents](https://patents.google.com) and search for "{search_terms}"
2. Check USPTO, EPO, or other patent offices
3. Review technical literature in IEEE Xplore, ACM Digital Library

This requires thorough analysis before filing any patent applications."""
                
                yield {
                    "type": "complete",
                    "response": fallback_msg,
                    "metadata": {
                        "should_draft_claims": False,
                        "has_claims": False,
                        "reasoning": "Prior art search with fallback response"
                    }
                }
            
        else:
            # Handle other intents
            yield {
                "type": "complete",
                "response": "I'm here to help with your patent-related questions. What specific aspect would you like to explore?",
                "metadata": {
                    "should_draft_claims": False,
                    "has_claims": False,
                    "reasoning": f"Handled {intent_classification.intent.value}"
                }
            }
        
    except Exception as e:
        logging.error(f"Error in agent_run_streaming: {e}")
        yield {
            "type": "error",
            "error": str(e),
            "text": f"I encountered an error: {str(e)}. Please try again."
        }

class IntelligentAgent:
    """Intelligent patent agent with streaming capabilities"""
    
    async def run_streaming(self, user_input: str, conversation_context: str = ""):
        """Main streaming interface"""
        async for event in agent_run_streaming(user_input, conversation_context):
            yield event

# Export the agent
agent = IntelligentAgent()

# Setup logging
logging.basicConfig(level=logging.INFO)
