# Wanda Voice Assistant - Active Window Detection
"""Detect active application for context-aware actions. Works on X11 and Wayland."""

import subprocess
import os
from typing import Dict, Optional


def detect_display_server() -> str:
    """Detect if running on X11 or Wayland."""
    session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if session_type == "wayland":
        return "wayland"
    if session_type == "x11":
        return "x11"
    
    # Fallback detection
    if os.environ.get("WAYLAND_DISPLAY"):
        return "wayland"
    if os.environ.get("DISPLAY"):
        return "x11"
    
    return "unknown"


class ActiveWindowDetector:
    """Detect active app for context-aware responses. Works on X11 and Wayland."""
    
    TERMINAL_NAMES = [
        "terminal", "konsole", "gnome-terminal", "cosmic-term",
        "alacritty", "kitty", "xterm", "tilix", "terminator",
        "wezterm", "foot", "contour"
    ]
    
    BROWSER_NAMES = [
        "firefox", "chrome", "chromium", "brave", "edge",
        "opera", "vivaldi", "zen", "librewolf"
    ]
    
    EDITOR_NAMES = [
        "code", "vscode", "atom", "sublime", "vim", "nvim",
        "emacs", "gedit", "kate", "cursor", "zed", "cosmic-edit"
    ]
    
    def __init__(self):
        self.display_server = detect_display_server()
        print(f"[ActiveWindow] Display server: {self.display_server}")
    
    def get_active_window(self) -> Dict[str, str]:
        """Get active window info (works on X11 and Wayland)."""
        
        # Wayland: Try COSMIC first (Pop!_OS COSMIC)
        if self.display_server == "wayland":
            window = self._get_wayland_cosmic()
            if window:
                return window
            
            window = self._get_wayland_gnome()
            if window:
                return window
            
            window = self._get_wayland_kde()
            if window:
                return window
            
            window = self._get_wayland_sway()
            if window:
                return window
        
        # X11: xdotool
        window = self._get_x11_xdotool()
        if window:
            return window
        
        # XWayland fallback
        window = self._get_xwayland()
        if window:
            return window
        
        return {"name": "unknown", "display": self.display_server}
    
    def _get_wayland_cosmic(self) -> Optional[Dict[str, str]]:
        """Get active window on COSMIC (Pop!_OS)."""
        try:
            # COSMIC uses its own IPC - try cosmic-query if available
            result = subprocess.run(
                ["cosmic-query", "focused-window"],
                capture_output=True, text=True, timeout=1
            )
            if result.returncode == 0:
                return {"name": result.stdout.strip(), "display": "wayland-cosmic"}
        except:
            pass
        
        # Fallback: check running processes for COSMIC apps
        try:
            result = subprocess.run(["ps", "-eo", "comm"], capture_output=True, text=True, timeout=1)
            if "cosmic-term" in result.stdout:
                return {"name": "cosmic-term", "display": "wayland-cosmic"}
            if "cosmic-edit" in result.stdout:
                return {"name": "cosmic-edit", "display": "wayland-cosmic"}
        except:
            pass
        
        return None
    
    def _get_wayland_gnome(self) -> Optional[Dict[str, str]]:
        """Get active window on GNOME Wayland."""
        try:
            result = subprocess.run(
                ["gdbus", "call", "--session",
                 "--dest", "org.gnome.Shell",
                 "--object-path", "/org/gnome/Shell",
                 "--method", "org.gnome.Shell.Eval",
                 "global.display.focus_window.get_title()"],
                capture_output=True, text=True, timeout=1
            )
            if result.returncode == 0 and "true" in result.stdout:
                # Parse: (true, 'Window Title')
                import re
                match = re.search(r"'([^']*)'", result.stdout)
                if match:
                    return {"name": match.group(1), "display": "wayland-gnome"}
        except:
            pass
        return None
    
    def _get_wayland_kde(self) -> Optional[Dict[str, str]]:
        """Get active window on KDE Plasma Wayland."""
        try:
            result = subprocess.run(
                ["qdbus", "org.kde.KWin", "/KWin", "activeClient"],
                capture_output=True, text=True, timeout=1
            )
            if result.returncode == 0:
                return {"name": result.stdout.strip(), "display": "wayland-kde"}
        except:
            pass
        return None
    
    def _get_wayland_sway(self) -> Optional[Dict[str, str]]:
        """Get active window on Sway/wlroots compositors."""
        try:
            result = subprocess.run(
                ["swaymsg", "-t", "get_tree"],
                capture_output=True, text=True, timeout=1
            )
            if result.returncode == 0:
                import json
                tree = json.loads(result.stdout)
                name = self._find_focused_sway(tree)
                if name:
                    return {"name": name, "display": "wayland-sway"}
        except:
            pass
        return None
    
    def _find_focused_sway(self, node: dict) -> Optional[str]:
        """Recursively find focused window in Sway tree."""
        if node.get("focused"):
            return node.get("name", "unknown")
        for child in node.get("nodes", []) + node.get("floating_nodes", []):
            result = self._find_focused_sway(child)
            if result:
                return result
        return None
    
    def _get_x11_xdotool(self) -> Optional[Dict[str, str]]:
        """Get active window using xdotool (X11)."""
        try:
            result = subprocess.run(
                ["xdotool", "getactivewindow", "getwindowname"],
                capture_output=True, text=True, timeout=1
            )
            if result.returncode == 0:
                return {"name": result.stdout.strip(), "display": "x11"}
        except:
            pass
        return None
    
    def _get_xwayland(self) -> Optional[Dict[str, str]]:
        """Try XWayland fallback."""
        try:
            # Some Wayland compositors support XWayland
            result = subprocess.run(
                ["xprop", "-root", "_NET_ACTIVE_WINDOW"],
                capture_output=True, text=True, timeout=1
            )
            if result.returncode == 0:
                # Parse window ID and get name
                pass  # Complex - skip for now
        except:
            pass
        return None
    
    def get_active_app_type(self) -> Optional[str]:
        """Get type of active application."""
        window = self.get_active_window()
        name = window["name"].lower()
        
        if any(t in name for t in self.TERMINAL_NAMES):
            return "terminal"
        if any(b in name for b in self.BROWSER_NAMES):
            return "browser"
        if any(e in name for e in self.EDITOR_NAMES):
            return "editor"
        
        return None
    
    def is_terminal(self) -> bool:
        return self.get_active_app_type() == "terminal"
    
    def is_browser(self) -> bool:
        return self.get_active_app_type() == "browser"
    
    def is_editor(self) -> bool:
        return self.get_active_app_type() == "editor"


if __name__ == "__main__":
    detector = ActiveWindowDetector()
    window = detector.get_active_window()
    app_type = detector.get_active_app_type()
    print(f"Display: {detector.display_server}")
    print(f"Active: {window['name']} ({window['display']})")
    print(f"Type: {app_type}")
