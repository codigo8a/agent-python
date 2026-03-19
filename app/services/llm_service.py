import httpx
import logging
from app.config import Config

logger = logging.getLogger(__name__)

class LLMService:
    """Service to interact with OpenRouter API."""
    
    def __init__(self):
        self._api_key = Config.OPENROUTER_API_KEY
        self._api_url = "https://openrouter.ai/api/v1/chat/completions"
        self._model = "openrouter/free" # Automatic routing for free models

    async def get_response(self, prompt: str) -> str:
        """Get a completion from OpenRouter."""
        if not self._api_key:
            return "Error: OpenRouter API key not configured."

        headers = {
            "Authorization": f"Bearer {self._api_key}",
            "HTTP-Referer": "https://github.com/codigo8a/agent-python", # Required by OpenRouter
            "X-Title": "Telegram Agent Bot",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self._model,
            "messages": [
                {
                    "role": "system", 
                    "content": (
                        "Eres un Agente de Inteligencia Artificial capaz de gestionar archivos en este servidor.\n"
                        "Tienes acceso a las siguientes herramientas/comandos que debes usar para ayudar al usuario:\n\n"
                        "1. `/list [ruta]` - Lista archivos y carpetas. Úsalo si no conoces la estructura del proyecto.\n"
                        "2. `/read [archivo]` - Lee el contenido de un archivo. Úsalo para entender el código.\n"
                        "3. `/create [archivo] [contenido]` - Crea un nuevo archivo.\n"
                        "4. `/edit [archivo] [buscar] [reemplazar]` - Edita un archivo reemplazando texto.\n\n"
                        "INSTRUCCIONES DE RESPUESTA:\n"
                        "- Si necesitas información que no tienes (ej. ver qué archivos hay), responde ÚNICAMENTE con el comando.\n"
                        "- Si ya tienes la información necesaria, responde de forma natural al usuario.\n"
                        "- SIEMPRE responde en español."
                    )
                },
                {"role": "user", "content": prompt}
            ]
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self._api_url,
                    headers=headers,
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                
                if "choices" in data and len(data["choices"]) > 0:
                    return data["choices"][0]["message"]["content"]
                else:
                    logger.error(f"Unexpected OpenRouter response: {data}")
                    return "Error: No se recibió una respuesta válida del modelo."
                    
        except httpx.HTTPStatusError as e:
            logger.error(f"OpenRouter API error: {e.response.text}")
            return f"Error de la API de OpenRouter: {e.response.status_code}"
        except Exception as e:
            logger.error(f"Error calling OpenRouter: {e}", exc_info=True)
            return f"Error inesperado al contactar con el modelo: {str(e)}"
