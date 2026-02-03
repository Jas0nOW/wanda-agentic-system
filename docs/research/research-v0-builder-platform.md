# Universal v0-Style Builder als Skill-Plattform für OpenCode Sovereign System, n8n und Ops

## Executive Summary

> **Hinweis:** Upstream-Quellen nennen `Sisyphus` als Default-Orchestrator. In WANDA ist **Commander** der einzige Primary; `Sisyphus` bleibt als Plugin-Default deaktiviert.

 Dein aktuelles “OpenCode Sovereign System” ist bereits eine sehr starke Grundlage: 9 Agenten (Sisyphus als Orchestrator), ein klarer 3‑Phasen‑Workflow (Grounding → Building → Fixing) und ein MCP‑Toolkit (u. a. Context7 + Web Search) sind schon genau die “Plumbing”, die Tools wie v0 und 10web im Kern erfolgreich macht. fileciteturn0file0 fileciteturn0file1

Der entscheidende Hebel, um das “v0/10web‑Feeling” **universell** (Web, Apps, n8n‑Workflows, Ops) zu bekommen, ist nicht “mehr Agenten”, sondern eine **Skill‑Plattform** mit:

Contract‑first Artefakten (Specs als Single‑Source‑of‑Truth), standardisierten Runners/Executors, einem begrenzten Self‑Healing‑Fix‑Loop und profilierten Quality Gates inklusive Exports. Das entspricht genau dem, was v0 als Plattform verspricht (Agent: Web Search, Site Inspection, Error Fixing, Integrationen) – nur mit deiner lokalen Orchestrierung und deinen Abos/CLIs. citeturn1view5turn12view0

Wichtig für “SOTA + Abo‑Lebensdauer”: Du brauchst eine **Cost/Quality/Latency Policy Engine** (Router‑Regeln, Budget‑Stops, Caching, Context‑Budgeting). Deine Basis erlaubt das schon: OpenCode Commands können Shell‑Output gezielt in Prompts injizieren (`!`), Dateien selektiv referenzieren (`@`), und oh‑my‑opencode liefert Hooks für Compaction/Truncation und LSP‑Refactoring – alles direkt verwertbar für Token‑Effizienz und deterministische Pipelines. citeturn12view0turn14view3turn3search2

**MVP‑Scope (realistisch, “funktioniert sicher”)**  
Du implementierst zunächst zwei Skills:

* `v0_web`: Prompt → UI_SPEC.yml → Code → lint/build/typecheck → Fix‑Loop (max 3) → Export  
* `v0_n8n`: Prompt → N8N_SPEC.yml → workflow.json → Create/Update über n8n Public API → Smoke‑Test über Trigger/Webhook → Fix‑Loop → Export

(Optional V1): `v0_ops` für Deploy/SEO/Performance/Monitoring, inspiriert am 10web‑End‑to‑End‑Ansatz (bauen + optimieren + managen). citeturn10search0turn10search12turn10search3turn10search15

---

## Ist-Analyse deines aktuellen Systems

**Install/Runtime & Kernannahmen**  
Du installierst OpenCode über `bun` und pinnst die Version auf **1.1.36**, plus oh‑my‑opencode Harness, plus “Antigravity Auth Bridge” (Trennung von Provider‑Keys vs. Abo‑Tokens). fileciteturn0file0  
Dabei ist wichtig: OpenCode hat inzwischen neuere Releases (z. B. **v1.1.40 vom 28. Jan 2026**) – du solltest das Pinning als bewusstes “Stability Profile” behandeln und Updates gezielt in einem Test‑Profil evaluieren, statt ad‑hoc. citeturn13search0turn13search18

**Agentic Architektur & Workflow**  
Dein System ist klar strukturiert:

* 9 Agenten mit Rollen (Sisyphus orchestriert; Architect macht Blueprint; Developer baut; Audit fix & security; UI/UX für Design; Oracle für komplexe Logik; Writer, Librarian, Explore). fileciteturn0file1  
* 3‑Phasen‑Protokoll: Architect → Developer/UI → Audit. fileciteturn0file0 fileciteturn0file1  
* Fallback‑Matrix über mehrere Provider (Antigravity → Anthropic → GitHub Copilot → Google → OpenAI). fileciteturn0file1

**Commands/Skills heute**  
Du hast Command Injection mit `/init-deep` und `/ralph-loop`. `/ralph-loop` ist bereits ein generisches Orchestrations‑Pattern (Blueprint → Implementieren/Testen → Security Scan). fileciteturn0file0  
OpenCode unterstützt Custom Commands offiziell über Markdown‑Files (global: `~/.config/opencode/commands/`, projektbezogen: `.opencode/commands/`) samt YAML‑Frontmatter (description/agent/model) sowie `!`‑Shell‑Output‑Injection und `@`‑File‑References. Das ist die technische Basis, um “v0‑Skills” als wiederholbare Pipelines zu definieren. citeturn12view0

