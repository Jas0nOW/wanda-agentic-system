ROLE: WANDA “Repo Cleaner + SSOT Builder” (extrem vorsichtig, deterministisch, null Halluzination)
DATE: 2026-02-01
OS TARGET: Pop!_OS COSMIC (Wayland)

SSOT DECISION (FINAL):
- Google/Auth/Quota: ONLY opencode-antigravity-auth@latest
- OPTIONAL: opencode-antigravity-quota@latest (quota visibility)
- DO NOT include any other Google auth plugin (NO opencode-gemini-auth, NO opencode-google-antigravity-auth) in any config layer.
- Reason: single authoritative Google auth stack to avoid hook/provider collisions.
- Provider fallback: only within Google as supported by opencode-antigravity-auth (dual quota + auto rotation). Cross-provider fallback is out-of-scope unless explicitly added later.

PRIMARY SOURCES ONLY:
- OpenCode official docs (opencode.ai)
- Official GitHub repos of used plugins (esp. NoeFabris/opencode-antigravity-auth)
- Issue trackers when needed

HARD SAFETY RULES:
1) Work ONLY in a new branch: chore/wanda-ssot-clean-2026-02-01
2) No destructive changes: no deleting, no mass renaming, no moving folders. Deprecate instead.
3) Small commits after each phase. Every change must be reversible.
4) Fix-loop max 3 per issue. If unresolved: ASSUMPTION + verification method + safe default, then continue.
5) Never print secrets/tokens. Use placeholders + paths + .gitignore.

INPUTS (must read fully, not snippets):
- README.md
- docs/WANDA_FINAL_BLUEPRINT.md
- docs/WANDA_HANDBOOK.html
- docs/BEI PROBLEMEN.md
- docs/workflows/wanda-lifecycle.md
- docs/guides/setup.md
- docs/guides/contributing.md
- docs/architecture/vision.md
- docs/architecture/technical.md
- docs/architecture/agents.md
- docs/architecture/agent-roster.md
- docs/architecture/plugin-standards.md
- docs/research/* (all)
- templates/AGENTS.md.template

GOAL OUTPUTS (repo ends in a clean implementable state):
A) IMPLEMENTATION-PLAN.md (single SSOT file, deterministic, troubleshooting-first)
B) docs/SSOT/ (canonical, new)
   - SSOT_INDEX.md
   - INVENTORY.md
   - CONFLICTS.md
   - PLUGIN_STACK.md       (final plugin policy: antigravity-auth only for Google)
   - SOURCES.md            (deduped, categorized, with dates)
C) .opencode/skills/
   - v0_web/SKILL.md
   - v0_n8n/SKILL.md
   - v0_ops/SKILL.md
D) .v0/
   - contracts/ specs/ runs/ exports/ logs/
E) Coverage Matrix in IMPLEMENTATION-PLAN.md (every local file mapped to SSOT sections)

PHASE 0 — Safety snapshot
0.1) Create branch chore/wanda-ssot-clean-2026-02-01
0.2) Add docs/SSOT/WORKLOG.md and start logging decisions + commits

PHASE 1 — Inventory & conflicts
1.1) Create docs/SSOT/INVENTORY.md:
     Path | Purpose | Key facts | Dependencies | Conflicts
1.2) Create docs/SSOT/CONFLICTS.md:
     Conflict-ID | Locations | Why conflict | SSOT decision | ASSUMPTION? + How to verify
1.3) Commit: "chore(ssot): inventory + conflicts"

PHASE 2 — Sources & broken citation cleanup
2.1) Create docs/SSOT/SOURCES.md (primary sources only, deduped, dated)
2.2) Search docs for:
     - conflicting plugin lists
     - placeholders like “”
     - outdated provider/model names
2.3) Replace with:
     - a real primary source link OR
     - ASSUMPTION + verification command
2.4) Commit: "docs(ssot): sources + citation cleanup"

PHASE 3 — Plugin SSOT (single Google auth owner)
3.1) Create docs/SSOT/PLUGIN_STACK.md:
     - Final plugin list (KEEP/OPTIONAL/DROP)
     - Explicit rule: ONLY opencode-antigravity-auth for Google
     - Detect violations:
       - grep configs for "opencode-gemini-auth" and "opencode-google-antigravity-auth"
       - grep for duplicate "plugin" keys in JSON (JSON overrides!)
     - Known failure modes: plugin double-load (global/project), cache stale, load-order surprises
     - Provide verification checklist commands
3.2) Patch existing docs to reference PLUGIN_STACK.md as canonical, and mark old plugin lists as DEPRECATED (do not delete).
3.3) Commit: "docs(ssot): canonical plugin stack (antigravity-auth only)"

PHASE 4 — Skills skeleton (contract-first)
4.1) Create .opencode/skills/{v0_web,v0_n8n,v0_ops}/SKILL.md each with:
     - Purpose
     - Input schema (JSON Schema) + example payload
     - Pipeline steps (commands/tools)
     - Quality gates
     - Export artifact paths under .v0/exports/
4.2) Create .v0/{contracts,specs,runs,exports,logs}/ + .v0/README.md (run evidence rules)
4.3) Commit: "feat(skills): v0 skills + v0 structure"

PHASE 5 — IMPLEMENTATION-PLAN.md (single master SSOT)
Write IMPLEMENTATION-PLAN.md in EXACT order:
1) Executive Summary
2) Goals / Non-Goals
3) Glossary
4) System Overview Diagram (Mermaid)
5) Canonical Architecture + Sequence Diagram (Mermaid)
6) Agent Fleet SSOT (Commander primary; others delegated; reconcile template conflicts)
7) Plugin Inventory SSOT (final policy + conflicts + detection + fixes)
8) Skills Platform SSOT (.v0 structure + v0_web/v0_n8n/v0_ops)
9) Installation & Setup (Pop!_OS COSMIC, copy/paste)
10) Operations Playbook
11) Troubleshooting (quota, auth, plugin collisions, caches) + decision tree (Mermaid)
12) Security & Compliance (secrets, supply-chain, sandboxing)
13) Verification Checklist (green checks, smoke tests)
14) Coverage Matrix (every local file → SSOT sections)
15) Sources (deduped)
Commit: "docs: add IMPLEMENTATION-PLAN SSOT"

FINAL SELF-AUDIT (must be included at end of IMPLEMENTATION-PLAN.md):
- Every local file covered + listed
- Every conflict resolved or ASSUMPTION + verification method
- Plugin policy enforced (no other Google auth plugins anywhere)
- Setup steps reproducible
- Troubleshooting includes detection commands and minimal fixes
- Sources primary + deduped
