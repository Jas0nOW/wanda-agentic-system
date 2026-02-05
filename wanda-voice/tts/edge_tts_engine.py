# WANDA Voice - Edge TTS Engine (Microsoft Neural Voices)
"""
Hochwertige TTS mit Microsoft Neural Voices.
Siri-Level Qualität, kostenlos, 15+ deutsche Stimmen.
"""

import asyncio
import tempfile
import subprocess
import os
from typing import Optional
from pathlib import Path

try:
    import edge_tts
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("[TTS] edge-tts nicht installiert: pip install edge-tts")


# Deutsche Neural Voices - nur tatsächlich verfügbare
GERMAN_VOICES = {
    # Deutschland - Weiblich
    "seraphina": {
        "id": "de-DE-SeraphinaMultilingualNeural",
        "name": "Seraphina",
        "gender": "weiblich",
        "style": "Premium, multilingual, sehr natürlich",
        "recommended": True
    },
    "katja": {
        "id": "de-DE-KatjaNeural",
        "name": "Katja",
        "gender": "weiblich",
        "style": "Professionell, Nachrichtensprecherin"
    },
    "amala": {
        "id": "de-DE-AmalaNeural",
        "name": "Amala",
        "gender": "weiblich",
        "style": "Warm, sympathisch"
    },
    # Deutschland - Männlich
    "florian": {
        "id": "de-DE-FlorianMultilingualNeural",
        "name": "Florian",
        "gender": "männlich",
        "style": "Premium, multilingual, sehr natürlich",
        "recommended_male": True
    },
    "conrad": {
        "id": "de-DE-ConradNeural",
        "name": "Conrad",
        "gender": "männlich",
        "style": "Tief, JARVIS-like"
    },
    "killian": {
        "id": "de-DE-KillianNeural",
        "name": "Killian",
        "gender": "männlich",
        "style": "Modern, dynamisch"
    },
    # Österreich
    "ingrid": {
        "id": "de-AT-IngridNeural",
        "name": "Ingrid",
        "gender": "weiblich",
        "style": "Österreichisch, freundlich"
    },
    "jonas": {
        "id": "de-AT-JonasNeural",
        "name": "Jonas",
        "gender": "männlich",
        "style": "Österreichisch, klar"
    },
    # Schweiz
    "leni": {
        "id": "de-CH-LeniNeural",
        "name": "Leni",
        "gender": "weiblich",
        "style": "Schweizerdeutsch, sanft"
    },
    "jan": {
        "id": "de-CH-JanNeural",
        "name": "Jan",
        "gender": "männlich",
        "style": "Schweizerdeutsch, ruhig"
    },
}