**MCP Setup: funktional, aber mit SOTA‑Drift‑Risiko**  
In deiner Doku heißt die Config‑Property `mcpServers`. In aktuellen OpenCode‑Docs heißt sie `mcp`. Das ist ein echter Drift‑Hotspot: Wenn du künftig sauber “SOTA” bleiben willst, empfehle ich, die Config strikt am Schema (`$schema: https://opencode.ai/config.json`) auszurichten und MCPs über den `mcp`‑Block zu definieren. fileciteturn0file0 citeturn17search0turn3search3

**Was v0/10web‑Feeling noch bremst (die echte Lückenliste)**  
Du bist “v0‑ready” beim Orchestrieren – aber für “v0‑Qualität reproduzierbar” fehlen heute vier harte Bausteine:

1. **Contract‑first Zwischenartefakte** als Single Source of Truth pro Skill (UI_SPEC / N8N_SPEC / OPS_SPEC), statt nur “blueprint.md”. (Du hast Blueprint‑Denke, aber noch nicht Spec‑Schemas + Validation.) fileciteturn0file0  
2. **Runner/Executor pro Skill** (Web: lint/build/typecheck/tests; n8n: create/update + smoke test + execution logs; ops: deploy + post‑deploy checks). OpenCode Commands können Runner‑Outputs gezielt einspeisen (`!`), was du aktuell im `/ralph-loop` noch nicht “standardisiert” nutzt. citeturn12view0  
3. **Fix‑Loop Controller** mit Stop‑Conditions (max Iterationen, Scope Guard, Budget Stop). Ohne das droht genau das, was Nutzer bei v0 “Agent Mode” bemängeln: Wiederholungen, unnötige Reviews, steigende Kosten. citeturn0search11  
4. **Eval/Regression Harness**, damit das System über Zeit messbar besser wird (statt “immer wieder neu prompten”). Oh‑my‑opencode liefert bereits Token‑/Context‑Management‑Hooks, aber du brauchst die produktive “Mess‑Schicht” darüber. citeturn14view3

---

## Zielarchitektur als Skill-Plattform mit Profiles

**Kernidee: Skills statt “ein Prompt”**  
Du baust eine Skill‑Registry: Jeder Skill ist eine deterministische Pipeline mit Contracts, Runner, Fix‑Loop, Export und Qualitätsgates – ausspielbar über OpenCode Commands (und später optional als Plugin/SDK‑Integration). citeturn12view0turn17search23turn17search27

**Skill Registry (Minimal, aber skalierfähig)**  
Die Registry besteht aus einem Ordner pro Skill (project‑local in `.opencode/` oder `.v0/`), plus globalen Defaults.

Empfehlte Basispfade (konsequent token‑sparend, weil “Truth” immer in wenigen Dateien liegt):

* `.v0/contracts/` (Schemas & Templates)  
* `.v0/specs/` (UI_SPEC.yml, N8N_SPEC.yml, OPS_SPEC.yml)  
* `.v0/runs/` (Runner Outputs, stark redaktiert)  
* `.v0/exports/` (Patch/ZIP/Instructions/Reports)  
* `.v0/eval/` (Benchmarks & Results)

**Profiles (entscheidend für “v0 für alles”)**  
Profiles sind Policy‑Bundles: Stack + Allowed Dependencies + Gates + Router‑Budgets. Beispiele:

* `profile:web-mvp`: Next.js + Tailwind + shadcn/ui; schnelle Iteration; minimale Tests. (v0‑kompatibel, weil v0 explizit Next.js/Tailwind/shadcn/ui als “modern stack” unterstützt.) citeturn1view5  
* `profile:saas`: zusätzlich auth/DB, strengere Gates (tests, e2e smoke).  
* `profile:n8n-prod`: strikte “no secrets in JSON”, dry‑run defaults, rollback‑Pflicht, Exec‑Monitoring.  
* `profile:ops-10web-like`: deploy + lighthouse/perf budgets + SEO baseline + monitoring.

**Mechanik: Deterministische Orchestrierung in OpenCode**  
OpenCode Agents lassen sich gezielt invoken (`@agent`) und Commands können eine bestimmte Engine/Agent erzwingen (Frontmatter `agent:`/`model:`). citeturn12view0turn1view2  
Oh‑my‑opencode bringt zusätzlich: konfigurierte Agents, Hooks, MCP‑Defaults (Context7/grep_app) und LSP‑Refactoring, was du bewusst für Token‑Effizienz und Präzision einsetzen kannst. citeturn14view3turn3search2turn17search5

---

## Skill Designs und Runner-Architektur

### Skill v0_web

