# Agent Core package for Agentic Native Drafting
__version__ = "1.0.0"

# Import core components
from .orchestrator import AgentOrchestrator
from .api import app

__all__ = ['AgentOrchestrator', 'app']
