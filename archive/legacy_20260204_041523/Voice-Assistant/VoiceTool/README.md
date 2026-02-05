# 🎙️ WANDA JARVIS - Sovereign AI Voice Assistant

Voice-powered AI assistant that controls your CLI tools (Gemini, OpenCode, Claude) with 3 operating modes.

## ✨ Features

- **Voice-to-AI**: Speak naturally, get AI responses read back
- **3 Modes**: Active (assisted), CLI-Proxy (inject to tools), Autonomous (full auto)
- **Smart Context**: Auto-refresh conversations, preserve knowledge
- **Local LLM**: Optional Ollama integration for prompt optimization
- **Multi-CLI**: Works with Gemini, OpenCode, Claude, Codex
- **German/English**: Bilingual support

## 🚀 Quick Start

```bash
# 1. Clone/navigate to directory
cd VoiceToolMVP

# 2. Run setup wizard
python3 setup.py

# 3. Start Wanda
./wanda
```

## 📋 Voice Commands

| Command | Action |
|---------|--------|
| `Wanda Pause` | Sleep mode |
| `Hallo Wanda` | Wake up |
| `Vollautonom` | Autonomous mode |
| `Lies mir vor` | Read last response |
| `Stopp` | Cancel current action |

## ⚙️ Requirements

### System
- Python 3.10+
- PipeWire/PulseAudio
- Microphone

### AI Tools (at least one)
- [Gemini CLI](https://ai.google.dev/gemini-api/docs/gemini-cli)
- [OpenCode](https://github.com/opencode-ai/opencode)
- [Claude Code](https://github.com/anthropics/claude-code)

### Optional
- [Ollama](https://ollama.com/) for local LLM

## 📦 Installation

### Local
```bash
python3 setup.py
./wanda
```

### Global
```bash
sudo ./install.sh
wanda  # from anywhere
```

### Systemd (autostart)
```bash
cp wanda.service ~/.config/systemd/user/
systemctl --user enable wanda
systemctl --user start wanda
```

## 🔧 Configuration

Edit `wanda.config.yaml`:

```yaml
# Ollama for local intelligence
ollama:
  enabled: true
  model: qwen2.5:32b

# TTS settings  
tts:
  voice: de_DE-eva_k-x_low
  mode: short  # short | full
```

## 📁 Structure

```
VoiceToolMVP/
├── main.py           # Entry point
├── setup.py          # Setup wizard
├── wanda             # Launcher script
├── wanda.config.yaml # Configuration
├── adapters/         # CLI + Ollama adapters
├── audio/            # Recording + VAD
├── conversation/     # Commands, context, state
├── modes/            # Autonomous mode
├── stt/              # Speech-to-text
├── tts/              # Text-to-speech
└── ui/               # Sounds + feedback
```

## 🎯 Modes

### 1️⃣ Active Mode
You're at keyboard, Wanda assists. Say "Wanda Pause" to sleep.

### 2️⃣ CLI-Proxy Mode
Voice input goes to active CLI tool. Responses read via TTS.

### 3️⃣ Autonomous Mode
Say "Vollautonom" - Wanda takes over, delegates tasks, reports progress.

## 📄 License

MIT

---

Made with ❤️ for sovereign AI workflows
