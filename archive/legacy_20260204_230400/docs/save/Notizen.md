# Notizen.md — WANDA Projekt-SSOT (intern) 🧠🛡️
Stand: 2026-02-04 (Europe/Berlin)

Zweck:
- **Interne** Master-Notizen (SSOT) für Planung, Bugs, Entscheidungen, Backlog, Research.
- Dient als Basis für: Issues, Implementierungs-Prompts, Repo-Docs, Installer-UX.

---

## 0) Kurzüberblick 🧭
WANDA ist ein „Sovereign AI OS“ / Jarvis-ähnliches System:
- **Voice-first** (lokal): VAD → STT → (optional Prompt-Improve via Ollama) → TTS → Confirm UI
- **Code/Agentic** (CLI/Cloud): OpenCode + Plugins + Multi-Provider + MCP
- Ziel: robust, token-effizient, cross-OS, release-ready.

---

## 1) System-Modi (Doppel-System) 🧩

### 1.1 Wanda Code System
Command:
- `wanda code`

Beschreibung:
- Startet optimiertes **OpenCode** mit Settings, Plugins, Prompts/Agenten, Provider/Auth, optionalen Zusatz-Plugins.

### 1.2 Wanda Voice System
Command:
- `wanda voice`
- `wanda voice --simple` (minimal/robust)

Run-Modes:
1) **mit Ollama** (Prompt-Verbesserer/Router, optional)
2) **ohne Ollama** (STT/TTS nur, für Nutzer ohne Ollama)

UX Pflicht:
- **Stille-Erkennung** (VAD) beendet Aufnahme automatisch
- danach Confirm-Step: `[Send] / [Edit] / [Redo] / [Cancel]`

### 1.3 Wanda (Global / Dual Mode)
Command:
- `wanda`

Beschreibung:
- Startet Voice + Code zusammen (ohne Duplikate), optional Banner/Status/Update-Check.

---

## 2) Ordner-Rollen (lokal) 📁

### OpenCode
- `.opencode`: entsteht durch OpenCode-Installation/Runtime
- Config: `~/.config/opencode`
- Cache/Runtime: `~/.cache/opencode`
- Auth/State: typischerweise `~/.local/share/opencode` (abhängig vom Setup)

### Gemini CLI
- `~/.gemini/GEMINI.md` (Global Context)
- `~/.gemini/system.md` (System Prompt; aktiv via `GEMINI_SYSTEM_MD`)
- `~/.gemini/settings.json` (Config, MCP, Keys)

### Claude Code
- `~/.claude/CLAUDE.md` (Global Context)
- `~/.claude/settings.json` (Config/Permissions)
- `~/.claude/skills/` (Skills)

### Codex CLI
- `~/.codex/config.toml` (Config/Keys)
- `~/.codex/instructions.md` (System Prompt)
- Projekt-Context: `AGENTS.md` im Repo-Root

---

## 3) Core-Stack (OpenCode + Plugins) 🧱
Ziel:
- Stabile OpenCode-Basis + Plugin-Stack ohne Agenten-Duplikate/Config-Drift.

Komponenten:
- Core: OpenCode
- Plugins:
  - `oh-my-opencode@3.2.1`
  - `micode@latest`
  - optional: `opencode-orchestrator`
- Zusätzlich (optional, aber aktuell relevant):
  - `opencode-context-analysis@latest`
  - `opencode-shell-strategy@latest`
  - `opencode-notifier@latest`

Zielzustand:
- Keine doppelten Agentenrollen, keine stillen Konflikte
- deterministische Config-Load-Order
- cross-OS lauffähig + Installer/Update-UX sauber

---

## 4) Aktuelle & bekannte Probleme (Incidents / Risiken) 🚨

### P0 — Agenten-Overlaps / Config-Overrides werden „zurückgesetzt“
Symptom:
- Unklar, ob System-/Plugin-Agenten sauber deaktiviert/umgestellt werden können.
- Änderungen (z. B. Agent-Namen/Modelle) scheinen beim Start wieder rückgängig gemacht zu werden.

Impact:
- Unvorhersehbares Routing, Token-/Zeitverschwendung, Debugging schwer („Config drift“).

To-Do (Fix-Strategie):
1) Standardisieren, **WO** konfiguriert wird (global vs project) + Load-Order dokumentieren.
2) „Config-Lock“: pro Layer genau 1 Source of Truth:
   - Core: `opencode.json/jsonc`
   - oh-my: `oh-my-opencode.json`
   - micode: `micode.json`
3) Prüfen, ob Start-time Rewrite/Generators aktiv sind (Hooks/Auto-Generators).

---

### P0 — micode verursacht (scheinbar) Anthropic Credential Errors
Symptom:
- Anthropic Modelle werfen Credential/Authorization Errors (scheinbar bei micode).

Regel:
- Erst isolieren, dann beschuldigen.

Isolations-Testplan:
1) Snapshot: Configs + auth.json sichern (read-only Kopie).
2) Matrix:
   - A) OpenCode ohne Plugins
   - B) nur micode
   - C) nur oh-my-opencode
   - D) micode + oh-my
3) Pro Test: 1x `/models`, 1x Prompt, Logs sichern + Ergebnis-Tabelle.

---

### P0 — BunInstallFailedError / Multi-OS „Plugin-Verlust“-Risiko
Symptom:
- `bun install` fails beim Plugin/Dependency Install.
- Explizit betroffen (dein Stack): context-analysis, shell-strategy, notifier.

