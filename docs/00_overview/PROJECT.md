# PROJECT — Wanda (Docs + Installer + Dual-Mode)

## One-liner
Turn Wanda into a **cross-platform, hardened CLI system** with a *clean installer UX*, a *dual-mode runtime* (voice/code), and a *minimal README* that delegates to a comprehensive AI-first installation guide.

## Why now
- Current AI installation prompt/docs are too long and not structured for agent-based installs.
- Plugin/agent ecosystems (OpenCode + oh-my-opencode + MiCode + orchestrators) create overlap risk.
- A reliable installer + update path is required before broader distribution.

## Goals

### Must
- **Agent-first install path** (works for Claude Code/OpenCode/Codex/etc.)
- **Human/manual install path** remains available
- **Deterministic config locations** with clear precedence rules
- **Dual-system modes** (single: voice OR code; and combined)
- **Installer UX**: defaults + recommendations + back/redo + safe re-install
- **Update mode**: `wanda update` + optional startup check & delayed auto-update
- **Hardening**: edge cases, rollback, logs, diagnostics, issue templates

### Should
- Minimal friction for new users (1–2 commands total)
- Token-efficient operation (fast models for tooling/search; strong models for architecture)
- Testable installation steps (doctor checks)

### Won’t (Phase 0)
- Shipping a full GUI (unless already present in repo)
- Deep model/provider politics beyond safe, official auth flows

## Scope

### In scope
1) Docs refactor: README + AI install prompt + full AI installation guide
2) Repo alignment: docs match current behavior; remove drift
3) Installer flow:
   - Fresh install
   - Re-install without nuking tokens/settings
   - Update mode
4) Modes:
   - `wanda` (default)
   - `wanda voice`
   - `wanda code`
   - `wanda` as “double system” mode that can delegate between voice+code
5) Cross-platform support matrix + automated doctor checks
6) Agent/plugin alignment:
   - OpenCode plugin loading
   - oh-my-opencode config and agent overrides
   - MiCode integration
   - opencode-orchestrator compatibility (optional)
7) v0-style skills packaging (final step): reusable skills/pipelines

### Out of scope (unless already in repo)
- Rewriting OpenCode/oh-my-opencode internals
- Non-official auth bypasses

## Primary deliverables
- `AI_INSTALLATION.md` (canonical, long, exhaustive)
- `AI_INSTALL_PROMPT.md` (2–3 lines max; points to AI_INSTALLATION)
- `README.md` minimal pointer (2 lines) + normal human install remains available
- `wanda` CLI commands: `install`, `config`, `doctor`, `update`, plus modes `wanda`, `wanda voice`, `wanda code`
- Cross-platform: Linux (COSMIC/GNOME), Windows, macOS (incl. Apple Silicon)

## Glossary
- **SSOT**: Single Source of Truth — one canonical place for each decision/spec.
- **Phase 0**: Audit + scope locking, no risky refactors without a plan.
- **Doctor**: A self-check command that validates prerequisites and configuration.
- **User config**: Config that applies globally for the current user profile.
- **Project config**: Config scoped to a repo/project directory.