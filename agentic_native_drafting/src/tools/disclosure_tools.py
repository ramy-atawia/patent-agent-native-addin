from src.interfaces import Tool
from typing import Dict, Any, AsyncGenerator
import logging

logger = logging.getLogger(__name__)

class DisclosureAssessmentTool(Tool):
    async def run(self, disclosure: str, context: str = "") -> AsyncGenerator[Dict[str, Any], None]:
        from src import prompt_loader
        from src.utils.llm_client import send_llm_request_streaming

        assessment_messages = [
            {
                "role": "system",
                "content": prompt_loader.load_prompt("disclosure_assessment_system")
            },
            {
                "role": "user",
                "content": prompt_loader.load_prompt("disclosure_assessment_user", disclosure=disclosure)
            }
        ]

        functions = [
            {
                "type": "function",
                "function": {
                    "name": "assess_technical_sufficiency",
                    "description": "Assess if disclosure has sufficient technical content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sufficient": {"type": "boolean"},
                            "confidence": {"type": "number", "minimum": 0.0, "maximum": 1.0},
                            "technical_elements_found": {"type": "array", "items": {"type": "string"}},
                            "message": {"type": "string"},
                            "requirements": {"type": "array", "items": {"type": "string"}}
                        },
                        "required": ["sufficient", "confidence", "technical_elements_found", "message"]
                    }
                }
            }
        ]

        async for chunk in send_llm_request_streaming(assessment_messages, functions, max_tokens=400):
            if chunk["type"] == "completion" and chunk.get("function_arguments"):
                result = json.loads(chunk["function_arguments"])
                return result
