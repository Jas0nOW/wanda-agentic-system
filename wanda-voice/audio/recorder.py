# Wanda Voice Assistant - Audio Recorder
"""Audio recording with hotkey trigger."""

import queue
import sys
import threading
import time
import numpy as np
import sounddevice as sd
from typing import Optional, Callable


class AudioRecorder:
    """Audio recorder with toggle hotkey."""

    def __init__(
        self,
        sample_rate: int = 16000,
        max_seconds: int = 30,
        silence_timeout: float = 2.5,
        silence_threshold: float = 0.008,
        min_seconds: float = 0.5,
        vad: Optional[object] = None,
        min_speech_ms: int = 150,
        hangover_frames: int = 8,
        on_auto_stop: Optional[Callable[[np.ndarray], None]] = None,
    ):
        """
        Initialize audio recorder.

        Args:
            sample_rate: Sample rate for recording (16000 recommended for STT)
            max_seconds: Maximum recording duration
        """
        self.sample_rate = sample_rate
        self.max_seconds = max_seconds
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.stream = None
        self.silence_timeout = silence_timeout
        self.silence_threshold = silence_threshold
        self.min_seconds = min_seconds
        self.vad = vad
        self.min_speech_ms = min_speech_ms
        self.hangover_frames = hangover_frames
        self.on_auto_stop = on_auto_stop
        self._record_start = None
        self._last_voice = None
        self._monitor_thread = None
        self._speech_start = None
        self._stop_lock = threading.Lock()
        self._stop_reason = None
        self._last_audio = None

        print(
            f"[Audio] Recorder initialized ({sample_rate}Hz, max {max_seconds}s, silence {silence_timeout}s)"
        )

    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream."""
        if status:
            print(f"[Audio] Status: {status}")

        if self.is_recording:
            try:
                energy = float(np.abs(indata).mean())
                if self.vad:
                    try:
                        self.vad.push_audio(indata.copy().flatten())
                    except Exception:
                        pass
                if energy >= self.silence_threshold and not self.vad:
                    self._last_voice = time.time()
            except Exception:
                pass
            # Copy data to avoid overwrite
            self.audio_queue.put(indata.copy())

    def _is_mic_muted(self) -> bool:
        try:
            import subprocess

            result = subprocess.run(
                ["pactl", "list", "sources"], capture_output=True, text=True, timeout=2
            )
            if "Mute: yes" in result.stdout:
                return True
        except Exception:
            pass
        return False

    def start_recording(self):
        """Start audio recording."""
        if self.is_recording:
            print("[Audio] Already recording")
            return

        if self._is_mic_muted():
            print("[Audio] ❌ Microphone is muted - please unmute to record")
            return

        print("[Audio] 🎤 Recording started...")
        self.is_recording = True
        self._record_start = time.time()
        self._last_voice = self._record_start
        self._speech_start = None
        self._stop_reason = None
        self._last_audio = None

        if self.vad:
            try:
                self.vad.reset()
            except Exception:
                pass

        # Clear queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except:
                break

        # Start stream if not already running
        if self.stream is None:
            try:
                self.stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype="float32",
                    callback=self._audio_callback,
                    blocksize=1024,
                )
                self.stream.start()
                self._start_monitor()
            except sd.PortAudioError as e:
                print(f"[Audio] ❌ Failed to open audio device: {e}")
                print("[Audio] Tip: Check if microphone is connected and not in use")
                self.is_recording = False
            except Exception as e:
                print(f"[Audio] ❌ Audio error: {e}")
                self.is_recording = False

    def _start_monitor(self):
        if self._monitor_thread and self._monitor_thread.is_alive():
            return
        self._monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()

    def _monitor_loop(self):
        while self.is_recording:
            try:
                now = time.time()
                reason = self._should_auto_stop(now)
                if reason:
                    self._auto_stop(reason)
                    return
            except Exception:
                pass
            time.sleep(0.1)

    def _should_auto_stop(self, now: float) -> Optional[str]:
        if self._record_start and now - self._record_start > self.max_seconds:
            return "max_seconds"
        if self.vad:
            if self.vad.is_user_speaking():
                if self._speech_start is None:
                    self._speech_start = now
                self._last_voice = now
            record_start = self._record_start if self._record_start is not None else now
            if (
                self._speech_start is not None
                and self.vad.silence_exceeded()
                and now - self._speech_start >= (self.min_speech_ms / 1000.0)
                and now - record_start > self.min_seconds
            ):
                return "silence_vad"
        else:
            record_start = self._record_start if self._record_start is not None else now
            if (
                self._last_voice
                and now - self._last_voice > self.silence_timeout
                and now - record_start > self.min_seconds
            ):
                return "silence_energy"
        return None

    def _auto_stop(self, reason: str):
        with self._stop_lock:
            if not self.is_recording:
                return
            self._stop_reason = reason
        audio = self.stop_recording()
        self._last_audio = audio
        if audio is not None and self.on_auto_stop:
            self.on_auto_stop(audio)

    def stop_recording(self) -> Optional[np.ndarray]:
        """
        Stop audio recording and return recorded audio.

        Returns:
            numpy array of audio data (float32), or None if no data
        """
        with self._stop_lock:
            if not self.is_recording:
                print("[Audio] Not recording")
                return None

        reason = self._stop_reason or "manual"
        print(f"[Audio] ⏸️  Recording stopped ({reason})")
        self.is_recording = False
        self._record_start = None
        self._last_voice = None
        self._speech_start = None

        # Collect audio data from queue
        audio_chunks = []
        while not self.audio_queue.empty():
            audio_chunks.append(self.audio_queue.get())

        if not audio_chunks:
            print("[Audio] No audio data recorded")
            return None

        # Concatenate chunks
        audio_data = np.concatenate(audio_chunks, axis=0)

        # Flatten to 1D if needed
        if audio_data.ndim > 1:
            audio_data = audio_data.flatten()

        duration = len(audio_data) / self.sample_rate
        print(f"[Audio] Recorded {duration:.1f}s ({len(audio_data)} samples)")

        return audio_data

    def cleanup(self):
        """Cleanup audio stream."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        print("[Audio] Cleanup done")

    def consume_last_audio(self) -> Optional[np.ndarray]:
        audio = self._last_audio
        self._last_audio = None
        return audio

    def get_last_stop_reason(self) -> Optional[str]:
        reason = self._stop_reason
        self._stop_reason = None
        return reason

    def set_vad(self, vad: Optional[object]) -> None:
        """Attach or replace VAD instance."""
        self.vad = vad


