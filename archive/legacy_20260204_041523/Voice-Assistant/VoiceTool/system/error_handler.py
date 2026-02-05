# Wanda Voice Assistant - Error Handler
"""Centralized error handling and graceful degradation."""

import sys
import traceback
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable
from functools import wraps


class WandaErrorHandler:
    """
    Centralized error handling:
    - Graceful degradation
    - Error logging
    - User-friendly messages
    """
    
    def __init__(self, log_dir: Optional[str] = None):
        self.log_dir = Path(log_dir) if log_dir else Path.home() / ".wanda" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Setup logging
        self.logger = logging.getLogger("wanda")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        log_file = self.log_dir / f"wanda_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        ))
        self.logger.addHandler(file_handler)
        
        # Console handler (warnings and errors only)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.WARNING)
        console_handler.setFormatter(logging.Formatter('⚠️ %(message)s'))
        self.logger.addHandler(console_handler)
    
    def handle(self, error: Exception, context: str = "", notify_user: bool = False) -> str:
        """
        Handle an error gracefully.
        
        Args:
            error: The exception
            context: Where the error occurred
            notify_user: Whether to return user-friendly message
        
        Returns:
            User-friendly error message
        """
        # Log full traceback
        self.logger.error(f"[{context}] {type(error).__name__}: {error}")
        self.logger.debug(traceback.format_exc())
        
        # Generate user-friendly message
        msg = self._get_user_message(error, context)
        
        if notify_user:
            print(f"❌ {msg}")
        
        return msg
    
    def _get_user_message(self, error: Exception, context: str) -> str:
        """Generate user-friendly error message."""
        error_type = type(error).__name__
        
        messages = {
            "FileNotFoundError": "Datei nicht gefunden. Bitte Pfad prüfen.",
            "PermissionError": "Keine Berechtigung. Bitte Rechte prüfen.",
            "TimeoutError": "Zeitüberschreitung. Bitte erneut versuchen.",
            "ConnectionError": "Verbindungsfehler. Bitte Netzwerk prüfen.",
            "subprocess.TimeoutExpired": "Prozess-Timeout. Bitte erneut versuchen.",
            "RuntimeError": f"Laufzeitfehler in {context}.",
        }
        
        return messages.get(error_type, f"Fehler: {str(error)[:100]}")
    
    def log_info(self, message: str):
        """Log info message."""
        self.logger.info(message)
    
    def log_warning(self, message: str):
        """Log warning."""
        self.logger.warning(message)
    
    def log_error(self, message: str):
        """Log error."""
        self.logger.error(message)


def safe_execute(fallback=None, context: str = ""):
    """
    Decorator for safe execution with fallback.
    
    Usage:
        @safe_execute(fallback="", context="STT")
        def transcribe(self, audio):
            ...
    """
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"[{context}] Error: {e}")
                return fallback
        return wrapper
    return decorator


def check_system_requirements() -> dict:
    """
    Check system requirements and return status.
    
    Returns:
        Dict with status of each requirement
    """
    status = {
        "python": False,
        "audio": False,
        "piper": False,
        "gemini": False,
        "ollama": False,
        "gtk": False,
        "evdev": False,
    }
    
    import subprocess
    
    # Python version
    status["python"] = sys.version_info >= (3, 10)
    
    # Audio (PipeWire/PulseAudio)
    try:
        result = subprocess.run(["pactl", "info"], capture_output=True, timeout=2)
        status["audio"] = result.returncode == 0
    except:
        pass
    
    # Piper TTS
    try:
        result = subprocess.run(["piper", "--version"], capture_output=True, timeout=2)
        status["piper"] = result.returncode == 0
    except:
        pass
    
    # Gemini CLI
    try:
        result = subprocess.run(["gemini", "--version"], capture_output=True, timeout=2)
        status["gemini"] = result.returncode == 0
    except:
        pass
    
    # Ollama
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, timeout=2)
        status["ollama"] = result.returncode == 0
    except:
        pass
    
    # GTK
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        status["gtk"] = True
    except:
        pass
    
    # evdev
    try:
        import evdev
        status["evdev"] = True
    except:
        pass
    
    return status


def print_system_status():
    """Print system status for debugging."""
    status = check_system_requirements()
    
    print("\n" + "=" * 40)
    print("🔧 SYSTEM STATUS")
    print("=" * 40)
    
    for component, ok in status.items():
        icon = "✅" if ok else "❌"
        print(f"  {icon} {component}")
    
    print("=" * 40 + "\n")
    
    return status


if __name__ == "__main__":
    print_system_status()
