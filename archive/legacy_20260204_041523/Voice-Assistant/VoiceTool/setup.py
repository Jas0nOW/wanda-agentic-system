#!/usr/bin/env python3
"""
Wanda JARVIS - Setup & Configuration Wizard
Re-runnable: Use for first setup OR to change settings.
"""

import os
import subprocess
import sys
import json
from pathlib import Path

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False


class WandaSetup:
    """Interactive setup wizard."""
    
    def __init__(self):
        self.project_dir = Path(__file__).parent.absolute()
        self.config_path = self.project_dir / "wanda.config.yaml"
        self.config = self._load_config()
        self.mode = "setup"  # setup or configure
    
    def _load_config(self):
        """Load existing config or defaults."""
        if self.config_path.exists() and YAML_AVAILABLE:
            try:
                with open(self.config_path) as f:
                    return yaml.safe_load(f)
            except:
                pass
        return self._default_config()
    
    def _default_config(self):
        return {
            "mode": "jarvis",
            "audio": {"sample_rate": 16000, "vad_engine": "silero"},
            "trigger": {"key": "rightctrl"},
            "stt": {"model": "large-v3-turbo", "device": "auto"},
            "tts": {"voice": "de_DE-eva_k-x_low", "mode": "short"},
            "output": {"speak": True, "sounds_enabled": True},
            "adapters": {"gemini_model": "flash"},
            "ollama": {"enabled": False, "model": ""},
        }
    
    def run(self):
        """Main wizard flow."""
        os.chdir(self.project_dir)
        
        self._print_header()
        
        # Detect if first run or reconfigure
        if self.config_path.exists():
            print("📋 Existing configuration found.\n")
            print("   [1] Full Setup (reset everything)")
            print("   [2] Configure Settings")
            print("   [3] Exit")
            choice = input("\nChoose (2): ").strip() or "2"
            
            if choice == "3":
                print("Bye!")
                return
            elif choice == "1":
                self.mode = "setup"
            else:
                self.mode = "configure"
        else:
            self.mode = "setup"
        
        if self.mode == "setup":
            self._check_python()
            self._setup_venv()
            self._install_dependencies()
        
        self._configure_ollama()
        self._configure_tts()
        self._configure_trigger()
        self._check_cli_tools()
        
        if self.mode == "setup":
            self._check_audio()
            self._create_launcher()
            self._create_desktop_file()
        
        self._save_config()
        self._print_success()
    
    def _print_header(self):
        print("\n" + "=" * 60)
        print("🎙️  WANDA JARVIS - Setup & Configuration")
        print("=" * 60 + "\n")
    
    def _check_python(self):
        if sys.version_info < (3, 10):
            print("❌ Python 3.10+ required")
            sys.exit(1)
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
    
    def _setup_venv(self):
        venv_path = self.project_dir / "venv"
        if not venv_path.exists():
            print("\n📦 Creating virtual environment...")
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("✅ Virtual environment ready")
    
    def _install_dependencies(self):
        print("\n📥 Installing dependencies (this may take a while)...")
        pip = self.project_dir / "venv" / "bin" / "pip"
        subprocess.run([str(pip), "install", "-q", "--upgrade", "pip"])
        subprocess.run([str(pip), "install", "-q", "-r", "requirements.txt"])
        # Install yaml for config
        subprocess.run([str(pip), "install", "-q", "pyyaml"])
        print("✅ Dependencies installed")
    
    def _configure_ollama(self):
        print("\n" + "-" * 40)
        print("🧠 OLLAMA CONFIGURATION")
        print("-" * 40)
        
        # Check if Ollama is installed
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=5)
            if result.returncode != 0:
                print("⚠️  Ollama not running. Start with: ollama serve")
                self.config["ollama"]["enabled"] = False
                return
        except FileNotFoundError:
            print("ℹ️  Ollama not installed (optional)")
            print("   Install: curl -fsSL https://ollama.com/install.sh | sh")
            self.config["ollama"]["enabled"] = False
            return
        except:
            self.config["ollama"]["enabled"] = False
            return
        
        # Parse available models
        lines = result.stdout.strip().split("\n")[1:]
        models = []
        for line in lines:
            if line.strip():
                parts = line.split()
                if parts:
                    models.append(parts[0])
        
        if not models:
            print("⚠️  No Ollama models found.")
            print("   Install a model: ollama pull qwen2.5:32b")
            self.config["ollama"]["enabled"] = False
            return
        
        print(f"✅ Ollama available with {len(models)} model(s)\n")
        print("Verfügbare Modelle:")
        for i, model in enumerate(models):
            marker = " ← current" if model == self.config["ollama"].get("model") else ""
            print(f"   [{i+1}] {model}{marker}")
        print("   [0] Ollama nicht verwenden")
        
        current = self.config["ollama"].get("model", "")
        default_idx = "0"
        if current in models:
            default_idx = str(models.index(current) + 1)
        
        choice = input(f"\nWähle ({default_idx}): ").strip() or default_idx
        
        try:
            idx = int(choice)
            if idx == 0:
                self.config["ollama"]["enabled"] = False
                self.config["ollama"]["model"] = ""
                print("ℹ️  Ollama deaktiviert")
            elif 1 <= idx <= len(models):
                self.config["ollama"]["enabled"] = True
                self.config["ollama"]["model"] = models[idx - 1]
                print(f"✅ Ollama: {models[idx - 1]}")
            else:
                print("⚠️  Ungültige Auswahl, Ollama deaktiviert")
                self.config["ollama"]["enabled"] = False
        except:
            print("⚠️  Ungültige Eingabe, Ollama deaktiviert")
            self.config["ollama"]["enabled"] = False
    
    def _configure_tts(self):
        print("\n" + "-" * 40)
        print("🔊 TTS CONFIGURATION")
        print("-" * 40)
        
        voices = [
            "de_DE-eva_k-x_low",
            "de_DE-karlsson-low",
            "de_DE-kerstin-low",
            "de_DE-ramona-low",
        ]
        
        current = self.config["tts"].get("voice", voices[0])
        
        print("Verfügbare Stimmen:")
        for i, voice in enumerate(voices):
            marker = " ← current" if voice == current else ""
            print(f"   [{i+1}] {voice}{marker}")
        
        default_idx = str(voices.index(current) + 1) if current in voices else "1"
        choice = input(f"\nWähle ({default_idx}): ").strip() or default_idx
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(voices):
                self.config["tts"]["voice"] = voices[idx]
                print(f"✅ Stimme: {voices[idx]}")
        except:
            pass
        
        # TTS mode
        print("\nTTS Modus:")
        print("   [1] short - Nur erste Sätze vorlesen")
        print("   [2] full - Alles vorlesen")
        
        current_mode = self.config["tts"].get("mode", "short")
        default = "1" if current_mode == "short" else "2"
        
        mode_choice = input(f"\nWähle ({default}): ").strip() or default
        self.config["tts"]["mode"] = "short" if mode_choice == "1" else "full"
    
    def _configure_trigger(self):
        print("\n" + "-" * 40)
        print("⌨️  TRIGGER KEY")
        print("-" * 40)
        
        keys = ["rightctrl", "leftctrl", "rightalt", "leftalt", "pause"]
        current = self.config["trigger"].get("key", "rightctrl")
        
        print("Verfügbare Tasten:")
        for i, key in enumerate(keys):
            marker = " ← current" if key == current else ""
            print(f"   [{i+1}] {key}{marker}")
        
        default_idx = str(keys.index(current) + 1) if current in keys else "1"
        choice = input(f"\nWähle ({default_idx}): ").strip() or default_idx
        
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(keys):
                self.config["trigger"]["key"] = keys[idx]
                print(f"✅ Trigger: {keys[idx]}")
        except:
            pass
    
    def _check_cli_tools(self):
        print("\n" + "-" * 40)
        print("🔗 CLI TOOLS")
        print("-" * 40)
        
        for tool in ["gemini", "opencode", "claude"]:
            try:
                result = subprocess.run(["which", tool], capture_output=True, timeout=2)
                if result.returncode == 0:
                    print(f"✅ {tool}")
                else:
                    print(f"⚠️  {tool} not found")
            except:
                print(f"⚠️  {tool} not found")
    
    def _check_audio(self):
        print("\n" + "-" * 40)
        print("🔊 AUDIO PERMISSIONS")
        print("-" * 40)
        
        result = subprocess.run(["groups"], capture_output=True, text=True)
        groups = result.stdout.lower()
        
        if "audio" not in groups:
            print("⚠️  Add to audio group: sudo usermod -aG audio $USER")
        else:
            print("✅ Audio group OK")
        
        if "input" not in groups:
            print("⚠️  Add to input group: sudo usermod -aG input $USER")
        else:
            print("✅ Input group OK")
    
    def _create_launcher(self):
        print("\n" + "-" * 40)
        print("🚀 CREATING LAUNCHER")
        print("-" * 40)
        
        launcher = f'''#!/bin/bash
# Wanda JARVIS Voice Assistant
cd "{self.project_dir}"
source venv/bin/activate
exec python3 main.py "$@"
'''
        launcher_path = self.project_dir / "wanda"
        with open(launcher_path, "w") as f:
            f.write(launcher)
        os.chmod(launcher_path, 0o755)
        print(f"✅ Launcher: {launcher_path}")
        
        # Create symlink for global access
        global_link = Path.home() / ".local" / "bin" / "wanda"
        global_link.parent.mkdir(parents=True, exist_ok=True)
        try:
            if global_link.exists() or global_link.is_symlink():
                global_link.unlink()
            global_link.symlink_to(launcher_path)
            print(f"✅ Global: {global_link} (add ~/.local/bin to PATH)")
        except Exception as e:
            print(f"⚠️  Could not create global link: {e}")
    
    def _create_desktop_file(self):
        # Installer desktop file (in project)
        installer_desktop = f'''[Desktop Entry]
Name=Wanda Setup
Comment=Configure Wanda JARVIS Voice Assistant
Exec="{self.project_dir}/setup.py"
Icon=preferences-system
Terminal=true
Type=Application
Categories=Utility;Settings;
'''
        installer_path = self.project_dir / "Wanda-Setup.desktop"
        with open(installer_path, "w") as f:
            f.write(installer_desktop)
        os.chmod(installer_path, 0o755)
        print(f"✅ Desktop: {installer_path}")
        
        # Wanda desktop file
        wanda_desktop = f'''[Desktop Entry]
Name=Wanda JARVIS
Comment=Sovereign AI Voice Assistant
Exec="{self.project_dir}/wanda"
Icon=audio-input-microphone
Terminal=true
Type=Application
Categories=Utility;Accessibility;
'''
        wanda_desktop_path = self.project_dir / "Wanda.desktop"
        with open(wanda_desktop_path, "w") as f:
            f.write(wanda_desktop)
        os.chmod(wanda_desktop_path, 0o755)
        
        # Also add to ~/.local/share/applications
        app_dir = Path.home() / ".local" / "share" / "applications"
        app_dir.mkdir(parents=True, exist_ok=True)
        try:
            (app_dir / "wanda.desktop").write_text(wanda_desktop)
            print(f"✅ App Menu: wanda.desktop added")
        except:
            pass
    
    def _save_config(self):
        print("\n" + "-" * 40)
        print("💾 SAVING CONFIGURATION")
        print("-" * 40)
        
        # Ensure we have yaml
        try:
            import yaml
            with open(self.config_path, "w") as f:
                yaml.dump(self.config, f, default_flow_style=False, sort_keys=False)
            print(f"✅ Config saved: {self.config_path}")
        except ImportError:
            # Fallback: write as simple format
            print("⚠️  YAML not available, using basic format")
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=2)
    
    def _print_success(self):
        print("\n" + "=" * 60)
        print("✅ CONFIGURATION COMPLETE!")
        print("=" * 60)
        
        print("\n🎙️  Start Wanda:")
        print(f"   {self.project_dir}/wanda")
        print("   OR double-click: Wanda.desktop")
        print("   OR from anywhere: wanda (if ~/.local/bin in PATH)")
        
        print("\n⚙️  Reconfigure anytime:")
        print(f"   python3 {self.project_dir}/setup.py")
        print("   OR double-click: Wanda-Setup.desktop")
        
        print("\n📋 Your Settings:")
        print(f"   Trigger: {self.config['trigger']['key']}")
        print(f"   TTS: {self.config['tts']['voice']} ({self.config['tts']['mode']})")
        if self.config["ollama"]["enabled"]:
            print(f"   Ollama: {self.config['ollama']['model']}")
        else:
            print("   Ollama: disabled")
        
        print("=" * 60 + "\n")


def main():
    setup = WandaSetup()
    setup.run()


if __name__ == "__main__":
    main()
