#!/usr/bin/env python3
# Wanda Voice Assistant - Full Main Loop (v2.0)
"""Complete Wanda with all 3 modes: Aktiv, CLI-Proxy, Autonomous.
Now delegates core pipeline to wanda_voice_core.WandaVoiceEngine."""

import sys
import time
import asyncio
import argparse
import os
import atexit
import fcntl
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

# Core imports
from config.config import Config
from audio.recorder import AudioRecorder, HotkeyHandler
from stt.faster_whisper_engine import FasterWhisperEngine

# TTS Engines
try:
    from tts.edge_tts_engine import EdgeTTSEngine

    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False

from tts.piper_engine import PiperEngine

# Wanda Voice Core (v2.0 engine)
CORE_AVAILABLE = False
try:
    from wanda_voice_core.engine import WandaVoiceEngine
    from wanda_voice_core.config import VoiceCoreConfig
    from wanda_voice_core.providers.gemini_cli import GeminiCLIProvider
    from wanda_voice_core.providers.ollama import OllamaProvider
    from wanda_voice_core.schemas import ConfirmationState, RouteType

    CORE_AVAILABLE = True
except ImportError as e:
    print(f"[Wanda] Core engine not available: {e}")

# Wanda Phase 2+3 imports (optional UI/mode components)
FULL_MODE = False
GTK_AVAILABLE = False
WAKE_WORD_AVAILABLE = False
MOBILE_AVAILABLE = False

try:
    from audio.silero_vad import get_vad
    from audio.interrupt_controller import InterruptController
    from conversation.command_detector import ConversationalCommandDetector
    from conversation.wanda_prompts import get_wanda_prompt
    from conversation.state_machine import StateMachine, WandaMode
    from conversation.context_manager import ContextManager
    from conversation.briefing import BriefingGenerator
    from conversation.intelligence import WorkflowEngine
    from adapters.ollama_manager import OllamaManager, create_ollama_manager
    from adapters.cli_proxy import CLIProxy
    from modes.autonomous import AutonomousController
    from modes.daily_init import DailyInitializer
    from preprocess.guardrails import Guardrails
    from ui.sounds import SoundFeedback
    from ui.orb import WandaOrb, run_gtk_main, quit_gtk, GTK_AVAILABLE

    FULL_MODE = True
except ImportError as e:
    print(f"[Wanda] Full mode modules missing: {e}")

try:
    from ui.log_window import LogWindow

    LOG_WINDOW_AVAILABLE = GTK_AVAILABLE
except ImportError:
    LOG_WINDOW_AVAILABLE = False

try:
    from audio.wake_word import get_wake_word_detector

    WAKE_WORD_AVAILABLE = True
except ImportError:
    WAKE_WORD_AVAILABLE = False

try:
    from mobile.telegram_bot import create_telegram_bot
    from mobile.notifier import WandaNotifier
    from mobile.project_init import ProjectInitializer

    MOBILE_AVAILABLE = True
except ImportError:
    MOBILE_AVAILABLE = False

BaseCommandDetector = None
COMMAND_DETECTOR_AVAILABLE = False
try:
    from conversation.command_detector import (
        ConversationalCommandDetector as BaseCommandDetector,
    )

    COMMAND_DETECTOR_AVAILABLE = True
except ImportError:
    COMMAND_DETECTOR_AVAILABLE = False

# Single instance lock
LOCK_PATH = "/tmp/wanda-voice.lock"
PID_PATH = "/tmp/wanda-voice.pid"
_lock_handle = None


def _release_instance_lock():
    global _lock_handle
    try:
        if _lock_handle:
            fcntl.flock(_lock_handle, fcntl.LOCK_UN)
            _lock_handle.close()
            _lock_handle = None
    except Exception:
        pass
    try:
        os.remove(PID_PATH)
    except FileNotFoundError:
        pass
    except Exception:
        pass


