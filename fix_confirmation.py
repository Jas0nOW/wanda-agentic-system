"""Quick fix for confirmation timeout issue.

The problem: When refiner is disabled, confirmation runs but doesn't
properly detect "abschicken" command.

This patch ensures confirmation works correctly.
"""

import sys
from pathlib import Path

# Read the current engine.py
engine_path = Path(__file__).parent.parent / "wanda_voice_core" / "engine.py"
content = engine_path.read_text()

# The issue is that when refiner is disabled, the confirmation runs
# but the SEND action doesn't properly continue to send the message.
# Let's fix the logic:

old_code = """            elif not self.refiner_enabled and confirmation_enabled:
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

                # Run confirmation flow
                action = await self._confirmation.run(refiner_result, run_id=run_id)
                result.confirmation_action = action

                # Handle confirmation result
                if action == ConfirmationState.SEND:
                    # User confirmed - continue to send
                    pass  # Continue with sending
                elif action == ConfirmationState.CANCEL:
                    # User cancelled - return early
                    return result
                elif action == ConfirmationState.REDO:
                    # User wants to redo - return early
                    return result
                elif action == ConfirmationState.EDIT:
                    # User wants to edit - return early
                    return result"""

new_code = """            elif not self.refiner_enabled and confirmation_enabled:
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

                # Run confirmation flow
                action = await self._confirmation.run(refiner_result, run_id=run_id)
                result.confirmation_action = action

                # Handle confirmation result - only SEND continues, all others return
                if action == ConfirmationState.SEND:
                    # User confirmed - continue to send (fall through to sending code)
                    pass
                else:
                    # CANCEL, REDO, or EDIT - return early without sending
                    return result"""

if old_code in content:
    content = content.replace(old_code, new_code)
    engine_path.write_text(content)
    print("✅ Fixed engine.py confirmation logic")
else:
    print(
        "⚠️  Could not find the code to patch - may already be patched or different version"
    )
    print("Checking current state...")
    if "elif not self.refiner_enabled and confirmation_enabled:" in content:
        print("✓ Found the refiner disabled block")
    else:
        print("✗ Could not find refiner disabled block")
