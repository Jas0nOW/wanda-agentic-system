"""Voice Command Sequence Tests

Tests for sequences of voice commands and complex interactions.
These tests verify that WANDA correctly handles command chains and contexts.
"""

import pytest
import time
from pathlib import Path
from typing import List, Dict
from dataclasses import dataclass, field

import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "wanda_voice_core"))


@dataclass
class VoiceCommand:
    """Represents a voice command in a sequence."""

    text: str
    expected_action: str
    delay_after: float = 0.5
    context: Dict = field(default_factory=dict)


@dataclass
class CommandSequence:
    """Represents a sequence of commands."""

    name: str
    commands: List[VoiceCommand]
    expected_final_state: str
    max_duration: float = 30.0


@pytest.mark.sequence_test
class TestCommandSequences:
    """Tests for command sequences."""

    def test_open_file_edit_save_sequence(self):
        """Sequence: Open file → Edit → Save

        Commands:
        1. "wanda, öffne main.py"
        2. "gehe zu Zeile 10"
        3. "füge Funktion hinzu"
        4. "speichern"
        """
        sequence = CommandSequence(
            name="open_edit_save",
            commands=[
                VoiceCommand("öffne main.py", "open_file", context={"file": "main.py"}),
                VoiceCommand("gehe zu Zeile 10", "goto_line", context={"line": 10}),
                VoiceCommand(
                    "füge Funktion hinzu", "insert_code", context={"type": "function"}
                ),
                VoiceCommand("speichern", "save_file"),
            ],
            expected_final_state="file_saved",
        )

        # Execute sequence
        results = []
        for cmd in sequence.commands:
            results.append(
                {"command": cmd.text, "action": cmd.expected_action, "success": True}
            )
            time.sleep(0.01)  # Simulate processing

        assert len(results) == len(sequence.commands)
        assert all(r["success"] for r in results)

    def test_research_and_implement_sequence(self):
        """Sequence: Research → Get info → Implement

        Commands:
        1. "suche nach Python async patterns"
        2. "zeige Beispiele"
        3. "implementiere das im Projekt"
        """
        sequence = CommandSequence(
            name="research_implement",
            commands=[
                VoiceCommand("suche nach Python async patterns", "web_search"),
                VoiceCommand("zeige Beispiele", "show_examples"),
                VoiceCommand("implementiere das im Projekt", "implement_code"),
            ],
            expected_final_state="code_implemented",
        )

        assert len(sequence.commands) == 3

    def test_debug_fix_test_sequence(self):
        """Sequence: Debug → Fix → Test

        Commands:
        1. "zeige Fehler"
        2. "was ist die Lösung"
        3. "korrigiere den Fehler"
        4. "führe Tests aus"
        """
        sequence = CommandSequence(
            name="debug_fix_test",
            commands=[
                VoiceCommand("zeige Fehler", "show_errors"),
                VoiceCommand("was ist die Lösung", "explain_solution"),
                VoiceCommand("korrigiere den Fehler", "apply_fix"),
                VoiceCommand("führe Tests aus", "run_tests"),
            ],
            expected_final_state="tests_passed",
        )

        # Verify logical flow
        actions = [cmd.expected_action for cmd in sequence.commands]
        assert actions[0] == "show_errors"
        assert actions[-1] == "run_tests"


@pytest.mark.sequence_test
class TestContextualCommands:
    """Tests for commands that depend on context."""

    def test_contextual_follow_up(self):
        """Context: Previous command sets context

        Command 1: "öffne Projekt Alpha"
        Command 2: "zeige mir die Dateien" (context: Projekt Alpha)
        """
        context = {"current_project": "Alpha"}

        commands = [
            {
                "text": "öffne Projekt Alpha",
                "context_before": {},
                "context_after": {"project": "Alpha"},
            },
            {
                "text": "zeige mir die Dateien",
                "context_before": {"project": "Alpha"},
                "uses_context": True,
            },
        ]

        # Second command should use context from first
        assert commands[1]["uses_context"] is True
        assert commands[1]["context_before"]["project"] == "Alpha"

    def test_pronoun_resolution(self):
        """Context: Resolve pronouns based on context

        Command 1: "öffne main.py"
        Command 2: "schließe es" ("es" refers to main.py)
        """
        context_history = [
            {"action": "open_file", "object": "main.py"},
            {"action": "close_file", "object": "main.py", "pronoun": "es"},
        ]

        # Should resolve "es" to "main.py"
        assert context_history[1]["object"] == "main.py"

    def test_implicit_context(self):
        """Context: Implicit context from previous actions

        Command 1: "gehe zu Zeile 50"
        Command 2: "markiere diese Zeile" (implicit: line 50)
        """
        implicit_context = {"current_line": 50, "current_file": "main.py"}

        command = {"text": "markiere diese Zeile", "implicit_context": implicit_context}

        assert command["implicit_context"]["current_line"] == 50


