# PHASE 0 — OWNER-MODE AUDIT + SCOPE LOCK (WANDA)

You are the OWNER + MAINTAINER + RELEASE ENGINEER of this repository.
Goal: produce a **repo-aware SSOT package** and a **Phase-1 implementation plan**, without doing large refactors yet.

## Non-negotiable rules
- Zero assumptions: verify everything in the repo.
- Make changes only to add missing SSOT docs or fix obviously broken docs links.
- Prefer official docs and primary sources.
- If anything is ambiguous, write it down as an **Explicit Decision**.

## Inputs you must discover from the repo
- Current `README.md` and any install docs (manual and AI prompts)
- Current CLI commands and how Wanda is invoked
- Current config locations, formats, and precedence
- Current OS support, dependencies, and packaging approach
- Existing voice pipeline (mic, silence detection, TTS), coding pipeline (OpenCode/others)

## External references you must use (primary)
- OpenCode docs: https://opencode.ai/docs/ecosystem/
- MiCode: https://github.com/vtemian/micode
- oh-my-opencode README raw: https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/README.md
- opencode-orchestrator: https://github.com/BuffMcBigHuge/opencode-orchestrator

## Deliverable A — SSOT Package (must be generated in-repo)
Create/ensure the following structure exists (SSOT):

/README.md
/docs/00_overview (PROJECT.md, GOALS.md, SCOPE.md, GLOSSARY.md)
/docs/01_research (RESEARCH_LOG.md, SOURCES.md)
/docs/02_architecture (ARCH.md, DATA_MODEL.md, INTEGRATIONS.md, SECURITY.md)
/docs/03_decisions (ADR-0001.md ...)
/docs/04_plan (MILESTONES.md, TASKS.md)
/docs/05_specs (SPEC_CLI.md, SPEC_INSTALLER.md, SPEC_FLOWS.md)
/prompts/tasks (PHASE1_IMPLEMENTATION_PROMPT.md placeholder)

Populate them with repo-grounded facts.

## Deliverable B — Drift Report
Write `docs/01_research/DRIFT_REPORT.md` containing:
- Which docs are outdated
- Which commands don’t exist or differ
- Which OS-specific steps are wrong
- Missing features vs requested scope

## Deliverable C — Phase-1 Implementation Plan (no code yet)
Write `docs/04_plan/PHASE1_PLAN.md`:
- Milestones M1..M5
- Dependencies and risks
- Test plan (doctor checks + CI)
- Rollback plan

## Specific scope you must plan for
1) Docs refactor:
   - `AI_INSTALLATION.md` becomes canonical.
   - `AI_INSTALL_PROMPT.md` becomes **2–3 lines** max and points to AI_INSTALLATION.
   - `README.md` has **2 lines** that point to AI_INSTALLATION.

2) Dual system modes:
   - `wanda voice`, `wanda code`, `wanda` (router)
   - single-mode and double-mode must work.

3) Installer behavior:
   - Fresh install
   - Reinstall without wiping tokens/settings
   - Update mode: `wanda update` + optional startup update check; if update found then auto-apply at next start
   - Clean UX: defaults + recommended settings + step-back

4) Cross-platform:
   - Linux (COSMIC Wayland + GNOME)
   - Windows
   - macOS incl. Apple Silicon (M-series)

5) Hardening:
   - logs, diagnostics bundle, issue templates
   - safe permissions, least privilege, no silent destructive ops

6) Agent/plugin harmony:
   - Inventory all agents that come from OpenCode + oh-my-opencode + MiCode + orchestrator
   - Document which should be enabled/disabled by default and why
   - Document config file locations and precedence

## Output format
At the end, print:
- A link/paths to the created SSOT files
- The 10 most important decisions remaining
- A checklist for Phase-1 prompt readiness
