# WANDA System State (Canonical)

Last updated: 2026-02-04

This document captures the current canonical layout, configuration sources,
plugins, MCP servers, and known issues. It is based on local files only.

## Canonical Paths (Single Source of Truth)

- Project root (canonical):
  - /home/jannis/Schreibtisch/Work-OS/10_LTL_Core/12_Internal_Tools/12.06_Wanda_Agentic-System

- System alias (symlink):
  - /home/jannis/.wanda-system -> /home/jannis/Schreibtisch/Work-OS/10_LTL_Core/12_Internal_Tools/12.06_Wanda_Agentic-System

- Home runtime context:
  - /home/jannis/.wanda (context.json)

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

Plugins configured in opencode.json:
- opencode-antigravity-auth@1.4.3
- opencode-antigravity-quota@latest
- opencode-knowledge@latest
- opencode-supermemory@latest
- opencode-scheduler@latest
- opencode-agent-skills@latest
- opencode-handoff@latest
- opencode-orchestrator@latest
- oh-my-opencode@latest
- micode@latest
- @cgasgarth/opencode-for-rust@latest

Note on plugin tools:
- The tool surface depends on each plugin version and is not fully visible
  in this repo. Use plugin docs or runtime tool listing to confirm.
- Known command entry present locally: command/antigravity-quota.md

## MCP Servers (Configured)

From opencode.json:
- MCP_DOCKER (local, docker mcp gateway)
- hostinger-web (local, hostinger-api-mcp)
- hostinger-vps (local, hostinger-api-mcp)

From SYSTEM.md (WANDA kernel reference list):
- brave, filesystem, memory, sequential-thinking, github, stripe,
  n8n-pro, supabase, vercel, postgres, docker, playwright, firecrawl, context7, git

Important:
- API tokens for Hostinger MCPs are embedded in opencode.json.
  Treat as secrets, do not commit or share.

## Agents and Categories

From oh-my-opencode.json:

Agents:
- sisyphus
- oracle
- librarian
- explore
- multimodal-looker
- prometheus
- metis
- momus
- atlas

Categories:
- visual-engineering
- ultrabrain
- deep
- artistry
- quick
- unspecified-low
- unspecified-high
- writing

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
