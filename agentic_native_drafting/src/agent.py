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

class FunctionCall(BaseModel):
    """Represents a function call from the LLM"""
    name: str
    arguments: Dict[str, Any]
    reasoning: str

class IntentClassification(BaseModel):
    """Result of intent classification"""
    intent: IntentType
    confidence_score: float
    reasoning: str
    suggested_actions: List[str]
    requires_context: bool

def get_azure_config():
    """Get Azure OpenAI configuration"""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
    
    if not endpoint or not api_key or not deployment_name:
        raise RuntimeError(f"Missing Azure OpenAI config: endpoint={endpoint}, deployment={deployment_name}, api_key={'set' if api_key else 'missing'}")
    
    return {
        "endpoint": endpoint.rstrip("/"),
        "api_key": api_key,
        "deployment_name": deployment_name,
        "api_version": api_version
    }

def send_llm_request_with_functions(messages: List[Dict], functions: Optional[List[Dict]] = None, max_tokens: int = 4000) -> Dict:
    """Send request to Azure OpenAI with function calling support"""
    config = get_azure_config()
    url = f"{config['endpoint']}/openai/deployments/{config['deployment_name']}/chat/completions?api-version={config['api_version']}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": config['api_key']
    }
    
    payload = {
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "temperature": 0.1
    }
    
    if functions:
        payload["tools"] = functions
        payload["tool_choice"] = "auto"
    
    with httpx.Client(timeout=60) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()

def send_llm_request(messages: List[Dict], max_tokens: int = 4000) -> str:
    """Send simple request to Azure OpenAI"""
    config = get_azure_config()
    url = f"{config['endpoint']}/openai/deployments/{config['deployment_name']}/chat/completions?api-version={config['api_version']}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": config['api_key']
    }
    
    payload = {
        "messages": messages,
        "max_completion_tokens": max_tokens,
        "temperature": 0.1
    }
    
    with httpx.Client(timeout=60) as client:
        response = client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']

async def classify_user_intent(user_input: str, conversation_context: str = "") -> IntentClassification:
    """Use LLM to classify user intent with confidence scores"""
    try:
        # Log context usage for debugging
        if conversation_context:
            logging.info(f"Using conversation context ({len(conversation_context)} chars) for intent classification")
        else:
            logging.info("No conversation context available for intent classification")
            
        prompt = f"""
        You are an expert patent attorney AI assistant. Analyze this user input and classify their intent.

        User Input: {user_input}
        
        Session History:
        {conversation_context if conversation_context else "No previous conversation in this session"}

        Available intent types:
        1. claim_drafting - User wants patent claims drafted (e.g., "draft claims", "create a claim", "write patent claims")
        2. claim_review - User wants existing claims reviewed (e.g., "review my claims", "check this claim", "validate claims", "review those claims")
        3. patent_guidance - User needs general patent advice (e.g., "how to patent", "patent process", "patent strategy")
        4. invention_analysis - User wants invention analyzed (e.g., "analyze my invention", "is this patentable", "evaluate invention")
        5. technical_query - User has technical questions (e.g., "how does this work", "technical details", "implementation")
        6. general_conversation - General chat or greetings (e.g., "hi", "hello", "thanks")

        IMPORTANT CONFIDENCE GUIDELINES:
        - For CLEAR, SPECIFIC requests: Use confidence 0.8-1.0
        - For MODERATELY CLEAR requests: Use confidence 0.7-0.8
        - For VAGUE or AMBIGUOUS requests: Use confidence 0.3-0.6
        - For INCOMPLETE thoughts (ending with "...", "maybe", "I don't know"): Use confidence 0.2-0.5
        - For UNCLEAR requests that need clarification: Use confidence 0.1-0.6

        REDUCE CONFIDENCE for:
        - Incomplete sentences ending with "..."
        - Vague language like "maybe", "something about", "I don't know"
        - Ambiguous requests that could mean multiple things
        - Requests that need more context or details

        Consider:
        - Explicit keywords in the user's request
        - Technical complexity of the input
        - Whether they're asking for specific actions
        - Context from previous conversation in this session
        - Professional patent terminology
        - References to previous claims or responses (e.g., "review those claims", "check my claims")
        - AMBIGUITY and CLARITY of the request

        Use the classify_user_intent function to provide your analysis.
        """

        messages = [
            {"role": "system", "content": "You are an expert patent attorney AI assistant. PRIORITIZE the user's latest explicit instruction (user_input) over conversation history. If the user_input contains action verbs like 'draft', 'write', 'generate', 'create', or 'system claims', return intent 'claim_drafting'. Always output JSON with fields: intent, confidence_score, reasoning, trigger_text, suggested_actions, requires_context."},
            {"role": "user", "content": prompt}
        ]
        
        functions = get_intent_classification_functions()
        response = send_llm_request_with_functions(messages, functions)
        
        if response['choices'][0]['message'].get('tool_calls'):
            tool_call = response['choices'][0]['message']['tool_calls'][0]
            if tool_call['function']['name'] == 'classify_user_intent':
                intent_data = json.loads(tool_call['function']['arguments'])
                
                return IntentClassification(
                    intent=IntentType(intent_data['intent']),
                    confidence_score=float(intent_data['confidence_score']),
                    reasoning=intent_data['reasoning'],
                    suggested_actions=intent_data['suggested_actions'],
                    requires_context=bool(intent_data['requires_context'])
                )
        
        # If no function call, raise error - no fallback
        raise RuntimeError("LLM did not return a function call for intent classification")
        
    except Exception as e:
        logging.error(f"Error in intent classification: {e}")
        # No fallback - re-raise the error
        raise

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
                                    "claim_text": {"type": "string", "description": "Complete claim text including all elements"},
                                    "claim_type": {
                                        "type": "string",
                                        "enum": ["independent", "dependent"]
                                    },
                                    "dependency": {
                                        "type": "string",
                                        "description": "For dependent claims, specify what they depend on (e.g., 'claim 1')"
                                    }
                                },
                                "required": ["claim_number", "claim_text", "claim_type"]
                            }
                        },
                        "summary": {
                            "type": "string",
                            "description": "Brief summary of the drafted claims"
                        }
                    },
                    "required": ["claims", "summary"]
                }
            }
        }
    ]

