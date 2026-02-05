"""Thread-safe EventBus for WANDA Voice Core."""

from __future__ import annotations
import threading
import time
from collections import deque
from typing import Any, Callable

from wanda_voice_core.schemas import RunEvent

# Standard event types
EVENT_TYPES = {
    "recording.start",
    "recording.stop",
    "vad.speech",
    "vad.silence",
    "stt.result",
    "router.result",
    "refiner.result",
    "refiner.toggle",
    "refiner.skipped",
    "provider.request",
    "provider.response",
    "provider.error",
    "provider.timeout",
    "tts.start",
    "tts.stop",
    "tts.interrupt",
    "confirmation.ask",
    "confirmation.response",
    "safety.check",
    "safety.blocked",
    "run.start",
    "run.end",
    "metrics.update",
    "state.change",
    "error",
}


class EventBus:
    """Thread-safe publish/subscribe event bus with rolling log."""

    def __init__(self, max_history: int = 100):
        self._subscribers: dict[str, list[Callable]] = {}
        self._lock = threading.Lock()
        self._history: deque[RunEvent] = deque(maxlen=max_history)

    def subscribe(self, event_type: str, callback: Callable[[RunEvent], None]) -> None:
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        with self._lock:
            if event_type in self._subscribers:
                try:
                    self._subscribers[event_type].remove(callback)
                except ValueError:
                    pass

    def emit(
        self,
        event_type: str,
        data: dict[str, Any] | None = None,
        run_id: str | None = None,
    ) -> RunEvent:
        event = RunEvent(
            event_type=event_type,
            data=data or {},
            timestamp=time.time(),
            run_id=run_id,
        )
        with self._lock:
            self._history.append(event)
            callbacks = list(self._subscribers.get(event_type, []))
            # Also notify wildcard subscribers
            callbacks.extend(self._subscribers.get("*", []))

        for cb in callbacks:
            try:
                cb(event)
            except Exception as e:
                print(f"[EventBus] Error in callback for {event_type}: {e}")

        return event

    def get_recent_events(self, n: int = 10) -> list[RunEvent]:
        with self._lock:
            items = list(self._history)
        return items[-n:]

    def get_events_for_run(self, run_id: str) -> list[RunEvent]:
        with self._lock:
            return [e for e in self._history if e.run_id == run_id]

    def clear(self) -> None:
        with self._lock:
            self._history.clear()
            self._subscribers.clear()
