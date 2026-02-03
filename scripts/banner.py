#!/usr/bin/env python3
"""
WANDA Enhanced Banner Generator
Creates animated, colorful ASCII art banners with gradients and effects.
"""

import time
import sys
import os


# ANSI Color Codes
class Colors:
    # Standard colors
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    MAGENTA = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"

    # Bright colors
    BRIGHT_BLACK = "\033[0;90m"
    BRIGHT_RED = "\033[0;91m"
    BRIGHT_GREEN = "\033[0;92m"
    BRIGHT_YELLOW = "\033[0;93m"
    BRIGHT_BLUE = "\033[0;94m"
    BRIGHT_MAGENTA = "\033[0;95m"
    BRIGHT_CYAN = "\033[0;96m"
    BRIGHT_WHITE = "\033[0;97m"

    # Special effects
    BOLD = "\033[1m"
    DIM = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    REVERSE = "\033[7m"
    STRIKETHROUGH = "\033[9m"

    # Reset
    RESET = "\033[0m"

    # 256 colors (gradients)
    @staticmethod
    def rgb(r, g, b):
        return f"\033[38;2;{r};{g};{b}m"

    @staticmethod
    def bg_rgb(r, g, b):
        return f"\033[48;2;{r};{g};{b}m"

    @staticmethod
    def gradient_color(start_rgb, end_rgb, steps, step):
        """Calculate intermediate color in gradient."""
        r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * step / steps)
        g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * step / steps)
        b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * step / steps)
        return Colors.rgb(r, g, b)


