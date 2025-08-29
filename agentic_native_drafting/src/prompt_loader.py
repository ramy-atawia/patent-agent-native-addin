"""
Simple Prompt Loader Utility

Loads prompt templates from text files and provides variable substitution.
"""

import os
from typing import Dict, Any
from pathlib import Path

class PromptLoader:
    """Simple utility to load and format prompt templates"""
    
    def __init__(self, prompts_dir: str = None):
        """Initialize with prompts directory path"""
        if prompts_dir is None:
            # Default to prompts folder relative to the parent of this file's directory
            current_dir = Path(__file__).parent
            self.prompts_dir = current_dir.parent / "prompts"
        else:
            self.prompts_dir = Path(prompts_dir)
        
        self._cache = {}
    
    def load_prompt(self, prompt_name: str, **variables) -> str:
        """
        Load and format a prompt template with variables
        
        Args:
            prompt_name: Name of the prompt file (without .txt extension)
            **variables: Variables to substitute in the template
            
        Returns:
            Formatted prompt string
        """
        # Get template from cache or load from file
        template = self._get_template(prompt_name)
        
        # Format with variables
        try:
            return template.format(**variables)
        except KeyError as e:
            raise ValueError(f"Missing required variable {e} for prompt '{prompt_name}'")
    
    def _get_template(self, prompt_name: str) -> str:
        """Get template from cache or load from file"""
        if prompt_name not in self._cache:
            file_path = self.prompts_dir / f"{prompt_name}.txt"
            
            if not file_path.exists():
                raise FileNotFoundError(f"Prompt file not found: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self._cache[prompt_name] = f.read()
        
        return self._cache[prompt_name]
    
    def list_available_prompts(self) -> list:
        """List all available prompt files"""
        if not self.prompts_dir.exists():
            return []
        
        return [f.stem for f in self.prompts_dir.glob("*.txt")]
    
    def clear_cache(self):
        """Clear the template cache"""
        self._cache.clear()

# Convenience instance for easy import

prompt_loader = PromptLoader()

def load_prompt(prompt_name: str, **variables) -> str:
    """
    Top-level convenience function for agent and LangChain compatibility.
    """
    return prompt_loader.load_prompt(prompt_name, **variables)
