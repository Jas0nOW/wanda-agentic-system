"""Tests for refiner toggle behavior."""

import pytest
import asyncio

from wanda_voice_core.engine import WandaVoiceEngine
from wanda_voice_core.providers.base import ProviderBase


class DummyProvider(ProviderBase):
    name = "dummy"

    async def send(self, prompt: str, context=None) -> str:
        return "ok"

    def is_available(self) -> bool:
        return True


@pytest.mark.asyncio
async def test_refiner_disabled_skips_refine():
    engine = WandaVoiceEngine()
    engine.set_providers(DummyProvider())
    engine.set_io(tts_speak=lambda t: None, stt_listen=lambda: None)

    engine.set_refiner_enabled(False)

    # If refiner is disabled, this should not call refiner
    result = await engine.process_text("brainstorm ideen", skip_confirmation=True)
    assert result.improved_text == "brainstorm ideen"
    assert result.response_text == "ok"
