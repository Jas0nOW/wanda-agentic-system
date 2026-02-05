"""Tests for Router/Refiner schema validation."""

import pytest
from wanda_voice_core.schemas import (
    RouterResult, RefinerResult, UtteranceRequest,
    RouteType, RefinerAction, ValidationError,
)


class TestRouterResult:
    def test_valid_result(self):
        r = RouterResult(route=RouteType.LLM, confidence=0.8)
        assert r.validate() is r

    def test_valid_command_result(self):
        r = RouterResult(
            route=RouteType.COMMAND,
            confidence=0.95,
            command={"name": "send"},
        )
        assert r.validate().route == RouteType.COMMAND

    def test_invalid_confidence_too_high(self):
        r = RouterResult(route=RouteType.LLM, confidence=1.5)
        with pytest.raises(ValidationError):
            r.validate()

    def test_invalid_confidence_negative(self):
        r = RouterResult(route=RouteType.LLM, confidence=-0.1)
        with pytest.raises(ValidationError):
            r.validate()

    def test_boundary_confidence(self):
        r0 = RouterResult(route=RouteType.LLM, confidence=0.0)
        r1 = RouterResult(route=RouteType.LLM, confidence=1.0)
        assert r0.validate()
        assert r1.validate()


class TestRefinerResult:
    def test_valid_result(self):
        r = RefinerResult(
            intent="summarize",
            improved_text="Verbessert",
            do=RefinerAction.SEND,
        )
        assert r.validate() is r

    def test_empty_intent_fails(self):
        r = RefinerResult(intent="", improved_text="text", do=RefinerAction.SEND)
        with pytest.raises(ValidationError):
            r.validate()

    def test_empty_text_fails(self):
        r = RefinerResult(intent="test", improved_text="", do=RefinerAction.SEND)
        with pytest.raises(ValidationError):
            r.validate()

    def test_questions_default_empty(self):
        r = RefinerResult(intent="test", improved_text="text", do=RefinerAction.ASK)
        assert r.questions == []

    def test_token_budget_default(self):
        r = RefinerResult(intent="test", improved_text="text", do=RefinerAction.SEND)
        assert r.token_budget["max_output_tokens"] == 2048


class TestUtteranceRequest:
    def test_valid_request(self):
        r = UtteranceRequest(text="Hallo Wanda")
        assert r.validate().text == "Hallo Wanda"

    def test_empty_text_fails(self):
        r = UtteranceRequest(text="")
        with pytest.raises(ValidationError):
            r.validate()

    def test_whitespace_text_fails(self):
        r = UtteranceRequest(text="   ")
        with pytest.raises(ValidationError):
            r.validate()

    def test_invalid_mode_fails(self):
        r = UtteranceRequest(text="Hello", mode="invalid")
        with pytest.raises(ValidationError):
            r.validate()

    def test_valid_modes(self):
        for mode in ("text", "voice"):
            r = UtteranceRequest(text="Test", mode=mode)
            assert r.validate()
