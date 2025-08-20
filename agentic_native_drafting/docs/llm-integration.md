# LLM Integration

Comprehensive guide to Azure OpenAI integration, prompt engineering, and function calling in the Agentic Native Drafting Service.

## 🎯 Overview

The system integrates with Azure OpenAI's GPT-4o-mini model to provide intelligent patent drafting capabilities through:
- **Dynamic Intent Classification**: Understanding user requests
- **Context-Aware Responses**: Using session history for consistency
- **Function Calling**: Structured execution of patent-related tasks
- **Confidence Scoring**: Decision-making based on LLM confidence

## 🔗 Azure OpenAI Integration

### **Configuration**

#### **Environment Variables**
```bash
# .env file
AZURE_OPENAI_ENDPOINT=https://{deployment}.cognitiveservices.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-12-01-preview
```

#### **Integration Setup**
```python
import os
from dotenv import load_dotenv
import httpx

# Load environment variables
load_dotenv()

# Azure OpenAI configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_DEPLOYMENT_NAME = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")

# API endpoint construction
api_url = f"{AZURE_OPENAI_ENDPOINT}/openai/deployments/{AZURE_OPENAI_DEPLOYMENT_NAME}/chat/completions?api-version={AZURE_OPENAI_API_VERSION}"
```

---

### **API Communication**

#### **HTTP Client Setup**
```python
async def send_llm_request(messages: List[Dict[str, str]], functions: List[Dict] = None) -> Dict:
    """Send request to Azure OpenAI API"""
    
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_API_KEY
    }
    
    payload = {
        "messages": messages,
        "model": AZURE_OPENAI_DEPLOYMENT_NAME,
        "temperature": 0.1,  # Low temperature for consistent outputs
        "max_tokens": 4000,
        "stream": False
    }
    
    if functions:
        payload["functions"] = functions
        payload["function_call"] = "auto"
    
    async with httpx.AsyncClient() as client:
        response = await client.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
```

#### **Response Handling**
```python
def parse_llm_response(response: Dict) -> Dict[str, Any]:
    """Parse Azure OpenAI API response"""
    
    if "choices" not in response or not response["choices"]:
        raise ValueError("No choices in LLM response")
    
    choice = response["choices"][0]
    message = choice["message"]
    
    result = {
        "content": message.get("content", ""),
        "function_call": message.get("function_call"),
        "finish_reason": choice.get("finish_reason")
    }
    
    return result
```

---

## 🧠 Intent Classification System

### **Core Classification Function**

#### **Intent Classification Implementation**
```python
async def classify_user_intent(user_input: str, conversation_context: str = "") -> IntentClassification:
    """Use LLM to classify user intent with confidence scores"""
    
    try:
        # Build context-aware prompt
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

        Consider:
        - Explicit keywords in the user's request
        - Technical complexity of the input
        - Whether they're asking for specific actions
        - Context from previous conversation in this session
        - Professional patent terminology
        - References to previous claims or responses (e.g., "review those claims", "check my claims")

        Use the classify_user_intent function to provide your analysis.
        """
        
        # Function definition for structured output
        functions = [
            {
                "name": "classify_user_intent",
                "description": "Classify the user's intent and provide confidence score",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "intent": {
                            "type": "string",
                            "enum": ["claim_drafting", "claim_review", "patent_guidance", "invention_analysis", "technical_query", "general_conversation"],
                            "description": "The classified intent type"
                        },
                        "confidence_score": {
                            "type": "number",
                            "minimum": 0.0,
                            "maximum": 1.0,
                            "description": "Confidence in the classification (0.0 to 1.0)"
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Explanation for the classification decision"
                        }
                    },
                    "required": ["intent", "confidence_score", "reasoning"]
                }
            }
        ]
        
        # Send request to LLM
        messages = [{"role": "user", "content": prompt}]
        response = await send_llm_request(messages, functions)
        result = parse_llm_response(response)
        
        # Parse function call response
        if result["function_call"]:
            function_args = json.loads(result["function_call"]["arguments"])
            
            return IntentClassification(
                intent=IntentType(function_args["intent"]),
                confidence_score=function_args["confidence_score"],
                reasoning=function_args["reasoning"]
            )
        else:
            raise RuntimeError("LLM did not return a function call for intent classification")
            
    except Exception as e:
        print(f"❌ Error in intent classification: {e}")
        raise
```

