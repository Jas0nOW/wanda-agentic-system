# WANDA Sovereign AI OS 🚀🤖🛡️
> **A Hybrid AI Operating System combining Local Voice Intelligence with Cloud Agentic Power.**

[![Version](https://img.shields.io/badge/version-1.0.5-blue)](https://github.com/jas0nOW/wanda-agentic-system)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview
WANDA (Workspace-Aware Neural Development Assistant) is a **Sovereign AI OS**:

- 🧠 **Specialized Agents** (multi-model: Claude / Gemini / Codex / optional others)
- 🧱 **Layer Architecture** (Brainstorming → Deploy)
- 🎙️ **Voice-First Interface** with Wanda-Mode (full autonomy optional)
- 🔌 **Docker MCP Gateway** (tooling via servers)

### Layers (human-readable)
1. **Orchestrator** is the only interface you talk to.
2. It can do fast brainstorming + short research, then creates a **Project Note** (goal, scope, constraints).
3. An **Architect** creates a safe, long-term workspace structure + stack decisions.
4. **Developers** implement (Frontend/UI, Backend, Ops).
5. An **Auditor** compares implementation vs plan, hunts bugs/edge cases/safety issues, and runs “break tests”.
6. If everything is green across all agents: you get a **deployment prompt**.
7. If anything fails or you reject: iterate, fix, update docs, keep a changelog.

---

## 🌟 Quick Start

### 🤖 AI AUTO INSTALL (RECOMMENDED)
Copy/paste this into your CLI coding agent (OpenCode / Claude Code / Codex / Gemini CLI):

```txt
Install this GitHub repo: https://github.com/jas0nOW/wanda-agentic-system
Run the installer:
  curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
Then follow the repo install guide: docs/AI_INSTALLATION.md (includes edge cases + fixes).
If anything fails: run `wanda -d`, collect logs, and open a GitHub Issue using the provided template.
```

### 🧑‍💻 One-line install (MANUAL NORMAL MODE)
```bash
curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
```

### After installation
```bash
wanda                 # Start WANDA (banner + OpenCode + Voice, no duplication)
wanda -d              # Debug mode (health checks + logs)
wanda update          # Check and apply updates
wanda status          # Show system status
wanda code            # Start only coding assistant (Wanda OpenCode System)
wanda voice           # Start voice assistant
wanda voice --simple  # Voice minimal/robust mode (no GUI)
```

---

## Workspace Hygiene (Pflicht) 🧹
- Änderungen an Dateien erst nach Lesen.
- Nichts löschen außer offensichtlichem Müll; sonst nach `archive/` verschieben.
- Backups minimal halten: pro Datei 1–2 Versionen.
- Wenn fertig oder zu viel Müll: aufräumen, sortieren, Ordnung herstellen.

---

## 🤖 AI Installation (Für KI-Assistenten)

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

✅ **Full guide (SSOT):** `docs/AI_INSTALLATION.md`  
🧠 **Tiny AI prompt:** `docs/AI_INSTALL_PROMPT.md`

---

## Edge Cases & Fixes (Common)
> For the full list (OS-specific): see `docs/AI_INSTALLATION.md`.

| Problem | Lösung |
|---------|--------|
| **Freeze beim Start** | `npm cache clean --force && npm install -g @anthropic-ai/opencode` |
| **Voice Assistant freeze** | `pip uninstall torch && pip install torch --index-url https://download.pytorch.org/whl/cpu` |
| **Permission denied** | `sudo chown -R $USER:$USER ~/.wanda-system` |
| **API errors** | API-Keys prüfen (Gemini/Claude/Codex configs) |
| **Missing packages** | `pip install -r requirements.txt` |
| **MCP not connecting** | Docker starten: `systemctl start docker` |

---

## Files the AI should know 📁

| File / Folder | Path | Purpose |
| :--- | :--- | :--- |
| `install.sh` | repo root | Main installer (interactive) |
| `bin/wanda` | repo root | CLI wrapper |
| `scripts/update.sh` | repo root | Update system |
| `config/agents.yaml` | repo root | Agent configuration |
| `config/voice_commands.yaml` | repo root | Voice commands |
| `GEMINI.md` | `~/.gemini/GEMINI.md` | Global AI context / memory |
| `system.md` | `~/.gemini/system.md` | Gemini system prompt (via `GEMINI_SYSTEM_MD`) |
| `settings.json` | `~/.gemini/settings.json` | Gemini config, MCP & API keys |
| `CLAUDE.md` | `~/.claude/CLAUDE.md` | Claude global context |
| `settings.json` | `~/.claude/settings.json` | Claude config & permissions |
| `skills/` | `~/.claude/skills/` | Modular Claude skills |
| `config.toml` | `~/.codex/config.toml` | Codex CLI config & API keys |
| `instructions.md` | `~/.codex/instructions.md` | Codex global system rules |
| `AGENTS.md` | `./AGENTS.md` | Shared agent context (Codex/Gemini/Claude) |

---

## CLI Config Cheatsheet

### Google Gemini CLI (Agent Mode)
- Config: `~/.gemini/settings.json`
- Context: `~/.gemini/GEMINI.md`
- System: `~/.gemini/system.md` (activate via `export GEMINI_SYSTEM_MD=~/.gemini/system.md`)

### Claude Code (Anthropic)
- Config: `~/.claude/settings.json`
- Context: `~/.claude/CLAUDE.md`
- Skills: `~/.claude/skills/`

### Codex CLI (OpenAI)
- Config: `~/.codex/config.toml`
- Instructions: `~/.codex/instructions.md`
- Agent Context: `AGENTS.md` (repo root)

---

## System Requirements 💻

| Profile | VRAM | RAM | Recommended Model |
|---------|------|-----|-------------------|
| **S** | 0–4GB | 8–16GB | `llama-3.2:3b` |
| **M** | 6–8GB | 16–32GB | `gemma-3:9b` |
| **M-High** | 10–12GB | 32–48GB | `qwen-2.5-coder:14b` |
| **High** | 16+GB | 48+GB | `deepseek-r1:32b` |

---

## Architecture 🧱

```
┌─────────────────────────────────────────────────────────┐
│                    USER (Voice/Chat)                    │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│               WANDA LOCAL GATEWAY                       │
│  Silero VAD → Whisper STT → Ollama → XTTS-v2 / Edge TTS │
│  Safety Checker → Confirm UI → CLI Injector             │
└─────────────────────┬───────────────────────────────────┘
                      ▼
┌─────────────────────────────────────────────────────────┐
│               WANDA CLOUD/CLI CORE (Agents)             │
│  Orchestrator → Planning → Dev → Audit → Deploy         │
│  (Claude / Gemini / Codex / optional others)            │
└─────────────────────────────────────────────────────────┘
```

### 9 Layers
1. Brainstorming → 2. Planning → 3. Architecture → 4. Development  
5. Audit → 6. Refactor → 7. Testing → 8. User-Approval → 9. Deploy

---

## MCP Servers (Docker)
| Server | Zweck |
|--------|-------|
| `github` | Repository ops |
| `brave` | Web search |
| `playwright` | Browser automation |
| `context7` | Library docs |
| `supermemory` | Persistent context |
| `filesystem` | File operations |

> Full list + compose file: see `docs/AI_INSTALLATION.md` / upcoming `docs/MCP.md`.

---

## Voice Commands 🎙️
```bash
wanda voice
```

| Command | Action |
|---------|--------|
| "Hallo Wanda" | Wake/Resume |
| "Bestätige" | Send prompt |
| "Stop" | Cancel task |
| "Vorlesen" | Read back |
| "Wanda Modus" | Full autonomy |

---

## Debug Mode 🧪
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

## Desktop App & Compatibility 🖥️
- Linux (X11/Wayland): use `wanda voice` or the generated `Wanda.desktop` launcher in `wanda-voice/`.
- Windows: use `wanda_voice.bat` (runs via WSL).
- macOS: run `wanda voice --simple` from Terminal for the most reliable startup.

---

## Auto-Update & Banner Style 🔁
- Auto-update on launch: `WANDA_AUTO_UPDATE=1 wanda`
- Banner style: `WANDA_BANNER_STYLE=animated|minimal wanda`
- One-off animated banner: `WANDA_BANNER_ANIMATED=1 wanda`

---

## License
MIT © 2026

*WANDA v1.0.5 — Sovereign AI Operating System*
