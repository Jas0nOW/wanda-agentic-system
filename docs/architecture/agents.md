# WANDA Sovereign AI OS - Agenten & Rollen (v4)

> **Status:** Single Source of Truth (SSOT) für Agenten-Architektur
> **Stand:** Februar 2026
> **System:** OpenCode + oh-my-opencode + MiCode

Diese Datei definiert die aktive Agenten-Flotte, ihre Hierarchie und die technische Orchestrierung.

---

## 1. System-Übersicht

- **7 Layers** mit klarer Reihenfolge: Brainstorming → Planning → Architecture → Development → Audit → Continuity → Meta
- **18 Agenten** in 7 Layern organisiert
- **Layer 3 Core** enthält 4 Agenten (Architect, Developer, Frontend-UI-UX, Audit)
- **Session Continuity** via Ledger-System

**Wichtig:** Layer 3 (Architecture) wird bei Fehlern NICHT wiederholt - nur Layer 1-2 loop zurück!

---

## 2. Die 7 Layers (Korrekte Reihenfolge)

```
Layer 1: BRAINSTORMING    → Ideation, NO code
Layer 2: PLANNING         → Orchestration, Routing  
Layer 3: ARCHITECTURE     → System Design, Blueprints
Layer 4: DEVELOPMENT      → Implementation, Code
Layer 5: AUDIT            → Security, Review, QC
Layer 6: CONTINUITY       → Session State, Handoffs
Layer 7: META             → Pre-Planning, Validation
```

---

## 3. Agenten pro Layer

### Layer 1: Brainstorming (Ideation)
| Agent | Rolle | Modell | Aufgabe |
|:------|:------|:-------|:--------|
| **brainstormer** | Ideator | Gemini 3 Pro | Kreative Ideen, Design-Thinking, NO code |

**Trigger:** `@brainstormer`, "brainstorm", "explore ideas"

---

### Layer 2: Planning (Orchestration)
| Agent | Rolle | Modell | Aufgabe |
|:------|:------|:-------|:--------|
| **orchestrator** | Router | Gemini 3 Flash | Task-Klassifikation, Agent-Delegation |

**Trigger:** Immer aktiv als Hauptinterface

---

### Layer 3: Core Development (4 Agenten)
| Agent | Rolle | Modell | Aufgabe |
|:------|:------|:-------|:--------|
| **architect** | Designer | Claude 4.5 Opus | System-Design, Blueprints |
| **developer** | Builder | Claude 4.5 Sonnet | Code-Implementierung, TDD |
| **frontend_ui_ux** | UI Specialist | Gemini 3 Pro | UI/UX, Design-Tokens |
| **audit** | Reviewer | Claude 4.5 Opus | Code-Review, Security |

---

### Layer 4: Specialist (Domain Experts)
| Agent | Rolle | Modell | Aufgabe |
|:------|:------|:-------|:--------|
| **oracle** | Think Tank | Claude 4.5 Opus | Deep Reasoning, Strategie |
| **librarian** | Researcher | Gemini 3 Flash | RAG, Dokumentation |
| **writer** | Tech Writer | Gemini 3 Flash | Technische Doku |
| **explore** | Mapper | Gemini 3 Flash | Codebase-Mapping |
| **multimodal_looker** | Visual | Gemini 3 Pro | Bild- & Diagramm-Analyse |

---

### Layer 5: Research (Codebase Analysis)
| Agent | Rolle | Modell | Aufgabe |
|:------|:------|:-------|:--------|
| **codebase_locator** | Locator | Gemini 3 Flash | Findet *WO* Dateien liegen |
| **codebase_analyzer** | Analyzer | Gemini 3 Flash | Erklärt *WIE* Code funktioniert |
| **pattern_finder** | Scout | Gemini 3 Flash | Findet existierende Patterns |

---

### Layer 6: Continuity (Session Management)
| Agent | Rolle | Modell | Aufgabe |
|:------|:------|:-------|:--------|
| **ledger_creator** | Continuity | Gemini 3 Flash | Speichert Session-State |
| **artifact_searcher** | History | Gemini 3 Flash | Sucht in vergangenen Sessions |

