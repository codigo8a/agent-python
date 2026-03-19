import logging
from typing import Dict, Any
from app.core.intent import Intent
from app.core.classifier import IntentClassifier
from app.handlers.file_handler import FileHandler
from app.handlers.system_handler import SystemHandler
from app.handlers.llm_handler import LLMHandler

logger = logging.getLogger(__name__)

class CommandRouter:
    """Class to route incoming messages using an Intent Classifier."""
    
    def __init__(self):
        self._classifier = IntentClassifier()
        self._file_handler = FileHandler()
        self._system_handler = SystemHandler()
        self._llm_handler = LLMHandler()

    async def route(self, text: str) -> str:
        """Route the message by identifying intent and delegating to handlers.
        Implements an agentic loop for LLM-driven actions.
        """
        try:
            # 1. Classify initial intent
            intent, params = self._classifier.classify(text)
            logger.info(f"Classified intent: {intent}")

            # 2. Basic routing for non-CHAT intents
            if intent in [Intent.LIST_FILES, Intent.READ_FILE, Intent.CREATE_FILE, Intent.EDIT_FILE]:
                return await self._file_handler.handle(intent, params)
            
            elif intent in [Intent.HELP, Intent.GREETING]:
                return await self._system_handler.handle(intent, params)
            
            # 3. Agentic Loop for CHAT (The AI "Agente")
            if intent == Intent.CHAT:
                response = await self._llm_handler.handle(intent, params)
                
                # Check if LLM wants to execute a tool (loop up to 3 times to avoid infinite loops)
                max_iterations = 3
                while response.startswith("/") and max_iterations > 0:
                    logger.info(f"LLM suggested action: {response}")
                    
                    # Identify the suggested command
                    tool_intent, tool_params = self._classifier.classify(response)
                    
                    if tool_intent in [Intent.LIST_FILES, Intent.READ_FILE, Intent.CREATE_FILE, Intent.EDIT_FILE]:
                        tool_result = await self._file_handler.handle(tool_intent, tool_params)
                    else:
                        tool_result = f"Error: No se pudo ejecutar el comando '{response}'."
                    
                    # Feed result back to LLM
                    logger.info(f"Feeding tool result back: {tool_result[:50]}...")
                    feedback_prompt = f"Resultado del comando {response}:\n{tool_result}\n\nAnaliza este resultado y da tu respuesta final o ejecuta otro comando si es necesario."
                    response = await self._llm_handler.handle(Intent.CHAT, {"text": feedback_prompt})
                    max_iterations -= 1
                
                return response

            return await self._system_handler.handle(Intent.UNKNOWN, params)
        except Exception as e:
            logger.error(f"Routing error: {e}", exc_info=True)
            return f"Error en el servidor: {str(e)}"