# Hotkey handler (evdev-based, for global hotkey)
class HotkeyHandler:
    """Handle hotkey triggers using evdev."""

    def __init__(
        self,
        key: str = "rightctrl",
        mode: str = "toggle",
        on_toggle: Optional[Callable] = None,
        on_press: Optional[Callable] = None,
        on_release: Optional[Callable] = None,
    ):
        """
        Initialize hotkey handler.

        Args:
            key: Key to use as hotkey (e.g., 'rightctrl')
            on_toggle: Callback function called on toggle
        """
        self.key = key
        self.mode = mode
        self.on_toggle = on_toggle
        self.on_press = on_press
        self.on_release = on_release
        self.running = False
        self.thread = None
        self.stdin_thread = None

        print(f"[Hotkey] Handler initialized ({key})")

    def start(self):
        """Start hotkey listener in background thread."""
        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._listener_loop, daemon=True)
        self.thread.start()
        print("[Hotkey] Listener started")

    def stop(self):
        """Stop hotkey listener."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        if self.stdin_thread:
            self.stdin_thread.join(timeout=1)
        print("[Hotkey] Listener stopped")

    def _listener_loop(self):
        """Main listener loop (evdev-based)."""
        try:
            import evdev
            from evdev import ecodes

            # Find keyboard device
            device = self._find_keyboard()
            if not device:
                print("[Hotkey] No keyboard found. Falling back to terminal mode.")
                print(
                    "[Hotkey] Tip: Add user to 'input' group: sudo usermod -a -G input $USER"
                )
                self._start_stdin_listener("no-keyboard")
                return

            print(f"[Hotkey] Listening on: {device.name}")

            ctrl_pressed = False
            key_code = self._resolve_key_code(ecodes)

            for event in device.read_loop():
                if not self.running:
                    break

                if event.type == ecodes.EV_KEY:
                    key = evdev.categorize(event)

                    if key.scancode == key_code:
                        if key.keystate == key.key_down and not ctrl_pressed:
                            ctrl_pressed = True
                            self._handle_key_event("down")
                        elif key.keystate == key.key_up:
                            ctrl_pressed = False
                            self._handle_key_event("up")

        except ImportError:
            print("[Hotkey] evdev not available, hotkey disabled")
            self._start_stdin_listener("no-evdev")
        except Exception as e:
            print(f"[Hotkey] Error: {e}")
            self._start_stdin_listener("error")

    def _start_stdin_listener(self, reason: str):
        """Fallback: toggle via stdin when hotkey isn't available."""
        if self.stdin_thread or not sys.stdin or not sys.stdin.isatty():
            return
        print("[Hotkey] Fallback: Press Enter to toggle recording")
        self.stdin_thread = threading.Thread(target=self._stdin_loop, daemon=True)
        self.stdin_thread.start()

    def _stdin_loop(self):
        while self.running:
            try:
                line = sys.stdin.readline()
            except Exception:
                break
            if not line:
                break
            cmd = line.strip().lower()
            if cmd in ("", "t", "toggle"):
                if self.mode == "hold":
                    if self.on_press:
                        self.on_press()
                    if self.on_release:
                        self.on_release()
                else:
                    if self.on_toggle:
                        self.on_toggle()

    def _handle_key_event(self, edge: str) -> None:
        if self.mode == "hold":
            if edge == "down" and self.on_press:
                self.on_press()
            elif edge == "up" and self.on_release:
                self.on_release()
        else:
            if edge == "down" and self.on_toggle:
                self.on_toggle()

    def _resolve_key_code(self, ecodes):
        """Resolve key name to evdev key code with aliases."""
        key = "".join(c for c in self.key.lower() if c.isalnum())
        aliases = {
            "rightctrl": "KEY_RIGHTCTRL",
            "rctrl": "KEY_RIGHTCTRL",
            "leftctrl": "KEY_LEFTCTRL",
            "lctrl": "KEY_LEFTCTRL",
            "ctrl": "KEY_RIGHTCTRL",
            "rightalt": "KEY_RIGHTALT",
            "ralt": "KEY_RIGHTALT",
            "leftalt": "KEY_LEFTALT",
            "lalt": "KEY_LEFTALT",
            "rightshift": "KEY_RIGHTSHIFT",
            "rshift": "KEY_RIGHTSHIFT",
            "leftshift": "KEY_LEFTSHIFT",
            "lshift": "KEY_LEFTSHIFT",
        }
        code_name = aliases.get(key)
        if not code_name:
            if len(key) == 1 and key.isalpha():
                code_name = f"KEY_{key.upper()}"
            elif key.startswith("f") and key[1:].isdigit():
                code_name = f"KEY_F{key[1:]}"
            elif key.isdigit():
                code_name = f"KEY_{key}"
            else:
                code_name = f"KEY_{key.upper()}"
        return getattr(ecodes, code_name, ecodes.KEY_RIGHTCTRL)

    def _find_keyboard(self):
        """Find keyboard input device."""
        try:
            import evdev
            from evdev import ecodes

            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                caps = device.capabilities()
                if ecodes.EV_KEY in caps:
                    keys = caps[ecodes.EV_KEY]
                    if ecodes.KEY_A in keys and ecodes.KEY_SPACE in keys:
                        return device
        except Exception as e:
            print(f"[Hotkey] Error finding keyboard: {e}")

        return None


# Test function
if __name__ == "__main__":
    print("Testing audio recorder...")
    recorder = AudioRecorder(sample_rate=16000)

    print("Recording for 2 seconds...")
    recorder.start_recording()
    time.sleep(2)
    audio = recorder.stop_recording()

    if audio is not None:
        print(f"✅ Recorded {len(audio)} samples")
    recorder.cleanup()
