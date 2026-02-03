# WANDA v1.x - Expanded Implementation Plan (Master Prompt Alignment)

This expanded plan incorporates the strict requirements from the "JANNIS / LazyTechLab MASTER PROMPT". Our goal is to stabilize the global environment and ensure a conflict-free, high-fidelity orchestration stack.

---

## 🔬 Discrepancy & Research Report

| Feature | Current WANDA (v1.0.1) | Master Prompt Requirement | Status |
|---|---|---|---|
| **Config Format** | `.json` (Standard) | `.jsonc` (JSON with Comments) | To be migrated 🔄 |
| **Workflow** | WANDA 7-Layer Kernel | 9-Layer (Layer 0–8) Architecture | To be merged 🔄 |
| **Plugin-Set** | Core (OMO, MiCode, Auth) | Full Baseline (A) + Experimental (B) | Expansion needed 🛠️ |
| **Security** | Standard Permissions | `envsitter-guard` + `.env` leak protection | To be added 🛡️ |
| **Deliverables** | Blueprints (EN/DE) | Routing Map, Cheat Sheet, Rollback | To be created 📄 |
| **Profiles** | Basic `experimental` folder | Profile-isolated `opencode-orchestrator` | To be enforced 🧪 |

---

## 🛠️ Phase E: Master Prompt Compliance (Priority 1)

### E.1 Baseline Expansion (Plugin Set A)
We will install and verify the verified 2026 SOTA utility stack:
- **Security**: `envsitter-guard` (Verified: Bun/OpenCode native env protection).
- **Stability**: `opencode-shell-strategy` (Prevents non-TTY hangs).
- **Efficiency**: `opencode-dynamic-context-pruning` + `opencode-context-analysis`.
- **Search**: `opencode-websearch-cited` (Positioned last in config).

### E.2 The Routing Map (Conflict Resolution)
To avoid command collisions between `oh-my-opencode` and `micode`:
- **Inventory**: Scan all commands introduced by plugins.
- **Rules**: 
    - `oh-my-opencode` is the **Leading Orchestrator** for general tasks.
    - `micode` is **Explicitly Triggered** for `Brainstorm → Plan → Implement` cycles.
- **De-Dupe**: Disable redundant agents (e.g., duplicated research agents) in the config.

### E.3 Forensics & Rollback
- **Forensics Phase**: Implement a `check_env()` step in `install.sh` that provides exactly one command at a time for manual verification.
- **Rollback**: Every change must produce a timestamped backup in `~/.config/opencode/backups/`.

---

## 📄 Deliverables for Jannis
1. `~/.config/opencode/ROUTING_MAP.md`: Clear mapping of task → tool.
2. `~/.config/opencode/CHEATSHEET.md`: Quick-commands for WANDA.
3. `~/.config/opencode/ROLLBACK.md`: Instructions for emergency recovery.
4. `~/.config/opencode/opencode.jsonc`: The finalized, documented global config.
