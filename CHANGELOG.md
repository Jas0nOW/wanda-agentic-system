# Changelog

All notable changes to WANDA Agentic System will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.1] - 2026-02-03

### 🎉 Major Release: Complete System Overhaul

This release transforms WANDA from a prototype into a **production-ready Sovereign AI OS**.

### Added

#### Personalized Installer
- Interactive installer asks for **username**, **workspace folder**, and **language**
- Automatic template processing with `{{USERNAME}}`, `{{WORKSPACE}}`, `{{LANGUAGE}}` tokens
- User-agnostic installation - works for anyone, not just the developer

#### Context Files (NEW)
- `prompts/context/MCP_TOOL_MAPPING.md` - Complete mapping of 15 MCP servers to 17 agents
- `prompts/context/AGENT_REGISTRY.md` - Full documentation of all 17 agents across 7 layers
- `prompts/context/PROJECT_CONTEXT.md.template` - User-specific context template

#### System Prompts (SOTA 2026)
- `prompts/system/OPENCODE_SYSTEM.md` - Cloud Core with Chain-of-Thought (XML-structured)
- `prompts/system/OLLAMA_SYSTEM.md` - Voice Gateway with routing heuristics
- `prompts/system/TERMINAL_POLICY.md` - Comprehensive DENY/CONFIRM/ALLOW command lists

#### Templates
- `templates/GEMINI.md.template` - Personalized Gemini CLI system prompt
- `mcp-servers/settings.json.template` - Docker MCP hub with 8 server configurations

#### MCP Server Integration
- **Docker as central hub** (`MCP_DOCKER`)
- Pre-configured servers: `filesystem`, `memory`, `github`, `brave`, `playwright`, `sequential-thinking`, `context7`
- Automatic setup via installer

#### Voice Assistant
- `wanda_local/main.py` - Entry point
- `wanda_local/src/vad.py` - Silero Voice Activity Detection
- `wanda_local/src/stt.py` - Whisper Speech-to-Text
- `wanda_local/src/gateway.py` - Ollama Gateway with routing
- `wanda_local/src/tts.py` - XTTS-v2 / macOS Siri TTS
- `wanda_local/src/safety.py` - Command safety checker
- `wanda_local/src/cli_injector.py` - OpenCode CLI integration
- `wanda_local/telegram_bot.py` - Telegram Bot handler

#### Documentation
- `docs/INSTALLATION.md` - Complete setup guide with Docker MCP instructions
- `docs/VALIDATION_CHECKLIST.md` - Testing and verification steps
- `docs/WANDA_AGENT_CONFIGURATION.md` - Agent configuration reference
- `docs/WANDA_ALIGNMENT_REPORT.md` - Architecture alignment documentation
- `docs/WANDA_MASTER_BLUEPRINT_DE.md` - German technical blueprint

#### Scripts
- `scripts/diagnostics.sh` - System health check
- `scripts/deploy-hook.sh` - VPS auto-deployment webhook

#### Tests
- `tests/test_smoke.py` - Basic smoke tests

### Changed

- **README.md** - Complete rewrite with v1.0.1 branding, MCP server table, improved Quick Start
- **install.sh** - Rewritten with personalization, template processing, MCP setup
- **mcp-servers/settings.json.template** - Full Docker hub configuration

### Fixed

- OpenCode profiles now use correct schema (`plugin`, `mcp`, `instructions` keys)
- MCP server format corrected: `{type: "local", command: [...], enabled: true}`

---

## [1.0.0] - 2026-01-15

### Added
- Initial repository structure
- Basic README
- License (MIT)
- .gitignore

---

## Migration Guide (1.0.0 → 1.0.1)

```bash
# 1. Backup existing config
cp ~/.gemini/GEMINI.md ~/.gemini/GEMINI.md.backup
cp ~/.gemini/settings.json ~/.gemini/settings.json.backup

# 2. Pull latest
cd ~/.wanda-system
git pull

# 3. Re-run installer for personalization
./install.sh

# 4. Verify MCP servers
gemini
# Then type: /mcp
```

---

*WANDA - Sovereign AI Operating System*
