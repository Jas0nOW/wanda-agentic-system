# Wanda Sovereign AI OS - Master Architecture 2026 (SOTA Restoration)

Diese Dokumentation ist die "Sovereign Source of Truth" (SSOT) für das agentische System von Jannis.

## 🤖 Der Swarm (Agenten & Hierarchie)
Das System nutzt **oh-my-opencode** zur Orchestrierung spezialisierter Agenten.

### Core Agents
| Agent | Mission | Modell |
| :--- | :--- | :--- |
| **Sisyphus** | Orchestrator: Dynamic Routing & Session Continuity | Gemini 3 Flash |
| **Architect** | Blueprint Designer: Reasoning-over-Execution | Claude 4.5 Opus (Thinking) |
| **Software-Engineer** | Builder: Implementierung via Flow Engineering | Claude 4.5 Sonnet |
| **Audit** | Fixer: Zero-Trust Security & PoC Exploits | Claude 4.5 Opus (Thinking) |
| **Frontend-UI-UX** | Designer: DTCG Design Tokens & AG-UI | Gemini 3 Pro |
| **Oracle** | Think Tank: Strategie & Closed-Loop Learning | Claude 4.5 Opus (Thinking) |
| **Writer** | Scribe: Recursive Technical Documentation & Drafting | Gemini 3 Flash |
| **Librarian** | Researcher: Source-First Grounding (SFG) | Gemini 3 Flash |
| **Explore** | Scout: AST-Guided Semantic Mapping | Gemini 3 Flash |

### 📁 Aufgaben-Kategorien (Brain-Swapping)
- **ultrabrain**: Claude 4.5 Opus (Thinking) [Max Budget] - Höchste Logik.
- **deep**: Claude 4.5 Opus (Thinking) [Max Budget] - Autonome Problemlösung.
- **visual-engineering**: Gemini 3 Pro - Frontend, CSS & Animationen.
- **artistry**: Gemini 3 Pro (High) - Kreative Konzepte & Design-Innovation.
- **quick**: Gemini 3 Flash - Trivial-Aufgaben & schnelle Edits.
- **writing**: Gemini 3 Flash - Dokumentation & technisches Schreiben.

## 🛠️ MCP Tool-Ecosystem (Managed Stability)

### 🚀 Vercel (Hybrid-Steuerung)
- **Vercel Remote**: `npx mcp-remote https://mcp.vercel.com` (Official OAuth API).
- **Vercel Local**: Managed via `@robinson_ai_systems/vercel-mcp` (Token-basiert).
- **Status**: VERCEL_TOKEN-Variable ist konfiguriert für Stabilität.

### 📊 Backend & Database
- **Supabase**: Cloud-Management (Auth, Functions, Storage).
- **Postgres**: Direkte SQL-Power (verbunden mit `Plant_Log` via Supabase Pooler).
- **n8n-pro**: Full Lifecycle Management (Workflows & Node Discovery).

### 🌐 Research & Intel
- **Brave Search**: SOTA Web-Grounding (Search API).
- **Firecrawl**: Deep Web Scraping (Markdown-Konvertierung).
- **Context7**: Live-Dokumentation für SOTA Libraries.

## ⚙️ Technische Details
- **RAM-Safe**: Alle MCP-Prozesse auf **2048MB (2GB)** limitiert (`--max-old-space-size=2048`).
- **Display**: Wayland-optimiert via `ELECTRON_OZONE_PLATFORM_HINT`.
- **Archiv**: `/home/jannis/Schreibtisch/Work-OS/_ARCHIVE_REDUNDANT/` (Backup aller Windows-Altlasten).
