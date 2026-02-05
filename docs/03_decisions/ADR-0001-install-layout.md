# ADR-0001: Install Layout and Runtime Boundary

Date: 2026-02-04
Status: Accepted

## Context
Multiple repo clones and mixed runtime locations caused drift. The system
needs a single canonical repo root, a stable alias, and strict separation
between repo-tracked files and runtime configuration/secrets.

## Decision
- Canonical repo root remains in Work-OS and is referenced via ~/.wanda-system.
- Runtime configs and state live in home-scoped XDG locations.
- Required symlinks inside repo root map runtime paths for convenience.
- Documentation cleanup uses archive-first (no deletions).

## Consequences
- Repo stays clean and portable.
- Runtime files and secrets are never committed.
- Cleanup is reversible via archive mappings.

## References
- docs/WANDA_SYSTEM_STATE.md
- docs/INSTALLATION.md
- docs/architecture/prompt-governance.md
