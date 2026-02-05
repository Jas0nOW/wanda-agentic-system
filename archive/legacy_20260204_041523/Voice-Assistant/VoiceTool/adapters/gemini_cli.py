# Wanda Voice Assistant - Gemini CLI Adapter
"""Adapter for communicating with Gemini CLI with retry/fallback."""

import subprocess
import time
from typing import Optional, List, Dict


class GeminiCLIAdapter:
    """Adapter for Gemini CLI with retry logic and fallback."""
    
    def __init__(
        self, 
        model: str = "flash", 
        gemini_path: str = "gemini",
        timeout: int = 90,
        max_retries: int = 2,
        fallback_model: Optional[str] = "pro"
    ):
        self.model = model
        self.gemini_path = gemini_path
        self.timeout = timeout
        self.max_retries = max_retries
        self.fallback_model = fallback_model
        self.history: List[Dict[str, str]] = []
        
        print(f"[Gemini] Adapter initialized (model={model}, timeout={timeout}s, retries={max_retries})")
        self._check_gemini()
    
    def _check_gemini(self):
        """Check if Gemini CLI is available."""
        try:
            result = subprocess.run(
                [self.gemini_path, "--version"],
                capture_output=True,
                text=True,
                timeout=3
            )
            if result.returncode == 0:
                print(f"[Gemini] CLI found: {result.stdout.strip()}")
            else:
                print("[Gemini] Warning: gemini command failed")
        except FileNotFoundError:
            print(f"[Gemini] ERROR: gemini not found at '{self.gemini_path}'")
        except Exception as e:
            print(f"[Gemini] Warning: {e}")
    
    def send_prompt(self, prompt: str, include_history: bool = True) -> str:
        """Send prompt with retry logic and fallback."""
        # Build full prompt with history
        if include_history and self.history:
            context = self._build_context()
            full_prompt = f"{context}\n\nUser: {prompt}"
        else:
            full_prompt = prompt
        
        # Try with retries
        for attempt in range(self.max_retries + 1):
            current_timeout = self.timeout + (attempt * 30)  # 90, 120, 150s
            
            try:
                print(f"[Gemini] Sending to {self.model} (attempt {attempt+1}, timeout={current_timeout}s)...")
                
                result = subprocess.run(
                    [self.gemini_path, self.model, full_prompt],
                    capture_output=True,
                    text=True,
                    timeout=current_timeout
                )
                
                if result.returncode == 0:
                    response = result.stdout.strip()
                    self._update_history(prompt, response)
                    return response
                
                # Non-zero exit - try fallback on last attempt
                if attempt == self.max_retries and self.fallback_model:
                    return self._try_fallback(full_prompt, prompt)
                
                error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                print(f"[Gemini] Error: {error_msg}")
                
            except subprocess.TimeoutExpired:
                print(f"[Gemini] Timeout ({current_timeout}s)")
                if attempt < self.max_retries:
                    wait = 2 ** attempt
                    print(f"[Gemini] Retrying in {wait}s...")
                    time.sleep(wait)
                elif self.fallback_model:
                    return self._try_fallback(full_prompt, prompt)
                else:
                    return "⏱️ Gemini timeout after retries."
            
            except Exception as e:
                print(f"[Gemini] Exception: {e}")
                if attempt == self.max_retries:
                    return f"❌ Error: {e}"
        
        return "❌ All attempts failed"
    
    def _try_fallback(self, full_prompt: str, original_prompt: str) -> str:
        """Try fallback model."""
        print(f"[Gemini] Trying fallback model: {self.fallback_model}...")
        try:
            result = subprocess.run(
                [self.gemini_path, self.fallback_model, full_prompt],
                capture_output=True,
                text=True,
                timeout=self.timeout + 60
            )
            if result.returncode == 0:
                response = result.stdout.strip()
                self._update_history(original_prompt, response)
                print("[Gemini] Fallback succeeded")
                return response
        except Exception as e:
            print(f"[Gemini] Fallback failed: {e}")
        
        return "❌ Primary and fallback failed"
    
    def _update_history(self, prompt: str, response: str):
        """Update conversation history."""
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": response})
        self._trim_history(12)
    
    def _build_context(self) -> str:
        """Build context string from history."""
        return "\n\n".join(
            f"{t['role'].capitalize()}: {t['content']}" 
            for t in self.history
        )
    
    def _trim_history(self, max_turns: int = 12):
        """Trim history to max turns."""
        max_messages = max_turns * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]
    
    def clear_history(self):
        """Clear conversation history."""
        self.history = []
        print("[Gemini] History cleared")


if __name__ == "__main__":
    print("Testing Gemini CLI Adapter with retry...")
    adapter = GeminiCLIAdapter()
    response = adapter.send_prompt("Sage nur 'Hallo'", include_history=False)
    print(f"\n✅ Response: {response}")
