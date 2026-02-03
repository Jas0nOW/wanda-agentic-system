#!/usr/bin/env python3
"""
WANDA Voice Wrapper - Robustes Error-Handling
Fängt alle Fehler ab und zeigt hilfreiche Meldungen.
"""

import os
import sys
import subprocess
import traceback

# Colors
RED = "\033[0;31m"
GREEN = "\033[0;32m"
YELLOW = "\033[1;33m"
CYAN = "\033[0;36m"
NC = "\033[0m"


def print_banner():
    print(f"{CYAN}")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║                                                              ║")
    print("║     🎙️  WANDA VOICE - Robust Mode                           ║")
    print("║                                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")
    print(f"{NC}")


def check_dependencies():
    """Check if all dependencies are installed."""
    issues = []

    # Check Python packages
    packages = ["sounddevice", "numpy", "vosk"]
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            issues.append(f"Python package missing: {pkg}")

    # Check model
    model_path = os.path.join(os.path.dirname(__file__), "model")
    if not os.path.exists(model_path) or not os.path.exists(
        os.path.join(model_path, "final.mdl")
    ):
        issues.append("Vosk model not found")

    return issues


def check_wayland_tools():
    """Check Wayland-specific tools."""
    tools = []

    if subprocess.run(["which", "wtype"], capture_output=True).returncode == 0:
        tools.append("wtype")
    if subprocess.run(["which", "xdotool"], capture_output=True).returncode == 0:
        tools.append("xdotool")

    return tools


def main():
    print_banner()

    # Check dependencies
    print(f"{CYAN}Checking dependencies...{NC}")
    issues = check_dependencies()

    if issues:
        print(f"\n{RED}❌ Missing dependencies:{NC}")
        for issue in issues:
            print(f"  • {issue}")
        print(f"\n{YELLOW}Run setup_voice.sh to install dependencies{NC}")
        input("\nPress Enter to exit...")
        return 1

    print(f"{GREEN}✓ All dependencies found{NC}")

    # Check Wayland tools
    tools = check_wayland_tools()
    if tools:
        print(f"{GREEN}✓ Typing tools: {', '.join(tools)}{NC}")
    else:
        print(f"{YELLOW}⚠ No typing tools found (wtype/xdotool){NC}")

    print(f"\n{CYAN}Starting Voice Assistant...{NC}\n")

    # Import and run actual voice assistant
    try:
        # Change to script directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Import voice module
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

        # Try to import and run
        try:
            import voice_to_text

            # If it has a main function, call it
            if hasattr(voice_to_text, "main"):
                voice_to_text.main()
            else:
                # Otherwise just let it run (it runs on import)
                pass
        except Exception as e:
            print(f"\n{RED}❌ Error starting Voice Assistant:{NC}")
            print(f"{RED}{str(e)}{NC}")
            print(f"\n{YELLOW}Full error:{NC}")
            traceback.print_exc()
            input("\nPress Enter to exit...")
            return 1

    except KeyboardInterrupt:
        print(f"\n\n{CYAN}👋 Goodbye!{NC}")
        return 0
    except Exception as e:
        print(f"\n{RED}❌ Unexpected error:{NC}")
        print(f"{RED}{str(e)}{NC}")
        traceback.print_exc()
        input("\nPress Enter to exit...")
        return 1


if __name__ == "__main__":
    sys.exit(main())
