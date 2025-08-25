"""
Response Standardizer Utility

This module provides utilities to standardize tool responses to match the existing
streaming event format expected by main.py and the frontend.
"""

from typing import Dict, Any, AsyncGenerator, List, Optional
from datetime import datetime
import json

class ResponseStandardizer:
    """
    Standardizes tool responses to match the existing streaming event format.
    
    Expected event types from main.py:
    - thoughts: AI reasoning and progress
    - results: Final completed results  
    - error: Error states
    - low_confidence: When AI needs clarification
    """
    
    @staticmethod
    def create_thought_event(content: str, thought_type: str = "processing", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a standardized thought event"""
        return {
            "event": "thoughts",
            "content": content,
            "thought_type": thought_type,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def create_progress_event(content: str, step: str, progress: float = 0.0, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a standardized progress event"""
        return {
            "event": "thoughts",
            "content": content,
            "thought_type": "progress",
            "step": step,
            "progress": progress,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def create_results_event(response: str, metadata: Dict[str, Any] = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a standardized results event"""
        return {
            "event": "results",
            "response": response,
            "metadata": metadata or {},
            "data": data or {},
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def create_error_event(error: str, context: str = "tool_error", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a standardized error event"""
        return {
            "event": "error",
            "error": error,
            "context": context,
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def create_low_confidence_event(text: str, confidence: float, suggestions: List[str] = None, metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a standardized low confidence event"""
        return {
            "event": "low_confidence",
            "text": text,
            "confidence": confidence,
            "suggestions": suggestions or [],
            "metadata": metadata or {},
            "timestamp": datetime.now().isoformat()
        }
    
    @staticmethod
    def convert_tool_response_to_streaming(tool_response: Dict[str, Any], tool_name: str) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Convert a tool response to streaming events.
        
        Args:
            tool_response: The tool's response dictionary
            tool_name: Name of the tool for context
        
        Yields:
            Streaming events in the expected format
        """
        try:
            # Check if it's an error response
            if tool_response.get("status") == "error":
                yield ResponseStandardizer.create_error_event(
                    error=tool_response.get("error", "Unknown error"),
                    context=f"{tool_name}_error",
                    metadata={"tool_name": tool_name}
                )
                return
            
            # Check if it's a success response
            if tool_response.get("status") == "success":
                # Extract the main response content
                response_content = tool_response.get("response", "")
                if not response_content:
                    # Try to construct response from available data
                    if "claims" in tool_response:
                        claims = tool_response["claims"]
                        if claims:
                            response_content = f"Successfully processed with {len(claims)} claims generated."
                        else:
                            response_content = "Processing completed successfully."
                    else:
                        response_content = "Processing completed successfully."
                
                # Create metadata
                metadata = {
                    "tool_name": tool_name,
                    "tool_status": "success",
                    "timestamp": tool_response.get("metadata", {}).get("timestamp", datetime.now().isoformat())
                }
                
                # Add tool-specific data
                data = {}
                for key in ["claims", "assessment", "analysis", "recommendations"]:
                    if key in tool_response:
                        data[key] = tool_response[key]
                
                # Add metadata from tool response
                if "metadata" in tool_response:
                    metadata.update(tool_response["metadata"])
                
                yield ResponseStandardizer.create_results_event(
                    response=response_content,
                    metadata=metadata,
                    data=data
                )
            else:
                # Unknown status, treat as error
                yield ResponseStandardizer.create_error_event(
                    error=f"Unknown response status: {tool_response.get('status', 'unknown')}",
                    context=f"{tool_name}_unknown_status",
                    metadata={"tool_name": tool_name, "response": tool_response}
                )
                
        except Exception as e:
            yield ResponseStandardizer.create_error_event(
                error=f"Error converting tool response: {str(e)}",
                context=f"{tool_name}_conversion_error",
                metadata={"tool_name": tool_name, "original_response": tool_response}
            )
    
    @staticmethod
    async def create_workflow_progress_stream(
        steps: List[str], 
        current_step: int = 0,
        tool_name: str = "workflow"
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Create a standardized workflow progress stream.
        
        Args:
            steps: List of step descriptions
            current_step: Current step index (0-based)
            tool_name: Name of the tool/workflow
        
        Yields:
            Progress events for each step
        """
        total_steps = len(steps)
        
        for i, step_description in enumerate(steps):
            if i < current_step:
                continue
                
            progress = (i / total_steps) * 100 if total_steps > 0 else 0
            
            yield ResponseStandardizer.create_progress_event(
                content=f"Step {i+1}/{total_steps}: {step_description}",
                step=f"step_{i+1}",
                progress=progress,
                metadata={
                    "tool_name": tool_name,
                    "current_step": i + 1,
                    "total_steps": total_steps,
                    "step_description": step_description
                }
            )
            
            # Simulate some processing time
            await asyncio.sleep(0.1)
        
        # Final completion event
        yield ResponseStandardizer.create_results_event(
            response=f"Workflow completed successfully with {total_steps} steps",
            metadata={
                "tool_name": tool_name,
                "total_steps": total_steps,
                "status": "completed"
            }
        )

# Convenience functions for easy import
def create_thought_event(content: str, thought_type: str = "processing", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    return ResponseStandardizer.create_thought_event(content, thought_type, metadata)

def create_results_event(response: str, metadata: Dict[str, Any] = None, data: Dict[str, Any] = None) -> Dict[str, Any]:
    return ResponseStandardizer.create_results_event(response, metadata, data)

def create_error_event(error: str, context: str = "tool_error", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
    return ResponseStandardizer.create_error_event(error, context, metadata)

def convert_tool_response_to_streaming(tool_response: Dict[str, Any], tool_name: str) -> AsyncGenerator[Dict[str, Any], None]:
    return ResponseStandardizer.convert_tool_response_to_streaming(tool_response, tool_name)
