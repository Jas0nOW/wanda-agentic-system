# Wanda Voice Assistant - Context Manager
"""Smart context management: fresh chats but maintain knowledge."""

import json
import time
from pathlib import Path
from typing import Optional, Dict, List, Any
from dataclasses import dataclass, asdict


@dataclass
class ConversationWindow:
    """A conversation window with context."""
    id: str
    start_time: float
    messages: List[Dict[str, str]]
    summary: Optional[str] = None
    tool: Optional[str] = None  # gemini, opencode, ollama


class ContextManager:
    """
    Smart context management:
    - Fresh chats when needed
    - Preserve important context
    - Auto-summarize old windows
    """
    
    def __init__(
        self, 
        max_messages_per_window: int = 20,
        max_windows: int = 5,
        persist_path: Optional[str] = None
    ):
        self.max_messages = max_messages_per_window
        self.max_windows = max_windows
        self.persist_path = Path(persist_path) if persist_path else Path.home() / ".wanda" / "context.json"
        
        self.windows: List[ConversationWindow] = []
        self.current_window: Optional[ConversationWindow] = None
        self.ollama_available = False
        
        self._load()
    
    def start_fresh_window(self, tool: str = "gemini") -> ConversationWindow:
        """Start a fresh conversation window."""
        # Summarize current window before switching
        if self.current_window and len(self.current_window.messages) > 3:
            self._summarize_window(self.current_window)
        
        # Create new window
        window = ConversationWindow(
            id=f"window_{int(time.time())}",
            start_time=time.time(),
            messages=[],
            tool=tool
        )
        
        self.windows.append(window)
        self.current_window = window
        
        # Trim old windows
        if len(self.windows) > self.max_windows:
            self.windows = self.windows[-self.max_windows:]
        
        self._save()
        return window
    
    def add_message(self, role: str, content: str):
        """Add message to current window."""
        if not self.current_window:
            self.start_fresh_window()
        
        self.current_window.messages.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })
        
        # Auto-fresh if window is too full
        if len(self.current_window.messages) >= self.max_messages:
            print("[Context] Window full, starting fresh...")
            self.start_fresh_window(self.current_window.tool)
        
        self._save()
    
    def should_refresh(self) -> bool:
        """Check if we should start fresh."""
        if not self.current_window:
            return True
        
        # Refresh if >20 messages
        if len(self.current_window.messages) >= self.max_messages:
            return True
        
        # Refresh if >30 min old
        age = time.time() - self.current_window.start_time
        if age > 1800:  # 30 min
            return True
        
        return False
    
    def get_context_for_prompt(self) -> str:
        """Get context string for new prompt."""
        context_parts = []
        
        # Add summaries from previous windows
        for window in self.windows[:-1]:  # Exclude current
            if window.summary:
                context_parts.append(f"[Previous Session Summary]: {window.summary}")
        
        # Add recent messages from current window
        if self.current_window:
            recent = self.current_window.messages[-6:]  # Last 3 turns
            for msg in recent:
                role = "User" if msg["role"] == "user" else "Wanda"
                context_parts.append(f"{role}: {msg['content'][:200]}")
        
        return "\n".join(context_parts)
    
    def _summarize_window(self, window: ConversationWindow):
        """Summarize a window (uses Ollama if available)."""
        if not window.messages:
            return
        
        # Simple summary: first and last topic
        first_msg = window.messages[0]["content"][:100] if window.messages else ""
        last_msg = window.messages[-1]["content"][:100] if window.messages else ""
        
        window.summary = f"Session about: {first_msg}... Last: {last_msg}"
        
        # TODO: Use Ollama for better summary
    
    def get_briefing_data(self) -> Dict[str, Any]:
        """Get data for startup briefing."""
        total_sessions = len(self.windows)
        
        last_session = None
        if self.windows:
            last = self.windows[-1]
            last_session = {
                "age": time.time() - last.start_time,
                "messages": len(last.messages),
                "tool": last.tool,
                "summary": last.summary
            }
        
        return {
            "total_sessions": total_sessions,
            "last_session": last_session
        }
    
    def _save(self):
        """Save to disk."""
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        data = [asdict(w) for w in self.windows]
        with open(self.persist_path, "w") as f:
            json.dump(data, f, indent=2)
    
    def _load(self):
        """Load from disk."""
        if self.persist_path.exists():
            try:
                with open(self.persist_path) as f:
                    data = json.load(f)
                self.windows = [ConversationWindow(**w) for w in data]
                if self.windows:
                    self.current_window = self.windows[-1]
            except:
                self.windows = []


if __name__ == "__main__":
    cm = ContextManager()
    cm.start_fresh_window("gemini")
    cm.add_message("user", "Test message")
    print(f"Windows: {len(cm.windows)}")
    print(f"Briefing: {cm.get_briefing_data()}")
