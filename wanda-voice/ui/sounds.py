# Wanda Voice Assistant - UI Sounds
"""Subtle audio feedback for JARVIS feel."""

import subprocess
from pathlib import Path
from typing import Optional


class SoundFeedback:
    """Subtle UI sounds for feedback."""
    
    # System sound paths
    SOUND_DIRS = [
        Path("/usr/share/sounds/freedesktop/stereo"),
        Path("/usr/share/sounds/gnome/default/audio"),
        Path("/usr/share/sounds/kde/runtime"),
    ]
    
    SOUND_MAP = {
        "pulse": ["message.oga", "message-new-instant.oga", "bell.oga"],
        "trigger": ["complete.oga", "button-toggle-on.oga", "device-added.oga"],
        "success": ["bell.oga", "complete.oga", "dialog-information.oga"],
        "error": ["dialog-error.oga", "dialog-warning.oga"],
        "cancel": ["dialog-cancel.oga", "message.oga"],
    }
    
    def __init__(self, enabled: bool = True):
        self.enabled = enabled
        self.player = self._detect_player()
    
    def _detect_player(self) -> Optional[str]:
        """Detect available audio player."""
        for player in ["paplay", "aplay", "mpv", "ffplay"]:
            try:
                subprocess.run(["which", player], capture_output=True)
                return player
            except:
                pass
        return None
    
    def _find_sound(self, sound_type: str) -> Optional[Path]:
        """Find sound file for type."""
        candidates = self.SOUND_MAP.get(sound_type, [])
        
        for sound_dir in self.SOUND_DIRS:
            if not sound_dir.exists():
                continue
            for candidate in candidates:
                path = sound_dir / candidate
                if path.exists():
                    return path
        
        return None
    
    def play(self, sound_type: str):
        """Play feedback sound."""
        if not self.enabled or not self.player:
            return
        
        sound_file = self._find_sound(sound_type)
        if not sound_file:
            return
        
        try:
            subprocess.Popen(
                [self.player, str(sound_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except:
            pass
    
    def pulse(self):
        """Subtle pulse when recording starts."""
        self.play("pulse")
    
    def trigger(self):
        """Sound when hotkey triggered."""
        self.play("trigger")
    
    def success(self):
        """Success sound."""
        self.play("success")
    
    def error(self):
        """Error sound."""
        self.play("error")
    
    def cancel(self):
        """Cancel sound."""
        self.play("cancel")


if __name__ == "__main__":
    sounds = SoundFeedback()
    print(f"Player: {sounds.player}")
    sounds.trigger()
