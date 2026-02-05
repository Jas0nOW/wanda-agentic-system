"""Token economy: caps, metrics, redaction for WANDA Voice Core."""

from __future__ import annotations
import re
from dataclasses import dataclass

# Hard caps
MAX_CONTEXT_CHARS = 8000
MAX_TURNS = 12
MAX_OUTPUT_TOKENS = 2048

# Approximate chars per token (German text is ~3.5 chars/token)
CHARS_PER_TOKEN = 3.5


def estimate_tokens(text: str) -> int:
    """Estimate token count from character count."""
    return max(1, int(len(text) / CHARS_PER_TOKEN))


def check_budget(text: str, max_tokens: int = MAX_OUTPUT_TOKENS) -> bool:
    """Check if text is within token budget."""
    return estimate_tokens(text) <= max_tokens


def truncate_to_budget(text: str, max_chars: int = MAX_CONTEXT_CHARS) -> str:
    """Truncate text to fit within character budget."""
    if len(text) <= max_chars:
        return text
    # Truncate at sentence boundary if possible
    truncated = text[:max_chars]
    last_period = truncated.rfind(".")
    if last_period > max_chars * 0.7:
        return truncated[: last_period + 1]
    return truncated + "..."


def summarize_context(
    messages: list[dict[str, str]], max_chars: int = MAX_CONTEXT_CHARS
) -> str:
    """Build a rolling context summary from message history, staying within budget."""
    if not messages:
        return ""

    # Take last MAX_TURNS pairs
    recent = messages[-(MAX_TURNS * 2) :]

    parts: list[str] = []
    total = 0
    for msg in reversed(recent):
        role = msg.get("role", "user")
        content = msg.get("content", "")
        # Truncate individual messages if very long
        if len(content) > 500:
            content = content[:500] + "..."
        entry = f"{role}: {content}"
        if total + len(entry) > max_chars:
            break
        parts.insert(0, entry)
        total += len(entry) + 1  # +1 for newline

    return "\n".join(parts)


# Redaction patterns
_PATTERNS = [
    (re.compile(r"\bsk-[a-zA-Z0-9]{20,}\b"), "[REDACTED_KEY]"),
    (re.compile(r"\b[a-f0-9]{40,}\b"), "[REDACTED_HEX]"),
    (re.compile(r"[A-Za-z0-9+/]{40,}={0,2}"), "[REDACTED_B64]"),
    (
        re.compile(r"-----BEGIN [A-Z ]+-----[\s\S]*?-----END [A-Z ]+-----"),
        "[REDACTED_CERT]",
    ),
    (
        re.compile(
            r"(?:password|passwd|secret|token)\s*[:=]\s*(?!\[REDACTED_)(?![a-f0-9]{40,}\b)\S+",
            re.IGNORECASE,
        ),
        "[REDACTED_SECRET]",
    ),
    # Stack traces (multi-line, simplified)
    (
        re.compile(r"Traceback \(most recent call last\):[\s\S]{0,2000}?(?:\n\S|\Z)"),
        "[REDACTED_STACKTRACE]",
    ),
]


def redact_sensitive(text: str) -> str:
    """Strip secrets, hex strings, base64 blobs, stack traces."""
    for pattern, replacement in _PATTERNS:
        text = pattern.sub(replacement, text)
    return text


@dataclass
class TokenMetrics:
    chars_in: int = 0
    chars_out: int = 0
    token_est_in: int = 0
    token_est_out: int = 0
    latency_ms: float = 0.0

    def update(self, text_in: str, text_out: str, latency_ms: float = 0.0) -> None:
        self.chars_in = len(text_in)
        self.chars_out = len(text_out)
        self.token_est_in = estimate_tokens(text_in)
        self.token_est_out = estimate_tokens(text_out)
        self.latency_ms = latency_ms

    def to_dict(self) -> dict:
        return {
            "chars_in": self.chars_in,
            "chars_out": self.chars_out,
            "token_est_in": self.token_est_in,
            "token_est_out": self.token_est_out,
            "latency_ms": self.latency_ms,
        }