# NOTE: We let the drafting function decide how many claims to produce based on the disclosure and session context.
def draft_claims(disclosure: str, document_content: str = "", conversation_history: str = "") -> List[str]:
    """Draft patent claims using structured LLM output.

    Inputs:
      - disclosure: the user's latest message / invention disclosure
      - document_content: full text of the current Word document (if provided)
      - conversation_history: prior chat messages or session context

    The model should decide the appropriate number of claims (recommended 3-7) based on the
    complexity of the disclosure and context. Return a list of complete claim texts.
    """
    try:
        # Build context-aware prompt
        context_prompt = ""
        if conversation_history or document_content:
            parts = []
            if conversation_history:
                logging.info(f"Using conversation_history ({len(conversation_history)} chars) for claims drafting")
                parts.append(f"Conversation History:\n{conversation_history}")
            if document_content:
                logging.info(f"Using document_content ({len(document_content)} chars) for claims drafting")
                parts.append(f"Document Content:\n{document_content}")
            context_prompt = "\n\n".join(parts)
        else:
            logging.info("No session history or document content available for claims drafting")
        
        messages = [
            {
                "role": "system",
                "content": """You are a patent attorney expert in drafting USPTO-compliant patent claims. 

IMPORTANT: Use the draft_patent_claims function to return structured claim data. Each claim must be complete and self-contained."""
            },
            {
                "role": "user",
                "content": f"""Draft an appropriate set of patent claims based on the user's query and the provided context. Choose a reasonable number of claims (typically 3-7) based on the scope and complexity; provide one independent claim followed by dependent claims as appropriate.

User Query:
{disclosure}

Document Content (from the open document, if any):
{document_content if document_content else 'None'}

Conversation History (if any):
{conversation_history if conversation_history else 'None'}

Requirements:
1. First claim should be an independent claim (method or system).
2. Subsequent claims should be dependent claims adding specific features.
3. Follow USPTO formatting and requirements.
4. Use clear, precise language.
5. Ensure claims are patentable subject matter under 35 USC 101.
6. Maintain consistency with session context if available.

Use the draft_patent_claims function to return structured claim data, and include a short explanation of why you selected the number of claims."""
            }
        ]
        
        # Use function calling for structured output
        functions = get_patent_claim_functions()
        response = send_llm_request_with_functions(messages, functions)
        
        logging.info(f"Function calling response received")
        
        if response['choices'][0]['message'].get('tool_calls'):
            tool_call = response['choices'][0]['message']['tool_calls'][0]
            logging.info(f"Tool call: {tool_call['function']['name']}")
            
            if tool_call['function']['name'] == 'draft_patent_claims':
                try:
                    claim_data = json.loads(tool_call['function']['arguments'])
                    logging.info(f"Parsed claim data: {claim_data}")
                    
                    # Extract claims from structured data
                    claims = []
                    for claim in claim_data['claims']:
                        claim_text = f"{claim['claim_number']}. {claim['claim_text']}"
                        claims.append(claim_text)
                        logging.info(f"Generated claim {claim['claim_number']}: {claim['claim_text'][:100]}...")
                    
                    return claims if claims else [f"Error: Could not generate valid patent claims. Please try again with more detailed invention description."]
                    
                except Exception as e:
                    logging.error(f"Error parsing function call data: {e}")
                    # Fall through to fallback
        
        # Fallback: simple text response if function calling fails
        logging.warning("Function calling failed, using fallback text parsing")
        content = send_llm_request(messages)
        
        # Simple fallback - just split by numbered lines
        lines = content.split('\n')
        claims = []
        current_claim = ""
        
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.', line):
                if current_claim:
                    claims.append(current_claim.strip())
                current_claim = line
            elif line and current_claim:
                current_claim += " " + line
        
        if current_claim:
            claims.append(current_claim.strip())
        
        return claims if claims else [f"Error: Could not generate valid patent claims. Please try again with more detailed invention description."]
        
    except Exception as e:
        logging.error(f"Error drafting claims: {e}")
        return [f"Error drafting claims: {str(e)}"]

