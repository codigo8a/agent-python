import httpx
import logging
from app.config import Config

logger = logging.getLogger(__name__)

class LLMService:
    """Service to interact with OpenRouter API."""
    
    def __init__(self):
        self._api_key = Config.OPENROUTER_API_KEY
        self._api_url = "https://openrouter.ai/api/v1/chat/completions"
        self._model = "google/gemini-flash-1.5-exp:free" # Use a more stable stable free model

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
                {"role": "system", "content": "Eres un asistente útil y amable integrado en un bot de Telegram. Responde de forma concisa."},
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
