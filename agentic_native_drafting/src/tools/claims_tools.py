from src.interfaces import Tool
from typing import Dict, Any, AsyncGenerator
import logging

logger = logging.getLogger(__name__)

class TemplateClaimTool(Tool):
    async def run(self, claim_text: str) -> bool:
        return await self._call_llm_for_template_claim(claim_text)

    async def _call_llm_for_template_claim(self, claim_text: str) -> bool:
        from src import prompt_loader
        import json
        from src.utils.llm_client import send_llm_request_streaming

        messages = [
            {
                "role": "system",
                "content": prompt_loader.load_prompt("template_claim_classification_system")
            },
            {
                "role": "user",
                "content": prompt_loader.load_prompt("template_claim_classification_user", claim_text=claim_text)
            }
        ]

        functions = [
            {
                "type": "function",
                "function": {
                    "name": "is_template_claim",
                    "description": "Classify if claim is a template/placeholder",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "is_template": {"type": "boolean"}
                        },
                        "required": ["is_template"]
                    }
                }
            }
        ]

        async for chunk in send_llm_request_streaming(messages, functions, max_tokens=100):
            if chunk["type"] == "completion" and chunk.get("function_arguments"):
                result = json.loads(chunk["function_arguments"])
                return result["is_template"]
