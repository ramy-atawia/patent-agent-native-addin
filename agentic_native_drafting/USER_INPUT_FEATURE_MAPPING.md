# 🎯 **USER INPUT FEATURE MAPPING GUIDE**

## **Overview**
This document illustrates how different user input conditions are analyzed and mapped to specific features, tools, and workflows in the Agentic Native Drafting system.

---

## 🔍 **INTENT CLASSIFICATION SYSTEM**

### **How It Works**
The system uses LLM-based intent classification to analyze user input and determine the most appropriate tool and workflow. The classification happens in the `AgentOrchestrator._get_llm_based_intent()` method.

### **Classification Prompt Structure**
```python
# System prompt for intent classification
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
```

---

## 📋 **INTENT TYPES & TOOL MAPPINGS**

### **1. 🏗️ CONTENT DRAFTING** (`content_drafting`)
**Tool**: `ContentDraftingTool`

#### **Trigger Keywords & Phrases:**
- "draft", "create", "write", "generate"
- "patent claims", "claims", "patent drafting"
- "new invention", "invention description"
- "technical specification", "specification"

#### **Example User Inputs:**
```
✅ "I want to draft patent claims for a wireless communication system"
✅ "Create claims for my new invention about solar panels"
✅ "Generate patent claims for a machine learning algorithm"
✅ "Write claims for an automotive safety system"
✅ "Draft patent claims for a medical device"
```

#### **Features Activated:**
- Input sufficiency assessment
- LLM-based content generation
- Structured output formatting
- Multiple content types (primary/secondary)
- Focus area identification
- Dependency mapping

#### **Output Format:**
```json
{
  "content": [
    {
      "content_number": "1",
      "content_text": "A method for optimizing handover...",
      "content_type": "primary",
      "dependency": null,
      "focus_area": "wireless_communication"
    }
  ],
  "reasoning": "Based on the user's request...",
  "input_assessment": {...}
}
```

---

### **2. 🔍 CONTENT REVIEW** (`content_review`)
**Tool**: `ContentReviewTool`

#### **Trigger Keywords & Phrases:**
- "review", "analyze", "evaluate", "assess"
- "check claims", "validate", "quality"
- "improve", "enhance", "optimize"
- "feedback", "suggestions"

#### **Example User Inputs:**
```
✅ "Review my patent claims for completeness"
✅ "Analyze the quality of my invention description"
✅ "Evaluate my patent specification"
✅ "Check if my claims are properly structured"
✅ "Provide feedback on my patent draft"
```

#### **Features Activated:**
- Content quality scoring
- Issue identification
- Structural analysis
- Technical term analysis
- Dependency validation
- Improvement recommendations

#### **Output Format:**
```json
{
  "content_quality_scores": [0.85, 0.92, 0.78],
  "identified_issues": ["Missing dependency", "Unclear terminology"],
  "structural_analysis": {...},
  "technical_coverage": {...},
  "recommendations": [...]
}
```

---

### **3. 🔎 PRIOR ART SEARCH** (`search`)
**Tool**: `PriorArtSearchTool`

#### **Trigger Keywords & Phrases:**
- "search", "find", "look for", "prior art"
- "existing patents", "similar inventions"
- "patent database", "literature search"
- "competitor analysis", "freedom to operate"

#### **Example User Inputs:**
```
✅ "Search for prior art related to wireless charging"
✅ "Find existing patents for machine learning in healthcare"
✅ "Look for similar inventions to my solar panel design"
✅ "Search patent database for automotive safety systems"
✅ "Find prior art for medical device innovations"
```

#### **Features Activated:**
- PatentsView API integration
- Keyword-based search
- Patent classification search
- Inventor/assignee search
- Citation analysis
- Relevance scoring

#### **Output Format:**
```json
{
  "search_results": [
    {
      "patent_number": "US10123456",
      "title": "Wireless Charging System",
      "abstract": "...",
      "relevance_score": 0.92,
      "classification": "H02J7/00"
    }
  ],
  "search_metadata": {...}
}
```

---

### **4. 💡 GUIDANCE & ADVICE** (`guidance`)
**Tool**: `GeneralGuidanceTool`

#### **Trigger Keywords & Phrases:**
- "guidance", "advice", "help", "recommendations"
- "best practices", "strategies", "tips"
- "how to", "what should I", "explain"
- "patent strategy", "filing advice"

