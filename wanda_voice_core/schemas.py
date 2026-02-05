"""Strict dataclass schemas for WANDA Voice Core."""

from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Optional
import time


class RouteType(str, Enum):
    COMMAND = "command"
    REFINE = "refine"
    LLM = "llm"


class RefinerAction(str, Enum):
    SEND = "send"
    ASK = "ask"
    EDIT = "edit"


class RiskLevel(str, Enum):
    SAFE = "safe"  # 0-2
    CAUTION = "caution"  # 3-5
    DANGEROUS = "dangerous"  # 6-8
    BLOCKED = "blocked"  # 9-10


class ConfirmationState(str, Enum):
    IDLE = "idle"
    RECORDING = "recording"
    TRANSCRIBING = "transcribing"
    REFINING = "refining"
    READBACK = "readback"
    AWAITING_RESPONSE = "awaiting_response"
    SEND = "send"
    EDIT = "edit"
    REDO = "redo"
    CANCEL = "cancel"


class ValidationError(Exception):
    pass


@dataclass
class RouterResult:
    route: RouteType
    confidence: float
    command: Optional[dict[str, Any]] = None
    notes: str = ""

    def validate(self) -> RouterResult:
        if not isinstance(self.route, RouteType):
            raise ValidationError(f"Invalid route: {self.route}")
        if not (0.0 <= self.confidence <= 1.0):
            raise ValidationError(f"Confidence must be 0..1, got {self.confidence}")
        return self


@dataclass
class RefinerResult:
    intent: str
    improved_text: str
    do: RefinerAction
    questions: list[str] = field(default_factory=list)
    token_budget: dict[str, int] = field(
        default_factory=lambda: {"max_output_tokens": 2048}
    )

    def validate(self) -> RefinerResult:
        if not self.intent:
            raise ValidationError("intent must not be empty")
        if not self.improved_text:
            raise ValidationError("improved_text must not be empty")
        if not isinstance(self.do, RefinerAction):
            raise ValidationError(f"Invalid action: {self.do}")
        return self


@dataclass
class UtteranceRequest:
    text: str
    mode: str = "text"  # "text" or "voice"
    context: Optional[str] = None

    def validate(self) -> UtteranceRequest:
        if not self.text or not self.text.strip():
            raise ValidationError("text must not be empty")
        if self.mode not in ("text", "voice"):
            raise ValidationError(f"Invalid mode: {self.mode}")
        return self


@dataclass
class UtteranceResponse:
    final_text: str
    response_text: str
    actions: list[str] = field(default_factory=list)
    events_summary: list[str] = field(default_factory=list)
    run_id: Optional[str] = None


@dataclass
class RunEvent:
    event_type: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    run_id: Optional[str] = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "event_type": self.event_type,
            "data": self.data,
            "timestamp": self.timestamp,
            "run_id": self.run_id,
        }


@dataclass
class EngineResult:
    """Result of a full engine pipeline run."""

    transcript: str = ""
    improved_text: str = ""
    response_text: str = ""
    route: Optional[RouteType] = None
    confirmation_action: Optional[ConfirmationState] = None
    run_id: Optional[str] = None
    error: Optional[str] = None
    metrics: dict[str, Any] = field(default_factory=dict)


@dataclass
class TokenMetrics:
    """Unified token metrics - Single Source of Truth.

    This class is the ONLY definition of TokenMetrics in the codebase.
    All other modules must import from here.
    """

    chars_in: int = 0
    chars_out: int = 0
    token_est_in: int = 0
    token_est_out: int = 0
    latency_ms: float = 0.0

    def update(self, text_in: str, text_out: str, latency_ms: float = 0.0) -> None:
        """Update metrics from input/output text."""
        from wanda_voice_core.token_economy import estimate_tokens

        self.chars_in = len(text_in)
        self.chars_out = len(text_out)
        self.token_est_in = estimate_tokens(text_in)
        self.token_est_out = estimate_tokens(text_out)
        self.latency_ms = latency_ms

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "chars_in": self.chars_in,
            "chars_out": self.chars_out,
            "token_est_in": self.token_est_in,
            "token_est_out": self.token_est_out,
            "latency_ms": self.latency_ms,
        }
