# Project Map

This file documents the canonical repo layout and the runtime boundary.

## Canonical Repo Root
- /home/jannis/Schreibtisch/Work-OS/10_LTL_Core/12_Internal_Tools/12.06_Wanda_Agentic-System
- Symlink: /home/jannis/.wanda-system -> repo root

## Repo Scope (Tracked)
- bin/ (CLI entry points)
- config/ (templates and command files)
- docs/ (canonical documentation)
- prompts/ (canonical prompts)
- templates/ (prompt templates)
- scripts/ (install/update/diagnostics)
- skills/ (skill definitions)
- wanda_cloud/ (profiles)
- wanda-agents/ (agent snapshots)

## Runtime Scope (Not Tracked)
- ~/.config/opencode (primary config, plugins, SYSTEM.md)
- ~/.gemini (Gemini CLI context)
- ~/.claude (Claude context + skills)
- ~/.codex (Codex config + instructions)
- ~/.cache/opencode, ~/.local/share/opencode (runtime state/auth)
- ~/.wanda (runtime context.json)

## Required Repo Symlinks
Inside repo root:
- .opencode -> ~/.config/opencode
- .gemini -> ~/.gemini
- .wanda -> ~/.wanda

## Notes
- Runtime files are never committed.
- Canonical prompts live under prompts/ and templates/ and mirror to runtime.
