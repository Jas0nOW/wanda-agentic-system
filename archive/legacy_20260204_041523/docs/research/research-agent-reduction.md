# X10 Research: Optimized Agent Fleet & Origin

> **Status:** DRAFT
> **Ziel:** Definition der finalen 14-Agenten-Flotte inkl. technischer Herkunft.

## 1. Die Optimierte Flotte (14 Agenten)

Wir reduzieren von 18 auf 14 Agenten durch Zusammenlegung redundanter Rollen.

| Agent | Rolle | Layer | Herkunft (Technisch) | Modell (SOTA Empfehlung) |
| :--- | :--- | :--- | :--- | :--- |
> **Hinweis:** Upstream-Quellen nennen `Sisyphus` als Default-Orchestrator. In WANDA ist **Commander** der einzige Primary; `Sisyphus` bleibt als Plugin-Default deaktiviert.

| **Sisyphus** | Orchestrator (Unified) | Orchestration | `oh-my-opencode` Plugin | Gemini 3 Flash (Speed/Context) |
| **Brainstormer** | Ideator | Ideation | `micode` Plugin | Gemini 3 Pro (Creativity) |
| **Architect** | Grounder | Core | `oh-my-opencode` Plugin | Claude Opus 4.5 Thinking |
| **Software-Engineer** | Builder | Core | `oh-my-opencode` Plugin | Claude Sonnet 4.5 |
| **Audit** | Fixer | Core | `oh-my-opencode` Plugin | Claude Opus 4.5 Thinking |
| **Frontend-UI-UX** | Designer | Core | Custom (Markdown) | Gemini 3 Pro |
| **Oracle** | Strategist (Unified) | Specialist | `oh-my-opencode` Plugin | GPT-5.2 (Reasoning) |
| **Librarian** | Researcher (Unified) | Specialist | `oh-my-opencode` Plugin | Gemini 3 Flash |
| **Writer** | Tech Writer | Specialist | `oh-my-opencode` Plugin | Gemini 3 Flash |
| **Explore** | Mapper (Unified) | Specialist | `oh-my-opencode` Plugin | Gemini 3 Flash |
| **Multimodal-Looker** | Visual Analyst | Specialist | `oh-my-opencode` Plugin | Gemini 3 Pro |
| **Ledger-Creator** | Continuity | Continuity | Custom (Markdown) | Gemini 3 Flash |
| **Codebase-Analyzer** | Deep Analyzer | Research | Custom (Markdown) | Gemini 3 Flash |
| **Pattern-Finder** | Scout | Research | Custom (Markdown) | Gemini 3 Flash |

### Eliminierte Redundanzen
*   **Commander:** Gemerged in `Sisyphus` (Orchestrator).
*   **Metis / Momus:** Gemerged in `Oracle` (Strategie & Review).
*   **Codebase-Locator:** Gemerged in `Explore` (Mapper).
*   **Artifact-Searcher:** Gemerged in `Librarian` (Researcher).

---

## 2. Herkunft & Erstellung

*   **Plugin-Agenten:** Kommen fertig aus `oh-my-opencode` oder `micode`. Anpassung via Config (`oh-my-opencode.json`).
*   **Custom-Agenten:** Müssen als Markdown-Dateien in `~/.config/opencode/agents/` definiert werden.

## 3. Nächste Schritte: Research Guides
*   `docs/research-agent-creation-guide.md`: Wie baut man Custom Agenten (Python/LangChain)?
*   `docs/research-agent-architecture.md`: Wie skaliert das System (Layer, MCP)?
