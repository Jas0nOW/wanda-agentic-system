"""
Safety Checker Module - Command Validation
==========================================
Implements the allowlist/denylist/confirmlist from TERMINAL_POLICY.md.
"""

import re
from enum import Enum
from dataclasses import dataclass


class SafetyLevel(Enum):
    ALLOW = "allow"
    CONFIRM = "confirm"
    DENY = "deny"


@dataclass
class SafetyResult:
    level: SafetyLevel
    message: str | None = None


class SafetyChecker:
    """Validates shell commands against security policies."""

    # Commands that are NEVER allowed
    DENYLIST = [
        r"rm\s+-rf\s+/",
        r"rm\s+-rf\s+/\*",
        r"dd\s+if=/dev/zero\s+of=/dev/sda",
        r"mkfs\.ext4\s+/dev/sda",
        r"curl\s+.*\|\s*bash",
        r"wget\s+.*\|\s*sh",
        r"nc\s+-e\s+/bin/bash",
        r"cat\s+~/.ssh/id_rsa",
        r"cat\s+/etc/shadow",
    ]

    # Commands that require user confirmation
    CONFIRMLIST = [
        r"rm\s+-rf\s+",
        r"rm\s+-r\s+",
        r"find\s+.*-delete",
        r"git\s+push\s+--force",
        r"git\s+reset\s+--hard",
        r"git\s+clean\s+-fdx",
        r"sudo\s+",
        r"shutdown",
        r"reboot",
        r"systemctl\s+stop",
    ]

    # Commands that are safe for autonomous execution
    ALLOWLIST = [
        r"^(ls|cat|head|tail|grep|tree|pwd)(\s|$)",
        r"^git\s+(status|log|diff|branch)(\s|$)",
        r"^npm\s+(install|run|test)(\s|$)",
        r"^python\s+-m\s+pytest",
        r"^cargo\s+build",
        r"^go\s+build",
        r"^(eslint|prettier|black|mypy)(\s|$)",
    ]

    def check(self, command: str) -> SafetyResult:
        """
        Check a command against security policies.
        
        Args:
            command: The shell command to validate
            
        Returns:
            SafetyResult with level and optional message
        """
        command = command.strip()

        # Check DENYLIST first
        for pattern in self.DENYLIST:
            if re.search(pattern, command, re.IGNORECASE):
                return SafetyResult(
                    level=SafetyLevel.DENY,
                    message=f"BLOCKED: This command is on the denylist ({pattern})"
                )

        # Check CONFIRMLIST
        for pattern in self.CONFIRMLIST:
            if re.search(pattern, command, re.IGNORECASE):
                return SafetyResult(
                    level=SafetyLevel.CONFIRM,
                    message=f"This command requires confirmation: {command}"
                )

        # Check ALLOWLIST
        for pattern in self.ALLOWLIST:
            if re.search(pattern, command, re.IGNORECASE):
                return SafetyResult(level=SafetyLevel.ALLOW)

        # Default: require confirmation for unknown commands
        return SafetyResult(
            level=SafetyLevel.CONFIRM,
            message=f"Unknown command, please confirm: {command}"
        )
