"""Tests for voice confirmation flow."""

import pytest
import asyncio
from unittest.mock import MagicMock, AsyncMock

from wanda_voice_core.confirmation import (
    ConfirmationFlow, detect_confirmation_command, ConfirmationState,
)
from wanda_voice_core.schemas import RefinerResult, RefinerAction
from wanda_voice_core.event_bus import EventBus


def test_detect_abschicken():
    assert detect_confirmation_command("abschicken") == ConfirmationState.SEND


def test_detect_verandern():
    assert detect_confirmation_command("verändern") == ConfirmationState.EDIT


def test_detect_nochmal():
    assert detect_confirmation_command("nochmal") == ConfirmationState.REDO


def test_detect_stop():
    assert detect_confirmation_command("stop") == ConfirmationState.CANCEL


def test_detect_ja():
    assert detect_confirmation_command("ja") == ConfirmationState.SEND


def test_detect_unknown():
    assert detect_confirmation_command("Das ist ein normaler Satz") is None


@pytest.fixture
def event_bus():
    return EventBus()


@pytest.fixture
def refined():
    return RefinerResult(
        intent="test",
        improved_text="Verbesserte Nachricht",
        do=RefinerAction.SEND,
    )


class TestConfirmationFlow:
    @pytest.mark.asyncio
    async def test_send_action(self, event_bus, refined):
        spoken = []
        flow = ConfirmationFlow(
            event_bus=event_bus,
            tts_speak=lambda t: spoken.append(t),
            stt_listen=lambda: "abschicken",
            timeout=5.0,
        )

        result = await flow.run(refined)
        assert result == ConfirmationState.SEND
        assert any("verbesserte Version" in s for s in spoken)

    @pytest.mark.asyncio
    async def test_cancel_action(self, event_bus, refined):
        flow = ConfirmationFlow(
            event_bus=event_bus,
            tts_speak=lambda t: None,
            stt_listen=lambda: "abbrechen",
            timeout=5.0,
        )
        result = await flow.run(refined)
        assert result == ConfirmationState.CANCEL

    @pytest.mark.asyncio
    async def test_edit_action(self, event_bus, refined):
        flow = ConfirmationFlow(
            event_bus=event_bus,
            tts_speak=lambda t: None,
            stt_listen=lambda: "verändern",
            timeout=5.0,
        )
        result = await flow.run(refined)
        assert result == ConfirmationState.EDIT

    @pytest.mark.asyncio
    async def test_redo_action(self, event_bus, refined):
        flow = ConfirmationFlow(
            event_bus=event_bus,
            tts_speak=lambda t: None,
            stt_listen=lambda: "nochmal",
            timeout=5.0,
        )
        result = await flow.run(refined)
        assert result == ConfirmationState.REDO

    @pytest.mark.asyncio
    async def test_timeout_cancels(self, event_bus, refined):
        """No valid response -> timeout -> cancel."""
        attempt = [0]

        def listen_none():
            attempt[0] += 1
            return None

        flow = ConfirmationFlow(
            event_bus=event_bus,
            tts_speak=lambda t: None,
            stt_listen=listen_none,
            timeout=1.0,
        )
        result = await flow.run(refined)
        assert result == ConfirmationState.CANCEL
        assert attempt[0] >= 2  # Asked twice before timeout
