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
   
   b) Install OpenCode plugins:
      npm install -g oh-my-opencode@3.2.1 micode@latest

5. Start the system:
   - Agent System: opencode --profile experimental
   - Voice Assistant: wanda

Report any errors and I will help troubleshoot.
```

---

## What Gets Installed

### OpenCode Configuration
- `~/.config/opencode/profiles/` - All agent profiles
- `~/.config/opencode/profiles/experimental/opencode.json` - 17 agents
- `~/.gemini/GEMINI.md` - System kernel prompt

### Plugins (via npm)
- `oh-my-opencode@3.2.1` - Agent orchestration
- `micode@latest` - Code intelligence
- `opencode-supermemory@latest` - Memory persistence
- `opencode-handoff@latest` - Session handoff
- `opencode-scheduler@latest` - Task scheduling
- `opencode-knowledge@latest` - Local knowledge

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
