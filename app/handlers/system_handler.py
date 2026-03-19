from typing import Dict, Any
from app.handlers.base_handler import BaseHandler
from app.core.intent import Intent

class SystemHandler(BaseHandler):
    """Handler for system-related intents like help or greetings."""
    
    async def handle(self, intent: Intent, params: Dict[str, Any]) -> str:
        """Execute system operations based on intent."""
        if intent == Intent.HELP:
            return (
                "🤖 **Bot Modular con Rule Engine**\n\n"
                "Puedes usar los siguientes comandos:\n"
                "- `/list [ruta]` o 'listar archivos'\n"
                "- `/read [archivo]` o 'lee el archivo'\n"
                "- `/create [archivo] [contenido]` o 'crea el archivo'\n"
                "- `/edit [archivo] [viejo] [nuevo]` o 'edita el archivo'\n"
                "- `/help` o 'ayuda'\n"
            )
        elif intent == Intent.GREETING:
            return "¡Hola! Soy tu bot de gestión de archivos. ¿En qué puedo ayudarte hoy? que pasa?"
        
        return "Lo siento, no entiendo esa intención. Prueba con /help."
