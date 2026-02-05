# Prompt Governance and Canonical Map

This document is the single source of truth for prompt locations, roles, and governance rules across the WANDA system.

## Canonical Prompt Map

### Canonical Repository (WANDA source)
- `prompts/system/WANDA_SYSTEM_PROMPT.md` - Co-owner mindset and high-level safety/efficiency rules.
- `prompts/system/OPENCODE_SYSTEM.md` - Cloud core prompt (OpenCode runtime).
- `prompts/system/OLLAMA_SYSTEM.md` - Local voice gateway prompt (Ollama routing and safety).
- `prompts/AGENT_ROSTER.md` - Agent graph and model roster.
- `prompts/context/AGENT_REGISTRY.md` - XML registry for all agents, triggers, models.
- `prompts/context/MCP_TOOL_MAPPING.md` - MCP server and tool mapping per agent.
- `prompts/context/PROJECT_CONTEXT.md.template` - User/workspace context template.
- `templates/GEMINI.md.template` - Personalized system kernel template for Gemini CLI.
- `templates/system.md.template` - Gemini CLI system prompt firmware template.
- `wanda-agents/GEMINI.md` - Realized Gemini kernel (reference snapshot).

### Runtime (User Home)
- `~/.claude/CLAUDE.md` - Claude Code system instructions.
- `~/.gemini/GEMINI.md` - Gemini CLI system kernel (generated from template).
- `~/.config/opencode/SYSTEM.md` - OpenCode system kernel.
- `~/.config/opencode/opencode.json` - OpenCode plugins and MCP config.
- `~/.config/opencode/oh-my-opencode.json` - Agent definitions and category models.

### Installer and Wiring
- `install.sh` - Template processing and deployment flow.
- `docs/architecture/opencode-system-kernel.md` - Documented copy of runtime kernel.

## Prompt Architecture (SOTA 2026)

### System Kernel (XML)
Prompts are structured as XML kernels with explicit sections. Core elements include:
- Identity and role
- Agent architecture and routing
- MCP server access
- Efficiency protocol
- Safety rules
- Terminal policy

### Chain of Thought (Embedded Policy)
The system defines a consistent plan/execute/verify loop in system prompts or templates to enforce disciplined execution.

### Dual-Core Model
- Cloud Core: `prompts/system/OPENCODE_SYSTEM.md`
- Local Voice Gateway: `prompts/system/OLLAMA_SYSTEM.md`

## Governance Rules (Documentation as Code)

1. Documentation is code: keep it current, precise, and minimal.
2. Archive instead of delete: completed plans/files go to an `Old/` folder or `archive/legacy_YYYYMMDD_HHMMSS/`.
3. Single source of truth: update `docs/SSOT/INVENTORY.md` and `docs/SSOT/CONFLICTS.md` when conflicts exist.
4. No prompt duplication: change the canonical file and propagate to runtime.
5. Avoid prompt noise: do not dump full prompt files in responses; reference paths.

## Update Procedure

1. Edit canonical prompt files in `prompts/` or `templates/`.
2. If the change affects runtime, update the corresponding files in:
   - `~/.claude/CLAUDE.md`
   - `~/.gemini/GEMINI.md`
   - `~/.config/opencode/SYSTEM.md`
3. If templates changed, re-run the installer or re-generate the target files.
4. Update `docs/architecture/opencode-system-kernel.md` if the kernel changed.
5. Move completed plans to `Old/` and archive legacy docs instead of deleting.

## Related References
- `docs/SSOT/INVENTORY.md`
- `docs/SSOT/CONFLICTS.md`
- `docs/workflows/wanda-lifecycle.md`
