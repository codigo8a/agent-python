import logging
from typing import Dict, Any
from app.core.intent import Intent
from app.core.classifier import IntentClassifier
from app.handlers.file_handler import FileHandler
from app.handlers.system_handler import SystemHandler

logger = logging.getLogger(__name__)

class CommandRouter:
    """Class to route incoming messages using an Intent Classifier."""
    
    def __init__(self):
        self._classifier = IntentClassifier()
        self._file_handler = FileHandler()
        self._system_handler = SystemHandler()

    async def route(self, text: str) -> str:
        """Route the message by identifying intent and delegating to handlers."""
        try:
            # 1. Classify intent
            intent, params = self._classifier.classify(text)
            logger.info(f"Classified intent: {intent} with params: {params}")

            # 2. Route to appropriate handler
            if intent in [Intent.LIST_FILES, Intent.READ_FILE, Intent.CREATE_FILE, Intent.EDIT_FILE]:
                return await self._file_handler.handle(intent, params)
            
            elif intent in [Intent.HELP, Intent.GREETING, Intent.UNKNOWN]:
                return await self._system_handler.handle(intent, params)

            return "Lo siento, hubo un error interno en el enrutamiento."
        except Exception as e:
            logger.error(f"Routing error: {e}", exc_info=True)
            return f"Error en el servidor: {str(e)}"
