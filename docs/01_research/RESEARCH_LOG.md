# RESEARCH_LOG (web)

This log captures key findings used in the Phase-0 prompt.

## OpenCode config location
- `~/.config/opencode/opencode.json` or `opencode.jsonc` (and Windows `%APPDATA%\opencode\...` per ecosystem docs/posts).

## oh-my-opencode
- Installed as an OpenCode plugin.
- Config locations: user `~/.config/opencode/oh-my-opencode.json` and project `.opencode/oh-my-opencode.json`.
- Supports JSONC; `.jsonc` takes priority when both exist.
- Provides multiple specialized agents (Sisyphus, Oracle, Librarian, Explore, etc.).

## opencode-orchestrator
- GitHub-issue-driven orchestrator that assumes OpenCode + oh-my-opencode are already configured; it does not manage LLM keys.
