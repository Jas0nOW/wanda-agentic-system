import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import subprocess
import time
import threading
import select

# Performance-Optimierung
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model")

is_listening = False
q = queue.Queue()


def send_notification(title, message):
    try:
        subprocess.run(["notify-send", "-t", "800", title, message])
    except:
        pass


def type_text(text):
    if not text:
        return
    text = text.strip()
    if text:
        try:
            # Wayland: wtype, X11: xdotool
            result = subprocess.run(["wtype", text + " "], capture_output=True)
            if result.returncode != 0:
                subprocess.run(
                    ["xdotool", "type", "--delay", "0", text + " "], check=True
                )
        except Exception as e:
            print(f"\n⚠️  Konnte nicht tippen: {e}")


def toggle_mic():
    global is_listening
    is_listening = not is_listening
    status = "AN" if is_listening else "AUS"
    color = "\033[92m" if is_listening else "\033[91m"
    print(
        f"\n[Mic: {color}{status}\033[0m] {'🎤 Spreche jetzt...' if is_listening else '⏸️  Pausiert'}"
    )
    send_notification("Voice", f"Mikrofon {status}")


def stdin_listener():
    """Einfacher Stdin-Listener - drücke Enter zum Umschalten"""
    global is_listening
    print("\n🎯 Drücke ENTER zum Aktivieren/Deaktivieren (oder Ctrl+C zum Beenden)")

    while True:
        try:
            # Non-blocking input check
            if select.select([sys.stdin], [], [], 0.1)[0]:
                line = sys.stdin.readline()
                if line:  # Enter wurde gedrückt
                    toggle_mic()
        except:
            break


def callback(indata, frames, time_info, status):
    if is_listening:
        q.put(bytes(indata))


try:
    print("--- LADE PROFI-MODELL (CPU-schonend) ---")
    model = vosk.Model(MODEL_PATH)
    rec = vosk.KaldiRecognizer(model, 44100)

    # Stdin-Listener in separatem Thread
    kb_thread = threading.Thread(target=stdin_listener, daemon=True)
    kb_thread.start()

    print("\n✅ BEREIT! (Terminal-Mode)")
    print("   Das Tool läuft im Vordergrund.")
    print("   → Drücke ENTER um Mikrofon AN/AUS zu schalten")
    print("   → Sprich und der Text wird automatisch getippt")
    print("   → Das aktive Fenster erhält den Text\n")

    with sd.RawInputStream(
        samplerate=44100,
        blocksize=8192,
        device=None,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        while True:
            if is_listening:
                try:
                    data = q.get(timeout=0.2)
                    if rec.AcceptWaveform(data):
                        res = json.loads(rec.Result())
                        text = res.get("text", "")
                        if text:
                            print(f"📝 Erkannt: '{text}'")
                            type_text(text)
                except queue.Empty:
                    continue
            else:
                while not q.empty():
                    q.get()
                time.sleep(0.1)

except KeyboardInterrupt:
    print("\n👋 Beendet.")
except Exception as e:
    print(f"\n❌ Fehler: {e}")
    import traceback

    traceback.print_exc()
    input("Enter...")
