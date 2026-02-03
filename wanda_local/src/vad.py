"""
Silero VAD Module - Voice Activity Detection
=============================================
Detects when the user is speaking and captures audio until silence.
Target latency: < 200ms.
"""

import torch
import numpy as np
from collections import deque


class SileroVAD:
    """Wrapper for Silero VAD model."""

    def __init__(self, latency_target_ms: int = 200, sample_rate: int = 16000):
        self.latency_target_ms = latency_target_ms
        self.sample_rate = sample_rate
        self.model, self.utils = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            force_reload=False,
            onnx=True,
        )
        self.get_speech_timestamps = self.utils[0]
        self.audio_buffer = deque(maxlen=100)  # ~6 seconds of audio
        self.is_speaking = False
        self.silence_threshold_ms = 500  # Stop after 500ms of silence

    async def listen(self) -> bytes | None:
        """
        Listen for voice input using the microphone.
        Returns audio bytes when speech is detected and ends.
        """
        import sounddevice as sd

        print("[VAD] Listening...")
        audio_chunks = []
        silence_duration = 0

        def callback(indata, frames, time, status):
            nonlocal silence_duration
            audio_np = np.frombuffer(indata, dtype=np.float32)
            
            # Check for speech
            speech_prob = self.model(torch.from_numpy(audio_np), self.sample_rate).item()
            
            if speech_prob > 0.5:
                self.is_speaking = True
                silence_duration = 0
                audio_chunks.append(audio_np.copy())
            elif self.is_speaking:
                silence_duration += frames / self.sample_rate * 1000
                audio_chunks.append(audio_np.copy())
                if silence_duration > self.silence_threshold_ms:
                    raise sd.CallbackStop()

        try:
            with sd.InputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype="float32",
                blocksize=int(self.sample_rate * 0.032),  # 32ms chunks
                callback=callback,
            ):
                sd.sleep(30000)  # Max 30 seconds
        except sd.CallbackStop:
            pass

        if audio_chunks:
            full_audio = np.concatenate(audio_chunks)
            self.is_speaking = False
            print(f"[VAD] Captured {len(full_audio) / self.sample_rate:.2f}s of audio")
            return full_audio.tobytes()

        return None
