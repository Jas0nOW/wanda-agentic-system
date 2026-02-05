"""LogWindow - GTK3 live event/transcript viewer for WANDA Voice."""

from __future__ import annotations
import time
from typing import Optional, Callable

try:
    import gi

    gi.require_version("Gtk", "3.0")
    from gi.repository import Gtk, Gdk, GLib, Pango

    GTK_AVAILABLE = True
except ImportError:
    GTK_AVAILABLE = False


class LogWindow:
    """GTK3 window showing live transcript, events, and controls.

    Subscribes to EventBus for real-time updates.
    """

    def __init__(
        self,
        on_send: Optional[Callable] = None,
        on_edit: Optional[Callable] = None,
        on_redo: Optional[Callable] = None,
        on_cancel: Optional[Callable] = None,
        on_readback: Optional[Callable] = None,
        on_toggle_refiner: Optional[Callable[[bool], None]] = None,
        refiner_enabled: bool = True,
    ):
        if not GTK_AVAILABLE:
            self.window = None
            return

        self.on_send = on_send
        self.on_edit = on_edit
        self.on_redo = on_redo
        self.on_cancel = on_cancel
        self.on_readback = on_readback
        self.on_toggle_refiner = on_toggle_refiner
        self.refiner_enabled = refiner_enabled

        self._build_ui()

    def _build_ui(self):
        """Build the GTK3 window."""
        self.window = Gtk.Window(title="WANDA Voice Log")
        self.window.set_default_size(500, 600)
        self.window.set_keep_above(False)
        self.window.set_deletable(True)
        self.window.connect("delete-event", self._on_delete)

        # Dark theme
        settings = Gtk.Settings.get_default()
        if settings:
            settings.set_property("gtk-application-prefer-dark-theme", True)

        # Main vertical box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        vbox.set_margin_start(8)
        vbox.set_margin_end(8)
        vbox.set_margin_top(8)
        vbox.set_margin_bottom(8)

        # Header
        header = Gtk.Label()
        header.set_markup("<b>WANDA Voice Log</b>")
        header.set_halign(Gtk.Align.START)
        vbox.pack_start(header, False, False, 0)

        # Status bar
        self.status_label = Gtk.Label(label="Status: Idle")
        self.status_label.set_halign(Gtk.Align.START)
        self.status_label.get_style_context().add_class("dim-label")
        vbox.pack_start(self.status_label, False, False, 0)

        # Toggle bar
        toggle_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        self.refiner_toggle = Gtk.CheckButton(label="Prompt-Verbesserer")
        self.refiner_toggle.set_active(self.refiner_enabled)
        self.refiner_toggle.connect("toggled", self._on_refiner_toggle)
        toggle_box.pack_start(self.refiner_toggle, False, False, 0)
        vbox.pack_start(toggle_box, False, False, 0)

        # Scrolled text view for transcript/events
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.set_vexpand(True)

        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD_CHAR)
        self.text_view.set_left_margin(6)
        self.text_view.set_right_margin(6)

        # Use monospace font
        font_desc = Pango.FontDescription("monospace 10")
        self.text_view.override_font(font_desc)

        # Text tags for coloring
        self.text_buffer = self.text_view.get_buffer()
        self.text_buffer.create_tag("transcript", foreground="#34d399")
        self.text_buffer.create_tag("improved", foreground="#60a5fa")
        self.text_buffer.create_tag("response", foreground="#fbbf24")
        self.text_buffer.create_tag("event", foreground="#9ca3af")
        self.text_buffer.create_tag("error", foreground="#f87171")
        self.text_buffer.create_tag("bold", weight=Pango.Weight.BOLD)

        scrolled.add(self.text_view)
        vbox.pack_start(scrolled, True, True, 0)

        # Button bar
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        send_btn = Gtk.Button(label="Senden")
        send_btn.connect("clicked", lambda _: self._call(self.on_send))
        send_btn.get_style_context().add_class("suggested-action")
        btn_box.pack_start(send_btn, True, True, 0)

        edit_btn = Gtk.Button(label="Bearbeiten")
        edit_btn.connect("clicked", lambda _: self._call(self.on_edit))
        btn_box.pack_start(edit_btn, True, True, 0)

        redo_btn = Gtk.Button(label="Nochmal")
        redo_btn.connect("clicked", lambda _: self._call(self.on_redo))
        btn_box.pack_start(redo_btn, True, True, 0)

        cancel_btn = Gtk.Button(label="Abbrechen")
        cancel_btn.connect("clicked", lambda _: self._call(self.on_cancel))
        cancel_btn.get_style_context().add_class("destructive-action")
        btn_box.pack_start(cancel_btn, True, True, 0)

        readback_btn = Gtk.Button(label="Vorlesen")
        readback_btn.connect("clicked", lambda _: self._call(self.on_readback))
        btn_box.pack_start(readback_btn, True, True, 0)

        vbox.pack_start(btn_box, False, False, 0)

        self.window.add(vbox)

    def _call(self, callback: Optional[Callable]) -> None:
        if callback:
            import threading

            threading.Thread(target=callback, daemon=True).start()

    def _on_refiner_toggle(self, widget) -> None:
        if self.on_toggle_refiner:
            enabled = bool(widget.get_active())
            self._call(lambda: self.on_toggle_refiner(enabled))

    def _on_delete(self, widget, event):
        """Hide instead of destroy on close."""
        self.window.hide()
        return True

    # --- Public API ---

    def show(self) -> None:
        if self.window:
            GLib.idle_add(self.window.show_all)

    def hide(self) -> None:
        if self.window:
            GLib.idle_add(self.window.hide)

    def set_status(self, text: str) -> None:
        if self.status_label:
            GLib.idle_add(self.status_label.set_text, f"Status: {text}")

    def append_transcript(self, text: str) -> None:
        self._append(f"[STT] {text}\n", "transcript")

    def append_improved(self, text: str) -> None:
        self._append(f"[Improved] {text}\n", "improved")

    def append_response(self, text: str) -> None:
        self._append(f"[Response] {text}\n", "response")

    def append_event(self, event_type: str, data: str = "") -> None:
        ts = time.strftime("%H:%M:%S")
        extra = f" - {data}" if data else ""
        self._append(f"[{ts}] {event_type}{extra}\n", "event")

    def append_error(self, text: str) -> None:
        self._append(f"[ERROR] {text}\n", "error")

    def _append(self, text: str, tag_name: str) -> None:
        """Thread-safe append to text buffer."""

        def do_append():
            end = self.text_buffer.get_end_iter()
            self.text_buffer.insert_with_tags_by_name(end, text, tag_name)
            # Auto-scroll
            end_mark = self.text_buffer.get_insert()
            self.text_view.scroll_to_mark(end_mark, 0, False, 0, 0)

        if self.text_buffer:
            GLib.idle_add(do_append)

    def clear(self) -> None:
        if self.text_buffer:
            GLib.idle_add(lambda: self.text_buffer.set_text(""))

    def destroy(self) -> None:
        if self.window:
            GLib.idle_add(self.window.destroy)

    # --- EventBus integration ---

    def on_event(self, event) -> None:
        """EventBus callback - route events to appropriate display."""
        etype = event.event_type
        data = event.data

        if etype == "stt.result":
            text = data.get("text", "")
            if text:
                self.append_transcript(text)
        elif etype == "refiner.result":
            self.append_improved(data.get("improved_text", ""))
        elif etype == "refiner.toggle":
            state = "on" if data.get("enabled") else "off"
            self.append_event("refiner.toggle", state)
        elif etype == "refiner.skipped":
            self.append_event("refiner.skipped", data.get("reason", ""))
        elif etype == "provider.response":
            self.append_response(f"via {data.get('provider', '?')}")
        elif etype == "state.change":
            self.set_status(data.get("new", "?"))
        elif etype == "error":
            self.append_error(data.get("message", "unknown"))
        else:
            self.append_event(etype, str(data)[:80])
