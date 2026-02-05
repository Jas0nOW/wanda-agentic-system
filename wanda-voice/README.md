# 🎙️ WANDA Voice Mode

WANDA Voice Mode is the desktop voice assistant frontend. It wires audio I/O, hotkeys, and GUI to the headless engine in `wanda_voice_core/`.

## Features

- Always-on or hotkey voice capture (Right Ctrl)
- Silence auto-stop + voice confirmation
- GUI mode (Orb + LogWindow) and `--simple` mode
- Provider routing (Gemini CLI primary, Ollama optional)
- Text insertion into active window (clipboard + paste)

## Quick Start

From repo root:

```bash
python3 wanda-voice/launcher.py           # GUI mode
python3 wanda-voice/launcher.py --simple  # No GUI
```

If installed system-wide:

```bash
wanda voice
wanda voice --simple
```

## Configuration

Config file search order:

1. `./wanda_voice.yaml`
2. `~/.wanda/voice.yaml`
3. `~/.wanda-system/wanda-voice/wanda.config.yaml`

See `docs/voice/CONFIG.md` for the full reference.

## Commands

Voice confirmation commands after readback:

- "Abschicken" → send
- "Verändern" → re-record/edit flow
- "Nochmal" → redo
- "Abbrechen" → cancel

## API + OVOS

- REST API: `python -m wanda_voice_core.api`
- OVOS bridge: `docs/voice/OVOS_BRIDGE.md`

## Troubleshooting

See `docs/voice/TROUBLESHOOTING.md` for audio, hotkey, and provider issues.

## Structure

```
wanda-voice/
├── main.py          # Frontend entry (audio, hotkeys, GUI)
├── launcher.py      # Wayland-aware launcher
├── audio/           # Recorder, VAD, wake word
├── conversation/    # Commands, state machine
├── stt/             # STT engines
├── tts/             # TTS engines
└── ui/              # Orb + LogWindow
```
