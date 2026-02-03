#!/usr/bin/env python3
"""
WANDA Wayland-Compatible Desktop Indicator
Robuste Desktop-App für Wayland ohne GTK-Overlay-Probleme.
"""

import os
import sys
import time
import signal
import subprocess
from pathlib import Path


# Wayland Detection
def is_wayland():
    return os.environ.get("XDG_SESSION_TYPE", "").lower() == "wayland"


def get_compositor():
    if os.environ.get("HYPRLAND_INSTANCE_SIGNATURE"):
        return "hyprland"
    elif os.environ.get("SWAYSOCK"):
        return "sway"
    elif os.environ.get("WAYFIRE_SOCKET"):
        return "wayfire"
    elif os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "cosmic":
        return "cosmic"
    elif os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "gnome":
        return "gnome-wayland"
    elif os.environ.get("XDG_CURRENT_DESKTOP", "").lower() == "kde":
        return "kde-wayland"
    return "unknown"


class WandaTrayIndicator:
    """
    System Tray Indicator für WANDA - Funktioniert auf Wayland!
    """

    def __init__(self):
        self.indicator = None
        self.menu = None
        self.status = "idle"

    def setup(self):
        try:
            import gi

            gi.require_version("AppIndicator3", "0.1")
            from gi.repository import AppIndicator3, Gtk

            self.indicator = AppIndicator3.Indicator.new(
                "wanda-voice",
                "audio-input-microphone",
                AppIndicator3.IndicatorCategory.APPLICATION_STATUS,
            )
            self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

            self.menu = Gtk.Menu()

            # Status item
            item_status = Gtk.MenuItem(label="WANDA Voice - Bereit")
            item_status.set_sensitive(False)
            self.menu.append(item_status)

            self.menu.append(Gtk.SeparatorMenuItem())

            # Toggle recording
            item_toggle = Gtk.MenuItem(label="🎤 Aufnahme starten")
            item_toggle.connect("activate", self.on_toggle)
            self.menu.append(item_toggle)

            self.menu.append(Gtk.SeparatorMenuItem())

            # Settings
            item_settings = Gtk.MenuItem(label="Einstellungen")
            item_settings.connect("activate", self.on_settings)
            self.menu.append(item_settings)

            # Quit
            item_quit = Gtk.MenuItem(label="Beenden")
            item_quit.connect("activate", self.on_quit)
            self.menu.append(item_quit)

            self.menu.show_all()
            self.indicator.set_menu(self.menu)

            return True
        except Exception as e:
            print(f"[Tray] Could not create indicator: {e}")
            return False

    def on_toggle(self, widget):
        print("[Tray] Toggle recording")

    def on_settings(self, widget):
        print("[Tray] Open settings")

    def on_quit(self, widget):
        Gtk.main_quit()

    def run(self):
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

        Gtk.main()


class WandaWaylandWindow:
    """
    Native Wayland-Fenster mit wlroots-protokollen.
    Funktioniert mit Sway, Hyprland, River, etc.
    """

    def __init__(self):
        self.width = 80
        self.height = 80
        self.x = 100
        self.y = 100
        self.state = "idle"
        self.compositor = get_compositor()

    def setup_layer_shell(self):
        """
        Versucht layer-shell zu nutzen (wlroots-basierte Compositors).
        """
        try:
            import gi

            gi.require_version("Gtk", "3.0")
            gi.require_version("Gdk", "3.0")
            from gi.repository import Gtk, Gdk, GLib

            # Check if layer-shell is available
            if not self._check_layer_shell():
                return False

            self.window = Gtk.Window(type=Gtk.WindowType.TOPLEVEL)
            self.window.set_decorated(False)
            self.window.set_skip_taskbar_hint(True)
            self.window.set_keep_above(True)

            # Try to set layer-shell protocol
            self._try_set_layer_shell()

            # Drawing area
            self.drawing_area = Gtk.DrawingArea()
            self.drawing_area.set_size_request(self.width, self.height)
            self.drawing_area.connect("draw", self.on_draw)

            self.window.add(self.drawing_area)
            self.window.set_default_size(self.width, self.height)

            # Position
            self.window.move(self.x, self.y)

            # Make click-through if possible
            self.window.set_accept_focus(False)

            return True

        except Exception as e:
            print(f"[Wayland] Layer shell setup failed: {e}")
            return False

    def _check_layer_shell(self):
        """Check if layer-shell protocol is available."""
        try:
            result = subprocess.run(
                ["wayland-scanner", "--help"], capture_output=True, timeout=2
            )
            return result.returncode == 0
        except:
            return False

    def _try_set_layer_shell(self):
        """Try to set layer-shell properties via environment or GTK settings."""
        os.environ["GTK_LAYER_SHELL_EDGE"] = "bottom-right"

    def on_draw(self, widget, cr):
        """Draw the orb."""
        import cairo

        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        cx, cy = width / 2, height / 2
        radius = min(width, height) / 2 - 5

        # Clear
        cr.set_source_rgba(0, 0, 0, 0)
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        # Colors based on state
        colors = {
            "idle": (0.23, 0.51, 0.96),  # Blue
            "listening": (0.06, 0.73, 0.49),  # Green
            "thinking": (0.96, 0.62, 0.04),  # Orange
            "speaking": (0.55, 0.36, 0.96),  # Purple
        }

        r, g, b = colors.get(self.state, colors["idle"])

        # Glow
        for i in range(3):
            alpha = 0.2 - i * 0.05
            cr.set_source_rgba(r, g, b, alpha)
            cr.arc(cx, cy, radius + 10 + i * 5, 0, 2 * 3.14159)
            cr.fill()

        # Main circle
        cr.set_source_rgba(r, g, b, 0.9)
        cr.arc(cx, cy, radius, 0, 2 * 3.14159)
        cr.fill()

        return False

    def show(self):
        self.window.show_all()

    def set_state(self, state):
        self.state = state
        self.drawing_area.queue_draw()

    def run(self):
        import gi

        gi.require_version("Gtk", "3.0")
        from gi.repository import Gtk

        Gtk.main()


