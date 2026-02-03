# Wanda Voice Assistant - faster-whisper STT Engine
"""Speech-to-Text using faster-whisper."""

import os
import tempfile
from pathlib import Path
from typing import Optional
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel


class FasterWhisperEngine:
    """STT engine using faster-whisper (CTranslate2-optimized)."""
    
    def __init__(self, model_name: str = "large-v3-turbo", device: str = "auto"):
        """
        Initialize faster-whisper engine.
        
        Args:
            model_name: Model to use (tiny, base, small, medium, large-v3, large-v3-turbo)
            device: Device for inference ('auto', 'cuda', 'cpu')
        """
        self.model_name = model_name
        self.device = self._detect_device(device)
        self.model = None
        
        print(f"[STT] Initializing faster-whisper ({model_name}, {self.device})")
        self._load_model()
    
    def _detect_device(self, device: str) -> str:
        """Auto-detect GPU availability."""
        if device == "auto":
            try:
                import torch
                if torch.cuda.is_available():
                    print(f"[STT] GPU detected: {torch.cuda.get_device_name(0)}")
                    return "cuda"
            except ImportError:
                pass
            print("[STT] No GPU detected, using CPU")
            return "cpu"
        return device
    
    def _load_model(self):
        """Load the Whisper model."""
        try:
            # compute_type: float16 for GPU, int8 for CPU (faster)
            compute_type = "float16" if self.device == "cuda" else "int8"
            
            self.model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=compute_type,
                download_root=None  # Uses HuggingFace cache
            )
            print(f"[STT] Model loaded: {self.model_name} ({compute_type})")
        except Exception as e:
            print(f"[STT] Error loading model: {e}")
            raise
    
    def transcribe(self, audio_data: np.ndarray, sample_rate: int = 16000, language: str = "de") -> str:
        """
        Transcribe audio data to text.
        
        Args:
            audio_data: numpy array of audio samples (float32, -1.0 to 1.0)
            sample_rate: sample rate of audio
            language: language code (de, en, etc.)
        
        Returns:
            Transcribed text
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        # Save audio to temp WAV file (faster-whisper expects file path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Write WAV file
            import scipy.io.wavfile as wav
            # Convert float32 to int16
            audio_int16 = (audio_data * 32767).astype(np.int16)
            wav.write(tmp_path, sample_rate, audio_int16)
            
            # Transcribe
            segments, info = self.model.transcribe(
                tmp_path,
                language=language,
                beam_size=5,
                vad_filter=True,  # Voice Activity Detection
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            # Collect segments
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        
        except Exception as e:
            print(f"[STT] Transcription error: {e}")
            return ""
        finally:
            # Cleanup temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
    
    def transcribe_file(self, audio_file: str, language: str = "de") -> str:
        """
        Transcribe audio from file.
        
        Args:
            audio_file: Path to audio file
            language: language code
        
        Returns:
            Transcribed text
        """
        if self.model is None:
            raise RuntimeError("Model not loaded")
        
        try:
            segments, info = self.model.transcribe(
                audio_file,
                language=language,
                beam_size=5,
                vad_filter=True
            )
            
            text = " ".join([segment.text for segment in segments])
            return text.strip()
        except Exception as e:
            print(f"[STT] Transcription error: {e}")
            return ""


# Test function
if __name__ == "__main__":
    print("Testing faster-whisper engine...")
    engine = FasterWhisperEngine(model_name="base", device="auto")
    print("✅ Engine initialized successfully")