Mitigation:
1) Version pinning (kein `@latest` auf kritischen Pfaden).
2) Cache-stable Update Scripts (Cache + node_modules reset).
3) Netzwerk/Proxy/Cert Diagnose in Installer aufnehmen.
4) Windows: bevorzugt offiziellen Installer/Binaries statt bun-global install.

---

### P1 — Google Modelle via normalen OAuth (nicht Antigravity) → API Probleme
Symptom:
- Google Modelle über regulären OAuth machen API Probleme.
- Unklar, ob „Fallback“ auf Antigravity wirklich greift.

To-Do:
1) „Primary Google Path“ entscheiden: Standard-Provider ODER Antigravity OAuth Plugin.
2) Fallback-Verhalten **testen** und ggf. **explizit implementieren** (nicht hoffen).

---

## 5) Epics / Backlog (Issue-ready) ✅

### EPIC A — Docs/UX: AI_INSTALLATION.md als „One True Install Doc“
Ziel:
- README kurz (2 Zeilen + Link), alle Details in `docs/AI_INSTALLATION.md`
- `docs/AI_INSTALL_PROMPT.md` max 3 Zeilen

Deliverables:
- `/README.md` (kurz)
- `/docs/AI_INSTALLATION.md` (vollständig, troubleshooting-first)
- `/docs/AI_INSTALL_PROMPT.md` (3 Zeilen)
- Issue Template „Installation Problem“ + Log-Anleitung

---

### EPIC B — State Audit + Gegen-Research + SOTA Upgrades
Agent-Rollen:
1) Auditor (Inventory)
2) Compatibility Researcher (OS/bun/auth)
3) SOTA Upgrader (Prompts/Struktur)
4) Agent-Config Expert (Load-Order, Overrides, Deaktivierung)

Outputs:
- `INVENTORY.md`, `CONFLICTS.md`, `DECISIONS.md`, `TASKS.md`

---

### EPIC C — Wanda Doppel-System funktionsfähig (single + dual mode)
Ziel:
- `wanda`, `wanda code`, `wanda voice` stabil + cross-OS.

---

### EPIC D — Installer: Fresh / Reinstall / Update (UX-first)
Ziel:
- Guided Setup (Name, Work-OS, Keys, MCP hub, Voice demos)
- Reinstall ohne Zwangs-Reset
- Update Mode + optional Auto-Update-on-next-launch

---

### EPIC E — Hardening (Owner-mode)
Ziel:
- Sicherheit, Reliability, Performance, Token-Effizienz
- Smoke Tests + Audit Pipeline
- Keine „magischen“ Defaults ohne Erklärung

---

### EPIC F — Agenten & Plugins harmonisieren (Overlaps eliminieren)
Outputs:
- `AGENTS_INVENTORY.md`, `AGENTS_CLUSTERING.md`, `AGENTS_FINAL.md`, `CONFIG_MAP.md`

---

### EPIC G — Finale „V0 Skills“
Ziel:
- Wiederverwendbare Skill-Pipelines:
  - Web/App generation
  - n8n workflow generation/deploy/fix
  - repo hardening / install+update / incident triage

---

## 6) Install/Run-Skizzen (Notiz-Referenz) 🧪
Repo-Clone (für KI-Installflows):
```bash
git clone https://github.com/jas0nOW/wanda-agentic-system.git ~/.wanda-system
cd ~/.wanda-system
chmod +x install.sh
./install.sh
```

Debug:
```bash
wanda -d
```

---

## 7) Research & Links (Primärquellen + Entry Points) 🔎
OpenCode / Plugins:
- OpenCode ecosystem: https://opencode.ai/docs/ecosystem/
- OpenCode plugins: https://opencode.ai/docs/plugins/
- OpenCode troubleshooting: https://opencode.ai/docs/troubleshooting/
- oh-my-opencode configurations: https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/configurations.md
- micode repo: https://github.com/vtemian/micode
- opencode-orchestrator (npm): https://www.npmjs.com/package/opencode-orchestrator

Voice Stack:
- Silero VAD: https://github.com/snakers4/silero-vad
- Whisper: https://github.com/openai/whisper
- whisper.cpp: https://github.com/ggml-org/whisper.cpp
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- edge-tts (Edge voices): https://github.com/rany2/edge-tts
- Coqui XTTS docs: https://docs.coqui.ai/en/latest/models/xtts.html
- PyTorch install matrix: https://pytorch.org/get-started/locally/

---

## 8) Definition of Done ✅
- OpenCode startet ohne Konflikte
- Plugins laufen zusammen (oh-my, micode, optional orchestrator) ohne Agent-Duplikate
- Overrides/Deaktivierungen sind reproduzierbar (kein „Reset“ beim Start)
- Voice: VAD silence-detect + confirm UI + stabile STT/TTS defaults + timeouts
- Installer: fresh/reinstall/update stabil + cross-OS
- Docs: README kurz, AI_INSTALLATION vollständig, Issue-Flow sauber
- SSOT: keine widersprüchlichen Infos

---

## 9) Nächste Schritte ▶️
1) EPIC A: README + AI_INSTALLATION + AI_INSTALL_PROMPT + Issue Template
2) EPIC F: Agent Inventory → Clustering → Final Set → Smoke Tests
3) EPIC H (Voice): VAD silence-detect + confirm UI + STT/TTS defaults + timeouts
