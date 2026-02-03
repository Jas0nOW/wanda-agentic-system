"""
WANDA Telegram Bot - Remote Voice & Notifications
==================================================
Receives voice notes, sends status notifications.
"""

import os
import logging
from pathlib import Path

# Load .env file
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent / ".env")

from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot Token (from .env or environment)
BOT_TOKEN = os.getenv("WANDA_TELEGRAM_BOT_TOKEN")
BOT_NAME = os.getenv("WANDA_TELEGRAM_BOT_NAME", "@wandavoice_bot")



class WandaTelegramBot:
    """Telegram bot for WANDA remote access."""

    def __init__(self, token: str = None):
        self.token = token or BOT_TOKEN
        if not self.token:
            raise ValueError("WANDA_TELEGRAM_BOT_TOKEN environment variable not set.")
        
        self.app = Application.builder().token(self.token).build()
        self._register_handlers()

    def _register_handlers(self):
        """Register command and message handlers."""
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("task", self.cmd_task))
        self.app.add_handler(MessageHandler(filters.VOICE, self.handle_voice))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        await update.message.reply_text(
            "🚀 WANDA Remote Gateway aktiv.\n\n"
            "Commands:\n"
            "/status - System status\n"
            "/task <text> - Create new task\n\n"
            "Du kannst auch Voice Notes schicken!"
        )

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        # TODO: Query actual system status
        await update.message.reply_text(
            "✅ WANDA Status:\n"
            "• Voice Gateway: Online\n"
            "• Ollama: Running\n"
            "• OpenCode: Connected\n"
            "• Active Tasks: 0"
        )

    async def cmd_task(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /task command - create a new task."""
        if not context.args:
            await update.message.reply_text("Usage: /task <beschreibung>")
            return

        task_description = " ".join(context.args)
        # TODO: Inject into WANDA pipeline
        await update.message.reply_text(
            f"📝 Task erstellt:\n\n{task_description}\n\n"
            "Wird an OpenCode weitergeleitet..."
        )

    async def handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice notes - transcribe and create task."""
        voice = update.message.voice
        file = await voice.get_file()
        
        # Download voice note
        voice_path = Path(f"/tmp/wanda_voice_{update.message.message_id}.ogg")
        await file.download_to_drive(voice_path)
        
        await update.message.reply_text("🎤 Voice Note empfangen. Transkribiere...")
        
        # TODO: Integrate with FasterWhisper for transcription
        # For now, placeholder response
        await update.message.reply_text(
            "📝 Transkription:\n[Voice transcription would appear here]\n\n"
            "Soll ich daraus einen Task erstellen? /task <text>"
        )

    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle plain text messages."""
        text = update.message.text
        # TODO: Route through Ollama gateway
        await update.message.reply_text(
            f"📨 Nachricht empfangen:\n{text}\n\n"
            "Verarbeite..."
        )

    def run(self):
        """Start the bot in polling mode."""
        logger.info("Starting WANDA Telegram Bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)


# Standalone notification sender
async def send_notification(chat_id: int, message: str, token: str = None):
    """
    Send a notification to a specific chat.
    Used for push updates from the main WANDA pipeline.
    
    Args:
        chat_id: Telegram chat ID to send to
        message: Notification message
        token: Bot token (uses env if not provided)
    """
    bot = Bot(token=token or BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message)


if __name__ == "__main__":
    bot = WandaTelegramBot()
    bot.run()
