"""OVOS Skill: WANDA Bridge - forwards utterances to WANDA Voice Core API."""

from __future__ import annotations
import json
from typing import Optional

try:
    from ovos_workshop.skills import OVOSSkill
    from ovos_workshop.decorators import fallback_handler
    OVOS_AVAILABLE = True
except ImportError:
    # Stub for development without OVOS
    OVOS_AVAILABLE = False

    class OVOSSkill:
        def __init__(self, *a, **kw): pass
        def speak(self, text): print(f"[OVOS-Stub] {text}")
        def log(self): return type("L", (), {"info": print, "error": print, "warning": print})()
        @property
        def settings(self): return {}

    def fallback_handler(priority=50):
        def dec(fn): return fn
        return dec


class WandaBridgeSkill(OVOSSkill):
    """Forwards all unhandled utterances to WANDA Voice Core API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wanda_url = "http://localhost:8370"

    def initialize(self):
        self.wanda_url = self.settings.get("wanda_api_url", "http://localhost:8370")
        self.log.info(f"[WandaBridge] API URL: {self.wanda_url}")

    @fallback_handler(priority=90)
    def handle_fallback(self, message) -> bool:
        """Catch-all fallback: send to WANDA."""
        utterance = message.data.get("utterance", "")
        if not utterance:
            return False

        response = self._send_to_wanda(utterance)
        if response:
            self.speak(response)
            return True
        return False

    def _send_to_wanda(self, text: str) -> Optional[str]:
        """Send utterance to WANDA API."""
        try:
            import requests
            resp = requests.post(
                f"{self.wanda_url}/v1/utterance",
                json={"text": text, "mode": "text"},
                timeout=120,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("response_text", "")
            self.log.error(f"[WandaBridge] API error: {resp.status_code}")
        except Exception as e:
            self.log.error(f"[WandaBridge] Connection error: {e}")
        return None


def create_skill():
    return WandaBridgeSkill()
