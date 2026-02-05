# SCOPE (Draft)

## In scope
1) Docs refactor: README + AI install prompt + full AI installation guide
2) Repo alignment: docs match current behavior; remove drift
3) Installer flow:
   - Fresh install
   - Re-install without nuking tokens/settings
   - Update mode
4) Modes:
   - `wanda` (default)
   - `wanda voice`
   - `wanda code`
   - `wanda` as “double system” mode that can delegate between voice+code
5) Cross-platform support matrix + automated doctor checks
6) Agent/plugin alignment:
   - OpenCode plugin loading
   - oh-my-opencode config and agent overrides
   - MiCode integration
   - opencode-orchestrator compatibility (optional)
7) v0-style skills packaging (final step): reusable skills/pipelines

## Out of scope (unless already in repo)
- Rewriting OpenCode/oh-my-opencode internals
- Non-official auth bypasses
