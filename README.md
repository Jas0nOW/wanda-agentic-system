<div align="center">

# 🌟 WANDA Agentic System

**Sovereign AI OS with 17 Agents + Voice Assistant**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-green.svg)](https://python.org)
[![OpenCode](https://img.shields.io/badge/OpenCode-Compatible-purple.svg)](https://opencode.ai)

*A complete AI development environment with multi-agent orchestration, voice control, and seamless tool integration.*

[Installation](#-installation) • [Features](#-features) • [Configuration](#-configuration) • [Usage](#-usage) • [Documentation](#-documentation)

---

</div>

## 🎯 Overview

WANDA is a comprehensive AI system consisting of two main components:

| Component | Description |
|-----------|-------------|
| **🤖 Agent System** | 17 specialized AI agents with orchestration, from architecture to code review |
| **🎤 Voice Assistant** | Local-first voice interface with STT, TTS, multiple modes, and mobile access |

```
┌─────────────────────────────────────────────────────────────────┐
│                      WANDA AGENTIC SYSTEM                       │
├────────────────────────────┬────────────────────────────────────┤
│     🤖 Agent System        │        🎤 Voice Assistant          │
│  ┌──────────────────────┐  │  ┌────────────────────────────┐   │
│  │ Orchestration Layer  │  │  │ Premium Siri-Style Orb     │   │
│  │ • Sisyphus (Flash)   │  │  │ • Click = Daily Start      │   │
│  ├──────────────────────┤  │  │ • Drag = Move              │   │
│  │ Core Layer           │  │  ├────────────────────────────┤   │
│  │ • Architect (Opus)   │  │  │ Multi-Mode                 │   │
│  │ • Software-Engineer  │  │  │ • Aktiv, Paused            │   │
│  │ • Audit (Opus)       │  │  │ • Autonomous, CLI-Proxy    │   │
│  ├──────────────────────┤  │  ├────────────────────────────┤   │
│  │ Specialist Layer     │  │  │ Mobile Access              │   │
│  │ • Oracle, Writer...  │  │  │ • Telegram Bot             │   │
│  └──────────────────────┘  │  │ • Push Notifications       │   │
│                            │  └────────────────────────────┘   │
└────────────────────────────┴────────────────────────────────────┘
```

---

## 🚀 Installation

### One-Command Install (Recommended)

```bash
curl -fsSL https://raw.githubusercontent.com/LazyTechLab/wanda-agentic-system/main/install.sh | bash
```

### Manual Installation

```bash
# 1. Clone repository
git clone https://github.com/LazyTechLab/wanda-agentic-system
cd wanda-agentic-system

# 2. Run installer
chmod +x install.sh
./install.sh
```

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| OS | Linux (Ubuntu 22.04+) | Pop!_OS / Fedora |
| Python | 3.10+ | 3.11+ |
| RAM | 4 GB | 16 GB |
| GPU | - | NVIDIA (CUDA) |
| Display | Wayland/X11 | Wayland |

<details>
<summary><strong>📦 Dependencies</strong></summary>

**System packages:**
```bash
sudo apt install python3 python3-pip python3-venv git ffmpeg
sudo apt install portaudio19-dev libasound2-dev  # For audio
sudo apt install libgirepository1.0-dev gir1.2-gtk-3.0  # For orb UI
```

**Python packages:** (installed automatically)
- `faster-whisper` - Local STT
- `piper-tts` - Local TTS
- `sounddevice`, `scipy`, `numpy` - Audio
- `evdev` - Hotkey handling
- `PyGObject` - GTK orb
- `python-telegram-bot` - Mobile access

</details>

---

## ✨ Features

### 🤖 Agent System (17 Agents)

<table>
<tr>
<th>Layer</th>
<th>Agents</th>
<th>Model</th>
</tr>
<tr>
<td><strong>Orchestration</strong></td>
<td>Sisyphus</td>
<td>Gemini 3 Flash</td>
</tr>
<tr>
<td><strong>Ideation</strong></td>
<td>Brainstormer</td>
<td>Gemini 3 Pro</td>
</tr>
<tr>
<td><strong>Core</strong></td>
<td>Architect, Software-Engineer, Frontend-UI-UX, Audit</td>
<td>Claude Opus / Sonnet</td>
</tr>
<tr>
<td><strong>Specialist</strong></td>
<td>Oracle, Writer, Librarian, Explore, Multimodal-Looker</td>
<td>Mixed</td>
</tr>
<tr>
<td><strong>Research</strong></td>
<td>Codebase-Locator, Codebase-Analyzer, Pattern-Finder</td>
<td>Gemini Flash</td>
</tr>
<tr>
<td><strong>Continuity</strong></td>
<td>Ledger-Creator, Artifact-Searcher</td>
<td>Gemini Flash</td>
</tr>
<tr>
<td><strong>Meta</strong></td>
<td>Metis, Momus</td>
<td>Claude Opus Thinking</td>
</tr>
</table>

### 🎤 Voice Assistant

| Feature | Description |
|---------|-------------|
| **Local STT** | Whisper (tiny → large) with CUDA acceleration |
| **Local TTS** | Piper with German voice, <200ms interrupt |
| **Premium Orb** | Siri-style animations, particle effects |
| **Multi-Mode** | Aktiv, Paused, Autonomous, CLI-Proxy |
| **Wake Word** | "Hey Wanda", "Hey Jarvis" (optional) |
| **Mobile** | Telegram bot + push notifications |
| **Wayland** | Full support for COSMIC, GNOME, KDE |

### 🔌 MCP Integration

Preconfigured for 14+ MCP servers:
- `brave`, `filesystem`, `memory`, `github`
- `supabase`, `vercel`, `docker`, `playwright`
- And more...

---

## ⚙️ Configuration

### Agent System

```bash
# Location
~/.config/opencode/profiles/

# Profiles available
├── opencode.jsonc          # Main config
├── stable/opencode.json    # Minimal (1 agent)
└── experimental/opencode.json  # Full (17 agents)
```

**Switch profiles:**
```bash
opencode --profile experimental
```

**Add Antigravity account:**
```json
// ~/.config/opencode/antigravity-accounts.json
{
  "accounts": [
    { "email": "your@email.com", "token": "YOUR_TOKEN" }
  ]
}
```

### Voice Assistant

```yaml
# ~/.wanda-system/wanda-voice/wanda.config.yaml

mode: aktiv
audio:
  sample_rate: 16000
  record_seconds: 20
  silence_threshold: 0.2

stt:
  engine: faster-whisper
  model: small
  device: cuda  # or cpu

tts:
  engine: piper
  voice: de_DE-eva_k-x_low

# Optional: Telegram
telegram:
  enabled: true
  token: "YOUR_BOT_TOKEN"

# Optional: Push notifications
notifications:
  enabled: true
  topic: "wanda-private"
```

### MCP Servers

```json
// ~/.gemini/settings.json
{
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"]
    }
  }
}
```

---

## 📖 Usage

### Agent System

```bash
# Start with orchestrator
opencode

# Use specific agent
@brainstormer "Design a REST API"

# Full autopilot workflow
/ralph-loop "Build authentication system"
```

### Voice Assistant

```bash
# Start
wanda

# Or with options
wanda --mode autonomous
wanda --no-orb
```

**Voice Commands:**
| Command | Action |
|---------|--------|
| *Click orb* | Daily Start (morning) or toggle recording |
| "Wanda Pause" | Go to sleep |
| "Hallo Wanda" | Wake up |
| "Vollautonom" | Enter autonomous mode |

**Telegram Commands:**
```
/start     - Welcome message
/status    - System status
/projekt   - Create project in Work-OS
/idee      - Capture idea
```

---

## 📁 Project Structure

```
wanda-agentic-system/
│
├── wanda-voice/              # 🎤 Voice Assistant
│   ├── audio/                # Recording, VAD
│   ├── stt/                  # Speech-to-text
│   ├── tts/                  # Text-to-speech
│   ├── adapters/             # Gemini, Ollama, CLI
│   ├── conversation/         # State, context, commands
│   ├── modes/                # Autonomous, Daily Init
│   ├── mobile/               # Telegram, notifications
│   ├── ui/                   # GTK Orb
│   └── wanda                 # Entry point
│
├── wanda-agents/             # 🤖 Agent System
│   ├── profiles/             # OpenCode configurations
│   │   ├── stable/
│   │   └── experimental/
│   └── GEMINI.md             # System kernel
│
├── mcp-servers/              # 🔌 MCP Integration
│   └── settings.json.template
│
├── docs/                     # 📚 Documentation
│   ├── architecture/
│   ├── guides/
│   └── workflows/
│
├── templates/                # 📝 Templates
├── install.sh                # Installer
└── README.md                 # This file
```

---

## 🔄 Updates

```bash
cd ~/.wanda-system
git pull
./install.sh
```

---

## 🤝 Contributing

See [docs/guides/contributing.md](docs/guides/contributing.md)

```bash
# Fork, clone, create branch
git checkout -b feature/my-feature

# Make changes, commit
git commit -m "feat: add amazing feature"

# Push and create PR
git push origin feature/my-feature
```

---

## 📜 License

MIT © [LazyTechLab](https://github.com/LazyTechLab)

---

<div align="center">

**Made with ❤️ by Jannis**

[⬆ Back to top](#-wanda-agentic-system)

</div>
