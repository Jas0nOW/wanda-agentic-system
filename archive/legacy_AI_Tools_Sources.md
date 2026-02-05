# AI Tools Quellen & Setup Guide

## 1. OpenCode
**CLI AI Coding Agent**

| Ressource | URL |
|-----------|-----|
| GitHub | https://github.com/opencode-ai/opencode |
| Docs | https://opencode.ai/docs/ |
| Providers | https://opencode.ai/docs/providers/ |
| Config | https://opencode.ai/docs/config/ |
| Models | https://opencode.ai/docs/models/ |

### Installation
```bash
curl -fsSL https://opencode.ai/install.sh | bash
# oder
npm install -g opencode
```

### Key Plugins
| Plugin | Zweck |
|--------|-------|
| `opencode-antigravity-auth` | Google OAuth (Gemini, Claude via AG) |
| `opencode-gemini-auth` | Gemini CLI OAuth |

**Antigravity Plugin:**
- GitHub: https://github.com/NoeFabris/opencode-antigravity-auth
- Docs: https://github.com/NoeFabris/opencode-antigravity-auth/blob/main/README.md
- Multi-Account: https://github.com/NoeFabris/opencode-antigravity-auth/blob/main/docs/MULTI-ACCOUNT.md

---

## 2. Oh-My-OpenCode
**OpenCode Plugin Suite mit Multi-Agent System**

| Ressource | URL |
|-----------|-----|
| GitHub | https://github.com/code-yeongyu/oh-my-opencode |
| Releases | https://github.com/code-yeongyu/oh-my-opencode/releases |
| Installation | https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/guide/installation.md |
| Configuration | https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/configurations.md |

### Installation
```bash
bunx oh-my-opencode install
# oder mit Flags:
bunx oh-my-opencode install --claude=yes --chatgpt=no --gemini=yes
```

### Features
- Multi-Agent: Sisyphus, Oracle, Librarian, Explore
- LSP & AST Tools
- Built-in MCPs (Exa, Context7, Grep.app)
- Provider Fallback: Native > Copilot > Free

---

## 3. OpenClaw (ex-Clawdbot/Moltbot)
**Personal AI Assistant - Multi-Platform Message Hub**

| Ressource | URL |
|-----------|-----|
| GitHub | https://github.com/moltbot/moltbot |
| Skills | https://github.com/VoltAgent/awesome-moltbot-skills |

### Geschichte
- Nov 2025: Clawdbot
- Jan 2026: → Moltbot (Anthropic C&D)
- 30. Jan 2026: → OpenClaw

### Features
- Unified Message Hub (WhatsApp, Telegram, Slack, Terminal)
- Local Memory System (Markdown)
- 100k+ GitHub Stars

---

## 4. V0 by Vercel
**AI Website/App Builder**

| Ressource | URL |
|-----------|-----|
| App | https://v0.app/ |
| Docs | https://v0.app/docs |
| Platform API | https://vercel.com/blog/build-your-own-ai-app-builder-with-the-v0-platform-api |
| AI SDK | https://ai-sdk.dev/docs/introduction |
| SDK GitHub | https://ai-sdk.dev/ |

### Platform API
- Text-to-App API
- Headless App Builder
- TypeScript SDK

### Use Cases
- Website Builder Bots
- Slack/Discord → deployed apps
- VSCode Plugins
- Embedded dev flows

---

## Quick Reference: Config Paths

```
~/.config/opencode/opencode.json          # Haupt-Config
~/.config/opencode/antigravity.json       # Antigravity Plugin Settings
~/.config/opencode/antigravity-accounts.json  # OAuth Accounts
~/.config/opencode/oh-my-opencode.json    # Oh-My-OpenCode Config
```

---

## Fetch-Tipps für andere KIs

```
# OpenCode Docs
WebFetch: https://opencode.ai/docs/providers/

# Antigravity Plugin README
WebFetch: https://github.com/NoeFabris/opencode-antigravity-auth

# Oh-My-OpenCode Installation & Docs
WebFetch: https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/guide/installation.md
WebFetch: https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs
WebFetch: https://github.com/code-yeongyu/oh-my-opencode

# V0 Docs
WebFetch: https://v0.app/docs
```
