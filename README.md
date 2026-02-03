# WANDA Sovereign AI OS 🚀🤖🛡️

> **A Hybrid AI Operating System combining Local Voice Intelligence with Cloud Agentic Power.**

[![Version](https://img.shields.io/badge/version-1.0.3-blue)](https://github.com/jas0nOW/wanda-agentic-system)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Overview

WANDA (Workspace-Aware Neural Development Assistant) is a **Doppel-Wanda System**:

1. **🟢 Local Gateway**: Voice Activity Detection, Speech-to-Text, Prompt Refinement (Ollama), Safety Checks, TTS.
2. **🔵 Cloud Core**: 17 Specialized Agents powered by Claude 4.5 & Gemini 3 via OpenCode.

---

## 🌟 Quick Start (AI Installer - EMPFOHLEN)

Der **personalisierte Installer** fragt nach deinem Namen, Arbeitsordner und Sprache - so funktioniert WANDA sofort für dich!

```bash
# One-line install (RECOMMENDED)
curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
```

Oder manuell:

```bash
git clone https://github.com/jas0nOW/wanda-agentic-system.git ~/.wanda-system
cd ~/.wanda-system
chmod +x install.sh
./install.sh
```

> **📖 Vollständige Anleitung**: [docs/INSTALLATION.md](docs/INSTALLATION.md)

---

## System Requirements

| Tier | RAM | Recommended Model | Capability |
|---|---|---|---|
| **S** | < 8GB | `qwen3:8b` | Basic routing |
| **M** | 16GB | `heretic-12b` | Voice interaction |
| **MH** | 50GB+ | `brainstorm-36b` | Full Gateway (Your Setup) |
| **G** | 64GB+ | `deepseek-v4` | Local autonomy |

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    USER (Voice/Chat)                    │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│               WANDA LOCAL GATEWAY                       │
│  Silero VAD → Whisper STT → Ollama → XTTS-v2 TTS       │
│  Safety Checker → CLI Injector                          │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│               WANDA CLOUD CORE                          │
│  OpenCode + oh-my-opencode (Leader)                     │
│  17 Agents: Architect, Developer, Oracle, ...           │
│  Claude 4.5 / Gemini 3                                  │
└─────────────────────────────────────────────────────────┘
```

---

## MCP Server (Docker Hub)

WANDA nutzt Docker als zentralen MCP Hub mit 8+ Servern:

| Server | Zweck |
|--------|-------|
| `MCP_DOCKER` | Gateway Hub |
| `filesystem` | Datei-Operationen |
| `memory` | Wissens-Speicher |
| `github` | Repository-Ops |
| `brave` | Web-Suche |
| `playwright` | Browser-Automation |
| `sequential-thinking` | Step-by-Step Reasoning |
| `context7` | Library Documentation |

> Der Installer konfiguriert alle MCP Server automatisch!

---

## Directory Structure

```
wanda-agentic-system/
├── install.sh              # 🌟 Personalized Installer
├── docs/
│   ├── INSTALLATION.md     # Full setup guide
│   └── WANDA_MASTER_BLUEPRINT_DE.md
├── prompts/
│   ├── system/             # OLLAMA_SYSTEM.md, TERMINAL_POLICY.md
│   └── context/            # MCP_TOOL_MAPPING.md, AGENT_REGISTRY.md
├── templates/
│   └── GEMINI.md.template  # Personalized system prompt
├── mcp-servers/
│   └── settings.json.template
├── wanda_local/            # Voice Gateway (Python)
├── wanda_cloud/            # OpenCode profiles
├── scripts/                # diagnostics.sh, deploy-hook.sh
└── tests/                  # Smoke tests
```

---

## Profiles

- **Stable** (Daily Driver): `oh-my-opencode` only. Minimal conflicts.
- **Experimental** (Lab): Multi-agent swarm with orchestrator.

Switch profiles:
```bash
# Use stable
ln -sf ~/.wanda-system/wanda_cloud/profiles/stable/opencode.jsonc ~/.config/opencode/opencode.jsonc

# Use experimental
ln -sf ~/.wanda-system/wanda_cloud/profiles/experimental/opencode.jsonc ~/.config/opencode/opencode.jsonc
```

---

## Voice Commands

Start the Voice Gateway:
```bash
cd ~/.wanda-system/wanda_local && source venv/bin/activate && python main.py
```

Commands:
- **"Hey Wanda"**: Wake word
- **"Guten Morgen"**: Get status briefing
- **Any voice input**: Transcribed → Refined → Routed to agent

---

## Telegram Bot

```bash
# Token in .env
echo 'WANDA_TELEGRAM_BOT_TOKEN="your_token"' > ~/.wanda-system/wanda_local/.env

# Start
python ~/.wanda-system/wanda_local/telegram_bot.py
```

---

## Safety

- **Denylist**: `rm -rf /`, `cat /etc/shadow` → BLOCKED
- **Confirmlist**: `git push --force`, `sudo` → Requires confirmation
- **Secrets**: `.env` files are never committed

---

## License

MIT © 2026

---

*WANDA - Sovereign AI Operating System v1.0.1*
