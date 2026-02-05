#!/usr/bin/env python3
"""
WANDA Voice Launcher - Wayland Compatible
Universal launcher for WANDA Voice Assistant with desktop environment detection.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

# Colors for terminal output
CYAN = "\033[0;36m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
RED = "\033[0;31m"
MAGENTA = "\033[0;35m"
NC = "\033[0m"
BOLD = "\033[1m"


def print_banner():
    """Print WANDA Voice banner."""
    print(f"{MAGENTA}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║     🎙️  WANDA VOICE - Sovereign AI Voice Assistant          ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{NC}")


def detect_desktop_environment():
    """Detect the current desktop environment and session type."""
    session_type = os.environ.get("XDG_SESSION_TYPE", "unknown")
    desktop_env = os.environ.get("XDG_CURRENT_DESKTOP", "unknown")
    wayland_display = os.environ.get("WAYLAND_DISPLAY", "")
    display = os.environ.get("DISPLAY", "")

    return {
        "session_type": session_type.lower(),
        "desktop_env": desktop_env.lower(),
        "wayland_display": wayland_display,
        "display": display,
    }


def module_available(module_name, import_name=None):
    """Check if a Python module can be imported."""
    try:
        __import__(import_name or module_name)
        return True
    except Exception:
        return False


def check_wayland_compositor():
    """Check which Wayland compositor is running."""
    # Check for specific compositor environment variables
    if os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"):
        return "hyprland"
    elif os.environ.get("SWAYSOCK"):
        return "sway"
    elif os.environ.get("WAYFIRE_SOCKET"):
        return "wayfire"
    elif os.path.exists("/run/user/1000/river-session"):
        return "river"
    elif (
        os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "gnome"
        and os.environ.get("XDG_SESSION_TYPE") == "wayland"
    ):
        return "gnome-wayland"
    elif (
        os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "kde"
        and os.environ.get("XDG_SESSION_TYPE") == "wayland"
    ):
        return "kde-wayland"
    elif os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "cosmic":
        return "cosmic"
    return "unknown"


def setup_wayland_environment():
    """Setup environment for Wayland compatibility."""
    env = os.environ.copy()

    # Force Wayland backend for GTK if available
    env["GDK_BACKEND"] = "wayland"

    # Disable GTK CSD (Client-Side Decorations) for better compatibility
    env["GTK_CSD"] = "0"

    # Enable fractional scaling support
    env["GDK_SCALE"] = os.environ.get("GDK_SCALE", "1")

    # For Qt applications on Wayland
    env["QT_QPA_PLATFORM"] = "wayland"

    return env


def setup_xwayland_fallback():
    """Setup environment to use XWayland fallback."""
    env = os.environ.copy()
    env["GDK_BACKEND"] = "x11"
    env["QT_QPA_PLATFORM"] = "xcb"
    return env


def get_python_executable(voice_dir: Path) -> str:
    """Prefer voice venv Python if available."""
    venv_python = voice_dir / "venv" / "bin" / "python3"
    if venv_python.exists():
        return str(venv_python)
    return sys.executable


def launch_voice_assistant(use_xwayland=False, debug=False):
    """Launch the WANDA voice assistant."""
    print_banner()

    # Detect environment
    env_info = detect_desktop_environment()
    compositor = check_wayland_compositor()

    print(f"{CYAN}Environment Detection:{NC}")
    print(f"  Session Type: {env_info['session_type']}")
    print(f"  Desktop: {env_info['desktop_env']}")
    print(f"  Compositor: {compositor}")
    print()

    # Wayland safety checks
    if env_info["session_type"] == "wayland":
        gi_ok = module_available("gi")
        evdev_ok = module_available("evdev")
        if not gi_ok:
            print(
                f"{YELLOW}Wayland fallback: missing GTK, switching to simple mode{NC}"
            )
            return launch_simple_voice()
        if not evdev_ok:
            print(
                f"{YELLOW}Wayland: evdev not available, hotkey disabled (GUI still enabled){NC}"
            )

    # Determine environment setup
    if use_xwayland or env_info["session_type"] != "wayland":
        print(f"{YELLOW}Using X11/XWayland backend{NC}")
        env = setup_xwayland_fallback()
    else:
        print(f"{GREEN}Using native Wayland backend{NC}")
        env = setup_wayland_environment()

    # Find voice assistant directory
    install_dir = os.environ.get(
        "WANDA_INSTALL_DIR", os.path.expanduser("~/.wanda-system")
    )
    voice_dir = Path(install_dir) / "wanda-voice"

    if not voice_dir.exists():
        # Try current directory
        voice_dir = Path(__file__).parent.parent / "wanda-voice"

    if not voice_dir.exists():
        print(f"{RED}Error: Voice assistant not found at {voice_dir}{NC}")
        print(f"{YELLOW}Please ensure WANDA is properly installed.{NC}")
        return 1

    print(f"{CYAN}Starting WANDA Voice from: {voice_dir}{NC}")
    print()

    # Prepare command
    python_exe = get_python_executable(voice_dir)
    cmd = [python_exe, str(voice_dir / "main.py")]

    if debug:
        cmd.append("--debug")
        print(f"{YELLOW}Debug mode enabled{NC}")

    # Launch with proper environment
    try:
        result = subprocess.run(cmd, cwd=str(voice_dir), env=env)
        return result.returncode
    except KeyboardInterrupt:
        print(f"\n{CYAN}WANDA Voice stopped by user{NC}")
        return 0
    except Exception as e:
        print(f"{RED}Error launching WANDA Voice: {e}{NC}")
        return 1


def launch_simple_voice():
    """Launch simplified voice mode without GUI (most compatible).
    Uses main.py --simple which delegates to WandaVoiceEngine."""
    print_banner()
    print(f"{YELLOW}Starting WANDA Voice in simple mode (no GUI){NC}")
    print(f"{CYAN}This mode works on all desktop environments including Wayland{NC}")
    print()

    install_dir = os.environ.get(
        "WANDA_INSTALL_DIR", os.path.expanduser("~/.wanda-system")
    )
    voice_dir = Path(install_dir) / "wanda-voice"

    if not voice_dir.exists():
        voice_dir = Path(__file__).parent.parent / "wanda-voice"

    if not voice_dir.exists():
        voice_dir = Path(__file__).parent

    python_exe = get_python_executable(voice_dir)
    cmd = [python_exe, str(voice_dir / "main.py"), "--simple"]

    try:
        result = subprocess.run(cmd, cwd=str(voice_dir))
        return result.returncode
    except KeyboardInterrupt:
        print(f"\n{CYAN}WANDA Voice stopped{NC}")
        return 0
    except Exception as e:
        print(f"{RED}Error: {e}{NC}")
        return 1


def main():
    parser = argparse.ArgumentParser(
        description="WANDA Voice Assistant Launcher - Wayland Compatible",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                    Launch with auto-detected backend
  %(prog)s --xwayland         Force XWayland/X11 backend
  %(prog)s --simple           Simple mode without GUI
  %(prog)s --debug            Debug mode with verbose output
        """,
    )

    parser.add_argument(
        "--xwayland",
        action="store_true",
        help="Force XWayland/X11 backend (more compatible)",
    )
    parser.add_argument(
        "--simple",
        action="store_true",
        help="Simple mode without GUI orb (most compatible)",
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    parser.add_argument(
        "--status", action="store_true", help="Show environment status and exit"
    )

    args = parser.parse_args()

    if args.status:
        print_banner()
        env_info = detect_desktop_environment()
        compositor = check_wayland_compositor()

        print(f"{CYAN}System Information:{NC}")
        print(f"  Session Type: {env_info['session_type']}")
        print(f"  Desktop Environment: {env_info['desktop_env']}")
        print(f"  Wayland Display: {env_info['wayland_display'] or 'Not set'}")
        print(f"  X11 Display: {env_info['display'] or 'Not set'}")
        print(f"  Detected Compositor: {compositor}")
        print()

        # Check dependencies
        print(f"{CYAN}Dependencies:{NC}")
        deps = [
            "sounddevice",
            "numpy",
            "faster-whisper",
            "piper-tts",
            "evdev",
            "PyGObject",
        ]
        for dep in deps:
            try:
                if dep == "PyGObject":
                    __import__("gi")
                elif dep == "piper-tts":
                    __import__("piper")
                elif dep == "faster-whisper":
                    __import__("faster_whisper")
                else:
                    __import__(dep.replace("-", "_"))
                print(f"  {GREEN}✓{NC} {dep}")
            except ImportError:
                print(f"  {RED}✗{NC} {dep} (not installed)")

        return 0

    if args.simple:
        return launch_simple_voice()
    else:
        return launch_voice_assistant(use_xwayland=args.xwayland, debug=args.debug)


if __name__ == "__main__":
    sys.exit(main())
