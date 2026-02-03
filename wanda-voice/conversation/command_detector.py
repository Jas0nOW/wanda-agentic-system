# Wanda Voice Assistant - Command Detector
"""Detects natural language commands in speech."""

from typing import Optional


class ConversationalCommandDetector:
    """Detects natural commands with exact and fuzzy matching."""
    
    COMMANDS = {
        "preview": [
            "lies mir vor", "lies vor", "vorlesen", 
            "was hast du verstanden", "zeig mal", "preview",
            "was habe ich gesagt"
        ],
        "send": [
            "abschicken", "senden", "send", "schick ab",
            "ok", "ja", "passt", "go", "los", "das passt"
        ],
        "continue": [
            "weiter", "mach weiter", "fortsetzen", 
            "continue", "mehr", "und"
        ],
        "redo": [
            "nochmal", "von vorn", "neu", "restart", 
            "redo", "von vorne"
        ],
        "cancel": [
            "stop", "abbrechen", "cancel", "nein", 
            "vergiss es", "weg damit", "stopp"
        ]
    }
    
    def detect_command(self, text: str) -> Optional[str]:
        """
        Detect command in natural speech.
        
        Returns:
            Command name or None if no command detected
        """
        if not text:
            return None
            
        text_lower = text.lower().strip()
        
        # Exact match first (highest priority)
        for command, keywords in self.COMMANDS.items():
            if text_lower in keywords:
                return command
        
        # Start/end match (avoid false positives in longer sentences)
        for command, keywords in self.COMMANDS.items():
            for keyword in keywords:
                if text_lower.startswith(keyword) or text_lower.endswith(keyword):
                    return command
        
        # Fuzzy match for very short inputs
        if len(text_lower) < 20:
            for command, keywords in self.COMMANDS.items():
                if any(kw in text_lower for kw in keywords):
                    return command
        
        return None  # No command = user continues speaking
    
    def is_confirmation(self, text: str) -> bool:
        """Check if text is a confirmation."""
        return self.detect_command(text) == "send"
    
    def is_cancellation(self, text: str) -> bool:
        """Check if text is a cancellation."""
        return self.detect_command(text) == "cancel"


if __name__ == "__main__":
    detector = ConversationalCommandDetector()
    tests = [
        ("lies mir vor", "preview"),
        ("ja", "send"),
        ("abschicken", "send"),
        ("stopp", "cancel"),
        ("weiter", "continue"),
        ("Das ist ein normaler Satz", None),
    ]
    for text, expected in tests:
        result = detector.detect_command(text)
        status = "✅" if result == expected else "❌"
        print(f"{status} '{text}' -> {result} (expected: {expected})")
