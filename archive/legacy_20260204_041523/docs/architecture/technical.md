# WANDA System Architecture

> **Blueprint:** v3.0 (Universal Builder + Voice Gateway)
> **Core Principle:** Deterministische Pipelines ("Skills") statt freier Prompts.

---

## 1. System High-Level Map

```text
[ VOICE / CHAT INGRESS ]       [ TERMINAL CONTROL ]
        │                               │
        ▼                               ▼
[ MOLTBOT GATEWAY ] <---------> [ OPENCODE CORE ]
(Auth, Routing, Policy)         (Orchestrator, Runners)
        │                               │
        └─────── [ SKILL REGISTRY ] ────┘
                 ├── v0_web
                 ├── v0_n8n
                 └── v0_ops
```

---

## 2. Skill Platform Architecture (The "v0" Engine)

The system operates via **Skills**. Each Skill is a strictly defined pipeline.

### 2.1 Directory Structure (`.v0/`)
*   `contracts/`: Schemas & Templates.
*   `specs/`: Active specifications (`UI_SPEC.yml`).
*   `runs/`: Execution logs and runner outputs.
*   `exports/`: Final artifacts (patches, zips).

### 2.2 Spec Templates (Reference)

#### UI_SPEC.yml (Web Builder)
```yaml
schema_version: 1
profile: web-mvp
stack:
  framework: "nextjs"
  styling: "tailwind"
  ui_library: "shadcn-ui"
constraints:
  allowed_libs: ["react", "next", "lucide-react"]
  forbidden: ["auth/db unless requested"]
routes:
  - path: "/"
    components:
      - name: "Hero"
dod:
  build: ["pnpm lint passes", "pnpm build passes"]
```

#### N8N_SPEC.yml (Workflow Builder)
```yaml
schema_version: 1
profile: n8n-prod
requirements:
  triggers:
    - type: "webhook"
      method: "POST"
design:
  node_source_of_truth: "n8n-mcp"
  error_strategy: { continue_on_fail: false }
credentials:
  policy: ["NO secrets embedded", "use n8n Credentials placeholders"]
dod:
  smoke_test: ["trigger endpoint returns 200"]
```

---

## 3. Voice & Chat Gateway (Moltbot)

The interface layer connecting messaging/voice to the internal runners.

### 3.1 Components
*   **Gateway Daemon:** Moltbot running locally.
*   **Channels:** WhatsApp (Chat), Twilio/Telnyx (Voice).
*   **Bridge Tool:** `v0_bridge` connects Moltbot to OpenCode.

### 3.2 Data Flow
1.  **Ingress:** Message/Voice received.
2.  **Auth:** Allowlist check (`dmPolicy`, `inboundPolicy`).
3.  **Routing:**
    *   *Chat:* Parsed to `CHAT_TOOL_SPEC`.
    *   *Voice:* Parsed to `VOICE_TOOL_SPEC` (default: notify mode).
4.  **Execution:** `v0_bridge` triggers OpenCode Runner via Queue/File.
5.  **Response:** Async notification sent back to origin channel.

### 3.3 Security Configuration (Reference)
*   **Gateway Auth:** Token required for non-loopback.
*   **Logging:** File logs (redacted), Session transcripts (protected).
*   **Approvals:** High-risk actions (Deploy/Exec) require explicit confirmation ("JA, AUSFÜHREN").

---

## 4. Runner Architecture

The execution engine managed by OpenCode/Commander.

1.  **Reader:** Reads `SPEC` + `Prompt`.
2.  **Generator:** Writes Code/JSON.
3.  **Runner Script:** Executes `lint`, `build`, or `deploy`.
4.  **Gate:** Checks Exit Code.
    *   *Pass:* Export.
    *   *Fail:* Loop back to Generator (max 3x) with Error Log.

---

## 5. Memory Architecture

*   **Graph (MCP):** Persistent entities (Projects, Stacks, Decisions).
*   **Ledger (File):** Session continuity (`thoughts/ledgers/`).
*   **Cloud (Supermemory):** Long-term facts.
