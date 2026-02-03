# Wanda Voice Assistant - Guardrails
"""Redact sensitive information before sending to AI."""

import re
from typing import List, Dict, Optional


class Guardrails:
    """Redact sensitive information before sending to AI."""
    
    DEFAULT_PATTERNS = {
        "api_key": r"(sk-[a-zA-Z0-9]{20,})",
        "openai_key": r"(sk-proj-[a-zA-Z0-9_-]{20,})",
        "password": r"(password|passwd|pwd|passwort)\s*[:=]\s*\S+",
        "bearer": r"(Bearer\s+[a-zA-Z0-9_-]{20,})",
        "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
        "ip_address": r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        "credit_card": r"\b\d{4}[\s-]?\d{4}[\s-]?\d{4}[\s-]?\d{4}\b",
        "private_key": r"-----BEGIN (RSA |EC |)PRIVATE KEY-----",
        "aws_key": r"AKIA[0-9A-Z]{16}",
    }
    
    def __init__(self, enabled: bool = True, custom_patterns: Optional[Dict[str, str]] = None):
        self.enabled = enabled
        self.patterns = self.DEFAULT_PATTERNS.copy()
        if custom_patterns:
            self.patterns.update(custom_patterns)
    
    def redact(self, text: str) -> str:
        """Redact sensitive strings."""
        if not self.enabled:
            return text
        
        for name, pattern in self.patterns.items():
            text = re.sub(
                pattern, 
                f"[REDACTED:{name}]", 
                text, 
                flags=re.IGNORECASE
            )
        
        return text
    
    def has_sensitive_data(self, text: str) -> bool:
        """Check if text contains sensitive data."""
        for pattern in self.patterns.values():
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def add_pattern(self, name: str, pattern: str):
        """Add custom pattern."""
        self.patterns[name] = pattern


if __name__ == "__main__":
    guard = Guardrails()
    
    tests = [
        "My API key is sk-1234567890abcdefghijkl",
        "password=supersecret123",
        "Email: test@example.com",
        "Normal text without secrets",
    ]
    
    for text in tests:
        redacted = guard.redact(text)
        print(f"'{text}'\n  -> '{redacted}'\n")
