# QUELLEN_GESAMT_CHAT_PLUS_DEEPRESEARCH.md
Stand: 2026-01-29
Scope: (A) Chat-Quellen + (B) “Quellen gescannt”-Liste (Moltbot/Voice/OpenCode/n8n/MCP/Context7/CLI Tools/v0/10web/Supply-Chain) + (C) zusätzliche SOTA-Prompting-Quellen, die im Wanda-Prompt zitiert wurden.

> Hinweis (Wichtig):
> Diese Liste ist “maximal vollständig nach aktuellem Input”.
> 100%-Garantie “nichts ausgelassen” ist erst möglich, wenn du mir zusätzlich
> 1) DEEP_RESEARCH_1.md + DEEP_RESEARCH_2.md (vollständig) gibst ODER
> 2) die DeepResearch “Sources/References” Exportliste.
> Dann kann ich eine finale “Source-of-Truth” Liste per Diff erzeugen.

---

## 1) Moltbot / ehem. Clawdbot (Hauptquellen + zentrale Unterseiten)

### Haupt-Domain / Docs-Index
- Moltbot Docs (Root): https://docs.molt.bot/
- Clawd Docs (Root): https://docs.clawd.bot/
- Projekt-Seite: https://clawd.bot/
- Business Insider (Rebrand / Hintergrund): https://www.businessinsider.com/clawdbot-moltbot-creator-anthropic-nice-name-change-2026-1?utm_source=chatgpt.com
- The Verge (Rebrand / Sicherheitskontext): https://www.theverge.com/report/869004/moltbot-clawdbot-local-ai-agent

### Channels / Routing / Automation
- WhatsApp Channel: https://docs.molt.bot/channels/whatsapp
- Channel Routing (Sessions): https://docs.molt.bot/concepts/channel-routing
- Webhook Automation: https://docs.molt.bot/automation/webhook

### Plugins / Tools / Execution
- Plugin Basics: https://docs.molt.bot/plugin
- Agent Tools Plugin: https://docs.molt.bot/plugins/agent-tools
- Voice Call Plugin: https://docs.molt.bot/plugins/voice-call
- Tools Invoke HTTP API: https://docs.molt.bot/gateway/tools-invoke-http-api
- Multi-Agent Sandbox & Tools: https://docs.molt.bot/multi-agent-sandbox-tools

### Governance / Cost / Logs / Approvals / Security
- Token Use / Cost: https://docs.molt.bot/token-use
- Logging: https://docs.molt.bot/gateway/logging
- Approvals (CLI): https://docs.molt.bot/cli/approvals
- (Zusätzliche Moltbot Kernseiten aus Scan)
  - Sandboxing: https://docs.molt.bot/gateway/sandboxing
  - Security: https://docs.molt.bot/gateway/security

### Repos (Hauptrepos / Org)
- Moltbot Org (Repo-Übersicht): https://github.com/moltbot
- clawd.bot Repo (aus Scan erwähnt): https://github.com/moltbot/clawd.bot
- Awesome Moltbot Skills (Skill-Sammlung): https://github.com/VoltAgent/awesome-moltbot-skills

---

## 2) Voice Provider Docs (Twilio / Telnyx) – Signatures, Webhooks, Streaming

### Twilio (Hauptseiten)
- Webhooks Security (X-Twilio-Signature): https://www.twilio.com/docs/usage/webhooks/webhooks-security?utm_source=chatgpt.com
- Security: https://www.twilio.com/docs/usage/security?utm_source=chatgpt.com
- Voice Media Streams: https://www.twilio.com/docs/voice/media-streams?utm_source=chatgpt.com
- Media Streams Firewall/Config: https://www.twilio.com/docs/global-infrastructure/firewall-configurations/media-streams-configuration?utm_source=chatgpt.com

