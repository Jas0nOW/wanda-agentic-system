# WANDA System Vision: Universal v0-Style Builder & Voice OS

> **Status:** Vision & Target Architecture (Soll-Zustand)
> **Basis:** DeepResearch Ergebnisse 1, 2 & 3
> **Ziel:** Eine souveräne, lokale Plattform, die "v0-Qualität" für Web, n8n und Ops liefert, gesteuert über Voice & Chat.

---

## 1. Kern-Vision: "v0 für Alles"

Das Ziel ist nicht nur ein "Coding Agent", sondern eine **Skill-Plattform**. Wie v0.dev für React-Komponenten, soll WANDA für *jede* Domäne (Web, Workflows, Ops) funktionieren.

### Die "v0-Formel" (Lokal repliziert)
1.  **Contract-First:** Keine Arbeit ohne Spec (Single Source of Truth).
2.  **Runner-Architektur:** Standardisierte Execution-Pipelines (Lint/Build/Test).
3.  **Fix-Loop:** Autonome Fehlerbehebung mit harten Limits (max 3 Versuche).
4.  **Quality Gates:** Nichts verlässt das System ohne grünen Haken.

---

## 2. Die Skills (Application Layer)

Das System wird durch **Skills** definiert, nicht durch Prompts. Jeder Skill ist eine deterministische Pipeline.

### Skill A: `v0_web` (Fullstack Builder)
*   **Input:** Prompt → `UI_SPEC.yml` (Spec)
*   **Stack:** Next.js + Tailwind + shadcn/ui (v0-kompatibel)
*   **Pipeline:**
    1.  `UI_SPEC.yml` erstellen & validieren (Architect + UI/UX Agent).
    2.  Code generieren (Software-Engineer).
    3.  **Runner:** `lint` + `build` + `typecheck`.
    4.  **Fix-Loop:** Bei Fehlern repariert Audit Agent (max 3 Iterationen).
    5.  **Export:** Git-Patch oder Pull Request.

### Skill B: `v0_n8n` (Workflow Automation)
*   **Input:** Prompt → `N8N_SPEC.yml`
*   **Source of Truth:** `n8n-mcp` (für aktuelle Node-Doku).
*   **Pipeline:**
    1.  Workflow-JSON generieren (ohne Secrets!).
    2.  **Runner:** Deploy via n8n API (oder File-Upload).
    3.  **Smoke Test:** Trigger via Webhook und Prüfen des Resultats.
    4.  **Fix-Loop:** Korrektur bei API-Fehlern oder Test-Failures.

### Skill C: `v0_ops` (Infrastructure & Monitoring)
*   **Input:** Prompt → `OPS_SPEC.yml`
*   **Pipeline:** Deploy (Vercel/Docker) + Post-Deploy Checks (Lighthouse, SEO, Uptime).

---

## 3. The Frontdoor: Voice & Chat Gateway (Moltbot)

Das System wird nicht nur über das Terminal bedient, sondern besitzt eine **Multi-Channel Frontdoor**.

### Architektur
*   **Gateway Daemon:** Moltbot (lokal laufend).
*   **Kanäle:** WhatsApp, Telegram, Discord (Chat) + Twilio/Telnyx (Voice).
*   **Routing:** 
    *   *Chat:* Text → Policy Engine → Skill Router → OpenCode Runner.
    *   *Voice:* Speech-to-Text → Intent Recognition → "Notify Mode" (kurzes Bestätigen, Arbeit im Hintergrund).

### Security Model (Red Team Ready)
1.  **Ingress Auth:** Allowlist für Telefonnummern/User-IDs.
2.  **Approval Gates:** Kritische Aktionen (Deploy, Delete, Cost) benötigen explizite Bestätigung ("JA, AUSFÜHREN").
3.  **Log Redaction:** Automatische Entfernung von Secrets/PII aus Logs.
4.  **Sandboxing:** Runner läuft isoliert vom Host-System.

---

## 4. Implementation Roadmap

### Phase 1: MVP (Terminal-Only)
- [ ] `.v0/` Ordner-Struktur anlegen (`specs/`, `contracts/`).
- [ ] `v0_web` Command implementieren (OpenCode Custom Command).
- [ ] `UI_SPEC.yml` Template erstellen.
- [ ] Manueller Runner-Test (Lint/Build Loop).

### Phase 2: Automation (Runner)
- [ ] Skripte für automatische Gates (`scripts/v0_web_gate.sh`).
- [ ] `v0_n8n` Skill mit n8n-mcp Integration.
- [ ] Patch-Protocol (Regeln für Fixes) etablieren.

### Phase 3: The Frontdoor (Voice/Chat)
- [ ] Moltbot installieren & konfigurieren.
- [ ] WhatsApp/Telegram anbinden.
- [ ] `v0_bridge` bauen (Chat triggert OpenCode Command).

---

## 5. Referenz-Dokumente (DeepResearch)

*   [Detail-Konzept v0 Builder](docs/research-v0-builder-platform.md)
*   [Detail-Konzept Voice Gateway](docs/research-voice-gateway.md)
*   [Analyse OpenCode Stack](docs/research-opencode-analysis.md)
