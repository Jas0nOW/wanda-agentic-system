# Wanda Voice Assistant - Startup Briefing
"""Generate intelligent startup briefings."""

import os
import subprocess
import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class BriefingGenerator:
    """
    Generates startup briefings from:
    - Conversation history
    - Git status
    - Active projects
    - System state
    """
    
    def __init__(self, history_path: Optional[str] = None):
        self.history_path = Path(history_path) if history_path else Path.home() / ".wanda" / "context.json"
        self.ollama = None  # Set externally if available
    
    def generate(self) -> str:
        """Generate full briefing text."""
        data = self._gather_data()
        
        # Use Ollama if available
        if self.ollama and self.ollama.available:
            return self.ollama.generate_briefing(data)
        
        # Fallback: template-based
        return self._template_briefing(data)
    
    def _gather_data(self) -> Dict[str, Any]:
        """Gather data for briefing."""
        data = {
            "time": datetime.now().strftime("%H:%M"),
            "greeting": self._get_greeting(),
        }
        
        # Last session
        session = self._get_last_session()
        if session:
            data["last_session"] = session
        
        # Git status
        git = self._get_git_status()
        if git:
            data["git"] = git
        
        # Active processes
        processes = self._get_active_tools()
        if processes:
            data["active_tools"] = processes
        
        return data
    
    def _get_greeting(self) -> str:
        """Time-based greeting."""
        hour = datetime.now().hour
        if hour < 6:
            return "Gute Nacht"
        elif hour < 12:
            return "Guten Morgen"
        elif hour < 18:
            return "Guten Tag"
        else:
            return "Guten Abend"
    
    def _get_last_session(self) -> Optional[Dict]:
        """Get last session info."""
        if not self.history_path.exists():
            return None
        
        try:
            with open(self.history_path) as f:
                windows = json.load(f)
            
            if windows:
                last = windows[-1]
                age_sec = datetime.now().timestamp() - last.get("start_time", 0)
                age_min = int(age_sec / 60)
                
                return {
                    "age_minutes": age_min,
                    "messages": len(last.get("messages", [])),
                    "tool": last.get("tool", "unknown"),
                    "summary": last.get("summary", "")
                }
        except:
            pass
        
        return None
    
    def _get_git_status(self) -> Optional[Dict]:
        """Get git status of current directory."""
        try:
            # Get branch
            branch = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True, text=True, timeout=2
            ).stdout.strip()
            
            # Get status
            status = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True, text=True, timeout=2
            ).stdout.strip()
            
            changes = len(status.split("\n")) if status else 0
            
            return {
                "branch": branch,
                "changes": changes
            }
        except:
            return None
    
    def _get_active_tools(self) -> list:
        """Get active CLI tools."""
        tools = []
        for tool in ["opencode", "gemini", "claude"]:
            try:
                result = subprocess.run(
                    ["pgrep", "-x", tool],
                    capture_output=True, timeout=1
                )
                if result.returncode == 0:
                    tools.append(tool)
            except:
                pass
        return tools
    
    def _template_briefing(self, data: Dict) -> str:
        """Generate briefing from template."""
        parts = [f"{data['greeting']} Jannis."]
        
        # Last session
        if "last_session" in data:
            s = data["last_session"]
            age = s["age_minutes"]
            if age < 60:
                parts.append(f"Letzte Session vor {age} Minuten mit {s['tool']}.")
            elif age < 1440:
                parts.append(f"Letzte Session vor {age // 60} Stunden.")
            
            if s.get("summary"):
                parts.append(s["summary"][:100])
        
        # Git
        if "git" in data:
            g = data["git"]
            if g["changes"] > 0:
                parts.append(f"{g['changes']} uncommitted changes auf {g['branch']}.")
        
        # Active tools
        if data.get("active_tools"):
            parts.append(f"Aktiv: {', '.join(data['active_tools'])}.")
        
        parts.append("Womit sollen wir starten?")
        
        return " ".join(parts)


if __name__ == "__main__":
    gen = BriefingGenerator()
    print(gen.generate())