**Was “v0‑Feeling” hier bedeutet (Mechanik, nicht UI)**  
v0 beschreibt sich als AI‑Platform, die Ideen in production‑ready Web‑Apps verwandelt, inklusive Web‑Search, Site‑Inspection und automatischem Error‑Fixing. citeturn1view5  
Dein Äquivalent lokal: **Spec‑first → Build‑Runner → Fix‑Loop**.

**Pipeline (ASCII)**  
User Prompt → Sisyphus → UI_SPEC.yml → (UI/UX) → Code‑Patch → Runner (lint/build/typecheck/tests) → Fixer → Gate → Export

**Runner‑Standard (MVP)**  
Für Web ist ein MVP‑Runner “lint + build + typecheck” (plus optional tests). Das passt exakt zu deinen existierenden Quality Gates “Compiles / Tests / Lint / Audit”. fileciteturn0file0

**Warum Next.js/Tailwind/shadcn/ui als Default‑Stack**  
Nicht weil “hip”, sondern weil v0 diesen Stack explizit unterstützt (“works with your stack … Next.js, Tailwind, shadcn/ui”). Damit ist die Prompt‑/Pattern‑Kompatibilität maximal. citeturn1view5

**Bekannte v0‑Failure‑Modes als Design‑Input**  
In Vercel Community und shadcn‑Issues sieht man typische Probleme: Version‑Mismatch, Export‑Konventionen (named exports), “Fix with v0” rotiert in Loops, und `shadcn add`/Registry Mismatches. Das sind exzellente Gründe, deine Pipeline lokal über echte Builds zu “erden” und Fix‑Loops hart zu begrenzen. citeturn0search26turn0search30turn0search2

### Skill v0_n8n

**Wahrheitsquelle: n8n‑MCP + n8n API**  
Dein Ansatz ist richtig: Node‑Wissen muss “Truth‑sourced” werden. Moderne MCP‑Server wie `czlonkowski/n8n-mcp` zielen genau darauf: Zugriff auf Node‑Doku/Properties/Operations, teils plus Templates. Die Node‑Zahlen schwanken je Quelle (und ändern sich), darum darf deine Pipeline keine festen Node‑Counts hardcoden. citeturn16search8turn16search12turn0search7turn0search33

**Wichtig: n8n kann selbst MCP Server sein**  
n8n hat einen MCP Server Trigger Node, der ein MCP‑URL‑Endpoint bereitstellt; er unterstützt SSE und streamable HTTP, aber kein stdio, und hat klare Einschränkungen bei mehreren Webhook‑Replicas (SSE/streamable HTTP brauchen “sticky” Routing). citeturn1view4  
Das ist relevant für “AI‑Tools auf n8n‑Workflows” – aber für deinen Builder‑Skill ist primär: Workflow‑JSON korrekt erzeugen + deploy/testen.

**Deployment & Auth**  
n8n Public REST API nutzt API‑Keys; der Key wird per Header `X-N8N-API-KEY` gesendet. citeturn5view2  
Die API ist laut n8n‑Docs in der Free Trial nicht verfügbar (Plan‑/Feature‑Constraint). citeturn5view1turn5view2  
Und in der Praxis musst du API‑Keys im n8n UI erstellen (Community bestätigt: nicht per Env‑Vars setzbar). citeturn4search11turn5view2

**Test‑Execution Realität (kritisch)**  
Ein häufiger Wunsch ist “Workflow per API wie ‘Execute Workflow’ starten”. n8n Community sagt dazu klar: Es gibt keinen dokumentierten Public API Endpoint, der ein beliebiges Workflow‑ID analog zum Editor‑Button “Execute Workflow” triggert; empfohlen wird Webhook Trigger als “API‑Trigger”. citeturn4search1turn6search9turn6search29  
Das beeinflusst deinen Runner: Smoke‑Tests müssen über Trigger laufen (Webhook/Cron/Test‑Events) oder über eine eigene “Manager‑Workflow”‑Schicht, die Webhooks/Execute‑Workflow Patterns kapselt. (n8n bietet dafür sogar Templates wie “workflow manager API”.) citeturn6search13turn6search1

### Skill v0_ops

**10web‑Feeling als Mechanik**  
10Web beschreibt sich als “Automated WordPress Platform” mit AI‑Builder, Hosting (Google Cloud), Optimierung, Management und automatischer Maintenance. citeturn10search0turn10search12  
Das “Feeling” entsteht durch: Deploy + Speed/Perf + Backups + Security + Monitoring, nicht nur durch “HTML generieren”.

**Vercel‑kompatibles Ops‑Subset (sehr praktikabel für Next.js)**  
Vercel selbst dokumentiert Integrations‑basiertes Performance Monitoring (z. B. Calibre, DebugBear) und hat ein Integrations‑Ökosystem. citeturn10search1turn10search7turn10search33  
Das liefert dir klare Runner‑/Gates: deploy → post‑deploy checks → perf budgets.

