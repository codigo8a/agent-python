import asyncio
import logging
from app.config import Config
from app.bot.telegram_bot import TelegramBot

# Setup logger for main module
logger = logging.getLogger(__name__)

class App:
    """Class to bootstrap and run the application."""
    
    def __init__(self):
        # Validate configuration before starting
        Config.validate()
        self._bot = TelegramBot(Config.TELEGRAM_BOT_TOKEN)

    async def start(self) -> None:
        """Start the application."""
        try:
            # Start the Telegram bot
            await self._bot.run()
        except asyncio.CancelledError:
            # Clean exit on cancellation
            logger.info("Application shut down gracefully.")
        except Exception as e:
            # Log unexpected errors
            logger.critical(f"Critical failure: {e}", exc_info=True)
            raise e
