# Wanda Voice Assistant - Telegram Bot
"""Telegram bot for mobile Wanda access with voice message support."""

from __future__ import annotations  # Defer type hint evaluation

import os
import io
import time
import threading
import tempfile
from typing import Optional, Callable, TYPE_CHECKING
from pathlib import Path

if TYPE_CHECKING:
    from telegram import Update
    from telegram.ext import ContextTypes

try:
    from telegram import Update, Bot
    from telegram.ext import (
        Application, CommandHandler, MessageHandler,
        ContextTypes, filters
    )
    TELEGRAM_AVAILABLE = True
except ImportError:
    TELEGRAM_AVAILABLE = False
    print("[Telegram] python-telegram-bot not installed")
    print("[Telegram] Install: pip install python-telegram-bot")


class WandaTelegramBot:
    """
    Telegram bot for remote Wanda access.
    
    Features:
    - Voice messages → STT → Wanda → Response
    - Text messages → Wanda → Response
    - Project creation commands
    - Push notifications on completion
    """
    
    def __init__(
        self,
        token: str,
        stt_engine = None,
        tts_engine = None,
        gemini_adapter = None,
        ollama_adapter = None,
        project_init = None,
        notifier = None,
        allowed_users: list = None
    ):
        """
        Initialize Telegram bot.
        
        Args:
            token: Telegram bot token from @BotFather
            stt_engine: FasterWhisperEngine for transcription
            tts_engine: PiperEngine for voice responses
            gemini_adapter: GeminiCLIAdapter for AI
            ollama_adapter: OllamaAdapter for local AI
            project_init: ProjectInitializer
            notifier: WandaNotifier
            allowed_users: List of allowed Telegram user IDs (for security)
        """
        if not TELEGRAM_AVAILABLE:
            self.available = False
            return
        
        self.token = token
        self.stt = stt_engine
        self.tts = tts_engine
        self.gemini = gemini_adapter
        self.ollama = ollama_adapter
        self.project_init = project_init
        self.notifier = notifier
        self.allowed_users = allowed_users or []
        
        self.application = None
        self.running = False
        self.available = bool(token)
        
        if not token:
            print("[Telegram] No token provided, bot disabled")
    
    def start(self):
        """Start the bot in background thread."""
        if not self.available:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("[Telegram] Bot started")
    
    def stop(self):
        """Stop the bot."""
        self.running = False
        if self.application:
            self.application.stop()
    
    def _run(self):
        """Main bot loop."""
        import asyncio
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self._async_run())
        except Exception as e:
            print(f"[Telegram] Error: {e}")
    
    async def _async_run(self):
        """Async bot runner."""
        self.application = Application.builder().token(self.token).build()
        
        # Add handlers
        self.application.add_handler(CommandHandler("start", self._cmd_start))
        self.application.add_handler(CommandHandler("help", self._cmd_help))
        self.application.add_handler(CommandHandler("status", self._cmd_status))
        self.application.add_handler(CommandHandler("projekt", self._cmd_projekt))
        self.application.add_handler(CommandHandler("idee", self._cmd_idee))
        
        # Voice messages
        self.application.add_handler(MessageHandler(
            filters.VOICE | filters.AUDIO,
            self._handle_voice
        ))
        
        # Text messages
        self.application.add_handler(MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            self._handle_text
        ))
        
        # Start polling
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()
        
        print("[Telegram] Bot is running...")
        
        while self.running:
            await asyncio.sleep(1)
        
        await self.application.stop()
    
    def _is_allowed(self, user_id: int) -> bool:
        """Check if user is allowed."""
        if not self.allowed_users:
            return True  # No restrictions
        return user_id in self.allowed_users
    
    async def _cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command."""
        if not self._is_allowed(update.effective_user.id):
            await update.message.reply_text("❌ Zugriff verweigert.")
            return
        
        await update.message.reply_text(
            "🌟 **Wanda Mobile**\n\n"
            "Ich bin dein persönlicher AI-Assistent!\n\n"
            "**Funktionen:**\n"
            "🎤 Voice Message = Ich höre dir zu\n"
            "💬 Text = Ich antworte\n"
            "📁 /projekt Name = Neues Projekt\n"
            "💡 /idee Text = Idee speichern\n"
            "ℹ️ /status = System-Status\n\n"
            "Sprich oder schreibe einfach los!",
            parse_mode="Markdown"
        )
    
    async def _cmd_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command."""
        await update.message.reply_text(
            "📖 **Wanda Hilfe**\n\n"
            "*Befehle:*\n"
            "/projekt <name> - Erstellt Projekt in Playground\n"
            "/idee <text> - Speichert Idee\n"
            "/status - Zeigt System-Status\n\n"
            "*Natürliche Sprache:*\n"
            "- \"Erstelle Projekt XYZ\"\n"
            "- \"Neue Idee: Eine App für...\"\n"
            "- \"Starte Venture ABC\"\n\n"
            "*Voice Messages:*\n"
            "Einfach Sprachnachricht senden!",
            parse_mode="Markdown"
        )
    
    async def _cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command."""
        if not self._is_allowed(update.effective_user.id):
            return
        
        status = [
            "📊 **Wanda Status**",
            "",
            f"🎤 STT: {'✅' if self.stt else '❌'}",
            f"🔊 TTS: {'✅' if self.tts else '❌'}",
            f"🤖 Gemini: {'✅' if self.gemini else '❌'}",
            f"🦙 Ollama: {'✅' if (self.ollama and self.ollama.available) else '❌'}",
            f"📁 Projekte: {'✅' if self.project_init else '❌'}",
            f"🔔 Notifications: {'✅' if (self.notifier and self.notifier.enabled) else '❌'}",
        ]
        
        await update.message.reply_text("\n".join(status), parse_mode="Markdown")
    
    async def _cmd_projekt(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /projekt command."""
        if not self._is_allowed(update.effective_user.id):
            return
        
        if not self.project_init:
            await update.message.reply_text("❌ Projekt-Initialisierung nicht verfügbar")
            return
        
        if not context.args:
            await update.message.reply_text("Verwendung: /projekt <name>")
            return
        
        name = " ".join(context.args)
        await update.message.reply_text(f"📁 Erstelle Projekt: {name}...")
        
        success, result = self.project_init.create_project(name)
        
        if success:
            await update.message.reply_text(f"✅ Projekt erstellt!\n\n📂 {result}")
        else:
            await update.message.reply_text(f"❌ Fehler: {result}")
    
    async def _cmd_idee(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /idee command."""
        if not self._is_allowed(update.effective_user.id):
            return
        
        if not self.project_init:
            await update.message.reply_text("❌ Ideen-Speicherung nicht verfügbar")
            return
        
        if not context.args:
            await update.message.reply_text("Verwendung: /idee <deine idee>")
            return
        
        idea = " ".join(context.args)
        result = self.project_init.capture_idea(idea)
        await update.message.reply_text(f"💡 {result}")
    
    async def _handle_voice(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle voice messages."""
        if not self._is_allowed(update.effective_user.id):
            return
        
        if not self.stt:
            await update.message.reply_text("❌ Spracherkennung nicht verfügbar")
            return
        
        await update.message.reply_text("🎤 Höre zu...")
        
        try:
            # Download voice file
            voice = update.message.voice or update.message.audio
            file = await context.bot.get_file(voice.file_id)
            
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as f:
                temp_path = f.name
            
            await file.download_to_drive(temp_path)
            
            # Convert to wav if needed and transcribe
            text = await self._transcribe_voice(temp_path)
            
            # Clean up
            os.unlink(temp_path)
            
            if not text:
                await update.message.reply_text("❌ Konnte Audio nicht verstehen")
                return
            
            await update.message.reply_text(f"📝 Verstanden: _{text}_", parse_mode="Markdown")
            
            # Process like text
            await self._process_message(update, text)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {e}")
    
    async def _transcribe_voice(self, audio_path: str) -> str:
        """Transcribe voice file."""
        try:
            import subprocess
            
            # Convert OGG to WAV
            wav_path = audio_path.replace(".ogg", ".wav")
            subprocess.run(
                ["ffmpeg", "-i", audio_path, "-ar", "16000", "-ac", "1", wav_path, "-y"],
                capture_output=True,
                timeout=30
            )
            
            # Load audio
            import numpy as np
            from scipy.io import wavfile
            
            rate, audio = wavfile.read(wav_path)
            audio = audio.astype(np.float32) / 32768.0
            
            # Transcribe
            text = self.stt.transcribe(audio, language="de")
            
            # Cleanup
            os.unlink(wav_path)
            
            return text
            
        except Exception as e:
            print(f"[Telegram] Transcription error: {e}")
            return ""
    
    async def _handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages."""
        if not self._is_allowed(update.effective_user.id):
            return
        
        text = update.message.text
        await self._process_message(update, text)
    
    async def _process_message(self, update: Update, text: str):
        """Process message and generate response."""
        
        # Check for project commands
        if self.project_init:
            cmd = self.project_init.parse_command(text)
            if cmd:
                if cmd["action"] == "create_project":
                    await update.message.reply_text(f"📁 Erstelle {cmd['type']}: {cmd['name']}...")
                    success, result = self.project_init.create_project(
                        cmd["name"],
                        project_type=cmd["type"]
                    )
                    if success:
                        await update.message.reply_text(f"✅ Erstellt!\n📂 {result}")
                    else:
                        await update.message.reply_text(f"❌ {result}")
                    return
                    
                elif cmd["action"] == "capture_idea":
                    result = self.project_init.capture_idea(cmd["idea"])
                    await update.message.reply_text(f"💡 {result}")
                    return
        
        # Send to AI
        await update.message.reply_text("🤔 Denke nach...")
        
        response = ""
        
        # Try Ollama first (local)
        if self.ollama and self.ollama.available:
            try:
                response = self.ollama.generate(text, max_tokens=500)
            except:
                pass
        
        # Fall back to Gemini
        if not response and self.gemini:
            try:
                response = self.gemini.send(text)
            except Exception as e:
                response = f"Fehler bei Gemini: {e}"
        
        if not response:
            response = "Konnte keine Antwort generieren. Bitte versuche es später erneut."
        
        # Send response (split if too long)
        if len(response) > 4000:
            for i in range(0, len(response), 4000):
                await update.message.reply_text(response[i:i+4000])
        else:
            await update.message.reply_text(response)


def create_telegram_bot(config: dict, **kwargs) -> Optional[WandaTelegramBot]:
    """Factory function to create Telegram bot from config."""
    if not TELEGRAM_AVAILABLE:
        return None
    
    token = config.get("telegram", {}).get("token", "")
    if not token:
        token = os.environ.get("WANDA_TELEGRAM_TOKEN", "")
    
    if not token:
        print("[Telegram] No token found in config or WANDA_TELEGRAM_TOKEN env var")
        return None
    
    allowed_users = config.get("telegram", {}).get("allowed_users", [])
    
    return WandaTelegramBot(
        token=token,
        allowed_users=allowed_users,
        **kwargs
    )


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python telegram_bot.py <BOT_TOKEN>")
        sys.exit(1)
    
    bot = WandaTelegramBot(token=sys.argv[1])
    bot.start()
    
    print("Bot running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        bot.stop()
