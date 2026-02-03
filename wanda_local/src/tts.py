"""
TTS Engine Module - Text to Speech
==================================
Supports multiple TTS backends: XTTS-v2 (Premium), StyleTTS2 (Medium), Piper (Fallback).
"""

import subprocess
from pathlib import Path
from enum import Enum


class TTSProfile(Enum):
    PREMIUM = "xtts-v2"
    MEDIUM = "styletts2"
    LOW = "vits"
    MACOS_SIRI = "siri"  # Native macOS TTS
    FALLBACK = "piper"


class TTSEngine:
    """Unified TTS engine with multiple backend support."""

    def __init__(self, profile: str = "premium"):
        self.profile = TTSProfile[profile.upper()] if isinstance(profile, str) else profile
        self.voice_reference = Path(__file__).parent.parent / "models/wanda_voice.wav"
        self.is_macos = self._detect_macos()
        
        # Auto-select Siri on macOS if no explicit profile
        if self.is_macos and profile == "premium":
            print("[TTS] macOS detected - using native Siri TTS for best integration")
            self.profile = TTSProfile.MACOS_SIRI

    def _detect_macos(self) -> bool:
        """Check if running on macOS."""
        import platform
        return platform.system() == "Darwin"

    async def speak(self, text: str) -> None:
        """
        Convert text to speech and play it.
        
        Args:
            text: The text to speak
        """
        print(f"[TTS] Speaking: {text}")

        if self.profile == TTSProfile.MACOS_SIRI:
            await self._speak_siri(text)
        elif self.profile == TTSProfile.PREMIUM:
            await self._speak_xtts(text)
        elif self.profile == TTSProfile.MEDIUM:
            await self._speak_styletts(text)
        elif self.profile == TTSProfile.LOW:
            await self._speak_vits(text)
        else:
            await self._speak_piper(text)

    async def _speak_siri(self, text: str) -> None:
        """Use macOS native 'say' command with Siri voices."""
        try:
            # Use German Siri voice (Anna) or fallback to default
            # Available German voices: Anna, Petra, Yannick
            subprocess.run(
                ["say", "-v", "Anna", "-r", "180", text],
                check=True
            )
        except FileNotFoundError:
            print("[TTS] macOS 'say' command not found, falling back to Piper.")
            await self._speak_piper(text)
        except subprocess.CalledProcessError:
            # Try default voice if Anna not available
            subprocess.run(["say", text], check=True)


    async def _speak_xtts(self, text: str) -> None:
        """Use Coqui XTTS-v2 for speech synthesis."""
        try:
            from TTS.api import TTS

            tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")
            tts.tts_to_file(
                text=text,
                speaker_wav=str(self.voice_reference),
                language="de",
                file_path="/tmp/wanda_speech.wav",
            )
            subprocess.run(["aplay", "/tmp/wanda_speech.wav"], check=True)
        except ImportError:
            print("[TTS] XTTS-v2 not available, falling back to Piper.")
            await self._speak_piper(text)

    async def _speak_styletts(self, text: str) -> None:
        """Use StyleTTS2 for speech synthesis."""
        # Placeholder for StyleTTS2 integration
        print("[TTS] StyleTTS2 not yet implemented, using Piper fallback.")
        await self._speak_piper(text)

    async def _speak_vits(self, text: str) -> None:
        """Use VITS for speech synthesis."""
        # Placeholder for VITS integration
        print("[TTS] VITS not yet implemented, using Piper fallback.")
        await self._speak_piper(text)

    async def _speak_piper(self, text: str) -> None:
        """Use Piper TTS as fallback."""
        try:
            # Piper command line
            process = subprocess.Popen(
                [
                    "piper",
                    "--model", "de_DE-kerstin-low",
                    "--output_file", "/tmp/wanda_speech.wav",
                ],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            process.communicate(input=text.encode("utf-8"))
            subprocess.run(["aplay", "/tmp/wanda_speech.wav"], check=True)
        except FileNotFoundError:
            print("[TTS] Piper not found. Please install piper-tts.")