---

### **Intent Types & Examples**

#### **1. Claim Drafting Intent**
**Trigger Phrases**:
- "draft patent claims"
- "create claims for my invention"
- "write patent claims"
- "generate claims"

**Example Classification**:
```
User Input: "Please draft patent claims for my AI-powered quantum computing system"
Intent: claim_drafting
Confidence: 0.95
Reasoning: "User explicitly requests drafting patent claims for a specific invention"
```

#### **2. Claim Review Intent**
**Trigger Phrases**:
- "review my claims"
- "check these claims"
- "validate my patent claims"
- "review those claims"

**Example Classification**:
```
User Input: "Review those claims I just showed you for quality"
Intent: claim_review
Confidence: 0.95
Reasoning: "User references previous claims and requests review"
```

#### **3. Patent Guidance Intent**
**Trigger Phrases**:
- "how do I patent"
- "patent process"
- "patent strategy"
- "patent advice"

**Example Classification**:
```
User Input: "How do I patent my AI invention?"
Intent: patent_guidance
Confidence: 0.9
Reasoning: "User seeks general patent process guidance"
```

#### **4. Invention Analysis Intent**
**Trigger Phrases**:
- "analyze my invention"
- "is this patentable"
- "evaluate invention"
- "patentability assessment"

**Example Classification**:
```
User Input: "I invented a 5G AI system, is it patentable?"
Intent: invention_analysis
Confidence: 0.9
Reasoning: "User describes invention and seeks patentability analysis"
```

---

## 🎯 Function Calling System

### **Function Definitions**

#### **Available Functions**
```python
# Function definitions for LLM function calling
FUNCTIONS = [
    {
        "name": "classify_user_intent",
        "description": "Classify user intent for patent-related requests",
        "parameters": {
            "type": "object",
            "properties": {
                "intent": {
                    "type": "string",
                    "enum": ["claim_drafting", "claim_review", "patent_guidance", "invention_analysis", "technical_query", "general_conversation"]
                },
                "confidence_score": {
                    "type": "number",
                    "minimum": 0.0,
                    "maximum": 1.0
                },
                "reasoning": {
                    "type": "string"
                }
            },
            "required": ["intent", "confidence_score", "reasoning"]
        }
    }
]
```

#### **Function Execution Flow**
```
LLM Response → Function Call Parsing → Function Execution → Response Generation
      ↓              ↓                    ↓              ↓
  Function      Extract Args        Call Function    Return Result
  Call Data     and Name           with Params      to Client
```

---

## 🔍 Confidence Threshold System

### **Decision Logic**

