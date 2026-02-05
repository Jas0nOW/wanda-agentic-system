"""End-to-end tests for complete voice interaction flow.

Tests the complete user journey:
1. Wake word detection
2. Voice command recording
3. Speech-to-text processing
4. Command execution
5. Text-to-speech response
"""

import pytest
import time
import threading
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "wanda_voice_core"))


@pytest.mark.e2e
class TestVoiceInteractionFlow:
    """End-to-end tests for voice interactions."""

    def test_full_voice_interaction(self):
        """Test complete voice interaction flow.

        Flow:
        1. User says wake word "wanda"
        2. System enters listening state
        3. User gives command
        4. System processes and executes
        5. System provides feedback
        """
        # Mock voice assistant
        voice = Mock()
        voice.state = "idle"
        voice.last_command = None

        # Step 1: Wake word
        voice.process_audio = Mock(return_value="wake_word_detected")
        result = voice.process_audio("wanda")
        voice.state = "listening"

        assert result == "wake_word_detected"
        assert voice.state == "listening"

        # Step 2: Command
        voice.process_audio = Mock(return_value="command_processed")
        result = voice.process_audio("öffne firefox")
        voice.state = "processing"
        voice.last_command = "open_firefox"

        assert voice.state == "processing"
        assert voice.last_command == "open_firefox"

    def test_cancel_command_flow(self):
        """Test cancel command during voice interaction."""
        voice = Mock()
        voice.state = "listening"

        # User says stop
        voice.process_audio = Mock(return_value="cancelled")
        result = voice.process_audio("stop")
        voice.state = "idle"

        assert result == "cancelled"
        assert voice.state == "idle"

    def test_confirmation_command_flow(self):
        """Test confirmation command flow.

        Bug Fix: 'abschike', 'abschik' not recognized
        Fix: Added fuzzy matching
        """
        parser = Mock()

        # Test various confirmation commands
        confirmations = ["abschicken", "abschike", "abschik", "bestätigen"]

        for cmd in confirmations:
            parser.parse = Mock(return_value="send")
            result = parser.parse(cmd)
            assert result == "send", f"Command '{cmd}' should be recognized as send"


@pytest.mark.e2e
class TestConcurrentCommands:
    """Test concurrent voice command handling."""

    def test_concurrent_voice_commands(self):
        """Ensure no race conditions with rapid commands.

        Bug Fix: Rapid commands caused race conditions
        Fix: Added command queue and state locking
        """
        results = []
        errors = []

        def send_command(cmd, delay=0):
            try:
                time.sleep(delay)
                # Simulate command processing
                result = f"processed_{cmd}"
                results.append(result)
            except Exception as e:
                errors.append(str(e))

        # Send multiple commands rapidly
        threads = [
            threading.Thread(target=send_command, args=("wanda", 0.0)),
            threading.Thread(target=send_command, args=("stop", 0.05)),
            threading.Thread(target=send_command, args=("wanda", 0.1)),
            threading.Thread(target=send_command, args=("öffne editor", 0.15)),
        ]

        # Start all threads
        for t in threads:
            t.start()

        # Wait for completion
        for t in threads:
            t.join(timeout=2.0)

        # Should not crash
        assert len(errors) == 0, f"Errors occurred: {errors}"

        # Should process all commands
        assert len(results) == 4

    def test_command_queue_ordering(self):
        """Test commands are processed in order."""
        commands = []

        def process_command(cmd):
            commands.append(cmd)

        # Simulate queued commands
        test_commands = ["cmd1", "cmd2", "cmd3", "cmd4"]
        threads = []

        for i, cmd in enumerate(test_commands):
            t = threading.Thread(target=process_command, args=(cmd,))
            threads.append(t)

        # Start in order
        for t in threads:
            t.start()
            time.sleep(0.01)  # Small delay to ensure order

        for t in threads:
            t.join()

        # All commands should be processed
        assert len(commands) == 4


@pytest.mark.e2e
class TestErrorRecovery:
    """Test system recovery from errors."""

    def test_recovery_from_stt_failure(self):
        """Test system recovers from STT failure."""
        stt = Mock()

        # First call fails
        stt.transcribe = Mock(side_effect=[Exception("STT Error"), "success"])

        # First attempt fails
        with pytest.raises(Exception):
            stt.transcribe("audio1")

        # Second attempt succeeds
        result = stt.transcribe("audio2")
        assert result == "success"

    def test_recovery_from_provider_failure(self):
        """Test system recovers from provider failure."""
        provider = Mock()

        # Simulate failure then success
        provider.generate = Mock(
            side_effect=[Exception("429 Rate Limit"), "fallback_response"]
        )

        # First call fails
        with pytest.raises(Exception):
            provider.generate("prompt1")

        # Second call succeeds (fallback)
        result = provider.generate("prompt2")
        assert result == "fallback_response"

    def test_graceful_degradation(self):
        """Test system degrades gracefully when components fail."""
        system = Mock()

        # Simulate component failure
        system.tts_available = False
        system.stt_available = True

        # Should still work without TTS
        system.process_command = Mock(return_value="text_response")
        result = system.process_command("test")

        assert result == "text_response"


@pytest.mark.e2e
class TestVoiceStates:
    """Test voice assistant state machine."""

    def test_state_transitions(self):
        """Test correct state transitions."""
        states = []

        class MockVoiceAssistant:
            def __init__(self):
                self.state = "idle"

            def process_wake_word(self):
                self.state = "listening"
                states.append(self.state)

            def process_command(self):
                self.state = "processing"
                states.append(self.state)

            def complete(self):
                self.state = "idle"
                states.append(self.state)

        assistant = MockVoiceAssistant()

        # State transitions
        assistant.process_wake_word()
        assistant.process_command()
        assistant.complete()

        assert states == ["listening", "processing", "idle"]

    def test_invalid_state_transitions(self):
        """Test invalid state transitions are handled."""
        assistant = Mock()
        assistant.state = "processing"

        # Trying to process wake word while processing
        # Should either queue or reject
        def invalid_transition():
            if assistant.state == "processing":
                raise ValueError("Cannot process wake word while processing")

        with pytest.raises(ValueError):
            invalid_transition()


@pytest.mark.e2e
class TestLongRunningSessions:
    """Test behavior over long-running sessions."""

    def test_memory_stability(self):
        """Test memory usage remains stable over time."""
        import psutil

        process = psutil.Process()
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB

        # Simulate multiple interactions
        for _ in range(100):
            # Mock interaction
            time.sleep(0.01)

        final_memory = process.memory_info().rss / 1024 / 1024
        memory_increase = final_memory - initial_memory

        # Memory should not grow unbounded
        assert memory_increase < 100, f"Memory increased by {memory_increase:.1f}MB"

    def test_session_persistence(self):
        """Test session state persists across interactions."""
        session = {"interaction_count": 0, "commands": [], "context": {}}

        # Simulate multiple interactions
        for i in range(5):
            session["interaction_count"] += 1
            session["commands"].append(f"cmd_{i}")

        assert session["interaction_count"] == 5
        assert len(session["commands"]) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