def acquire_single_instance() -> bool:
    """Prevent multiple voice instances."""
    global _lock_handle
    try:
        _lock_handle = open(LOCK_PATH, "w")
        fcntl.flock(_lock_handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        print("[Wanda] Voice already running. Exiting.")
        return False
    except Exception as e:
        print(f"[Wanda] Warning: cannot lock instance ({e}).")
        return True

    try:
        _lock_handle.write(str(os.getpid()))
        _lock_handle.flush()
    except Exception:
        pass

    try:
        with open(PID_PATH, "w") as f:
            f.write(str(os.getpid()))
    except Exception:
        pass

    atexit.register(_release_instance_lock)
    return True


class WandaVoiceAssistant:
    """Wanda Voice Assistant - v2.0 with WandaVoiceEngine integration."""

    def __init__(self, config_path=None, daemon=False):
        print("=" * 70)
        print("  WANDA - SOVEREIGN AI VOICE ASSISTANT v2.0")
        print("=" * 70)

        self.config = Config(config_path)
        self.daemon = daemon
        self.stt_tts_only = self.config.get("pipeline.stt_tts_only", False)
        self.speak_transcript = self.config.get("pipeline.speak_transcript", True)
        self.transcript_prefix = self.config.get("pipeline.transcript_prefix", "")
        self.always_listening = self.config.get("listening.always_on", False)
        self.last_response = None
        self.refiner_enabled = self.config.get("refiner.enabled", True)

        # Core audio/STT/TTS (stays in frontend - platform-specific)
        self._init_core()

        # WandaVoiceEngine (v2.0 pipeline)
        self.engine = None
        if CORE_AVAILABLE and not self.stt_tts_only:
            self._init_engine()

        # Defaults for optional components
        self.wake_word = None
        self.state = None
        self.commands = BaseCommandDetector() if COMMAND_DETECTOR_AVAILABLE else None
        self.guardrails = None
        self.sounds = None
        self.context = None
        self.workflows = None
        self.cli_proxy = None
        self.briefing = None
        self.autonomous = None
        self.daily_init = None
        self.orb = None
        self.log_window = None

        class _DisabledOllama:
            available = False

            def cleanup(self):
                return None

        self.ollama = _DisabledOllama()

        # Phase 2+3 (UI and mode components)
        if FULL_MODE:
            self._init_wanda()
            self._init_phase3()

        # State
        self.running = False
        self.is_recording = False
        self._shutting_down = False
        self._processing = False

        # Async event loop for engine calls
        self._loop = asyncio.new_event_loop()
        self._loop_thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._loop_thread.start()

        # Hotkey
        self.hotkey = HotkeyHandler(
            key=self.config.get("trigger.key", "rightctrl"),
            mode=self.config.get("trigger.mode", "toggle"),
            on_toggle=self.toggle_recording,
            on_press=self.start_recording,
            on_release=self.stop_recording,
        )

        print("\n[Wanda] Fully initialized")

    def _init_core(self):
        """Core MVP components (audio, STT, TTS)."""
        self.recorder = AudioRecorder(
            sample_rate=self.config.audio_config.get("sample_rate", 16000),
            max_seconds=self.config.audio_config.get("max_seconds", 60),
            silence_timeout=self.config.audio_config.get("silence_timeout", 1.2),
            silence_threshold=self.config.audio_config.get("silence_threshold", 0.01),
            min_seconds=self.config.audio_config.get("min_seconds", 1.0),
            min_speech_ms=self.config.audio_config.get("min_speech_ms", 200),
            hangover_frames=self.config.audio_config.get("hangover_frames", 5),
            on_auto_stop=self._auto_stop,
        )
        self.stt = FasterWhisperEngine(
            model_name=self.config.stt.get("model", "large-v3-turbo"),
            device=self.config.stt.get("device", "auto"),
        )
        tts_engine = self.config.tts.get("engine", "edge")
        tts_voice = self.config.tts.get("voice", "katja")
        tts_mode = self.config.tts.get("mode", "short")

        if tts_engine == "edge" and EDGE_TTS_AVAILABLE:
            self.tts = EdgeTTSEngine(voice=tts_voice)
            self.tts.mode = tts_mode
        else:
            piper_voice = self.config.tts.get("voice", "de_DE-kerstin-low")
            if not piper_voice.startswith("de_DE"):
                piper_voice = "de_DE-kerstin-low"
            self.tts = PiperEngine(voice=piper_voice, mode=tts_mode)

    def _init_engine(self):
        """Initialize WandaVoiceEngine with providers."""
        core_config = VoiceCoreConfig()
        self.engine = WandaVoiceEngine(core_config)

        # Setup providers
        primary = GeminiCLIProvider(
            model=self.config.get("adapters.gemini_model", "flash"),
            timeout=self.config.get("adapters.timeout", 90),
        )
        fallback = None
        if self.config.get("ollama.enabled", False):
            ollama_model = self.config.get("ollama.model", "qwen3:8b")
            fallback = OllamaProvider(model=ollama_model)

        self.engine.set_providers(primary, fallback)

        # Apply refiner default
        self.engine.set_refiner_enabled(self.refiner_enabled)

        # Wire TTS/STT for confirmation flow
        self.engine.set_io(
            tts_speak=lambda text: self._speak(text),
            stt_listen=lambda: self._listen_short(),
        )

        # Subscribe to EventBus for Orb/LogWindow updates
        self.engine.event_bus.subscribe("*", self._on_engine_event)

        print("[Wanda] Engine v2.0 initialized")

    def _init_wanda(self):
        """Phase 2 Wanda components."""
        vad_engine = self.config.audio_config.get("vad_engine", "silero")
        self.vad = get_vad(
            vad_engine,
            silence_duration=self.config.audio_config.get("silence_timeout", 1.2),
        )
        try:
            self.recorder.set_vad(self.vad)
        except Exception:
            pass
        self.interrupt = InterruptController(self.vad, self.tts)
        self.commands = ConversationalCommandDetector()
        self.guardrails = Guardrails(
            enabled=self.config.get("security.redact_secrets", False)
        )
        self.sounds = SoundFeedback(
            enabled=self.config.get("output.sounds_enabled", True)
        )

    def _init_phase3(self):
        """Phase 3 Multi-Mode components."""
        self.state = StateMachine(on_mode_change=self._on_mode_change)

        self.context = ContextManager(
            max_messages_per_window=self.config.get("context.max_messages", 20),
            max_windows=5,
        )

        ollama_enabled = self.config.get("ollama.enabled", False)
        if ollama_enabled:
            ollama_model = self.config.get("ollama.model", "")
            if ollama_model:
                self.ollama = OllamaManager(
                    model=ollama_model, auto_unload=True, unload_timeout=120
                )
            else:
                self.ollama = type("DisabledOllama", (), {"available": False})()
        else:
            self.ollama = type("DisabledOllama", (), {"available": False})()

        self.cli_proxy = CLIProxy(on_output=self._on_cli_output)
        self.briefing = BriefingGenerator()
        self.briefing.ollama = self.ollama if self.ollama.available else None

        self.autonomous = AutonomousController(
            cli_proxy=self.cli_proxy,
            ollama=self.ollama if self.ollama.available else None,
            on_progress=lambda msg: self._speak(msg),
            on_complete=lambda msg: self._speak(msg),
        )

        self.workflows = WorkflowEngine()

        # Visual Orb Indicator
        self.orb = None
        if GTK_AVAILABLE:
            self.orb = WandaOrb(size=60, on_click=self._on_orb_click)
            self.gtk_thread = threading.Thread(target=run_gtk_main, daemon=True)
            self.gtk_thread.start()

        # LogWindow (new in v2.0)
        self.log_window = None
        if LOG_WINDOW_AVAILABLE and self.config.get("ui.log_window", True):
            self.log_window = LogWindow(
                on_send=lambda: self._confirmation_override("send"),
                on_edit=lambda: self._confirmation_override("edit"),
                on_redo=lambda: self._confirmation_override("redo"),
                on_cancel=lambda: self._confirmation_override("cancel"),
                on_readback=lambda: self._speak(
                    self.last_response or "Keine letzte Antwort."
                ),
                on_toggle_refiner=self._toggle_refiner,
                refiner_enabled=self.refiner_enabled,
            )

        self.daily_init = DailyInitializer(
            briefing=self.briefing,
            ollama=self.ollama if self.ollama.available else None,
            speak_callback=lambda msg: self._speak(msg),
            orb_callback=lambda state: self.orb.set_state(state) if self.orb else None,
        )

        self.wake_word = None
        if WAKE_WORD_AVAILABLE and self.config.get("wake_word.enabled", False):
            wake_words = self.config.get("wake_word.words", None)
            threshold = self.config.get("wake_word.threshold", 0.5)
            self.wake_word = get_wake_word_detector(
                on_wake=self._on_wake_word,
                stt_engine=self.stt,
                wake_words=wake_words,
                threshold=threshold,
            )

        self.notifier = None
        self.project_init = None
        self.telegram_bot = None

        if MOBILE_AVAILABLE:
            if self.config.get("notifications.enabled", False):
                self.notifier = WandaNotifier(
                    topic=self.config.get("notifications.topic", "wanda-private"),
                    server=self.config.get("notifications.server", "https://ntfy.sh"),
                    enabled=True,
                )
            self.project_init = ProjectInitializer(
                ollama=self.ollama if self.ollama.available else None,
                notifier=self.notifier,
            )
            if self.config.get("telegram.enabled", False):
                self.telegram_bot = create_telegram_bot(
                    self.config._config,
                    stt_engine=self.stt,
                    tts_engine=self.tts,
                    gemini_adapter=None,
                    ollama_adapter=self.ollama,
                    project_init=self.project_init,
                    notifier=self.notifier,
                )

    def _confirmation_override(self, action: str):
        """Handle confirmation override from LogWindow buttons."""
        if not self.engine:
            return
        mapping = {
            "send": ConfirmationState.SEND,
            "edit": ConfirmationState.EDIT,
            "redo": ConfirmationState.REDO,
            "cancel": ConfirmationState.CANCEL,
        }
        state = mapping.get(action)
        if state:
            self.engine.override_confirmation(state)
            print(f"[Wanda] UI override: {action}")

    def _toggle_refiner(self, enabled: bool) -> None:
        if not self.engine:
            return
        self.engine.set_refiner_enabled(enabled)
        self.refiner_enabled = enabled

    def _on_engine_event(self, event):
        """Handle events from WandaVoiceEngine."""
        etype = event.event_type
        data = event.data

        # Update Orb
        if self.orb:
            state_map = {
                "recording.start": "listening",
                "recording.stop": "thinking",
                "stt.result": "thinking",
                "provider.request": "thinking",
                "provider.response": "speaking",
                "tts.start": "speaking",
                "tts.stop": "idle",
                "run.end": "idle",
                "error": "idle",
            }
            if etype in state_map:
                self.orb.set_state(state_map[etype])

        # Update LogWindow
        if self.log_window:
            self.log_window.on_event(event)

    def _on_mode_change(self, old_mode, new_mode):
        """Handle mode transitions."""
        print(f"[Wanda] Mode: {old_mode.name} -> {new_mode.name}")
        if new_mode == WandaMode.AKTIV and self.wake_word:
            try:
                self.wake_word.reset()
            except Exception:
                pass
        if self.orb:
            state_map = {
                WandaMode.AKTIV: "idle",
                WandaMode.PAUSED: "paused",
                WandaMode.AUTONOMOUS: "autonomous",
                WandaMode.CLI_PROXY: "thinking",
            }
            self.orb.set_state(state_map.get(new_mode, "idle"))

    def _on_cli_output(self, output: str):
        if self.config.get("output.speak", True):
            self._speak(output, mode="short")

    def _on_wake_word(self):
        if not self.state:
            self.toggle_recording()
            return
        if self.state.is_paused():
            response = self.state.transition(WandaMode.AKTIV)
            self._speak(response)
        elif not self.is_recording:
            self._on_orb_click()

    def _on_orb_click(self):
        if self.state and self.state.is_paused():
            response = self.state.transition(WandaMode.AKTIV)
            self._speak(response)
            return
        if FULL_MODE and self.daily_init and self.daily_init.is_first_session_today():
            threading.Thread(
                target=self.daily_init.run_daily_start, daemon=True
            ).start()
            return
        self.toggle_recording()

    def start_recording(self):
        if self.state and self.state.is_paused():
            return
        if self.is_recording:
            return
        if FULL_MODE:
            self.sounds.trigger()
            if self.orb:
                self.orb.set_state("listening")
        self.recorder.start_recording()
        self.is_recording = True
        print("\n[Wanda] Recording...")

    def stop_recording(self):
        if not self.is_recording:
            return
        self.is_recording = False
        audio = self.recorder.stop_recording()
        if audio is not None:
            threading.Thread(target=self._process, args=(audio,)).start()

    def toggle_recording(self):
        if self.is_recording:
            self.stop_recording()
        else:
            self.start_recording()

    def _process(self, audio):
        """Main processing pipeline - delegates to WandaVoiceEngine."""
        self._processing = True
        try:
            # 1. Transcribe
            text = self.stt.transcribe(audio, language="de")
            if not text:
                print("[Wanda] No speech detected")
                if FULL_MODE and self.orb:
                    self.orb.set_state("idle")
                return

            print(f"[STT] {text}")

            # Handle paused state
            if self.state and self.state.is_paused():
                mode_cmd = self.state.detect_mode_command(text)
                if mode_cmd == WandaMode.AKTIV:
                    response = self.state.transition(WandaMode.AKTIV)
                    self._speak(response)
                return

            # STT/TTS only mode
            if self.stt_tts_only:
                if self.speak_transcript:
                    self._speak(f"{self.transcript_prefix}{text}".strip())
                if FULL_MODE and self.orb:
                    self.orb.set_state("idle")
                return

            # Mode commands
            if FULL_MODE:
                mode_cmd = self.state.detect_mode_command(text)
                if mode_cmd:
                    response = self.state.transition(mode_cmd)
                    self._speak(response)
                    if mode_cmd == WandaMode.AUTONOMOUS:
                        self.autonomous.start(text)
                    return

            # Refiner toggle commands
            if self.commands:
                cmd = self.commands.detect_command(text)
                if cmd in ("refiner_on", "refiner_off") and self.engine:
                    enabled = cmd == "refiner_on"
                    self.engine.set_refiner_enabled(enabled)
                    self.refiner_enabled = enabled
                    state_text = "an" if enabled else "aus"
                    self._speak(f"Prompt-Verbesserer {state_text}.")
                    return

            # Use WandaVoiceEngine for the rest of the pipeline
            if self.engine:
                future = asyncio.run_coroutine_threadsafe(
                    self.engine.process_text(text), self._loop
                )
                result = future.result(timeout=180)

                if result.error:
                    print(f"[Wanda] Engine error: {result.error}")
                    if FULL_MODE and self.orb:
                        self.orb.set_state("idle")
                    return

                # Handle confirmation results
                if result.confirmation_action in (
                    ConfirmationState.CANCEL,
                    ConfirmationState.REDO,
                ):
                    if FULL_MODE and self.orb:
                        self.orb.set_state("idle")
                    return

                if result.confirmation_action == ConfirmationState.EDIT:
                    self._speak("Okay, du kannst den Text bearbeiten.")
                    if FULL_MODE and self.orb:
                        self.orb.set_state("idle")
                    return

                # Got a response - speak it
                if result.response_text:
                    print(f"\n{'=' * 70}\n[WANDA]\n{result.response_text}\n{'=' * 70}")
                    if FULL_MODE and self.orb:
                        self.orb.set_state("speaking")
                    self._speak(result.response_text)

                    # Copy to clipboard and paste
                    if result.improved_text:
                        self.engine.paste_to_active_window(result.improved_text)

                if FULL_MODE:
                    self.sounds.success()
                    if self.orb:
                        self.orb.set_state("idle")
            else:
                # Fallback: direct Gemini (legacy path)
                self._process_legacy(text)

        except Exception as e:
            print(f"[Wanda] Error: {e}")
            if FULL_MODE and self.orb:
                self.orb.set_state("idle")
            import traceback

            traceback.print_exc()
        finally:
            self._processing = False

    def _process_legacy(self, text):
        """Legacy processing path when engine is not available."""
        from adapters.gemini_cli import GeminiCLIAdapter

        if FULL_MODE and self.guardrails:
            text = self.guardrails.redact(text)

        prompt = text
        if FULL_MODE and self.ollama and self.ollama.available:
            prompt = self.ollama.optimize_prompt(text, "gemini")

        if FULL_MODE:
            wanda_prompt = get_wanda_prompt("default")
            prompt = f"{wanda_prompt}\n\nUser: {prompt}"

        if not hasattr(self, "gemini") or self.gemini is None:
            self.gemini = GeminiCLIAdapter(
                model=self.config.get("adapters.gemini_model", "flash"),
                timeout=90,
                max_retries=2,
            )

        if FULL_MODE and self.orb:
            self.orb.set_state("thinking")
        response = self.gemini.send_prompt(prompt, include_history=True)
        if not response:
            response = "Keine Antwort von Gemini. Bitte nochmal versuchen."

        print(f"\n{'=' * 70}\n[WANDA]\n{response}\n{'=' * 70}")
        if FULL_MODE and self.orb:
            self.orb.set_state("speaking")
        self._speak(response)

        if FULL_MODE:
            self.sounds.success()
            if self.orb:
                self.orb.set_state("idle")

    def _auto_stop(self, audio):
        """Auto-stop handler when silence/max duration reached."""
        self.is_recording = False
        reason = None
        try:
            reason = self.recorder.get_last_stop_reason()
        except Exception:
            pass
        if reason:
            print(f"[Wanda] Auto-stop reason: {reason}")
        if audio is not None:
            threading.Thread(target=self._process, args=(audio,)).start()

    def _speak(self, text, mode=None):
        """Speak with interrupt support."""
        if not self.config.get("output.speak", True):
            return
        mode = mode or self.config.tts.get("mode", "short")
        if FULL_MODE:
            self.interrupt.speak_with_interrupt(text, mode)
        else:
            self.tts.speak(text, mode)
        self.last_response = text

    def _listen_short(self):
        """Listen for a short confirmation response (blocking)."""
        self.recorder.start_recording()
        start = time.time()
        while self.recorder.is_recording and time.time() - start < 8:
            time.sleep(0.1)
        if self.recorder.is_recording:
            audio = self.recorder.stop_recording()
        else:
            audio = self.recorder.consume_last_audio()
        if audio is not None:
            return self.stt.transcribe(audio, language="de")
        return None

    def send_text(self, text: str) -> None:
        if not self.engine:
            print("[Wanda] Engine not available")
            return
        future = asyncio.run_coroutine_threadsafe(
            self.engine.process_text(text, skip_confirmation=True), self._loop
        )
        result = future.result(timeout=180)
        if result.error:
            print(f"[Wanda] Engine error: {result.error}")
            return
        print(f"\n{'=' * 70}\n[WANDA]\n{result.response_text}\n{'=' * 70}")

    def stt_test(self, audio_path: str) -> None:
        print(f"[STT] Test file: {audio_path}")
        text = self.stt.transcribe_file(audio_path, language="de")
        print(f"[STT] Result: {text}")

    def run(self):
        """Main loop."""
        if FULL_MODE and self.orb:
            self.orb.show()
        if self.log_window:
            self.log_window.show()

        if FULL_MODE:
            briefing_text = self.briefing.generate()
            print(f"\n[Briefing] {briefing_text}")
            self._speak(briefing_text)

        print("\n" + "=" * 70)
        print("  WANDA READY!")
        print("=" * 70)
        wake_status = (
            "[Wake Word]" if (self.wake_word and self.wake_word.available) else ""
        )
        print(f"  Orb = Daily Start | RIGHT CTRL = Record {wake_status}")
        print(f"  'Wanda Pause' / 'Hey Wanda' = Sleep/Wake | 'Vollautonom' = Auto\n")

        if FULL_MODE and self.wake_word and self.wake_word.available:
            self.wake_word.start()

        self.hotkey.start()
        self.running = True

        if self.always_listening and not self.is_recording:
            self.toggle_recording()

        try:
            while self.running:
                time.sleep(0.5)
                if (
                    self.always_listening
                    and not self.is_recording
                    and not self._processing
                ):
                    self.toggle_recording()
        except KeyboardInterrupt:
            print("\n[Wanda] Shutting down...")
        finally:
            self._cleanup()

    def _cleanup(self):
        """Cleanup all resources."""
        if self._shutting_down:
            return
        self._shutting_down = True
        print("[Wanda] Cleaning up...")

        if self.ollama and hasattr(self.ollama, "cleanup"):
            self.ollama.cleanup()

        self._loop.call_soon_threadsafe(self._loop.stop)

        if FULL_MODE:
            try:
                self.vad.stop()
            except Exception:
                pass
            try:
                self.cli_proxy.close_all()
            except Exception:
                pass
            try:
                self.autonomous.stop()
            except Exception:
                pass
            if self.log_window:
                try:
                    self.log_window.destroy()
                except Exception:
                    pass
            if self.orb:
                try:
                    self.orb.destroy()
                except Exception:
                    pass
            try:
                quit_gtk()
            except Exception:
                pass
            if self.wake_word:
                try:
                    self.wake_word.stop()
                except Exception:
                    pass

        self.hotkey.stop()
        self.recorder.cleanup()
        print("[Wanda] Goodbye!")


def main():
    parser = argparse.ArgumentParser(description="Wanda Voice Assistant v2.0")
    parser.add_argument("--config", help="Config file path")
    parser.add_argument("--daemon", action="store_true", help="Daemon mode")
    parser.add_argument("--simple", action="store_true", help="Simple mode (no GUI)")
    parser.add_argument(
        "--no-refine", action="store_true", help="Disable prompt refiner"
    )
    parser.add_argument("--send-text", help="Send text directly to provider (no mic)")
    parser.add_argument("--stt-file", help="Transcribe a WAV file and exit")
    args = parser.parse_args()

    if not acquire_single_instance():
        sys.exit(1)

    wanda = WandaVoiceAssistant(config_path=args.config, daemon=args.daemon)

    if args.no_refine:
        wanda._toggle_refiner(False)

    if args.stt_file:
        wanda.stt_test(args.stt_file)
        wanda._cleanup()
        return

    if args.send_text:
        wanda.send_text(args.send_text)
        wanda._cleanup()
        return

    wanda.run()


if __name__ == "__main__":
    main()
