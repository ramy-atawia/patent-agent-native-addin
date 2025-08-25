# Prompts Directory

This directory contains all LLM prompts used by the new modular backend system. All prompts are externalized from the code for better maintainability, version control, and prompt engineering.

## 📁 **Prompt Files Overview**

### **Core Intent Classification**
| File | Purpose | Used By |
|------|---------|----------|
| `intent_analysis_system.txt` | System prompt for intent analysis | `IntentClassificationTool` |
| `intent_analysis_user.txt` | User prompt for intent analysis | `IntentClassificationTool` |
| `intent_classification_system.txt` | System prompt for intent classification | `IntentClassificationTool` |
| `intent_classification_user.txt` | User prompt for intent classification | `IntentClassificationTool` |
| `intent_classification_orchestrator_system.txt` | System prompt for orchestrator intent classification | `AgentOrchestrator` |
| `intent_classification_orchestrator_user.txt` | User prompt for orchestrator intent classification | `AgentOrchestrator` |

### **Claims Processing**
| File | Purpose | Used By |
|------|---------|----------|
| `claims_analysis_system.txt` | System prompt for claims analysis | `ClaimDraftingTool` |
| `claims_analysis_user.txt` | User prompt for claims analysis | `ClaimDraftingTool` |
| `claims_generation_system.txt` | System prompt for claims generation | `ClaimDraftingTool` |
| `claims_generation_user.txt` | User prompt for claims generation | `ClaimDraftingTool` |
| `claim_drafting_user.txt` | Legacy user prompt for claim drafting | Legacy system |

### **Disclosure Assessment**
| File | Purpose | Used By |
|------|---------|----------|
| `disclosure_assessment_system.txt` | System prompt for disclosure assessment | `DisclosureAssessmentTool` |
| `disclosure_assessment_user.txt` | User prompt for disclosure assessment | `DisclosureAssessmentTool` |

### **General Conversation**
| File | Purpose | Used By |
|------|---------|----------|
| `general_conversation_system.txt` | System prompt for general conversation | `GeneralConversationTool` |
| `general_conversation_user.txt` | User prompt for general conversation | `GeneralConversationTool` |

### **Patent Guidance**
| File | Purpose | Used By |
|------|---------|----------|
| `patent_guidance_system.txt` | System prompt for patent guidance | `PatentGuidanceTool` |
| `patent_guidance_user.txt` | User prompt for patent guidance | `PatentGuidanceTool` |

### **Prior Art Search**
| File | Purpose | Used By |
|------|---------|----------|
| `prior_art_search_system.txt` | System prompt for prior art search | `PriorArtSearchTool` |
| `search_strategy_generation.txt` | Legacy search strategy generation | Legacy system |
| `patent_relevance_analysis.txt` | Legacy patent relevance analysis | Legacy system |
| `comprehensive_report_generation.txt` | Legacy comprehensive report generation | Legacy system |

### **Template Claims**
| File | Purpose | Used By |
|------|---------|----------|
| `template_claim_classification_system.txt` | System prompt for template claim classification | `TemplateClaimTool` |
| `template_claim_classification_user.txt` | User prompt for template claim classification | `TemplateClaimTool` |

## 🔄 **LLM Call Flow with Prompt Files**

### **1. Intent Classification (Orchestrator)**
```python
# System prompt from: intent_classification_orchestrator_system.txt
# User prompt from: intent_classification_orchestrator_user.txt
messages = [
    {
        "role": "system",
        "content": prompt_loader.load_prompt("intent_classification_orchestrator_system")
    },
    {
        "role": "user",
        "content": prompt_loader.load_prompt("intent_classification_orchestrator_user", user_input=user_input)
    }
]
```

### **2. Intent Classification (Tool)**
```python
# System prompt from: intent_analysis_system.txt
# User prompt from: intent_analysis_user.txt
# Then: intent_classification_system.txt + intent_classification_user.txt
```

### **3. Claims Drafting**
```python
# System prompt from: claims_generation_system.txt
# User prompt from: claims_generation_user.txt
```

### **4. General Conversation**
```python
# System prompt from: general_conversation_system.txt
# User prompt from: general_conversation_user.txt
```

### **5. Patent Guidance**
```python
# System prompt from: patent_guidance_system.txt
# User prompt from: patent_guidance_user.txt
```

### **6. Prior Art Search**
```python
# System prompt from: prior_art_search_system.txt
```

### **7. Template Claim Classification**
```python
# System prompt from: template_claim_classification_system.txt
# User prompt from: template_claim_classification_user.txt
```

## ✅ **Verification Status**

| Component | Status | Prompt Files Used |
|-----------|--------|-------------------|
| `AgentOrchestrator` | ✅ **COMPLETE** | `intent_classification_orchestrator_*.txt` |
| `IntentClassificationTool` | ✅ **COMPLETE** | `intent_analysis_*.txt`, `intent_classification_*.txt` |
| `ClaimDraftingTool` | ✅ **COMPLETE** | `claims_generation_*.txt` |
| `GeneralConversationTool` | ✅ **COMPLETE** | `general_conversation_*.txt` |
| `PatentGuidanceTool` | ✅ **COMPLETE** | `patent_guidance_*.txt` |
| `PriorArtSearchTool` | ✅ **COMPLETE** | `prior_art_search_system.txt` |
| `TemplateClaimTool` | ✅ **COMPLETE** | `template_claim_classification_*.txt` |
| `DisclosureAssessmentTool` | ✅ **COMPLETE** | `disclosure_assessment_*.txt` |

## 🎯 **Benefits of Externalized Prompts**

1. **Maintainability**: Prompts can be edited without touching Python code
2. **Version Control**: Prompt changes are tracked separately from code logic
3. **Testing**: Different prompt versions can be tested easily
4. **Collaboration**: Non-developers can contribute to prompt engineering
5. **Reusability**: Prompts can be shared across different functions
6. **Documentation**: Each prompt is self-documenting with clear variable names

## 📝 **Variable Substitution**

Prompts support Python string formatting with named variables. Use `{variable_name}` syntax in prompt files.

### **Common Variables:**
- `{user_input}` - User's input text
- `{conversation_context}` - Previous conversation context
- `{disclosure}` - Technical disclosure content
- `{analysis_content}` - Analysis results from previous steps
- `{context}` - Additional context information

## 🚫 **No Hardcoded Prompts**

**ALL LLM calls in the new backend now use prompt files.** This ensures:
- ✅ **Zero hardcoded prompts** in Python code
- ✅ **100% prompt file usage** for all LLM interactions
- ✅ **Consistent prompt management** across the entire system
- ✅ **Easy prompt versioning** and A/B testing

## 🔍 **Legacy System Notes**

Some prompt files (marked as "Legacy system") are kept for compatibility with the old monolithic backend. These are not used by the new modular system but are preserved for reference and potential future integration.
