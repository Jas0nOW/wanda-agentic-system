 WANDA Voice Mode - Implementation Plan

 Scope

 Build the complete "Wanda Voice Mode" as a Jarvis-grade desktop voice assistant. Create a headless wanda_voice_core/ package with clean extension points, refactor existing wanda-voice/ as a
 frontend, add OVOS bridge, REST API, tests, and docs.

 Key Decisions (ADRs)

 1. Keep wanda-voice/ as frontend - Don't rewrite from scratch. Refactor main.py to delegate to new wanda_voice_core/ engine.
 2. Archive wanda_local/ - Move to archive/. Code migrated into wanda_voice_core/.
 3. Python asyncio - Core engine uses asyncio for non-blocking I/O. Frontends bridge via threads where needed (GTK).
 4. aiohttp for API - Lightweight REST API, no FastAPI dependency (minimize requirements).
 5. No new heavy deps - Reuse edge-tts, piper, faster-whisper, sounddevice, evdev, PyGObject already in venv.

 ---
 Phase 1: Create wanda_voice_core/ Package (Core Infrastructure)

 New files to create:

 wanda_voice_core/__init__.py - Package init, exports WandaVoiceEngine, version="2.0.0"

 wanda_voice_core/schemas.py - Strict dataclass schemas:
 - RouterResult: { route: command|refine|llm, confidence: 0..1, command: {}?, notes: "" }
 - RefinerResult: { intent: "", improved_text: "", do: send|ask|edit, questions: [], token_budget: {max_output_tokens: N} }
 - UtteranceRequest/Response for API
 - RunEvent for event logging
 - Validation via validate() methods

 wanda_voice_core/event_bus.py - Thread-safe EventBus:
 - subscribe(event_type, callback), emit(event_type, data), get_recent_events(n)
 - Event types: recording.start/stop, vad.speech/silence, stt.result, router/refiner.result, provider.request/response/error/timeout, tts.start/stop/interrupt, confirmation.ask/response,
 safety.check/blocked, run.start/end, metrics.update, state.change, error
 - Rolling log of last 100 events

 wanda_voice_core/run_manager.py - Run artifacts:
 - start_run() -> run_id, log_event(), save_artifact(), save_audio(), end_run()
 - Writes to runs/{run_id}/ (events.jsonl, summary.json, audio.wav)

 wanda_voice_core/token_economy.py - Token caps & metrics:
 - estimate_tokens(), check_budget(), truncate_to_budget()
 - summarize_context() for rolling short memory
 - redact_sensitive() - strips secrets/hex/base64/stack traces
 - Hard caps: MAX_CONTEXT_CHARS=8000, MAX_TURNS=12, MAX_OUTPUT_TOKENS=2048
 - Metrics: chars_in/out, token_est_in/out, latency_ms

 wanda_voice_core/config.py - Extended config:
 - Profiles: gui, simple, offline
 - All sections: audio, vad, stt, router, refiner, providers, tts, safety, token_economy, ui, hotkey, confirmation, api
 - Loads from wanda_voice.yaml, falls back to embedded defaults
 - Reuse pattern from existing wanda-voice/config/config.py

 Reuse from existing code:

 - wanda-voice/config/config.py -> extend for new sections
 - wanda-voice/audio/silero_vad.py -> copy SileroVAD + EnergyVAD as-is
 - wanda-voice/stt/faster_whisper_engine.py -> fix duplicate _ensure_utf8_locale, move to core
 - wanda-voice/tts/edge_tts_engine.py + piper_engine.py -> wrap in unified TTS interface
 - wanda-voice/adapters/gemini_cli.py -> move to providers/gemini_cli.py
 - wanda-voice/adapters/ollama_manager.py -> move to providers/ollama.py
 - wanda_local/src/safety.py -> enhance for risk scoring in safety.py

 ---
 Phase 2: Core Logic Modules (Router, Refiner, Safety, Providers)

 wanda_voice_core/router.py - IntentRouter:
 - Keyword-based fast classification (reuse preprocess/intent.py patterns)
 - Routes to: "command" (voice commands like abschicken/stop), "refine" (needs Ollama improvement), "llm" (send directly to Gemini)
 - Returns strict RouterResult JSON schema
 - Optional Ollama-based routing for ambiguous inputs
 - Confidence scoring

 wanda_voice_core/refiner.py - PromptRefiner:
 - Uses Ollama HTTP API with strict JSON schema output
 - System prompt forces structured RefinerResult
 - Handles: intent extraction, text improvement, action determination (send/ask/edit)
 - Falls back to passthrough if Ollama unavailable

 wanda_voice_core/safety.py - SafetyPolicy:
 - Merge wanda_local/src/safety.py denylist/allowlist + risk scoring
 - Risk levels: SAFE (0-2), CAUTION (3-5), DANGEROUS (6-8), BLOCKED (9-10)
 - Voice confirmation gate: risk >= CAUTION requires spoken confirmation
 - GUI confirmation gate: risk >= DANGEROUS requires both voice + UI button
 - Default: command_execution=OFF. Voice can only send text to LLM providers.
 - Injection defense: tool outputs treated as data, never instructions

 wanda_voice_core/providers/__init__.py + base.py - Provider interface:
 - Abstract ProviderBase with send(prompt, context) -> str, is_available() -> bool

 wanda_voice_core/providers/gemini_cli.py - Refactored from existing:
 - Reuse wanda-voice/adapters/gemini_cli.py retry/timeout logic
 - Add token economy enforcement (truncate context, cap output)
 - Timeout hardening: default 90s, retries with 2s/4s backoff, max 2 retries
 - Clear "Gemini unavailable" state on final failure

 wanda_voice_core/providers/ollama.py - Refactored from existing:
 - Reuse wanda-voice/adapters/ollama_manager.py lifecycle management
 - Add structured JSON output support
 - Optional fallback provider when Gemini fails (if enabled)

 ---
 Phase 3: Voice Confirmation Flow + Engine

 wanda_voice_core/confirmation.py - Voice confirmation orchestrator:
 - State machine: IDLE -> RECORDING -> TRANSCRIBING -> REFINING -> READBACK -> AWAITING_RESPONSE -> (SEND|EDIT|REDO|CANCEL)
 - After STT transcript, calls Refiner for improved text
 - TTS reads back: "Hier ist die verbesserte Version: {text}"
 - TTS asks: "Soll ich abschicken oder verändern?"
 - Listens for short response, runs through CommandDetector
 - Valid commands: "Abschicken" -> send, "Verändern" -> re-record, "Nochmal" -> redo from scratch, "Abbrechen/Stop" -> cancel
 - Timeout on awaiting response (10s default) -> ask again once, then cancel
 - Emits events at each stage

 wanda_voice_core/engine.py - Main WandaVoiceEngine orchestrator:
 - Constructor takes config, wires all components
 - async process_audio(audio_data) -> EngineResult - full pipeline
 - async process_text(text) -> EngineResult - text-only (for API/OVOS)
 - Pipeline: AudioInput -> VAD -> STT -> Router -> (Refiner?) -> Confirmation -> Provider -> TTS
 - EventBus integration: emits events at each step
 - RunManager: creates run, logs artifacts
 - Token economy: enforces caps at each stage
 - Clipboard insertion: after confirmation, copies to clipboard + pastes (xdotool/wtype)
 - Active window detection: reuse wanda-voice/system/active_window.py

 Reuse:

 - wanda-voice/audio/recorder.py AudioRecorder + HotkeyHandler (as-is, imported by frontend)
 - wanda-voice/conversation/command_detector.py (reuse for confirmation detection)
 - wanda-voice/conversation/state_machine.py (reuse for mode management)
 - wanda-voice/audio/interrupt_controller.py (reuse for barge-in)
 - wanda-voice/system/active_window.py (reuse for clipboard insertion)

 ---
 Phase 4: Hardening (Timeouts, Barge-in, Token Caps, Metrics)

 Modify providers/gemini_cli.py:
 - Configurable timeout (default 90s), max_retries (default 2)
 - Exponential backoff: 2s, 4s between retries
 - On final failure: emit "provider.timeout" event, return localized error
 - Optional Ollama fallback if enabled

 Modify engine.py:
 - Barge-in: if user says "Stop" during TTS, interrupt immediately, return to listening
 - Token caps enforced: context truncated to MAX_CONTEXT_CHARS before sending
 - Metrics emission: chars_in/out, token_est, latency_ms per run
 - Redaction: never send raw logs, stack traces, or long hex strings to LLM

 Modify TTS (wrapped in core):
 - Streaming-friendly: split text by sentences, speak sequentially
 - Interruptable: check stop flag between sentences
 - Offline fallback: Piper always available even without network

 ---
 Phase 5: REST API + OVOS Bridge

 wanda_voice_core/api.py - REST API (aiohttp):
 - POST /v1/utterance - { text, mode, context } -> { final_text, response_text, actions, events_summary }
 - GET /v1/health - health check
 - GET /v1/status - current state, loaded models, metrics
 - Optional SSE /v1/stream for real-time events
 - Disabled by default (config: api.enabled=false, api.port=8370)
 - No auth needed (localhost only by default)

 ovos_bridge/README.md - Setup instructions for OVOS integration

 ovos_bridge/wanda_bridge_skill/__init__.py - OVOS skill:
 - Forwards utterances to Wanda Core API (POST /v1/utterance)
 - Speaks response via OVOS TTS
 - Configurable Wanda API URL

 ovos_bridge/docker-compose.yml - Optional OVOS stack (placeholder)

 ---
 Phase 6: Desktop UI (LogWindow) + Frontend Wiring

 wanda-voice/ui/log_window.py - NEW LogWindow:
 - GTK3 window (Gtk.Window) with scrollable text view
 - Shows: live transcript (partial + final), improved prompt preview, provider response, event timeline
 - Buttons: Send, Edit, Redo, Cancel, Readback
 - Shows: provider name, retry count, timeout status
 - Subscribes to EventBus for real-time updates
 - Opens from Orb context menu or automatically in gui mode

 Modify wanda-voice/main.py:
 - Import WandaVoiceEngine from wanda_voice_core
 - Replace inline pipeline logic with engine.process_audio()
 - Wire EventBus to Orb (state changes) and LogWindow (all events)
 - Keep HotkeyHandler, AudioRecorder in frontend (they handle platform-specific I/O)
 - Support both hold-to-talk (key down = start, key up = stop) and toggle mode
 - On auto-stop (silence), enter confirmation flow instead of direct send

 wanda-voice/launcher.py - Update:
 - --simple mode uses engine directly without GTK
 - --gui mode (default) starts Orb + LogWindow
 - Both modes use same wanda_voice_core engine

 ---
 Phase 7: Tests + Docs + Cleanup

 Tests (tests/):

 tests/test_vad.py - VAD silence detection:
 - Fixture: 3s audio with 1.5s speech + 1.5s silence
 - Assert silence detection triggers within 200ms of actual silence start

 tests/test_schemas.py - Router/Refiner schema validation:
 - Valid RouterResult/RefinerResult pass
 - Invalid data (missing fields, wrong types) raises ValidationError

 tests/test_gemini_timeout.py - Gemini CLI timeout handling:
 - Mock subprocess.run to simulate timeout
 - Assert retry logic fires, fallback model tried
 - Assert "unavailable" state after all retries fail

 tests/test_clipboard.py - Clipboard insertion:
 - Mock xclip/wl-copy
 - Assert text copied to clipboard correctly

 tests/test_confirmation.py - Voice confirmation flow:
 - Mock STT to return "abschicken"
 - Assert flow completes with send action

 tests/test_token_economy.py - Token caps:
 - Assert context truncation at MAX_CONTEXT_CHARS
 - Assert redaction of secrets

 Docs (docs/voice/):

 docs/voice/ARCH.md - Architecture overview with ASCII diagrams
 docs/voice/CONFIG.md - All config options with defaults
 docs/voice/TROUBLESHOOTING.md - Common issues and fixes
 docs/voice/OVOS_BRIDGE.md - OVOS integration guide

 Cleanup:

 - Move wanda_local/ to archive/legacy_wanda_local_YYYYMMDD/
 - Remove .env with exposed Telegram token from wanda_local
 - Fix duplicate _ensure_utf8_locale in faster_whisper_engine.py
 - Delete __pycache__/ dirs
 - Update README.md with voice quickstart
 - Update docs/SSOT/INVENTORY.md

 ---
 Critical Files (Full Paths)

 New files to create:

 wanda_voice_core/__init__.py
 wanda_voice_core/schemas.py
 wanda_voice_core/event_bus.py
 wanda_voice_core/run_manager.py
 wanda_voice_core/token_economy.py
 wanda_voice_core/config.py
 wanda_voice_core/router.py
 wanda_voice_core/refiner.py
 wanda_voice_core/safety.py
 wanda_voice_core/confirmation.py
 wanda_voice_core/engine.py
 wanda_voice_core/api.py
 wanda_voice_core/providers/__init__.py
 wanda_voice_core/providers/base.py
 wanda_voice_core/providers/gemini_cli.py
 wanda_voice_core/providers/ollama.py
 ovos_bridge/README.md
 ovos_bridge/wanda_bridge_skill/__init__.py
 ovos_bridge/docker-compose.yml
 wanda-voice/ui/log_window.py
 tests/test_vad.py
 tests/test_schemas.py
 tests/test_gemini_timeout.py
 tests/test_clipboard.py
 tests/test_confirmation.py
 tests/test_token_economy.py
 tests/conftest.py
 docs/voice/ARCH.md
 docs/voice/CONFIG.md
 docs/voice/TROUBLESHOOTING.md
 docs/voice/OVOS_BRIDGE.md

 Existing files to modify:

 wanda-voice/main.py                      # Refactor to use WandaVoiceEngine
 wanda-voice/launcher.py                  # Update simple/gui mode routing
 wanda-voice/stt/faster_whisper_engine.py  # Fix duplicate function
 wanda-voice/config/config.py             # Extend with new sections
 README.md                                 # Add voice quickstart
 docs/SSOT/INVENTORY.md                    # Update artifact list

 Existing files to reuse (import, don't copy):

 wanda-voice/audio/recorder.py            # AudioRecorder + HotkeyHandler
 wanda-voice/audio/silero_vad.py           # SileroVAD + EnergyVAD + get_vad()
 wanda-voice/audio/interrupt_controller.py # Barge-in support
 wanda-voice/tts/edge_tts_engine.py        # EdgeTTSEngine
 wanda-voice/tts/piper_engine.py           # PiperEngine
 wanda-voice/conversation/command_detector.py  # ConversationalCommandDetector
 wanda-voice/conversation/state_machine.py     # StateMachine + WandaMode
 wanda-voice/system/active_window.py           # ActiveWindowDetector
 wanda-voice/ui/orb.py                         # WandaOrb (keep as-is)
 wanda-voice/ui/confirm.py                     # ConfirmUI (terminal mode)
 wanda-voice/preprocess/intent.py              # IntentDetector patterns

 Files to archive:

 wanda_local/                              # -> archive/legacy_wanda_local/

 ---
 Verification

 End-to-end test (manual):

 1. cd wanda-voice && python main.py --simple -> should start, respond to Enter/RightCtrl
 2. Speak, silence auto-stops, refined text read back, "Abschicken" sends
 3. python main.py -> Orb appears, LogWindow shows events
 4. python -m wanda_voice_core.api -> API starts on :8370
 5. curl -X POST localhost:8370/v1/utterance -d '{"text":"Hallo","mode":"text"}' -> returns response

 Automated tests:

 cd tests && python -m pytest -v

 DoD checklist:

 - Auto-stop on silence works reliably
 - Voice confirmation works (abschicken/verändern/nochmal/abbrechen)
 - Orb + LogWindow show correct state + content
 - Gemini CLI provider robust with retry/timeout
 - Token economy enforced (caps, schemas, summaries)
 - No dangerous command execution by default; safety gates exist
 - OVOS bridge exists (API + adapter + docs)
 - Tests pass; docs complete; quickstart works