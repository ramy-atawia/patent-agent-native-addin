# 🔄 **USER INPUT FLOW DIAGRAM**

## **Complete System Flow Visualization**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           🚀 USER INPUT RECEPTION                                  │
│                                                                                     │
│  User types: "I want to draft patent claims for a wireless communication system"   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📱 FRONTEND (Word Add-in)                               │   │
│  │                                                                             │   │
│  │  • ChatBot.tsx receives user input                                         │   │
│  │  • Forms ChatRequest object                                                │   │
│  │  • Calls apiService.chatStream()                                           │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🌐 API SERVICE PROCESSING                                   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📡 api.ts: chatStream()                                  │   │
│  │                                                                             │   │
│  │  1. startPatentRun(request) → POST /api/patent/run                         │   │
│  │  2. fetch stream → GET /api/patent/stream?run_id={run_id}                  │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🎯 BACKEND API RECEPTION                                   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📥 api.py: start_patent_run_frontend()                  │   │
│  │                                                                             │   │
│  │  • Receives FrontendChatRequest                                            │   │
│  │  • Creates session via session_manager.create_session()                    │   │
│  │  • Creates run via session_manager.create_run()                            │   │
│  │  • Returns: {"run_id": "run-456", "session_id": "abc-123"}                 │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🔄 STREAMING INITIATION                                    │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📡 api.py: stream_patent_response()                      │   │
│  │                                                                             │   │
│  │  • Retrieves run data from session_manager.get_run(run_id)                 │   │
│  │  • Updates run status to "processing"                                      │   │
│  │  • Calls orchestrator.handle() with stored context                         │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🎯 ORCHESTRATOR PROCESSING                                 │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🧠 orchestrator.py: handle()                            │   │
│  │                                                                             │   │
│  │  1. Update conversation memory                                              │   │
│  │  2. Yield initialization event                                              │   │
│  │  3. Yield intent analysis event                                            │   │
│  │  4. Call _get_llm_based_intent()                                           │   │
│  │  5. Route to appropriate tool                                               │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🤖 LLM INTENT CLASSIFICATION                               │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🎯 _get_llm_based_intent()                              │   │
│  │                                                                             │   │
│  │  Input: "I want to draft patent claims for a wireless communication system" │   │
│  │                                                                             │   │
│  │  LLM Analysis:                                                             │   │
│  │  • Keywords: "draft", "patent claims", "wireless communication"            │   │
│  │  • Intent: "content_drafting"                                              │   │
│  │  • Confidence: 0.95                                                        │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🛣️ TOOL ROUTING DECISION                                   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🎯 _get_tool_name_for_intent()                          │   │
│  │                                                                             │   │
│  │  intent_to_tool = {                                                         │   │
│  │    "content_drafting": "ContentDraftingTool",                              │   │
│  │    "content_review": "ContentReviewTool",                                   │   │
│  │    "search": "PriorArtSearchTool",                                          │   │
│  │    "guidance": "GeneralGuidanceTool",                                       │   │
│  │    "general_conversation": "GeneralConversationTool"                        │   │
│  │  }                                                                          │   │
│  │                                                                             │   │
│  │  Result: "ContentDraftingTool"                                              │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┐
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🛠️ TOOL EXECUTION                                         │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🏗️ ContentDraftingTool.run()                            │   │
│  │                                                                             │   │
│  │  1. Input sufficiency assessment                                            │   │
│  │     • Call _assess_input_sufficiency()                                      │   │
│  │     • LLM analyzes input quality                                            │   │
│  │                                                                             │   │
│  │  2. Content generation                                                      │   │
│  │     • Call _draft_content_with_llm()                                        │   │
│  │     • LLM generates patent claims                                           │   │
│  │                                                                             │   │
│  │  3. Response formatting                                                     │   │
│  │     • Call _format_response()                                               │   │
│  │     • Structure output for frontend                                         │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        📤 RESPONSE STREAMING BACK                                 │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📡 Streaming Events Back to Frontend                    │   │
│  │                                                                             │   │
│  │  1. Initialization event                                                   │   │
│  │  2. Intent analysis event                                                  │   │
│  │  3. Tool routing event                                                     │   │
│  │  4. Tool execution event                                                   │   │
│  │  5. Results event                                                          │   │
│  │                                                                             │   │
│  │  Format: Server-Sent Events (SSE)                                          │   │
│  │  • event: {event_type}                                                     │   │
│  │  • data: {JSON_data}                                                       │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        📱 FRONTEND RECEPTION & DISPLAY                            │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📱 Frontend Event Processing                            │   │
│  │                                                                             │   │
│  │  1. Receive SSE events                                                     │   │
│  │  2. Process each event type                                                │   │
│  │  3. Update UI in real-time                                                 │   │
│  │  4. Display final results                                                  │   │
│  │                                                                             │   │
│  │  Event Types:                                                              │   │
│  │  • thoughts: Show processing steps                                         │   │
│  │  • results: Display final output                                           │   │
│  │  • error: Show error messages                                              │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## **🔍 DETAILED INTENT CLASSIFICATION FLOW**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🤖 LLM INTENT CLASSIFICATION DETAILED FLOW                  │
│                                                                                     │
│  User Input: "I want to draft patent claims for a wireless communication system"   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📝 Prompt Construction                                  │   │
│  │                                                                             │   │
│  │  System Prompt: intent_classification_orchestrator_system                  │   │
│  │  User Prompt: intent_classification_orchestrator_user                      │   │
│  │                                                                             │   │
│  │  Variables:                                                                 │   │
│  │  • user_input: "I want to draft patent claims..."                         │   │
│  │  • context: "patent_streaming"                                             │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                          │
│                                        ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🎯 Function Schema Definition                           │   │
│  │                                                                             │   │
│  │  functions = [{                                                             │   │
│  │    "type": "function",                                                     │   │
│  │    "function": {                                                            │   │
│  │      "name": "classify_intent",                                            │   │
│  │      "parameters": {                                                        │   │
│  │        "properties": {                                                      │   │
│  │          "intent": {                                                        │   │
│  │            "type": "string",                                                │   │
│  │            "enum": ["content_drafting", "content_review", "search",         │   │
│  │                     "guidance", "analysis", "query",                       │   │
│  │                     "general_conversation"]                                │   │
│  │          },                                                                 │   │
│  │          "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0}, │   │
│  │          "reasoning": {"type": "string"}                                    │   │
│  │        }                                                                    │   │
│  │      }                                                                      │   │
│  │    }                                                                        │   │
│  │  }]                                                                         │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                          │
│                                        ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🤖 LLM Analysis & Response                              │   │
│  │                                                                             │   │
│  │  LLM Analysis:                                                             │   │
│  │  • Keywords identified: "draft", "patent claims", "wireless"               │   │
│  │  • Context: Patent-related request                                         │   │
│  │  • Action: Content creation                                                │   │
│  │                                                                             │   │
│  │  LLM Response:                                                             │   │
│  │  {                                                                          │   │
│  │    "intent": "content_drafting",                                           │   │
│  │    "confidence": 0.95,                                                     │   │
│  │    "reasoning": "User explicitly requests to draft patent claims..."       │   │
│  │  }                                                                          │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                          │
│                                        ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    ✅ Intent Classification Result                          │   │
│  │                                                                             │   │
│  │  Return: ("content_drafting", 0.95)                                        │   │
│  │                                                                             │   │
│  │  Confidence Level: HIGH (0.9 - 1.0)                                        │   │
│  │  Action: Proceed with ContentDraftingTool                                  │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## **🛠️ TOOL EXECUTION FLOW**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🛠️ CONTENT DRAFTING TOOL EXECUTION FLOW                    │
│                                                                                     │
│  Tool: ContentDraftingTool                                                        │
│  Input: "I want to draft patent claims for a wireless communication system"       │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📊 Phase 1: Input Assessment                             │   │
│  │                                                                             │   │
│  │  Method: _assess_input_sufficiency()                                        │   │
│  │                                                                             │   │
│  │  LLM Assessment:                                                            │   │
│  │  • Sufficiency Score: 0.3 (Low - needs more details)                       │   │
│  │  • Strengths: Clear intent expressed                                        │   │
│  │  • Areas for Improvement: Input too brief, missing technical details       │   │
│  │  • Recommendations: Provide more detailed description, include technical    │   │
│  │    concepts                                                                  │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                          │
│                                        ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🏗️ Phase 2: Content Generation                           │   │
│  │                                                                             │   │
│  │  Method: _draft_content_with_llm()                                          │   │
│  │                                                                             │   │
│  │  LLM Prompt: claims_generation_system + claims_generation_user             │   │
│  │                                                                             │   │
│  │  Variables:                                                                 │   │
│  │  • disclosure: User input                                                   │   │
│  │  • max_claims: 20                                                           │   │
│  │  • claim_types: "primary, secondary"                                       │   │
│  │  • focus_areas: "wireless_communication"                                   │   │
│  │                                                                             │   │
│  │  LLM Response:                                                              │   │
│  │  {                                                                          │   │
│  │    "content": [                                                             │   │
│  │      {                                                                      │   │
│  │        "content_number": "1",                                               │   │
│  │        "content_text": "A method for optimizing handover...",               │   │
│  │        "content_type": "primary",                                           │   │
│  │        "dependency": null,                                                  │   │
│  │        "focus_area": "wireless_communication"                               │   │
│  │      }                                                                      │   │
│  │    ],                                                                       │   │
│  │    "reasoning": "Based on the user's request...",                           │   │
│  │    "input_assessment": {...}                                                │   │
│  │  }                                                                          │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                          │
│                                        ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    📝 Phase 3: Response Formatting                          │   │
│  │                                                                             │   │
│  │  Method: _format_response()                                                 │   │
│  │                                                                             │   │
│  │  Output Structure:                                                          │   │
│  │  {                                                                          │   │
│  │    "content": [generated content items],                                    │   │
│  │    "reasoning": "Content drafted based on input",                           │   │
│  │    "input_assessment": assessment results,                                  │   │
│  │    "metadata": {                                                            │   │
│  │      "input_length": 25,                                                    │   │
│  │      "outputs_generated": 1,                                                │   │
│  │      "timestamp": "2025-01-27T00:48:05"                                    │   │
│  │    }                                                                        │   │
│  │  }                                                                          │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## **📊 CONFIDENCE SCORING MATRIX**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        🎯 CONFIDENCE SCORING & TOOL SELECTION                      │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🟢 HIGH CONFIDENCE (0.9 - 1.0)                          │   │
│  │                                                                             │   │
│  │  Examples:                                                                  │   │
│  │  • "Draft patent claims for wireless charging system"                      │   │
│  │  • "Review my patent specification for completeness"                       │   │
│  │  • "Search for prior art in machine learning"                              │   │
│  │                                                                             │   │
│  │  Action: Use primary tool immediately                                       │   │
│  │  Fallback: None needed                                                      │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🟡 MEDIUM CONFIDENCE (0.7 - 0.89)                       │   │
│  │                                                                             │   │
│  │  Examples:                                                                  │   │
│  │  • "I need help creating claims for my invention"                          │   │
│  │  • "Can you analyze my patent draft?"                                      │   │
│  │  • "Help me find similar patents"                                          │   │
│  │                                                                             │   │
│  │  Action: Use primary tool with enhanced guidance                            │   │
│  │  Fallback: Provide clarification prompts                                    │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🟠 LOW CONFIDENCE (0.5 - 0.69)                          │   │
│  │                                                                             │   │
│  │  Examples:                                                                  │   │
│  │  • "I have an invention, what should I do?"                                │   │
│  │  • "Can you help me with my patent?"                                       │   │
│  │  • "I need assistance"                                                      │   │
│  │                                                                             │   │
│  │  Action: Use guidance tool with clarification questions                     │   │
│  │  Fallback: General conversation tool                                        │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🔴 VERY LOW CONFIDENCE (< 0.5)                          │   │
│  │                                                                             │   │
│  │  Examples:                                                                  │   │
│  │  • "Hello"                                                                  │   │
│  │  • "Help"                                                                   │   │
│  │  • "What is this?"                                                          │   │
│  │                                                                             │   │
│  │  Action: Use general conversation tool                                      │   │
│  │  Fallback: Welcome message + help menu                                      │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## **🔄 ERROR HANDLING & FALLBACK FLOW**

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        ❌ ERROR HANDLING & FALLBACK STRATEGIES                     │
│                                                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🔄 Primary Tool Failure                                  │   │
│  │                                                                             │   │
│  │  Error: ContentDraftingTool fails                                          │   │
│  │  Action: Try alternative tool                                               │   │
│  │  Fallback: GeneralConversationTool                                          │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                          │
│                                        ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🤖 LLM Classification Failure                            │   │
│  │                                                                             │   │
│  │  Error: LLM intent classification fails                                    │   │
│  │  Action: Use keyword-based fallback                                         │   │
│  │  Fallback: Pattern matching on keywords                                     │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                          │
│                                        ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    🛠️ Tool Not Found                                        │   │
│  │                                                                             │   │
│  │  Error: Requested tool doesn't exist                                        │   │
│  │  Action: Use GeneralConversationTool                                        │   │
│  │  Fallback: Provide tool list + guidance                                     │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                          │
│                                        ▼                                          │
│  ┌─────────────────────────────────────────────────────────────────────────────┐   │
│  │                    💥 Critical System Error                                 │   │
│  │                                                                             │   │
│  │  Error: System-level failure                                                │   │
│  │  Action: Return error event                                                 │   │
│  │  Fallback: Suggest restart + contact support                                │   │
│  │                                                                             │   │
│  └─────────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

This comprehensive flow diagram shows exactly how user input flows through the system, gets classified, routed to appropriate tools, and returns results! 🚀
