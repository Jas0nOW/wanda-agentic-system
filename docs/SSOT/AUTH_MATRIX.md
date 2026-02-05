# Auth / Provider Matrix (SSOT)

Last updated: 2026-02-05

Purpose: track available auth plugins, provider coverage, and open questions.
Sources:
- OpenCode ecosystem list: https://opencode.ai/docs/ecosystem/
- awesome‑opencode list: https://github.com/awesome-opencode/awesome-opencode

---

## A) Auth Plugins (Known)

### 1) Antigravity Auth (active)
- Plugin: opencode-antigravity-auth
- Purpose: Use Google Antigravity IDE auth to access Gemini + Anthropic models
- URL: https://github.com/NoeFabris/opencode-antigravity-auth
- Status: Active in runtime (see `docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md`)

### 2) Antigravity Multi-Auth
- Plugin: opencode-antigravity-multi-auth
- Purpose: Multiple Google accounts with rotation
- URL: https://github.com/theblazehen/opencode-antigravity-multi-auth
- Status: Candidate (not installed)

### 3) Google Antigravity Auth (alt)
- Plugin: opencode-google-antigravity-auth
- Purpose: Google Antigravity OAuth + search support
- URL: https://github.com/shekohex/opencode-google-antigravity-auth
- Status: Candidate (not installed)

### 4) Gemini Auth
- Plugin: opencode-gemini-auth
- Purpose: Use Google account/Gemini plan
- URL: https://github.com/jenslys/opencode-gemini-auth
- Status: Candidate (not installed)

### 5) OpenAI Codex Auth
- Plugin: opencode-openai-codex-auth
- Purpose: ChatGPT Plus/Pro OAuth for Codex backend
- URL: https://github.com/numman-ali/opencode-openai-codex-auth
- Status: Candidate (not installed)

---

## B) Decision Questions (Open)

- Which auth path is primary for Google models? (Antigravity vs Gemini Auth)
- Do we want multi-account rotation for rate limits?
- Are there ToS/OAuth constraints we must avoid?

---

## C) Next Validation Steps

1) Define provider coverage target (Gemini, Anthropic, OpenAI).
2) Test each auth plugin in isolation with a single model.
3) Record error modes and fallback behavior.
4) Pick primary + fallback strategy and document in SSOT.
