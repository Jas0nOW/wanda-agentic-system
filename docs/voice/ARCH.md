# WANDA Voice Mode - Architecture

## Overview

```
                    ┌─────────────────────────────────────────────┐
                    │              WANDA Voice System              │
                    │                                             │
  ┌─────────┐      │  ┌──────────────────────────────────────┐   │
  │ Mic/Key │──────┼─>│        wanda-voice/ (Frontend)        │   │
  │ evdev   │      │  │  AudioRecorder, HotkeyHandler, Orb   │   │
  └─────────┘      │  │  LogWindow, InterruptController       │   │
                    │  └──────────────┬───────────────────────┘   │
                    │                 │ audio/text                 │
                    │                 v                            │
                    │  ┌──────────────────────────────────────┐   │
                    │  │      wanda_voice_core/ (Engine)       │   │
                    │  │                                       │   │
                    │  │  ┌─────┐  ┌────────┐  ┌──────────┐   │   │
                    │  │  │ STT │->│ Router │->│ Refiner  │   │   │
                    │  │  └─────┘  └────┬───┘  └────┬─────┘   │   │
                    │  │               │           │           │   │
                    │  │          command    refine/llm        │   │
                    │  │               │           │           │   │
                    │  │               v           v           │   │
                    │  │  ┌──────────────────────────────┐     │   │
                    │  │  │     Confirmation Flow        │     │   │
                    │  │  │  Readback -> Listen -> Decide│     │   │
                    │  │  └──────────────┬───────────────┘     │   │
                    │  │                 │ SEND                │   │
                    │  │                 v                     │   │
                    │  │  ┌──────────────────────────────┐     │   │
                    │  │  │      Safety Policy           │     │   │
                    │  │  │  Denylist/Caution/Allow       │     │   │
                    │  │  └──────────────┬───────────────┘     │   │
                    │  │                 │                     │   │
                    │  │                 v                     │   │
                    │  │  ┌────────────────────┐              │   │
                    │  │  │    Providers        │              │   │
                    │  │  │ ┌───────┐ ┌──────┐ │              │   │
                    │  │  │ │Gemini │ │Ollama│ │              │   │
                    │  │  │ │ CLI   │ │ HTTP │ │              │   │
                    │  │  │ └───────┘ └──────┘ │              │   │
                    │  │  └────────┬───────────┘              │   │
                    │  │           │                           │   │
                    │  │           v                           │   │
                    │  │  ┌─────────────┐  ┌──────────────┐   │   │
                    │  │  │ Token Econ. │  │ EventBus     │   │   │
                    │  │  │ Caps/Redact │  │ Pub/Sub      │   │   │
                    │  │  └─────────────┘  └──────────────┘   │   │
                    │  └──────────────────────────────────────┘   │
                    │                                             │
  ┌─────────┐      │  ┌──────────────────────────────────────┐   │
  │ Speaker │<─────┼──│        TTS (Edge/Piper)               │   │
  └─────────┘      │  └──────────────────────────────────────┘   │
                    │                                             │
                    │  ┌──────────────────────────────────────┐   │
                    │  │       REST API (:8370)                │   │
                    │  │  POST /v1/utterance                   │   │
                    │  │  GET  /v1/health                      │   │
                    │  │  GET  /v1/stream (SSE)                │   │
                    │  └──────────────────────────────────────┘   │
                    │                                             │
                    │  ┌──────────────────────────────────────┐   │
                    │  │       OVOS Bridge                     │   │
                    │  │  wanda_bridge_skill -> API             │   │
                    │  └──────────────────────────────────────┘   │
                    └─────────────────────────────────────────────┘
```

## Package Structure

| Package | Role |
|---------|------|
| `wanda_voice_core/` | Headless engine, no GUI deps |
| `wanda_voice_core/providers/` | LLM provider adapters |
| `wanda-voice/` | GTK frontend, audio I/O, platform-specific |
| `ovos_bridge/` | OVOS skill forwarding to API |

## Key Flows

### Voice Input Flow
1. User presses RightCtrl (or holds)
2. AudioRecorder captures audio
3. Silence detected -> auto-stop
4. STT transcribes
5. Router classifies (command/refine/llm)
6. Refiner improves text (Ollama)
7. Confirmation: readback + listen for "abschicken"
8. Provider sends to Gemini/Ollama
9. TTS speaks response
10. Text pasted to active window

### API Flow
1. POST /v1/utterance with text
2. Engine processes (skip confirmation)
3. Returns response JSON

## Safety

- Command execution OFF by default
- Risk scoring 0-10
- Voice confirmation for risk >= 3
- GUI confirmation for risk >= 6
- Denylist blocks destructive commands
- Prompt injection detection
