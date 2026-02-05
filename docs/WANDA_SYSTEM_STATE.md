# WANDA System State (Canonical)

Last updated: 2026-02-05

This document captures the current canonical layout, configuration sources,
plugins, MCP servers, and known issues. It is based on local files only.

## Canonical Paths (Single Source of Truth)

- Project root (canonical):
  - /home/jannis/Schreibtisch/Work-OS/10_LTL_Core/12_Internal_Tools/12.06_Wanda_Agentic-System

- System alias (symlink):
  - /home/jannis/.wanda-system -> /home/jannis/Schreibtisch/Work-OS/10_LTL_Core/12_Internal_Tools/12.06_Wanda_Agentic-System

- Home runtime context:
  - /home/jannis/.wanda (context.json)

## Lokale Ordnerrollen (Runtime)

- `.opencode`: entsteht durch OpenCode-Installation; Settings liegen in `~/.config/opencode`.
- `.gemini`: Gemini CLI System mit System Prompt, Context-Dateien und CLI-spezifischer Erweiterung.
- `.codex` und `.claude`: enthalten Context + Systemprompt (je 2 MD-Dateien werden bei Installation getauscht).

## WANDA Doppel-System (CLI)

1) **Wanda Code System**
   - Terminal: `wanda code`
   - Startet optimiertes OpenCode mit Settings, Plugins und Prompts.

2) **Wanda Voice System**
   - Terminal: `wanda voice`
   - Voice System mit modernen Edge Stimmen.
   - Zwei Run-Modes:
     - Mit Ollama (laufend als Prompt-Verbesserer)
     - Ohne Ollama (einfaches TTS/STT fuer Nutzer ohne Ollama)

3) **Wanda (global)**
   - Terminal: `wanda`
   - Startet beide Systeme zusammen.

## Update-System

- Wanda hat ein Update-System, das auf das GitHub-Repo zeigt.

## Required Symlinks

Inside the canonical repo root:

- .opencode -> /home/jannis/.config/opencode
- .gemini -> /home/jannis/.gemini
- .wanda -> /home/jannis/.wanda

These keep the repo clean while using the standard config locations.

## Opencode Configuration (Source of Truth)

Location:
- /home/jannis/.config/opencode

Key files:
- opencode.json
- oh-my-opencode.json
- SYSTEM.md
- command/antigravity-quota.md

Repo mirrors:
- docs/architecture/opencode-system-kernel.md
- config/command/antigravity-quota.md

Plugins configured in opencode.json (runtime):
- oh-my-opencode@3.2.3
- opencode-orchestrator@latest
- opencode-antigravity-auth@1.4.3
- opencode-antigravity-quota@latest
- opencode-handoff@latest
- opencode-scheduler@latest
- opencode-websearch-cited@latest
- opencode-knowledge@latest
- opencode-supermemory@latest
- opencode-agent-skills@latest

SSOT reference:
- docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md

Disabled plugins (known):
- opencode-context-analysis@latest
- opencode-shell-strategy@latest
- opencode-notifier@latest

Investigation:
- micode@latest (Anthropic credential errors suspected)

Note on plugin tools:
- The tool surface depends on each plugin version and is not fully visible
  in this repo. Use plugin docs or runtime tool listing to confirm.
- Known command entry present locally: command/antigravity-quota.md

## MCP Servers (Configured)

From opencode.json (runtime MCPs):
- MCP_DOCKER (Docker MCP Gateway hub)
- hostinger-web (Hostinger account A)
- hostinger-vps (Hostinger account B)

From Docker MCP registry (available servers):
- brave, context7, docker, filesystem, firecrawl, git, github, github-official,
  hostinger-mcp-server, memory, n8n, n8n-instance, playwright, postgres,
  sequentialthinking, stripe, supabase, supermemory, vercel

Important:
- Hostinger MCPs are separate accounts by design.
- API tokens for Hostinger MCPs are embedded in local opencode.json.
  Treat as secrets, do not commit or share.
- Oh‑My‑OpenCode default MCPs: context7, grep_app, websearch.

## Agents and Categories

From oh-my-opencode.json:

Agents:
- sisyphus
- oracle
- librarian
- explore
- multimodal-looker
- architect
- metis
- momus
- software-engineer

Categories:
- visual-engineering
- ultrabrain
- deep
- artistry
- quick
- unspecified-low
- unspecified-high
- writing

## LSP Servers

SSOT reference:
- docs/SSOT/LSP_INVENTORY.md

## Model Assignments

SSOT reference:
- docs/SSOT/MODEL_ASSIGNMENT_MATRIX.md

## Installer Flow

SSOT reference:
- docs/SSOT/INSTALLER_FLOW_SPEC.md

## Installer Notes (macOS)

Known issue:
- opencode binary may fail with "Killed: 9" on macOS due to quarantine.

Mitigations used in installer:
- Install opencode via curl first
- Remove quarantine via xattr for all discovered binaries

## Performance and Speed Notes

- Prefer gemini-3-flash / low-thinking variants for quick or exploratory tasks.
- Use parallel tool calls for independent steps; avoid sequential scans.
- Cache heavy MCP calls where possible; re-validate only when configs change.

## Known Problems and Watchouts

- Quarantine on macOS can break opencode after reinstall.
- Multiple repo clones caused drift; canonical root is now fixed.
- Plugin tooling is volatile; re-validate after updates.
- Secrets are currently in opencode.json; move to env-based configuration
  if possible.
- Voice transcription sometimes produces gibberish (STT quality/latency).
- Slow model responses when using heavy reasoning tiers.
- Context pruning is not enforced consistently across tools.
- MCP/Docker install validation can be flaky; rerun gateway checks.
- Plugin conflicts observed between orchestrators (oh-my-opencode vs opencode-orchestrator).

## Archives

Legacy content moved to:
- /home/jannis/Schreibtisch/Work-OS/10_LTL_Core/12_Internal_Tools/12.06_Wanda_Agentic-System/archive/

## TODO (Operational)

- Confirm plugin tool lists via plugin docs or runtime tool listing.
- Optional: externalize MCP API tokens into env.
