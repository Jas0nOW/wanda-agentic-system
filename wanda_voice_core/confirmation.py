"""Voice confirmation flow for WANDA Voice Core."""

from __future__ import annotations
import asyncio
import queue
from typing import Any, Callable, Optional

from wanda_voice_core.schemas import ConfirmationState, RefinerResult
from wanda_voice_core.event_bus import EventBus


# Confirmation command detection
CONFIRM_COMMANDS = {
    ConfirmationState.SEND: [
        "abschicken",
        "abschike",
        "abschik",
        "abschick",
        "senden",
        "send",
        "ja",
        "passt",
        "go",
        "los",
        "schick ab",
        "schick",
        "ok",
        "das passt",
    ],
    ConfirmationState.EDIT: [
        "verändern",
        "ändern",
        "bearbeiten",
        "edit",
        "editieren",
    ],
    ConfirmationState.REDO: [
        "nochmal",
        "von vorn",
        "neu",
        "von vorne",
        "redo",
        "restart",
    ],
    ConfirmationState.CANCEL: [
        "stop",
        "abbrechen",
        "cancel",
        "nein",
        "vergiss es",
        "stopp",
    ],
}


def detect_confirmation_command(text: str) -> Optional[ConfirmationState]:
    """Detect a confirmation command from text."""
    import difflib

    if not text:
        return None

    normalized = text.lower().strip()

    for state, keywords in CONFIRM_COMMANDS.items():
        for kw in keywords:
            if normalized == kw:
                return state

            if (
                normalized.startswith(kw + " ")
                or normalized.endswith(" " + kw)
                or f" {kw} " in normalized
            ):
                return state

            if len(kw) > 3:
                ratio = difflib.SequenceMatcher(None, normalized, kw).ratio()
                if ratio > 0.8:
                    return state

                words = normalized.split()
                for word in words:
                    if len(word) > 3:
                        word_ratio = difflib.SequenceMatcher(None, word, kw).ratio()
                        if word_ratio > 0.85:
                            return state

    return None


class ConfirmationFlow:
    """Orchestrates voice confirmation: readback -> listen -> decide."""

    def __init__(
        self,
        event_bus: EventBus,
        tts_speak: Callable[[str], Any],
        stt_listen: Callable[[], Optional[str]],
        timeout: float = 10.0,
    ):
        self.event_bus = event_bus
        self.tts_speak = tts_speak
        self.stt_listen = stt_listen
        self.timeout = timeout
        self.state = ConfirmationState.IDLE
        self._override_queue: queue.Queue[ConfirmationState] = queue.Queue()

    def _set_state(
        self, state: ConfirmationState, run_id: Optional[str] = None
    ) -> None:
        old = self.state
        self.state = state
        self.event_bus.emit(
            "state.change",
            {"old": old.value, "new": state.value, "component": "confirmation"},
            run_id=run_id,
        )

    async def run(
        self, refined: RefinerResult, run_id: Optional[str] = None
    ) -> ConfirmationState:
        """Execute the full confirmation flow.

        Returns the final action: SEND, EDIT, REDO, or CANCEL.
        """
        # 1. Readback
        self._set_state(ConfirmationState.READBACK, run_id)
        self.event_bus.emit(
            "confirmation.ask",
            {
                "text": refined.improved_text,
                "phase": "readback",
            },
            run_id=run_id,
        )

        readback = f"Hier ist die verbesserte Version: {refined.improved_text}"
        await self._speak(readback)

        # 2. Ask what to do
        self._set_state(ConfirmationState.AWAITING_RESPONSE, run_id)
        ask_text = "Soll ich abschicken oder verändern?"
        await self._speak(ask_text)

        # 3. Listen for response
        response_text, override = await self._wait_for_response(self.timeout)

        if override:
            self._set_state(override, run_id)
            self.event_bus.emit(
                "confirmation.response",
                {
                    "action": override.value,
                    "source": "ui",
                },
                run_id=run_id,
            )
            return override

        if response_text:
            action = detect_confirmation_command(response_text)
            if action:
                self._set_state(action, run_id)
                self.event_bus.emit(
                    "confirmation.response",
                    {
                        "text": response_text,
                        "action": action.value,
                    },
                    run_id=run_id,
                )
                return action

        # 4. No valid response - ask once more
        await self._speak("Ich habe dich nicht verstanden. Abschicken oder verändern?")
        response_text, override = await self._wait_for_response(self.timeout)

        if override:
            self._set_state(override, run_id)
            self.event_bus.emit(
                "confirmation.response",
                {
                    "action": override.value,
                    "source": "ui",
                },
                run_id=run_id,
            )
            return override

        if response_text:
            action = detect_confirmation_command(response_text)
            if action:
                self._set_state(action, run_id)
                self.event_bus.emit(
                    "confirmation.response",
                    {
                        "text": response_text,
                        "action": action.value,
                    },
                    run_id=run_id,
                )
                return action

        # 5. Timeout -> cancel
        self._set_state(ConfirmationState.CANCEL, run_id)
        self.event_bus.emit(
            "confirmation.response",
            {
                "action": "cancel",
                "reason": "timeout",
            },
            run_id=run_id,
        )
        await self._speak("Okay, abgebrochen.")
        return ConfirmationState.CANCEL

    async def _speak(self, text: str) -> None:
        """Speak text (handles both sync and async tts)."""
        result = self.tts_speak(text)
        if asyncio.iscoroutine(result):
            await result

    async def _wait_for_response(
        self, timeout: float
    ) -> tuple[Optional[str], Optional[ConfirmationState]]:
        """Wait for either STT response or UI override."""
        listen_task = asyncio.create_task(asyncio.to_thread(self.stt_listen))
        start = asyncio.get_running_loop().time()
        try:
            while True:
                if listen_task.done():
                    result = listen_task.result()
                    return result, None

                try:
                    override = self._override_queue.get_nowait()
                    return None, override
                except queue.Empty:
                    pass

                if asyncio.get_running_loop().time() - start >= timeout:
                    return None, None

                await asyncio.sleep(0.1)
        except Exception as e:
            print(f"[Confirmation] Listen error: {e}")
            return None, None
        finally:
            if not listen_task.done():
                listen_task.cancel()

    def reset(self) -> None:
        self.state = ConfirmationState.IDLE

    def set_override(self, action: ConfirmationState) -> None:
        """Override confirmation via UI."""
        try:
            self._override_queue.put(action, block=False)
        except Exception:
            pass
