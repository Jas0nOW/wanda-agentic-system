# Wanda Voice Assistant - Daily Initializer
"""Daily start routine: Greeting, Briefing, OpenCode, Goals."""

import subprocess
import time
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Callable, Dict, Any

try:
    from conversation.briefing import BriefingGenerator
    from adapters.ollama_adapter import OllamaAdapter
except ImportError:
    BriefingGenerator = None
    OllamaAdapter = None


class DailyInitializer:
    """
    Wanda's Daily Start Routine:
    1. Personalized greeting
    2. Session briefing
    3. Open OpenCode in terminal
    4. Ask about today's goals
    """
    
    GREETINGS = {
        "morning": [
            "Guten Morgen Jannis! Bereit für einen produktiven Tag?",
            "Morgen! Kaffee schon fertig? Zeit zum Coden.",
            "Hey! Lass uns was Großartiges bauen heute.",
        ],
        "afternoon": [
            "Hey Jannis! Wie läuft der Tag?",
            "Nachmittags-Session! Was steht an?",
            "Back to work! Was bauen wir?",
        ],
        "evening": [
            "Abend-Coding-Session! Was geht?",
            "Hey! Noch motiviert? Let's build.",
            "Abendmodus aktiviert. Was machen wir?",
        ],
        "night": [
            "Late night coding! Was treibt dich um?",
            "Noch wach? Lass uns was hacken.",
            "Nacht-Session! Was ist der Plan?",
        ]
    }
    
    def __init__(
        self, 
        briefing: Optional['BriefingGenerator'] = None,
        ollama: Optional['OllamaAdapter'] = None,
        speak_callback: Optional[Callable[[str], None]] = None,
        orb_callback: Optional[Callable[[str], None]] = None
    ):
        self.briefing = briefing or (BriefingGenerator() if BriefingGenerator else None)
        self.ollama = ollama
        self.speak = speak_callback or print
        self.set_orb_state = orb_callback or (lambda x: None)
        
        self.initialized_today = False
        self.last_init_date: Optional[str] = None
    
    def run_daily_start(self) -> str:
        """Execute full daily start routine."""
        self.set_orb_state("speaking")
        
        parts = []
        
        # 1. Personalized greeting
        greeting = self._get_greeting()
        parts.append(greeting)
        self.speak(greeting)
        time.sleep(0.5)
        
        # 2. Briefing
        if self.briefing:
            briefing_text = self.briefing.generate()
            parts.append(briefing_text)
            self.speak(briefing_text)
            time.sleep(0.5)
        
        # 3. Open OpenCode
        self._open_opencode()
        parts.append("OpenCode ist bereit.")
        self.speak("OpenCode ist bereit.")
        time.sleep(0.3)
        
        # 4. Ask for goals
        goal_prompt = self._get_goal_prompt()
        parts.append(goal_prompt)
        self.speak(goal_prompt)
        
        self.set_orb_state("listening")
        
        # Track initialization
        self.initialized_today = True
        self.last_init_date = datetime.now().strftime("%Y-%m-%d")
        
        return " ".join(parts)
    
    def _get_greeting(self) -> str:
        """Get time-appropriate greeting."""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            period = "morning"
        elif 12 <= hour < 17:
            period = "afternoon"
        elif 17 <= hour < 22:
            period = "evening"
        else:
            period = "night"
        
        import random
        greetings = self.GREETINGS[period]
        return random.choice(greetings)
    
    def _get_goal_prompt(self) -> str:
        """Get goal-asking prompt."""
        prompts = [
            "Was wollen wir heute Cooles bauen?",
            "Was steht auf deiner Agenda?",
            "Welches Projekt tacklen wir heute?",
            "Was ist der Plan für heute?",
        ]
        import random
        return random.choice(prompts)
    
    def _open_opencode(self) -> bool:
        """Open OpenCode in a new terminal."""
        try:
            # Try various terminal emulators
            terminals = [
                ["gnome-terminal", "--", "opencode"],
                ["konsole", "-e", "opencode"],
                ["xfce4-terminal", "-e", "opencode"],
                ["alacritty", "-e", "opencode"],
                ["kitty", "opencode"],
                ["xterm", "-e", "opencode"],
            ]
            
            for cmd in terminals:
                try:
                    result = subprocess.run(
                        ["which", cmd[0]], 
                        capture_output=True, 
                        timeout=1
                    )
                    if result.returncode == 0:
                        # Found terminal, launch opencode
                        subprocess.Popen(
                            cmd,
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            start_new_session=True
                        )
                        print(f"[Daily] Opened OpenCode with {cmd[0]}")
                        return True
                except:
                    continue
            
            # Fallback: try opening in background
            subprocess.Popen(
                ["opencode"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            print("[Daily] Opened OpenCode (background)")
            return True
            
        except Exception as e:
            print(f"[Daily] Could not open OpenCode: {e}")
            return False
    
    def is_first_session_today(self) -> bool:
        """Check if this is the first session today."""
        today = datetime.now().strftime("%Y-%m-%d")
        return self.last_init_date != today
    
    def get_quick_greeting(self) -> str:
        """Get a quick greeting for subsequent orb clicks."""
        return "Ich höre. Was brauchst du?"


if __name__ == "__main__":
    init = DailyInitializer(speak_callback=print)
    init.run_daily_start()
