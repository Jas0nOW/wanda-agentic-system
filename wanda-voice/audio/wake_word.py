# Wanda Voice Assistant - Wake Word Detection
"""Wake word detection using openwakeword (Alexa/Hey Siri style)."""

import threading
import time
import numpy as np
from typing import Optional, Callable, List


class WakeWordDetector:
    """
    Wake word detection for hands-free activation.

    Uses openwakeword for efficient on-device detection.
    Supports custom wake words like "Hey Wanda".
    """

    # Built-in model names (openwakeword)
    BUILTIN_MODELS = [
        "alexa",
        "hey_mycroft",
        "hey_jarvis",
    ]

    def __init__(
        self,
        wake_words: List[str] = None,
        on_wake: Optional[Callable[[], None]] = None,
        threshold: float = 0.5,
        sample_rate: int = 16000,
    ):
        """
        Initialize wake word detector.

        Args:
            wake_words: List of wake word model names to load
            on_wake: Callback when wake word detected
            threshold: Detection threshold (0-1)
            sample_rate: Audio sample rate
        """
        self.wake_words = wake_words or ["hey_jarvis"]
        self.on_wake = on_wake
        self.threshold = threshold
        self.sample_rate = sample_rate

        self.model = None
        self.running = False
        self.stream = None
        self.thread = None

        self._init_model()

    def _init_model(self):
        """Initialize openwakeword model."""
        try:
            from openwakeword.model import Model

            # Load specified wake word models
            self.model = Model(
                wakeword_models=self.wake_words, inference_framework="onnx"
            )
            print(f"[WakeWord] Loaded models: {self.wake_words}")

        except ImportError:
            print("[WakeWord] openwakeword not installed")
            print("[WakeWord] Install: pip install openwakeword")
            self.model = None
        except Exception as e:
            print(f"[WakeWord] Error loading model: {e}")
            self.model = None

    @property
    def available(self) -> bool:
        """Check if wake word detection is available."""
        return self.model is not None

    def start(self):
        """Start wake word detection in background."""
        if not self.available:
            print("[WakeWord] Not available, skipping")
            return

        if self.running:
            return

        self.running = True
        self.thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.thread.start()
        print("[WakeWord] Detection started")

    def stop(self):
        """Stop wake word detection."""
        self.running = False
        if self.stream:
            try:
                self.stream.stop()
                self.stream.close()
            except:
                pass
            self.stream = None

        if self.thread:
            self.thread.join(timeout=1)
        print("[WakeWord] Detection stopped")

    def _detection_loop(self):
        """Main detection loop."""
        try:
            import sounddevice as sd

            # Audio buffer
            chunk_size = 1280  # ~80ms at 16kHz

            def audio_callback(indata, frames, time_info, status):
                if not self.running:
                    return

                # Get audio chunk
                audio = indata[:, 0]  # Mono

                # Run prediction
                prediction = self.model.predict(audio)

                # Check for wake word
                for wake_word in self.wake_words:
                    score = prediction.get(wake_word, 0)
                    if score > self.threshold:
                        print(f"[WakeWord] Detected '{wake_word}' (score: {score:.2f})")
                        if self.on_wake:
                            # Run callback in separate thread
                            threading.Thread(target=self.on_wake, daemon=True).start()

                        # Brief cooldown to prevent repeat triggers
                        time.sleep(1.5)

            # Start audio stream
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=chunk_size,
                callback=audio_callback,
            )
            self.stream.start()

            # Keep thread alive
            while self.running:
                time.sleep(0.1)

        except Exception as e:
            print(f"[WakeWord] Error: {e}")
            self.running = False


class SimpleWakeWordDetector:
    """
    Simple wake word detector using speech recognition.
    Fallback when openwakeword is not available.
    """

    WAKE_PHRASES = [
        "hey wanda",
        "hallo wanda",
        "wanda",
        "hey jarvis",
        "jarvis",
        "okay wanda",
        "ok wanda",
        "wanda start",
        "wandastart",
        "wunderstart",
        "wanderstart",
        "wunder",
        "wonda",
        "wonder",
    ]

    def __init__(self, on_wake: Optional[Callable[[], None]] = None, stt_engine=None):
        """
        Initialize simple detector.

        Args:
            on_wake: Callback when wake word detected
            stt_engine: STT engine for transcription
        """
        self.on_wake = on_wake
        self.stt = stt_engine
        self.running = False
        self.thread = None

    @property
    def available(self) -> bool:
        return self.stt is not None

    def start(self):
        """Start detection."""
        if not self.available:
            return

        self.running = True
        self.thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.thread.start()
        print("[WakeWord] Simple detection started (uses STT)")

    def stop(self):
        """Stop detection."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)

    def _detection_loop(self):
        """Detection loop using VAD + STT."""
        try:
            import sounddevice as sd

            chunk_duration = 2.0  # Check every 2 seconds
            chunk_samples = int(16000 * chunk_duration)

            while self.running:
                # Record short chunk
                audio = sd.rec(
                    chunk_samples, samplerate=16000, channels=1, dtype="float32"
                )
                sd.wait()

                if not self.running:
                    break

                # Check if speech present (simple energy check)
                energy = np.sqrt(np.mean(audio**2))
                if energy < 0.01:  # Too quiet
                    continue

                # Transcribe
                text = self.stt.transcribe(audio.flatten(), language="de")
                text_lower = text.lower().strip()

                # Check for wake phrases
                for phrase in self.WAKE_PHRASES:
                    if phrase in text_lower:
                        print(f"[WakeWord] Detected: '{phrase}'")
                        if self.on_wake:
                            self.on_wake()
                        time.sleep(2)  # Cooldown
                        break

        except Exception as e:
            print(f"[WakeWord] Error: {e}")


def get_wake_word_detector(
    on_wake: Callable = None,
    stt_engine=None,
    wake_words: Optional[list] = None,
    threshold: float = 0.5,
):
    """Get best available wake word detector."""
    # Try openwakeword first
    detector = WakeWordDetector(
        on_wake=on_wake, wake_words=wake_words, threshold=threshold
    )
    if detector.available:
        return detector

    # Fallback to simple detector
    if stt_engine:
        return SimpleWakeWordDetector(on_wake=on_wake, stt_engine=stt_engine)

    print("[WakeWord] No wake word detection available")
    return None


if __name__ == "__main__":

    def on_wake():
        print("🌟 Wake word detected! Wanda is listening...")

    detector = get_wake_word_detector(on_wake=on_wake)
    if detector and detector.available:
        detector.start()
        print("Say 'Hey Jarvis' or 'Hey Wanda'...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            detector.stop()
    else:
        print("Wake word detection not available")
