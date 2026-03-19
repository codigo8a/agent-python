import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from app.config import Config
from app.core.router import Router

# Set up logging for this module
logger = logging.getLogger(__name__)

class TelegramBot:
    """Telegram bot implementation using python-telegram-bot."""
    
    def __init__(self, token: str):
        self._token = token
        self._router = Router()
        self._app = Application.builder().token(self._token).build()

    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Process incoming messages and respond."""
        try:
            # Check if there is a message and text
            if update.message and update.message.text:
                logger.info(f"Received message: {update.message.text}")
                
                # Get response from the router
                response = await self._router.route()
                
                # Send the response back
                await update.message.reply_text(response)
        except Exception as e:
            logger.error(f"Error handling message: {e}", exc_info=True)

    def setup_handlers(self) -> None:
        """Configure message handlers for the bot."""
        # This will catch ANY incoming message with text and call _handle_message
        self._app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self._handle_message))
        # Optional: Add /start handler
        self._app.add_handler(MessageHandler(filters.COMMAND, self._handle_message))

    async def run(self) -> None:
        """Start the bot in polling mode."""
        logger.info("Starting Telegram bot...")
        self.setup_handlers()
        
        # In python-telegram-bot v20+, this is the async-safe way to start
        async with self._app:
            await self._app.initialize()
            await self._app.start()
            await self._app.updater.start_polling()
            logger.info("Bot is now polling.")
            
            # Keep the bot running until it's cancelled
            try:
                # Use a loop that can be interrupted
                while True:
                    await asyncio.sleep(3600)  # Sleep for an hour
            except asyncio.CancelledError:
                logger.info("Bot execution cancelled. Cleaning up...")
                await self._app.updater.stop()
                await self._app.stop()
                await self._app.shutdown()
                raise
