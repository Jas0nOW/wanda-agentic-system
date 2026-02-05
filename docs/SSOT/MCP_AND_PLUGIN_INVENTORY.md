# MCP + Plugin Inventory (SSOT)

Last updated: 2026-02-05

This is the single source of truth for:
- OpenCode plugins (runtime)
- OpenCode MCP configuration
- Docker MCP registry (available servers)
- Oh‑My‑OpenCode default MCPs

Sources:
- Runtime OpenCode config: `~/.config/opencode/opencode.json`
- Docker MCP registry: `~/.docker/mcp/registry.yaml`
- Docker MCP config: `~/.docker/mcp/config.yaml`
- Oh‑My‑OpenCode defaults (mcps): context7, grep_app, websearch

---

## A) OpenCode Plugins (runtime)
Source: `~/.config/opencode/opencode.json`

Installed plugins:
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

Note:
- The template `config/opencode.json.template` may include additional plugins not in runtime.
- If a plugin is removed due to errors, it should be documented here and in `docs/WANDA_SYSTEM_STATE.md`.

Runtime count: 10

### Disabled / Removed (known)
Source: `docs/save/Notizen.md`

- opencode-context-analysis@latest (disabled due to BunInstallFailedError risk)
- opencode-shell-strategy@latest (disabled due to BunInstallFailedError risk)
- opencode-notifier@latest (disabled due to BunInstallFailedError risk)

Disabled count: 3

### Degraded / Investigation
Source: `docs/save/Notizen.md`

- micode@latest (Anthropic credential errors suspected; kept optional)

### Optional / Experimental
- opencode-orchestrator@latest (kept as experimental in runtime)

Total inventory (runtime + disabled + optional/degraded): 14

Candidate backlog:
- docs/SSOT/PLUGIN_CANDIDATES.md

---

## B) OpenCode MCP Configuration (runtime)
Source: `~/.config/opencode/opencode.json`

Configured MCPs:
- MCP_DOCKER (Docker MCP Gateway hub)
- hostinger-web (Hostinger account A)
- hostinger-vps (Hostinger account B)

Note:
- Hostinger MCPs are separate accounts by design.
- Tokens live in local config only; never commit.

---

## C) Docker MCP Registry (available servers)
Source: `~/.docker/mcp/registry.yaml`

Registry servers (19):
- brave
- context7
- docker
- filesystem
- firecrawl
- git
- github
- github-official
- hostinger-mcp-server
- memory
- n8n
- n8n-instance
- playwright
- postgres
- sequentialthinking
- stripe
- supabase
- supermemory
- vercel

Notes:
- Naming is registry‑key based (example: `sequentialthinking` without dash).
- Active/available servers depend on Docker MCP gateway runtime and secrets.

---

## D) Docker MCP Config (active settings)
Source: `~/.docker/mcp/config.yaml`

Configured paths:
- filesystem: /home/jannis
- git: /home/jannis
- n8n: api_url set

---

## E) Oh‑My‑OpenCode Default MCPs
Oh‑My‑OpenCode enables these MCPs by default unless disabled:
- context7
- grep_app
- websearch

These are OpenCode MCPs (not Docker MCP registry entries).

---

## Update Rules
- Update this file whenever `opencode.json` or the Docker MCP registry changes.
- Prefer factual lists over counts to avoid drift.
- If counts are used elsewhere, reference this file for the current number.
