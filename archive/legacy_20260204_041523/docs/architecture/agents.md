# WANDA Sovereign AI OS - Agenten & Rollen (v3)

> **Status:** Single Source of Truth (SSOT) für Agenten-Architektur
> **Stand:** Februar 2026
> **System:** OpenCode + oh-my-opencode + MiCode

Diese Datei definiert die aktive Agenten-Flotte, ihre Hierarchie und die technische Orchestrierung.

## 1. System-Übersicht

- **1 Hauptagent** + **Subagenten-Flotte** in **7 Layers**
- **Hierarchische Sortierung**: Main (Primary) & Subagenten (Delegation)
- **7 Kategorien** für dynamische Skill-Zuweisung
- **15 Plugins** installiert (Unified System)
- **Session Continuity** via Ledger-System

---

## 2. Main Agent (Primary - Sichtbar)

Nur der Commander ist direkt ansteuerbar. Alle anderen Hauptagenten sind deaktiviert.

| Agent | Rolle | Modell | Aufgabe | Mode |
|:------|:------|:-------|:--------|:-----|
| **commander** | Orchestrator | GPT-5.2 Codex | Mission-Controller. Routing, Orchestrierung, Policy-Gates. | **Primary** |

---

## 3. Subagenten-Fleet (Delegation)

Diese Agenten werden vom Commander bei Bedarf gerufen ("Delegation").

| Agent | Rolle | Modell | Aufgabe |
|:------|:------|:-------|:--------|
| **oracle** | Think Tank | OpenAI GPT 5.2 | Deep Reasoning, Architektur-Validierung. |
| **librarian** | Researcher | Gemini 3 Flash | RAG, Quellen-Checks, Dokumentation. |
| **writer** | Tech Writer | Gemini 3 Flash | Technische Doku & Berichte. |
| **explore** | Mapper | Gemini 3 Flash | Codebase-Mapping & Navigation. |
| **pattern-hunter** | Code-Guard | GPT 5.2 Codex | Konventionen, Mindmodel, Patterns. |
| **quality-gate** | Auditor | GPT 5.2 Codex | Verification Evidence, Test-Gates. |
| **brainstormer** | Ideator | Gemini 3 Flash | Konzept & Ideation. |
| **frontend-dev** | UI Specialist | Gemini 3 Pro | UI/UX & Design-Tokens (v0_web). |
| **multimodal-looker** | Visual | Gemini 3 Pro | Bild- & Diagramm-Analyse. |
| **codebase-locator** | Locator | Gemini 3 Flash | Findet *WO* Dateien liegen. |
| **codebase-analyzer** | Analyzer | Gemini 3 Flash | Erklärt *WIE* Code funktioniert. |
| **pattern-finder** | Scout | Gemini 3 Flash | Findet existierende Patterns (DRY). |
| **ledger-creator** | Continuity | Gemini 3 Flash | Speichert Session-State in Ledgers. |
| **artifact-searcher** | History | Gemini 3 Flash | Sucht in vergangenen Handoffs/Ledgers. |
| **mm-orchestrator** | Mindmodel | GPT-5.2 Codex | Mindmodel-Extraktion (MiCode). |
| **mm-pattern-discoverer** | Mindmodel | GPT-5.2 Codex | Muster-Extraktion (MiCode). |
| **mm-stack-detector** | Mindmodel | GPT-5.2 Codex | Stack-Erkennung (MiCode). |
| **mm-dependency-mapper** | Mindmodel | GPT-5.2 Codex | Dependency-Map (MiCode). |

*(Hinweis: `prometheus`, `atlas`, `sisyphus`, `planner`, `executor`, `implementer`, `reviewer`, `worker` sind technisch vorhanden, aber im WANDA-Betrieb deaktiviert/gemerged.)*

---

## 4. Technische Orchestrierung

