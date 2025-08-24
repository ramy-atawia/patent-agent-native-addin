# Agent Prompts

This directory contains prompt templates used by the intelligent patent agent system. All prompts are externalized for easy editing and version control.

## Prompt Categories

### 1. Intent Analysis & Classification
- **intent_analysis_system.txt** - System prompt for analyzing user intent
- **intent_analysis_user.txt** - User prompt template for intent analysis
- **intent_classification_system.txt** - System prompt for intent classification
- **intent_classification_user.txt** - User prompt template for intent classification

### 2. Disclosure Assessment
- **disclosure_assessment_system.txt** - System prompt for evaluating technical content sufficiency
- **disclosure_assessment_user.txt** - User prompt template for disclosure assessment

### 3. Claims Analysis & Generation
- **claims_analysis_system.txt** - System prompt for technical analysis
- **claims_analysis_user.txt** - User prompt template for claims analysis
- **claims_generation_system.txt** - System prompt for claims generation
- **claims_generation_user.txt** - User prompt template for claims generation

### 4. Legacy Prior Art Search Prompts
- **claims_analysis.txt** - Original claims analysis prompt (prior art system)
- **comprehensive_report_generation.txt** - Report generation prompt (prior art system)
- **patent_relevance_analysis.txt** - Relevance analysis prompt (prior art system)
- **search_strategy_generation.txt** - Search strategy prompt (prior art system)

## Usage

Prompts are loaded using the `PromptLoader` class from `src/prompt_loader.py`:

```python
from src.prompt_loader import prompt_loader

# Load a simple prompt
system_prompt = prompt_loader.load_prompt("intent_analysis_system")

# Load a prompt with variables
user_prompt = prompt_loader.load_prompt("intent_analysis_user", 
    user_input="draft claims for AI",
    conversation_context="No previous conversation"
)
```

## Variable Substitution

Prompts support Python string formatting with named variables. Use `{variable_name}` syntax in prompt files.

### Common Variables:
- `{user_input}` - User's input text
- `{conversation_context}` - Previous conversation context
- `{disclosure}` - Technical disclosure content
- `{analysis_content}` - Analysis results from previous steps
- `{context_prompt}` - Additional context information

## LLM Call Flow

The agent system uses 5 distinct LLM calls for sufficient requests:

1. **Assessment** (disclosure_assessment_*) - Evaluate technical sufficiency
2. **Intent Analysis** (intent_analysis_*) - Analyze user intent
3. **Intent Classification** (intent_classification_*) - Classify intent via function call
4. **Claims Analysis** (claims_analysis_*) - Technical analysis and strategy
5. **Claims Generation** (claims_generation_*) - Generate patent claims via function call

For insufficient requests, only the Assessment call is made before early return.

---

## Legacy Prior Art Search Prompts

### 1. `search_strategy_generation.txt`
**Purpose**: Generates focused patent search strategies using PatentsView API syntax.

**Variables**:
- `{user_query}`: The user's search query (string)

**Usage**: Used by `SimplifiedQueryGenerator.generate_search_strategies()`

### 2. `patent_relevance_analysis.txt` 
**Purpose**: Analyzes patent relevance to search query and returns a JSON score.

**Variables**:
- `{search_query}`: The original search query (string)
- `{title}`: Patent title (truncated to 200 chars)
- `{abstract}`: Patent abstract (truncated to 400 chars)

**Usage**: Used by `SimplifiedPatentAnalyzer.check_relevance()`

### 3. `comprehensive_report_generation.txt`
**Purpose**: Generates comprehensive patent analysis reports with mandatory 9-section structure.

**Variables**:
- `{query}`: The search query (string)
- `{total_patents}`: Number of patents analyzed (integer)
- `{patent_inventory}`: JSON-formatted patent data with claims analysis

**Usage**: Used by `SimplifiedReportGenerator.generate_report()`

### 4. `claims_analysis.txt`
**Purpose**: Provides intelligent LLM-based analysis of patent claims for IP strategy decisions.

**Variables**:
- `{patent_title}`: The patent title (string)
- `{search_query}`: The search context/query (string)
- `{total_claims}`: Total number of claims (integer)
- `{independent_claims}`: Number of independent claims (integer)
- `{dependent_claims}`: Number of dependent claims (integer)
- `{claims_data}`: JSON-formatted claims data with text and metadata

**Usage**: Used by `SimplifiedReportGenerator._analyze_claims_with_llm()`

**Output**: JSON structure with claims summary, technical scope, key innovations, blocking potential, claim breadth, and differentiation factors.

**Variables**:
- `{query}`: The search query (string)
- `{total_patents}`: Number of patents analyzed (integer)
- `{patent_inventory}`: JSON formatted list of patent summaries with claims

**Usage**: Used by `SimplifiedReportGenerator.generate_report()`

## How It Works

The prompts are loaded using the `PromptLoader` class in `src/prompt_loader.py`:

```python
from .prompt_loader import prompt_loader

# Load and format a prompt
formatted_prompt = prompt_loader.load_prompt(
    "search_strategy_generation", 
    user_query="dynamic spectrum sharing"
)
```

## Editing Prompts

To modify prompts:

1. Edit the `.txt` files directly
2. Use `{variable_name}` syntax for placeholders
3. No code changes required - prompts are loaded dynamically
4. Cache is automatically managed

## Benefits

- ✅ **Easy to edit**: No code changes needed to modify prompts
- ✅ **Version control**: Track prompt changes separately from code  
- ✅ **Maintainable**: Clear separation of concerns
- ✅ **Reusable**: Prompts can be used in other parts of the system
- ✅ **Readable**: Much easier to read and edit large prompts

## File Structure

```
prompts/
├── README.md                           # This documentation
├── search_strategy_generation.txt      # Search strategy generation prompt
├── patent_relevance_analysis.txt       # Patent relevance scoring prompt  
└── comprehensive_report_generation.txt # Report generation prompt
```
