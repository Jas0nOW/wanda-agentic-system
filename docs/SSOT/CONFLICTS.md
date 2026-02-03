# SSOT Conflicts

## C-001 Orchestrator: Commander vs Sisyphus vs Orchestrator-Commander
- Sources: `docs/architecture/agents.md`, `docs/architecture/agent-roster.md`, `templates/AGENTS.md.template`, `docs/research/research-opencode-analysis.md`
- Conflict: Multiple primaries (Sisyphus, Commander, Orchestrator Commander).
- SSOT decision: Commander (MiCode) is the only primary. Others are disabled or subagent-only.
- Verification: In active agent roster, only Commander is primary.

## C-002 Agent count and roster mismatch
- Sources: `templates/AGENTS.md.template`, `docs/research/research-agent-reduction.md`, `docs/architecture/agent-roster.md`
- Conflict: 17 vs 14 vs explicit roster list.
- SSOT decision: `docs/architecture/agent-roster.md` is canonical; templates are non-binding.
- Verification: SSOT docs reference roster only; templates marked as templates.

## C-003 `.v0` location
- Sources: `docs/WANDA_FINAL_BLUEPRINT.md`, `docs/architecture/technical.md`, `docs/01.02 - DeepResearch.md`
- Conflict: `~/.v0` vs project-local `.v0/`.
- SSOT decision: `.v0/` is project-local and versioned; `~/.v0` is optional cache only.
- Verification: SSOT implementation plan uses repo-local `.v0/` paths.

## C-004 Fallback behavior vs B1 policy
- Sources: `docs/WANDA_FINAL_BLUEPRINT.md`, `docs/architecture/agents.md`
- Conflict: Auto fallback chain vs B1 (no runtime auto-failover).
- SSOT decision: No runtime auto-fallback. Switching is explicit via profile wrappers (`OPENCODE_CONFIG`, `OPENCODE_CONFIG_DIR`).
- Verification: SSOT docs define manual profile switching only.

## C-005 Antigravity plugin naming and scope
- Sources: `docs/WANDA_FINAL_BLUEPRINT.md`, `docs/architecture/plugin-standards.md`, `docs/01.02 - DeepResearch.md`
- Conflict: `opencode-antigravity-quota` vs `opencode-antigravity-auth` naming and behavior.
- SSOT decision: Use `opencode-antigravity-auth@latest` as canonical. `opencode-antigravity-quota@latest` is optional and only if verified.
- Verification: SSOT plugin list shows auth plugin as required; quota plugin flagged optional.

## C-006 Plugin inventory count
- Sources: `docs/WANDA_FINAL_BLUEPRINT.md`, `docs/architecture/plugin-standards.md`
- Conflict: plugin list and load-order assumptions differ.
- SSOT decision: Maintain a single canonical plugin list and mark optional plugins explicitly.
- Verification: SSOT docs include a single list with required vs optional.

## C-007 MCP server list variance
- Sources: `docs/WANDA_FINAL_BLUEPRINT.md`, `docs/architecture/agents.md`
- Conflict: MCP server list differs across docs.
- SSOT decision: SSOT MCP list must be deduped and tied to actual use-cases (skills/tools).
- Verification: SSOT MCP list includes only servers referenced by skills and workflows.

## C-008 Model naming vs real model IDs
- Sources: `docs/WANDA_HANDBOOK.html`, `docs/architecture/agents.md`
- Conflict: Human labels (e.g., "Gemini 3 Pro") vs actual model IDs.
- SSOT decision: Use real model IDs in config; labels only as glossary aliases.
- Verification: SSOT config examples list concrete model IDs.

## C-009 Template vs SSOT policy
- Sources: `templates/AGENTS.md.template`, `docs/architecture/agent-roster.md`
- Conflict: Template declares Sisyphus orchestrator; roster declares Commander primary.
- SSOT decision: Templates are non-binding; roster is SSOT.
- Verification: Templates explicitly marked non-canonical in SSOT docs.
