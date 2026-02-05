# Plugin Candidates (SSOT)

Last updated: 2026-02-05

Sources:
- OpenCode ecosystem list: https://opencode.ai/docs/ecosystem/
- awesome‑opencode list: https://github.com/awesome-opencode/awesome-opencode

Note:
- This file is the backlog of potential plugins to evaluate.
- Active/disabled runtime plugins live in `docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md`.

---

## A) Auth / Provider Plugins (ecosystem)

- opencode-openai-codex-auth — ChatGPT Plus/Pro subscription auth
  https://github.com/numman-ali/opencode-openai-codex-auth
- opencode-gemini-auth — Gemini plan auth
  https://github.com/jenslys/opencode-gemini-auth
- opencode-antigravity-auth — Antigravity free model auth (current in runtime)
  https://github.com/NoeFabris/opencode-antigravity-auth
- opencode-google-antigravity-auth — Google Antigravity OAuth + search support
  https://github.com/shekohex/opencode-google-antigravity-auth
- opencode-antigravity-multi-auth — Multi‑account rotation for Antigravity
  https://github.com/theblazehen/opencode-antigravity-multi-auth

Evaluation focus:
- Coverage across providers (Google, OpenAI, Anthropic, etc.)
- OAuth compliance and ToS risk
- Fallback behavior vs explicit routing

---

## B) Context / Token / Perf Plugins (ecosystem)

- opencode-dynamic-context-pruning — prune obsolete tool outputs
  https://github.com/Tarquinen/opencode-dynamic-context-pruning
- opencode-shell-strategy — non‑interactive shell strategy (disabled currently)
  https://github.com/JRedeker/opencode-shell-strategy
- opencode-md-table-formatter — cleanup markdown tables
  https://github.com/franlol/opencode-md-table-formatter/tree/main
- opencode-morph-fast-apply — faster edit apply
  https://github.com/JRedeker/opencode-morph-fast-apply
- opencode-type-inject — inject TS/Svelte types into reads
  https://github.com/nick-vi/opencode-type-inject
- opencode-context-analysis — token usage analysis (also in awesome list)
  https://github.com/IgorWarzocha/Opencode-Context-Analysis-Plugin

---

## C) Workflow / Orchestration Plugins (ecosystem)

- oh-my-opencode — agent harness (current in runtime)
  https://github.com/code-yeongyu/oh-my-opencode
- opencode-orchestrator — experimental autopilot (current in runtime)
  https://www.npmjs.com/package/opencode-orchestrator
- opencode-background-agents — async delegation
  https://github.com/kdcokenny/opencode-background-agents
- opencode-background — background process management (awesome list)
  https://github.com/zenobi-us/opencode-background
- opencode-workspace — bundled multi‑agent harness
  https://github.com/kdcokenny/opencode-workspace
- @openspoon/subtask2 — command orchestration extensions
  https://github.com/spoons-and-mirrors/subtask2
- @plannotator/opencode — interactive plan review
  https://github.com/backnotprop/plannotator/tree/main/apps/opencode-plugin

---

## D) Dev UX / Environment Plugins (ecosystem)

- opencode-devcontainers — devcontainer isolation
  https://github.com/athal7/opencode-devcontainers
- opencode-daytona — isolated Daytona sandboxes
  https://github.com/jamesmurdza/daytona/blob/main/guides/typescript/opencode/README.md
- opencode-pty — interactive PTY processes
  https://github.com/shekohex/opencode-pty.git
- opencode-worktree — git worktree automation
  https://github.com/kdcokenny/opencode-worktree
- opencode-zellij-namer — auto Zellij session naming
  https://github.com/24601/opencode-zellij-namer
- opencode-direnv — load direnv vars on session start (awesome list)
  https://github.com/simonwjackson/opencode-direnv
- opencode-canvas — interactive terminal canvases (awesome list)
  https://github.com/mailshieldai/opencode-canvas
- opencode-ignore — ignore files by pattern (awesome list)
  https://github.com/lgladysz/opencode-ignore

---

## E) Observability / Notifications (ecosystem)

- opencode-notifier — desktop notifications (disabled currently)
  https://github.com/mohak34/opencode-notifier
- opencode-notificator — notifications + sounds
  https://github.com/panta82/opencode-notificator
- opencode-notify — OS notifications
  https://github.com/kdcokenny/opencode-notify
- opencode-wakatime — usage tracking
  https://github.com/angristan/opencode-wakatime
- opencode-helicone-session — Helicone session headers
  https://github.com/H2Shami/opencode-helicone-session
- opencode-model-announcer — inject model name into context (awesome list)
  https://github.com/ramarivera/opencode-model-announcer

---

## F) Skills / Prompt Loading (ecosystem)

- opencode-skillful — lazy load prompts on demand
  https://github.com/zenobi-us/opencode-skillful
- opencode-agent-skills (JDT) — dynamic skills loader (awesome list)
  https://github.com/joshuadavidthomas/opencode-agent-skills
- opencode-agent-memory — persistent self‑editable memory blocks (awesome list)
  https://github.com/joshuadavidthomas/opencode-agent-memory

---

## G) Bundled / UI Projects (ecosystem)

- octto — interactive UI for brainstorming
  https://github.com/vtemian/octto
- opencode-workspace — bundled multi‑agent orchestration
  https://github.com/kdcokenny/opencode-workspace

## H) Clients / UI / Integrations (ecosystem)

- OpenWork — Open-source Claude Cowork alternative
  https://github.com/different-ai/openwork
- OpenChamber — Web/Desktop app + VS Code extension
  https://github.com/btriapitsyn/openchamber
- OpenCode-Obsidian — Obsidian integration
  https://github.com/mtymek/opencode-obsidian
- opencode.nvim (NickvanDyke) — Neovim frontend
  https://github.com/NickvanDyke/opencode.nvim
- opencode.nvim (sudo-tee) — Neovim frontend
  https://github.com/sudo-tee/opencode.nvim
- portal — mobile-first web UI over Tailscale/VPN
  https://github.com/hosenur/portal
- CodeNomad — desktop/web/mobile client
  https://github.com/NeuralNomadsAI/CodeNomad
- ocx — OpenCode extension manager
  https://github.com/kdcokenny/ocx
- opencode plugin template — plugin starter
  https://github.com/zenobi-us/opencode-plugin-template/

## I) Security / Safety Plugins (awesome list)

- envsitter-guard — prevent .env leaks
  https://github.com/boxpositron/envsitter-guard
- claude-code-safety-net — block destructive commands
  https://github.com/kenryu42/claude-code-safety-net
- opencode-froggy — hooks + specialized agents
  https://github.com/smartfrog/opencode-froggy
- opencode-beads — beads issue tracker integration
  https://github.com/joshuadavidthomas/opencode-beads

---

## J) Items already integrated (do not duplicate)

- oh-my-opencode (agent harness)
- opencode-websearch-cited (websearch)
- opencode-supermemory (memory)
- opencode-scheduler (jobs)
- opencode-antigravity-auth (auth)

Reference: `docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md`

---

## K) Notes

- Sources include OpenCode ecosystem and awesome‑opencode; overlap is expected.
- Use this file for evaluation shortlists; install only after validation.