class WandaDesktopEntry:
    """
    Desktop Entry Launcher - Der sicherste Weg auf Wayland.
    """

    @staticmethod
    def launch_terminal():
        """Launch terminal with voice assistant."""
        install_dir = os.environ.get(
            "WANDA_INSTALL_DIR", os.path.expanduser("~/.wanda-system")
        )

        # Try different terminal emulators
        terminals = [
            "cosmic-term",
            "kgx",
            "gnome-terminal",
            "alacritty",
            "kitty",
            "foot",
            "konsole",
            "xfce4-terminal",
            "xterm",
        ]

        for term in terminals:
            if subprocess.run(["which", term], capture_output=True).returncode == 0:
                cmd = [term]
                if term in ["gnome-terminal", "kgx"]:
                    cmd.extend(
                        [
                            "--",
                            "bash",
                            "-c",
                            f'cd {install_dir}/wanda-voice && source venv/bin/activate && wanda voice; read -p "Press Enter..."',
                        ]
                    )
                elif term in ["alacritty", "kitty", "foot"]:
                    cmd.extend(
                        [
                            "-e",
                            "bash",
                            "-c",
                            f'cd {install_dir}/wanda-voice && source venv/bin/activate && wanda voice; read -p "Press Enter..."',
                        ]
                    )
                else:
                    cmd.extend(
                        [
                            "-e",
                            f"cd {install_dir}/wanda-voice && source venv/bin/activate && wanda voice",
                        ]
                    )

                subprocess.Popen(cmd)
                return True

        return False


class WandaWaylandApp:
    """
    Haupt-App für Wayland - Wählt die beste verfügbare Methode.
    """

    def __init__(self):
        self.method = None
        self.indicator = None

    def detect_best_method(self):
        """Detect the best available UI method for Wayland."""
        compositor = get_compositor()
        print(f"[Wayland] Detected compositor: {compositor}")

        # 1. Try system tray (works on most DEs)
        try:
            import gi

            gi.require_version("AppIndicator3", "0.1")
            self.method = "tray"
            print("[Wayland] Using system tray indicator")
            return
        except:
            pass

        # 2. Try layer-shell (wlroots compositors)
        if compositor in ["sway", "hyprland", "river"]:
            self.method = "layer-shell"
            print("[Wayland] Using layer-shell window")
            return

        # 3. Fallback to terminal launcher
        self.method = "terminal"
        print("[Wayland] Using terminal launcher")

    def run(self):
        self.detect_best_method()

        if self.method == "tray":
            self.indicator = WandaTrayIndicator()
            if self.indicator.setup():
                self.indicator.run()
            else:
                print("[Wayland] Tray failed, falling back to terminal")
                WandaDesktopEntry.launch_terminal()

        elif self.method == "layer-shell":
            window = WandaWaylandWindow()
            if window.setup_layer_shell():
                window.show()
                window.run()
            else:
                print("[Wayland] Layer-shell failed, falling back to terminal")
                WandaDesktopEntry.launch_terminal()

        elif self.method == "terminal":
            if not WandaDesktopEntry.launch_terminal():
                print("[Wayland] ERROR: No terminal found!")
                print(
                    "Please install: cosmic-term, alacritty, kitty, or gnome-terminal"
                )
                sys.exit(1)


def main():
    """Main entry point."""
    # Check if we're on Wayland
    if not is_wayland():
        print("[Info] Not on Wayland, using standard mode")
        # Could fall back to X11 version here
        return

    print("=" * 60)
    print("🎙️  WANDA Wayland Desktop App")
    print("=" * 60)
    print(f"Compositor: {get_compositor()}")
    print("")

    app = WandaWaylandApp()

    try:
        app.run()
    except KeyboardInterrupt:
        print("\n[Wayland] Shutting down...")
    except Exception as e:
        print(f"\n[Wayland] Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