---

## Contracts, Commands, Router Policies und Roadmap

### Prompt-Contracts als Single Source of Truth

**UI_SPEC.yml (Template, copy‑paste)**  
```yaml
schema_version: 1
profile: web-mvp
meta:
  task: "$ARGUMENTS"
  created_at: "<ISO-8601>"
  owner: "LazyTechLab"
stack:
  framework: "nextjs"
  language: "typescript"
  styling: "tailwind"
  ui_library: "shadcn-ui"
constraints:
  allowed_libs:
    - "react"
    - "next"
    - "tailwindcss"
    - "lucide-react"
  forbidden:
    - "new UI frameworks without Context7 proof"
    - "adding auth/db unless requested"
routes:
  - path: "/"
    page_name: "Home"
    layout: "marketing"
    components:
      - name: "Hero"
        props:
          title: "..."
          subtitle: "..."
          cta_primary: { label: "Get started", href: "/signup" }
      - name: "FeaturesGrid"
      - name: "FAQ"
state:
  global: []
  per_route:
    "/":
      - name: "newsletterEmail"
        type: "string"
        validation: "email"
data_mocks:
  enabled: true
  fixtures:
    - name: "pricingPlans"
      type: "array"
dod:
  build:
    - "pnpm lint passes"
    - "pnpm build passes"
    - "Typecheck passes (tsc/next typecheck)"
  ux:
    - "mobile-first"
    - "basic a11y (labels, focus states)"
  scope:
    - "only touch files under src/ (or app/) and components/"
export:
  format: ["git-branch", "patch"]
  report: ".v0/exports/EXPORT.md"
```

**N8N_SPEC.yml (Template, copy‑paste)**  
```yaml
schema_version: 1
profile: n8n-prod
meta:
  task: "$ARGUMENTS"
  n8n_instance: "<name>"
  n8n_api:
    base_url: "<https://your-n8n-host>"
    api_version: "v1"
    auth: "X-N8N-API-KEY"
  created_at: "<ISO-8601>"
requirements:
  triggers:
    # für Smoke-Tests zwingend: Webhook (oder alternative Trigger)
    - type: "webhook"
      method: "POST"
      path: "/ai/smoke-test"
      expects_json: true
  inputs:
    - name: "payload"
      type: "object"
  outputs:
    - name: "result"
      type: "object"
design:
  node_source_of_truth: "n8n-mcp"
  allow_custom_code: true
  code_node_language: "javascript"
  error_strategy:
    continue_on_fail: false
    error_trigger: true
credentials:
  policy:
    - "NO secrets embedded in workflow.json"
    - "use n8n Credentials placeholders by name"
    - "env vars allowed via expressions"
workflow:
  name: "AI Generated Workflow"
  tags: ["ai", "builder"]
  nodes:
    - role: "trigger"
      must_be: ["Webhook"]
    - role: "validation"
      patterns: ["schema validation", "guardrails"]
    - role: "main"
      patterns: ["http request", "transform", "branching"]
dod:
  api:
    - "create/update via n8n public API succeeds"
  smoke_test:
    - "trigger endpoint returns 200 for valid input"
    - "returns structured error for invalid input"
  ops:
    - "workflow can be deactivated (rollback) without manual UI steps"
export:
  files:
    - "workflow.json"
    - "EXPORT.md"
```

**OPS_SPEC.yml (Template, copy‑paste)**  
```yaml
schema_version: 1
profile: ops-10web-like
meta:
  task: "$ARGUMENTS"
targets:
  deploy:
    provider: "vercel"   # optional: "docker", "self-host", etc.
    environment: "preview"
  domain:
    required: false
checks:
  http:
    - url: "<deployment-url>/"
      expect_status: 200
    - url: "<deployment-url>/sitemap.xml"
      expect_status: 200
  seo_baseline:
    - "meta title/description present"
    - "open graph tags present"
  performance:
    strategy: "lighthouse"
    budgets:
      performance: 0.8
      accessibility: 0.9
      best_practices: 0.85
      seo: 0.85
monitoring:
  uptime:
    enabled: true
  error_tracking:
    enabled: false
dod:
  - "deploy succeeded"
  - "post-deploy checks succeeded"
```

**Warum diese Form?**  
Weil OpenCode Commands Shell‑Outputs (`!`) und selektive File‑Kontexte (`@`) unterstützen – du willst also Specs so definieren, dass der Builder fast nie “alles lesen” muss. citeturn12view0

### Patch Protocol (Scope Guard, copy‑paste)

