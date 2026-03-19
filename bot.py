import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Habilitar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Token de Telegram (Cargado desde .env)
TOKEN = os.getenv("TELEGRAM_TOKEN")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responder con 'que pasa?' a cualquier mensaje recibido."""
    if update.message and update.message.text:
        logger.info(f"Mensaje recibido: {update.message.text}")
        await update.message.reply_text("que pasa?")

if __name__ == '__main__':
    # Construir la aplicación
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Manejador de mensajes de texto (que no sean comandos)
    echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
    application.add_handler(echo_handler)
    
    logger.info("El bot ha iniciado...")
    # Ejecutar el bot hasta que se presione Ctrl-C
    application.run_polling()
