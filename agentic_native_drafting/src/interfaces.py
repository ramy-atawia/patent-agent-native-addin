from abc import ABC, abstractmethod
from typing import Any, Dict, AsyncGenerator

class Tool(ABC):
    @abstractmethod
    async def run(self, *args, **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Run the atomic tool operation.
        
        Yields:
            Streaming events in standardized format:
            - thoughts: AI reasoning and progress
            - results: Final completed results
            - error: Error states
            - low_confidence: When AI needs clarification
        """
        pass

class Chain(ABC):
    @abstractmethod
    async def execute(self, *args, **kwargs) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Execute the workflow, yielding streaming results.
        
        Yields:
            Streaming events in standardized format:
            - thoughts: Workflow progress and reasoning
            - results: Final completed results
            - error: Error states
            - low_confidence: When AI needs clarification
        """
        pass

class Agent(ABC):
    @abstractmethod
    async def handle(self, user_input: str, context: str = "") -> AsyncGenerator[Dict[str, Any], None]:
        """
        Main agent orchestration entrypoint.
        
        Yields:
            Streaming events in standardized format:
            - thoughts: Intent analysis and routing
            - results: Final completed results
            - error: Error states
            - low_confidence: When AI needs clarification
        """
        pass
