"""Tests for recorder auto-stop and hotkey handling."""

import importlib.util
import types
import sys
from pathlib import Path


def _load_recorder_module():
    if "sounddevice" not in sys.modules:
        sys.modules["sounddevice"] = types.SimpleNamespace(
            InputStream=object,
            PortAudioError=Exception,
        )
    module_path = Path(__file__).parent.parent / "wanda-voice" / "audio" / "recorder.py"
    spec = importlib.util.spec_from_file_location("wanda_voice_recorder", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


recorder_module = _load_recorder_module()
AudioRecorder = recorder_module.AudioRecorder
HotkeyHandler = recorder_module.HotkeyHandler


class DummyVAD:
    def __init__(self, silence=True, speaking=False):
        self._silence = silence
        self._speaking = speaking

    def is_user_speaking(self):
        return self._speaking

    def silence_exceeded(self):
        return self._silence

    def reset(self):
        return None


def test_vad_auto_stop_reason():
    recorder = AudioRecorder(sample_rate=16000, max_seconds=60, vad=DummyVAD())
    recorder.is_recording = True
    recorder._record_start = 0.0
    recorder._speech_start = 0.0
    reason = recorder._should_auto_stop(now=10.0)
    assert reason == "silence_vad"


def test_hotkey_hold_press_release():
    pressed = {"down": 0, "up": 0}

    def on_press():
        pressed["down"] += 1

    def on_release():
        pressed["up"] += 1

    handler = HotkeyHandler(mode="hold", on_press=on_press, on_release=on_release)
    handler._handle_key_event("down")
    handler._handle_key_event("up")

    assert pressed["down"] == 1
    assert pressed["up"] == 1