---

### Layer 7: Meta (Quality Gates)
| Agent | Rolle | Modell | Aufgabe |
|:------|:------|:-------|:--------|
| **metis** | Pre-Planner | Claude 4.5 Opus | Analysiert Requests vor Planning |
| **momus** | Plan Reviewer | Claude 4.5 Opus | Bewertet Pläne auf Vollständigkeit |

---

## 4. Workflow & Routing

### Standard Workflow
```
Brainstormer (L1) → Orchestrator (L2) → Architect (L3) → Developer (L3) 
→ Frontend-UI-UX (L3) → Audit (L3) → [Continuity (L6)]
```

### Quick-Mode Entscheidungen

| Modus | Kriterien | Aktion |
|:------|:----------|:-------|
| **TRIVIAL** | Typo, Version bump | Sofort ausführen |
| **SMALL** | Funktion <20 Zeilen | Kurzer Plan → ausführen |
| **COMPLEX** | 5+ Dateien, Architektur | Vollständiger 7-Layer Workflow |

---

## 5. MCP Server & Tools

| Server | Zweck |
|:-------|:------|
| **brave** | Web-Suche & Research |
| **filesystem** | Datei-Operationen |
| **memory** | Knowledge Graph |
| **sequential-thinking** | Chain-of-Thought |
| **github** | GitHub API |
| **context7** | Library Dokumentation |
| **websearch** | Web-Suche (Exa) |
| **grep_app** | Code-Suche |
| **git** | Git Operationen |
| **playwright** | Browser Automation |
| **firecrawl** | Web Scraping |
| **supabase/postgres** | Datenbanken |
| **vercel** | Deployment |
| **n8n-pro** | Workflows |
| **docker** | Container |

---

## 6. Workflow-Befehle

| Befehl | Flow | Beschreibung |
|:-------|:-----|:-------------|
| `/ralph-loop` | Architect → Developer → Audit | **3-Phasen Autopilot** |
| `/init-deep` | Context7 → Architect → Structure | **Projekt-Init** |
| `/ledger` | Ledger-Creator | **Session Save** |
| `@brainstormer` | Brainstormer → Architect → Developer | **Design-First** |

---

## 7. Konfigurations-Dateien

| Datei | Ort | Zweck |
|:------|:----|:------|
| Agent Prompts | `prompts/agents/*.md` | 18 Agenten-Definitionen |
| Main Config | `~/.config/opencode/opencode.json` | Plugins, Modelle, MCP |
| AGENTS.md | `docs/architecture/agents.md` | Diese Datei (SSOT) |

---

## 8. Agenten-Prompts Verzeichnis

```
prompts/agents/
├── brainstormer.md         # Layer 1
├── orchestrator.md         # Layer 2
├── architect.md            # Layer 3
├── developer.md            # Layer 3
├── frontend_ui_ux.md       # Layer 3
├── audit.md                # Layer 3
├── oracle.md               # Layer 4
├── librarian.md            # Layer 4
├── writer.md               # Layer 4
├── explore.md              # Layer 4
├── multimodal_looker.md    # Layer 4
├── codebase_locator.md     # Layer 5
├── codebase_analyzer.md    # Layer 5
├── pattern_finder.md       # Layer 5
├── ledger_creator.md       # Layer 6
├── artifact_searcher.md    # Layer 6
├── metis.md                # Layer 7
└── momus.md                # Layer 7
```

---

## 9. Änderungshistorie

| Version | Datum | Änderungen |
|:--------|:------|:-----------|
| **v4.0** | 2026-02-05 | **MAJOR:** 7-Layer Struktur korrigiert, doppelte Agenten entfernt |
| v3.2 | 2026-02-04 | Dual Quota & Fallbacks |
| v3.0 | 2026-02-01 | Initiale Architektur |

*Letzte Aktualisierung: 5. Februar 2026 (v4.0 - Layer-Struktur korrigiert)*