#### **Confidence-Based Routing**
```python
async def agent_run(user_input: str, conversation_context: str = "") -> AgentResponse:
    """Main agent logic with confidence threshold: execute (>0.7) or seek clarification (≤0.7)"""
    
    try:
        # Step 1: Classify user intent using LLM
        intent_classification = await classify_user_intent(user_input, conversation_context)
        
        # Step 2: Check confidence threshold
        if intent_classification.confidence_score <= 0.7:
            # Low confidence - seek clarification
            clarification_message = f"I'm not entirely sure what you're asking for. Could you provide more details about what you need? Your request seems to be about {intent_classification.intent.value.replace('_', ' ')} but I want to make sure I understand correctly."
            
            return AgentResponse(
                conversation_response=clarification_message,
                reasoning=f"Low confidence ({intent_classification.confidence_score}) - seeking user clarification...",
                metadata={
                    "should_draft_claims": False,
                    "has_claims": False,
                    "confidence": intent_classification.confidence_score,
                    "detected_intent": intent_classification.intent.value
                }
            )
        
        # High confidence - execute the detected intent
        print(f"✅ High confidence ({intent_classification.confidence_score}) - executing {intent_classification.intent.value}")
        
        # Step 3: Route to appropriate function based on intent
        if intent_classification.intent == IntentType.CLAIM_DRAFTING:
            # Draft patent claims with session history
            claims = draft_claims(user_input, 3, conversation_context)
            
            return AgentResponse(
                conversation_response=f"I've drafted {len(claims)} patent claims based on your invention:\n\n" + "\n\n".join(f"{i+1}. {claim}" for i, claim in enumerate(claims)),
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). {intent_classification.reasoning}",
                metadata={
                    "should_draft_claims": True,
                    "has_claims": True,
                    "confidence": intent_classification.confidence_score,
                    "num_claims": len(claims)
                },
                data={
                    "claims": claims,
                    "num_claims": len(claims)
                }
            )
            
        elif intent_classification.intent == IntentType.CLAIM_REVIEW:
            # Handle claim review - extract claims from user input and review them
            review_comments = review_claims(user_input, conversation_context)
            
            # Format response with severity indicators
            severity_emojis = {"minor": "🟢", "major": "🟡", "critical": "🔴"}
            formatted_comments = []
            
            for comment in review_comments:
                emoji = severity_emojis.get(comment.severity.lower(), "⚪")
                formatted_comments.append(f"{emoji} **{comment.severity.upper()}**: {comment.comment}")
                if comment.suggestion:
                    formatted_comments.append(f"   *Suggestion: {comment.suggestion}*")
            
            response_text = f"I've reviewed your patent claims and found {len(review_comments)} issue(s):\n\n" + "\n\n".join(formatted_comments)
            
            return AgentResponse(
                conversation_response=response_text,
                reasoning=f"Executing {intent_classification.intent.value} (confidence: {intent_classification.confidence_score}). {intent_classification.reasoning}",
                review_comments=review_comments,
                metadata={
                    "should_draft_claims": False,
                    "has_claims": False,
                    "confidence": intent_classification.confidence_score,
                    "review_count": len(review_comments)
                }
            )
            
        # ... handle other intent types
        
    except Exception as e:
        print(f"❌ Error in agent run: {e}")
        return AgentResponse(
            conversation_response="I encountered an error processing your request. Please try again with more specific details about what you need.",
            reasoning=f"Error occurred: {str(e)}",
            metadata={
                "should_draft_claims": False,
                "has_claims": False,
                "error": str(e)
            }
        )
```

---

## 📝 Prompt Engineering

### **Prompt Design Principles**

#### **1. Role Definition**
```python
# Clear role definition for consistent behavior
role_prompt = """You are an expert patent attorney AI assistant with deep knowledge of:
- USPTO patent law and requirements
- Patent claim drafting and review
- Technical invention analysis
- Patent strategy and guidance

Your responses should be:
- Professional and legally accurate
- Technically precise
- Actionable and specific
- Consistent with patent law standards"""
```

#### **2. Context Integration**
```python
# Session history integration for context awareness
context_prompt = f"""
Session History:
{conversation_context if conversation_context else "No previous conversation in this session"}

Use this context to:
- Maintain technical consistency with previous discussions
- Reference previously generated claims when appropriate
- Build upon previous feedback and improvements
- Understand the user's invention and patent goals"""
```

#### **3. Output Formatting**
```python
# Structured output requirements
format_prompt = """
Format your response as follows:

For Patent Claims:
1. [Independent claim with clear technical elements]
2. [Dependent claim adding specific features]
3. [Additional dependent claims as needed]

For Reviews:
🟢 MINOR: [Issue description]
🟡 MAJOR: [Issue description]  
🔴 CRITICAL: [Issue description]

For Guidance:
- [Key point 1]
- [Key point 2]
- [Key point 3]"""
```

---

### **Specialized Prompts**

#### **1. Claim Drafting Prompt**
```python
def draft_claims(disclosure: str, num_claims: int = 3, session_history: str = "") -> List[str]:
    """Draft patent claims based on disclosure and session history"""
    
    # Build context-aware prompt
    context_prompt = ""
    if session_history:
        context_prompt = f"""
Session History:
{session_history}
Use this context to ensure consistency with any previously discussed inventions or claims."""
    
    messages = [
        {
            "role": "system",
            "content": "You are a patent attorney expert in drafting USPTO-compliant patent claims. Generate patent claims directly in your response."
        },
        {
            "role": "user", 
            "content": f"""Draft {num_claims} patent claims based on this invention disclosure:

{disclosure}{context_prompt}

Requirements:
1. First claim should be an independent claim (method or system)
2. Subsequent claims should be dependent claims adding specific features
3. Follow USPTO formatting and requirements
4. Use clear, precise language
5. Ensure claims are patentable subject matter under 35 USC 101
6. Maintain consistency with session context if available

Format each claim as a numbered list item."""
        }
    ]
    
    # Send to LLM and parse response
    response = await send_llm_request(messages)
    result = parse_llm_response(response)
    
    # Parse numbered claims from response
    claims = parse_numbered_claims(result["content"])
    return claims
```

