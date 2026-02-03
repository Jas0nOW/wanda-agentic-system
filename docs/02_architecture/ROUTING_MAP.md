# ROUTING_MAP.md - Orchestration Conflict Resolution

> **Profile**: Experimental  
> **Status**: SSOT for Multi-Agent Routing

---

## The Leadership Hierarchy

When multiple orchestration plugins are active, conflicts are resolved as follows:

```
┌─────────────────────────────────────────────────────────────────┐
│                     OH-MY-OPENCODE (BOSS)                       │
│  - Session Init, Auth, Quota, High-Level Routing                │
│  - Commands: /oracle, /librarian, /frontend, /brainstorm        │
└───────────────────────────┬─────────────────────────────────────┘
                            │ Invokes (on user request)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                     MICODE (PLAYBOOK)                           │
│  - Workflow Engine: Brainstorm → Plan → Implement               │
│  - Command: /micode <task>                                      │
│  - NOT an autonomous loop. Manual invocation only.              │
└───────────────────────────┬─────────────────────────────────────┘
                            │ May spawn (in experimental)
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                 OPENCODE-ORCHESTRATOR (LAB)                     │
│  - Background Agents, Swarm Logic                               │
│  - EXPERIMENTAL ONLY. Disabled in stable profile.               │
│  - Defers to oh-my-opencode on conflict.                        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Agent Deduplication

To prevent duplicate agents from consuming tokens:

| Agent Name | Source Plugin | Status |
|---|---|---|
| `oracle` | oh-my-opencode | ✅ Active |
| `librarian` | oh-my-opencode | ✅ Active |
| `brainstormer` | oh-my-opencode | ✅ Active |
| `frontend-dev` | micode | ✅ Active (via /micode) |
| `architect` | opencode-orchestrator | ⚠️ Experimental |
| `developer` | opencode-orchestrator | ⚠️ Experimental |

---

## Conflict Resolution Rules

1.  **Same Task, Two Answers**: If `oh-my-opencode` and `opencode-orchestrator` both respond to the same prompt, the `oh-my-opencode` response is shown. The other is logged but discarded.
2.  **Token Budget**: `oh-my-opencode` manages the global token budget. If `opencode-orchestrator` exceeds its allocation, its background agents are paused.
3.  **Manual Override**: User can always force routing via explicit command (e.g., `/micode plan` or `/orchestrator background`).