### Telnyx (Hauptseiten)
- Voice API Webhooks (Signatures): https://developers.telnyx.com/docs/voice/programmable-voice/voice-api-webhooks?utm_source=chatgpt.com
- Media Streaming (WebSockets): https://developers.telnyx.com/docs/voice/programmable-voice/media-streaming?utm_source=chatgpt.com
- Voice API Commands & Resources: https://developers.telnyx.com/docs/voice/programmable-voice/voice-api-commands-and-resources?utm_source=chatgpt.com
- Telnyx Help (Webhooks): https://support.telnyx.com/en/articles/4334722-how-to-leverage-webhooks

### Telnyx Demos (Repo, aus Scan)
- Telnyx dual-provider demo (Android): https://github.com/team-telnyx/telnyx-voice-demo-android
- Call control IVR example: https://github.com/team-telnyx/call-control-ivr-example

---

## 3) OpenCode (Docs + Hauptrepo + relevante Ecosystem-Themen)

### OpenCode Docs (Haupt)
- Agents: https://opencode.ai/docs/agents/
- Config: https://opencode.ai/docs/config/
- MCP servers: https://opencode.ai/docs/mcp-servers/
- Server: https://opencode.ai/docs/server/
- Ecosystem: https://opencode.ai/docs/ecosystem/

### OpenCode Repo
- opencode-ai/opencode (Hauptrepo): https://github.com/opencode-ai/opencode
- Releases (Haupt): https://github.com/opencode-ai/opencode/releases

### Dynamic Context Pruning (Token-Effizienz)
- DCP Repo: https://github.com/Opencode-DCP/opencode-dynamic-context-pruning
- DCP README: https://github.com/Opencode-DCP/opencode-dynamic-context-pruning/blob/master/README.md

### Antigravity / OAuth Plugins (aus Scan erwähnt)
- opencode-antigravity-auth: https://github.com/NoeFabris/opencode-antigravity-auth
- Releases: https://github.com/NoeFabris/opencode-antigravity-auth/releases
- opencode-openai-codex-auth: https://github.com/numman-ali/opencode-openai-codex-auth

---

## 4) Oh My OpenCode (Docs + Repo)

- Features: https://ohmyopencode.com/features/
- Docs Root: https://ohmyopencode.com/documentation/
- Repo (Release erwähnt): https://github.com/code-yeongyu/oh-my-opencode

---

## 5) n8n (Offizielle Docs + MCP + API)

### n8n Docs (Haupt)
- n8n Docs Root: https://docs.n8n.io/
- API reference / Public REST API: https://docs.n8n.io/api/
- API Authentication (X-N8N-API-KEY): https://docs.n8n.io/api/authentication/
- Export/Import Workflows: https://docs.n8n.io/workflows/export-import/
- Executions (Konzept/Details): https://docs.n8n.io/workflows/executions/
- Environment variables: https://docs.n8n.io/hosting/configuration/environment-variables/
- Dealing with errors: https://docs.n8n.io/workflows/workflow-errors/

### n8n MCP (Repos aus Scan)
- czlonkowski/n8n-mcp (Haupt): https://github.com/czlonkowski/n8n-mcp
- n8n-mcp Deployment/Docs (Beispiele aus Scan):
  - N8N_DEPLOYMENT.md: https://github.com/czlonkowski/n8n-mcp/blob/main/docs/N8N_DEPLOYMENT.md
  - HTTP_DEPLOYMENT.md: https://github.com/czlonkowski/n8n-mcp/blob/main/docs/HTTP_DEPLOYMENT.md
  - INSTALLATION.md: https://github.com/czlonkowski/n8n-mcp/blob/main/docs/INSTALLATION.md
  - README: https://github.com/czlonkowski/n8n-mcp/blob/main/README.md

### n8n “nodes mcp” / tools (aus Scan)
- nerding-io/n8n-nodes-mcp: https://github.com/nerding-io/n8n-nodes-mcp
- Bartmr/n8n-nodes-data-validation: https://github.com/Bartmr/n8n-nodes-data-validation

### n8n Skills (aus Scan)
- czlonkowski/n8n-skills: https://github.com/czlonkowski/n8n-skills

