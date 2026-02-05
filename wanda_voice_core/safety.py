"""Safety policy for WANDA Voice Core."""

from __future__ import annotations
import re
from dataclasses import dataclass
from typing import Optional

from wanda_voice_core.schemas import RiskLevel


@dataclass
class SafetyResult:
    risk_level: RiskLevel
    risk_score: int  # 0-10
    message: str = ""
    requires_voice_confirm: bool = False
    requires_gui_confirm: bool = False


# Zero-tolerance patterns (score 10)
DENYLIST = [
    re.compile(r"rm\s+-rf\s+/(?:\s|$|\*)", re.IGNORECASE),
    re.compile(r"dd\s+if=/dev/zero\s+of=/dev/sd", re.IGNORECASE),
    re.compile(r"mkfs\.\w+\s+/dev/sd", re.IGNORECASE),
    re.compile(r"curl\s+.*\|\s*(?:bash|sh)", re.IGNORECASE),
    re.compile(r"wget\s+.*\|\s*(?:bash|sh)", re.IGNORECASE),
    re.compile(r"nc\s+-e\s+/bin/(?:ba)?sh", re.IGNORECASE),
    re.compile(r"cat\s+~?/.ssh/id_rsa", re.IGNORECASE),
    re.compile(r"cat\s+/etc/shadow", re.IGNORECASE),
    re.compile(r"chmod\s+777\s+/", re.IGNORECASE),
    re.compile(r":\(\)\{\s*:\|:\s*&\s*\};:", re.IGNORECASE),  # fork bomb
]

# Dangerous patterns (score 7-8)
DANGEROUS_LIST = [
    (re.compile(r"rm\s+-rf?\s+", re.IGNORECASE), 7),
    (re.compile(r"find\s+.*-delete", re.IGNORECASE), 7),
    (re.compile(r"git\s+push\s+--force", re.IGNORECASE), 8),
    (re.compile(r"git\s+reset\s+--hard", re.IGNORECASE), 7),
    (re.compile(r"git\s+clean\s+-fdx", re.IGNORECASE), 7),
    (re.compile(r"docker\s+system\s+prune\s+-a", re.IGNORECASE), 7),
]

# Caution patterns (score 3-5)
CAUTION_LIST = [
    (re.compile(r"sudo\s+", re.IGNORECASE), 5),
    (re.compile(r"shutdown", re.IGNORECASE), 5),
    (re.compile(r"reboot", re.IGNORECASE), 5),
    (re.compile(r"systemctl\s+(?:stop|restart)", re.IGNORECASE), 4),
    (re.compile(r"npm\s+publish", re.IGNORECASE), 4),
    (re.compile(r"pip\s+install\s+--user", re.IGNORECASE), 3),
    (re.compile(r"git\s+push(?:\s|$)", re.IGNORECASE), 3),
]

# Safe patterns (score 0)
ALLOWLIST = [
    re.compile(r"^(?:ls|cat|head|tail|grep|tree|pwd)(?:\s|$)", re.IGNORECASE),
    re.compile(r"^git\s+(?:status|log|diff|branch)(?:\s|$)", re.IGNORECASE),
    re.compile(r"^npm\s+(?:install|run|test)(?:\s|$)", re.IGNORECASE),
    re.compile(r"^python\s+-m\s+pytest", re.IGNORECASE),
    re.compile(r"^(?:eslint|prettier|black|mypy)(?:\s|$)", re.IGNORECASE),
]

# Prompt injection defense patterns
INJECTION_PATTERNS = [
    re.compile(r"ignore\s+(?:all\s+)?previous\s+instructions", re.IGNORECASE),
    re.compile(r"you\s+are\s+now\s+", re.IGNORECASE),
    re.compile(r"system\s*prompt\s*:", re.IGNORECASE),
    re.compile(r"<\s*/?system\s*>", re.IGNORECASE),
]


class SafetyPolicy:
    """Validates commands and text against security policies."""

    def __init__(self, command_execution: bool = False,
                 risk_threshold_voice: int = 3,
                 risk_threshold_gui: int = 6):
        self.command_execution = command_execution
        self.risk_threshold_voice = risk_threshold_voice
        self.risk_threshold_gui = risk_threshold_gui

    def check_command(self, command: str) -> SafetyResult:
        """Check a shell command against security policies."""
        command = command.strip()

        # Denylist: always blocked
        for pattern in DENYLIST:
            if pattern.search(command):
                return SafetyResult(
                    risk_level=RiskLevel.BLOCKED,
                    risk_score=10,
                    message=f"BLOCKED: Matches denylist pattern",
                )

        # Dangerous
        for pattern, score in DANGEROUS_LIST:
            if pattern.search(command):
                return SafetyResult(
                    risk_level=RiskLevel.DANGEROUS,
                    risk_score=score,
                    message=f"DANGEROUS: {command[:50]}",
                    requires_voice_confirm=True,
                    requires_gui_confirm=True,
                )

        # Caution
        for pattern, score in CAUTION_LIST:
            if pattern.search(command):
                return SafetyResult(
                    risk_level=RiskLevel.CAUTION,
                    risk_score=score,
                    message=f"Requires confirmation: {command[:50]}",
                    requires_voice_confirm=score >= self.risk_threshold_voice,
                    requires_gui_confirm=score >= self.risk_threshold_gui,
                )

        # Allowlist
        for pattern in ALLOWLIST:
            if pattern.search(command):
                return SafetyResult(
                    risk_level=RiskLevel.SAFE,
                    risk_score=0,
                )

        # Unknown: treat as caution
        return SafetyResult(
            risk_level=RiskLevel.CAUTION,
            risk_score=4,
            message=f"Unknown command, confirmation required",
            requires_voice_confirm=True,
        )

    def check_text(self, text: str) -> SafetyResult:
        """Check text for injection attempts."""
        for pattern in INJECTION_PATTERNS:
            if pattern.search(text):
                return SafetyResult(
                    risk_level=RiskLevel.BLOCKED,
                    risk_score=9,
                    message="Potential prompt injection detected",
                )
        return SafetyResult(risk_level=RiskLevel.SAFE, risk_score=0)

    def is_safe_for_voice(self, result: SafetyResult) -> bool:
        """Check if action can proceed without voice confirmation."""
        return result.risk_score < self.risk_threshold_voice

    def is_safe_for_auto(self, result: SafetyResult) -> bool:
        """Check if action can proceed without any confirmation."""
        return result.risk_level == RiskLevel.SAFE
