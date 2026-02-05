# Wanda Voice Assistant - piper TTS Engine
"""Text-to-Speech using piper-tts with stop capability."""

import subprocess
import threading
from pathlib import Path
from typing import Optional


class PiperEngine:
    """TTS engine using piper with interrupt support."""
    
    def __init__(self, voice: str = "de_DE-eva_k-x_low", mode: str = "short"):
        self.voice = voice
        self.mode = mode
        self.piper_cmd: Optional[str] = None
        self.current_process: Optional[subprocess.Popen] = None
        self.player_process: Optional[subprocess.Popen] = None
        self.stop_flag = threading.Event()
        
        print(f"[TTS] Initializing piper ({voice}, mode={mode})")
        self._check_piper()
    
    def _check_piper(self):
        """Check if piper is available."""
        # Check venv first
        venv_piper = Path(__file__).parent.parent / "venv" / "bin" / "piper"
        if venv_piper.exists():
            self.piper_cmd = str(venv_piper)
            print(f"[TTS] piper found in venv")
            return
        
        # Fallback to system PATH
        try:
            result = subprocess.run(["piper", "--version"], capture_output=True, timeout=2)
            if result.returncode == 0:
                self.piper_cmd = "piper"
                print("[TTS] piper found in PATH")
        except:
            print("[TTS] Warning: piper not found")
    
    def speak(self, text: str, mode: Optional[str] = None) -> bool:
        """Speak text (stoppable)."""
        if not text or not text.strip() or not self.piper_cmd:
            return False
        
        self.stop_flag.clear()
        mode = mode or self.mode
        
        if mode == "short":
            text = self._extract_short(text)
        
        print(f"[TTS] Speaking ({len(text)} chars)")
        
        try:
            player = self._get_audio_player()
            if not player:
                print("[TTS] No audio player found")
                return False
            
            # Start piper process
            self.current_process = subprocess.Popen(
                [self.piper_cmd, "--model", self.voice, "--output-raw"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL
            )
            
            # Start player process
            self.player_process = subprocess.Popen(
                player,
                stdin=self.current_process.stdout,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Send text
            self.current_process.stdin.write(text.encode('utf-8'))
            self.current_process.stdin.close()
            
            # Wait with stop check
            while self.player_process.poll() is None:
                if self.stop_flag.is_set():
                    self._kill_processes()
                    return False
                threading.Event().wait(0.05)
            
            self.current_process.wait()
            return self.current_process.returncode == 0
            
        except Exception as e:
            print(f"[TTS] Error: {e}")
            return False
        finally:
            self.current_process = None
            self.player_process = None
    
    def stop(self):
        """Stop TTS immediately."""
        self.stop_flag.set()
        self._kill_processes()
        print("[TTS] Stopped")
    
    def _kill_processes(self):
        """Kill current TTS processes."""
        for proc in [self.player_process, self.current_process]:
            if proc and proc.poll() is None:
                try:
                    proc.kill()
                except:
                    pass
    
    def _extract_short(self, text: str) -> str:
        """Extract first 2-3 sentences."""
        sentences = []
        current = ""
        for char in text:
            current += char
            if char in '.!?' and len(current.strip()) > 10:
                sentences.append(current.strip())
                current = ""
                if len(sentences) >= 2:
                    break
        if current.strip() and len(sentences) < 2:
            sentences.append(current.strip())
        return " ".join(sentences[:3])
    
    def _get_audio_player(self) -> Optional[list]:
        """Detect available audio player."""
        try:
            subprocess.run(["aplay", "--version"], capture_output=True, timeout=1)
            return ["aplay", "-r", "22050", "-f", "S16_LE", "-t", "raw", "-c", "1"]
        except:
            pass
        try:
            subprocess.run(["paplay", "--version"], capture_output=True, timeout=1)
            return ["paplay", "--raw", "--rate=22050", "--format=s16le", "--channels=1"]
        except:
            pass
        return None


if __name__ == "__main__":
    print("Testing stoppable piper TTS...")
    engine = PiperEngine()
    success = engine.speak("Hallo, ich bin Wanda.", mode="full")
    print(f"✅ TTS test: {'success' if success else 'failed'}")