---

## 6) MCP Spezifikation (Transport/HTTP/SSE/STDIO)

- MCP Spec Repo (Haupt): https://github.com/modelcontextprotocol/specification
- Transports (aus Scan erwähnt, Datum 2025-03-26): https://github.com/modelcontextprotocol/specification/blob/main/docs/specification/2025-03-26/basic/transports.mdx

---

## 7) Context7 (Upstash) – Docs/Repo

- Upstash Context7 (Main): https://github.com/upstash/context7-mcp
- Context7 Produkt/Artikel (aus Scan): https://upstash.com/blog/context7

---

## 8) CLI Engines (Gemini CLI / Codex CLI / Claude Code)

### Gemini CLI
- gemini-cli Repo: https://github.com/google-gemini/gemini-cli
- Google Cloud Doc (Gemini CLI): https://cloud.google.com/gemini/docs/gemini-cli
- (Artikel/News aus Scan: Gemini CLI in Terminal, Security-Kontext etc. – wenn du die final brauchst, bitte die konkrete URL-Liste exporten)

### Codex CLI (OpenAI)
- Codex CLI Docs: https://developers.openai.com/codex/cli
- Codex Repo: https://github.com/openai/codex

### Claude Code
- Claude Code Docs: https://code.claude.com/
- MCP in Claude Code: https://code.claude.com/docs/mcp

---

## 9) v0.dev + 10Web (Produktprinzipien / Ops Feeling)

- v0 Docs: https://v0.dev/docs
- 10Web Help Center (Was ist 10Web): https://help.10web.io/hc/en-us/articles/360018941419-What-Is-10Web-Automated-WordPress-Platform
- 10Web Site (Booster/Builder): https://10web.io/

---

## 10) Supply Chain / Security Standards (für Playbooks)

- OWASP Cheat Sheet Series: https://cheatsheetseries.owasp.org/
- OWASP CI/CD “Dependency Chain Abuse” (CICD-SEC-3): https://owasp.org/www-project-top-10-ci-cd-security-risks/

---

## 11) SOTA Prompting / Agent-Methoden (die im Wanda-Prompt zitiert wurden)
> Diese Quellen sind “Methodik/Prompting”, nicht Tool-Dokus.

- Plan-then-execute / Prompt-Methoden: https://powertofly.com/up/mastering-prompt-engineering?utm_source=chatgpt.com
- ReAct vs naive chaining (Agent-Pattern): https://developers.redhat.com/articles/2025/07/22/react-vs-naive-prompt-chaining-llama-stack?utm_source=chatgpt.com
- Advanced Prompting Patterns: https://aiengineering.academy/PromptEngineering/Advanced_Prompting/?utm_source=chatgpt.com
- Prompt Engineering 2025/2026 (ToT/Reflection etc.): https://www.shivakumarpati.com/articles/2025/prompt-engineering-2025.html?utm_source=chatgpt.com
- Prompt Best Practices 2026 (Evaluator/Checklists): https://promptbuilder.cc/blog/prompt-engineering-best-practices-2026?utm_source=chatgpt.com
- Agentic AI Workflows (Governance/Patterns): https://rahulkolekar.com/agentic-ai-in-2026-from-single-prompts-to-end-to-end-workflows/?utm_source=chatgpt.com

---

## 12) Offene Lücken (nur wenn du “100% Vollständigkeit” willst)
Für eine garantierte “nichts ausgelassen”-Liste brauche ich EINES davon:
- A) den kompletten Text/Dateien von `DEEP_RESEARCH_1.md` und `DEEP_RESEARCH_2.md`, oder
- B) die DeepResearch “Sources/References”-Exportliste (alle URLs)
Dann erstelle ich:
- `QUELLEN_FINAL_DEEPRESEARCH_1.md`
- `QUELLEN_FINAL_DEEPRESEARCH_2.md`
- `QUELLEN_FINAL_ALL_IN_ONE.md` (deduped + kategorisiert + “wofür genutzt”)
