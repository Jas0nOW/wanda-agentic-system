# GOALS

## Must
- **Agent-first install path** (works for Claude Code/OpenCode/Codex/etc.)
- **Human/manual install path** remains available
- **Deterministic config locations** with clear precedence rules
- **Dual-system modes** (single: voice OR code; and combined)
- **Installer UX**: defaults + recommendations + back/redo + safe re-install
- **Update mode**: `wanda update` + optional startup check & delayed auto-update
- **Hardening**: edge cases, rollback, logs, diagnostics, issue templates

## Should
- Minimal friction for new users (1–2 commands total)
- Token-efficient operation (fast models for tooling/search; strong models for architecture)
- Testable installation steps (doctor checks)

## Won’t (Phase 0)
- Shipping a full GUI (unless already present in repo)
- Deep model/provider politics beyond safe, official auth flows
