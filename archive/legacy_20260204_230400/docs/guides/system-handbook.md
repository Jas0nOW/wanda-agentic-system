# OpenCode System Handbuch (v2)

## Uebersicht

Dieses System nutzt **9 spezialisierte AI-Agenten** mit **15 SOTA-Modellen** ueber **5 Provider**.

---

## Agent-Team

| Agent | Rolle | Engine | Aufgabe |
|-------|-------|--------|---------|
| ⚡ **Sisyphus** | Orchestrator | Gemini 3 Flash | Quick-Help + Workflow-Steuerung |
| 🏗️ **Architect** | The Grounder | Claude 4.5 Opus | Tech Stack & Blueprint |
| 🛠️ **Developer** | The Builder | Claude 4.5 Sonnet | Feature-Implementierung |
| 🛡️ **Audit** | The Fixer | GPT-5.2 Codex | Find-Break-Fix |
| 🎨 **UI/UX** | The Designer | Gemini 3 Pro | Frontend & Visuals |
| 🏛️ **Oracle** | Deep Thinker | Claude 4.5 Opus | Komplexe Logik |
| 📝 **Writer** | The Scribe | Gemini 3 Flash | Dokumentation |
| 📚 **Librarian** | Researcher | Gemini 3 Flash | Wissensabruf |
| 🔍 **Explore** | Scout | Gemini 3 Flash | Kontext-Scanning |

---

## 3-Phasen-Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                     PHASE 1: GROUNDING                      │
│                    ┌───────────────┐                        │
│       User ───────►│   Architect   │──────► blueprint.md    │
│                    │  (Claude Opus)│                        │
│                    └───────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PHASE 2: BUILDING                       │
│                    ┌───────────────┐                        │
│    Blueprint ─────►│   Developer   │──────► Code            │
│                    │(Claude Sonnet)│                        │
│                    └───────────────┘                        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                     PHASE 3: FIXING                         │
│                    ┌───────────────┐                        │
│       Code ───────►│     Audit     │──────► Production      │
│                    │    (Codex)    │                        │
│                    └───────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Fallback-Matrix (Infinite Chain)

**Beispiel: Developer**
```
antigravity/claude-sonnet-4-5
       ↓ (wenn erschoepft)
anthropic/claude-sonnet-4-5
       ↓ (wenn erschoepft)
github/claude-sonnet-4-5
       ↓ (wenn erschoepft)
google/gemini-3-pro-preview
       ↓ (wenn erschoepft)
openai/gpt-5.2-codex
```

**Provider:**
1. ⚡ Antigravity (Primary)
2. 🟣 Anthropic
3. 🐙 GitHub Copilot
4. 🔵 Google
5. 🟢 OpenAI

---

## Befehle

| Befehl | Aktion |
|--------|--------|
| `/init-deep` | Projekt initialisieren |
| `/ralph-loop "Task"` | Autonomen Workflow starten |
| `@architect "Idee"` | Blueprint erstellen lassen |
| `@audit` | Security-Review starten |

---

## Status

- **Agenten**: 9 konfiguriert
- **Modelle**: 15 verfuegbar
- **Provider**: 5 aktiv
- **Fallback**: Infinite Chain aktiviert

**Bereit zum Bauen.**
