"""Extended configuration for WANDA Voice Core."""

from __future__ import annotations
from pathlib import Path
from typing import Any, Optional

import yaml


# Profiles
PROFILES = {
    "gui": {
        "ui": {"orb": True, "log_window": True},
        "tts": {"engine": "edge", "voice": "katja", "mode": "short"},
    },
    "simple": {
        "ui": {"orb": False, "log_window": False},
        "tts": {"engine": "piper", "voice": "de_DE-kerstin-low", "mode": "short"},
    },
    "offline": {
        "ui": {"orb": False, "log_window": False},
        "tts": {"engine": "piper", "voice": "de_DE-kerstin-low", "mode": "short"},
        "providers": {"primary": "ollama", "gemini_enabled": False},
    },
}


DEFAULT_CONFIG: dict[str, Any] = {
    "profile": "gui",
    "audio": {
        "backend": "pipewire",
        "sample_rate": 16000,
        "max_seconds": 60,
        "silence_timeout": 1.2,
        "silence_threshold": 0.01,
        "min_seconds": 1.0,
    },
    "vad": {
        "engine": "silero",
        "min_silence_duration_ms": 500,
    },
    "stt": {
        "engine": "faster-whisper",
        "model": "large-v3-turbo",
        "device": "auto",
        "language": "de",
    },
    "router": {
        "use_ollama": False,
        "confidence_threshold": 0.6,
    },
    "refiner": {
        "enabled": True,
        "model": "qwen3:8b",
        "timeout": 30,
    },
    "providers": {
        "primary": "gemini_cli",
        "gemini_model": "flash",
        "gemini_timeout": 90,
        "gemini_max_retries": 2,
        "gemini_fallback_model": "pro",
        "ollama_model": "qwen3:8b",
        "ollama_enabled": False,
        "ollama_as_fallback": False,
    },
    "tts": {
        "engine": "edge",
        "voice": "katja",
        "mode": "short",
        "piper_voice": "de_DE-kerstin-low",
        "interruptable": True,
    },
    "safety": {
        "command_execution": False,
        "risk_threshold_voice": 3,
        "risk_threshold_gui": 6,
        "redact_secrets": True,
    },
    "token_economy": {
        "max_context_chars": 8000,
        "max_turns": 12,
        "max_output_tokens": 2048,
    },
    "ui": {
        "orb": True,
        "log_window": True,
        "orb_size": 60,
    },
    "hotkey": {
        "key": "rightctrl",
        "mode": "toggle",  # "toggle" or "hold"
    },
    "confirmation": {
        "enabled": True,
        "timeout": 10,
        "readback": True,
    },
    "api": {
        "enabled": False,
        "port": 8370,
        "host": "127.0.0.1",
    },
    "history": {
        "max_turns": 12,
        "persist": False,
    },
}


def _deep_merge(base: dict, override: dict) -> dict:
    """Deep merge override into base."""
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


class VoiceCoreConfig:
    """Configuration loader for WANDA Voice Core."""

    def __init__(self, config_path: Optional[Path] = None, profile: Optional[str] = None):
        if config_path is None:
            # Search common locations
            candidates = [
                Path.cwd() / "wanda_voice.yaml",
                Path.home() / ".wanda" / "voice.yaml",
                Path.home() / ".wanda-system" / "wanda-voice" / "wanda.config.yaml",
            ]
            for c in candidates:
                if c.exists():
                    config_path = c
                    break

        self._raw = self._load(config_path)

        # Apply profile defaults first, then user config on top
        active_profile = profile or self._raw.get("profile", "gui")
        profile_defaults = PROFILES.get(active_profile, {})
        self.config = _deep_merge(
            _deep_merge(DEFAULT_CONFIG, profile_defaults),
            self._raw,
        )

    def _load(self, path: Optional[Path]) -> dict[str, Any]:
        if path is None or not path.exists():
            return {}
        try:
            with open(path) as f:
                data = yaml.safe_load(f) or {}
            print(f"[Config] Loaded from {path}")
            return data
        except Exception as e:
            print(f"[Config] Error loading {path}: {e}")
            return {}

    def get(self, key: str, default: Any = None) -> Any:
        """Dot-notation access: config.get('providers.gemini_model')."""
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    @property
    def audio(self) -> dict[str, Any]:
        return self.config.get("audio", {})

    @property
    def stt(self) -> dict[str, Any]:
        return self.config.get("stt", {})

    @property
    def tts(self) -> dict[str, Any]:
        return self.config.get("tts", {})

    @property
    def providers(self) -> dict[str, Any]:
        return self.config.get("providers", {})

    @property
    def safety(self) -> dict[str, Any]:
        return self.config.get("safety", {})

    @property
    def api(self) -> dict[str, Any]:
        return self.config.get("api", {})

    @property
    def confirmation(self) -> dict[str, Any]:
        return self.config.get("confirmation", {})

    def to_dict(self) -> dict[str, Any]:
        return dict(self.config)
