#!/usr/bin/env python3
"""
Wanda JARVIS - Setup & Configuration Wizard
Vollständiger Installer für alle Systeme.
"""

import os
import subprocess
import sys
import json
from pathlib import Path

# ============================================================================
# HARDWARE DETECTION
# ============================================================================

def get_system_info() -> dict:
    """Detect CPU, RAM, GPU, VRAM."""
    info = {
        "cpu": "Unknown",
        "cpu_cores": 0,
        "ram_gb": 0,
        "gpu": None,
        "vram_gb": 0,
        "tier": "cpu"
    }

    # CPU
    try:
        with open("/proc/cpuinfo") as f:
            for line in f:
                if line.startswith("model name"):
                    info["cpu"] = line.split(":")[1].strip()
                    break
        info["cpu_cores"] = os.cpu_count() or 1
    except:
        pass

    # RAM
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemTotal"):
                    kb = int(line.split()[1])
                    info["ram_gb"] = round(kb / (1024 * 1024), 1)
                    break
    except:
        pass

    # GPU (NVIDIA)
    try:
        result = subprocess.run(
            ["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader,nounits"],
            capture_output=True, text=True, timeout=5
        )
        if result.returncode == 0:
            parts = result.stdout.strip().split(",")
            info["gpu"] = parts[0].strip()
            info["vram_gb"] = round(int(parts[1].strip()) / 1024, 1)
    except:
        pass

    # Determine tier
    vram = info["vram_gb"]
    ram = info["ram_gb"]

    if vram >= 20:
        info["tier"] = "high"
    elif vram >= 10:
        info["tier"] = "medium"
    elif vram >= 5:
        info["tier"] = "low"
    elif vram >= 3:
        info["tier"] = "minimal"
    elif ram >= 32:
        info["tier"] = "cpu-high"
    elif ram >= 16:
        info["tier"] = "cpu"
    else:
        info["tier"] = "cpu-low"

    return info


# ============================================================================
# MODEL RECOMMENDATIONS
# ============================================================================

OLLAMA_MODELS = {
    "high": {
        "models": ["qwen3:32b", "llama3.3:70b-instruct-q4_K_M", "deepseek-r1:32b"],
        "description": "32B+ Parameter (20GB+ VRAM)"
    },
    "medium": {
        "models": ["qwen3:14b", "llama3.3:latest", "mistral-nemo:12b"],
        "description": "12-14B Parameter (10-20GB VRAM)"
    },
    "low": {
        "models": ["qwen3:8b", "llama3.2:latest", "gemma3:9b"],
        "description": "7-9B Parameter (5-10GB VRAM)"
    },
    "minimal": {
        "models": ["qwen3:4b", "phi4:latest", "gemma3:4b"],
        "description": "3-4B Parameter (3-5GB VRAM)"
    },
    "cpu-high": {
        "models": ["qwen3:8b-q4_K_M", "llama3.2:8b-q4_K_M"],
        "description": "8B quantisiert (CPU + 32GB RAM)"
    },
    "cpu": {
        "models": ["qwen3:4b-q4_K_M", "phi4:q4_K_M"],
        "description": "4B quantisiert (CPU + 16GB RAM)"
    },
    "cpu-low": {
        "models": ["qwen3:1.7b", "phi3:mini"],
        "description": "1-2B Parameter (CPU + 8GB RAM)"
    }
}


# ============================================================================
# TTS VOICES
# ============================================================================

EDGE_VOICES = {
    "seraphina": ("de-DE-SeraphinaMultilingualNeural", "Seraphina", "Premium, sehr natürlich"),
    "amala": ("de-DE-AmalaNeural", "Amala", "Warm, sympathisch"),
    "florian": ("de-DE-FlorianMultilingualNeural", "Florian", "Premium männlich"),
    "katja": ("de-DE-KatjaNeural", "Katja", "Professionell"),
    "conrad": ("de-DE-ConradNeural", "Conrad", "Tief, JARVIS-like"),
    "killian": ("de-DE-KillianNeural", "Killian", "Modern, dynamisch"),
    "ingrid": ("de-AT-IngridNeural", "Ingrid (AT)", "Österreichisch"),
    "jonas": ("de-AT-JonasNeural", "Jonas (AT)", "Österreichisch"),
    "leni": ("de-CH-LeniNeural", "Leni (CH)", "Schweizerdeutsch"),
    "jan": ("de-CH-JanNeural", "Jan (CH)", "Schweizerdeutsch"),
}

