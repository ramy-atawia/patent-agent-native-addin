#!/usr/bin/env python3
"""
Self-contained LLM client for the new backend.
No dependencies on legacy agent.py, main.py, or prior_art_search.py
"""

import os
import json
import asyncio
import httpx
import logging
from typing import AsyncGenerator, Dict, Any, List, Optional
from datetime import datetime

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not available, use system environment variables

logger = logging.getLogger(__name__)

class LLMClient:
    """Self-contained LLM client for Azure OpenAI"""
    
    def __init__(self):
        self.endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
        
        if not all([self.endpoint, self.api_key, self.deployment_name]):
            raise ValueError("Missing Azure OpenAI configuration. Check environment variables.")
    
    async def send_request_streaming(
        self, 
        messages: List[Dict], 
        functions: Optional[List[Dict]] = None, 
        max_tokens: int = 8000  # Increased for longer patent claims
    ) -> AsyncGenerator[Dict, None]:
        """Send streaming request to Azure OpenAI"""
        
        url = f"{self.endpoint}/openai/deployments/{self.deployment_name}/chat/completions?api-version={self.api_version}"
        
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key
        }
        
        payload = {
            "messages": messages,
            "max_tokens": max_tokens,  # Use max_tokens instead of max_completion_tokens
            "temperature": 0.0,
            "stream": True
        }
        
        if functions:
            payload["tools"] = functions
            payload["tool_choice"] = "auto"
        
        try:
            async with httpx.AsyncClient(timeout=120) as client:  # Increased timeout for longer responses
                async with client.stream("POST", url, headers=headers, json=payload) as response:
                    response.raise_for_status()
                    
                    content_buffer = ""
                    function_call_buffer = ""
                    
                    async for line in response.aiter_lines():
                        if line.startswith("data: "):
                            data_str = line[6:]
                            
                            if data_str.strip() == "[DONE]":
                                break
                            
                            try:
                                data = json.loads(data_str)
                                
                                if "choices" in data and len(data["choices"]) > 0:
                                    choice = data["choices"][0]
                                    delta = choice.get("delta", {})
                                    
                                    # Handle content streaming
                                    if "content" in delta and delta["content"]:
                                        chunk = delta["content"]
                                        content_buffer += chunk
                                        
                                        yield {
                                            "type": "content_chunk",
                                            "content": chunk,
                                            "full_content": content_buffer
                                        }
                                    
                                    # Handle function calls
                                    if "tool_calls" in delta:
                                        for tool_call in delta["tool_calls"]:
                                            if "function" in tool_call:
                                                func = tool_call["function"]
                                                if "name" in func:
                                                    yield {
                                                        "type": "function_call",
                                                        "function_name": func["name"]
                                                    }
                                                if "arguments" in func:
                                                    function_call_buffer += func["arguments"]
                                                        
                                    # Check for completion
                                    if choice.get("finish_reason"):
                                        yield {
                                            "type": "completion",
                                            "finish_reason": choice["finish_reason"],
                                            "full_content": content_buffer,
                                            "function_arguments": function_call_buffer
                                        }
                                        break
                                        
                            except json.JSONDecodeError:
                                continue
                                
        except Exception as e:
            logger.error(f"LLM request failed: {e}")
            raise e

# Global LLM client instance
llm_client = LLMClient()

async def send_llm_request_streaming(
    messages: List[Dict], 
    functions: Optional[List[Dict]] = None, 
    max_tokens: int = 8000  # Increased for longer patent claims
) -> AsyncGenerator[Dict, None]:
    """Global function for LLM requests (maintains compatibility)"""
    async for chunk in llm_client.send_request_streaming(messages, functions, max_tokens):
        yield chunk
