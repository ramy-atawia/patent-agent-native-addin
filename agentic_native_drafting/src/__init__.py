# Source package for Agentic Native Drafting
__version__ = "1.0.0"

# Import key components to make them available at package level
from . import prompt_loader
from . import interfaces

# Make prompt_loader available for easy access
__all__ = ['prompt_loader', 'interfaces']