def get_claim_review_functions():
    """Define functions for structured claim review output"""
    return [
        {
            "type": "function",
            "function": {
                "name": "review_patent_claims",
                "description": "Review patent claims and provide structured feedback",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "review_comments": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "comment_id": {"type": "integer"},
                                    "claim_reference": {"type": "string", "description": "Which claim this comment refers to"},
                                    "issue_category": {
                                        "type": "string",
                                        "enum": ["uspto_compliance", "claim_structure", "clarity_precision", "technical_accuracy", "patent_strategy"]
                                    },
                                    "problem_description": {"type": "string"},
                                    "severity": {
                                        "type": "string",
                                        "enum": ["minor", "major", "critical"]
                                    },
                                    "suggested_improvement": {"type": "string"}
                                },
                                "required": ["comment_id", "claim_reference", "issue_category", "problem_description", "severity", "suggested_improvement"]
                            }
                        },
                        "overall_assessment": {
                            "type": "string",
                            "description": "Overall assessment of the claims"
                        }
                    },
                    "required": ["review_comments", "overall_assessment"]
                }
            }
        }
    ]

def review_claims(claims_text: str, session_history: str = "") -> List[ReviewComment]:
    """Review patent claims using structured LLM output"""
    try:
        # Build context-aware prompt
        context_prompt = ""
        if session_history:
            logging.info(f"Using session history ({len(session_history)} chars) for claims review")
            context_prompt = f"""

Session Context:
{session_history}

Use this context to understand what was previously discussed and provide more relevant feedback."""
        else:
            logging.info("No session history available for claims review")
        
        messages = [
            {
                "role": "system",
                "content": "You are a senior patent attorney expert in USPTO compliance and patent claim quality. Use the review_patent_claims function to return structured review data."
            },
            {
                "role": "user", 
                "content": f"""Review these patent claims for quality, compliance, and potential improvements:

{claims_text}{context_prompt}

Review each claim for:
1. **USPTO Compliance**: 35 USC 101 (patentable subject matter), 102 (novelty), 103 (obviousness)
2. **Claim Structure**: Independent vs dependent, proper dependencies
3. **Clarity & Precision**: Clear language, definite boundaries, proper terminology
4. **Technical Accuracy**: Logical flow, complete elements, proper scope
5. **Patent Strategy**: Claim breadth, coverage, potential issues

Use the review_patent_claims function to return structured review data with specific issues and improvements."""
            }
        ]
        
        # Use function calling for structured output
        functions = get_claim_review_functions()
        response = send_llm_request_with_functions(messages, functions)
        
        logging.info(f"Function calling response received for review")
        
        if response['choices'][0]['message'].get('tool_calls'):
            tool_call = response['choices'][0]['message']['tool_calls'][0]
            logging.info(f"Tool call: {tool_call['function']['name']}")
            
            if tool_call['function']['name'] == 'review_patent_claims':
                try:
                    review_data = json.loads(tool_call['function']['arguments'])
                    logging.info(f"Parsed review data: {review_data}")
                    
                    # Convert structured data to ReviewComment objects
                    review_comments = []
                    for comment in review_data['review_comments']:
                        comment_text = f"{comment['claim_reference']}: {comment['problem_description']} - {comment['suggested_improvement']}"
                        review_comments.append(ReviewComment(
                            comment=comment_text,
                            severity=comment['severity']
                        ))
                    
                    return review_comments if review_comments else [
                        ReviewComment(
                            comment="No specific issues found. Claims appear to be well-drafted and compliant.",
                            severity="minor"
                        )
                    ]
                    
                except Exception as e:
                    logging.error(f"Error parsing function call data: {e}")
                    # Fall through to fallback
        
        # Fallback: simple text response if function calling fails
        logging.warning("Function calling failed for review, using fallback text parsing")
        content = send_llm_request(messages)
        
        # Simple fallback parsing
        review_comments = []
        lines = content.split('\n')
        current_comment = ""
        current_severity = "minor"
        
        for line in lines:
            line = line.strip()
            if re.match(r'^\d+\.', line):
                if current_comment:
                    review_comments.append(ReviewComment(
                        comment=current_comment.strip(),
                        severity=current_severity
                    ))
                current_comment = line
                current_severity = "minor"
            elif line.lower().startswith(('severity:', 'level:', 'priority:')):
                if 'critical' in line.lower():
                    current_severity = "critical"
                elif 'major' in line.lower():
                    current_severity = "major"
                else:
                    current_severity = "minor"
                current_comment += " " + line
            elif line:
                current_comment += " " + line
        
        if current_comment:
            review_comments.append(ReviewComment(
                comment=current_comment.strip(),
                severity=current_severity
            ))
        
        return review_comments if review_comments else [
            ReviewComment(
                comment="No specific issues found. Claims appear to be well-drafted and compliant.",
                severity="minor"
            )
        ]
        
    except Exception as e:
        logging.error(f"Error reviewing claims: {e}")
        return [ReviewComment(
            comment=f"Error reviewing claims: {str(e)}. Please try again.",
            severity="critical"
        )]

