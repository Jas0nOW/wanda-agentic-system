#!/usr/bin/env python3
"""
WANDA Ollama Manager - Smart On-Demand Ollama Control

Startet Ollama nur wenn Wanda es braucht, stoppt es danach.
Optimiert für RAM/VRAM auf Wayland/Cosmic.
"""

import subprocess
import time
import atexit
import signal
from typing import Optional

try:
    import requests

    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


class OllamaManager:
    """
    Manages Ollama lifecycle - starts on-demand, stops on exit.
    Prevents Ollama from hogging RAM when not needed.
    """

    def __init__(
        self, model: str = None, auto_unload: bool = True, unload_timeout: int = 60
    ):
        """
        Args:
            model: Model to use (e.g., "qwen3:8b")
            auto_unload: Automatically unload model after timeout
            unload_timeout: Seconds before unloading idle model
        """
        self.model = model
        self.auto_unload = auto_unload
        self.unload_timeout = unload_timeout
        self.api_url = "http://localhost:11434"

        self._ollama_started_by_us = False
        self._model_loaded = False
        self.available = False
        self._reported_running = False

        # Register cleanup on exit
        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, lambda s, f: self.cleanup())
        signal.signal(signal.SIGINT, lambda s, f: self.cleanup())

    def ensure_running(self) -> bool:
        """Ensure Ollama is running, start if needed."""
        if self._is_ollama_running():
            self.available = True
            if not self._reported_running:
                if self._ollama_started_by_us:
                    print("[Ollama] Server running (started by WANDA)")
                else:
                    print("[Ollama] Server already running")
                self._reported_running = True
            return True

        print("[Ollama] Starting Ollama server...")
        try:
            # Start Ollama in background
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            self._ollama_started_by_us = True
            self._reported_running = True

            # Wait for it to be ready
            for _ in range(30):  # 30 seconds timeout
                time.sleep(1)
                if self._is_ollama_running():
                    print("[Ollama] Server ready")
                    self.available = True
                    return True

            print("[Ollama] Timeout waiting for server")
            return False

        except FileNotFoundError:
            print("[Ollama] Not installed")
            return False
        except Exception as e:
            print(f"[Ollama] Error starting: {e}")
            return False

    def _is_ollama_running(self) -> bool:
        """Check if Ollama API is responding."""
        if not REQUESTS_AVAILABLE:
            return False
        try:
            response = requests.get(f"{self.api_url}/api/tags", timeout=2)
            return response.status_code == 200
        except:
            return False

    def load_model(self, model: str = None) -> bool:
        """Load model into memory (preload for faster first response)."""
        model = model or self.model
        if not model:
            return False

        if not self.ensure_running():
            return False

        print(f"[Ollama] Loading {model}...")
        try:
            # Send a minimal request to load the model
            response = requests.post(
                f"{self.api_url}/api/generate",
                json={
                    "model": model,
                    "prompt": "",
                    "keep_alive": f"{self.unload_timeout}s",
                },
                timeout=120,
            )
            if response.status_code == 200:
                print(f"[Ollama] {model} loaded")
                self._model_loaded = True
                return True
        except Exception as e:
            print(f"[Ollama] Error loading: {e}")
        return False

    def unload_model(self, model: str = None) -> bool:
        """Unload model from memory to free RAM/VRAM."""
        model = model or self.model
        if not model or not self._is_ollama_running():
            return False

        print(f"[Ollama] Unloading {model}...")
        try:
            # Set keep_alive to 0 to unload immediately
            response = requests.post(
                f"{self.api_url}/api/generate",
                json={"model": model, "prompt": "", "keep_alive": "0"},
                timeout=30,
            )
            if response.status_code == 200:
                print(f"[Ollama] {model} unloaded")
                self._model_loaded = False
                return True
        except Exception as e:
            print(f"[Ollama] Error unloading: {e}")
        return False

    def generate(
        self, prompt: str, system: str = None, model: str = None
    ) -> Optional[str]:
        """Generate response from Ollama."""
        model = model or self.model
        if not model:
            return None

        if not self.ensure_running():
            return None

        try:
            payload = {
                "model": model,
                "prompt": prompt,
                "stream": False,
                "keep_alive": f"{self.unload_timeout}s" if self.auto_unload else "-1",
            }
            if system:
                payload["system"] = system

            response = requests.post(
                f"{self.api_url}/api/generate", json=payload, timeout=60
            )

            if response.status_code == 200:
                return response.json().get("response", "").strip()

        except Exception as e:
            print(f"[Ollama] Error: {e}")
        return None

    def stop_server(self):
        """Stop Ollama server if we started it."""
        if not self._ollama_started_by_us:
            print("[Ollama] Not started by us, keeping running")
            return

        print("[Ollama] Stopping server...")
        try:
            # First unload model
            if self._model_loaded and self.model:
                self.unload_model()

            # Stop via systemctl or pkill
            subprocess.run(
                ["systemctl", "--user", "stop", "ollama"],
                capture_output=True,
                timeout=5,
            )
            subprocess.run(
                ["pkill", "-f", "ollama serve"], capture_output=True, timeout=5
            )
            print("[Ollama] Server stopped")
        except Exception as e:
            print(f"[Ollama] Error stopping: {e}")

    def cleanup(self):
        """Cleanup on exit."""
        if self._model_loaded and self.model:
            self.unload_model()
        if self._ollama_started_by_us:
            self.stop_server()

    def get_loaded_models(self) -> list:
        """Get list of currently loaded models."""
        if not self._is_ollama_running():
            return []
        try:
            response = requests.get(f"{self.api_url}/api/ps", timeout=5)
            if response.status_code == 200:
                data = response.json()
                return [m.get("name") for m in data.get("models", [])]
        except:
            pass
        return []

    def optimize_prompt(self, raw_prompt: str, target_tool: str = "gemini") -> str:
        """Optimize prompt for target tool (compatible with OllamaAdapter)."""
        if not self.model:
            return raw_prompt

        system = """Du bist Wanda's Prompt-Optimierer. Verbessere den Prompt:
- Entferne Füllwörter (ähm, also, halt)
- Füge Kontext hinzu
- Strukturiere klar
- Behalte die Absicht

Antworte NUR mit dem optimierten Prompt, keine Erklärung."""

        optimization_prompt = f"Optimiere für {target_tool}:\n\n{raw_prompt}"

        result = self.generate(optimization_prompt, system=system)
        return result if result else raw_prompt

    def get_gpu_layers(self, model: str = None) -> dict:
        """Check if model is using GPU or CPU."""
        model = model or self.model
        if not model or not self._is_ollama_running():
            return {}

        try:
            response = requests.get(f"{self.api_url}/api/ps", timeout=5)
            if response.status_code == 200:
                for m in response.json().get("models", []):
                    if m.get("name") == model:
                        return {
                            "model": model,
                            "size": m.get("size"),
                            "processor": m.get("processor"),  # "GPU" or "CPU"
                            "vram": m.get("size_vram", 0),
                        }
        except:
            pass
        return {}


# Convenience function
def create_ollama_manager(config: dict) -> Optional[OllamaManager]:
    """Create OllamaManager from config if enabled."""
    ollama_config = config.get("ollama", {})

    if not ollama_config.get("enabled", False):
        return None

    model = ollama_config.get("model", "")
    if not model:
        return None

    return OllamaManager(
        model=model,
        auto_unload=True,
        unload_timeout=120,  # 2 minutes idle before unload
    )


if __name__ == "__main__":
    print("Testing Ollama Manager...")

    manager = OllamaManager(model="qwen3:4b", auto_unload=True, unload_timeout=30)

    if manager.ensure_running():
        print("✅ Ollama running")

        # Test generate
        response = manager.generate("Sag Hallo in einem Satz.")
        print(f"Response: {response}")

        # Check GPU usage
        info = manager.get_gpu_layers()
        print(f"GPU Info: {info}")

        # Cleanup
        manager.cleanup()
    else:
        print("❌ Ollama not available")
