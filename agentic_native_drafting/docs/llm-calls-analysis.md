# LLM Calls Analysis - Input/Output Table

This document provides a detailed breakdown of all LLM calls made in the agent system, showing inputs, outputs, and flow patterns.

## Overview

The system has two main execution paths:
- **Insufficient Details Path**: 1 LLM call (~300ms)
- **Sufficient Details Path**: 5 LLM calls (~3-5 seconds)

## Detailed LLM Calls Table

| Call # | Function | Purpose | Input | Output | Max Tokens | Uses Functions | Execution Path |
|--------|----------|---------|-------|--------|------------|----------------|----------------|
| 1 | `assess_disclosure_sufficiency()` | Evaluate if user input has enough technical content | **System**: Patent attorney prompt for technical assessment<br>**User**: User's request for evaluation | **Function Call**: `assess_technical_sufficiency`<br>- `sufficient`: boolean<br>- `confidence`: 0.0-1.0<br>- `technical_elements_found`: array<br>- `message`: string<br>- `requirements`: array | 400 | ✅ Yes | Both paths |
| 2 | `classify_user_intent_streaming()` - Analysis | Analyze user intent without function calls | **System**: Patent attorney analyzing user intent<br>**User**: User input + conversation context + available intents | **Streaming Text**: Intent reasoning and analysis | 300 | ❌ No | Sufficient only |
| 3 | `classify_user_intent_streaming()` - Classification | Classify intent based on analysis | **System**: Classify intent using function<br>**User**: Analysis content + user input | **Function Call**: `classify_user_intent`<br>- `intent`: enum value<br>- `confidence_score`: 0.0-1.0<br>- `reasoning`: string<br>- `suggested_actions`: array<br>- `requires_context`: boolean | 200 | ✅ Yes | Sufficient only |
| 4 | `draft_claims_streaming()` - Analysis | Analyze invention for claim drafting strategy | **System**: Patent attorney analyzing invention<br>**User**: Invention description + context | **Streaming Text**: Technical analysis and claim strategy | 800 | ❌ No | Sufficient only |
| 5 | `draft_claims_streaming()` - Generation | Generate actual patent claims | **System**: Draft claims using function<br>**User**: Analysis content + invention description | **Function Call**: `draft_patent_claims`<br>- `claims`: array of claim objects<br>- `summary`: string | 2000 | ✅ Yes | Sufficient only |

## Flow Analysis

### Insufficient Details Path (Fast Track)
```
User Input → LLM Call #1 (Assessment) → Insufficient Result → Early Return
Time: ~300ms | LLM Calls: 1
```

### Sufficient Details Path (Full Pipeline)
```
User Input → LLM Call #1 (Assessment) → Sufficient → 
LLM Call #2 (Intent Analysis) → LLM Call #3 (Intent Classification) → 
LLM Call #4 (Claim Analysis) → LLM Call #5 (Claim Generation) → Complete
Time: ~3-5s | LLM Calls: 5
```

## Input/Output Details

### Call #1: assess_disclosure_sufficiency()
**Input Structure:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "Patent attorney evaluation prompt with examples..."
    },
    {
      "role": "user", 
      "content": "Assess this user request: '{user_input}'"
    }
  ]
}
```

**Output Structure:**
```json
{
  "sufficient": true/false,
  "confidence": 0.85,
  "technical_elements_found": ["AI", "network optimization"],
  "message": "Response message for user",
  "requirements": ["List of additional info needed"]
}
```

### Call #2: Intent Analysis (Streaming)
**Input Structure:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "Patent attorney analyzing user intent..."
    },
    {
      "role": "user",
      "content": "User Input: '{input}' Context: '{context}' Available intents: ..."
    }
  ]
}
```

**Output:** Streaming text analysis of user intent and reasoning

### Call #3: Intent Classification
**Input Structure:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "Classify intent using function..."
    },
    {
      "role": "user",
      "content": "Based on analysis: '{analysis}' Classify: '{input}'"
    }
  ]
}
```

**Output Structure:**
```json
{
  "intent": "claim_drafting",
  "confidence_score": 0.9,
  "reasoning": "User wants patent claims for specific technology",
  "suggested_actions": ["Proceed with claim drafting"],
  "requires_context": true
}
```

### Call #4: Claims Analysis (Streaming)
**Input Structure:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "Patent attorney analyzing invention for claim drafting..."
    },
    {
      "role": "user",
      "content": "Invention: '{disclosure}' {context} Provide analysis covering: 1. Key technical elements..."
    }
  ]
}
```

**Output:** Streaming technical analysis and claim strategy

### Call #5: Claims Generation
**Input Structure:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "Draft claims using function..."
    },
    {
      "role": "user",
      "content": "Based on analysis: '{analysis}' Draft claims for: '{disclosure}'"
    }
  ]
}
```

**Output Structure:**
```json
{
  "claims": [
    {
      "claim_number": 1,
      "claim_text": "A method comprising...",
      "claim_type": "independent",
      "dependency": null
    }
  ],
  "summary": "Claims summary description"
}
```

## Performance Characteristics

| Metric | Insufficient Path | Sufficient Path |
|--------|-------------------|-----------------|
| **LLM Calls** | 1 | 5 |
| **Response Time** | ~300ms | ~3-5 seconds |
| **Token Usage** | ~400 tokens | ~3,700 tokens |
| **Use Case** | Missing technical details | Complete claim drafting |

## Redundancy Issue Identified

**Problem**: `assess_disclosure_sufficiency()` is called twice for sufficient requests:
1. Once in `agent_run_streaming()` for early detection
2. Once again in `draft_claims_streaming()` (redundant)

**Impact**: Extra ~300ms and 400 tokens for sufficient requests

**Optimization Opportunity**: Remove the redundant call in `draft_claims_streaming()` since assessment already passed in the main flow.

## System Architecture Benefits

1. **Early Return Pattern**: Efficiently handles insufficient requests without unnecessary processing
2. **Streaming Responses**: Provides real-time feedback to users during long operations
3. **Function-Based Outputs**: Structured data for consistent parsing and validation
4. **Separation of Concerns**: Analysis and generation steps are clearly separated
5. **Pure LLM Assessment**: No fallback logic, relies entirely on AI evaluation

## Token Efficiency

- **Assessment**: 400 tokens (function call)
- **Intent Analysis**: 300 tokens (streaming text)
- **Intent Classification**: 200 tokens (function call)
- **Claims Analysis**: 800 tokens (streaming text)
- **Claims Generation**: 2000 tokens (function call)
- **Total for Full Pipeline**: ~3,700 tokens
