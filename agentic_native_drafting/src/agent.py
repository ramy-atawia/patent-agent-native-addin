from typing import List, Dict, Optional, Any, Union, AsyncGenerator
import os
import json
import re
import logging
import httpx
import asyncio
from dotenv import load_dotenv
from pydantic import BaseModel
from enum import Enum

from .models import AgentResponse, ReviewComment
from .prior_art_search import PatentSearchEngine, PatentSearchConfig

# Load environment variables
load_dotenv()

class ThoughtType(str, Enum):
    """Types of LLM decision thoughts"""
    ANALYZING_INPUT = "analyzing_input"
    EVALUATING_INTENT = "evaluating_intent" 
    PLANNING_APPROACH = "planning_approach"
    SELECTING_STRATEGY = "selecting_strategy"
    PROCESSING_CONTEXT = "processing_context"
    GENERATING_CONTENT = "generating_content"
    VALIDATING_OUTPUT = "validating_output"
    MAKING_DECISION = "making_decision"
    REASONING = "reasoning"

class StreamingThought(BaseModel):
    """Structure for streaming LLM thoughts"""
    type: ThoughtType
    content: str
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = {}
    timestamp: Optional[str] = None

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
    max_tokens: int = 4000,
    thought_callback: Optional[callable] = None
) -> AsyncGenerator[Dict, None]:
    """Send streaming request to Azure OpenAI with thought extraction"""
    config = get_azure_config()
    url = f"{config['endpoint']}/openai/deployments/{config['deployment_name']}/chat/completions?api-version={config['api_version']}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": config['api_key']
    }
    
    payload = {
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "temperature": 0.0,  # More deterministic, less verbose
        "stream": True  # Enable streaming
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
                    data_str = line[6:]  # Remove "data: " prefix
                    
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
                                
                                # Extract thoughts from the streaming content
                                if thought_callback:
                                    thoughts = await extract_thoughts_from_chunk(chunk, content_buffer)
                                    for thought in thoughts:
                                        await thought_callback(thought)
                                
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

async def extract_thoughts_from_chunk(chunk: str, full_content: str) -> List[StreamingThought]:
    """Extract LLM decision thoughts from streaming content"""
    thoughts = []
    
    # Look for decision markers in the content
    decision_patterns = [
        (r"I need to|I should|Let me", ThoughtType.ANALYZING_INPUT),
        (r"This appears to be|This seems like|I can see", ThoughtType.EVALUATING_INTENT),
        (r"My approach will be|I'll start by|The best strategy", ThoughtType.PLANNING_APPROACH),
        (r"I'm choosing|I'll select|The optimal choice", ThoughtType.SELECTING_STRATEGY),
        (r"Based on the context|Considering the history|Given the information", ThoughtType.PROCESSING_CONTEXT),
        (r"I'm generating|Creating|Drafting", ThoughtType.GENERATING_CONTENT),
        (r"Let me verify|I need to check|Validating", ThoughtType.VALIDATING_OUTPUT),
        (r"Therefore|Because|Since|As a result", ThoughtType.REASONING),
        (r"I've decided|My decision is|I conclude", ThoughtType.MAKING_DECISION)
    ]
    
    for pattern, thought_type in decision_patterns:
        if re.search(pattern, chunk, re.IGNORECASE):
            thoughts.append(StreamingThought(
                type=thought_type,
                content=chunk.strip(),
                metadata={"pattern_matched": pattern}
            ))
            break
    
    return thoughts

async def classify_user_intent_streaming(user_input: str, conversation_context: str = "") -> AsyncGenerator[Dict, None]:
    """Stream the intent classification process with thoughts"""
    
    prompt = f"""
    You are an expert patent attorney AI assistant. Analyze the user input and immediately classify their intent using the classify_user_intent function.

    User Input: {user_input}
    
    Session History:
    {conversation_context if conversation_context else "No previous conversation in this session"}

    Available intent types:
    1. claim_drafting - User wants patent claims drafted
    2. claim_review - User wants existing claims reviewed  
    3. patent_guidance - User needs general patent advice
    4. invention_analysis - User wants invention analyzed
    5. prior_art_search - User wants prior art search
    6. technical_query - User has technical questions
    7. general_conversation - General chat or greetings

    Analyze the input quickly and call the classify_user_intent function immediately with your classification.
    """

    messages = [
        {"role": "system", "content": "You are an expert patent attorney AI assistant. Analyze user input quickly and call the classify_user_intent function immediately. Avoid lengthy explanations."},
        {"role": "user", "content": prompt}
    ]
    
    functions = get_intent_classification_functions()
    
    try:
        final_content = ""
        function_result = None
        reasoning_chunk_count = 0
        max_reasoning_chunks = 50  # Limit verbose reasoning
        
        async for chunk in send_llm_request_streaming(messages, functions, thought_callback=None):
            if chunk["type"] == "content_chunk":
                # Limit the number of reasoning chunks to prevent infinite streaming
                reasoning_chunk_count += 1
                if reasoning_chunk_count <= max_reasoning_chunks:
                    # Stream the LLM's reasoning
                    yield {
                        "type": "reasoning_chunk",
                        "content": chunk["content"]
                    }
                else:
                    # Skip further reasoning chunks
                    continue
            elif chunk["type"] == "function_call":
                # COMMENTED OUT: Technical function call notifications (not needed for users)
                # yield {
                #     "type": "thought",
                #     "thought_type": ThoughtType.MAKING_DECISION.value,
                #     "content": f"Calling function: {chunk['function_name']}"
                # }
                pass
            elif chunk["type"] == "completion":
                final_content = chunk["full_content"]
                if chunk["function_arguments"]:
                    function_result = json.loads(chunk["function_arguments"])
        
        if function_result:
            intent_classification = IntentClassification(
                intent=IntentType(function_result['intent']),
                confidence_score=float(function_result['confidence_score']),
                reasoning=function_result['reasoning'],
                suggested_actions=function_result['suggested_actions'],
                requires_context=bool(function_result['requires_context'])
            )
            
            yield {
                "type": "intent_classified",
                "intent": intent_classification.intent.value,
                "confidence": intent_classification.confidence_score,
                "reasoning": intent_classification.reasoning,
                "suggested_actions": intent_classification.suggested_actions
            }
        else:
            # Fallback: If LLM doesn't call function, classify based on keywords
            print(f"⚠️ LLM didn't call function, using fallback classification for: {user_input}")
            
            fallback_intent = "general_conversation"
            fallback_confidence = 0.7
            
            # Simple keyword-based classification
            input_lower = user_input.lower()
            if "draft" in input_lower and ("claim" in input_lower or "patent" in input_lower):
                fallback_intent = "claim_drafting"
                fallback_confidence = 0.8
            elif "review" in input_lower and "claim" in input_lower:
                fallback_intent = "claim_review"
                fallback_confidence = 0.8
            elif "prior art" in input_lower or ("search" in input_lower and ("patent" in input_lower or "prior" in input_lower)):
                fallback_intent = "prior_art_search"
                fallback_confidence = 0.9  # High confidence for explicit prior art searches
            elif "patent" in input_lower or "invention" in input_lower:
                fallback_intent = "patent_guidance"
                fallback_confidence = 0.7
            else:
                fallback_confidence = 0.7
            
            yield {
                "type": "intent_classified",
                "intent": fallback_intent,
                "confidence": fallback_confidence,
                "reasoning": f"Fallback classification based on keywords in: '{user_input[:50]}...'",
                "suggested_actions": [f"Proceed with {fallback_intent} workflow"]
            }
            
    except Exception as e:
        yield {
            "type": "error",
            "error": str(e),
            "context": "intent_classification"
        }

async def draft_claims_streaming(disclosure: str, document_content: str = "", conversation_history: str = "") -> AsyncGenerator[Dict, None]:
    """Stream the claims drafting process with detailed thoughts"""
    
    context_prompt = ""
    if conversation_history or document_content:
        parts = []
        if conversation_history:
            parts.append(f"Conversation History:\n{conversation_history[:2000]}...")
        if document_content:
            parts.append(f"Document Content:\n{document_content[:2000]}...")
        context_prompt = "\n\n".join(parts)
    
    messages = [
        {
            "role": "system",
            "content": "You are a patent attorney expert. Think step by step through the claim drafting process, explaining your reasoning and decisions. Use the draft_patent_claims function to return structured claim data."
        },
        {
            "role": "user",
            "content": f"""Draft patent claims based on this invention disclosure. Think through your approach step by step.

User Query: {disclosure}
{context_prompt}

Requirements:
1. First claim should be an independent claim (method or system)
2. Subsequent claims should be dependent claims adding specific features
3. Follow USPTO formatting and requirements
4. Use clear, precise language
5. Ensure claims are patentable subject matter under 35 USC 101

First explain your analysis and approach, then use the draft_patent_claims function."""
        }
    ]
    
    functions = get_patent_claim_functions()
    
    try:
        claims = []
        function_result = None
        
        async for chunk in send_llm_request_streaming(messages, functions, thought_callback=None):
            if chunk["type"] == "content_chunk":
                yield {
                    "type": "analysis_chunk",
                    "content": chunk["content"]
                }
            elif chunk["type"] == "function_call":
                # COMMENTED OUT: Technical function call notifications (not needed for users)
                # yield {
                #     "type": "thought",
                #     "thought_type": ThoughtType.GENERATING_CONTENT.value,
                #     "content": "Generating structured claim data..."
                # }
                pass
            elif chunk["type"] == "completion":
                if chunk["function_arguments"]:
                    function_result = json.loads(chunk["function_arguments"])
        
        if function_result and "claims" in function_result:
            for i, claim in enumerate(function_result['claims'], 1):
                claim_text = f"{claim['claim_number']}. {claim['claim_text']}"
                claims.append(claim_text)
                
                # COMMENTED OUT: Excessive per-claim notifications (too verbose)
                # yield {
                #     "type": "thought",
                #     "thought_type": ThoughtType.VALIDATING_OUTPUT.value,
                #     "content": f"Generated claim {i}: {claim['claim_type']} claim"
                # }
                
                await asyncio.sleep(0.2)
                
                yield {
                    "type": "claim_generated",
                    "claim_number": i,
                    "claim_text": claim_text,
                    "claim_type": claim['claim_type'],
                    "total_claims": len(function_result['claims'])
                }
        
        yield {
            "type": "thought",
            "thought_type": ThoughtType.MAKING_DECISION.value,
            "content": f"Successfully completed claims drafting: {len(claims)} claims generated"
        }
        
        yield {
            "type": "claims_complete",
            "claims": claims,
            "num_claims": len(claims),
            "summary": function_result.get('summary', '') if function_result else ''
        }
        
    except Exception as e:
        yield {
            "type": "error",
            "error": str(e),
            "context": "claims_drafting"
        }

def get_intent_classification_functions():
    """Define functions for intent classification"""
    return [
        {
            "type": "function",
            "function": {
                "name": "classify_user_intent",
                "description": "Classify the user's intent and determine the best course of action",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "intent": {
                            "type": "string",
                            "enum": ["claim_drafting", "claim_review", "patent_guidance", "invention_analysis", "technical_query", "general_conversation", "prior_art_search"],
                            "description": "The primary intent of the user's request"
                        },
                        "confidence_score": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "description": "Confidence in the intent classification (0.0 to 1.0)"
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Explanation of why this intent was chosen"
                        },
                        "suggested_actions": {
                            "type": "array",
                            "items": {"type": "string"},
                            "description": "List of suggested actions to take"
                        },
                        "requires_context": {
                            "type": "boolean",
                            "description": "Whether this request requires conversation context"
                        }
                    },
                    "required": ["intent", "confidence_score", "reasoning", "suggested_actions", "requires_context"]
                }
            }
        }
    ]

