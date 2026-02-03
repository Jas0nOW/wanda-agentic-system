# Research: Plugin & Agent Analysis (Status Quo)

> **Status:** ACTIVE INVESTIGATION
> **Ziel:** Klärung der Herkunft und Funktion aller installierten Plugins ("micode", "opencode-knowledge", etc.) zur Eliminierung von Redundanzen.

## 1. Der "Commander" Fall
*   **Befund:** "Commander" ist kein Standard-Agent eines öffentlichen Plugins.
*   **Herkunft:** Definiert in `opencode.json` (`default_agent: "Commander"`) mit lokalem Prompt (`agents/Commander.txt`).
*   **Problem:** Nutzt `gpt-5.2-codex` (Code-Completion Modell) für Orchestrierung.
*   **Plan:** Upgrade auf `Gemini 3 Flash` (Kontext-Monster) oder `Claude Opus`. Beibehaltung des Namens "Commander" als Alias für den verbesserten Orchestrator.

## 2. Plugin-Inventur (Zu Prüfen)
Wir müssen die Quelle und Funktion folgender Pakete verifizieren:

| Plugin | Vermutete Funktion | Status |
| :--- | :--- | :--- |
| `opencode-antigravity-auth@latest` | Antigravity OAuth / Provider-Bridge | Zu prüfen |
| `oh-my-opencode@latest` | Agent Harness / Orchestrierung | Zu prüfen |
| `opencode-knowledge@latest` | Knowledge Base Injection (AGENTS.md) | Zu prüfen |
| `opencode-supermemory@latest` | Cloud Memory / Langzeit-Fakten | Zu prüfen |
| `opencode-scheduler@latest` | Task Scheduling / Cron | Zu prüfen |
| `opencode-antigravity-quota@latest` | Quota-Management (Antigravity) | Zu prüfen |
| `@cgasgarth/opencode-for-rust@latest` | Rust Tooling / LSP / Toolchain | Zu prüfen |
| `micode@latest` | Workflow (Brainstorm -> Plan) | **UNKLAR** (Online kaum Spuren) |
| `opencode-agent-skills@latest` | Skills Loader | Zu prüfen |
| `opencode-orchestrator@latest` | Task Routing / Autopilot | Zu prüfen |
| `opencode-handoff@latest` | Session Continuity | Zu prüfen |
| `opencode-gemini-auth@latest` | Gemini CLI OAuth | Zu prüfen |

## 3. Strategie
1.  **Online-Check:** Existieren diese Pakete auf NPM/GitHub?
2.  **Code-Check:** Wenn nicht online, sind es lokale Aliases oder private Forks?
3.  **Bereinigung:** Wenn redundant (z.B. `orchestrator` vs. `oh-my-opencode`), wird das schwächere Plugin entfernt.
