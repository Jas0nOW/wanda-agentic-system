# Wanda Voice Assistant - Confirm UI
"""Terminal-based confirmation dialog for transcripts."""

import sys
from typing import Tuple, Optional


class ConfirmUI:
    """Terminal UI for confirming/editing transcripts before sending."""
    
    def __init__(self):
        """Initialize confirm UI."""
        pass
    
    def show(self, transcript: str) -> Tuple[str, str]:
        """
        Show confirmation dialog.
        
        Args:
            transcript: The transcribed text
        
        Returns:
            Tuple of (action, text) where:
            - action: 'send', 'redo', or 'cancel'
            - text: edited text (if action='send'), or original transcript
        """
        print("\n" + "="*70)
        print("📝 TRANSKRIPT:")
        print(transcript)
        print("="*70)
        print("\n[ENTER] Senden | [e] Edit | [r] Redo | [c] Cancel")
        
        while True:
            try:
                choice = input(">>> ").strip().lower()
                
                if choice == "" or choice == "s":
                    # Send
                    return ("send", transcript)
                
                elif choice == "e":
                    # Edit mode
                    print("\n✏️  Edit Mode (enter new text, or leave empty to keep original):")
                    edited = input(">>> ").strip()
                    
                    if edited:
                        print(f"\n✅ Updated to: {edited}")
                        return ("send", edited)
                    else:
                        print("⚠️  Keeping original text")
                        return ("send", transcript)
                
                elif choice == "r":
                    # Redo recording
                    print("\n🔄 Redo recording...")
                    return ("redo", transcript)
                
                elif choice == "c":
                    # Cancel
                    print("\n❌ Cancelled")
                    return ("cancel", transcript)
                
                else:
                    print("⚠️  Invalid choice. Try again: [ENTER/e/r/c]")
            
            except KeyboardInterrupt:
                print("\n❌ Cancelled")
                return ("cancel", transcript)
            except EOFError:
                print("\n❌ Cancelled")
                return ("cancel", transcript)


# Test function
if __name__ == "__main__":
    print("Testing Confirm UI...")
    ui = ConfirmUI()
    
    test_transcript = "Hallo Gemini, wie geht's dir heute?"
    action, text = ui.show(test_transcript)
    
    print(f"\n✅ Result: action={action}, text={text}")
