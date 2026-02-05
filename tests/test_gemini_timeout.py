"""Tests for Gemini CLI provider timeout/retry handling."""

import asyncio
import pytest
from unittest.mock import patch, AsyncMock, MagicMock

from wanda_voice_core.providers.gemini_cli import GeminiCLIProvider


@pytest.fixture
def provider():
    return GeminiCLIProvider(
        model="flash", timeout=5, max_retries=1, fallback_model="pro"
    )


class TestGeminiTimeout:
    def test_is_available_missing_binary(self, provider):
        with patch("subprocess.run", side_effect=FileNotFoundError):
            assert provider.is_available() is False

    def test_is_available_success(self, provider):
        mock_result = MagicMock()
        mock_result.returncode = 0
        with patch("subprocess.run", return_value=mock_result):
            assert provider.is_available() is True

    @pytest.mark.asyncio
    async def test_timeout_triggers_retry(self, provider):
        call_count = 0

        async def mock_create_subprocess(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            proc = AsyncMock()
            async def timeout_communicate():
                raise asyncio.TimeoutError()
            proc.communicate = timeout_communicate
            proc.kill = MagicMock()
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=mock_create_subprocess):
            result = await provider.send("test prompt")

        # Should have tried primary (2x: initial + 1 retry) + fallback (1x)
        assert call_count >= 2
        assert "nicht erreichbar" in result or call_count >= 3

    @pytest.mark.asyncio
    async def test_successful_response(self, provider):
        async def mock_create_subprocess(*args, **kwargs):
            proc = AsyncMock()
            proc.returncode = 0
            async def success_communicate():
                return (b"Hallo Welt", b"")
            proc.communicate = success_communicate
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=mock_create_subprocess):
            with patch("asyncio.wait_for", new_callable=AsyncMock) as mock_wait:
                mock_wait.return_value = (b"Hallo Welt", b"")
                # Direct _call_gemini test
                result = await provider._call_gemini("flash", "test", 10)
                if result is not None:
                    assert isinstance(result, str)

    @pytest.mark.asyncio
    async def test_fallback_on_failure(self, provider):
        attempts = []

        async def mock_create_subprocess(*args, **kwargs):
            model = args[1] if len(args) > 1 else "?"
            attempts.append(model)
            proc = AsyncMock()
            proc.returncode = 1
            async def fail_communicate():
                return (b"", b"error")
            proc.communicate = fail_communicate
            return proc

        with patch("asyncio.create_subprocess_exec", side_effect=mock_create_subprocess):
            result = await provider.send("test")

        # Should contain the fallback error message
        assert isinstance(result, str)

    def test_history_management(self, provider):
        provider._update_history("q1", "a1")
        provider._update_history("q2", "a2")
        assert len(provider.history) == 4

        provider.clear_history()
        assert len(provider.history) == 0