FAVORITE_VOICES = ["seraphina", "amala", "florian"]


# ============================================================================
# INPUT HELPER
# ============================================================================

def get_input(prompt: str, valid_options: list, default: str = None, allow_back: bool = True) -> str:
    """
    Get validated user input.
    Returns: choice or "back" or None (for default)
    """
    valid_set = set(str(v).lower() for v in valid_options)
    if allow_back:
        valid_set.add("b")
        valid_set.add("back")

    while True:
        choice = input(prompt).strip().lower()

        # Default
        if not choice and default:
            return default

        # Back
        if choice in ("b", "back") and allow_back:
            return "back"

        # Valid choice
        if choice in valid_set:
            return choice

        # Demo check (1d, 2d, etc.)
        if choice.endswith("d") and choice[:-1] in valid_set:
            return choice

        # Invalid
        print(f"   ❌ Ungültige Eingabe: '{choice}'")
        print(f"   Gültig: {', '.join(sorted(valid_options))}" + (" oder [b]ack" if allow_back else ""))


# ============================================================================
# SETUP CLASS
# ============================================================================

class WandaSetup:
    """Interactive setup wizard."""

    def __init__(self):
        self.project_dir = Path(__file__).parent.absolute()
        self.config_path = self.project_dir / "wanda.config.yaml"
        self.config = self._load_config()
        self.hw_info = get_system_info()
        self.steps = []  # For back navigation

    def _load_config(self) -> dict:
        """Load existing config."""
        if self.config_path.exists():
            try:
                content = self.config_path.read_text()
                # Try JSON first (might have been saved as JSON)
                if content.strip().startswith("{"):
                    return json.loads(content)
                # Try YAML
                try:
                    import yaml
                    return yaml.safe_load(content)
                except:
                    return json.loads(content)
            except:
                pass
        return self._default_config()

    def _default_config(self) -> dict:
        return {
            "mode": "jarvis",
            "audio": {"sample_rate": 16000, "vad_engine": "silero"},
            "trigger": {"key": "rightctrl"},
            "stt": {"model": "large-v3-turbo", "device": "auto"},
            "tts": {
                "engine": "edge",
                "voice": "seraphina",
                "voice_key": "seraphina",
                "voice_id": "de-DE-SeraphinaMultilingualNeural",
                "voice_name": "Seraphina",
                "mode": "short"
            },
            "output": {"speak": True, "sounds_enabled": True},
            "adapters": {"gemini_model": "flash"},
            "ollama": {"enabled": False, "model": ""},
        }

    def run(self):
        """Main wizard."""
        os.chdir(self.project_dir)
        self._print_header()
        self._show_hardware()

        # Menu
        print("\n   [1] Vollständiges Setup (empfohlen)")
        print("   [2] Nur Konfiguration ändern")
        print("   [0] Beenden")

        choice = get_input("\nWähle (1): ", ["0", "1", "2"], "1", allow_back=False)

        if choice == "0":
            return

        if choice == "1":
            self._full_setup()

        self._configure_all()
        self._save_config()
        self._print_success()

    def _print_header(self):
        print("\n" + "=" * 60)
        print("🎙️  WANDA JARVIS - Setup & Konfiguration")
        print("=" * 60)

    def _show_hardware(self):
        """Display detected hardware."""
        hw = self.hw_info
        print(f"\n🖥️  Hardware erkannt:")
        print(f"   CPU: {hw['cpu'][:50]} ({hw['cpu_cores']} Kerne)")
        print(f"   RAM: {hw['ram_gb']} GB")
        if hw["gpu"]:
            print(f"   GPU: {hw['gpu']} ({hw['vram_gb']} GB VRAM)")
        else:
            print("   GPU: Keine NVIDIA GPU erkannt")
        print(f"   Tier: {hw['tier'].upper()} - {OLLAMA_MODELS.get(hw['tier'], {}).get('description', '')}")

    def _full_setup(self):
        """Complete installation."""
        print("\n" + "-" * 40)
        print("📦 INSTALLATION")
        print("-" * 40)

        # Python check
        if sys.version_info < (3, 10):
            print("❌ Python 3.10+ erforderlich")
            sys.exit(1)
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")

        # Create venv
        venv_path = self.project_dir / "venv"
        if not venv_path.exists():
            print("\n📦 Erstelle virtuelle Umgebung...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual Environment")

        # Install dependencies
        print("\n📥 Installiere Abhängigkeiten...")
        pip = str(self.project_dir / "venv" / "bin" / "pip")

        # Core packages
        packages = [
            "pyyaml",
            "numpy",
            "scipy",
            "sounddevice",
            "edge-tts",
            "faster-whisper",
            "piper-tts",
            "evdev",
            "requests",
            "pexpect",
        ]

        for pkg in packages:
            result = subprocess.run(
                [pip, "install", "-q", pkg],
                capture_output=True
            )
            status = "✅" if result.returncode == 0 else "⚠️"
            print(f"   {status} {pkg}")

        # PyTorch with CUDA if GPU available
        if self.hw_info["gpu"]:
            print("\n   📥 PyTorch mit CUDA...")
            subprocess.run([pip, "install", "-q", "torch", "--index-url",
                          "https://download.pytorch.org/whl/cu121"], capture_output=True)
        else:
            subprocess.run([pip, "install", "-q", "torch", "--index-url",
                          "https://download.pytorch.org/whl/cpu"], capture_output=True)
        print("   ✅ PyTorch")

        # Check groups
        self._check_permissions()

        # Create launcher
        self._create_launcher()

    def _check_permissions(self):
        """Check audio/input group membership."""
        print("\n🔐 Berechtigungen...")
        result = subprocess.run(["groups"], capture_output=True, text=True)
        groups = result.stdout.lower()

        if "audio" not in groups:
            print("   ⚠️  Nicht in 'audio' Gruppe: sudo usermod -aG audio $USER")
        else:
            print("   ✅ Audio-Gruppe")

        if "input" not in groups:
            print("   ⚠️  Nicht in 'input' Gruppe: sudo usermod -aG input $USER")
        else:
            print("   ✅ Input-Gruppe")

    def _create_launcher(self):
        """Create global launcher scripts."""
        print("\n🚀 Erstelle Launcher...")

        bin_dir = Path.home() / ".local" / "bin"
        bin_dir.mkdir(parents=True, exist_ok=True)

        # wanda-voice launcher
        launcher = f'''#!/bin/bash
# WANDA Voice Assistant
cd "{self.project_dir}"
source venv/bin/activate
exec python3 main.py "$@"
'''
        launcher_path = self.project_dir / "wanda-voice-run"
        launcher_path.write_text(launcher)
        os.chmod(launcher_path, 0o755)

        # Global symlink
        global_link = bin_dir / "wanda-voice"
        try:
            if global_link.exists() or global_link.is_symlink():
                global_link.unlink()
            global_link.symlink_to(launcher_path)
            print(f"   ✅ wanda-voice (global)")
        except Exception as e:
            print(f"   ⚠️  Symlink: {e}")

        # Check PATH
        if str(bin_dir) not in os.environ.get("PATH", ""):
            print(f"\n   💡 Füge zu ~/.bashrc hinzu:")
            print(f'      export PATH="$HOME/.local/bin:$PATH"')

    def _configure_all(self):
        """Configuration wizard with back navigation."""
        steps = [
            ("tts", self._configure_tts),
            ("ollama", self._configure_ollama),
            ("trigger", self._configure_trigger),
        ]

        idx = 0
        while idx < len(steps):
            name, func = steps[idx]
            result = func()
            if result == "back" and idx > 0:
                idx -= 1
            else:
                idx += 1

    def _configure_tts(self) -> str:
        """Configure TTS voice."""
        print("\n" + "=" * 50)
        print("🎙️  WANDA STIMME")
        print("=" * 50)

        current = self.config.get("tts", {}).get("voice", "seraphina")

        while True:
            print("\nTop 3 Stimmen:\n")
            for i, key in enumerate(FAVORITE_VOICES, 1):
                vid, name, style = EDGE_VOICES[key]
                star = " ⭐" if i == 1 else ""
                curr = " ← aktuell" if key == current else ""
                print(f"   [{i}] {name}{star}{curr} - {style}")

            print("\n   [0] Alle 10 Stimmen")
            print("   💡 Demo: 1d, 2d, 3d")

            choice = get_input("\nWähle (1): ", ["0", "1", "2", "3"], "1", allow_back=False)

            # Demo
            if choice.endswith("d"):
                idx = int(choice[0]) - 1
                if 0 <= idx < len(FAVORITE_VOICES):
                    key = FAVORITE_VOICES[idx]
                    vid, name, style = EDGE_VOICES[key]
                    print(f"\n🎤 Demo: {name}...")
                    self._play_demo(vid)
                continue

            # All voices
            if choice == "0":
                result = self._select_all_voices(current)
                if result and result != "back":
                    return "next"
                continue

            # Select
            idx = int(choice) - 1
            key = FAVORITE_VOICES[idx]
            vid, name, style = EDGE_VOICES[key]
            self.config["tts"] = {
                "engine": "edge",
                "voice": key,
                "voice_key": key,
                "voice_id": vid,
                "voice_name": name,
                "mode": "short"
            }
            print(f"\n✅ Stimme: {name}")
            return "next"

    def _select_all_voices(self, current: str) -> str:
        """Show all voices."""
        keys = list(EDGE_VOICES.keys())

        while True:
            print("\n" + "-" * 40)
            print("Alle Stimmen:\n")

            for i, key in enumerate(keys, 1):
                vid, name, style = EDGE_VOICES[key]
                curr = " ← aktuell" if key == current else ""
                print(f"   [{i:2}] {name}{curr} - {style}")

            print("\n   💡 Demo: 1d, 2d, ... 10d")

            valid = [str(i) for i in range(1, len(keys)+1)]
            choice = get_input("\nWähle oder [b]ack: ", valid, None, allow_back=True)

            if choice == "back":
                return "back"

            # Demo
            if choice.endswith("d"):
                idx = int(choice[:-1]) - 1
                if 0 <= idx < len(keys):
                    key = keys[idx]
                    vid, name, style = EDGE_VOICES[key]
                    print(f"\n🎤 Demo: {name}...")
                    self._play_demo(vid)
                continue

            # Select
            idx = int(choice) - 1
            key = keys[idx]
            vid, name, style = EDGE_VOICES[key]
            self.config["tts"] = {
                "engine": "edge",
                "voice": key,
                "voice_key": key,
                "voice_id": vid,
                "voice_name": name,
                "mode": "short"
            }
            print(f"\n✅ Stimme: {name}")
            return "next"

    def _play_demo(self, voice_id: str):
        """Play TTS demo."""
        try:
            import asyncio
            import tempfile

            # Activate venv for edge_tts
            venv_python = self.project_dir / "venv" / "bin" / "python3"

            demo_script = f'''
import asyncio
import edge_tts
import subprocess
import tempfile
import os

async def main():
    tmp = tempfile.mktemp(suffix=".mp3")
    text = "Hallo! Ich bin Wanda, deine persönliche KI-Assistentin."
    communicate = edge_tts.Communicate(text, "{voice_id}")
    await communicate.save(tmp)
    subprocess.run(["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", tmp])
    os.unlink(tmp)

asyncio.run(main())
'''
            subprocess.run([str(venv_python), "-c", demo_script], check=False)
        except Exception as e:
            print(f"   Demo-Fehler: {e}")

    def _configure_ollama(self) -> str:
        """Configure Ollama."""
        print("\n" + "=" * 50)
        print("🧠 OLLAMA (Lokales LLM)")
        print("=" * 50)

        # Check Ollama
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print("\n⚠️  Ollama nicht aktiv. Starte mit: ollama serve")
                self.config["ollama"] = {"enabled": False, "model": ""}
                return "next"
        except FileNotFoundError:
            print("\nℹ️  Ollama nicht installiert (optional)")
            print("   Install: curl -fsSL https://ollama.com/install.sh | sh")
            self.config["ollama"] = {"enabled": False, "model": ""}
            return "next"
        except:
            self.config["ollama"] = {"enabled": False, "model": ""}
            return "next"

        # Parse models
        lines = result.stdout.strip().split("\n")[1:]
        installed = [line.split()[0] for line in lines if line.strip()]

        if not installed:
            print("\n⚠️  Keine Modelle installiert.")
            rec = OLLAMA_MODELS.get(self.hw_info["tier"], {}).get("models", ["qwen3:4b"])[0]
            print(f"   Empfohlen: ollama pull {rec}")
            self.config["ollama"] = {"enabled": False, "model": ""}
            return "next"

        current = self.config.get("ollama", {}).get("model", "")
        tier = self.hw_info["tier"]

        while True:
            print(f"\n✅ Ollama aktiv ({len(installed)} Modelle)")
            print(f"   Dein Tier: {tier.upper()}\n")

            print("   [1] Auto (bestes für Hardware)")
            print("   [2] Aus installierten wählen")
            print("   [3] Custom Model eingeben")
            print("   [0] Ollama deaktivieren")

            choice = get_input("\nWähle (1): ", ["0", "1", "2", "3"], "1", allow_back=True)

            if choice == "back":
                return "back"

            if choice == "0":
                self.config["ollama"] = {"enabled": False, "model": ""}
                print("✅ Ollama deaktiviert")
                return "next"

            if choice == "1":
                # Auto select
                recommended = OLLAMA_MODELS.get(tier, {}).get("models", [])
                selected = None
                for rec in recommended:
                    for inst in installed:
                        if rec.split(":")[0] in inst:
                            selected = inst
                            break
                    if selected:
                        break
                if not selected:
                    selected = installed[0]

                self.config["ollama"] = {"enabled": True, "model": selected}
                print(f"✅ Auto: {selected}")
                return "next"

            if choice == "2":
                # Select from installed
                print("\nInstallierte Modelle:\n")
                for i, m in enumerate(installed, 1):
                    curr = " ← aktuell" if m == current else ""
                    print(f"   [{i}] {m}{curr}")

                valid = [str(i) for i in range(1, len(installed)+1)]
                sel = get_input("\nWähle: ", valid, "1", allow_back=True)

                if sel == "back":
                    continue

                idx = int(sel) - 1
                self.config["ollama"] = {"enabled": True, "model": installed[idx]}
                print(f"✅ Ollama: {installed[idx]}")
                return "next"

            if choice == "3":
                # Custom
                print("\nCustom Model (z.B. mistral:7b):")
                custom = input("   Model: ").strip()
                if custom:
                    self.config["ollama"] = {"enabled": True, "model": custom}
                    print(f"✅ Custom: {custom}")
                    return "next"

    def _configure_trigger(self) -> str:
        """Configure trigger key."""
        print("\n" + "=" * 50)
        print("⌨️  TRIGGER-TASTE")
        print("=" * 50)

        keys = ["rightctrl", "pause", "leftctrl", "rightalt", "leftalt"]
        current = self.config.get("trigger", {}).get("key", "rightctrl")

        print("\nVerfügbare Tasten:\n")
        for i, key in enumerate(keys, 1):
            curr = " ← aktuell" if key == current else ""
            print(f"   [{i}] {key}{curr}")

        valid = [str(i) for i in range(1, len(keys)+1)]
        choice = get_input("\nWähle (1): ", valid, "1", allow_back=True)

        if choice == "back":
            return "back"

        idx = int(choice) - 1
        self.config["trigger"] = {"key": keys[idx]}
        print(f"✅ Trigger: {keys[idx]}")
        return "next"

    def _save_config(self):
        """Save configuration."""
        print("\n" + "-" * 40)
        print("💾 Speichere Konfiguration...")

        try:
            import yaml
            with open(self.config_path, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False, allow_unicode=True)
        except ImportError:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)

        print(f"✅ {self.config_path}")

    def _print_success(self):
        """Print success message."""
        print("\n" + "=" * 60)
        print("✅ SETUP ABGESCHLOSSEN!")
        print("=" * 60)

        print(f"\n🎙️  Stimme: {self.config['tts'].get('voice_name', 'Seraphina')}")
        if self.config.get("ollama", {}).get("enabled"):
            print(f"🧠 Ollama: {self.config['ollama']['model']}")
        print(f"⌨️  Trigger: {self.config['trigger']['key']}")

        print("\n🚀 Starte WANDA:")
        print("   wanda-voice")
        print(f"\n   oder: cd {self.project_dir} && source venv/bin/activate && python3 main.py")

        print("\n⚙️  Konfiguration ändern:")
        print(f"   python3 {self.project_dir}/setup.py")
        print("=" * 60 + "\n")


def main():
    setup = WandaSetup()
    setup.run()


if __name__ == "__main__":
    main()