```markdown
# PATCH_PROTOCOL.md (Skill-agnostisch)

## Allowed Changes
- Web: only under app/, src/, components/, styles/, public/, package.json scripts if needed
- n8n: only workflow.json + EXPORT.md + test payload fixtures
- Ops: only deploy scripts + OPS_SPEC.yml + EXPORT.md

## Forbidden
- No secrets in any committed file
- No new dependencies without Context7 citation or explicit approval
- No refactors unrelated to failing gate

## Minimal-Diff Rule
- Prefer smallest change that makes the failing gate pass
- Change ≤ 3 files per fix iteration unless explicitly justified

## Fix Loop Limits
- max 3 iterations per gate failure
- if still failing: write ROOT_CAUSE.md + next actions
```

### Log Pack Format (Token‑effizient)

Du willst Logs nicht “voll reinballern”. Mit OpenCode kannst du Log‑Output gezielt injizieren – aber du solltest ihn **stark redaktieren** und in Stufen liefern.

```yaml
# LOG_PACK.yml
context_level: "short|medium|long"
includes:
  - "gate_status_summary"
  - "top_errors_only"
  - "changed_files_list"
  - "minimal_repro_steps"
redaction:
  remove:
    - "tokens"
    - "api keys"
    - "full stack traces if not needed"
```

### OpenCode Commands als Skills (copy-paste-fähig)

OpenCode dokumentiert Custom Commands via Markdown‑Files + YAML‑Frontmatter; file name wird zum Command‑Namen, und du kannst `!` zum Injizieren von Shell‑Output nutzen. citeturn12view0

**`.opencode/commands/v0-web.md`**  
```markdown
---
description: "v0_web: Spec → Code → Build Gates → Fix Loop → Export"
agent: sisyphus
subtask: false
---

Du bist Sisyphus (Orchestrator). Ziel: v0-style Web Building mit maximaler Token-Effizienz.

1) CONTRACT
- @architect: Erstelle .v0/specs/UI_SPEC.yml (nutze das Template in .v0/contracts/UI_SPEC_TEMPLATE.yml).
- @frontend-ui-ux: Review UI_SPEC.yml (mobile-first, a11y, Design-Tokens).

2) IMPLEMENT
- @software-engineer: Implementiere exakt nach UI_SPEC.yml.
- Nutze Context7 vor neuen libs. (Wenn neue lib nötig: nenne WHY + Kontext7-Snippet.)

3) RUNNER (GATES)
- Sammle Status vor dem Build:
  !`git status --porcelain`
  !`git diff --stat`

- Führe Gates aus (pass/fail muss eindeutig sein):
  !`pnpm -s lint || true`
  !`pnpm -s build || true`

4) FIX LOOP (max 3)
- Wenn FAIL: @audit bekommt NUR:
  - UI_SPEC.yml (per @.v0/specs/UI_SPEC.yml)
  - relevante Fail-Ausgaben aus den Runner-Outputs (oben)
  - Liste geänderter Dateien (!git diff --stat)
- @audit löst mit minimal-diff und hält PATCH_PROTOCOL.md ein.
- Danach Gates erneut ausführen (Step 3).
- Nach 3 Fehlschlägen: Schreibe .v0/exports/ROOT_CAUSE.md + Stop.

5) EXPORT
- @writer: schreibe .v0/exports/EXPORT.md (Setup, Run, Build, DoD-Status, bekannte Limits).
```

**`.opencode/commands/v0-n8n.md`**  
```markdown
---
description: "v0_n8n: Spec → workflow.json → Deploy/Test (API+Trigger) → Fix Loop → Export"
agent: sisyphus
subtask: false
---

Du bist Sisyphus. Ziel: n8n Workflow Builder mit n8n-mcp als Truth Source und n8n Public API als Deploy-Mechanik.

0) IMPORTANT REALITY CHECK
- Es gibt keinen dokumentierten Public API Endpoint, um beliebige Workflows wie 'Execute Workflow' per ID zu starten.
- Smoke Tests müssen über Trigger laufen (Webhook empfohlen).

1) CONTRACT
- @architect: Erstelle .v0/specs/N8N_SPEC.yml (nutze Template).
- @librarian: Ziehe Node-Wahrheit über n8n-mcp (Node Names + Parameter-Schema + Beispiele).
  Output: .v0/specs/NODE_PALETTE.yml (nur die Nodes, die wir brauchen).

2) GENERATE
- @software-engineer: Erstelle workflow.json (NO secrets; placeholders only).

3) DEPLOY (n8n API)
- Prüfe API Auth Header-Konzept:
  (Dokumentation: X-N8N-API-KEY)
- Runner nimmt env vars N8N_API_URL + N8N_API_KEY aus sicherer Umgebung (nicht committen).

4) SMOKE TEST
- Workflow MUSS Webhook Trigger haben, damit wir per HTTP testen können.
- Sende ein minimales Test-Payload und prüfe 200/structured error.

5) FIX LOOP (max 3)
- Wenn Deploy/Smoke-Test failt: @audit bekommt:
  @.v0/specs/N8N_SPEC.yml
  @.v0/specs/NODE_PALETTE.yml
  @workflow.json
  Runner Output (gekürzt)

6) EXPORT
- @writer: EXPORT.md (Import/Activate/Test, Rollback/Disable Steps)
```

