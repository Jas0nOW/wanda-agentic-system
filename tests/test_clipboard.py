"""Tests for clipboard insertion."""

import pytest
from unittest.mock import patch, MagicMock

from wanda_voice_core.engine import WandaVoiceEngine
from wanda_voice_core.config import VoiceCoreConfig


@pytest.fixture
def engine():
    config = VoiceCoreConfig()
    return WandaVoiceEngine(config)


class TestClipboard:
    def test_copy_to_clipboard_wl_copy(self, engine):
        engine._clipboard_tool = ["wl-copy"]
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.communicate = MagicMock(return_value=(b"", b""))

        with patch("subprocess.Popen", return_value=mock_proc) as mock_popen:
            result = engine.copy_to_clipboard("Test text")
            assert result is True
            mock_popen.assert_called_once()
            # Verify text was sent to stdin
            mock_proc.communicate.assert_called_once_with(input=b"Test text")

    def test_copy_to_clipboard_xclip(self, engine):
        engine._clipboard_tool = ["xclip", "-selection", "clipboard"]
        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.communicate = MagicMock(return_value=(b"", b""))

        with patch("subprocess.Popen", return_value=mock_proc) as mock_popen:
            result = engine.copy_to_clipboard("Hallo Wanda")
            assert result is True

    def test_copy_fails_no_tool(self, engine):
        engine._clipboard_tool = None
        result = engine.copy_to_clipboard("test")
        assert result is False

    def test_copy_fails_on_error(self, engine):
        engine._clipboard_tool = ["wl-copy"]
        with patch("subprocess.Popen", side_effect=OSError("no such file")):
            result = engine.copy_to_clipboard("test")
            assert result is False

    def test_type_text_wtype(self, engine):
        engine._typing_tool = ["wtype"]
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(returncode=0)
            result = engine.type_text("Hello")
            assert result is True
            mock_run.assert_called_once()

    def test_type_text_no_tool(self, engine):
        engine._typing_tool = None
        result = engine.type_text("test")
        assert result is False

    def test_paste_to_active_window(self, engine):
        engine._clipboard_tool = ["wl-copy"]
        engine._typing_tool = ["wtype"]

        mock_proc = MagicMock()
        mock_proc.returncode = 0
        mock_proc.communicate = MagicMock(return_value=(b"", b""))

        with patch("subprocess.Popen", return_value=mock_proc):
            with patch("subprocess.run") as mock_run:
                result = engine.paste_to_active_window("Pasted text")
                assert result is True
