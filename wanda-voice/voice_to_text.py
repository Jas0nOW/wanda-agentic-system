import os
import queue
import sounddevice as sd
import vosk
import sys
import json
import subprocess
import time
import threading
import evdev
from evdev import InputDevice, categorize, ecodes

# Performance-Optimierung für schwächere Hardware
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
        print(f"[DEBUG] Tippe: '{text}'")  # Debug
        try:
            # Wayland: wtype, X11: xdotool
            result = subprocess.run(
                ["wtype", text + " "], capture_output=True, text=True
            )
            print(f"[DEBUG] wtype returncode: {result.returncode}")
            if result.stderr:
                print(f"[DEBUG] wtype stderr: {result.stderr}")
            if result.returncode != 0:
                print(f"[DEBUG] wtype failed, trying xdotool...")
                result2 = subprocess.run(
                    ["xdotool", "type", "--delay", "0", text + " "],
                    capture_output=True,
                    text=True,
                )
                print(f"[DEBUG] xdotool returncode: {result2.returncode}")
        except Exception as e:
            print(f"[DEBUG] Typing error: {e}")


def find_keyboard_device():
    """Finde das erste Tastatur-Input-Device"""
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
    for device in devices:
        caps = device.capabilities()
        if ecodes.EV_KEY in caps:
            keys = caps[ecodes.EV_KEY]
            if ecodes.KEY_A in keys and ecodes.KEY_SPACE in keys:
                print(f"Tastatur gefunden: {device.name}")
                return device
    return None


def keyboard_listener():
    """Keyboard-Listener Thread - funktioniert unter Wayland!"""
    global is_listening
    device = find_keyboard_device()
    if not device:
        print("Keine Tastatur gefunden! Versuche: sudo usermod -a -G input $USER")
        return
    try:
        # KEIN device.grab() - sonst wird die Tastatur blockiert!
        print("Tastatur-Listener aktiv (rechte Strg-Taste)")
        ctrl_pressed = False
        for event in device.read_loop():
            if event.type == ecodes.EV_KEY:
                key = categorize(event)
                if key.scancode == ecodes.KEY_RIGHTCTRL:
                    if key.keystate == key.key_down and not ctrl_pressed:
                        ctrl_pressed = True
                        is_listening = not is_listening
                        status = "AN" if is_listening else "AUS"
                        color = "\033[92m" if is_listening else "\033[91m"
                        print(f"\n[Mic: {color}{status}\033[0m]")
                        send_notification("Voice", f"Mikrofon {status}")
                    elif key.keystate == key.key_up:
                        ctrl_pressed = False
    except Exception as e:
        print(f"\nTastatur-Error: {e}")
    finally:
        pass  # Kein ungrab nötig, da kein grab


def callback(indata, frames, time_info, status):
    global is_listening
    if is_listening:
        q.put(bytes(indata))
        # Zeige Audio-Level als einfacher Balken
        import numpy as np

        volume = np.abs(np.frombuffer(indata, dtype=np.int16)).mean()
        bars = int(volume / 500)  # Skalierung
        if bars > 0:
            print(
                f"\r🎤 {'█' * min(bars, 20)}{'░' * (20 - min(bars, 20))} {int(volume)}    ",
                end="",
                flush=True,
            )


try:
    print("--- LADE PROFI-MODELL (CPU-schonend) ---")
    model = vosk.Model(MODEL_PATH)
    rec = vosk.KaldiRecognizer(model, 44100)

    kb_thread = threading.Thread(target=keyboard_listener, daemon=True)
    kb_thread.start()

    print("\nBEREIT! (Rechte Strg-Taste)")
    print(
        "Tipp: Falls keine Reaktion -> 'sudo usermod -a -G input $USER' dann Neuanmeldung"
    )

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
                        print(f"[DEBUG] Erkannt: '{text}'")  # Debug-Output
                        if text:
                            type_text(text)
                except queue.Empty:
                    continue
            else:
                while not q.empty():
                    q.get()
                time.sleep(0.1)

except KeyboardInterrupt:
    print("\nBeendet.")
except Exception as e:
    print(f"\nFehler: {e}")
    input("Enter...")
