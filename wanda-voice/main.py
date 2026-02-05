#!/usr/bin/env python3
# Wanda Voice Assistant - JARVIS Full Main Loop
"""Complete Wanda with all 3 modes: Aktiv, CLI-Proxy, Autonomous."""

import sys
import time
import signal
import argparse
import os
import atexit
import fcntl
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

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
from adapters.gemini_cli import GeminiCLIAdapter

# JARVIS Phase 2+3 imports (core)
FULL_MODE = False
GTK_AVAILABLE = False
WAKE_WORD_AVAILABLE = False
MOBILE_AVAILABLE = False

try:
    from audio.silero_vad import get_vad
    from audio.interrupt_controller import InterruptController
    from conversation.command_detector import ConversationalCommandDetector
    from conversation.jarvis_prompts import get_jarvis_prompt
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
    print(f"[Wanda] Core voice modules missing: {e}")

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


class WandaJARVIS:
    """Wanda Voice Assistant - Full JARVIS Implementation."""

    def __init__(self, config_path=None, daemon=False):
        print("=" * 70)
        print("🎙️  WANDA JARVIS - SOVEREIGN AI VOICE ASSISTANT")
        print("=" * 70)

        self.config = Config(config_path)
        self.daemon = daemon
        self.stt_tts_only = self.config.get("pipeline.stt_tts_only", False)
        self.speak_transcript = self.config.get("pipeline.speak_transcript", True)
        self.transcript_prefix = self.config.get("pipeline.transcript_prefix", "")

        # Core
        self._init_core()

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

        class _DisabledOllama:
            available = False

            def cleanup(self):
                return None

        self.ollama = _DisabledOllama()

        # Phase 2+3
        if FULL_MODE:
            self._init_jarvis()
            self._init_phase3()

        # State
        self.running = False
        self.is_recording = False
        self._shutting_down = False

        # Hotkey
        self.hotkey = HotkeyHandler(
            key=self.config.get("trigger.key", "rightctrl"),
            on_toggle=self.toggle_recording,
        )

        print("\n✅ [Wanda] Fully initialized")

    def _init_core(self):
        """Core MVP components."""
        self.recorder = AudioRecorder(
            sample_rate=self.config.audio_config.get("sample_rate", 16000),
            max_seconds=60,
            silence_timeout=self.config.audio_config.get("silence_timeout", 1.2),
            silence_threshold=self.config.audio_config.get("silence_threshold", 0.01),
            min_seconds=self.config.audio_config.get("min_seconds", 1.0),
            on_auto_stop=self._auto_stop,
        )
        self.stt = FasterWhisperEngine(
            model_name=self.config.stt.get("model", "large-v3-turbo"),
            device=self.config.stt.get("device", "auto"),
        )
        # TTS: Edge (Siri-Qualität) oder Piper (Offline)
        tts_engine = self.config.tts.get("engine", "edge")
        tts_voice = self.config.tts.get("voice", "katja")
        tts_mode = self.config.tts.get("mode", "short")

        if tts_engine == "edge" and EDGE_TTS_AVAILABLE:
            self.tts = EdgeTTSEngine(voice=tts_voice)
            self.tts.mode = tts_mode
        else:
            # Fallback to Piper
            piper_voice = self.config.tts.get("voice", "de_DE-kerstin-low")
            if not piper_voice.startswith("de_DE"):
                piper_voice = "de_DE-kerstin-low"
            self.tts = PiperEngine(voice=piper_voice, mode=tts_mode)
        if not self.stt_tts_only:
            self.gemini = GeminiCLIAdapter(
                model=self.config.gemini_config.get("gemini_model", "flash"),
                timeout=self.config.gemini_config.get("timeout", 90),
                max_retries=2,
            )
        else:
            self.gemini = None

    def _init_jarvis(self):
        """Phase 2 JARVIS components."""
        self.vad = get_vad("silero")
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
        # State Machine
        self.state = StateMachine(on_mode_change=self._on_mode_change)

        # Context Manager (smart context with auto-refresh)
        self.context = ContextManager(
            max_messages_per_window=self.config.get("context.max_messages", 20),
            max_windows=5,
        )

        # Ollama (smart on-demand management)
        ollama_enabled = self.config.get("ollama.enabled", False)
        if ollama_enabled:
            ollama_model = self.config.get("ollama.model", "")
            if ollama_model:
                print(f"[Ollama] On-demand mode: {ollama_model}")
                self.ollama = OllamaManager(
                    model=ollama_model,
                    auto_unload=True,
                    unload_timeout=120,  # Unload after 2 min idle
                )
                print("[Ollama] Starts on first use, auto-unloads after 120s idle")
                print("[Ollama] Will stop server on exit if started by WANDA")
                # Don't start yet - will start on first use
            else:
                self.ollama = type("DisabledOllama", (), {"available": False})()
        else:
            self.ollama = type("DisabledOllama", (), {"available": False})()

        # CLI Proxy
        self.cli_proxy = CLIProxy(on_output=self._on_cli_output)

        # Briefing Generator
        self.briefing = BriefingGenerator()
        self.briefing.ollama = self.ollama if self.ollama.available else None

        # Autonomous Controller
        self.autonomous = AutonomousController(
            cli_proxy=self.cli_proxy,
            ollama=self.ollama if self.ollama.available else None,
            on_progress=lambda msg: self._speak(msg),
            on_complete=lambda msg: self._speak(msg),
        )

        # Workflow Engine
        self.workflows = WorkflowEngine()

        # Visual Orb Indicator
        self.orb = None
        if GTK_AVAILABLE:
            self.orb = WandaOrb(size=60, on_click=self._on_orb_click)
            import threading

            self.gtk_thread = threading.Thread(target=run_gtk_main, daemon=True)
            self.gtk_thread.start()

        # Daily Initializer
        self.daily_init = DailyInitializer(
            briefing=self.briefing,
            ollama=self.ollama if self.ollama.available else None,
            speak_callback=lambda msg: self._speak(msg),
            orb_callback=lambda state: self.orb.set_state(state) if self.orb else None,
        )

        # Wake Word Detector (optional)
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

        # Mobile Access
        self.notifier = None
        self.project_init = None
        self.telegram_bot = None

        if MOBILE_AVAILABLE:
            # Push Notifications
            if self.config.get("notifications.enabled", False):
                self.notifier = WandaNotifier(
                    topic=self.config.get("notifications.topic", "wanda-private"),
                    server=self.config.get("notifications.server", "https://ntfy.sh"),
                    enabled=True,
                )

            # Project Initializer
            self.project_init = ProjectInitializer(
                ollama=self.ollama if self.ollama.available else None,
                notifier=self.notifier,
            )

            # Telegram Bot
            if self.config.get("telegram.enabled", False):
                self.telegram_bot = create_telegram_bot(
                    self.config._config,
                    stt_engine=self.stt,
                    tts_engine=self.tts,
                    gemini_adapter=self.gemini,
                    ollama_adapter=self.ollama,
                    project_init=self.project_init,
                    notifier=self.notifier,
                )

    def _on_mode_change(self, old_mode, new_mode):
        """Handle mode transitions."""
        print(f"[Wanda] Mode: {old_mode.name} → {new_mode.name}")
        # Update orb
        if self.orb:
            state_map = {
                WandaMode.AKTIV: "idle",
                WandaMode.PAUSED: "paused",
                WandaMode.AUTONOMOUS: "autonomous",
                WandaMode.CLI_PROXY: "thinking",
            }
            self.orb.set_state(state_map.get(new_mode, "idle"))

    def _on_cli_output(self, output: str):
        """Handle CLI output - read via TTS."""
        if self.config.get("output.speak", True):
            self._speak(output, mode="short")

    def _on_wake_word(self):
        """Handle wake word detection - activate Wanda."""
        print("🌟 [Wanda] Wake word detected!")

        if not self.state:
            self.toggle_recording()
            return

        if self.state.is_paused():
            # Resume from pause
            response = self.state.transition(WandaMode.AKTIV)
            self._speak(response)
        else:
            # Start daily init or toggle recording
            self._on_orb_click()

    def _on_orb_click(self):
        """Handle orb click - Daily Start or toggle recording."""
        if self.state and self.state.is_paused():
            # Wake up from pause
            response = self.state.transition(WandaMode.AKTIV)
            self._speak(response)
            return

        # First click of the day = Daily Start
        if FULL_MODE and self.daily_init and self.daily_init.is_first_session_today():
            import threading

            threading.Thread(
                target=self.daily_init.run_daily_start, daemon=True
            ).start()
            return

        # Subsequent clicks = toggle recording
        self.toggle_recording()

    def toggle_recording(self):
        """Toggle recording."""
        if self.state and self.state.is_paused():
            return  # Ignore when paused

        if not self.is_recording:
            if FULL_MODE:
                self.sounds.trigger()
                if self.orb:
                    self.orb.set_state("listening")
            self.recorder.start_recording()
            self.is_recording = True
            print("\n🎤 Recording...")
        else:
            self.is_recording = False
            audio = self.recorder.stop_recording()
            if audio is not None:
                import threading

                threading.Thread(target=self._process, args=(audio,)).start()

    def _process(self, audio):
        """Main processing pipeline."""
        try:
            # 1. Transcribe
            text = self.stt.transcribe(audio, language="de")
            if not text:
                print("❌ No speech")
                return

            if self.state:
                print(f"✅ [{self.state.mode.name}] {text}")
            else:
                print(f"✅ [STT] {text}")

            # 2. STT/TTS only mode (no LLM)
            if self.stt_tts_only:
                if self.speak_transcript:
                    transcript = f"{self.transcript_prefix}{text}".strip()
                    self._speak(transcript)
                return

            # 3. Mode commands (pause/resume/autonomous)
            if FULL_MODE:
                mode_cmd = self.state.detect_mode_command(text)
                if mode_cmd:
                    response = self.state.transition(mode_cmd)
                    self._speak(response)

                    if mode_cmd == WandaMode.AUTONOMOUS:
                        # Start autonomous with remaining text
                        self.autonomous.start(text)
                    return

            # 4. JARVIS commands (preview, cancel, etc)
            if self.commands:
                cmd = self.commands.detect_command(text)
                if cmd:
                    self._handle_command(cmd, text)
                    return

            # 5. Workflow detection
            if self.workflows:
                workflow = self.workflows.detect_workflow(text)
                if workflow:
                    params = self.workflows.extract_params(text, workflow)
                    result = self.workflows.execute(workflow, params)
                    self._speak(result)
                    return

            # 6. Guardrails
            if FULL_MODE and self.guardrails:
                text = self.guardrails.redact(text)

            # 7. Optimize prompt (Ollama if available)
            prompt = text
            if FULL_MODE and self.ollama and self.ollama.available:
                prompt = self.ollama.optimize_prompt(text, "gemini")

            # 8. Add JARVIS prompt
            if FULL_MODE:
                jarvis = get_jarvis_prompt("default")
                prompt = f"{jarvis}\n\nUser: {prompt}"

            # 9. Check context freshness
            if FULL_MODE and self.context:
                if self.context.should_refresh():
                    self.context.start_fresh_window("gemini")

            # 10. Send to Gemini
            print("\n[Wanda] 🤖 Asking Gemini...")
            if FULL_MODE and self.orb:
                self.orb.set_state("thinking")
            response = self.gemini.send_prompt(prompt, include_history=True)

            # 11. Update context
            if FULL_MODE and self.context:
                self.context.add_message("user", text)
                self.context.add_message("assistant", response)

            # 12. Output
            print(f"\n{'=' * 70}\n🤖 WANDA:\n{response}\n{'=' * 70}")
            if FULL_MODE and self.orb:
                self.orb.set_state("speaking")
            self._speak(response)

            if FULL_MODE:
                self.sounds.success()
                if self.orb:
                    self.orb.set_state("idle")

        except Exception as e:
            print(f"❌ Error: {e}")
            if FULL_MODE and self.orb:
                self.orb.set_state("idle")
            import traceback

            traceback.print_exc()

    def _auto_stop(self, audio):
        """Auto-stop handler when silence/max duration reached."""
        self.is_recording = False
        if audio is not None:
            import threading

            threading.Thread(target=self._process, args=(audio,)).start()

    def _handle_command(self, cmd, text):
        """Handle JARVIS commands."""
        if cmd == "preview":
            last = (
                self.context.current_window.messages[-1]["content"]
                if self.context.current_window
                else None
            )
            if last:
                self._speak(last, mode="full")
        elif cmd == "cancel":
            self.tts.stop()
            self.sounds.cancel()
        elif cmd == "send":
            self._speak("Verstanden, abgeschickt.")

    def _speak(self, text, mode=None):
        """Speak with interrupt support."""
        if not self.config.get("output.speak", True):
            return
        mode = mode or self.config.tts.get("mode", "short")
        if FULL_MODE:
            self.interrupt.speak_with_interrupt(text, mode)
        else:
            self.tts.speak(text, mode)

    def run(self):
        """Main loop."""
        # Show orb
        if FULL_MODE and self.orb:
            self.orb.show()

        # Startup briefing
        if FULL_MODE:
            briefing_text = self.briefing.generate()
            print(f"\n📋 Briefing: {briefing_text}")
            self._speak(briefing_text)

        print("\n" + "=" * 70)
        print("🚀 WANDA JARVIS READY!")
        print("=" * 70)
        wake_status = (
            "🎤 Wake Word aktiv"
            if (self.wake_word and self.wake_word.available)
            else ""
        )
        print(f"📌 Click Orb = Daily Start | RIGHT CTRL = Record {wake_status}")
        print("📌 'Wanda Pause' / 'Hey Wanda' = Sleep/Wake | 'Vollautonom' = Auto\n")

        # Start wake word if available
        if FULL_MODE and self.wake_word and self.wake_word.available:
            self.wake_word.start()

        self.hotkey.start()
        self.running = True

        try:
            while self.running:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n👋 Shutting down...")
        finally:
            self._cleanup()

    def _cleanup(self):
        """Cleanup all resources."""
        if self._shutting_down:
            return
        self._shutting_down = True
        print("[Wanda] Cleaning up...")

        # Cleanup Ollama (unload model, stop if we started it)
        if self.ollama and hasattr(self.ollama, "cleanup"):
            self.ollama.cleanup()

        if FULL_MODE:
            try:
                self.vad.stop()
            except:
                pass
            try:
                self.cli_proxy.close_all()
            except:
                pass
            try:
                self.autonomous.stop()
            except:
                pass
            if self.orb:
                try:
                    self.orb.destroy()
                except:
                    pass
            try:
                quit_gtk()
            except:
                pass
            if self.wake_word:
                try:
                    self.wake_word.stop()
                except:
                    pass

        self.hotkey.stop()
        self.recorder.cleanup()
        print("[Wanda] Goodbye!")


def main():
    parser = argparse.ArgumentParser(description="Wanda JARVIS Voice Assistant")
    parser.add_argument("--config", help="Config file path")
    parser.add_argument("--daemon", action="store_true", help="Daemon mode")
    args = parser.parse_args()

    if not acquire_single_instance():
        sys.exit(1)

    wanda = WandaJARVIS(config_path=args.config, daemon=args.daemon)
    wanda.run()


if __name__ == "__main__":
    main()
