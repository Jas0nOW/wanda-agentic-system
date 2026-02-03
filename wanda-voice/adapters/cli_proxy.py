# Wanda Voice Assistant - CLI Proxy
"""Multi-CLI injection and output capture for opencode, gemini, claude."""

import subprocess
import time
import threading
from typing import Optional, Callable, Dict, List
from pathlib import Path

try:
    import pexpect
    PEXPECT_AVAILABLE = True
except ImportError:
    PEXPECT_AVAILABLE = False


class CLISession:
    """A session with a CLI tool."""
    
    def __init__(self, tool: str, command: str, timeout: int = 120):
        self.tool = tool
        self.command = command
        self.timeout = timeout
        self.session: Optional[pexpect.spawn] = None
        self.last_output = ""
        
    def start(self) -> bool:
        """Start CLI session."""
        if not PEXPECT_AVAILABLE:
            print(f"[CLI] pexpect not available")
            return False
        
        try:
            self.session = pexpect.spawn(
                self.command,
                encoding="utf-8",
                timeout=self.timeout
            )
            print(f"[CLI] Started {self.tool}")
            return True
        except Exception as e:
            print(f"[CLI] Failed to start {self.tool}: {e}")
            return False
    
    def send(self, text: str) -> str:
        """Send text to CLI and get response."""
        if not self.session or not self.session.isalive():
            return "Session not active"
        
        try:
            self.session.sendline(text)
            
            # Wait for response (prompt marker)
            self.session.expect([r"[>$#]", pexpect.TIMEOUT], timeout=self.timeout)
            
            response = self.session.before.strip()
            self.last_output = response
            
            # Clean echoed input
            lines = response.split("\n")
            if lines and text in lines[0]:
                lines = lines[1:]
            
            return "\n".join(lines).strip()
            
        except pexpect.TIMEOUT:
            return "⏱️ CLI timeout"
        except Exception as e:
            return f"Error: {e}"
    
    def close(self):
        """Close session."""
        if self.session:
            try:
                self.session.sendline("exit")
                self.session.close()
            except:
                pass
            self.session = None


