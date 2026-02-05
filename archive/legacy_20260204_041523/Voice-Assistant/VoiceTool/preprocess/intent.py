# Wanda Voice Assistant - Intent Detection & Prompt Preprocessing
"""Intent detection and prompt rewriting."""

import re
from typing import Dict, Tuple


class IntentDetector:
    """Detect user intent from transcript and rewrite prompt."""
    
    # Intent keywords (case-insensitive)
    INTENT_KEYWORDS = {
        "brainstorm": [
            "brainstorm", "ideen", "optionen", "möglichkeiten",
            "vorschläge", "alternativen", "brainstorming"
        ],
        "research": [
            "recherchiere", "research", "finde", "suche", "quellen",
            "dokumentation", "informationen", "nachschlagen"
        ],
        "buildfix": [
            "fix", "bug", "error", "fehler", "problem", "stacktrace",
            "debug", "repariere", "löse", "behebe"
        ],
        "dictation": [
            "diktieren", "nur text", "schreibe auf", "notiere"
        ]
    }
    
    # Prompt templates
    TEMPLATES = {
        "brainstorm": """Du bist ein Brainstorm-Partner. Liefere Optionen und Trade-offs. 
Keine Aufgabenliste, außer ich frage explizit danach.

User: {prompt}""",
        
        "research": """Finde verlässliche Quellen, nenne Links und fasse zusammen. 
Gib danach konkrete Next Steps.

User: {prompt}""",
        
        "buildfix": """Stelle zuerst Diagnosefragen nur wenn nötig, sonst gib direkte Schritte, 
Kommandos und Definition of Done.

User: {prompt}""",
        
        "default": "{prompt}"
    }
    
    def __init__(self):
        """Initialize intent detector."""
        pass
    
    def detect_intent(self, text: str) -> str:
        """
        Detect intent from text based on keywords.
        
        Args:
            text: User's text
        
        Returns:
            Intent name (brainstorm, research, buildfix, dictation, default)
        """
        text_lower = text.lower()
        
        # Check each intent
        for intent, keywords in self.INTENT_KEYWORDS.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return intent
        
        return "default"
    
    def rewrite_prompt(self, text: str, intent: str = None) -> Tuple[str, str]:
        """
        Rewrite prompt based on intent.
        
        Args:
            text: Original text
            intent: Intent (auto-detected if None)
        
        Returns:
            Tuple of (intent, rewritten_prompt)
        """
        if intent is None:
            intent = self.detect_intent(text)
        
        # Don't rewrite for dictation mode
        if intent == "dictation":
            return (intent, text)
        
        # Get template
        template = self.TEMPLATES.get(intent, self.TEMPLATES["default"])
        
        # Apply template
        rewritten = template.format(prompt=text)
        
        return (intent, rewritten)
    
    def apply_guardrails(self, text: str, redact_secrets: bool = False) -> str:
        """
        Apply safety guardrails (optional).
        
        Args:
            text: Text to check
            redact_secrets: Whether to redact potential secrets
        
        Returns:
            Processed text
        """
        if not redact_secrets:
            return text
        
        # Simple regex-based redaction (can be extended)
        # Redact things that look like API keys, tokens, etc.
        
        # Example: sk-... (OpenAI style)
        text = re.sub(r'\bsk-[a-zA-Z0-9]{32,}\b', '[REDACTED_KEY]', text)
        
        # Example: long hex strings (potential tokens)
        text = re.sub(r'\b[a-f0-9]{40,}\b', '[REDACTED_TOKEN]', text)
        
        return text


# Test function
if __name__ == "__main__":
    print("Testing Intent Detector...")
    detector = IntentDetector()
    
    test_cases = [
        "Brainstorme mir Ideen für ein neues Feature",
        "Recherchiere die besten Python Testing Frameworks",
        "Fix den Bug in meinem Code",
        "Wie geht es dir heute?"
    ]
    
    for text in test_cases:
        intent, rewritten = detector.rewrite_prompt(text)
        print(f"\n📝 Input: {text}")
        print(f"🎯 Intent: {intent}")
        print(f"✏️  Rewritten:\n{rewritten[:100]}...")
