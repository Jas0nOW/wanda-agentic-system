# WANDA Installation Guide (SOTA 2026)

> **Vollständige Anleitung für die Installation des WANDA Agentic System**
> Diese Datei wird vom Installer ausgelesen und enthält alle notwendigen Schritte.

---

## Schnellstart (One-Liner)

```bash
curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
```

Oder manuell:

```bash
git clone https://github.com/jas0nOW/wanda-agentic-system.git ~/.wanda-system
cd ~/.wanda-system
chmod +x install.sh
./install.sh
```

---

## Voraussetzungen

### Minimale Anforderungen

| Komponente | Minimum | Empfohlen |
|------------|---------|-----------|
| **RAM** | 16 GB | 32+ GB |
| **VRAM** | 6 GB (NVIDIA) | 12+ GB |
| **Storage** | 20 GB | 50+ GB |
| **OS** | Linux, macOS, WSL2 | Linux (Ubuntu 22+) |

### Erforderliche Software

```bash
# Debian/Ubuntu
sudo apt update && sudo apt install -y \
    python3 python3-pip python3-venv \
    git curl wget \
    nodejs npm

# macOS
brew install python3 git node

# Docker (für MCP Server)
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER
# Logout/Login erforderlich
```

---

## MCP Server Setup (Docker Hub)

WANDA nutzt **Docker als zentralen MCP Hub**. Alle MCP Server laufen über den Docker MCP Gateway.

### Docker MCP Gateway starten

```bash
# Installation prüfen
docker --version

# MCP Gateway aktivieren (läuft automatisch)
docker mcp gateway status

# Alle verfügbaren Server auflisten
docker mcp gateway catalog
```

### MCP Server Mapping

| Server | Kategorie | Zweck | Secrets erforderlich |
|--------|-----------|-------|---------------------|
| `MCP_DOCKER` | Hub | Zentrale Gateway | - |
| `filesystem` | Core | Datei-Operationen | - |
| `memory` | Core | Wissens-Speicher | - |
| `github` | Dev | Repository-Ops | `GITHUB_TOKEN` |
| `brave` | Research | Web-Suche | `BRAVE_API_KEY` |
| `playwright` | Automation | Browser-Tests | - |
| `sequential-thinking` | Reasoning | Step-by-Step | - |
| `context7` | Research | Library-Docs | - |
| `firecrawl` | Research | Web-Scraping | `FIRECRAWL_API_KEY` |
| `supabase` | Database | Supabase-Ops | `SUPABASE_ACCESS_TOKEN` |
| `vercel` | Deploy | Vercel-Deploy | `VERCEL_API_TOKEN` |
| `stripe` | Payment | Stripe-API | `STRIPE_API_KEY` |
| `n8n-pro` | Automation | Workflow-Engine | - |

### Secrets konfigurieren

```bash
# ~/.bashrc oder ~/.zshrc hinzufügen:
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxx"
export BRAVE_API_KEY="BSAxxxxxxxxxxxxxxxx"
export FIRECRAWL_API_KEY="fc-xxxxxxxxxxxx"
# Optional:
export SUPABASE_ACCESS_TOKEN="sbp_xxxx"
export VERCEL_API_TOKEN="xxx"
export STRIPE_API_KEY="sk_live_xxx"

# Neu laden
source ~/.bashrc
```

---

## Konfigurationsdateien

### ~/.gemini/settings.json

Diese Datei konfiguriert Gemini CLI mit allen MCP Servern:

```json
{
  "$schema": "https://geminicli.com/settings.schema.json",
  "model": { "name": "auto-gemini-3" },
  "experimental": { "plan": true },
  "checkpointing": true,
  "mcpServers": {
    "MCP_DOCKER": {
      "command": "docker",
      "args": ["mcp", "gateway", "run"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-filesystem", "$HOME"]
    },
    "memory": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-memory"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-github"],
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
    },
    "brave": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-brave-search"],
      "env": { "BRAVE_API_KEY": "$BRAVE_API_KEY" }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-playwright"]
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-sequential-thinking"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

### ~/.gemini/GEMINI.md

Wird vom Installer personalisiert mit:
- `{{USERNAME}}` → Dein Name
- `{{WORKSPACE}}` → Dein Arbeitsordner
- `{{LANGUAGE}}` → Deine Sprache (de/en)

### ~/.config/opencode/opencode.jsonc

Symlink zu: `~/.wanda-system/wanda_cloud/profiles/stable/opencode.jsonc`

---

## OpenCode Plugins

Der Installer installiert automatisch:

```bash
npm install -g oh-my-opencode@3.2.1
```

Weitere empfohlene Plugins (manuell):

```bash
npm install -g opencode-antigravity-auth
npm install -g opencode-antigravity-quota
npm install -g envsitter-guard
npm install -g opencode-handoff
npm install -g opencode-websearch-cited
npm install -g opencode-shell-strategy
npm install -g opencode-context-analysis
```

---

## Ollama (Lokale Modelle)

Für Voice Assistant und lokale Verarbeitung:

```bash
# Installation
curl -fsSL https://ollama.com/install.sh | sh