**Warum Commands (und nicht sofort Plugin)?**  
Weil es der schnellste Weg zum MVP ist, und OpenCode Commands bereits `!`‑Shell Injection + `@`‑File References + Agent‑Binding supporten. citeturn12view0  
**V1/V2** kann den Runner als Plugin/Tool kapseln (weniger Token‑Noise), denn OpenCode unterstützt Plugins, Custom Tools, und hat Server+SDK für programmatic control. citeturn3search18turn17search27turn17search23

### Roadmap (MVP → V1 → V2, timeboxed)

**MVP (1–2 Tage, “läuft stabil”)**
* Lege `.v0/` Struktur + Templates an.  
* Implementiere `v0-web` und `v0-n8n` Commands.  
* Baue je Skill einen minimalen Runner‑Script‑Wrapper (z. B. `scripts/v0_web_gate.sh`, `scripts/v0_n8n_deploy.sh`).  
* Definiere Stop‑Conditions (max 3 Iterationen). (Explizit, weil Agent‑Loops sonst Kosten multiplizieren – beobachtbar auch bei v0 Agent Mode.) citeturn0search11turn12view0

**V1 (2–5 Tage, “professionell & token‑sparend”)**
* “Policy Engine” als Router‑Regeln (cheap → mid → expensive) mitsamt Budget‑Stops.  
* Eval Harness: 20 Tasks Web + 20 Tasks n8n als Regression Set.  
* Add “Profiles” + Gates pro Profil.

**V2 (laufend, “letztes Level”)**
* Plugin/Tool: Runner liefert strukturierte Fehler statt ganzer Logs (Token‑Effizienz). citeturn17search7turn3search18  
* Ops Skill (`v0_ops`) inkl Deploy + SEO/perf budgets + Monitoring. (Vercel Integrations bieten dafür konkrete Pfade.) citeturn10search33turn10search1turn10search7  
* Optional: UI/Non‑Tech Oberfläche über OpenWork (“opencode config → usable experiences”). citeturn13search27

---

## Evaluation, Security, Troubleshooting und Minimal Pattern Library

### Evaluation & Regression Harness (damit du nicht rückfällig wirst)

**Warum zwingend**  
Ohne Regression Suite wirst du bei jedem neuen Projekt “neu prompten” und bekommst Drift. Mit Suite misst du: “Welche Policy/Persona Änderung hat Qualität verbessert vs verschlechtert?”

**Minimal‑Setup (praktikabel)**
* `eval/tasks/*.yml`: Prompt + Profile + erwartete Gates.  
* `eval/run.sh`: startet OpenCode non‑interactive gegen ein Repo‑Fixture (OpenCode CLI erlaubt programmatic Runs). citeturn3search10turn3search20  
* `eval/results/*.json`: Gate‑Status, Iterationszahl, Kosten‑Schätzung (siehe Token‑Playbook unten).

n8n‑seitig kannst du “Execution Data” nutzen, um Test‑Runs zu taggen/auffindbar zu machen (Limitierungen für Key/Value Größen beachten). citeturn6search22

### Security Playbook (konkret, nicht generisch)

**Supply Chain & Dependency Risiken**  
OWASP behandelt Software Supply Chain Security explizit (u. a. Dependency Confusion, kompromittierte Upstreams, CI/CD Exploits). citeturn10search2  
Für Node/JS ist die OWASP NPM Security Cheat Sheet sehr konkret (Lockfile erzwingen, run‑scripts minimieren, Audits). citeturn10search26  
OWASP CI/CD Top‑10 beschreibt “Dependency Chain Abuse” als konkretes Risiko beim Nachladen von Dependencies. citeturn10search22

**Tooling‑spezifische Risiken (für dein Setup extrem relevant)**  
* OpenCode hatte ein Advisory: automatisch gestarteter, unauthentifizierter HTTP Server kann laut Advisory dazu führen, dass lokale Prozesse oder Websites via permissive CORS Shell Commands ausführen. Das muss in deinem Hardening‑Profil berücksichtigt werden (z. B. Server deaktivieren/restriktiv binden, Netzwerk‑Policies). citeturn13search23turn17search27  
* Gemini CLI hatte 2025 einen gemeldeten Security Flaw rund um allow‑listed command execution (Tracebit‑Bericht via Presse), mit Fix‑Hinweis auf Version‑Update und Empfehlung zu Sandboxing (Docker/Podman/macOS Seatbelt). Das ist 1:1 relevant, weil dein System stark “bash‑fähig” ist. citeturn11news36turn11news37

