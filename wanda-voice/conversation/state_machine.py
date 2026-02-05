# Wanda Voice Assistant - State Machine
"""Mode switching: Aktiv, Paused, CLI-Proxy, Autonomous."""

from enum import Enum, auto
import re
from typing import Optional, Callable
import time


class WandaMode(Enum):
    """Wanda operating modes."""

    AKTIV = auto()  # Normal operation, user at keyboard
    PAUSED = auto()  # Sleeping, waiting for wake command
    CLI_PROXY = auto()  # Proxying to CLI tool
    AUTONOMOUS = auto()  # Full autonomous mode


class StateMachine:
    """
    Manages Wanda's operating mode with smart transitions.
    """

    PAUSE_COMMANDS = [
        "pause",
        "wanda stopp",
        "wanda pause",
        "pausiere dich",
        "stopp",
        "schlaf",
        "wanda schlaf",
        "gute nacht",
        "gute nacht wanda",
        "tschau",
        "tschau wanda",
        "bis später",
        "bis später wanda",
    ]

    RESUME_COMMANDS = [
        "wanda weiter",
        "fortfahren",
        "aufwachen",
        "hallo wanda",
        "wanda fortfahren",
        "weiter",
        "wach auf",
        "wanda start",
        "wandastart",
        "wunderstart",
        "wanderstart",
        "guten morgen",
        "guten morgen wanda",
        "bist du da",
        "bist du wach",
    ]

    AUTONOMOUS_TRIGGERS = [
        "vollautonom",
        "vollautomatisch",
        "wanda mode",
        "los wanda",
        "autonom",
        "übernimm",
        "mach alles",
    ]

    def __init__(self, on_mode_change: Optional[Callable] = None):
        self.mode = WandaMode.AKTIV
        self.previous_mode = None
        self.pause_time: Optional[float] = None
        self.on_mode_change = on_mode_change

        # Context tracking
        self.last_context: Optional[str] = None
        self.session_start = time.time()

    def detect_mode_command(self, text: str) -> Optional[WandaMode]:
        """Detect mode change command in text."""
        text_lower = self._normalize(text)

        # Check pause
        for cmd in self.PAUSE_COMMANDS:
            if cmd in text_lower or text_lower == cmd:
                return WandaMode.PAUSED

        # Check resume (only if paused)
        if self.mode == WandaMode.PAUSED:
            for cmd in self.RESUME_COMMANDS:
                if cmd in text_lower or text_lower == cmd:
                    return WandaMode.AKTIV

        # Check autonomous
        for cmd in self.AUTONOMOUS_TRIGGERS:
            if cmd in text_lower:
                return WandaMode.AUTONOMOUS

        return None

    def _normalize(self, text: str) -> str:
        text = text.lower().strip()
        text = text.replace("wunder", "wanda")
        text = text.replace("wander", "wanda")
        text = text.replace("wonder", "wanda")
        text = text.replace("wonda", "wanda")
        text = re.sub(r"[^a-z0-9äöüß\s]", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def transition(self, new_mode: WandaMode) -> str:
        """Transition to new mode, return announcement."""
        self.previous_mode = self.mode
        self.mode = new_mode

        if self.on_mode_change:
            self.on_mode_change(self.previous_mode, new_mode)

        if new_mode == WandaMode.PAUSED:
            self.pause_time = time.time()
            return "Verstanden. Ich pausiere mich. Sag 'Hallo Wanda' wenn du mich brauchst."

        elif new_mode == WandaMode.AKTIV:
            pause_duration = self._get_pause_duration()
            self.pause_time = None
            if pause_duration:
                return f"Hallo Jannis! Ich war {pause_duration} pausiert. Wo machen wir weiter?"
            return "Ich bin wieder da. Wie kann ich helfen?"

        elif new_mode == WandaMode.AUTONOMOUS:
            return "Vollautonom-Modus aktiviert. Ich übernehme. Sag 'Stopp' um abzubrechen."

        elif new_mode == WandaMode.CLI_PROXY:
            return "CLI-Proxy aktiv. Ich leite deine Sprache an das aktive Tool weiter."

        return ""

    def _get_pause_duration(self) -> Optional[str]:
        """Get human-readable pause duration."""
        if not self.pause_time:
            return None

        duration = time.time() - self.pause_time
        if duration < 60:
            return f"{int(duration)} Sekunden"
        elif duration < 3600:
            return f"{int(duration / 60)} Minuten"
        else:
            return f"{int(duration / 3600)} Stunden"

    def is_active(self) -> bool:
        return self.mode == WandaMode.AKTIV

    def is_paused(self) -> bool:
        return self.mode == WandaMode.PAUSED

    def is_autonomous(self) -> bool:
        return self.mode == WandaMode.AUTONOMOUS

    def is_cli_proxy(self) -> bool:
        return self.mode == WandaMode.CLI_PROXY

    def set_context(self, context: str):
        """Store context for resume."""
        self.last_context = context

    def get_resume_context(self) -> Optional[str]:
        """Get context for resume announcement."""
        return self.last_context


if __name__ == "__main__":
    sm = StateMachine()

    tests = [
        "Wanda Pause",
        "Hallo Wanda",
        "Vollautonom",
        "normaler text",
    ]

    for text in tests:
        cmd = sm.detect_mode_command(text)
        print(f"'{text}' -> {cmd}")