### 4.1 Dual-Quota-System (Resource Optimization)
Das System nutzt eine **Dual-Quota-Strategie** mit klar getrennten Limits:
1.  **Google Antigravity Quota**: Nutzung via IDE-Auth (Modelle: `google/antigravity-*`).
2.  **Google CLI Quota**: Nutzung via CLI-Auth (Modelle: `google/gemini-*`).
*Beide Kontingente sind parallel nutzbar und müssen als getrennte Limits behandelt werden.*

### 4.2 Provider-Level Fallback Chain
Um Ausfallsicherheit zu gewährleisten, greift eine automatische Fallback-Logik:
*   **Chain:** `Antigravity` → `Anthropic` → `OpenAI`
*   **Trigger:** Quota/Provider-Ausfall. Vor dem Switch wird das **IDE vs CLI Quota** geprüft.

---

## 5. Speicher-Architektur (Memory)

WANDA nutzt eine **3-Layer Speicher-Architektur**:

1.  **Layer 1: Memory MCP (Knowledge Graph)**
    *   *Ort*: Integrierter MCP Server (`memory`)
    *   *Zweck*: WANDA System-Wissen, Entitäten, Beziehungen. Persistent lokal.
2.  **Layer 2: opencode-knowledge Plugin (AGENTS.md)**
    *   *Ort*: `~/.config/opencode/AGENTS.md`
    *   *Zweck*: Session-Regeln, Persona-Definitionen (Read-Only Injection).
3.  **Layer 3: opencode-supermemory Plugin (Cloud Memory)**
    *   *Ort*: Cloud / `~/.config/opencode/supermemory.jsonc`
    *   *Zweck*: Langzeit-Fakten ("remember this"), Ähnlichkeitssuche.

---

## 6. MCP Server & Tools

| Server | Zweck |
|:-------|:------|
| **brave** | Web-Suche & Research |
| **filesystem** | Datei-Operationen (Read/Write/Edit) |
| **memory** | Knowledge Graph Persistenz |
| **sequential-thinking** | Chain-of-Thought (CoT) Reasoning |
| **github** | GitHub API Integration |
| **context7** | Library Dokumentation (SOTA) |
| **websearch** | Web-Suche (Exa) |
| **grep_app** | Code-Suche (grep.app) |
| **exa** | Web-Datenzugriff (Exa MCP) |
| **git** | Git Operationen (Commit/Diff/Log) |
| **playwright** | Browser Automation |
| **firecrawl** | Web Scraping |
| **supabase** | Datenbank-Zugriff |
| **postgres** | Datenbank-Zugriff |
| **vercel** | Deployment Management |
| **n8n-pro** | Workflow Automatisierung |
| **n8n-mcp** | Node-Doku & Workflow-Truth-Source |
| **stripe** | Billing & Zahlungs-APIs |
| **docker** | Container/Runtime Management |

---

## 7. Workflow-Befehle

| Befehl | Flow | Beschreibung |
|:-------|:-----|:-------------|
| `/ralph-loop` | Commander → Architect → Developer → Audit | **3-Phasen Autopilot** für komplexe Tasks. |
| `/init` | Context7 → Architect → Structure | **Projekt-Initialisierung** (MiCode Standard). |
| `/ledger` | Ledger-Creator | **Session Save** (Erstellt Continuity Point). |
| `@brainstormer` | Brainstormer → Design → Planner | **Design-First Exploration**. |

---

## 8. Konfigurations-Dateien (Referenz)

| Datei | Ort | Zweck |
|:------|:----|:------|
| Agent Config | `~/.config/opencode/oh-my-opencode.json` | 18 Agenten-Definitionen (Plugin Defaults, WANDA deaktiviert Teile) |
| Main Config | `~/.config/opencode/opencode.json` | Plugins, Modelle, MCP Server |
| AGENTS.md | `~/.config/opencode/AGENTS.md` | Session Knowledge Base |

*Letzte Aktualisierung: Februar 2026 (v3.2 - Dual Quota & Fallbacks Added)*