**n8n Secrets Hygiene**
* n8n API Auth läuft über `X-N8N-API-KEY` Header; Keys werden im UI erstellt und können (Enterprise) scoped werden – das ist deine Basis für least‑privilege Deploy Keys. citeturn5view2turn4search11  
* In deinen Contracts: “NO secrets embedded in workflow.json” ist Pflicht (Credentials als placeholders + n8n Credential Store).

### Troubleshooting Map (Kurz, aber wirksam)

**Web (Next.js/Tailwind/shadcn)**
* Wenn “v0 export/shadcn add” bricht: bekanntes Muster sind Registry/Version‑Mismatches; dein Runner muss lokal bauen und ggf. Versions‑Pinning erzwingen. citeturn0search30turn0search23  
* Named Export vs default export kann bei v0 Deploy/Preview Fehlern relevant sein; in Vercel Community wird explizit auf named exports hingewiesen. citeturn0search26

**n8n**
* Update‑Workflow API erfordert typischerweise das Posten des gesamten Node‑Graphs (nicht “einzelne Nodes” patchen). citeturn4search20turn6search11  
* “Execute workflow by ID via API” ist nicht dokumentiert; setze daher konsequent auf Trigger (Webhook) für Smoke Tests. citeturn4search1turn6search9  
* Beim MCP Server Trigger musst du bei mehreren Webhook‑Replicas sticky routing für `/mcp*` sicherstellen, sonst brechen SSE/streamable HTTP Verbindungen. citeturn1view4

### Minimal Pattern Library (Startset, damit dein Builder nicht halluziniert)

**Web Patterns (10) – als Specs wiederverwendbar**
1. Marketing Landing (Hero + Features + FAQ + CTA)  
2. Pricing (Plan Cards + Comparison Table)  
3. Auth Shell (Sign‑in/Sign‑up + forgot password)  
4. Dashboard Layout (Sidebar + Topbar + responsive)  
5. CRUD Table (filters + pagination + dialog edit)  
6. Settings Page (tabs + forms)  
7. Wizard (multi-step form + validation)  
8. “Empty/Loading/Error” State Kit  
9. Upload flow (file + progress)  
10. Audit/Changelog page (events list)

**n8n Patterns (10) – “v0 für Workflows”**
1. Webhook → Validate → Transform → Respond  
2. Cron → Fetch API → Dedup → Notify  
3. Inbox automation: IMAP trigger → classify → route  
4. Lead enrichment: webhook → enrich via APIs → CRM update  
5. Retry wrapper: HTTP request with exponential backoff  
6. DLQ‑Pattern: on error → push to queue/store  
7. RAG ingest: scrape → chunk → vector db  
8. Monitoring: executions → alert on failure  
9. Backup flows: export workflows → store (Drive/S3)  
10. “Workflow manager API” façade: webhook triggers other workflows securely citeturn6search13turn6search6

---

## Token- und Credit-Effizienz Playbook

### Architekturprinzip: Token sparen, ohne “dumm” zu werden

Du hast schon eine Efficiency‑Philosophie im Kernel (“Batch ops”, “Fail fast”, “Cache context”). fileciteturn0file0  
Jetzt wird das operationalisiert.

### Policy Engine: Cost/Quality/Latency Router

**Warum Router?**  
Du nutzt mehrere Engines/Abos (Antigravity/Claude/Gemini/OpenAI/GitHub). Deine Doku hat bereits eine Fallback‑Matrix. fileciteturn0file1  
Damit daraus “Abo‑schonend” wird, brauchst du ein deterministisches routing:

**Router‑Regeln (Beispiel, anpassbar)**
* **cheap**: Outline/Blueprint/Spec‑Drafts (geringe Fehlerkosten)  
* **mid**: Implementierung im normalen Scope  
* **expensive**: Log‑basiertes Debugging, Refactor‑kritisch, Security Review

Sisyphus ist in deiner Konfiguration bewusst schnell gewählt (Gemini Flash) und soll delegieren; das passt perfekt zur Router‑Rolle. fileciteturn0file0

### Context Budgeting: “Minimal necessary context” als Standard

OpenCode Commands geben dir drei Hebel, die direkt Token sparen:

1. **`@file`**: nur relevante Dateien in den Prompt injizieren (statt Repo‑breit). citeturn12view0  
2. **`!` Shell Output Injection**: nur Gate‑Outputs, nicht blind alle Logs. citeturn12view0  
3. **subtask**: schwere Analysen als Subagent, um Primary Context sauber zu halten. citeturn12view0

### Compaction/Truncation: SOTA‑Hooks nutzen statt “mehr Kontext kaufen”

**OpenCode Compaction**  
OpenCode bietet `compaction.auto` und `compaction.prune` (prune entfernt alte Tool‑Outputs, spart Tokens). citeturn17search3

