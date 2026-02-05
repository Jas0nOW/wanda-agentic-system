#!/usr/bin/env python3
"""
WANDA Stimmen-Demo - Alle verfügbaren Microsoft Neural Voices.
"""

import asyncio
import subprocess
import tempfile
import os
import sys

try:
    import edge_tts
except ImportError:
    print("edge-tts nicht installiert. Starte: source venv/bin/activate")
    sys.exit(1)

# Nur die tatsächlich verfügbaren Stimmen
VOICES = [
    # Deutschland - Weiblich
    (
        "de-DE-SeraphinaMultilingualNeural",
        "Seraphina",
        "Premium, multilingual, sehr natürlich",
        "weiblich",
    ),
    ("de-DE-KatjaNeural", "Katja", "Professionell, Nachrichtensprecherin", "weiblich"),
    ("de-DE-AmalaNeural", "Amala", "Warm, sympathisch", "weiblich"),
    # Deutschland - Männlich
    (
        "de-DE-FlorianMultilingualNeural",
        "Florian",
        "Premium, multilingual, sehr natürlich",
        "männlich",
    ),
    ("de-DE-ConradNeural", "Conrad", "Tief, assistant-like", "männlich"),
    ("de-DE-KillianNeural", "Killian", "Modern, dynamisch", "männlich"),
    # Österreich
    ("de-AT-IngridNeural", "Ingrid (AT)", "Österreichisch, freundlich", "weiblich"),
    ("de-AT-JonasNeural", "Jonas (AT)", "Österreichisch, klar", "männlich"),
    # Schweiz
    ("de-CH-LeniNeural", "Leni (CH)", "Schweizerdeutsch, sanft", "weiblich"),
    ("de-CH-JanNeural", "Jan (CH)", "Schweizerdeutsch, ruhig", "männlich"),
]

DEMO_TEXT = "Hallo! Ich bin Wanda, deine persönliche KI-Assistentin. Wie kann ich dir heute helfen?"


async def play_voice(voice_id: str):
    """Generate and play voice sample."""
    tmp = tempfile.mktemp(suffix=".mp3")
    try:
        communicate = edge_tts.Communicate(DEMO_TEXT, voice_id)
        await communicate.save(tmp)
        subprocess.run(
            ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", tmp], check=False
        )
    except Exception as e:
        print(f"   Fehler: {e}")
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def main():
    print("\n" + "=" * 60)
    print("🎙️  WANDA STIMMEN-DEMO")
    print("=" * 60)

    female = [v for v in VOICES if v[3] == "weiblich"]
    male = [v for v in VOICES if v[3] == "männlich"]

    print("\n👩 Weibliche Stimmen:\n")
    for i, (vid, name, style, _) in enumerate(female, 1):
        star = " ⭐" if "Premium" in style else ""
        print(f"   [{i}] {name}{star} - {style}")

    print("\n👨 Männliche Stimmen:\n")
    for i, (vid, name, style, _) in enumerate(male, len(female) + 1):
        star = " ⭐" if "Premium" in style else ""
        print(f"   [{i}] {name}{star} - {style}")

    print("\n   [a] Alle anhören")
    print("   [0] Beenden")

    choice = input("\nNummer wählen: ").strip().lower()

    if choice == "0":
        return

    all_voices = female + male

    if choice == "a":
        voices_to_play = all_voices
    else:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(all_voices):
                voices_to_play = [all_voices[idx]]
            else:
                print("Ungültig.")
                return
        except:
            print("Ungültig.")
            return

    print("\n" + "-" * 40)
    for vid, name, style, _ in voices_to_play:
        print(f"\n🎤 {name} - {style}")
        asyncio.run(play_voice(vid))

        if len(voices_to_play) > 1:
            cont = input("   [Enter] nächste, [s] stopp: ").strip().lower()
            if cont == "s":
                break

    print("\n✅ Demo beendet.\n")


if __name__ == "__main__":
    main()
