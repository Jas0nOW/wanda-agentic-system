# WANDA Sovereign AI OS - Unified Agent Configuration (Draft)

This document outlines the proposed consolidation of Opencode, OhMyOpencode, MiCode, and Orchestrator into a single, unified agentic system.

---

## 1. The Unified Core (Kernel)
The system will use `GEMINI.md` as the global system instruction (Kernel). Every agent, regardless of its role, will inherit the WANDA core identity:
- **Tone**: Terse, efficient, German/English adaptive.
- **Principles**: Design first, no assumptions, research before code.
- **Tools**: Access to 14 MCP servers and specialized plugin tools (MiCode AST, OMO Backgrounders).

---

## 2. Refined Agent Roster

### 2.1 Primary Active Agents (Quick Access)
These agents are the "face" of WANDA and can be summoned directly by name.

| Agent | Core Layer | Model (Local/Cloud) | Primary Task |
|---|---|---|---|
| **Orchestrator** | Orchestration | Gemini 3 Flash / Qwen 2.5 (32B) | Task Routing, Session Mgmt |
| **Brainstormer** | Ideation | Gemini 3 Pro | Design-First questioning, Concept testing |
| **Architect** | Core | Claude 4.5 Thinking | Structural planning, File mapping |
| **Developer** | Core | Claude Sonnet 4.5 | Implementation, Bug fixing |
| **Librarian** | Specialist | Gemini 3 Flash / DeepSeek | Documentation research, Context gathering |
| **Writer** | Specialist | Gemini 3 Flash | Documentation, Reports, Code comments |

### 2.2 Specialized Sub-Agents (Autonomous)
These agents are called by the Orchestrator or the Developer in the background.

- **Audit**: Zero-trust code review (Claude Opus).
- **Oracle**: Deep reasoning & strategic backup (Claude Opus).
- **Explore**: Contextual grep & codebase mapping (Gemini Flash).
- **Multimodal-Looker**: Analyzing images, PDFs, diagrams (Gemini Pro).
- **Research Suite**: `codebase-locator`, `codebase-analyzer`, `pattern-finder`.
- **Continuity Suite**: `ledger-creator`, `artifact-searcher`.
- **Meta Suite**: `metis` (Pre-planning), `momus` (Review).

---

## 3. Integration of the 4 Pillars

### 3.1 OhMyOpencode (OMO) - The Nervous System
- **Role**: Manages the agent registry and model fallback chains.
- **Action**: All 17 agents will be defined in `oh-my-opencode.json`.
- **Enhancement**: Use OMO's "Background Tasks" for the Research Suite during the Architect phase.

### 3.2 MiCode - The Workflow Logic
- **Role**: Provides the `Brainstorm → Plan → Implement` methodology.
- **Action**: The `Architect` agent will adopt MiCode's `Plan` prompt logic. The `Brainstormer` adopts the collaborative questioning style.
- **Continuous Logic**: `/ledger` command will be unified into the WANDA Continuity Layer.

### 3.3 Opencore - The Toolset
- **Role**: Standardizes tool access (MCP servers).
- **Action**: Unified permission model ("ask" for bash/edit/write) across all agents.

### 3.4 Opencode-Orchestrator - The Autonomous Goal
- **Role**: High-level task tracking (v1.5+ focus).
- **Action**: Integration into the `Orchestrator` primary agent for long-running tasks.

---

## 4. Prompt Optimization Strategy

- **Harmonization**: Convert all hardcoded plugin prompts into configurable Markdown templates in `~/wanda-agentic-system/wanda-agents/prompts/`.
- **Ollama Specifics**: Prompts for local models will explicitly instruct on using the user's high RAM for context-heavy reasoning while keeping token output clean.
- **Workflows**: Common workflows (like `/ralph-loop`) will be re-written to use the unified 7-layer hierarchy instead of jumping between random agents.

---

## 5. Next Steps
1. **Approve Roster**: Is the primary list (6 agents) exactly what you need?
2. **Review Implementation**: I will start moving prompts to the repo if approved.
