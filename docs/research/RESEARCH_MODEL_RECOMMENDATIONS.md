# Model Recommendations Research (WANDA)

Last updated: 2026-02-05

Purpose: Document the rationale and process for selecting "best" models per agent, with provider coverage and validation steps. This doc informs the installer and defaults.

Sources:
- Agent roster: prompts/context/AGENT_REGISTRY.md
- Runtime models: ~/.config/opencode/opencode.json
- Providers list: https://opencode.ai/docs/providers/
- Auth plugins: docs/SSOT/AUTH_MATRIX.md
- LSP context: docs/SSOT/LSP_INVENTORY.md

---

## 1) Available Models (Current Runtime)

From `~/.config/opencode/opencode.json`:
- Gemini 3 Flash (Antigravity)
- Gemini 3 Pro (Antigravity)
- Claude Sonnet 4.5 (Antigravity)
- Claude Opus 4.5 Thinking (Antigravity)

---

## 2) Selection Criteria (What "Best" Means)

We define "best" per agent as a weighted combination:
- Accuracy (task success rate)
- Reasoning depth (complexity handling)
- Latency (interaction speed)
- Cost (token + provider pricing)
- Tool reliability (MCP/LSP integration stability)
- Safety and compliance (provider ToS, auth limits)

Each agent has different weightings:
- Orchestrator: latency > accuracy
- Architect/Audit: reasoning > latency
- UI/UX: creativity + visual reasoning
- Research agents: retrieval reliability + speed

---

## 3) Provider Coverage (Optional via /connect)

OpenCode supports 75+ providers. We only enable providers we can authenticate and verify.
- Use `/connect` to add a provider and `/models` to validate.
- Credentials stored in `~/.local/share/opencode/auth.json`.

Provider selection must be recorded in:
- docs/SSOT/AUTH_MATRIX.md
- docs/SSOT/MODEL_ASSIGNMENT_MATRIX.md

---

## 4) Draft Recommendations (Defaults)

Primary/Fallback mapping is in:
- docs/SSOT/MODEL_ASSIGNMENT_MATRIX.md

This doc focuses on *how* to validate those picks.

---

## 5) Validation Plan (Trust but Verify)

### A) Per‑Agent Bench
- Choose 2–3 representative tasks per agent.
- Run each task on primary + fallback model.
- Record success rate, time, and qualitative score.

### B) Stability Checks
- MCP tool call success rate per model
- LSP diagnostics consistency
- Context window behavior under long prompts

### C) Cost/Latency Sampling
- 3–5 sample runs each
- Measure average latency per response
- Estimate cost per 1k/10k tokens (if provider pricing available)

Results are stored in:
- docs/research/RESEARCH_MODEL_RECOMMENDATIONS.md (this file)
- docs/SSOT/MODEL_ASSIGNMENT_MATRIX.md (updated mapping)

---

## 6) Open Questions

- Which provider is primary for GPT‑5.2 access?
- Is Antigravity auth the default or just fallback for free routing?
- Should any agents be pinned to local Ollama models for offline mode?

---

## 7) Installer Implications

Installer should:
- Detect available providers
- Offer the recommended default mapping
- Allow per‑agent overrides
- Provide rollback to defaults

Reference installer flow:
- docs/SSOT/INSTALLER_FLOW_SPEC.md
