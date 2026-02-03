# Wanda Voice Assistant - Audio Recorder
"""Audio recording with hotkey trigger."""

import queue
import threading
import time
import numpy as np
import sounddevice as sd
from typing import Optional, Callable


class AudioRecorder:
    """Audio recorder with toggle hotkey."""
    
    def __init__(self, sample_rate: int = 16000, max_seconds: int = 15):
        """
        Initialize audio recorder.
        
        Args:
            sample_rate: Sample rate for recording (16000 recommended for STT)
            max_seconds: Maximum recording duration
        """
        self.sample_rate = sample_rate
        self.max_seconds = max_seconds
        self.is_recording = False
        self.audio_queue = queue.Queue()
        self.stream = None
        
        print(f"[Audio] Recorder initialized ({sample_rate}Hz, max {max_seconds}s)")
    
    def _audio_callback(self, indata, frames, time_info, status):
        """Callback for audio stream."""
        if status:
            print(f"[Audio] Status: {status}")
        
        if self.is_recording:
            # Copy data to avoid overwrite
            self.audio_queue.put(indata.copy())
    
    def start_recording(self):
        """Start audio recording."""
        if self.is_recording:
            print("[Audio] Already recording")
            return
        
        print("[Audio] 🎤 Recording started...")
        self.is_recording = True
        
        # Clear queue
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
            except:
                break
        
        # Start stream if not already running
        if self.stream is None:
            try:
                self.stream = sd.InputStream(
                    samplerate=self.sample_rate,
                    channels=1,
                    dtype='float32',
                    callback=self._audio_callback,
                    blocksize=1024
                )
                self.stream.start()
            except sd.PortAudioError as e:
                print(f"[Audio] ❌ Failed to open audio device: {e}")
                print("[Audio] Tip: Check if microphone is connected and not in use")
                self.is_recording = False
            except Exception as e:
                print(f"[Audio] ❌ Audio error: {e}")
                self.is_recording = False
    
    def stop_recording(self) -> Optional[np.ndarray]:
        """
        Stop audio recording and return recorded audio.
        
        Returns:
            numpy array of audio data (float32), or None if no data
        """
        if not self.is_recording:
            print("[Audio] Not recording")
            return None
        
        print("[Audio] ⏸️  Recording stopped")
        self.is_recording = False
        
        # Collect audio data from queue
        audio_chunks = []
        while not self.audio_queue.empty():
            audio_chunks.append(self.audio_queue.get())
        
        if not audio_chunks:
            print("[Audio] No audio data recorded")
            return None
        
        # Concatenate chunks
        audio_data = np.concatenate(audio_chunks, axis=0)
        
        # Flatten to 1D if needed
        if audio_data.ndim > 1:
            audio_data = audio_data.flatten()
        
        duration = len(audio_data) / self.sample_rate
        print(f"[Audio] Recorded {duration:.1f}s ({len(audio_data)} samples)")
        
        return audio_data
    
    def cleanup(self):
        """Cleanup audio stream."""
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        print("[Audio] Cleanup done")


# Hotkey handler (evdev-based, for global hotkey)
class HotkeyHandler:
    """Handle hotkey triggers using evdev."""
    
    def __init__(self, key: str = "rightctrl", on_toggle: Callable = None):
        """
        Initialize hotkey handler.
        
        Args:
            key: Key to use as hotkey (e.g., 'rightctrl')
            on_toggle: Callback function called on toggle
        """
        self.key = key
        self.on_toggle = on_toggle
        self.running = False
        self.thread = None
        
        print(f"[Hotkey] Handler initialized ({key})")
    
    def start(self):
        """Start hotkey listener in background thread."""
        if self.running:
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._listener_loop, daemon=True)
        self.thread.start()
        print("[Hotkey] Listener started")
    
    def stop(self):
        """Stop hotkey listener."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        print("[Hotkey] Listener stopped")
    
    def _listener_loop(self):
        """Main listener loop (evdev-based)."""
        try:
            import evdev
            from evdev import ecodes
            
            # Find keyboard device
            device = self._find_keyboard()
            if not device:
                print("[Hotkey] No keyboard found. Falling back to terminal mode.")
                print("[Hotkey] Tip: Add user to 'input' group: sudo usermod -a -G input $USER")
                return
            
            print(f"[Hotkey] Listening on: {device.name}")
            
            ctrl_pressed = False
            key_code = getattr(ecodes, f"KEY_{self.key.upper()}", ecodes.KEY_RIGHTCTRL)
            
            for event in device.read_loop():
                if not self.running:
                    break
                
                if event.type == ecodes.EV_KEY:
                    key = evdev.categorize(event)
                    
                    if key.scancode == key_code:
                        if key.keystate == key.key_down and not ctrl_pressed:
                            ctrl_pressed = True
                            if self.on_toggle:
                                self.on_toggle()
                        elif key.keystate == key.key_up:
                            ctrl_pressed = False
        
        except ImportError:
            print("[Hotkey] evdev not available, hotkey disabled")
        except Exception as e:
            print(f"[Hotkey] Error: {e}")
    
    def _find_keyboard(self):
        """Find keyboard input device."""
        try:
            import evdev
            from evdev import ecodes
            
            devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
            for device in devices:
                caps = device.capabilities()
                if ecodes.EV_KEY in caps:
                    keys = caps[ecodes.EV_KEY]
                    if ecodes.KEY_A in keys and ecodes.KEY_SPACE in keys:
                        return device
        except Exception as e:
            print(f"[Hotkey] Error finding keyboard: {e}")
        
        return None


# Test function
if __name__ == "__main__":
    print("Testing audio recorder...")
    recorder = AudioRecorder(sample_rate=16000)
    
    print("Recording for 2 seconds...")
    recorder.start_recording()
    time.sleep(2)
    audio = recorder.stop_recording()
    
    if audio is not None:
        print(f"✅ Recorded {len(audio)} samples")
    recorder.cleanup()