def general_conversation(query: str) -> str:
    """Handle general conversation and guidance"""
    try:
        messages = [
            {
                "role": "system",
                "content": "You are a helpful patent attorney AI assistant. Provide clear, actionable guidance on patent-related topics."
            },
            {
                "role": "user",
                "content": query
            }
        ]
        
        response = send_llm_request(messages)
        return response
        
    except Exception as e:
        logging.error(f"Error in general_conversation: {e}")
        return "I'm here to help with patent drafting! What would you like to work on?"

async def agent_run(user_input: str, conversation_context: str = "") -> AgentResponse:
    """Main agent logic with simple confidence threshold: execute (>0.7) or seek clarification (≤0.7)"""
    try:
        # Step 1: Classify user intent using LLM
        intent_classification = await classify_user_intent(user_input, conversation_context)
        
        logging.info(f"Intent classified as: {intent_classification.intent} (confidence: {intent_classification.confidence_score})")
        logging.info(f"Reasoning: {intent_classification.reasoning}")
        
        # Step 2: Simple confidence threshold decision
        if intent_classification.confidence_score <= 0.7:
            # Confidence too low - seek clarification
            return AgentResponse(
                conversation_response="I'm not entirely sure what you're asking for. Could you provide more details about what you need?",
                reasoning=f"Low confidence ({intent_classification.confidence_score}) - seeking user clarification",
                should_draft_claims=False
            )
        
        # Confidence > 0.7 - execute the detected intent
        if intent_classification.intent == IntentType.CLAIM_DRAFTING:
            # Draft patent claims with session history. The drafting routine decides how many claims are appropriate.
            claims = draft_claims(user_input, conversation_context)
            
            # Try to extract structured data if available
            structured_claims = None
            drafting_result = None
            
            # Check if we have structured claim data from function calling
            try:
                # This would be populated if function calling succeeded
                # For now, we'll create a basic structure
                structured_claims = []
                for i, claim_text in enumerate(claims, 1):
                    if "Error:" in claim_text:
                        continue
                    claim_type = "independent" if i == 1 else "dependent"
                    dependency = f"claim {i-1}" if i > 1 else None
                    structured_claims.append({
                        "claim_number": i,
                        "claim_text": claim_text,
                        "claim_type": claim_type,
                        "dependency": dependency
                    })
            except Exception as e:
                logging.warning(f"Could not create structured claims: {e}")
            
            return AgentResponse(
                conversation_response=f"I've drafted {len(claims)} patent claims based on your invention:\n\n" + "\n\n".join(claims),
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). {intent_classification.reasoning}",
                should_draft_claims=True,
                claims=claims,
                structured_claims=structured_claims
            )
            
        elif intent_classification.intent == IntentType.CLAIM_REVIEW:
            # Handle claim review - extract claims from user input and review them
            # The user input should contain the claims to review
            review_comments = review_claims(user_input, conversation_context)
            
            # Try to extract structured review data if available
            review_result = None
            try:
                # This would be populated if function calling succeeded
                # For now, we'll create a basic structure
                review_result = {
                    "review_comments": review_comments,
                    "overall_assessment": f"Found {len(review_comments)} issues to address",
                    "claims_reviewed": [user_input]  # Store what was reviewed
                }
            except Exception as e:
                logging.warning(f"Could not create structured review result: {e}")
            
            # Format the response
            if review_comments:
                response_text = f"I've reviewed your patent claims and found {len(review_comments)} issue(s):\n\n"
                for i, comment in enumerate(review_comments, 1):
                    severity_emoji = {"critical": "🔴", "major": "🟡", "minor": "🟢"}
                    response_text += f"{severity_emoji.get(comment.severity, '⚪')} **{comment.severity.upper()}**: {comment.comment}\n\n"
            else:
                response_text = "I've reviewed your patent claims and found no specific issues. They appear to be well-drafted and compliant."
            
            return AgentResponse(
                conversation_response=response_text,
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). {intent_classification.reasoning}",
                should_draft_claims=False,
                review_comments=review_comments,
                review_result=review_result
            )
            
        elif intent_classification.intent == IntentType.PATENT_GUIDANCE:
            # Provide patent guidance
            response_text = general_conversation(user_input)
            return AgentResponse(
                conversation_response=response_text,
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). {intent_classification.reasoning}",
                should_draft_claims=False
            )
        elif intent_classification.intent == IntentType.PRIOR_ART_SEARCH:
            # Prior art search handler
            from .prior_art_search import search_prior_art_optimized

            # Extract search terms (simple heuristic; LLM can refine)
            search_terms = user_input.replace("search prior art", "").replace("find prior art", "").replace("prior art", "").strip()
            if not search_terms:
                search_terms = user_input

            result = search_prior_art_optimized(search_terms, max_results=10)
            
            # Format the result for display
            from .prior_art_search import format_optimized_results
            formatted_results = format_optimized_results(result)
            
            # Create simplified result structure for compatibility
            simplified = {
                "results": formatted_results,
                "thought_process": f"Prior art search completed for: {search_terms}",
                "prior_art_result": formatted_results,
                "patents": [patent.patent_id for patent in result.patents]
            }

            return AgentResponse(
                conversation_response=formatted_results,
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). Found {len(result.patents)} relevant patents",
                should_draft_claims=False,
                prior_art_result=simplified
            )
            
        elif intent_classification.intent == IntentType.INVENTION_ANALYSIS:
            # Analyze invention for patentability
            analysis = general_conversation(f"Please analyze this invention for patentability and provide specific guidance: {user_input}")
            return AgentResponse(
                conversation_response=analysis,
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). {intent_classification.reasoning}",
                should_draft_claims=False
            )
            
        elif intent_classification.intent == IntentType.TECHNICAL_QUERY:
            # Handle technical questions
            response_text = general_conversation(user_input)
            return AgentResponse(
                conversation_response=response_text,
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). {intent_classification.reasoning}",
                should_draft_claims=False
            )
            
        else:
            # General conversation
            response_text = general_conversation(user_input)
            return AgentResponse(
                conversation_response=response_text,
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). {intent_classification.reasoning}",
                should_draft_claims=False
            )
            
    except Exception as e:
        logging.error(f"Error in agent_run: {e}")
        return AgentResponse(
            conversation_response="I encountered an error processing your request. Could you try rephrasing it?",
            reasoning=f"Error occurred: {str(e)}",
            should_draft_claims=False
        )

