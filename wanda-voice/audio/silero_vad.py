# Wanda Voice Assistant - Silero VAD
"""Production-grade Voice Activity Detection using Silero."""

import time
import threading
import queue
from typing import Optional

try:
    import torch
    import numpy as np

    SILERO_AVAILABLE = True
except ImportError:
    SILERO_AVAILABLE = False
    print("[VAD] Warning: torch not installed, using energy-based fallback")


class SileroVAD:
    """
    Production-grade VAD using Silero.
    - 95%+ accuracy
    - < 1ms latency per chunk
    - Trained on 6000+ languages
    """

    def __init__(
        self,
        threshold: float = 0.5,
        sampling_rate: int = 16000,
        silence_duration: float = 2.0,
    ):
        self.threshold = threshold
        self.sampling_rate = sampling_rate
        self.silence_duration = silence_duration

        # State
        self.is_speaking = False
        self.silence_start: Optional[float] = None
        self.audio_queue: queue.Queue = queue.Queue()
        self.running = True

        # Load model
        if SILERO_AVAILABLE:
            self._load_model()
        else:
            self.model = None
            print("[VAD] Using energy-based fallback")

        # Start monitor thread
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        print(f"[VAD] Initialized (threshold={threshold}, silence={silence_duration}s)")

    def _load_model(self):
        """Load Silero VAD model."""
        try:
            self.model, _ = torch.hub.load(
                repo_or_dir="snakers4/silero-vad",
                model="silero_vad",
                force_reload=False,
                onnx=True,
            )
            print("[VAD] Silero model loaded (ONNX)")
        except Exception as e:
            print(f"[VAD] Failed to load Silero: {e}")
            self.model = None

    def push_audio(self, chunk: "np.ndarray"):
        """Push audio chunk for VAD analysis."""
        self.audio_queue.put(chunk)

    def _monitor_loop(self):
        """Continuous monitoring loop."""
        while self.running:
            try:
                chunk = self.audio_queue.get(timeout=0.1)
                self._process_chunk(chunk)
            except queue.Empty:
                continue

    def _process_chunk(self, chunk: "np.ndarray"):
        """Process audio chunk."""
        if self.model and SILERO_AVAILABLE:
            # Silero VAD
            audio_tensor = torch.from_numpy(chunk).float()
            speech_prob = self.model(audio_tensor, self.sampling_rate).item()
            voice_detected = speech_prob > self.threshold
        else:
            # Energy-based fallback
            energy = np.abs(chunk).mean()
            voice_detected = energy > 0.01

        # Update state
        if voice_detected:
            self.is_speaking = True
            self.silence_start = None
        else:
            if self.is_speaking and self.silence_start is None:
                self.silence_start = time.time()
            self.is_speaking = False

    def is_user_speaking(self) -> bool:
        """Check if user is currently speaking."""
        return self.is_speaking

    def silence_exceeded(self) -> bool:
        """Check if silence duration exceeded (for auto-stop)."""
        if self.silence_start is None:
            return False
        return time.time() - self.silence_start > self.silence_duration

    def reset(self):
        """Reset VAD state."""
        self.is_speaking = False
        self.silence_start = None
        # Clear queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except:
                break

    def stop(self):
        """Stop VAD monitoring."""
        self.running = False


# Energy-based fallback for systems without torch
class EnergyVAD:
    """Simple energy-based VAD fallback."""

    def __init__(self, threshold: float = 0.01, silence_duration: float = 2.0):
        self.threshold = threshold
        self.silence_duration = silence_duration
        self.is_speaking = False
        self.silence_start: Optional[float] = None
        print(f"[VAD] Energy-based (threshold={threshold})")

    def push_audio(self, chunk: "np.ndarray"):
        """Process audio chunk."""
        import numpy as np

        energy = np.abs(chunk).mean()

        if energy > self.threshold:
            self.is_speaking = True
            self.silence_start = None
        else:
            if self.is_speaking and self.silence_start is None:
                self.silence_start = time.time()
            self.is_speaking = False

    def is_user_speaking(self) -> bool:
        return self.is_speaking

    def silence_exceeded(self) -> bool:
        if self.silence_start is None:
            return False
        return time.time() - self.silence_start > self.silence_duration

    def reset(self):
        self.is_speaking = False
        self.silence_start = None

    def stop(self):
        pass


def get_vad(engine: str = "silero", **kwargs):
    """Factory function to get appropriate VAD engine."""
    if engine == "silero" and SILERO_AVAILABLE:
        return SileroVAD(**kwargs)
    else:
        return EnergyVAD(**kwargs)


if __name__ == "__main__":
    print("Testing Silero VAD...")
    vad = get_vad("silero")
    print(f"✅ VAD initialized: {type(vad).__name__}")
