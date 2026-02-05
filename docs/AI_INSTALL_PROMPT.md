# 🌟 WANDA Agentic System - AI Installation Prompt

**Copy this full prompt to your AI (OpenCode, Gemini CLI, Claude, etc.) to automatically install WANDA:**

---

```
Install the WANDA Agentic System from GitHub:

1. Clone the repository:
   git clone https://github.com/jas0nOW/wanda-agentic-system ~/.wanda-system

2. Run the installer:
   cd ~/.wanda-system && chmod +x install.sh && ./install.sh

3. Follow the interactive prompts to install:
   - Agent System (17 agents, profiles, GEMINI.md)
   - Voice Assistant (STT, TTS, Orb UI)
   - MCP Servers (optional)

4. After installation, configure:
   a) Add Antigravity account:
      Create ~/.config/opencode/antigravity-accounts.json with:
      {"accounts": [{"email": "user@email.com", "token": "YOUR_TOKEN"}]}
   
   b) Install OpenCode plugins (SSOT list):
      See docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md

   c) Create OpenCode config and command:
      cp ~/.wanda-system/config/opencode.json.template ~/.config/opencode/opencode.json
      mkdir -p ~/.config/opencode/command
      cp ~/.wanda-system/config/command/antigravity-quota.md ~/.config/opencode/command/antigravity-quota.md

5. Start the system:
   - Agent System: opencode --profile experimental
   - Voice Assistant: wanda

Report any errors and I will help troubleshoot.
```

---

## What Gets Installed

### OpenCode Configuration
- `~/.config/opencode/opencode.json` - Base config (from template)
- `~/.config/opencode/oh-my-opencode.json` - Agent routing
- `~/.config/opencode/SYSTEM.md` - System kernel
- `~/.config/opencode/command/antigravity-quota.md` - Quota command
- `~/.gemini/GEMINI.md` - System kernel prompt

### Plugins (via npm)
- Canonical list: docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md

### Voice Assistant
- `~/.wanda-system/wanda-voice/` - All voice modules
- `/usr/local/bin/wanda` - Global command

---

## Updates

When I push updates to GitHub, users just run:
```bash
cd ~/.wanda-system && git pull && ./install.sh
```

All configs get updated automatically!