#### **2. Claim Review Prompt**
```python
def review_claims(claims_text: str, session_history: str = "") -> List[ReviewComment]:
    """Review patent claims and provide feedback using session history for context"""
    
    # Build context-aware prompt
    context_prompt = ""
    if session_history:
        context_prompt = f"""
Session Context:
{session_history}
Use this context to understand what was previously discussed and provide more relevant feedback."""
    
    messages = [
        {
            "role": "system",
            "content": "You are a senior patent attorney expert in USPTO compliance and patent claim quality. Review claims and provide specific, actionable feedback."
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

For each issue found, provide:
- Specific problem description
- Severity level (minor/major/critical)
- Suggested improvement

Format your response as a numbered list of review comments."""
        }
    ]
    
    # Send to LLM and parse response
    response = await send_llm_request(messages)
    result = parse_llm_response(response)
    
    # Parse review comments from response
    comments = parse_review_comments(result["content"])
    return comments
```

---

## 🔄 Response Parsing

### **Structured Output Parsing**

#### **1. Claim Parsing**
```python
def parse_numbered_claims(response_text: str) -> List[str]:
    """Parse numbered patent claims from LLM response"""
    
    claims = []
    lines = response_text.split('\n')
    
    for line in lines:
        line = line.strip()
        # Look for numbered claims (1., 2., 3., etc.)
        if re.match(r'^\d+\.', line):
            # Extract claim text (remove number and period)
            claim_text = re.sub(r'^\d+\.\s*', '', line)
            if claim_text:
                claims.append(claim_text)
    
    return claims
```

#### **2. Review Comment Parsing**
```python
def parse_review_comments(response_text: str) -> List[ReviewComment]:
    """Parse review comments from LLM response"""
    
    comments = []
    lines = response_text.split('\n')
    
    current_comment = None
    
    for line in lines:
        line = line.strip()
        
        # Look for numbered comments
        if re.match(r'^\d+\.', line):
            # Save previous comment if exists
            if current_comment:
                comments.append(current_comment)
            
            # Start new comment
            comment_text = re.sub(r'^\d+\.\s*', '', line)
            current_comment = ReviewComment(
                comment=comment_text,
                severity="minor",  # Default severity
                suggestion=""
            )
        
        # Look for severity indicators
        elif "minor" in line.lower() or "🟢" in line:
            if current_comment:
                current_comment.severity = "minor"
        elif "major" in line.lower() or "🟡" in line:
            if current_comment:
                current_comment.severity = "major"
        elif "critical" in line.lower() or "🔴" in line:
            if current_comment:
                current_comment.severity = "critical"
        
        # Look for suggestions
        elif "suggestion:" in line.lower() or "suggest:" in line.lower():
            if current_comment:
                suggestion = re.sub(r'^.*?suggestion:?\s*', '', line, flags=re.IGNORECASE)
                current_comment.suggestion = suggestion
    
    # Add final comment
    if current_comment:
        comments.append(current_comment)
    
    return comments
```

---

## 📊 Performance & Optimization

### **Response Time Optimization**

#### **1. Prompt Optimization**
- **Concise Prompts**: Remove unnecessary instructions
- **Clear Structure**: Use consistent formatting
- **Context Limits**: Limit session history length
- **Token Management**: Monitor token usage

#### **2. Caching Strategies**
```python
# Future enhancement: Response caching
class ResponseCache:
    def __init__(self):
        self._cache = {}
        self._max_size = 1000
    
    def get_cached_response(self, prompt_hash: str) -> Optional[Dict]:
        return self._cache.get(prompt_hash)
    
    def cache_response(self, prompt_hash: str, response: Dict):
        if len(self._cache) >= self._max_size:
            # Remove oldest entries
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]
        
        self._cache[prompt_hash] = response
```

