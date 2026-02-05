# Wanda Voice Assistant - Session Adapter
"""Persistent Gemini CLI session using PTY."""

import threading
from typing import Optional

try:
    import pexpect
    PEXPECT_AVAILABLE = True
except ImportError:
    PEXPECT_AVAILABLE = False


class GeminiSessionAdapter:
    """
    Persistent Gemini CLI session using PTY.
    Maintains context across multiple turns.
    """
    
    def __init__(self, model: str = "flash", timeout: int = 120):
        if not PEXPECT_AVAILABLE:
            raise ImportError("pexpect not installed. Run: pip install pexpect")
        
        self.model = model
        self.timeout = timeout
        self.session: Optional[pexpect.spawn] = None
        self.lock = threading.Lock()
        
        print(f"[Session] Adapter initialized (model={model})")
    
    def start_session(self):
        """Start persistent Gemini session."""
        self.session = pexpect.spawn(
            f"gemini {self.model}",
            encoding="utf-8",
            timeout=self.timeout
        )
        
        # Wait for initial prompt
        try:
            self.session.expect([">", "\\$", ">>>"], timeout=15)
            print("[Session] Gemini session started")
        except pexpect.TIMEOUT:
            print("[Session] Warning: Initial prompt not detected")
    
    def send_prompt(self, prompt: str) -> str:
        """Send prompt to active session."""
        with self.lock:
            if not self.session or not self.session.isalive():
                self.start_session()
            
            try:
                # Send prompt
                self.session.sendline(prompt)
                
                # Wait for response (next prompt marker)
                self.session.expect([">", "\\$", ">>>"], timeout=self.timeout)
                
                # Extract response
                response = self.session.before.strip()
                
                # Clean up (remove echoed prompt)
                lines = response.split("\n")
                if lines and prompt in lines[0]:
                    lines = lines[1:]
                
                return "\n".join(lines).strip()
                
            except pexpect.TIMEOUT:
                return "⏱️ Session timeout"
            except pexpect.EOF:
                print("[Session] Session ended unexpectedly")
                return "❌ Session ended"
    
    def close(self):
        """Close session."""
        if self.session:
            try:
                self.session.sendline("/quit")
                self.session.close()
            except:
                pass
            self.session = None
            print("[Session] Closed")
    
    def is_alive(self) -> bool:
        """Check if session is alive."""
        return self.session is not None and self.session.isalive()


if __name__ == "__main__":
    if PEXPECT_AVAILABLE:
        print("Testing Session Adapter...")
        adapter = GeminiSessionAdapter()
        print("✅ Session adapter initialized")
    else:
        print("❌ pexpect not installed")
