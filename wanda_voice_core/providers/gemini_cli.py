"""Gemini CLI provider for WANDA Voice Core."""

from __future__ import annotations
import asyncio
import subprocess
import time
from typing import Optional

from wanda_voice_core.providers.base import ProviderBase
from wanda_voice_core.token_economy import truncate_to_budget, MAX_CONTEXT_CHARS


class GeminiCLIProvider(ProviderBase):
    """LLM provider using Gemini CLI with retry/timeout/fallback."""

    name = "gemini_cli"

    def __init__(
        self,
        model: str = "flash",
        gemini_path: str = "gemini",
        timeout: int = 90,
        max_retries: int = 2,
        fallback_model: Optional[str] = "pro",
        local_fallback: bool = True,
        local_model: str = "qwen3:8b",
    ):
        self.model = model
        self.gemini_path = gemini_path
        self.timeout = timeout
        self.max_retries = max_retries
        self.fallback_model = fallback_model
        self.local_fallback = local_fallback
        self.local_model = local_model
        self._local_provider: Optional[ProviderBase] = None
        self.history: list[dict[str, str]] = []
        self._available: Optional[bool] = None

    def is_available(self) -> bool:
        if self._available is not None:
            return self._available
        try:
            result = subprocess.run(
                [self.gemini_path, "--version"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            self._available = result.returncode == 0
        except Exception:
            self._available = False
        return self._available

    async def send(self, prompt: str, context: Optional[str] = None) -> str:
        """Send prompt with retry logic and fallback."""
        full_prompt = self._build_prompt(prompt, context)
        # Enforce token budget
        full_prompt = truncate_to_budget(full_prompt, MAX_CONTEXT_CHARS)

        # Try primary model with retries
        for attempt in range(self.max_retries + 1):
            current_timeout = self.timeout + (attempt * 30)
            result = await self._call_gemini(self.model, full_prompt, current_timeout)
            if result is not None:
                self._update_history(prompt, result)
                return result

            if attempt < self.max_retries:
                wait = 2 ** (attempt + 1)  # 2s, 4s
                print(f"[Gemini] Retry in {wait}s...")
                await asyncio.sleep(wait)

        # Try fallback model
        if self.fallback_model:
            print(f"[Gemini] Trying fallback: {self.fallback_model}")
            result = await self._call_gemini(
                self.fallback_model, full_prompt, self.timeout + 60
            )
            if result is not None:
                self._update_history(prompt, result)
                return result

        if self.local_fallback:
            local_result = await self._try_local_fallback(full_prompt)
            if local_result is not None:
                self._update_history(prompt, local_result)
                return local_result

        return "Gemini ist gerade nicht erreichbar. Bitte versuche es nochmal."

    async def _try_local_fallback(self, prompt: str) -> Optional[str]:
        try:
            from wanda_voice_core.providers.ollama import OllamaProvider

            if self._local_provider is None:
                print(f"[Gemini] Initializing local fallback: {self.local_model}")
                self._local_provider = OllamaProvider(model=self.local_model)

            if self._local_provider.is_available():
                print(f"[Gemini] Using local fallback (Ollama)")
                return await self._local_provider.send(prompt)
        except Exception as e:
            print(f"[Gemini] Local fallback error: {e}")
        return None

    async def _call_gemini(
        self, model: str, prompt: str, timeout: int
    ) -> Optional[str]:
        """Execute Gemini CLI command securely via stdin to avoid process list leaks."""
        proc = None
        try:
            started = time.time()
            # SECURITY FIX: Use stdin instead of command line argument to prevent
            # prompt from appearing in process lists (ps, top, etc.)
            proc = await asyncio.create_subprocess_exec(
                self.gemini_path,
                model,
                "-",  # Read from stdin
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
            )
            # Send prompt via stdin
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=prompt.encode()), timeout=timeout
            )
            elapsed = round(time.time() - started, 2)
            if proc.returncode == 0:
                if stderr:
                    print(f"[Gemini] stderr: {stderr.decode().strip()[:200]}")
                print(f"[Gemini] ok ({elapsed}s, {len(stdout)} bytes)")
                return stdout.decode().strip()
            print(f"[Gemini] Error: {stderr.decode().strip()[:200]}")
        except asyncio.TimeoutError:
            print(f"[Gemini] Timeout ({timeout}s)")
            try:
                if proc:
                    proc.kill()
            except Exception:
                pass
        except FileNotFoundError:
            print(f"[Gemini] Binary not found: {self.gemini_path}")
            self._available = False
        except Exception as e:
            print(f"[Gemini] Exception: {e}")
        return None

    def _build_prompt(self, prompt: str, context: Optional[str] = None) -> str:
        parts = []
        if context:
            parts.append(context)
        if self.history:
            history_str = "\n".join(
                f"{m['role']}: {m['content']}" for m in self.history[-24:]
            )
            parts.append(history_str)
        parts.append(f"User: {prompt}")
        return "\n\n".join(parts)

    def _update_history(self, prompt: str, response: str) -> None:
        self.history.append({"role": "user", "content": prompt})
        self.history.append({"role": "assistant", "content": response})
        # Trim to max turns
        max_msgs = 24
        if len(self.history) > max_msgs:
            self.history = self.history[-max_msgs:]

    def clear_history(self) -> None:
        self.history.clear()
