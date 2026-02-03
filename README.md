# WANDA Sovereign AI OS 🚀🤖🛡️

> **A Hybrid AI Operating System combining Local Voice Intelligence with Cloud Agentic Power.**

[![Version](https://img.shields.io/badge/version-1.0.4-blue)](https://github.com/jas0nOW/wanda-agentic-system)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## Overview

WANDA (Workspace-Aware Neural Development Assistant) is a **Sovereign AI OS**:

- **17 Specialized Agents** powered by Claude 4.5, Gemini 3, Codex 5.2
- **9 Layer Architecture** (Brainstorming → Deploy)
- **Voice-First Interface** with Wanda-Mode (full autonomy)
- **Docker MCP Gateway** with 18 servers

---

## 🌟 Quick Start

```bash
# One-line install (RECOMMENDED)
curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
```

After installation:

```bash
wanda              # Start WANDA (shows banner, opens AI CLI)
wanda -d           # Debug mode (check for errors)
wanda update       # Check and apply updates
wanda status       # Show system status
wanda voice        # Start voice assistant
```

---

## 🤖 AI Installation (Für KI-Assistenten)

Die KI kann WANDA mit folgendem Workflow installieren:

### Step 1: Repo klonen
```bash
git clone https://github.com/jas0nOW/wanda-agentic-system.git ~/.wanda-system
cd ~/.wanda-system
```

### Step 2: Installer ausführen
```bash
chmod +x install.sh
./install.sh
```

### Step 3: Bei Problemen
```bash
wanda -d   # Debug mode - zeigt Fehler nach 10/20 Sek
```

### Edge Cases & Fixes

| Problem | Lösung |
|---------|--------|
| **Freeze beim Start** | `npm cache clean --force && npm install -g @anthropic-ai/opencode` |
| **Voice Assistant freeze** | `pip uninstall torch && pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| **Permission denied** | `sudo chown -R $USER:$USER ~/.wanda-system` |
| **API errors** | API-Keys in `~/.gemini/settings.json` prüfen |
| **Missing packages** | `pip install -r requirements.txt` |
| **MCP not connecting** | Docker starten: `systemctl start docker` |

### Dateien die die KI kennen sollte

| Datei | Zweck |
|-------|-------|
| `install.sh` | Hauptinstaller (interaktiv) |
| `bin/wanda` | CLI wrapper |
| `scripts/update.sh` | Update system |
| `config/agents.yaml` | Agent-Konfiguration |
| `config/voice_commands.yaml` | Voice-Kommandos |
| `~/.gemini/GEMINI.md` | System prompt |
| `~/.gemini/settings.json` | MCP & API keys |

---

## System Requirements

| Profile | VRAM | RAM | Recommended Model |
|---------|------|-----|-------------------|
| **S** | 0-4GB | 8-16GB | `llama-3.2:3b` |
| **M** | 6-8GB | 16-32GB | `gemma-3:9b` |
| **M-High** | 10-12GB | 32-48GB | `qwen-2.5-coder:14b` |
| **High** | 16+GB | 48+GB | `deepseek-r1:32b` |

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
│               WANDA CLOUD CORE (17 Agents)              │
│  Sisyphus (Orchestrator) → Prometheus → Atlas → Audit  │
│  Claude 4.5 / Gemini 3 / Codex 5.2                     │
└─────────────────────────────────────────────────────────┘
```

### 9 Layers
1. Brainstorming → 2. Planning → 3. Architecture → 4. Development
5. Audit → 6. Refactor → 7. Testing → 8. User-Approval → 9. Deploy

---

## MCP Servers (Docker Hub)

| Server | Zweck |
|--------|-------|
| `github` | Repository-Ops |
| `brave` | Web-Suche |
| `playwright` | Browser-Automation |
| `context7` | Library Docs |
| `supermemory` | Persistent Context |
| `filesystem` | Datei-Operationen |

---

## Voice Commands

```bash
wanda voice   # Start Voice Assistant
```

| Command | Action |
|---------|--------|
| "Hallo Wanda" | Wake/Resume |
| "Bestätige" | Send prompt |
| "Stop" | Cancel task |
| "Vorlesen" | Read back |
| "Wanda Modus" | Full autonomy |

---

## Debug Mode

```bash
wanda -d
```

- Startet WANDA mit Error-Monitoring
- Prüft nach 10 und 20 Sekunden
- Bei Problemen: Diagnose-Optionen
  - "Ja" - Läuft
  - "Freezed" - Package-Fix Anleitung
  - "Eigene Antwort" - Problem-Analyse

---

## License

MIT © 2026

---

*WANDA v1.0.4 - Sovereign AI Operating System*
