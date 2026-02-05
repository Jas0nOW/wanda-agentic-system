"""Intent router for WANDA Voice Core."""

from __future__ import annotations
import re
from typing import Optional

from wanda_voice_core.schemas import RouterResult, RouteType


# Voice command patterns (exact match -> "command" route)
COMMAND_KEYWORDS: dict[str, list[str]] = {
    "send": ["abschicken", "senden", "send", "schick ab", "ja", "passt", "go", "los"],
    "cancel": ["stop", "abbrechen", "cancel", "nein", "vergiss es", "stopp"],
    "redo": ["nochmal", "von vorn", "neu", "von vorne", "redo"],
    "edit": ["verändern", "ändern", "bearbeiten", "edit"],
    "readback": ["lies vor", "vorlesen", "lies mir vor", "nochmal vorlesen"],
    "pause": ["wanda pause", "pause"],
    "resume": ["wanda weiter", "hey wanda", "resume"],
}

# Intent keywords -> "refine" route (needs Ollama improvement)
REFINE_KEYWORDS = [
    "brainstorm", "ideen", "optionen", "möglichkeiten", "vorschläge",
    "recherchiere", "research", "finde", "suche",
    "fix", "bug", "error", "fehler", "debug",
    "diktieren", "schreibe auf", "notiere",
]

# Patterns that suggest direct LLM usage
LLM_PATTERNS = [
    re.compile(r"^(was|wie|wo|wann|warum|wer|welche)", re.IGNORECASE),
    re.compile(r"(erkläre|beschreibe|zeige|erzähle)", re.IGNORECASE),
]


class IntentRouter:
    """Routes utterances to command/refine/llm pipelines."""

    def __init__(self, confidence_threshold: float = 0.6):
        self.confidence_threshold = confidence_threshold

    def route(self, text: str) -> RouterResult:
        """Route text to appropriate pipeline."""
        if not text or not text.strip():
            return RouterResult(route=RouteType.LLM, confidence=0.0, notes="empty input")

        normalized = self._normalize(text)

        # 1. Check voice commands (highest priority)
        cmd_result = self._check_commands(normalized)
        if cmd_result:
            return cmd_result

        # 2. Check refine keywords
        if self._needs_refinement(normalized):
            return RouterResult(
                route=RouteType.REFINE,
                confidence=0.7,
                notes="keyword match -> refine",
            )

        # 3. Short inputs (< 5 words) likely need refinement
        word_count = len(normalized.split())
        if word_count < 5:
            return RouterResult(
                route=RouteType.REFINE,
                confidence=0.6,
                notes="short input -> refine for clarity",
            )

        # 4. Default: send to LLM
        return RouterResult(
            route=RouteType.LLM,
            confidence=0.8,
            notes="default -> llm",
        )

    def _check_commands(self, text: str) -> Optional[RouterResult]:
        """Check for voice commands."""
        for cmd_name, keywords in COMMAND_KEYWORDS.items():
            for kw in keywords:
                if text == kw or text.startswith(kw + " ") or text.endswith(" " + kw):
                    return RouterResult(
                        route=RouteType.COMMAND,
                        confidence=0.95,
                        command={"name": cmd_name, "keyword": kw},
                        notes=f"command: {cmd_name}",
                    )
        return None

    def _needs_refinement(self, text: str) -> bool:
        """Check if text contains refine-worthy keywords."""
        return any(kw in text for kw in REFINE_KEYWORDS)

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = text.replace("wunder", "wanda")
        text = text.replace("wander", "wanda")
        text = re.sub(r"[^a-z0-9äöüß\s]", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text