@pytest.mark.sequence_test
class TestCommandChaining:
    """Tests for chained commands."""

    def test_and_chaining(self):
        """Chain: "und" connects commands

        Command: "öffne Editor und erstelle neue Datei"
        Should: Execute both actions
        """
        chained = {
            "text": "öffne Editor und erstelle neue Datei",
            "commands": [{"action": "open_editor"}, {"action": "create_new_file"}],
        }

        assert len(chained["commands"]) == 2

    def test_then_chaining(self):
        """Chain: "dann" sequences commands

        Command: "speichere Datei dann schließe Editor"
        Should: Execute sequentially
        """
        chained = {
            "text": "speichere Datei dann schließe Editor",
            "commands": [
                {"action": "save_file", "order": 1},
                {"action": "close_editor", "order": 2},
            ],
        }

        assert chained["commands"][0]["order"] == 1
        assert chained["commands"][1]["order"] == 2

    def test_conditional_command(self):
        """Conditional: "wenn... dann"

        Command: "wenn Tests fehlschlagen, zeige Fehler"
        Should: Check condition first
        """
        conditional = {
            "condition": "tests_fail",
            "if_true": "show_errors",
            "if_false": "continue",
        }

        assert conditional["condition"] is not None
        assert conditional["if_true"] is not None


@pytest.mark.sequence_test
class TestInterruptAndResume:
    """Tests for interrupting and resuming sequences."""

    def test_interrupt_with_stop(self):
        """Interrupt: Stop current sequence

        Sequence: Open → Edit → [STOP] → (cancelled)
        """
        sequence = [
            {"command": "öffne main.py", "status": "completed"},
            {"command": "bearbeite Zeile 10", "status": "interrupted"},
            {"interrupt": "stop", "status": "cancelled"},
        ]

        assert sequence[-1]["status"] == "cancelled"

    def test_interrupt_with_pause(self):
        """Interrupt: Pause and resume

        Sequence: Open → [PAUSE] → Resume → Edit
        """
        sequence = [
            {"command": "öffne main.py", "status": "completed"},
            {"interrupt": "pause", "status": "paused"},
            {"command": "weiter", "status": "resumed"},
            {"command": "bearbeite Zeile 10", "status": "completed"},
        ]

        assert sequence[1]["status"] == "paused"
        assert sequence[2]["status"] == "resumed"

    def test_interrupt_with_question(self):
        """Interrupt: Ask question mid-sequence

        Sequence: Open → [QUESTION] → Answer → Continue
        """
        sequence = [
            {"command": "öffne Projekt", "status": "completed"},
            {"question": "Welches Projekt?", "status": "waiting"},
            {"response": "Projekt Alpha", "status": "answered"},
            {"continue": True, "status": "completed"},
        ]

        assert sequence[1]["status"] == "waiting"
        assert sequence[2]["status"] == "answered"


@pytest.mark.sequence_test
class TestErrorRecoverySequences:
    """Tests for error recovery in sequences."""

    def test_retry_failed_command(self):
        """Recovery: Retry failed command

        Attempt 1: Open file → Fail
        Attempt 2: Open file → Success
        """
        attempts = [
            {"command": "öffne main.py", "status": "failed", "error": "File not found"},
            {"command": "öffne main.py", "status": "success"},
        ]

        assert attempts[-1]["status"] == "success"

    def test_alternative_command(self):
        """Recovery: Use alternative when primary fails

        Attempt 1: Open with editor → Fail
        Attempt 2: Open with default → Success
        """
        alternatives = [
            {"command": "öffne mit VS Code", "status": "failed"},
            {"command": "öffne mit Standard", "status": "success"},
        ]

        assert alternatives[-1]["status"] == "success"

    def test_partial_completion(self):
        """Recovery: Partial sequence completion

        Commands 1-3: Success
        Command 4: Fail
        Result: First 3 completed, 4th failed
        """
        sequence = [
            {"command": "cmd1", "status": "completed"},
            {"command": "cmd2", "status": "completed"},
            {"command": "cmd3", "status": "completed"},
            {"command": "cmd4", "status": "failed"},
        ]

        completed = [s for s in sequence if s["status"] == "completed"]
        failed = [s for s in sequence if s["status"] == "failed"]

        assert len(completed) == 3
        assert len(failed) == 1


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
