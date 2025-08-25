from src.interfaces import Tool
from typing import Tuple

class IntentClassificationTool(Tool):
    async def run(self, user_input: str, conversation_context: str = "") -> dict:
        return await self._llm_intent_classification(user_input, conversation_context)

    async def _llm_intent_classification(self, user_input: str, conversation_context: str = "") -> dict:
        from .. import prompt_loader
        import json
        from ..agent import send_llm_request_streaming

        # Step 1: LLM-based analysis
        analysis_messages = [
            {
                "role": "system",
                "content": prompt_loader.load_prompt("intent_analysis_system")
            },
            {
                "role": "user",
                "content": prompt_loader.load_prompt("intent_analysis_user", user_input=user_input, conversation_context=conversation_context if conversation_context else "No previous conversation")
            }
        ]
        analysis_content = ""
        buffer = ""
        async for chunk in send_llm_request_streaming(analysis_messages, max_tokens=300):
            if chunk["type"] == "content_chunk":
                buffer += chunk["content"]
                if chunk["content"].endswith(('.', '!', '?', '\n')):
                    if buffer.strip():
                        analysis_content += buffer
                        buffer = ""
            elif chunk["type"] == "completion":
                if buffer.strip():
                    analysis_content += buffer
                    buffer = ""

        # Step 2: LLM-based classification
        classification_messages = [
            {
                "role": "system",
                "content": prompt_loader.load_prompt("intent_classification_system")
            },
            {
                "role": "user",
                "content": prompt_loader.load_prompt("intent_classification_user", analysis_content=analysis_content, user_input=user_input)
            }
        ]
        # You may need to import or define get_intent_classification_functions
        from ..agent import get_intent_classification_functions
        functions = get_intent_classification_functions()
        async for chunk in send_llm_request_streaming(classification_messages, functions, max_tokens=200):
            if chunk["type"] == "completion" and chunk.get("function_arguments"):
                result = json.loads(chunk["function_arguments"])
                return {
                    "intent": result["intent"],
                    "confidence": result["confidence_score"],
                    "reasoning": result["reasoning"],
                    "suggested_actions": result["suggested_actions"]
                }
        
        # If LLM classification fails, raise error
        raise ValueError("LLM intent classification failed")
