import os
import logging
from dotenv import load_dotenv

# Basic logging configuration
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load .env file
load_dotenv()

class Config:
    """Application configuration from environment variables."""
    TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN", "")
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")

    @classmethod
    def validate(cls) -> None:
        """Validate that all required configuration is present."""
        if not cls.TELEGRAM_BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN is missing in .env or environment variables.")
            raise ValueError("TELEGRAM_BOT_TOKEN is required to start the bot.")
        
        if not cls.OPENROUTER_API_KEY:
            logger.warning("OPENROUTER_API_KEY is missing. LLM features will be disabled.")
