# Wanda Voice Assistant - Config Module
"""Configuration management for Wanda."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class Config:
    """Configuration loader and manager."""

    DEFAULT_CONFIG = {
        "mode": "chat",
        "intent": "auto",
        "trigger": {"type": "focus_hotkey", "key": "rightctrl"},
        "audio": {
            "backend": "pipewire",
            "sample_rate": 44100,
            "max_seconds": 15,
            "silence_timeout": 1.2,
            "silence_threshold": 0.01,
            "min_seconds": 1.0,
        },
        "stt": {
            "engine": "faster-whisper",
            "model": "large-v3-turbo",
            "device": "auto",  # auto, cuda, cpu
        },
        "confirm": {"enabled": True, "edit_mode": "inline"},
        "preprocess": {"enabled": True, "rewrite": "template"},
        "tts": {
            "engine": "piper",
            "voice": "de_DE-eva_k-x_low",
            "mode": "short",
            "alternatives": [
                "de_DE-karlsson-low",
                "de_DE-kerstin-low",
                "de_DE-ramona-low",
            ],
        },
        "output": {"speak": True},
        "wake_word": {"enabled": True},
        "pipeline": {
            "stt_tts_only": False,
            "speak_transcript": True,
            "transcript_prefix": "Verstanden: ",
        },
        "history": {"max_turns": 12, "persist": False},
        "adapters": {"target": "gemini_cli", "gemini_model": "flash"},
        "security": {"redact_secrets": False},
    }

    def __init__(self, config_path: Optional[Path] = None):
        """Initialize config loader."""
        if config_path is None:
            # Default to wanda.config.yaml in project root
            base_dir = Path(__file__).parent.parent
            config_path = base_dir / "wanda.config.yaml"
        else:
            config_path = Path(config_path)

        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load config from YAML file, create default if not exists."""
        if not self.config_path.exists():
            print(f"[Config] Creating default config at {self.config_path}")
            self._save_default_config()
            return self.DEFAULT_CONFIG.copy()

        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)
            print(f"[Config] Loaded from {self.config_path}")
            return config
        except Exception as e:
            print(f"[Config] Error loading config: {e}")
            print("[Config] Using default config")
            return self.DEFAULT_CONFIG.copy()

    def _save_default_config(self):
        """Save default config to file."""
        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_path, "w") as f:
                yaml.dump(
                    self.DEFAULT_CONFIG, f, default_flow_style=False, sort_keys=False
                )
        except Exception as e:
            print(f"[Config] Error saving default config: {e}")

    def get(self, key: str, default=None):
        """Get config value by key."""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    @property
    def stt(self) -> Dict[str, Any]:
        """Get STT config."""
        return self.config.get("stt", {})

    @property
    def tts(self) -> Dict[str, Any]:
        """Get TTS config."""
        return self.config.get("tts", {})

    @property
    def audio_config(self) -> Dict[str, Any]:
        """Get audio config."""
        return self.config.get("audio", {})

    @property
    def gemini_config(self) -> Dict[str, Any]:
        """Get Gemini adapter config."""
        return self.config.get("adapters", {})
