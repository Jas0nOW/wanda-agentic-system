# OpenCode System Handbuch (v3) - [SSOT: WANDA_SYSTEM_DOCS.md]

## 🎯 Übersicht

Dieses System nutzt **18 spezialisierte AI-Agenten** mit **20+ SOTA-Modellen** über **5 Provider**.
WANDA ist ein souveränes AI-Betriebssystem, das auf OpenCode basiert.

---

## 👥 Agent-Team (Hierarchisch)

### Core Fleet (Primär, sichtbar)
| Agent | Rolle | Engine | Aufgabe |
|-------|-------|--------|---------|
| 💡 **Brainstormer** | Ideator | Gemini 3 Pro | Design-First Workflow |
| ⚡ **Commander** | Orchestrator | GPT-5.2 Codex | Quick-Mode Decision Engine & Routing |
| 📚 **Librarian** | Researcher | Gemini 3 Flash | Source-First RAG & Verification |
| 🏗️ **Architect** | Grounder | Claude 4.5 Opus | Tech Stack & Blueprint |
| 🛠️ **Software-Engineer** | Builder | Claude 4.5 Sonnet | Feature-Implementierung |
| 🛡️ **Audit** | Fixer | Claude 4.5 Opus | Zero-Trust Find-Break-Fix |
| ✍️ **Writer** | Tech Writer | Gemini 3 Flash | Verifiable Documentation |

### Specialist Fleet (Hintergrund)
Das System verfügt über weitere spezialisierte Agenten für Research (Explore), Analyse (Locator, Analyzer, Pattern-Finder), Continuity (Ledger-Creator, Artifact-Searcher) und Strategie (Oracle, Metis, Momus).

---

## 🔄 3-Phasen-Workflow

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
│                    │ (Claude Opus) │                        │
│                    └───────────────┘                        │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔗 Provider (Unified)

**Provider (unterstuetzt, optional):**
1. ⚡ Antigravity (Primary, konfiguriert)
2. 🟣 Anthropic (optional)
3. 🐙 GitHub Copilot (optional)
4. 🔵 Google (optional)
5. 🟢 OpenAI (optional)

---

## 🚀 Befehle

| Befehl | Aktion |
|--------|--------|
| `/init` | Projekt initialisieren |
| `/ralph-loop "Task"` | Autonomen 3-Phasen-Workflow starten |
| `@brainstormer "Idee"` | Design-First Exploration starten |
| `/ledger` | Session-Status sichern |

---

## ✅ Status

- **Agenten**: 18 aktiv
- **Modelle**: 20+ verfügbar
- **Provider**: 5 aktiv
- **Plugins**: 10 installiert

**Single Source of Truth:** Siehe `WANDA_SYSTEM_DOCS.md` für technische Details.
