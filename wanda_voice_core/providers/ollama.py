"""Ollama provider for WANDA Voice Core."""

from __future__ import annotations
import json
from typing import Any, Optional

from wanda_voice_core.providers.base import ProviderBase
from wanda_voice_core.token_economy import truncate_to_budget, MAX_CONTEXT_CHARS


class OllamaProvider(ProviderBase):
    """LLM provider using Ollama HTTP API."""

    name = "ollama"

    def __init__(
        self,
        model: str = "qwen3:8b",
        api_url: str = "http://localhost:11434",
        timeout: int = 60,
        auto_start: bool = True,
    ):
        self.model = model
        self.api_url = api_url
        self.timeout = timeout
        self.auto_start = auto_start
        self._available: Optional[bool] = None

    def is_available(self) -> bool:
        try:
            import requests
            resp = requests.get(f"{self.api_url}/api/tags", timeout=3)
            self._available = resp.status_code == 200
        except Exception:
            self._available = False
        return self._available

    async def send(self, prompt: str, context: Optional[str] = None) -> str:
        """Send prompt to Ollama."""
        import aiohttp

        full_prompt = prompt
        if context:
            full_prompt = truncate_to_budget(
                f"{context}\n\nUser: {prompt}", MAX_CONTEXT_CHARS
            )

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": full_prompt,
            "stream": False,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("response", "").strip()
                    return f"Ollama error: HTTP {resp.status}"
        except Exception as e:
            print(f"[Ollama] Error: {e}")
            return f"Ollama nicht erreichbar: {e}"

    async def generate_json(self, prompt: str, system: str = "",
                            model: Optional[str] = None) -> Optional[dict]:
        """Generate structured JSON response."""
        import aiohttp

        payload: dict[str, Any] = {
            "model": model or self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.3, "num_predict": 512},
        }
        if system:
            payload["system"] = system

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.api_url}/api/generate",
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                ) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return json.loads(data.get("response", "{}"))
        except Exception as e:
            print(f"[Ollama] JSON generation error: {e}")
        return None

    def ensure_running(self) -> bool:
        """Start Ollama if not running (delegates to system)."""
        if self.is_available():
            return True
        if not self.auto_start:
            return False
        try:
            import subprocess
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )
            import time
            for _ in range(15):
                time.sleep(1)
                if self.is_available():
                    return True
        except Exception as e:
            print(f"[Ollama] Failed to start: {e}")
        return False
