# WANDA Contributing Guidelines & Rules of Engagement

> **Status:** Active Policy
> **Enforcement:** Mandatory for all Agents (Core & Specialist) and Human Operators.

## 1. The Patch Protocol

All code modifications must adhere to the **Patch Protocol** to ensure stability and reproducibility.

### 1.1 Scope Guards
*   **Web Tasks:** Changes allowed only in `src/`, `app/`, `components/`, `public/`.
*   **n8n Tasks:** Changes allowed only in `workflow.json` and test payloads.
*   **Ops Tasks:** Changes allowed only in deployment scripts and specs.
*   **Forbidden:** 
    *   No secrets in any committed file (use `.env` or Vault).
    *   No new dependencies without `Context7` verification or explicit approval.

### 1.2 The Fix-Loop Limit
*   **Max Iterations:** 3 per gate failure.
*   **Failure Procedure:** If a build/test fails 3 times in a row, the Agent **MUST** stop and write a `ROOT_CAUSE.md` file instead of trying blindly again.
*   **Minimal Diff:** Prefer the smallest change that fixes the error.

---

## 2. Contract-First Workflow

No implementation starts without a Spec.

1.  **Read/Create Spec:** `UI_SPEC.yml`, `N8N_SPEC.yml`, or `OPS_SPEC.yml`.
2.  **Validate Spec:** Ensure it matches the user prompt and system constraints.
3.  **Implement:** Code against the Spec, not the Prompt.

---

## 3. Security Standards

### 3.1 Secrets Hygiene
*   **Never commit secrets.**
*   **n8n:** Use Credentials placeholders (e.g., `{{ $credentials.slackToken }}`) instead of hardcoded strings.
*   **Logs:** All output logs must be redacted (no Bearer tokens, no API keys).

### 3.2 Tool Safety
*   **Exec:** Shell execution is restricted to the specific Runner environment.
*   **Web Fetch:** Only allow-listed domains for external resources.

---

## 4. Documentation Standards

*   **Update Docs:** If you change the architecture, update `ARCHITECTURE.md`.
*   **Update Agents:** If you change an Agent's role, update `../wanda-architecture-agents.md`.
*   **Single Source of Truth:** Do not duplicate information. Reference existing files.

---

## 5. Agent Search Tips (Fetch-Tipps)

For Agents needing to retrieve external docs, use these verified entry points:

```
# OpenCode Docs
WebFetch: https://opencode.ai/docs/providers/

# Antigravity Plugin README
WebFetch: https://github.com/NoeFabris/opencode-antigravity-auth

# Oh-My-OpenCode Installation & Docs
WebFetch: https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/guide/installation.md

# V0 Docs
WebFetch: https://v0.app/docs
```