def get_patent_claim_functions():
    """Define functions for structured patent claim output"""
    return [
        {
            "type": "function",
            "function": {
                "name": "draft_patent_claims",
                "description": "Draft patent claims with structured output",
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

async def agent_run_streaming_with_thoughts(user_input: str, conversation_context: str = "") -> AsyncGenerator[Dict[str, Any], None]:
    """Enhanced streaming version with detailed LLM decision thoughts"""
    try:
        # Step 1: Intent classification with thoughts
        intent_classification = None
        async for event in classify_user_intent_streaming(user_input, conversation_context):
            yield event
            if event.get("type") == "intent_classified":
                intent_classification = IntentClassification(
                    intent=IntentType(event["intent"]),
                    confidence_score=event["confidence"],
                    reasoning=event["reasoning"],
                    suggested_actions=event["suggested_actions"],
                    requires_context=True  # Default assumption
                )
        
        if not intent_classification:
            # Fallback intent classification if nothing was received
            print("⚠️ No intent classification received, using fallback")
            fallback_intent_type = "general_conversation"
            
            # Simple keyword-based fallback
            input_lower = user_input.lower()
            fallback_intent_type = "general_conversation"
            fallback_confidence = 0.6
            
            if "draft" in input_lower and ("claim" in input_lower or "patent" in input_lower):
                fallback_intent_type = "claim_drafting"
                fallback_confidence = 0.8
            elif "review" in input_lower and "claim" in input_lower:
                fallback_intent_type = "claim_review"
                fallback_confidence = 0.8
            elif "prior art" in input_lower or "search" in input_lower:
                fallback_intent_type = "prior_art_search"
                fallback_confidence = 0.8  # Higher confidence for prior art searches
            elif "patent" in input_lower or "invention" in input_lower:
                fallback_intent_type = "patent_guidance"
                fallback_confidence = 0.7
            
            intent_classification = IntentClassification(
                intent=IntentType(fallback_intent_type),
                confidence_score=fallback_confidence,
                reasoning=f"Fallback classification for: {user_input[:50]}...",
                suggested_actions=[f"Proceed with {fallback_intent_type}"],
                requires_context=False
            )
            
            yield {
                "type": "intent_classified",
                "intent": intent_classification.intent.value,
                "confidence": intent_classification.confidence_score,
                "reasoning": intent_classification.reasoning,
                "suggested_actions": intent_classification.suggested_actions
            }
        
        # Step 2: Confidence threshold check - only for very low confidence
        if intent_classification.confidence_score <= 0.5:
            yield {
                "type": "low_confidence",
                "text": "I need more information to help you effectively. Could you provide more details?",
                "confidence": intent_classification.confidence_score,
                "suggestions": intent_classification.suggested_actions
            }
            return
        
        # Step 3: Execute high-confidence intents with detailed thoughts
        if intent_classification.intent == IntentType.CLAIM_DRAFTING:
            # Stream claims drafting with thoughts
            claims = []
            async for event in draft_claims_streaming(user_input, "", conversation_context):
                yield event
                if event.get("type") == "claims_complete":
                    claims = event.get("claims", [])

            response_text = f"I've drafted {len(claims)} patent claims based on your invention:\n\n" + "\n\n".join(claims)
            yield {
                "type": "complete",
                "response": response_text,
                "metadata": {
                    "should_draft_claims": True,
                    "has_claims": True,
                    "reasoning": f"Executed {intent_classification.intent.value} with {intent_classification.confidence_score:.0%} confidence"
                },
                "data": {
                    "claims": claims,
                    "num_claims": len(claims)
                }
            }
            
        elif intent_classification.intent == IntentType.PRIOR_ART_SEARCH:
            # Real prior art search using the optimized module
            search_terms = user_input.replace("prior art search results for", "").replace("search prior art", "").replace("find prior art", "").strip()
            if not search_terms:
                search_terms = user_input
            
            yield {
                "type": "thinking",
                "content": f"🔍 Performing prior art search for: {search_terms}",
                "metadata": {"search_terms": search_terms}
            }
            
            try:
                yield {
                    "type": "thinking", 
                    "content": "📡 Connecting to patent databases...",
                    "metadata": {}
                }
                
                # Perform the actual search using clean architecture
                config = PatentSearchConfig()
                # Lower relevance threshold for better frontend results
                config.default_relevance_threshold = 0.2
                engine = PatentSearchEngine(config)
                
                search_result = await engine.search(search_terms, max_results=20, relevance_threshold=0.2)
                
                yield {
                    "type": "thinking",
                    "content": f"📊 Found {search_result.total_found} relevant patents",
                    "metadata": {"patents_found": search_result.total_found}
                }
                
                # Format the results using enhanced LLM report generation
                yield {
                    "type": "thinking",
                    "content": "🧠 Generating comprehensive patent attorney report...",
                    "metadata": {}
                }
                
                # Generate comprehensive report using clean architecture
                formatted_results = await engine.generate_report(search_result)
                
                yield {
                    "type": "complete",
                    "response": formatted_results,
                    "metadata": {
                        "should_draft_claims": False,
                        "has_claims": False,
                        "reasoning": f"Completed prior art search with {intent_classification.confidence_score:.0%} confidence"
                    },
                    "data": {
                        "prior_art_result": {
                            "search_terms": search_terms,
                            "patents_found": search_result.total_found,
                            "patents": [
                                {
                                    "patent_id": p.patent_id,
                                    "title": p.title,
                                    "relevance_score": p.relevance_score
                                } for p in search_result.patents[:20]
                            ]
                        }
                    }
                }
                
            except ImportError as e:
                # Fallback if prior art search module isn't available
                formatted_results = f"""# Prior Art Search for '{search_terms}'

**⚠️ Enhanced Search Temporarily Unavailable**

I've identified your request for prior art search on **{search_terms}**. However, the full patent database search functionality is currently unavailable.

## What you can do:
1. **Manual Search**: Visit [Google Patents](https://patents.google.com) and search for "{search_terms}"
2. **Patent Databases**: Check USPTO, EPO, or other patent offices
3. **Technical Literature**: Review IEEE Xplore, ACM Digital Library for related work

## Search Terms Identified:
- **{search_terms}**

This appears to be in the **telecommunications/AI** domain, which typically has extensive prior art. I recommend conducting a thorough search before filing any patent applications.
"""
                
                yield {
                    "type": "complete",
                    "response": formatted_results,
                    "metadata": {
                        "should_draft_claims": False,
                        "has_claims": False,
                        "reasoning": f"Prior art search intent identified with {intent_classification.confidence_score:.0%} confidence, but enhanced search unavailable"
                    },
                    "data": {
                        "prior_art_result": {
                            "search_terms": search_terms,
                            "status": "fallback_response",
                            "message": "Enhanced search temporarily unavailable"
                        }
                    }
                }
                
            except Exception as e:
                error_msg = f"Prior art search failed: {str(e)}"
                logging.error(error_msg)
                yield {
                    "type": "error",
                    "error": error_msg,
                    "text": f"I encountered an error while searching for prior art: {str(e)}. Please try again or contact support."
                }
            
        else:
            # Handle other intents (general conversation)
            # Simulate response generation
            await asyncio.sleep(0.3)
            response_text = "I'm here to help with your patent-related questions. What specific aspect would you like to explore?"
            
            yield {
                "type": "complete",
                "response": response_text,
                "metadata": {
                    "should_draft_claims": False,
                    "has_claims": False,
                    "reasoning": f"Executed {intent_classification.intent.value} with {intent_classification.confidence_score:.0%} confidence"
                }
            }
        
    except Exception as e:
        logging.error(f"Error in agent_run_streaming_with_thoughts: {e}")
        yield {
            "type": "error",
            "error": str(e),
            "text": f"I encountered an error: {str(e)}. Please try again."
        }

# Enhanced Agent class
class IntelligentAgentWithThoughts:
    """Enhanced intelligent agent with detailed LLM decision thought streaming"""
    
    async def run_streaming(self, user_input: str, conversation_context: str = ""):
        """Streaming version with detailed LLM thoughts"""
        async for event in agent_run_streaming_with_thoughts(user_input, conversation_context):
            yield event

# Export the enhanced agent
agent_with_thoughts = IntelligentAgentWithThoughts()

# Setup logging
logging.basicConfig(level=logging.INFO)