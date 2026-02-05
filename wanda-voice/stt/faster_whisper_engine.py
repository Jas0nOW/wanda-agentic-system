# Wanda Voice Assistant - faster-whisper STT Engine
"""Speech-to-Text using faster-whisper."""

import os
import locale
import tempfile
from pathlib import Path
from typing import Optional
import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel


def _ensure_utf8_locale():
    if not os.environ.get("LC_ALL"):
        os.environ["LC_ALL"] = "C.UTF-8"
    if not os.environ.get("LANG"):
        os.environ["LANG"] = "C.UTF-8"
    try:
        locale.setlocale(locale.LC_ALL, "C.UTF-8")
    except Exception:
        pass


_ensure_utf8_locale()


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
            self.compute_type = compute_type

            self.model = WhisperModel(
                self.model_name,
                device=self.device,
                compute_type=compute_type,
                download_root=None,  # Uses HuggingFace cache
            )
            print(f"[STT] Model loaded: {self.model_name} ({compute_type})")
        except Exception as e:
            print(f"[STT] Error loading model: {e}")
            raise

    def transcribe(
        self, audio_data: np.ndarray, sample_rate: int = 16000, language: str = "de"
    ) -> str:
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

        # Debug: Audio stats
        audio_min, audio_max = audio_data.min(), audio_data.max()
        audio_mean = np.abs(audio_data).mean()
        duration = len(audio_data) / sample_rate
        print(
            f"[STT] Model={self.model_name}, device={self.device}, compute={getattr(self, 'compute_type', '?')}"
        )
        print(
            f"[STT] Audio stats: min={audio_min:.4f}, max={audio_max:.4f}, mean_abs={audio_mean:.4f}"
        )
        print(f"[STT] Audio duration: {duration:.2f}s @ {sample_rate}Hz")

        # Normalize audio if needed (should be -1.0 to 1.0)
        if audio_max > 1.0 or audio_min < -1.0:
            print(f"[STT] Warning: Audio out of range, normalizing...")
            max_val = max(abs(audio_min), abs(audio_max))
            audio_data = audio_data / max_val

        # Boost quiet audio (if mean is very low)
        if audio_mean < 0.01:
            print(f"[STT] Warning: Audio very quiet, boosting...")
            audio_data = audio_data * (0.3 / max(audio_mean, 0.0001))
            audio_data = np.clip(audio_data, -1.0, 1.0)

        # Save audio to temp WAV file (faster-whisper expects file path)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
            tmp_path = tmp.name

        try:
            # Write WAV file
            import scipy.io.wavfile as wav

            # Convert float32 to int16
            audio_int16 = (audio_data * 32767).astype(np.int16)
            wav.write(tmp_path, sample_rate, audio_int16)

            # Transcribe with anti-hallucination settings
            segments, info = self.model.transcribe(
                tmp_path,
                language=language,
                beam_size=5,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500),
                # Anti-hallucination settings
                condition_on_previous_text=False,
                no_speech_threshold=0.6,
                log_prob_threshold=-1.0,
                compression_ratio_threshold=2.4,
                suppress_blank=True,
            )
            print(
                "[STT] Decode settings: beam=5, no_speech=0.6, logprob=-1.0, comp_ratio=2.4"
            )

            # Collect segments with confidence filtering
            valid_segments = []
            for segment in segments:
                # Skip segments with very low confidence (avg_logprob)
                if hasattr(segment, "avg_logprob") and segment.avg_logprob < -1.5:
                    print(
                        f"[STT] Skipping low-confidence segment: {segment.text[:30]}..."
                    )
                    continue
                # Skip nonsense-looking segments (too many repeated chars)
                if len(segment.text) > 5:
                    unique_ratio = len(set(segment.text.lower())) / len(segment.text)
                    if unique_ratio < 0.15:  # Too repetitive = likely hallucination
                        print(
                            f"[STT] Skipping repetitive segment: {segment.text[:30]}..."
                        )
                        continue
                valid_segments.append(segment.text)

            text = " ".join(valid_segments)
            print(
                f"[STT] Transcribed: {text[:100]}..."
                if len(text) > 100
                else f"[STT] Transcribed: {text}"
            )
            return text.strip()

        except UnicodeDecodeError as e:
            print(f"[STT] Transcription error (encoding): {e}")
            _ensure_utf8_locale()
            try:
                segments, info = self.model.transcribe(
                    tmp_path,
                    language=language,
                    beam_size=5,
                    vad_filter=True,
                    vad_parameters=dict(min_silence_duration_ms=500),
                    condition_on_previous_text=False,
                    no_speech_threshold=0.6,
                    log_prob_threshold=-1.0,
                    compression_ratio_threshold=2.4,
                    suppress_blank=True,
                )
                valid_segments = []
                for segment in segments:
                    if hasattr(segment, "avg_logprob") and segment.avg_logprob < -1.5:
                        continue
                    if len(segment.text) > 5:
                        unique_ratio = len(set(segment.text.lower())) / len(
                            segment.text
                        )
                        if unique_ratio < 0.15:
                            continue
                    valid_segments.append(segment.text)
                text = " ".join(valid_segments)
                return text.strip()
            except Exception as retry_error:
                print(f"[STT] Retry failed: {retry_error}")
                return ""

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
                audio_file, language=language, beam_size=5, vad_filter=True
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
