from typing import Dict, Any
from app.handlers.base_handler import BaseHandler
from app.services.llm_service import LLMService

class LLMHandler(BaseHandler):
    """Handler for LLM-powered chat."""
    
    def __init__(self):
        self._llm_service = LLMService()

    async def handle(self, intent, params: Dict[str, Any]) -> str:
        """Process the text through the LLM."""
        prompt = params.get("text", "")
        if not prompt:
            return "Dime algo para conversar."
            
        return await self._llm_service.get_response(prompt)
