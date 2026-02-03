# SSOT Worklog

## 2026-02-02

### Context
- Branch: `chore/wanda-ssot-clean-2026-02-01`
- Scope: establish SSOT inventory + conflict log before new SSOT docs

### Decisions (B1)
- Use `opencode-antigravity-auth@latest` as canonical Google auth plugin.
- `opencode-antigravity-quota@latest` is optional and only if verified.
- No runtime auto-failover; use profile switching via `OPENCODE_CONFIG` / `OPENCODE_CONFIG_DIR`.

### Actions
- Created `docs/SSOT/` directory.
- Added `docs/SSOT/INVENTORY.md` and `docs/SSOT/CONFLICTS.md` based on current docs.

### Next
- Review SSOT inventory/conflicts for alignment with B1 policy.
- Commit Phase 1 (`chore(ssot): add inventory + conflicts`).
