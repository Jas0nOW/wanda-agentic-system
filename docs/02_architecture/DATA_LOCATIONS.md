# Data Locations

This file lists canonical runtime locations. These are not tracked in the repo.

## OpenCode
- Config: ~/.config/opencode
- System kernel: ~/.config/opencode/SYSTEM.md
- Plugins and MCP config: ~/.config/opencode/opencode.json
- Cache: ~/.cache/opencode
- Auth/state: ~/.local/share/opencode

## Gemini CLI
- Context: ~/.gemini/GEMINI.md
- System prompt: ~/.gemini/system.md (enable via GEMINI_SYSTEM_MD)
- Config: ~/.gemini/settings.json

## Claude Code
- Context: ~/.claude/CLAUDE.md
- Config: ~/.claude/settings.json
- Skills: ~/.claude/skills/

## Codex CLI
- Config: ~/.codex/config.toml
- Instructions: ~/.codex/instructions.md

## WANDA Runtime
- Context: ~/.wanda/context.json

## Security
- Secrets must remain outside the repo.
- Do not mirror ~/.config/opencode/opencode.json into git.
