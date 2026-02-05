# Install Boundary

This document defines the repo vs runtime boundary for WANDA.

## Repo Scope (Tracked)
- Source, prompts, docs, templates, scripts, and configuration templates.
- Canonical prompt sources under prompts/ and templates/.

## Runtime Scope (Not Tracked)
- User configs and secrets live in home directories.
- Runtime state, caches, and auth are home-scoped.

## Canonical Paths
- Repo root: /home/jannis/Schreibtisch/Work-OS/10_LTL_Core/12_Internal_Tools/12.06_Wanda_Agentic-System
- Alias: /home/jannis/.wanda-system -> repo root

## Required Repo Symlinks
Inside repo root:
- .opencode -> ~/.config/opencode
- .gemini -> ~/.gemini
- .wanda -> ~/.wanda

## Rules
- Never commit runtime files or secrets.
- Keep canonical prompts in-repo and mirror to runtime as needed.
- Archive instead of delete for documentation cleanup.

## References
- docs/WANDA_SYSTEM_STATE.md
- docs/INSTALLATION.md
- docs/architecture/prompt-governance.md