class WandaBanner:
    """Enhanced WANDA banner with animations and effects."""

    # WANDA ASCII Art - Large
    LOGO_LARGE = [
        "██╗    ██╗ █████╗ ███╗   ██╗██████╗  █████╗",
        "██║    ██║██╔══██╗████╗  ██║██╔══██╗██╔══██╗",
        "██║ █╗ ██║███████║██╔██╗ ██║██║  ██║███████║",
        "██║███╗██║██╔══██║██║╚██╗██║██║  ██║██╔══██║",
        "╚███╔███╔╝██║  ██║██║ ╚████║██████╔╝██║  ██║",
        " ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝",
    ]

    # WANDA ASCII Art - Compact
    LOGO_COMPACT = [
        "██╗    ██╗ █████╗ ███╗   ██╗██████╗  █████╗",
        "██║    ██║██╔══██╗████╗  ██║██╔══██╗██╔══██╗",
        "██║ █╗ ██║███████║██╔██╗ ██║██║  ██║███████║",
        "██║███╗██║██╔══██║██║╚██╗██║██║  ██║██╔══██║",
        "╚███╔███╔╝██║  ██║██║ ╚████║██████╔╝██║  ██║",
        " ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝",
    ]

    # Color schemes
    SCHEMES = {
        "cyberpunk": {
            "primary": (255, 0, 255),  # Magenta
            "secondary": (0, 255, 255),  # Cyan
            "accent": (255, 255, 0),  # Yellow
            "bg": (10, 0, 20),
        },
        "ocean": {
            "primary": (0, 150, 255),  # Deep Blue
            "secondary": (0, 255, 200),  # Aqua
            "accent": (100, 200, 255),  # Light Blue
            "bg": (0, 10, 30),
        },
        "sunset": {
            "primary": (255, 100, 0),  # Orange
            "secondary": (255, 0, 100),  # Pink
            "accent": (255, 200, 0),  # Gold
            "bg": (30, 5, 10),
        },
        "matrix": {
            "primary": (0, 255, 0),  # Green
            "secondary": (0, 200, 0),  # Dark Green
            "accent": (150, 255, 150),  # Light Green
            "bg": (0, 10, 0),
        },
        "royal": {
            "primary": (124, 58, 237),  # Purple
            "secondary": (59, 130, 246),  # Blue
            "accent": (236, 72, 153),  # Pink
            "bg": (20, 0, 40),
        },
    }

    def __init__(self, scheme="cyberpunk"):
        self.scheme = self.SCHEMES.get(scheme, self.SCHEMES["cyberpunk"])
        self.frame_count = 0

    def _rainbow_gradient(self, text, offset=0):
        """Apply rainbow gradient to text."""
        result = ""
        colors = [
            (255, 0, 0),  # Red
            (255, 127, 0),  # Orange
            (255, 255, 0),  # Yellow
            (0, 255, 0),  # Green
            (0, 0, 255),  # Blue
            (75, 0, 130),  # Indigo
            (148, 0, 211),  # Violet
        ]

        for i, char in enumerate(text):
            if char == " ":
                result += char
                continue
            color_idx = (i + offset) % len(colors)
            result += Colors.rgb(*colors[color_idx]) + char + Colors.RESET

        return result

    def _gradient_line(self, text, start_color, end_color):
        """Apply horizontal gradient to a line."""
        result = ""
        length = len(text)

        for i, char in enumerate(text):
            if char == " ":
                result += char
                continue
            color = Colors.gradient_color(start_color, end_color, length, i)
            result += color + char + Colors.RESET

        return result

    def _glow_effect(self, text, color):
        """Add glow effect with shadow."""
        glow = Colors.DIM + Colors.rgb(
            max(0, color[0] - 50), max(0, color[1] - 50), max(0, color[2] - 50)
        )
        bright = Colors.BOLD + Colors.rgb(*color)
        return glow + text + Colors.RESET

    def _animated_wave(self, text, frame, color1, color2):
        """Create animated wave effect."""
        result = ""
        wave = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 0.8, 0.6, 0.4, 0.2]

        for i, char in enumerate(text):
            if char == " ":
                result += char
                continue

            wave_idx = (i + frame) % len(wave)
            intensity = wave[wave_idx]

            r = int(color1[0] + (color2[0] - color1[0]) * intensity)
            g = int(color1[1] + (color2[1] - color1[1]) * intensity)
            b = int(color1[2] + (color2[2] - color1[2]) * intensity)

            result += Colors.rgb(r, g, b) + char + Colors.RESET

        return result

    def print_static(self, show_subtitle=True, version="1.0.4"):
        """Print static banner with gradient."""
        primary = self.scheme["primary"]
        secondary = self.scheme["secondary"]
        accent = self.scheme["accent"]

        # Top border
        print(Colors.rgb(*primary) + "╔" + "═" * 62 + "╗" + Colors.RESET)
        print(Colors.rgb(*primary) + "║" + " " * 62 + "║" + Colors.RESET)

        # Logo with gradient
        for i, line in enumerate(self.LOGO_LARGE):
            if i < 3:
                colored = self._gradient_line(line, primary, secondary)
            else:
                colored = self._gradient_line(line, secondary, accent)
            padding = (62 - len(line)) // 2
            print(
                Colors.rgb(*primary)
                + "║"
                + " " * padding
                + colored
                + " " * (62 - padding - len(line))
                + Colors.rgb(*primary)
                + "║"
                + Colors.RESET
            )

        # Subtitle
        if show_subtitle:
            print(Colors.rgb(*primary) + "║" + " " * 62 + "║" + Colors.RESET)
            subtitle = "Workspace-Aware Neural Development Assistant"
            colored_sub = self._gradient_line(subtitle, accent, primary)
            padding = (62 - len(subtitle)) // 2
            print(
                Colors.rgb(*primary)
                + "║"
                + " " * padding
                + colored_sub
                + " " * (62 - padding - len(subtitle))
                + Colors.rgb(*primary)
                + "║"
                + Colors.RESET
            )

            version_text = f"v{version} - Sovereign AI OS"
            colored_ver = (
                Colors.BOLD + Colors.rgb(*secondary) + version_text + Colors.RESET
            )
            padding = (62 - len(version_text)) // 2
            print(
                Colors.rgb(*primary)
                + "║"
                + " " * padding
                + colored_ver
                + " " * (62 - padding - len(version_text))
                + Colors.rgb(*primary)
                + "║"
                + Colors.RESET
            )

        # Bottom border
        print(Colors.rgb(*primary) + "║" + " " * 62 + "║" + Colors.RESET)
        print(Colors.rgb(*primary) + "╚" + "═" * 62 + "╝" + Colors.RESET)

    def print_animated(self, duration=2.0, fps=10):
        """Print animated banner."""
        frames = int(duration * fps)

        for frame in range(frames):
            # Clear screen
            print("\033[2J\033[H", end="")

            primary = self.scheme["primary"]
            secondary = self.scheme["secondary"]
            accent = self.scheme["accent"]

            # Top border with pulse
            pulse = abs((frame % 20) - 10) / 10.0
            r = int(primary[0] * (0.7 + 0.3 * pulse))
            g = int(primary[1] * (0.7 + 0.3 * pulse))
            b = int(primary[2] * (0.7 + 0.3 * pulse))

            print(Colors.rgb(r, g, b) + "╔" + "═" * 62 + "╗" + Colors.RESET)
            print(Colors.rgb(r, g, b) + "║" + " " * 62 + "║" + Colors.RESET)

            # Logo with wave animation
            for i, line in enumerate(self.LOGO_LARGE):
                if i < 3:
                    colored = self._animated_wave(line, frame + i, primary, secondary)
                else:
                    colored = self._animated_wave(line, frame + i, secondary, accent)
                padding = (62 - len(line)) // 2
                print(
                    Colors.rgb(r, g, b)
                    + "║"
                    + " " * padding
                    + colored
                    + " " * (62 - padding - len(line))
                    + Colors.rgb(r, g, b)
                    + "║"
                    + Colors.RESET
                )

            # Subtitle
            print(Colors.rgb(r, g, b) + "║" + " " * 62 + "║" + Colors.RESET)
            subtitle = "Workspace-Aware Neural Development Assistant"
            colored_sub = self._animated_wave(subtitle, frame, accent, primary)
            padding = (62 - len(subtitle)) // 2
            print(
                Colors.rgb(r, g, b)
                + "║"
                + " " * padding
                + colored_sub
                + " " * (62 - padding - len(subtitle))
                + Colors.rgb(r, g, b)
                + "║"
                + Colors.RESET
            )

            version_text = "v1.0.4 - Sovereign AI OS"
            colored_ver = (
                Colors.BOLD + Colors.rgb(*secondary) + version_text + Colors.RESET
            )
            padding = (62 - len(version_text)) // 2
            print(
                Colors.rgb(r, g, b)
                + "║"
                + " " * padding
                + colored_ver
                + " " * (62 - padding - len(version_text))
                + Colors.rgb(r, g, b)
                + "║"
                + Colors.RESET
            )

            print(Colors.rgb(r, g, b) + "║" + " " * 62 + "║" + Colors.RESET)
            print(Colors.rgb(r, g, b) + "╚" + "═" * 62 + "╝" + Colors.RESET)

            # Status indicator
            dots = "." * ((frame % 4) + 1)
            print(
                f"\n{Colors.CYAN}Initializing{dots}{' ' * (3 - len(dots))}{Colors.RESET}"
            )

            time.sleep(1.0 / fps)

        # Final static frame
        print("\033[2J\033[H", end="")
        self.print_static()

    def print_minimal(self):
        """Print minimal banner for idle state."""
        primary = self.scheme["primary"]
        accent = self.scheme["accent"]

        # Compact header
        print(Colors.rgb(*primary) + "◢" + "━" * 40 + "◣" + Colors.RESET)

        # WANDA text with gradient
        text = "  WANDA AI OS  "
        colored = self._gradient_line(text, primary, accent)
        print(
            Colors.rgb(*primary)
            + "┃"
            + colored.center(40)
            + Colors.rgb(*primary)
            + "┃"
            + Colors.RESET
        )

        print(Colors.rgb(*primary) + "◥" + "━" * 40 + "◤" + Colors.RESET)


def print_banner(scheme="cyberpunk", animated=False, minimal=False):
    """Convenience function to print banner."""
    banner = WandaBanner(scheme=scheme)

    if minimal:
        banner.print_minimal()
    elif animated:
        banner.print_animated()
    else:
        banner.print_static()


def get_available_schemes():
    """Return list of available color schemes."""
    return list(WandaBanner.SCHEMES.keys())


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="WANDA Banner Generator")
    parser.add_argument(
        "--scheme",
        choices=get_available_schemes(),
        default="cyberpunk",
        help="Color scheme to use",
    )
    parser.add_argument("--animated", action="store_true", help="Show animated banner")
    parser.add_argument("--minimal", action="store_true", help="Show minimal banner")
    parser.add_argument(
        "--list-schemes", action="store_true", help="List available color schemes"
    )

    args = parser.parse_args()

    if args.list_schemes:
        print("Available color schemes:")
        for scheme in get_available_schemes():
            print(f"  - {scheme}")
    else:
        print_banner(scheme=args.scheme, animated=args.animated, minimal=args.minimal)
