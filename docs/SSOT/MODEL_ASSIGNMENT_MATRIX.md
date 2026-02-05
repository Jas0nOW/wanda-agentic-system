# Model Assignment Matrix (SSOT)

Last updated: 2026-02-05

Purpose: recommended model mapping per WANDA agent/subagent, with provider options and fallbacks.

Sources:
- Agent roster: prompts/context/AGENT_REGISTRY.md
- Runtime models (current): ~/.config/opencode/opencode.json
- OpenCode providers: https://opencode.ai/docs/providers/
- Auth plugins: docs/SSOT/AUTH_MATRIX.md
- Local voice gateway: prompts/system/OLLAMA_SYSTEM.md

---

## 1) Available Now (Runtime)

From `~/.config/opencode/opencode.json`:
- Gemini 3 Flash (Antigravity)
- Gemini 3 Pro (Antigravity)
- Claude Sonnet 4.5 (Antigravity)
- Claude Opus 4.5 Thinking (Antigravity)

Note:
- OpenCode supports 75+ providers and local models via `/connect`, but only the above are currently configured. See https://opencode.ai/docs/providers/

---

## 2) Provider Options (Optional)

Provider auth plugins (see docs/SSOT/AUTH_MATRIX.md):
- opencode-antigravity-auth (current)
- opencode-antigravity-multi-auth
- opencode-google-antigravity-auth
- opencode-gemini-auth
- opencode-openai-codex-auth

OpenCode provider connection:
- `/connect` writes credentials to `~/.local/share/opencode/auth.json` (per providers doc).

---

## 3) Local Models (Voice Gateway)

Local voice middleware uses Ollama (see prompts/system/OLLAMA_SYSTEM.md):
- Primary local model: brainstorm-36b (Ollama)
- Responsibilities: prompt refinement, routing, safety checks, context brief

Installer default pulls (from docs/INSTALLATION.md):
- brainstorm-36b (voice gateway)
- neo-20b (code completion)
- heretic-12b (fallback)
- qwen3:8b (lightweight)

---

## 4) Model Mapping (Recommended Defaults)

Legend:
- Primary: preferred default model
- Fallback: lighter/cheaper option
- Optional: provider-dependent alternatives

| Agent | Primary (available now) | Fallback (available now) | Optional alternatives | Rationale |
| --- | --- | --- | --- | --- |
| Brainstormer | Gemini 3 Pro | Gemini 3 Flash | GPT‑5.2 (if OpenAI added) | Ideation and creative exploration |
| Sisyphus (Orchestrator) | Gemini 3 Flash | Gemini 3 Pro | GPT‑5.2 (routing quality) | Fast routing and task dispatch |
| Architect | Claude Opus 4.5 Thinking | Claude Sonnet 4.5 | GPT‑5.2 (deep planning) | Deep reasoning + architecture |
| Software‑Engineer | Claude Sonnet 4.5 | Gemini 3 Pro | GPT‑5.2 (code) | Implementation accuracy |
| Frontend‑UI‑UX | Gemini 3 Pro | Gemini 3 Flash | GPT‑5.2 (design prompt) | Creative + layout |
| Audit | Claude Opus 4.5 Thinking | Claude Sonnet 4.5 | GPT‑5.2 (security) | Deep analysis and verification |
| Oracle | Gemini 3 Pro | Gemini 3 Flash | GPT‑5.2 (research synthesis) | Research and synthesis |
| Writer | Gemini 3 Pro | Gemini 3 Flash | GPT‑5.2 (long‑form docs) | Documentation clarity |
| Librarian | Gemini 3 Flash | Gemini 3 Pro | GPT‑5.2 (knowledge mgmt) | Fast retrieval and cataloging |
| Explore | Gemini 3 Flash | Gemini 3 Pro | GPT‑5.2 (complex search) | Quick codebase navigation |
| Multimodal‑Looker | Gemini 3 Pro | Gemini 3 Flash | GPT‑5.2 (vision) | Image/visual analysis |
| Codebase‑Locator | Gemini 3 Flash | Gemini 3 Pro | GPT‑5.2 | Fast search tasks |
| Codebase‑Analyzer | Gemini 3 Flash | Gemini 3 Pro | GPT‑5.2 | Structural analysis (read‑only) |
| Pattern‑Finder | Gemini 3 Flash | Gemini 3 Pro | GPT‑5.2 | Pattern detection (read‑only) |
| Ledger‑Creator | Gemini 3 Flash | Gemini 3 Pro | GPT‑5.2 | Session summaries |
| Artifact‑Searcher | Gemini 3 Flash | Gemini 3 Pro | GPT‑5.2 | Retrieval and restoration |
| Metis | Claude Opus 4.5 Thinking | Claude Sonnet 4.5 | GPT‑5.2 | Pre‑planning and risk analysis |
| Momus | Claude Opus 4.5 Thinking | Claude Sonnet 4.5 | GPT‑5.2 | Plan review and critique |

---

## 5) Routing Notes (Voice Gateway)

The local gateway (Ollama) should route requests by intent:
- code/build/fix -> OpenCode
- plan/analyze -> Claude (Opus/Sonnet)
- search/visual/creative -> Gemini
- shell commands -> terminal (with safety checks)

Source: prompts/system/OLLAMA_SYSTEM.md

---

## 6) Open Questions

- Which optional provider should be primary for GPT‑5.2 access (OpenAI vs other gateway)?
- Do we want multi‑account rotation for Antigravity (rate‑limit mitigation)?
- Should any agent be pinned to a local Ollama model for offline mode?

---

## 7) Change Control

Any changes must be reflected in:
- prompts/context/AGENT_REGISTRY.md (agent roster)
- docs/SSOT/AUTH_MATRIX.md (provider choices)
- install.sh (default selections)
