# WANDA Master Blueprint (v2.0 - Fallback Matrix Secured) 
## AKTUESLLSTE DATEI 01.02 - 22:13

> **Vision:** Ein Sovereign AI OS, gesteuert über Voice & Chat (Moltbot), das autonome "v0-style" Builds für Web, Workflows (n8n), Projekte und Ops liefert.
> **Core:** OpenCode + oh-my-opencode + MiCode + orchestrator + Moltbot Gateway.

---

## 1. Primary + Subagenten (Unified Roster)

**Primary:** Commander (MiCode). Alle anderen Hauptagenten sind deaktiviert und laufen als Subagenten oder Logik-Module.

**Subagenten (Auswahl):** Oracle, Librarian, Writer, Explore, Pattern-Hunter, Quality-Gate, Brainstormer, Frontend-Dev, Multimodal-Looker, codebase-locator, codebase-analyzer, pattern-finder, ledger-creator, artifact-searcher, mm-orchestrator, mm-pattern-discoverer, mm-stack-detector, mm-dependency-mapper.

**Technical Fallback Logic:**
1.  **Quota Check:** Antigravity IDE **vs** Google CLI (getrennte Limits).
2.  **Provider Switch:** Antigravity → Anthropic → OpenAI.
3.  **Loop:** Retry max 3 times before failing task.

---

## 2. The v0 Skill Registry (Application Layer)

WANDA arbeitet nicht "irgendwie", sondern über standardisierte Skills (Pipelines), die durch Specs definiert sind.

### Skill A: `v0_web` (Fullstack Builder)
*   **Trigger:** Chat/Voice: "Baue eine Landingpage..."
*   **Contract:** `.v0/specs/UI_SPEC.yml` (Next.js/Tailwind/shadcn).
*   **Flow:** Brainstormer (Spec) → Commander (Code) → Quality-Gate (Lint/Build).

### Skill B: `v0_n8n` (Workflow Automation)
*   **Trigger:** Chat/Voice: "Erstelle ein n8n Scenario/Workflow.."
*   **Contract:** `.v0/specs/N8N_SPEC.yml`.
*   **Tech:** `n8n-mcp` (Node Docs) + n8n API (Deployment).
*   **Flow:** Brainstormer (Spec) → Commander (JSON Gen) → API Deploy → Smoke Test.

### Skill C: `v0_ops` (Infrastructure)
*   **Trigger:** Chat/Voice: "Deploy das auf Staging."
*   **Contract:** `.v0/specs/OPS_SPEC.yml`.
*   **Flow:** Commander (Docker/Vercel/Supabase) → Quality-Gate (Health Check).

---

## 3. The Frontdoor: Moltbot Gateway (Voice & Chat)

Dies ist die Schnittstelle zur Außenwelt. Moltbot läuft als lokaler Daemon oder auf dem VPS.

*   **Ingress:** Telegram, Discord, WhatsApp, Voice Calls (Twilio/Telnyx).
*   **Routing:** 
*   *Voice:* Speech-to-Text → "Short Pack" (Zusammenfassung) → Commander.
    *   *Chat:* Text → Policy Check → Skill Router.
*   **Feedback:** Moltbot sendet Status-Updates ("Build läuft...", "Done: Link") zurück in den Chat.
*   **Security:** Allowlist für Telefonnummern. Kritische Aktionen (Deploy/Delete) brauchen "JA, AUSFÜHREN" Bestätigung.

---

## 4. The 8-Phase Workflow (Das Gesetz)

Dieser Prozess wird von den Agenten strikt eingehalten, egal ob per Voice oder CLI gestartet.

1.  **Brainstorming** (Brainstormer): Idee → Spec Draft.
2.  **Deep Research** (Librarian): SOTA-Check & Tech-Stack Wahl.
3.  **Initialization** (Commander): Skeleton & `.v0/` Configs.
4.  **Implementation** (Commander Parallel): Frontend/Backend Code.
5.  **Testing** (Quality-Gate): Unit/Integration Tests.
6.  **Refactoring** (Pattern-Hunter): Code Style Enforcement.
7.  **Deployment** (Commander Ops): Go Live.
8.  **Feedback/Docs** (Librarian): Abschlussbericht an User (Voice/Chat).

---

## 5. Technical Implementation Strategy

### A. Moltbot Config (`~/.clawdbot/moltbot.json`)
*   Plugins: `voice-call`, `v0-bridge`.
*   Channels: Telegram, Discord, WhatsApp (Allowlist), Voice (Twilio).
*   Tools: `deny: ["exec"]` für Frontdoor-Agent (Security).

### B. OpenCode Config (`~/.config/opencode/`)
*   **Plugins (15):**
    *   `opencode-antigravity-auth@latest`
    *   `opencode-openai-codex-auth@latest`
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
    *   `opencode-gemini-auth@latest`
*   **MCPs:** `brave`, `filesystem`, `memory`, `sequential-thinking`, `github`, `stripe`, `n8n-API`, `n8n-mcp`, `supabase`, `postgres`, `vercel`, `docker`, `playwright`, `firecrawl`, `context7`, `websearch`, `grep_app`, `git`.

### C. Directory Structure
*   `~/.v0/specs/`: Ablageort für Specs.
*   `~/.v0/contracts/`: Templates (UI_SPEC, etc.).
*   `~/.v0/exports/`: Ergebnisse für den User.

---

> **Status:** Final Blueprint v2.0
> **Date:** 01.02.2026

---

# WICHTIGE RESEARCHES BEI PROBLEMEN

OPENCODE CONFIGURE:

https://opencode.ai/docs/plugins/
https://opencode.ai/docs/tools/
https://opencode.ai/docs/rules/
https://opencode.ai/docs/agents/
https://opencode.ai/docs/models/
https://opencode.ai/docs/formatters/
https://opencode.ai/docs/permissions/
https://opencode.ai/docs/lsp/
https://opencode.ai/docs/mcp-servers/
https://opencode.ai/docs/acp/
https://opencode.ai/docs/skills/
https://opencode.ai/docs/custom-tools/


OHMYOPENCODE CONFIGURE:

https://ohmyopencode.com/documentation/
https://ohmyopencode.com/configuration/
https://ohmyopencode.com/features/


MICODE CONFIGURE:

https://github.com/vtemian/micode?tab=readme-ov-file


OPENCODE-ORCHESTRATOR:

https://www.npmjs.com/package/opencode-orchestrator

---

Plugin-Reihenfolge & doppelte Installationen
OpenCode lädt Plugins aus mehreren Quellen (Global config → Project config → globale Plugin-Dir → Projekt-Plugin-Dir). Hooks laufen sequenziell; gleiches npm-Paket (Name+Version) nur einmal, aber lokales Plugin + npm-Plugin werden beide geladen. Das kann “doppelte” Effekte machen.