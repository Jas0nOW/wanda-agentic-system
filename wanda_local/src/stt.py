"""
Faster-Whisper STT Module - Speech to Text
==========================================
GPU-accelerated transcription using faster-whisper.
"""

from faster_whisper import WhisperModel


class FasterWhisperSTT:
    """Wrapper for Faster-Whisper model."""

    def __init__(self, model: str = "large-v3-turbo", device: str = "cuda"):
        """
        Initialize the Whisper model.
        
        Args:
            model: Model size (tiny, base, small, medium, large-v3-turbo)
            device: "cuda" for GPU, "cpu" for CPU
        """
        self.model = WhisperModel(model, device=device, compute_type="float16")
        self.language = "de"  # Default to German

    async def transcribe(self, audio_bytes: bytes) -> str:
        """
        Transcribe audio bytes to text.
        
        Args:
            audio_bytes: Raw audio data (16kHz, mono, float32)
            
        Returns:
            Transcribed text string
        """
        import numpy as np
        import tempfile
        import soundfile as sf

        # Convert bytes to numpy array
        audio_np = np.frombuffer(audio_bytes, dtype=np.float32)

        # Write to temporary WAV file (faster-whisper expects file path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            sf.write(f.name, audio_np, 16000)
            temp_path = f.name

        # Transcribe
        segments, info = self.model.transcribe(
            temp_path,
            language=self.language,
            beam_size=5,
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=500),
        )

        # Collect all segments
        transcript = " ".join([segment.text for segment in segments])

        print(f"[STT] Language: {info.language} (prob: {info.language_probability:.2f})")
        return transcript.strip()
