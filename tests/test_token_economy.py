"""Tests for token economy: caps, redaction, metrics."""

import pytest
from wanda_voice_core.token_economy import (
    estimate_tokens, check_budget, truncate_to_budget,
    summarize_context, redact_sensitive, TokenMetrics,
    MAX_CONTEXT_CHARS, MAX_OUTPUT_TOKENS,
)


class TestEstimateTokens:
    def test_short_text(self):
        assert estimate_tokens("Hallo") >= 1

    def test_longer_text(self):
        text = "Dies ist ein längerer Satz mit mehreren Wörtern."
        tokens = estimate_tokens(text)
        assert tokens > 5

    def test_empty_text(self):
        assert estimate_tokens("") == 1  # minimum 1


class TestCheckBudget:
    def test_within_budget(self):
        assert check_budget("Kurzer Text") is True

    def test_exceeds_budget(self):
        long_text = "x" * (MAX_OUTPUT_TOKENS * 10)
        assert check_budget(long_text) is False


class TestTruncateToBudget:
    def test_short_text_unchanged(self):
        text = "Kurzer Text"
        assert truncate_to_budget(text) == text

    def test_long_text_truncated(self):
        text = "x" * (MAX_CONTEXT_CHARS + 1000)
        result = truncate_to_budget(text)
        assert len(result) <= MAX_CONTEXT_CHARS + 3  # +3 for "..."

    def test_truncate_at_sentence(self):
        text = "Erster Satz. " * 1000
        result = truncate_to_budget(text, max_chars=100)
        assert result.endswith(".")


class TestRedactSensitive:
    def test_redact_api_key(self):
        text = "My key is sk-abcdefghijklmnopqrstuvwxyz123456789"
        result = redact_sensitive(text)
        assert "sk-" not in result
        assert "[REDACTED_KEY]" in result

    def test_redact_long_hex(self):
        text = f"Token: {'a' * 50}"
        result = redact_sensitive(text)
        assert "[REDACTED_HEX]" in result

    def test_redact_password(self):
        text = "password: mysecretpassword123"
        result = redact_sensitive(text)
        assert "[REDACTED_SECRET]" in result

    def test_safe_text_unchanged(self):
        text = "Dies ist ein normaler Satz ohne Geheimnisse."
        result = redact_sensitive(text)
        assert result == text

    def test_redact_cert(self):
        text = "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAK\n-----END RSA PRIVATE KEY-----"
        result = redact_sensitive(text)
        assert "[REDACTED_CERT]" in result


class TestSummarizeContext:
    def test_empty_messages(self):
        assert summarize_context([]) == ""

    def test_few_messages(self):
        msgs = [
            {"role": "user", "content": "Hallo"},
            {"role": "assistant", "content": "Hi!"},
        ]
        result = summarize_context(msgs)
        assert "Hallo" in result
        assert "Hi!" in result

    def test_respects_max_chars(self):
        msgs = [
            {"role": "user", "content": "x" * 500}
            for _ in range(100)
        ]
        result = summarize_context(msgs, max_chars=1000)
        assert len(result) <= 1100  # some tolerance for role prefix


class TestTokenMetrics:
    def test_update(self):
        m = TokenMetrics()
        m.update("Hallo Wanda", "Antwort hier", latency_ms=150.0)
        assert m.chars_in == 11
        assert m.chars_out == 12
        assert m.latency_ms == 150.0
        assert m.token_est_in > 0
        assert m.token_est_out > 0

    def test_to_dict(self):
        m = TokenMetrics()
        m.update("a", "b", 10.0)
        d = m.to_dict()
        assert "chars_in" in d
        assert "latency_ms" in d