# Empfohlene Modelle
ollama pull brainstorm-36b      # Voice Gateway
ollama pull neo-20b             # Code Completion
ollama pull heretic-12b         # Fallback
ollama pull qwen3:8b            # Lightweight

# Service starten
sudo systemctl enable ollama
sudo systemctl start ollama
```

---

## Voice Assistant Setup

```bash
cd ~/.wanda-system/wanda_local

# Python venv
python3 -m venv venv
source venv/bin/activate

# Dependencies
pip install -r requirements.txt

# Konfiguration prüfen
cat config.yaml

# Starten
python main.py
```

### macOS Siri TTS

Auf macOS wird automatisch die native `say`-Kommando mit deutscher Stimme "Anna" genutzt.

---

## Telegram Bot (Optional)

```bash
# Token von @BotFather holen
# In ~/.wanda-system/wanda_local/.env eintragen:
WANDA_TELEGRAM_BOT_TOKEN=your_token_here
WANDA_USER_NAME=DeinName

# Lokal starten
cd ~/.wanda-system/wanda_local
source venv/bin/activate
python telegram_bot.py

# Für 24/7 (mit PM2)
npm install -g pm2
pm2 start telegram_bot.py --interpreter python3 --name wanda-telegram
pm2 save
pm2 startup
```

---

## Troubleshooting

### MCP Server Verbindungsprobleme

```bash
# Docker Status prüfen
docker ps
docker mcp gateway status

# NPX Cache leeren
npx clear-npx-cache

# MCP Server manuell testen
npx -y @anthropic/mcp-filesystem $HOME
```

### Ollama nicht erreichbar

```bash
# Status prüfen
systemctl status ollama

# Logs prüfen
journalctl -u ollama -f

# Neustart
sudo systemctl restart ollama
```

### Gemini CLI MCP Liste leer

```bash
# Gemini CLI neustarten
gemini

# Im CLI:
/mcp

# Sollte alle Server listen
```

---

## Dateien-Übersicht

```
~/.wanda-system/
├── install.sh                 # Personalisierter Installer
├── docs/
│   └── INSTALLATION.md        # Diese Datei
├── prompts/
│   ├── system/
│   │   ├── OPENCODE_SYSTEM.md
│   │   ├── OLLAMA_SYSTEM.md
│   │   └── TERMINAL_POLICY.md
│   └── context/
│       ├── MCP_TOOL_MAPPING.md
│       ├── AGENT_REGISTRY.md
│       └── PROJECT_CONTEXT.md
├── templates/
│   └── GEMINI.md.template
├── mcp-servers/
│   └── settings.json.template
├── wanda_cloud/
│   └── profiles/
│       ├── stable/
│       └── experimental/
├── wanda_local/
│   ├── main.py
│   ├── telegram_bot.py
│   └── src/
└── scripts/
    ├── diagnostics.sh
    └── deploy-hook.sh
```

---

## Nach der Installation

```bash
# 1. Diagnostik laufen lassen
bash ~/.wanda-system/scripts/diagnostics.sh

# 2. Gemini CLI testen
gemini
# Dann: /mcp (MCP Server prüfen)
# Dann: /settings (Einstellungen prüfen)

# 3. OpenCode testen
opencode
# Kein Fehler = Erfolg!

# 4. Voice Assistant testen
cd ~/.wanda-system/wanda_local
source venv/bin/activate
python main.py
```

---

## Support

- **Repository**: https://github.com/jas0nOW/wanda-agentic-system
- **Issues**: https://github.com/jas0nOW/wanda-agentic-system/issues
- **Version**: 1.0.1

---

*WANDA - Sovereign AI Operating System*