#### **Example User Inputs:**
```
✅ "Give me guidance on patent filing strategy"
✅ "What are best practices for claim drafting?"
✅ "Help me understand patent prosecution"
✅ "Advice on international patent filing"
✅ "Recommendations for patent portfolio management"
```

#### **Features Activated:**
- Patent law guidance
- Best practice recommendations
- Strategic advice
- Educational content
- Process explanations
- Risk assessment

#### **Output Format:**
```json
{
  "guidance_type": "patent_strategy",
  "recommendations": [...],
  "best_practices": [...],
  "risks_and_considerations": [...],
  "next_steps": [...]
}
```

---

### **5. 📊 ANALYSIS & QUERY** (`analysis`)
**Tool**: `GeneralConversationTool`

#### **Trigger Keywords & Phrases:**
- "analyze", "examine", "investigate", "study"
- "compare", "contrast", "evaluate"
- "statistics", "trends", "patterns"
- "market analysis", "competitive landscape"

#### **Example User Inputs:**
```
✅ "Analyze patent trends in AI technology"
✅ "Compare different patent filing strategies"
✅ "Examine the competitive landscape in my field"
✅ "Study patent citation patterns"
✅ "Investigate market trends for my invention"
```

#### **Features Activated:**
- Data analysis
- Trend identification
- Comparative analysis
- Statistical insights
- Market research
- Competitive intelligence

---

### **6. 💬 GENERAL CONVERSATION** (`general_conversation`)
**Tool**: `GeneralConversationTool`

#### **Trigger Keywords & Phrases:**
- "hello", "hi", "greetings"
- "general questions", "casual conversation"
- "explain", "what is", "tell me about"
- "conversation", "chat"

#### **Example User Inputs:**
```
✅ "Hello, how can you help me with patents?"
✅ "What is the Agentic Native Drafting system?"
✅ "Tell me about patent law basics"
✅ "How does the patent process work?"
✅ "General questions about intellectual property"
```

#### **Features Activated:**
- General conversation handling
- System information
- Basic explanations
- Welcome messages
- Help content
- Educational responses

---

## 🎯 **CONFIDENCE SCORING SYSTEM**

### **Confidence Levels:**
- **0.9 - 1.0**: High confidence - Clear intent, specific keywords
- **0.7 - 0.89**: Medium confidence - Good intent, some ambiguity
- **0.5 - 0.69**: Low confidence - Unclear intent, fallback needed
- **< 0.5**: Very low confidence - Use general conversation tool

### **Confidence Factors:**
1. **Keyword presence** (draft, review, search, etc.)
2. **Context clarity** (patent-specific terminology)
3. **Request specificity** (detailed vs. vague)
4. **Domain relevance** (patent/IP related)

---

## 🔄 **WORKFLOW SELECTION LOGIC**

### **Primary Workflow Selection:**
```python
def _get_tool_name_for_intent(self, intent_type: str) -> str:
    intent_to_tool = {
        "content_drafting": "ContentDraftingTool",
        "content_review": "ContentReviewTool", 
        "search": "PriorArtSearchTool",
        "guidance": "GeneralGuidanceTool",
        "analysis": "GeneralConversationTool",
        "query": "GeneralConversationTool",
        "general_conversation": "GeneralConversationTool"
    }
    return intent_to_tool.get(intent_type, "GeneralConversationTool")
```

### **Fallback Logic:**
1. **Primary tool** fails → Try alternative tool
2. **LLM classification** fails → Use keyword-based fallback
3. **Tool not found** → Use GeneralConversationTool
4. **Error occurs** → Return error event with suggestions

---

## 📝 **USER INPUT EXAMPLES BY COMPLEXITY**

### **🟢 Simple Inputs (High Confidence)**
```
Input: "Draft patent claims for wireless charging"
Intent: content_drafting (0.95)
Tool: ContentDraftingTool
Features: Basic content generation
```

### **🟡 Medium Inputs (Medium Confidence)**
```
Input: "I need help creating claims for my invention about solar panels"
Intent: content_drafting (0.85)
Tool: ContentDraftingTool
Features: Enhanced content generation + guidance
```

