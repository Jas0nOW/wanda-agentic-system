"""Prompt refiner using Ollama for WANDA Voice Core."""

from __future__ import annotations
import json
from typing import Optional

from wanda_voice_core.schemas import RefinerResult, RefinerAction

REFINER_SYSTEM_PROMPT = """Du bist Wandas Prompt-Optimierer. Du erhältst einen rohen Sprachtext und verbesserst ihn.

REGELN:
- Entferne Füllwörter (ähm, also, halt, sozusagen)
- Korrigiere Grammatik und Interpunktion
- Füge fehlenden Kontext hinzu wenn offensichtlich
- Behalte die ursprüngliche Absicht bei
- Antworte IMMER im folgenden JSON-Format, NICHTS anderes:

{
  "intent": "<kurze Absichtsbeschreibung>",
  "improved_text": "<verbesserter Text>",
  "do": "send|ask|edit",
  "questions": [],
  "token_budget": {"max_output_tokens": 2048}
}

"do" Regeln:
- "send": Text ist klar, kann direkt gesendet werden
- "ask": Text ist unklar, questions enthält Rückfragen
- "edit": Text braucht manuelle Überarbeitung"""


class PromptRefiner:
    """Refines raw speech transcripts using Ollama."""

    def __init__(self, ollama_url: str = "http://localhost:11434",
                 model: str = "qwen3:8b", timeout: int = 30):
        self.ollama_url = ollama_url
        self.model = model
        self.timeout = timeout

    async def refine(self, raw_text: str) -> RefinerResult:
        """Refine raw transcript. Falls back to passthrough if Ollama unavailable."""
        try:
            return await self._refine_via_ollama(raw_text)
        except Exception as e:
            print(f"[Refiner] Ollama unavailable ({e}), using passthrough")
            return self._passthrough(raw_text)

    async def _refine_via_ollama(self, raw_text: str) -> RefinerResult:
        """Call Ollama HTTP API for refinement."""
        import aiohttp

        payload = {
            "model": self.model,
            "prompt": f"Verbessere diesen Sprachtext:\n\n{raw_text}",
            "system": REFINER_SYSTEM_PROMPT,
            "stream": False,
            "format": "json",
            "options": {"temperature": 0.3, "num_predict": 512},
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=aiohttp.ClientTimeout(total=self.timeout),
            ) as resp:
                if resp.status != 200:
                    raise ConnectionError(f"Ollama returned {resp.status}")
                data = await resp.json()

        response_text = data.get("response", "")
        return self._parse_response(response_text, raw_text)

    def _parse_response(self, response_text: str, original: str) -> RefinerResult:
        """Parse Ollama JSON response into RefinerResult."""
        try:
            parsed = json.loads(response_text)
            action = parsed.get("do", "send")
            try:
                action_enum = RefinerAction(action)
            except ValueError:
                action_enum = RefinerAction.SEND

            return RefinerResult(
                intent=parsed.get("intent", "unknown"),
                improved_text=parsed.get("improved_text", original),
                do=action_enum,
                questions=parsed.get("questions", []),
                token_budget=parsed.get("token_budget", {"max_output_tokens": 2048}),
            )
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[Refiner] Failed to parse response: {e}")
            return self._passthrough(original)

    def _passthrough(self, text: str) -> RefinerResult:
        """Return input as-is when refinement unavailable."""
        return RefinerResult(
            intent="passthrough",
            improved_text=text,
            do=RefinerAction.SEND,
        )

    def refine_sync(self, raw_text: str) -> RefinerResult:
        """Synchronous refinement using requests (for non-async contexts)."""
        try:
            import requests
            payload = {
                "model": self.model,
                "prompt": f"Verbessere diesen Sprachtext:\n\n{raw_text}",
                "system": REFINER_SYSTEM_PROMPT,
                "stream": False,
                "format": "json",
                "options": {"temperature": 0.3, "num_predict": 512},
            }
            resp = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                return self._parse_response(data.get("response", ""), raw_text)
        except Exception as e:
            print(f"[Refiner] Sync refinement failed: {e}")
        return self._passthrough(raw_text)