#### **3. Batch Processing**
```python
# Future enhancement: Batch LLM requests
async def batch_classify_intents(user_inputs: List[str]) -> List[IntentClassification]:
    """Classify multiple user inputs in a single LLM request"""
    
    # Combine multiple inputs into single prompt
    combined_prompt = "Classify the following user inputs:\n\n"
    for i, input_text in enumerate(user_inputs):
        combined_prompt += f"{i+1}. {input_text}\n"
    
    # Send single request
    messages = [{"role": "user", "content": combined_prompt}]
    response = await send_llm_request(messages, FUNCTIONS)
    
    # Parse multiple classifications
    # Implementation depends on LLM response format
```

---

## 🔒 Error Handling & Reliability

### **Error Scenarios**

#### **1. API Failures**
```python
async def send_llm_request_with_retry(messages: List[Dict[str, str]], functions: List[Dict] = None, max_retries: int = 3) -> Dict:
    """Send LLM request with retry logic"""
    
    for attempt in range(max_retries):
        try:
            return await send_llm_request(messages, functions)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 429:  # Rate limit
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Rate limited, waiting {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            elif e.response.status_code >= 500:  # Server error
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt
                    print(f"Server error, retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
            else:
                raise
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                print(f"Request failed, retrying in {wait_time} seconds...")
                await asyncio.sleep(wait_time)
            else:
                raise
    
    raise Exception(f"Failed after {max_retries} attempts")
```

#### **2. Response Validation**
```python
def validate_llm_response(response: Dict) -> bool:
    """Validate LLM response structure and content"""
    
    # Check required fields
    if "choices" not in response:
        return False
    
    if not response["choices"]:
        return False
    
    choice = response["choices"][0]
    if "message" not in choice:
        return False
    
    message = choice["message"]
    
    # For function calls, validate function call structure
    if "function_call" in message:
        function_call = message["function_call"]
        if "name" not in function_call or "arguments" not in function_call:
            return False
    
    return True
```

---

## 🔮 Future Enhancements

### **Planned Improvements**

#### **1. Advanced Function Calling**
```python
# Future: More sophisticated function calling
FUNCTIONS = [
    {
        "name": "draft_claims",
        "description": "Draft patent claims for an invention",
        "parameters": {
            "type": "object",
            "properties": {
                "invention_type": {"type": "string", "enum": ["system", "method", "composition", "apparatus"]},
                "technical_domain": {"type": "string"},
                "claim_count": {"type": "integer", "minimum": 1, "maximum": 20},
                "complexity_level": {"type": "string", "enum": ["basic", "intermediate", "advanced"]}
            }
        }
    }
]
```

#### **2. Multi-Model Support**
```python
# Future: Support multiple LLM providers
class LLMProvider:
    def __init__(self, provider: str = "azure_openai"):
        self.provider = provider
        self.client = self._initialize_client()
    
    async def send_request(self, messages: List[Dict], functions: List[Dict] = None) -> Dict:
        if self.provider == "azure_openai":
            return await self._azure_openai_request(messages, functions)
        elif self.provider == "openai":
            return await self._openai_request(messages, functions)
        elif self.provider == "anthropic":
            return await self._anthropic_request(messages, functions)
```

#### **3. Prompt Templates**
```python
# Future: Template-based prompt management
class PromptTemplate:
    def __init__(self, template_name: str):
        self.template = self._load_template(template_name)
    
    def render(self, **kwargs) -> str:
        return self.template.format(**kwargs)

# Usage
template = PromptTemplate("intent_classification")
prompt = template.render(
    user_input=user_input,
    conversation_context=conversation_context,
    available_intents=intent_types
)
```

---

## 📋 Best Practices

### **For Developers**

1. **Prompt Design**:
   - Keep prompts concise and focused
   - Use consistent formatting and structure
   - Include clear examples and requirements
   - Test prompts with various inputs

2. **Error Handling**:
   - Implement comprehensive retry logic
   - Validate all LLM responses
   - Provide meaningful error messages
   - Log errors for debugging

3. **Performance**:
   - Monitor response times and token usage
   - Implement caching where appropriate
   - Use batch processing for multiple requests
   - Optimize prompt length and complexity

### **For Users**

1. **Clear Communication**:
   - Use specific, unambiguous language
   - Provide detailed invention descriptions
   - Reference previous claims explicitly
   - Ask one question at a time

2. **Context Management**:
   - Use the same session for related requests
   - Build upon previous feedback
   - Maintain consistent terminology
   - Reference specific claims when requesting reviews

---

**Next**: Read the [Development Guide](development.md) to understand how to set up and develop the system.
