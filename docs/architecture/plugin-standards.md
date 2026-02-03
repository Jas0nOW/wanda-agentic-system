# WANDA Factory Standard - Plugin Inventory (Februar 2026)

> **Zweck:** Dieses Dokument hält den absoluten Werkszustand (Factory Defaults) der installierten Plugins fest. Es dient als Referenz für die Entscheidung, welche Agenten und Logiken in das finale WANDA-System übernommen werden.
> **Datenquelle:** Source-Code-Extraktion aus `node_modules` (Cache).
> **Hinweis:** WANDA nutzt **Commander** als einzigen Primary. Default-Orchestratoren wie `Sisyphus` bleiben als Plugin-Defaults dokumentiert, sind im System jedoch deaktiviert.

---

## Installed Plugins (SSOT)

*   `opencode-antigravity-auth@latest`
*   `oh-my-opencode@latest`
*   `opencode-knowledge@latest`
*   `opencode-supermemory@latest`
*   `opencode-scheduler@latest`
*   `opencode-antigravity-quota@latest`
*   `@cgasgarth/opencode-for-rust@latest`
*   `micode@latest`
*   `opencode-agent-skills@latest`
*   `opencode-orchestrator@latest`
*   `opencode-handoff@latest`
*   `@gitlab/opencode-gitlab-auth@latest`

---

## 1. Core: `OpenCode` (v1.1.48)
**Fokus:** Runtime, CLI, TUI, Plugin-Engine.

### Standard-Verhalten
*   **Modell:** Kein festes Default-Modell. Fragt bei `opencode init` nach Providern (Anthropic, OpenAI, Google) und generiert `opencode.json`.
*   **Fallback:** Wenn kein Agent-Modell definiert ist, greift das `systemDefaultModel`.
*   **Tools:** Bietet die Basis-Tools (`filesystem`, `git`, `mcp-manager`).

---

## 2. Plugin: `oh-my-opencode` (v3.2.1)
**Fokus:** Multi-Agent Team-Orchestrierung & UI-Hooks.

### Agenten & Rollen (Standard)
| Agent | Standard-Modell (Config-Default) | Kern-Aufgabe |
|:---|:---|:---|
| **Sisyphus** | `claude-3-5-sonnet` / `opus` | "Engineering Manager": Plant, delegiert an Subagenten. |
| **Oracle** | `gpt-5.2` | "Think Tank": Deep Reasoning, Strategie-Review. |
| **Librarian** | `claude-3-5-sonnet` | "Researcher": RAG, Doku-Suche, Faktencheck. |
| **Explore** | `claude-haiku-4-5` | "Scout": Schnelles Grep & Mapping. |
| **Prometheus** | `claude-3-opus` | "Master Planner": Erstellt komplexe Work-Plans. |
| **Metis** | `claude-3-opus` | "Pre-Planner": Analysiert Ambiguitäten vor dem Start. |
| **Momus** | `gpt-5.2` | "Reviewer": Bewertet Pläne auf Vollständigkeit. |
| **Atlas** | `claude-3-5-sonnet` | "Legacy Executor": Führt aus (jetzt meist in Sisyphus integriert). |
| **Multimodal**| `gemini-3-flash` | "Visual Analyst": Bild-Analyse. |

### Kategorien (Delegation Targets)
*   **`visual-engineering`** (Gemini 3 Pro): UI/UX, Design-First.
*   **`ultrabrain`** (GPT-5.2 Codex): Tiefe Logik & Architektur.
*   **`artistry`** (Gemini 3 Pro): Kreative Konzepte & visuelle Ideen.
*   **`quick`** (Claude Haiku): Triviale Fixes.
*   **`unspecified-low`** (Claude Sonnet 4.5): Allgemeine Tasks (Low Effort).
*   **`unspecified-high`** (Claude Opus 4.5): Allgemeine Tasks (High Effort).
*   **`writing`** (Gemini 3 Flash): Dokumentation.

### Kern-Prompts & Features
*   **Ultrawork:** Parallelisierung von Tasks in Hintergrund-Sessions.
*   **Continuation Loop:** Sisyphus wiederholt Aufgaben, bis sie verifiziert sind.
*   **Hooks:** `comment-checker`, `rules-injector`, `session-recovery`, `context-injector`.

---

## 3. Plugin: `micode` (v0.9.1)
**Fokus:** Projekt-Konformität & Mindmodel-Integration.

### Agenten & Rollen (Standard)
| Agent | Standard-Modell (HARDCODED) | Kern-Aufgabe |
|:---|:---|:---|
| **Commander** | `openai/gpt-5.2-codex` | "Mission Controller": Streng regelbasiert. |
| **Brainstormer** | `openai/gpt-5.2-codex` | "Ideator": Nutzt interaktive Brainstorming-Loops. |
| **mm-orchestrator**| `openai/gpt-5.2-codex` | Steuert die Mindmodel-Extraktion. |
| **mm-stack-detector** | `openai/gpt-5.2-codex` | Erkennt Tech-Stack. |
| **mm-pattern-discoverer** | `openai/gpt-5.2-codex` | Findet wiederkehrende Code-Muster. |
| **mm-dependency-mapper** | `openai/gpt-5.2-codex` | Mappt Abhängigkeiten. |
| **ledger-creator** | `openai/gpt-5.2-codex` | Erstellt Continuity-Ledgers. |

### Kern-Prompts (Direktiven)
*   **Constraint First:** *"YOU MUST call mindmodel_lookup BEFORE writing ANY code."*
*   **Seniority:** Framed als "Senior Engineer", der keine unnötigen Fragen stellt.
*   **PTY Workflow:** Nutzt `pty_spawn` für interaktive Terminal-Tools.

### Tools & Hooks
*   `mindmodel_lookup`: Abfrage von Projekt-Patterns aus `.mindmodel/`.
*   `pty_spawn`: Interaktive Terminal-Tools.

---

## 4. Plugin: `opencode-orchestrator` (v1.2.58)
**Fokus:** Autonome Missions-Abarbeitung (Fire & Forget).

### Agenten & Rollen (Standard)
| Agent | Standard-Modell | Kern-Aufgabe |
|:---|:---|:---|
| **Commander** | Dynamisch (Config) | Steuert den gesamten `mission_lifecycle` (Phasen). |
| **Planner** | Dynamisch (Config) | Zerlegt Aufgaben in atomare Todos (`planning_decomposition`). |
| **Worker** | Dynamisch (Config) | Führt Code-Änderungen via TDD (`execution_tdd`) aus. |
| **Reviewer** | Dynamisch (Config) | Prüft auf Beweise (`verification_evidence`). |

### Kern-Prompts (Direktiven)
*   **Phasen-Modell:** Striktes Vorgehen: Philosophy → Discovery → Planning → Execution → Verification.
*   **Hallucination Guard:** Dedizierter Prompt zur Vermeidung von Fehl-Annahmen.
*   **Resolution:** *"You are only 'released' when the system verifies 100% check-off."*

### Tools & Hooks
*   `task_checkpoint`: Speichert Status bei langen Operationen.
*   `git_worktree_isolation`: Arbeitet in separaten Branches/Worktrees.

---

## Zusammenfassung der Konflikte
1.  **3 Chefs:** Sisyphus (OmO), Commander (MiCode) und Commander (Orchestrator) konkurrieren um die Leitung.
2.  **Modell-Konflikt:** MiCode erzwingt GPT-5.2 Codex (veraltet), OmO bevorzugt Claude, WANDA will Gemini Flash.
3.  **Tool-Wildwuchs:** `mindmodel_lookup` (MiCode) vs. `context7` (OmO) vs. `discovery` (Orch).