# Agent class for compatibility
class IntelligentAgent:
    """Intelligent agent with simple confidence threshold: execute (>0.7) or seek clarification (≤0.7)"""
    async def run(self, user_input: str, conversation_context: str = ""):
        return await agent_run(user_input, conversation_context)
    
    async def run_streaming(self, user_input: str, conversation_context: str = ""):
        """Streaming version of agent logic that yields progress as each step completes"""
        async for event in agent_run_streaming(user_input, conversation_context):
            yield event

async def agent_run_streaming(user_input: str, conversation_context: str = "") -> AsyncGenerator[Dict[str, Any], None]:
    """Streaming version of agent logic that yields progress as each step completes"""
    try:
        # Step 1: Stream intent classification
        yield {
            "type": "intent_analysis",
            "message": "Analyzing your request to understand the intent...",
            "user_input": user_input[:100] + "..." if len(user_input) > 100 else user_input
        }
        
        intent_classification = await classify_user_intent(user_input, conversation_context)
        
        yield {
            "type": "intent_classified",
            "intent": intent_classification.intent.value,
            "confidence_score": intent_classification.confidence_score,
            "reasoning": intent_classification.reasoning,
            "suggested_actions": intent_classification.suggested_actions
        }
        
        logging.info(f"Intent classified as: {intent_classification.intent} (confidence: {intent_classification.confidence_score})")
        
        # Step 2: Check confidence threshold
        if intent_classification.confidence_score <= 0.7:
            yield {
                "type": "low_confidence",
                "message": "I'm not entirely sure what you're asking for. Could you provide more details?",
                "confidence": intent_classification.confidence_score
            }
            return
        
        # Step 3: Execute high-confidence intents with streaming
        if intent_classification.intent == IntentType.CLAIM_DRAFTING:
            yield {
                "type": "claims_drafting_start",
                "message": "Starting patent claims drafting...",
                "disclosure_length": len(user_input)
            }
            
            yield {
                "type": "claims_progress",
                "message": "Analyzing invention disclosure...",
                "stage": "analysis"
            }
            await asyncio.sleep(0.3)  # Simulate analysis time
            
            yield {
                "type": "claims_progress",
                "message": "Identifying key inventive features...",
                "stage": "feature_identification"
            }
            await asyncio.sleep(0.4)  # Simulate feature identification time
            
            yield {
                "type": "claims_progress",
                "message": "Drafting comprehensive patent claims...",
                "stage": "drafting"
            }
            await asyncio.sleep(0.3)  # Simulate drafting preparation time
            
            # Actually draft the claims
            claims = draft_claims(user_input, conversation_context)
            
            # Stream each claim as it's "generated" with simulated delays
            for i, claim in enumerate(claims, 1):
                # Simulate the time it takes to generate each claim
                await asyncio.sleep(0.5)  # 500ms delay between claims
                
                yield {
                    "type": "claim_generated",
                    "claim_number": i,
                    "text": claim,
                    "total_claims": len(claims)
                }
            
            yield {
                "type": "claims_complete",
                "message": f"Successfully drafted {len(claims)} patent claims",
                "num_claims": len(claims),
                "claims": claims
            }
            
            # Send final completion event with the actual claims
            yield {
                "type": "complete",
                "message": f"Successfully drafted {len(claims)} patent claims",
                "response": f"I've drafted {len(claims)} patent claims based on your invention:\n\n" + "\n\n".join(claims),
                "metadata": {
                    "should_draft_claims": True,
                    "has_claims": True,
                    "reasoning": f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score})"
                },
                "data": {
                    "claims": claims,
                    "num_claims": len(claims)
                }
            }
            
        elif intent_classification.intent == IntentType.PRIOR_ART_SEARCH:
            yield {
                "type": "prior_art_start",
                "message": "Starting prior art search..."
            }
            await asyncio.sleep(0.3)  # Simulate startup time
            
            yield {
                "type": "prior_art_progress",
                "message": "Searching patent databases for relevant prior art...",
                "stage": "searching"
            }
            await asyncio.sleep(0.8)  # Simulate database search time
            
            yield {
                "type": "prior_art_progress",
                "message": "Analyzing search results for relevance and blocking potential...",
                "stage": "analyzing"
            }
            await asyncio.sleep(0.6)  # Simulate analysis time
            
            yield {
                "type": "prior_art_progress",
                "message": "Generating comprehensive prior art analysis report...",
                "stage": "reporting"
            }
            await asyncio.sleep(0.5)  # Simulate report generation time
            
            # Actually perform the search
            from .prior_art_search import search_prior_art_optimized, format_optimized_results
            
            search_terms = user_input.replace("search prior art", "").replace("find prior art", "").replace("prior art", "").strip()
            if not search_terms:
                search_terms = user_input
                
            result = search_prior_art_optimized(search_terms, max_results=10)
            formatted_results = format_optimized_results(result)
            
            yield {
                "type": "prior_art_complete",
                "message": "Prior art search completed",
                "results": formatted_results,
                "patents_found": len(result.patents)
            }
            
            # Send final completion event with the prior art results
            yield {
                "type": "complete",
                "message": "Prior art search completed",
                "response": formatted_results,
                "metadata": {
                    "should_draft_claims": False,
                    "has_claims": False,
                    "reasoning": f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score})"
                },
                "data": {
                    "prior_art_result": {
                        "results": formatted_results,
                        "patents_found": len(result.patents)
                    }
                }
            }
            
        elif intent_classification.intent == IntentType.CLAIM_REVIEW:
            yield {
                "type": "review_start",
                "message": "Starting claim review process..."
            }
            
            yield {
                "type": "review_progress",
                "message": "Analyzing claim structure and language...",
                "stage": "analysis"
            }
            
            yield {
                "type": "review_progress",
                "message": "Checking USPTO compliance...",
                "stage": "compliance_check"
            }
            
            # Actually review the claims
            review_comments = review_claims(user_input, conversation_context)
            
            yield {
                "type": "review_complete",
                "message": f"Claim review completed - found {len(review_comments)} issues",
                "review_comments": review_comments
            }
            
        else:
            # Handle other intents
            yield {
                "type": "processing",
                "message": f"Processing {intent_classification.intent.value} request...",
                "intent": intent_classification.intent.value
            }
            
            # Execute the intent
            if intent_classification.intent == IntentType.PATENT_GUIDANCE:
                response_text = general_conversation(user_input)
            elif intent_classification.intent == IntentType.INVENTION_ANALYSIS:
                response_text = general_conversation(f"Please analyze this invention for patentability and provide specific guidance: {user_input}")
            elif intent_classification.intent == IntentType.TECHNICAL_QUERY:
                response_text = general_conversation(user_input)
            else:
                response_text = general_conversation(user_input)
            
            yield {
                "type": "complete",
                "message": "Request processed successfully",
                "response": response_text
            }
        
    except Exception as e:
        logging.error(f"Error in agent_run_streaming: {e}")
        yield {
            "type": "error",
            "error": str(e),
            "message": "I encountered an error processing your request. Please try again."
        }

# Export the agent
agent = IntelligentAgent()

# Setup logger
logging.basicConfig(level=logging.INFO)