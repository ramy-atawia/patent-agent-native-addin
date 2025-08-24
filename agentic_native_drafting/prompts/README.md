# Patent Search Prompts

This folder contains the LLM prompts used by the patent search system, extracted from the main code for better maintainability.

## Available Prompts

### 1. `search_strategy_generation.txt`
**Purpose**: Generates focused patent search strategies using PatentsView API syntax.

**Variables**:
- `{user_query}`: The user's search query (string)

**Usage**: Used by `SimplifiedQueryGenerator.generate_search_strategies()`

---

### 2. `patent_relevance_analysis.txt` 
**Purpose**: Analyzes patent relevance to search query and returns a JSON score.

**Variables**:
- `{search_query}`: The original search query (string)
- `{title}`: Patent title (truncated to 200 chars)
- `{abstract}`: Patent abstract (truncated to 400 chars)

**Usage**: Used by `SimplifiedPatentAnalyzer.check_relevance()`

---

### 3. `comprehensive_report_generation.txt`
**Purpose**: Generates comprehensive patent analysis reports with mandatory 9-section structure.

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
