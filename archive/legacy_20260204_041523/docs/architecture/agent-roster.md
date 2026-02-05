> **Status:** Unified Roster (Final)
> **Basis:** Audit der Plugins `oh-my-opencode`, `micode`, `opencode-orchestrator`.
> **Strategie:** Keine redundanten Hauptagenten. Commander bleibt Primary, alles andere läuft als Subagent.

---

## 1. Primary (Main Agent)

### 👑 **Commander (MiCode)**
*   **Herkunft:** `micode`.
*   **Warum er gewonnen hat:** Streng regelbasiert, übernimmt Orchestrierung und Routing.
*   **Modell:** `openai/gpt-5.2-codex`.
*   **Aufgabe:** Mission-Controller, Policy-Gates, Delegation an Subagenten.

---

## 2. Subagenten (Delegation)

### Core Spezialisten (oh-my-opencode)
*   **Oracle** — Architektur & Deep Reasoning.
*   **Librarian** — RAG, Quellenarbeit, Dokumentation.
*   **Explore** — schnelle Codebase-Navigation.
*   **Writer** — technische Doku.
*   **Multimodal-Looker** — visuelle Analyse.

### Qualität & Patterns
*   **Pattern-Hunter** — Konventionen, `.mindmodel`, Legacy-Patterns.
*   **Quality-Gate** — Verification Evidence, Test-Gates.

### UI & Ideation
*   **Brainstormer** — Design-First, Ideation-Loop.
*   **Frontend-Dev** — UI/UX, Design-Tokens, v0_web.

### Codebase & Continuity (MiCode)
*   **codebase-locator** — WO liegen Dateien.
*   **codebase-analyzer** — WIE funktioniert Code.
*   **pattern-finder** — vorhandene Patterns.
*   **ledger-creator** — Continuity Ledger.
*   **artifact-searcher** — Handoffs/History.

### Mindmodel-Tools (MiCode)
*   **mm-orchestrator** — Mindmodel-Steuerung.
*   **mm-pattern-discoverer** — Muster-Extraktion.
*   **mm-stack-detector** — Stack-Erkennung.
*   **mm-dependency-mapper** — Dependency-Map.

---

## 3. Deaktivierte Hauptagenten (Redundanz-Schnitt)

| Agent | Quelle | Status | Grund |
|:---|:---|:---|:---|
| **Sisyphus** | `oh-my-opencode` | deaktiviert | Commander übernimmt Orchestrierung. |
| **Commander (Orchestrator)** | `opencode-orchestrator` | deaktiviert | Doppelrolle zu MiCode Commander. |
| **Planner** | `opencode-orchestrator` | deaktiviert | Nur als Subagent/Logik genutzt. |
| **Worker** | `opencode-orchestrator` | deaktiviert | Nur als Subagent/Logik genutzt. |
| **Reviewer** | `opencode-orchestrator` | deaktiviert | Quality-Gate übernimmt. |
| **Executor/Implementer** | `micode` | deaktiviert | Delegation via Commander. |
| **Prometheus/Atlas/Metis/Momus** | `oh-my-opencode` | deaktiviert | Redundante Planung/Review. |
