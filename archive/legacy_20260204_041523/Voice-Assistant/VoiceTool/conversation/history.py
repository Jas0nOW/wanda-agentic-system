# Wanda Voice Assistant - Conversation History
"""Multi-turn conversation history with persistence."""

import json
from pathlib import Path
from typing import List, Dict, Optional


class ConversationHistory:
    """Manage conversation history for context."""
    
    def __init__(self, max_turns: int = 12, persist: bool = False, 
                 persist_path: Optional[str] = None):
        self.max_turns = max_turns
        self.persist = persist
        self.persist_path = Path(persist_path) if persist_path else Path.home() / ".wanda" / "history.json"
        self.history: List[Dict[str, str]] = []
        
        if persist:
            self._load()
    
    def add_turn(self, role: str, content: str):
        """Add a turn to history."""
        self.history.append({"role": role, "content": content})
        
        # Trim to max_turns
        max_messages = self.max_turns * 2
        if len(self.history) > max_messages:
            self.history = self.history[-max_messages:]
        
        if self.persist:
            self._save()
    
    def add_user(self, content: str):
        """Add user message."""
        self.add_turn("user", content)
    
    def add_assistant(self, content: str):
        """Add assistant message."""
        self.add_turn("assistant", content)
    
    def get_context(self) -> str:
        """Get history as context string."""
        lines = []
        for turn in self.history:
            role = "User" if turn["role"] == "user" else "Wanda"
            lines.append(f"{role}: {turn['content']}")
        return "\n".join(lines)
    
    def get_last_user_message(self) -> Optional[str]:
        """Get last user message."""
        for turn in reversed(self.history):
            if turn["role"] == "user":
                return turn["content"]
        return None
    
    def get_last_assistant_message(self) -> Optional[str]:
        """Get last assistant message."""
        for turn in reversed(self.history):
            if turn["role"] == "assistant":
                return turn["content"]
        return None
    
    def clear(self):
        """Clear history."""
        self.history = []
        if self.persist:
            self._save()
    
    def _save(self):
        """Save to disk."""
        self.persist_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.persist_path, "w") as f:
            json.dump(self.history, f, indent=2)
    
    def _load(self):
        """Load from disk."""
        if self.persist_path.exists():
            try:
                with open(self.persist_path) as f:
                    self.history = json.load(f)
            except:
                self.history = []


if __name__ == "__main__":
    history = ConversationHistory(max_turns=3)
    history.add_user("Hallo")
    history.add_assistant("Hi! Wie kann ich helfen?")
    history.add_user("Brainstorme Ideen")
    print(history.get_context())
