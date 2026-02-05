"""Main WANDA Voice Engine - pipeline orchestrator."""

from __future__ import annotations
import asyncio
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Optional

from wanda_voice_core.schemas import (
    ConfirmationState,
    EngineResult,
    RefinerAction,
    RefinerResult,
    RouteType,
    RunEvent,
    TokenMetrics,
)
from wanda_voice_core.config import VoiceCoreConfig
from wanda_voice_core.event_bus import EventBus
from wanda_voice_core.run_manager import RunManager
from wanda_voice_core.router import IntentRouter
from wanda_voice_core.refiner import PromptRefiner
from wanda_voice_core.safety import SafetyPolicy
from wanda_voice_core.confirmation import ConfirmationFlow
from wanda_voice_core.token_economy import (
    truncate_to_budget,
    redact_sensitive,
    estimate_tokens,
    MAX_CONTEXT_CHARS,
)
from wanda_voice_core.providers.base import ProviderBase


class WandaVoiceEngine:
    """Main engine orchestrating the full voice pipeline.

    Pipeline: Text -> Router -> (Refiner?) -> Confirmation -> Provider -> TTS
    """

    def __init__(self, config: Optional[VoiceCoreConfig] = None):
        self.config = config or VoiceCoreConfig()
        self.event_bus = EventBus()
        self.run_manager = RunManager()

        # Core modules
        self.router = IntentRouter(
            confidence_threshold=self.config.get("router.confidence_threshold", 0.6)
        )
        self.refiner = PromptRefiner(
            model=self.config.get("refiner.model", "qwen3:8b"),
            timeout=self.config.get("refiner.timeout", 30),
        )
        self.refiner_enabled = self.config.get("refiner.enabled", True)
        self.safety = SafetyPolicy(
            command_execution=self.config.get("safety.command_execution", False),
            risk_threshold_voice=self.config.get("safety.risk_threshold_voice", 3),
            risk_threshold_gui=self.config.get("safety.risk_threshold_gui", 6),
        )

        # Providers (set externally or via _init_providers)
        self._primary_provider: Optional[ProviderBase] = None
        self._fallback_provider: Optional[ProviderBase] = None

        # Confirmation flow (requires tts/stt callbacks, set via set_io)
        self._tts_speak: Optional[Callable] = None
        self._stt_listen: Optional[Callable] = None
        self._confirmation: Optional[ConfirmationFlow] = None

        # Clipboard tool detection
        self._clipboard_tool = self._detect_clipboard_tool()
        self._typing_tool = self._detect_typing_tool()

    # --- Setup ---

    def set_providers(
        self, primary: ProviderBase, fallback: Optional[ProviderBase] = None
    ) -> None:
        self._primary_provider = primary
        self._fallback_provider = fallback

    def set_io(self, tts_speak: Callable, stt_listen: Callable) -> None:
        """Set TTS and STT callbacks for confirmation flow."""
        self._tts_speak = tts_speak
        self._stt_listen = stt_listen
        self._confirmation = ConfirmationFlow(
            event_bus=self.event_bus,
            tts_speak=tts_speak,
            stt_listen=stt_listen,
            timeout=self.config.get("confirmation.timeout", 10),
        )

    def set_refiner_enabled(self, enabled: bool) -> None:
        self.refiner_enabled = bool(enabled)
        self.event_bus.emit("refiner.toggle", {"enabled": self.refiner_enabled})

    def override_confirmation(self, action: ConfirmationState) -> None:
        if self._confirmation:
            self._confirmation.set_override(action)

    # --- Main Pipeline ---

    async def process_text(
        self, text: str, skip_confirmation: bool = False
    ) -> EngineResult:
        """Process text input through the full pipeline (for API/OVOS)."""
        run_id = self.run_manager.start_run()
        result = EngineResult(run_id=run_id)
        t0 = time.time()

        try:
            self.event_bus.emit("run.start", {"text": text[:100]}, run_id=run_id)
            result.transcript = text

            # Safety check
            safety_result = self.safety.check_text(text)
            self.event_bus.emit(
                "safety.check",
                {
                    "risk_level": safety_result.risk_level.value,
                    "risk_score": safety_result.risk_score,
                },
                run_id=run_id,
            )

            if safety_result.risk_level.value == "blocked":
                result.error = safety_result.message
                self.event_bus.emit(
                    "safety.blocked", {"message": safety_result.message}, run_id=run_id
                )
                return result

            # Route
            route_result = self.router.route(text)
            result.route = route_result.route
            self.event_bus.emit(
                "router.result",
                {
                    "route": route_result.route.value,
                    "confidence": route_result.confidence,
                },
                run_id=run_id,
            )

            # Handle commands directly
            if route_result.route == RouteType.COMMAND:
                result.response_text = f"Kommando: {route_result.command}"
                return result

            # Refine / confirm
            improved_text = text
            confirmation_enabled = (
                not skip_confirmation
                and self._confirmation
                and self.config.get("confirmation.enabled", True)
            )

            if (
                route_result.route == RouteType.REFINE
                and self.refiner_enabled
                and self.config.get("refiner.enabled", True)
            ):
                refiner_result = await self.refiner.refine(text)
                improved_text = refiner_result.improved_text
                result.improved_text = improved_text
                self.event_bus.emit(
                    "refiner.result",
                    {
                        "intent": refiner_result.intent,
                        "action": refiner_result.do.value,
                        "improved_text": improved_text,
                    },
                    run_id=run_id,
                )

                if confirmation_enabled:
                    action = await self._confirmation.run(refiner_result, run_id=run_id)
                    result.confirmation_action = action
                    if action == ConfirmationState.CANCEL:
                        return result
                    elif action == ConfirmationState.REDO:
                        return result
                    elif action == ConfirmationState.EDIT:
                        return result
            elif not self.refiner_enabled and confirmation_enabled:
                refiner_result = RefinerResult(
                    intent="raw",
                    improved_text=text,
                    do=RefinerAction.SEND,
                )
                result.improved_text = text
                self.event_bus.emit(
                    "refiner.skipped",
                    {
                        "reason": "disabled",
                    },
                    run_id=run_id,
                )
                action = await self._confirmation.run(refiner_result, run_id=run_id)
                result.confirmation_action = action
                if action == ConfirmationState.CANCEL:
                    return result
                elif action == ConfirmationState.REDO:
                    return result
                elif action == ConfirmationState.EDIT:
                    return result
            else:
                result.improved_text = text

            # Redact and truncate
            prompt = redact_sensitive(improved_text)
            prompt = truncate_to_budget(prompt, MAX_CONTEXT_CHARS)

            # Send to provider
            response = await self._send_to_provider(prompt, run_id)
            result.response_text = response

            # Metrics
            latency = (time.time() - t0) * 1000
            result.metrics = {
                "chars_in": len(prompt),
                "chars_out": len(response),
                "token_est_in": estimate_tokens(prompt),
                "token_est_out": estimate_tokens(response),
                "latency_ms": latency,
            }
            self.event_bus.emit("metrics.update", result.metrics, run_id=run_id)

        except Exception as e:
            result.error = str(e)
            self.event_bus.emit("error", {"message": str(e)}, run_id=run_id)
        finally:
            self.event_bus.emit(
                "run.end",
                {
                    "has_error": result.error is not None,
                },
                run_id=run_id,
            )
            self.run_manager.end_run(
                {"result": result.response_text[:200] if result.response_text else ""}
            )

        return result

    async def process_audio(
        self, audio_data: Any, stt_engine: Any = None
    ) -> EngineResult:
        """Process audio input: STT -> pipeline.

        Args:
            audio_data: numpy array of audio samples
            stt_engine: STT engine with .transcribe(audio, language) method
        """
        run_id = self.run_manager.start_run()
        self.event_bus.emit("recording.stop", {}, run_id=run_id)

        if stt_engine is None:
            return EngineResult(run_id=run_id, error="No STT engine provided")

        # Transcribe
        self.event_bus.emit("stt.result", {"status": "transcribing"}, run_id=run_id)
        language = self.config.get("stt.language", "de")

        try:
            text = stt_engine.transcribe(audio_data, language=language)
        except Exception as e:
            return EngineResult(run_id=run_id, error=f"STT error: {e}")

        if not text or not text.strip():
            self.event_bus.emit("stt.result", {"status": "empty"}, run_id=run_id)
            return EngineResult(
                run_id=run_id, transcript="", error="No speech detected"
            )

        self.event_bus.emit("stt.result", {"text": text[:100]}, run_id=run_id)

        # Close current run and delegate to process_text
        self.run_manager.end_run()
        return await self.process_text(text)

    # --- Provider ---

    async def _send_to_provider(self, prompt: str, run_id: str) -> str:
        """Send prompt to primary provider with fallback."""
        if not self._primary_provider:
            return "Kein Provider konfiguriert."

        self.event_bus.emit(
            "provider.request",
            {
                "provider": self._primary_provider.name,
                "chars": len(prompt),
            },
            run_id=run_id,
        )

        try:
            response = await self._primary_provider.send(prompt)
            self.event_bus.emit(
                "provider.response",
                {
                    "provider": self._primary_provider.name,
                    "chars": len(response),
                },
                run_id=run_id,
            )
            return response
        except Exception as e:
            self.event_bus.emit(
                "provider.error",
                {
                    "provider": self._primary_provider.name,
                    "error": str(e),
                },
                run_id=run_id,
            )

            # Try fallback
            if self._fallback_provider:
                try:
                    response = await self._fallback_provider.send(prompt)
                    self.event_bus.emit(
                        "provider.response",
                        {
                            "provider": self._fallback_provider.name,
                            "chars": len(response),
                            "fallback": True,
                        },
                        run_id=run_id,
                    )
                    return response
                except Exception as e2:
                    self.event_bus.emit(
                        "provider.timeout",
                        {
                            "error": str(e2),
                        },
                        run_id=run_id,
                    )

            return "Provider nicht erreichbar. Bitte versuche es nochmal."

    # --- Clipboard / Typing ---

    def copy_to_clipboard(self, text: str) -> bool:
        """Copy text to system clipboard."""
        if not self._clipboard_tool:
            return False
        try:
            proc = subprocess.Popen(
                self._clipboard_tool,
                stdin=subprocess.PIPE,
            )
            proc.communicate(input=text.encode())
            return proc.returncode == 0
        except Exception:
            return False

    def type_text(self, text: str) -> bool:
        """Type text into active window using wtype/xdotool."""
        if not self._typing_tool:
            return False
        try:
            subprocess.run(
                [*self._typing_tool, text],
                timeout=5,
                check=True,
            )
            return True
        except Exception:
            return False

    def paste_to_active_window(self, text: str) -> bool:
        """Copy to clipboard then paste via keyboard shortcut."""
        if not self.copy_to_clipboard(text):
            return False
        try:
            if self._typing_tool and self._typing_tool[0] == "wtype":
                subprocess.run(["wtype", "-M", "ctrl", "v", "-m", "ctrl"], timeout=3)
            else:
                subprocess.run(["xdotool", "key", "ctrl+v"], timeout=3)
            return True
        except Exception:
            return False

    # --- Detection ---

    def _detect_clipboard_tool(self) -> Optional[list[str]]:
        """Detect clipboard command (wl-copy or xclip)."""
        import shutil

        if shutil.which("wl-copy"):
            return ["wl-copy"]
        if shutil.which("xclip"):
            return ["xclip", "-selection", "clipboard"]
        return None

    def _detect_typing_tool(self) -> Optional[list[str]]:
        """Detect typing tool (wtype or xdotool)."""
        import shutil
        import os

        if os.environ.get("WAYLAND_DISPLAY") and shutil.which("wtype"):
            return ["wtype"]
        if shutil.which("xdotool"):
            return ["xdotool", "type", "--"]
        return None