class CLIProxy:
    """
    Proxy for multiple CLI AI tools.
    Handles detection, injection, and output capture.
    """
    
    CLI_TOOLS = {
        "gemini": {
            "command": "gemini",
            "process_names": ["gemini"],
            "window_patterns": ["gemini"]
        },
        "opencode": {
            "command": "opencode",
            "process_names": ["opencode"],
            "window_patterns": ["opencode", "oc"]
        },
        "claude": {
            "command": "claude",
            "process_names": ["claude", "claude-code"],
            "window_patterns": ["claude"]
        },
        "codex": {
            "command": "codex",
            "process_names": ["codex"],
            "window_patterns": ["codex"]
        }
    }
    
    def __init__(self, on_output: Optional[Callable[[str], None]] = None):
        self.sessions: Dict[str, CLISession] = {}
        self.active_tool: Optional[str] = None
        self.on_output = on_output  # Callback for TTS
    
    def detect_active_cli(self) -> Optional[str]:
        """Detect which CLI tool is active (works on X11 and Wayland)."""
        import os
        is_wayland = os.environ.get("XDG_SESSION_TYPE") == "wayland" or os.environ.get("WAYLAND_DISPLAY")
        
        # Try window detection
        window_name = None
        
        if is_wayland:
            # GNOME Wayland
            try:
                result = subprocess.run(
                    ["gdbus", "call", "--session",
                     "--dest", "org.gnome.Shell",
                     "--object-path", "/org/gnome/Shell",
                     "--method", "org.gnome.Shell.Eval",
                     "global.display.focus_window.get_title()"],
                    capture_output=True, text=True, timeout=1
                )
                if "true" in result.stdout:
                    import re
                    match = re.search(r"'([^']*)'", result.stdout)
                    if match:
                        window_name = match.group(1).lower()
            except:
                pass
            
            # Sway/wlroots
            if not window_name:
                try:
                    result = subprocess.run(
                        ["swaymsg", "-t", "get_tree"],
                        capture_output=True, text=True, timeout=1
                    )
                    if result.returncode == 0:
                        import json
                        tree = json.loads(result.stdout)
                        focused = self._find_focused(tree)
                        if focused:
                            window_name = focused.lower()
                except:
                    pass
        
        # X11 / XWayland fallback
        if not window_name:
            try:
                result = subprocess.run(
                    ["xdotool", "getactivewindow", "getwindowname"],
                    capture_output=True, text=True, timeout=1
                )
                if result.returncode == 0:
                    window_name = result.stdout.lower()
            except:
                pass
        
        # Match window name to CLI tool
        if window_name:
            for tool, info in self.CLI_TOOLS.items():
                if any(p in window_name for p in info["window_patterns"]):
                    return tool
        
        # Fallback: check running processes
        try:
            result = subprocess.run(["ps", "-e"], capture_output=True, text=True)
            processes = result.stdout.lower()
            for tool, info in self.CLI_TOOLS.items():
                if any(p in processes for p in info["process_names"]):
                    return tool
        except:
            pass
        
        return None
    
    def _find_focused(self, node: dict) -> Optional[str]:
        """Find focused window in Sway tree."""
        if node.get("focused"):
            return node.get("name")
        for child in node.get("nodes", []) + node.get("floating_nodes", []):
            result = self._find_focused(child)
            if result:
                return result
        return None
    
    def get_or_create_session(self, tool: str) -> Optional[CLISession]:
        """Get existing session or create new one."""
        if tool in self.sessions and self.sessions[tool].session:
            if self.sessions[tool].session.isalive():
                return self.sessions[tool]
        
        # Create new session
        if tool not in self.CLI_TOOLS:
            return None
        
        session = CLISession(tool, self.CLI_TOOLS[tool]["command"])
        if session.start():
            self.sessions[tool] = session
            return session
        
        return None
    
    def send_to_cli(self, text: str, tool: Optional[str] = None) -> str:
        """Send text to CLI tool and get response."""
        tool = tool or self.detect_active_cli() or "gemini"
        self.active_tool = tool
        
        session = self.get_or_create_session(tool)
        if not session:
            return f"Could not start {tool} session"
        
        print(f"[CLI] Sending to {tool}: {text[:50]}...")
        response = session.send(text)
        
        # Callback for TTS
        if self.on_output:
            self.on_output(response)
        
        return response
    
    def inject_to_active_window(self, text: str) -> bool:
        """Inject text into active window (X11 and Wayland)."""
        import os
        is_wayland = os.environ.get("XDG_SESSION_TYPE") == "wayland" or os.environ.get("WAYLAND_DISPLAY")
        
        if is_wayland:
            # Try wtype first (Wayland native)
            success = self._inject_wtype(text)
            if success:
                return True
            
            # Try ydotool (works on both)
            success = self._inject_ydotool(text)
            if success:
                return True
        
        # Fallback: xdotool (X11 or XWayland)
        return self._inject_xdotool(text)
    
    def _inject_wtype(self, text: str) -> bool:
        """Inject using wtype (Wayland native)."""
        try:
            subprocess.run(["wtype", text], timeout=30, check=True)
            subprocess.run(["wtype", "-k", "Return"], timeout=2)
            return True
        except:
            return False
    
    def _inject_ydotool(self, text: str) -> bool:
        """Inject using ydotool (works on X11 and Wayland)."""
        try:
            subprocess.run(["ydotool", "type", "--", text], timeout=30, check=True)
            subprocess.run(["ydotool", "key", "28:1", "28:0"], timeout=2)  # Enter key
            return True
        except:
            return False
    
    def _inject_xdotool(self, text: str) -> bool:
        """Inject using xdotool (X11 only)."""
        try:
            subprocess.run(
                ["xdotool", "type", "--delay", "10", text],
                timeout=30
            )
            subprocess.run(["xdotool", "key", "Return"], timeout=2)
            return True
        except Exception as e:
            print(f"[CLI] Injection failed: {e}")
            return False
    
    def close_all(self):
        """Close all sessions."""
        for session in self.sessions.values():
            session.close()
        self.sessions = {}


if __name__ == "__main__":
    print("Testing CLI Proxy...")
    proxy = CLIProxy()
    
    active = proxy.detect_active_cli()
    print(f"Active CLI: {active}")