**Oh‑my‑opencode Token‑Features**  
Oh‑my‑opencode dokumentiert Preemptive Compaction, aggressive truncation, “truncate all tool outputs”, auto resume und DCP (Dynamic Context Pruning) als optionale Features (teils experimental). Das ist genau dein Werkzeugkasten, um Context‑Explosionen zu verhindern, ohne Qualität komplett zu killen. citeturn14view3

**Wichtig: MCPs sind nicht “kostenlos”**  
MCPs erhöhen Context und können Start‑Latency verursachen; es gibt Berichte/Issues, dass Context7 + grep_app lange binden und sogar das Senden von Messages blockieren können, bis MCPs verbunden sind. Daraus folgt: MCPs projektbezogen/Profil‑bezogen aktivieren, nicht global “alles an”. citeturn17search11turn14view3

### Prompt Pack Formate je Skill (short/medium/long)

**v0_web**
* short: UI_SPEC.yml + changed files list + top 1–3 errors  
* medium: + relevant file contents via `@` (max 3–5 Files)  
* long: + full build log nur wenn Fixer 2× scheitert

**v0_n8n**
* short: N8N_SPEC.yml + NODE_PALETTE.yml + API error snippet  
* medium: + workflow.json + minimal failing node subsection  
* long: + sanitized execution payload + redacted logs

### Kosten-Monitoring (praktisch, ohne Overengineering)

* Pro Skill‑Run: schreibe `.v0/runs/cost.json` (Model, Iterations, grobe Token‑Schätzung aus Output‑Größen + provider dashboard).  
* Alerts: “>3 Iterationen” oder “>Budget” → Stop.

Für programmatic control kannst du OpenCode server/SDK nutzen (Server startet zusammen mit TUI; SDK existiert). citeturn17search27turn17search23

### “Cheap mode vs Quality mode” (Konzeptbeispiel)

* Cheap mode: nur Spec + minimal gates; keine UI polish; keine e2e.  
* Quality mode: UI polish + a11y pass + optional screenshot/perf budgets (Vercel Integrations/Monitoring‑Patterns existieren). citeturn10search33turn10search1turn10search7

### Implementation Playbook (KI ausführbar, Schritt für Schritt)

1. Lege `.v0/` Struktur + Contract Templates an (UI_SPEC_TEMPLATE.yml, N8N_SPEC_TEMPLATE.yml, OPS_SPEC_TEMPLATE.yml, PATCH_PROTOCOL.md).  
2. Implementiere `.opencode/commands/v0-web.md` und `.opencode/commands/v0-n8n.md` (copy‑paste oben).  
3. Baue Runner‑Wrapper Scripts (`scripts/v0_web_gate.sh`, `scripts/v0_n8n_deploy.sh`) und nutze `!`‑Injection nur für deren **kurze** Summary (Top errors). citeturn12view0  
4. Ergänze Profiles (web-mvp, n8n-prod) als YAML‑Files; binde sie in Specs ein.  
5. Setze Budget‑Stops: max 3 Fix‑Iterationen; max credits pro Run; Stop → ROOT_CAUSE.md. (Begründung: vermeidet Agent‑Loops/Kostenmultiplikation, wie sie in v0 Agent Mode kritisiert wurden.) citeturn0search11  
6. Eval Harness: 10 Web Tasks + 10 n8n Tasks als Start; nightly run; speichere results JSON.  
7. Hardening: prüfe OpenCode server exposure (Advisory) und Gemini CLI sandboxing; dokumentiere in SECURITY.md. citeturn13search23turn11news36turn11news37  
8. Erst danach V1: Plugin/Custom Tool zur strukturierten Log‑Extraktion (Token‑Noise reduzieren). citeturn17search7turn3search18

**Quellenliste (kuratierte Kernquellen, die die tragenden Aussagen stützen)**  
OpenCode: Commands/Agents/Config/MCP/Server/SDK Docs. citeturn12view0turn1view2turn17search3turn17search0turn17search27turn17search23  
Oh‑my‑opencode: Config/Hooks/Experimental Features/LSP. citeturn14view3turn3search2turn17search5turn13search2turn13search26  
v0: Plattform‑Capabilities und typische Failure‑Modes. citeturn1view5turn0search11turn0search2turn0search30turn0search26  
n8n: API Auth & Limits, MCP Server Trigger, Execution‑Konzept, Execution‑Realität. citeturn5view2turn5view1turn1view4turn4search1turn6search9turn6search29turn6search5  
10web & Ops: 10Web Plattform/Booster, Vercel Monitoring/Integrations. citeturn10search0turn10search12turn10search3turn10search15turn10search33turn10search1turn10search7  
Security: OWASP supply chain & npm security & CI/CD dependency abuse; OpenCode advisory; Gemini CLI vuln reporting. citeturn10search2turn10search26turn10search22turn13search23turn11news36turn11news37
