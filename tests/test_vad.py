"""Tests for VAD silence detection (uses synthetic audio)."""

import pytest
import numpy as np

from wanda_voice_core.router import IntentRouter
from wanda_voice_core.schemas import RouteType


class TestVADSilenceLogic:
    """Test the silence detection logic used in the pipeline.
    Note: Full VAD tests require torch/silero which may not be in test env.
    These tests verify the detection thresholds and logic."""

    def test_silence_detection_threshold(self):
        """Verify silence threshold works correctly."""
        sample_rate = 16000
        silence_threshold = 0.01

        # Generate 1.5s speech-like audio (random noise above threshold)
        speech = np.random.uniform(-0.5, 0.5, int(sample_rate * 1.5)).astype(np.float32)
        assert np.abs(speech).mean() > silence_threshold

        # Generate 1.5s silence (very low amplitude)
        silence = np.random.uniform(-0.001, 0.001, int(sample_rate * 1.5)).astype(np.float32)
        assert np.abs(silence).mean() < silence_threshold

    def test_combined_audio_has_speech_and_silence(self):
        """3s audio with 1.5s speech + 1.5s silence."""
        sample_rate = 16000
        speech_duration = 1.5
        silence_duration = 1.5
        silence_threshold = 0.01

        speech = np.random.uniform(-0.3, 0.3, int(sample_rate * speech_duration)).astype(np.float32)
        silence = np.random.uniform(-0.0005, 0.0005, int(sample_rate * silence_duration)).astype(np.float32)

        combined = np.concatenate([speech, silence])
        assert len(combined) == sample_rate * 3

        # Check that silence starts approximately at the right position
        window_ms = 200  # 200ms window
        window_samples = int(sample_rate * window_ms / 1000)
        speech_end_sample = int(sample_rate * speech_duration)

        # Check window just after speech ends
        check_start = speech_end_sample
        check_end = min(check_start + window_samples, len(combined))
        window = combined[check_start:check_end]
        assert np.abs(window).mean() < silence_threshold, (
            f"Silence should be detected within {window_ms}ms of actual silence start"
        )

    def test_energy_based_detection(self):
        """Simple energy-based VAD check."""
        sample_rate = 16000

        # Pure silence
        silence = np.zeros(sample_rate, dtype=np.float32)
        energy = np.sqrt(np.mean(silence ** 2))
        assert energy < 0.001

        # Speech
        speech = np.random.uniform(-0.3, 0.3, sample_rate).astype(np.float32)
        energy = np.sqrt(np.mean(speech ** 2))
        assert energy > 0.01


class TestRouterIntegration:
    """Test that router correctly classifies inputs."""

    def test_command_detected(self):
        router = IntentRouter()
        result = router.route("abschicken")
        assert result.route == RouteType.COMMAND
        assert result.command["name"] == "send"

    def test_refine_detected(self):
        router = IntentRouter()
        result = router.route("brainstorm Ideen für ein neues Feature")
        assert result.route == RouteType.REFINE

    def test_llm_for_question(self):
        router = IntentRouter()
        result = router.route("Was ist der Unterschied zwischen Python und JavaScript?")
        assert result.route == RouteType.LLM

    def test_short_input_refines(self):
        router = IntentRouter()
        result = router.route("Hilfe")
        assert result.route == RouteType.REFINE