### **🟠 Complex Inputs (Lower Confidence)**
```
Input: "Can you help me with my patent? I have an invention but I'm not sure how to proceed"
Intent: guidance (0.75)
Tool: GeneralGuidanceTool
Features: Strategic guidance + educational content
```

### **🔴 Ambiguous Inputs (Low Confidence)**
```
Input: "I need assistance"
Intent: general_conversation (0.60)
Tool: GeneralConversationTool
Features: Clarification questions + help menu
```

---

## 🎨 **CONTEXT-AWARE FEATURE SELECTION**

### **Document Context:**
- **Has document content** → Enable document-aware features
- **No document content** → Focus on general guidance
- **Document type detection** → Adjust tool behavior

### **Conversation History:**
- **Previous requests** → Maintain context across interactions
- **User preferences** → Remember preferred tools/approaches
- **Session continuity** → Build on previous work

### **Domain Context:**
- **Patent-specific** → Use specialized patent tools
- **General IP** → Use guidance tools
- **Technical** → Enable technical analysis features

---

## 🚀 **ADVANCED FEATURE SELECTION**

### **Multi-Tool Workflows:**
```
Input: "Draft claims and then review them for quality"
Workflow: ContentDraftingTool → ContentReviewTool
Features: Sequential execution, output chaining
```

### **Conditional Features:**
```
Input: "Draft claims for my wireless invention"
Conditions: 
- If technical details provided → Full content generation
- If minimal details → Input assessment + guidance
- If document attached → Document-aware generation
```

### **Adaptive Responses:**
```
Input: "Help me with patents"
Response: 
- New user → Educational content + tool introduction
- Experienced user → Advanced features + shortcuts
- Returning user → Personalized recommendations
```

---

## 📊 **FEATURE SELECTION MATRIX**

| User Input Type | Primary Tool | Secondary Tools | Features | Confidence Threshold |
|----------------|--------------|-----------------|----------|---------------------|
| **Content Creation** | ContentDraftingTool | - | Generation, Assessment, Formatting | 0.8+ |
| **Content Review** | ContentReviewTool | - | Analysis, Scoring, Recommendations | 0.8+ |
| **Prior Art Search** | PriorArtSearchTool | - | Search, Analysis, Relevance | 0.8+ |
| **Strategic Guidance** | GeneralGuidanceTool | - | Advice, Best Practices, Strategy | 0.7+ |
| **Data Analysis** | GeneralConversationTool | - | Analysis, Trends, Insights | 0.7+ |
| **General Help** | GeneralConversationTool | - | Education, Clarification, Help | 0.6+ |

---

## 🔧 **CUSTOMIZATION & EXTENSIBILITY**

### **Adding New Intent Types:**
1. **Update intent classification** in orchestrator
2. **Add tool mapping** in `_get_tool_name_for_intent()`
3. **Create new tool** implementing Tool interface
4. **Update prompts** for new intent types

### **Modifying Feature Selection:**
1. **Adjust confidence thresholds** per intent type
2. **Add conditional logic** for complex workflows
3. **Implement tool chaining** for multi-step processes
4. **Add context-aware** feature selection

---

## 📈 **MONITORING & ANALYTICS**

### **Intent Classification Metrics:**
- **Accuracy**: % of correct intent classifications
- **Confidence distribution**: Spread of confidence scores
- **Tool usage**: Frequency of each tool selection
- **User satisfaction**: Feedback on tool appropriateness

### **Feature Performance:**
- **Tool execution time**: Performance metrics per tool
- **Success rates**: % of successful tool executions
- **Error patterns**: Common failure modes
- **User engagement**: Feature usage patterns

---

## 🎯 **BEST PRACTICES FOR USER INPUT**

### **For High-Quality Results:**
1. **Be specific**: "Draft claims for wireless charging system" vs "Help with patents"
2. **Provide context**: Include technical details, domain information
3. **State intent clearly**: Use action words (draft, review, search, analyze)
4. **Include examples**: Reference similar inventions or technologies

### **For Complex Requests:**
1. **Break down requests**: Separate multiple objectives
2. **Provide background**: Explain the invention context
3. **Specify requirements**: Mention specific needs or constraints
4. **Ask follow-up questions**: Request clarification when needed

---

This mapping system ensures that users get the most appropriate tools and features based on their input, leading to better results and user experience! 🚀
