# Wanda Voice Assistant - Interrupt Controller
"""Controls TTS interruption when user speaks."""

import threading
import time
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from audio.silero_vad import SileroVAD
    from tts.piper_engine import PiperEngine


class InterruptController:
    """
    Monitors user voice during TTS and stops instantly.
    Target: < 200ms interrupt latency.
    """
    
    def __init__(self, vad: 'SileroVAD', tts: 'PiperEngine'):
        self.vad = vad
        self.tts = tts
        self.interrupted = False
        self.check_interval = 0.05  # 50ms = < 200ms total latency
    
    def speak_with_interrupt(self, text: str, mode: str = "short") -> bool:
        """
        Speak text, but stop immediately if user interrupts.
        
        Args:
            text: Text to speak
            mode: TTS mode ('short' or 'full')
        
        Returns:
            True if interrupted, False if completed normally
        """
        self.interrupted = False
        
        # Reset VAD state
        self.vad.reset()
        
        # Start TTS in separate thread
        tts_thread = threading.Thread(target=self.tts.speak, args=(text, mode))
        tts_thread.start()
        
        # Monitor for interruption
        while tts_thread.is_alive():
            if self.vad.is_user_speaking():
                # User is talking → KILL TTS immediately
                self.tts.stop()
                self.interrupted = True
                print("[Interrupt] User interrupted TTS")
                tts_thread.join(timeout=0.5)
                break
            time.sleep(self.check_interval)
        
        return self.interrupted
    
    def was_interrupted(self) -> bool:
        """Check if last speak was interrupted."""
        return self.interrupted


if __name__ == "__main__":
    print("Interrupt Controller module loaded")