class EdgeTTSEngine:
    """
    Microsoft Edge TTS - Neural Voice Engine.
    Siri-Level Qualität, kostenlos.
    """

    def __init__(self, voice: str = "katja", rate: str = "+0%", pitch: str = "+0Hz"):
        """
        Initialize Edge TTS.

        Args:
            voice: Voice key from GERMAN_VOICES (e.g., "katja", "louisa", "conrad")
            rate: Speed adjustment (e.g., "+10%", "-5%")
            pitch: Pitch adjustment (e.g., "+5Hz", "-10Hz")
        """
        self.voice_key = voice.lower()
        self.voice_id = GERMAN_VOICES.get(self.voice_key, {}).get("id", "de-DE-KatjaNeural")
        self.rate = rate
        self.pitch = pitch
        self.available = EDGE_TTS_AVAILABLE

        if self.available:
            voice_info = GERMAN_VOICES.get(self.voice_key, {})
            print(f"[TTS] Edge Neural: {voice_info.get('name', voice)} ({voice_info.get('style', '')})")
        else:
            print("[TTS] Edge TTS nicht verfügbar - installiere: pip install edge-tts")

    async def _generate_async(self, text: str, output_path: str) -> bool:
        """Generate speech asynchronously."""
        try:
            communicate = edge_tts.Communicate(
                text,
                self.voice_id,
                rate=self.rate,
                pitch=self.pitch
            )
            await communicate.save(output_path)
            return True
        except Exception as e:
            print(f"[TTS] Fehler: {e}")
            return False

    def generate(self, text: str, output_path: str = None) -> Optional[str]:
        """
        Generate speech from text.

        Args:
            text: Text to speak
            output_path: Optional output path (creates temp file if None)

        Returns:
            Path to audio file or None on error
        """
        if not self.available:
            return None

        if not output_path:
            output_path = tempfile.mktemp(suffix=".mp3")

        # Run async in sync context
        try:
            asyncio.run(self._generate_async(text, output_path))
            return output_path
        except RuntimeError:
            # Already in async context
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._generate_async(text, output_path))
            return output_path

    def speak(self, text: str, mode: str = "short"):
        """
        Speak text immediately.

        Args:
            text: Text to speak
            mode: "short" (first sentences) or "full" (everything)
        """
        if not self.available:
            print(f"[TTS] (unavailable) {text[:100]}...")
            return

        # Truncate for short mode
        if mode == "short" and len(text) > 300:
            # Find sentence end
            for end in [". ", "! ", "? ", "\n"]:
                idx = text.find(end, 100)
                if idx > 0 and idx < 400:
                    text = text[:idx+1]
                    break
            else:
                text = text[:300] + "..."

        # Generate audio
        audio_path = self.generate(text)
        if not audio_path:
            return

        # Play with ffplay (most compatible)
        try:
            subprocess.run(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", audio_path],
                check=False,
                timeout=60
            )
        except FileNotFoundError:
            # Fallback to mpv
            try:
                subprocess.run(
                    ["mpv", "--no-video", "--really-quiet", audio_path],
                    check=False,
                    timeout=60
                )
            except FileNotFoundError:
                print("[TTS] Kein Audio-Player gefunden (ffplay/mpv)")
        except subprocess.TimeoutExpired:
            pass
        finally:
            # Cleanup
            try:
                os.unlink(audio_path)
            except:
                pass

    def speak_async(self, text: str, mode: str = "short"):
        """Speak in background thread."""
        import threading
        thread = threading.Thread(target=self.speak, args=(text, mode), daemon=True)
        thread.start()
        return thread

    def stop(self):
        """Stop playback (kill mpv/ffplay)."""
        try:
            subprocess.run(["pkill", "-f", "mpv.*wanda"], check=False)
            subprocess.run(["pkill", "-f", "ffplay.*wanda"], check=False)
        except:
            pass

    def set_voice(self, voice_key: str):
        """Change voice."""
        if voice_key.lower() in GERMAN_VOICES:
            self.voice_key = voice_key.lower()
            self.voice_id = GERMAN_VOICES[self.voice_key]["id"]
            print(f"[TTS] Stimme: {GERMAN_VOICES[self.voice_key]['name']}")

    def list_voices(self) -> dict:
        """Get all available voices."""
        return GERMAN_VOICES


def get_voice_list():
    """Get formatted voice list for display."""
    female = []
    male = []
    for key, v in GERMAN_VOICES.items():
        entry = f"{v['name']}: {v['style']}"
        if v.get("recommended"):
            entry += " ⭐"
        if v["gender"] == "weiblich":
            female.append((key, entry))
        else:
            male.append((key, entry))
    return {"female": female, "male": male}


# Test
if __name__ == "__main__":
    print("Testing Edge TTS...")

    if not EDGE_TTS_AVAILABLE:
        print("Install: pip install edge-tts")
        exit(1)

    engine = EdgeTTSEngine(voice="katja")

    print("\nVerfügbare Stimmen:")
    voices = get_voice_list()
    print("\n👩 Weiblich:")
    for key, desc in voices["female"]:
        print(f"   {key}: {desc}")
    print("\n👨 Männlich:")
    for key, desc in voices["male"]:
        print(f"   {key}: {desc}")

    print("\n🎙️ Test mit Katja...")
    engine.speak("Hallo! Ich bin Wanda, deine persönliche KI-Assistentin. Wie kann ich dir heute helfen?")
    print("✅ Done")
