# Wanda Voice Assistant - Premium Visual Indicator
"""Premium Siri-style animated orb with fluid animations and click/drag separation."""

import math
import time
import threading
from typing import Optional, Callable

try:
    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gdk, GLib
    import cairo

    GTK_AVAILABLE = True
except ImportError:
    GTK_AVAILABLE = False
    print("[UI] GTK not available, visual indicator disabled")


class WandaOrb:
    """
    Premium Siri-style visual indicator orb.

    Features:
    - Fluid pulsing animation
    - Smooth color transitions
    - Particle effects for active states
    - Wave animation for speaking
    - Click vs drag detection (no accidental triggers)
    - Always-on-top, draggable
    """

    # Premium color palette with gradients
    COLORS = {
        "idle": {"primary": "#3b82f6", "secondary": "#1d4ed8", "glow": "#60a5fa"},
        "listening": {"primary": "#10b981", "secondary": "#059669", "glow": "#34d399"},
        "thinking": {"primary": "#f59e0b", "secondary": "#d97706", "glow": "#fbbf24"},
        "speaking": {"primary": "#8b5cf6", "secondary": "#7c3aed", "glow": "#a78bfa"},
        "paused": {"primary": "#6b7280", "secondary": "#4b5563", "glow": "#9ca3af"},
        "autonomous": {"primary": "#ef4444", "secondary": "#dc2626", "glow": "#f87171"},
    }

    # Minimum drag distance before it's considered a drag (not a click)
    DRAG_THRESHOLD = 8
    # Minimum hold time before drag mode activates (ms)
    HOLD_THRESHOLD_MS = 150

    def __init__(self, size: int = 70, on_click: Optional[Callable] = None):
        if not GTK_AVAILABLE:
            self.window = None
            return

        self.size = size
        self.on_click = on_click
        self.state = "idle"
        self.target_state = "idle"

        # Drag/click handling
        self.press_time = 0
        self.press_pos = None
        self.is_dragging = False

        # Animation state
        self.pulse = 0.0
        self.pulse_speed = 0.08
        self.color_transition = 0.0
        self.wave_phase = 0.0
        self.particles = []
        self.ring_rotation = 0.0

        # Current colors (for smooth transition)
        self.current_r = 0.23
        self.current_g = 0.51
        self.current_b = 0.96

        # Create window
        self._create_window()

    def _create_window(self):
        """Create the transparent window."""
        self.window = Gtk.Window(type=Gtk.WindowType.POPUP)
        self.window.set_decorated(False)
        self.window.set_keep_above(True)
        self.window.set_skip_taskbar_hint(True)
        self.window.set_skip_pager_hint(True)
        self.window.set_accept_focus(False)
        self.window.set_focus_on_map(False)
        try:
            self.window.set_type_hint(Gdk.WindowTypeHint.NOTIFICATION)
        except Exception:
            pass
        try:
            self.window.stick()
        except Exception:
            pass
        self.window.set_resizable(False)

        # Transparency
        screen = self.window.get_screen()
        visual = screen.get_rgba_visual()
        if visual:
            self.window.set_visual(visual)
        self.window.set_app_paintable(True)

        # Drawing area (larger for glow effects)
        draw_size = self.size + 40
        self.drawing_area = Gtk.DrawingArea()
        self.drawing_area.set_size_request(draw_size, draw_size)
        self.drawing_area.connect("draw", self._on_draw)

        # Events
        self.window.add_events(
            Gdk.EventMask.BUTTON_PRESS_MASK
            | Gdk.EventMask.BUTTON_RELEASE_MASK
            | Gdk.EventMask.POINTER_MOTION_MASK
        )
        self.window.connect("button-press-event", self._on_button_press)
        self.window.connect("button-release-event", self._on_button_release)
        self.window.connect("motion-notify-event", self._on_motion)

        self.window.add(self.drawing_area)
        self.window.set_size_request(draw_size, draw_size)

        # Position: bottom-right corner
        self._position_window()

    def _position_window(self):
        """Position window in bottom-right corner."""
        try:
            display = Gdk.Display.get_default()
            monitor = display.get_primary_monitor()
            if monitor:
                geometry = monitor.get_geometry()
                x = geometry.width - self.size - 60
                y = geometry.height - self.size - 120
                self.window.move(x, y)
        except:
            self.window.move(1800, 900)  # Fallback

    def show(self):
        """Show the orb."""
        if self.window:
            GLib.idle_add(self._show)

    def _show(self):
        self.window.show_all()
        self._ensure_foreground()
        GLib.timeout_add(2000, self._ensure_foreground)
        self._start_animation()
        return False

    def _ensure_foreground(self):
        if self.window:
            try:
                self.window.set_keep_above(True)
            except Exception:
                pass
        return True

    def hide(self):
        """Hide the orb."""
        if self.window:
            GLib.idle_add(self.window.hide)

    def set_state(self, state: str):
        """Set orb state with smooth transition."""
        if state in self.COLORS:
            self.target_state = state
            # Add particles on state change
            if state != self.state and state in ["listening", "thinking", "autonomous"]:
                self._spawn_particles(8)
            self.state = state
        if self.window:
            GLib.idle_add(self.drawing_area.queue_draw)

    def _spawn_particles(self, count: int):
        """Spawn celebration particles."""
        import random

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            self.particles.append(
                {
                    "x": 0,
                    "y": 0,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": 1.0,
                    "size": random.uniform(2, 5),
                }
            )

    def _hex_to_rgb(self, hex_color: str) -> tuple:
        """Convert hex color to RGB tuple (0-1 range)."""
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) / 255 for i in (0, 2, 4))

    def _on_draw(self, widget, cr):
        """Draw the premium orb."""
        width = widget.get_allocated_width()
        height = widget.get_allocated_height()
        cx, cy = width / 2, height / 2
        radius = self.size / 2 - 5

        # Get colors
        colors = self.COLORS.get(self.state, self.COLORS["idle"])
        primary = self._hex_to_rgb(colors["primary"])
        secondary = self._hex_to_rgb(colors["secondary"])
        glow = self._hex_to_rgb(colors["glow"])

        # Smooth color transition
        self.current_r += (primary[0] - self.current_r) * 0.1
        self.current_g += (primary[1] - self.current_g) * 0.1
        self.current_b += (primary[2] - self.current_b) * 0.1

        # Clear background
        cr.set_operator(cairo.OPERATOR_SOURCE)
        cr.set_source_rgba(0, 0, 0, 0)
        cr.paint()
        cr.set_operator(cairo.OPERATOR_OVER)

        # Dynamic pulse based on state
        if self.state == "listening":
            pulse_intensity = 0.15 + 0.1 * math.sin(self.pulse * 3)
        elif self.state == "thinking":
            pulse_intensity = 0.1 * abs(math.sin(self.pulse * 2))
        elif self.state == "speaking":
            pulse_intensity = 0.12 * abs(math.sin(self.wave_phase * 4))
        elif self.state == "autonomous":
            pulse_intensity = 0.08 * abs(math.sin(self.pulse * 5))
        else:
            pulse_intensity = 0.05 * abs(math.sin(self.pulse))

        # Outer glow (multiple layers)
        for i in range(3):
            glow_radius = radius + 15 + i * 8 + pulse_intensity * 20
            alpha = 0.15 - i * 0.04
            cr.set_source_rgba(glow[0], glow[1], glow[2], alpha)
            cr.arc(cx, cy, glow_radius, 0, 2 * math.pi)
            cr.fill()

        # Rotating ring for active states
        if self.state in ["listening", "thinking", "autonomous"]:
            cr.save()
            cr.translate(cx, cy)
            cr.rotate(self.ring_rotation)
            cr.translate(-cx, -cy)

            for i in range(6):
                angle = i * (math.pi / 3) + self.ring_rotation
                ring_x = cx + math.cos(angle) * (radius + 8)
                ring_y = cy + math.sin(angle) * (radius + 8)
                cr.set_source_rgba(glow[0], glow[1], glow[2], 0.6)
                cr.arc(ring_x, ring_y, 3, 0, 2 * math.pi)
                cr.fill()

            cr.restore()

        # Wave effect for speaking
        if self.state == "speaking":
            for i in range(3):
                wave_r = radius + 5 + i * 12 + 8 * math.sin(self.wave_phase + i * 0.5)
                alpha = 0.3 - i * 0.1
                cr.set_source_rgba(
                    self.current_r, self.current_g, self.current_b, alpha
                )
                cr.set_line_width(2)
                cr.arc(cx, cy, wave_r, 0, 2 * math.pi)
                cr.stroke()

        # Main orb with gradient
        gradient = cairo.RadialGradient(
            cx - radius / 3, cy - radius / 3, 0, cx, cy, radius
        )
        gradient.add_color_stop_rgba(0, glow[0], glow[1], glow[2], 1.0)
        gradient.add_color_stop_rgba(
            0.5, self.current_r, self.current_g, self.current_b, 0.95
        )
        gradient.add_color_stop_rgba(1, secondary[0], secondary[1], secondary[2], 0.9)

        # Pulsing radius
        pulse_radius = radius * (1 + pulse_intensity * 0.15)
        cr.set_source(gradient)
        cr.arc(cx, cy, pulse_radius, 0, 2 * math.pi)
        cr.fill()

        # Glass highlight
        highlight = cairo.LinearGradient(
            cx - radius, cy - radius, cx + radius, cy + radius
        )
        highlight.add_color_stop_rgba(0, 1, 1, 1, 0.4)
        highlight.add_color_stop_rgba(0.5, 1, 1, 1, 0.1)
        highlight.add_color_stop_rgba(1, 1, 1, 1, 0)
        cr.set_source(highlight)
        cr.arc(cx, cy, pulse_radius, 0, 2 * math.pi)
        cr.fill()

        # Inner highlight dot
        cr.set_source_rgba(1, 1, 1, 0.6)
        cr.arc(cx - radius / 3, cy - radius / 3, radius / 5, 0, 2 * math.pi)
        cr.fill()

        # Draw particles
        for p in self.particles:
            alpha = p["life"]
            cr.set_source_rgba(glow[0], glow[1], glow[2], alpha)
            cr.arc(cx + p["x"], cy + p["y"], p["size"] * p["life"], 0, 2 * math.pi)
            cr.fill()

        return False

    def _on_button_press(self, widget, event):
        """Handle button press - record position and time."""
        if event.button == 1:
            self.press_time = time.time() * 1000
            self.press_pos = (event.x_root, event.y_root)
            self.is_dragging = False
        return True

    def _on_button_release(self, widget, event):
        """Handle button release - determine if click or drag."""
        if event.button == 1 and self.press_pos:
            dx = abs(event.x_root - self.press_pos[0])
            dy = abs(event.y_root - self.press_pos[1])
            elapsed = time.time() * 1000 - self.press_time

            # It's a click if:
            # 1. Movement is below threshold AND
            # 2. We weren't in drag mode
            if (
                dx < self.DRAG_THRESHOLD
                and dy < self.DRAG_THRESHOLD
                and not self.is_dragging
            ):
                if self.on_click:
                    # Run callback in thread to not block
                    threading.Thread(target=self.on_click, daemon=True).start()

            self.press_pos = None
            self.is_dragging = False
        return True

    def _on_motion(self, widget, event):
        """Handle drag motion."""
        if self.press_pos:
            dx = abs(event.x_root - self.press_pos[0])
            dy = abs(event.y_root - self.press_pos[1])
            elapsed = time.time() * 1000 - self.press_time

            # Enter drag mode if moved enough OR held long enough
            if (
                dx > self.DRAG_THRESHOLD
                or dy > self.DRAG_THRESHOLD
                or elapsed > self.HOLD_THRESHOLD_MS
            ):
                self.is_dragging = True

            if self.is_dragging:
                x, y = self.window.get_position()
                new_x = int(x + event.x_root - self.press_pos[0])
                new_y = int(y + event.y_root - self.press_pos[1])
                self.window.move(new_x, new_y)
                self.press_pos = (event.x_root, event.y_root)
        return True

    def _start_animation(self):
        """Start the animation loop."""

        def animate():
            if not self.window or not self.window.get_visible():
                return False

            # Update pulse
            self.pulse += self.pulse_speed
            if self.pulse > 2 * math.pi:
                self.pulse -= 2 * math.pi

            # Update wave phase
            self.wave_phase += 0.15

            # Update ring rotation
            if self.state in ["listening", "thinking", "autonomous"]:
                speed = 0.05 if self.state == "thinking" else 0.08
                if self.state == "autonomous":
                    speed = 0.12
                self.ring_rotation += speed

            # Update particles
            for p in self.particles[:]:
                p["x"] += p["vx"]
                p["y"] += p["vy"]
                p["life"] -= 0.03
                if p["life"] <= 0:
                    self.particles.remove(p)

            self.drawing_area.queue_draw()
            return True

        GLib.timeout_add(33, animate)  # ~30 FPS

    def destroy(self):
        """Cleanup."""
        if self.window:
            GLib.idle_add(self.window.destroy)


def run_gtk_main():
    """Run GTK main loop in separate thread."""
    if GTK_AVAILABLE:
        Gtk.main()


def quit_gtk():
    """Quit GTK main loop."""
    if GTK_AVAILABLE:
        GLib.idle_add(Gtk.main_quit)


if __name__ == "__main__":
    if GTK_AVAILABLE:

        def on_click():
            print("✨ Orb clicked!")

        orb = WandaOrb(size=70, on_click=on_click)
        orb.show()

        # Demo state changes
        def demo():
            states = [
                "listening",
                "thinking",
                "speaking",
                "autonomous",
                "paused",
                "idle",
            ]
            for state in states:
                time.sleep(3)
                print(f"State: {state}")
                GLib.idle_add(lambda s=state: orb.set_state(s))

        threading.Thread(target=demo, daemon=True).start()
        Gtk.main()
    else:
        print("GTK not available")
