# WANDA AI Installation Guide

> **Für KI-Assistenten**: Diese Anleitung enthält alle Informationen um WANDA automatisch zu installieren und Fehler zu beheben.

## Quick Install

```bash
# Empfohlener One-Liner
curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
```

## Manual Install

```bash
git clone https://github.com/jas0nOW/wanda-agentic-system.git ~/.wanda-system
cd ~/.wanda-system
chmod +x install.sh
./install.sh
```

---

## Installer Workflow

Der Installer fragt interaktiv:

1. **User Info**: Name, Workspace, Language
2. **Hardware Profile**: S/M/M-High/High (auto-detected)
3. **Ollama Config**: Skip / Recommended / Defaults / Custom
4. **Cloud Providers**: Anthropic, Google, OpenAI, GitHub Copilot Tiers
5. **Agent Models**: WANDA Defaults / Subscription-Based / Custom
6. **Components**: Agents / Voice / Telegram
7. **MCP Setup**: Docker Gateway / npx Fallback / Skip

---

## Post-Installation

```bash
# WANDA starten
wanda

# Debug mode bei Problemen
wanda -d

# Status prüfen
wanda status
```

---

## Edge Cases & Fixes

### Freeze beim Starten (90% der Fälle)

**Symptom**: WANDA startet, aber nichts passiert.

**Lösung**:
```bash
# npm Cache leeren
npm cache clean --force

# OpenCode neu installieren
npm install -g @anthropic-ai/opencode

# Oder Gemini CLI
npm install -g @anthropic-ai/gemini-cli
```

### Voice Assistant Freeze

**Symptom**: Voice startet nicht oder hängt.

**Lösung**:
```bash
# PyTorch CPU-only installieren (vermeidet CUDA Konflikte)
pip uninstall torch
pip install torch --index-url https://download.pytorch.org/whl/cpu

# Whisper + VAD neu installieren
pip install --upgrade faster-whisper silero-vad
```

### Permission Denied

**Symptom**: `EACCES`, `Permission denied` Fehler.

**Lösung**:
```bash
sudo chown -R $USER:$USER ~/.wanda-system
chmod +x ~/.wanda-system/bin/wanda
chmod +x ~/.wanda-system/scripts/update.sh
```

### API Errors

**Symptom**: `401 Unauthorized`, `API key invalid`.

**Lösung**: API-Keys in `~/.gemini/settings.json` prüfen:
```json
{
  "mcpServers": {
    "github": {
      "env": {
        "GITHUB_TOKEN": "ghp_xxx"
      }
    }
  }
}
```

### MCP Not Connecting

**Symptom**: `MCP server not found`, Docker errors.

**Lösung**:
```bash
# Docker starten
systemctl start docker

# Docker Container prüfen
docker ps

# Fallback: npx MCP verwenden (wird bei Neuinstall angeboten)
```

### Node/npm Errors

**Symptom**: `npm ERR!`, Module nicht gefunden.

**Lösung**:
```bash
# Node.js Version prüfen (18+ erforderlich)
node -v

# npm Update
npm install -g npm@latest

# Cache + Reinstall
npm cache clean --force
npm install -g @anthropic-ai/opencode
```

### Python Version

**Symptom**: `SyntaxError`, async Fehler.

**Lösung**:
```bash
# Python 3.10+ erforderlich
python --version

# Falls zu alt:
# Ubuntu: sudo apt install python3.11
# macOS: brew install python@3.11
```

---

## Wichtige Dateien

| Pfad | Zweck |
|------|-------|
| `~/.wanda-system/` | Installation Root |
| `~/.wanda-system/bin/wanda` | CLI wrapper |
| `~/.wanda-system/config/agents.yaml` | Agent-Konfiguration |
| `~/.wanda-system/config/voice_commands.yaml` | Voice-Kommandos |
| `~/.gemini/GEMINI.md` | System Prompt |
| `~/.gemini/settings.json` | MCP & API Keys |
| `~/.config/opencode/opencode.jsonc` | OpenCode Config |

---

## Debug Mode

```bash
wanda -d
```

**Was passiert**:
1. Startet WANDA im Hintergrund
2. Prüft nach 10 Sekunden auf Fehler
3. Prüft nach 20 Sekunden auf Fehler
4. Fragt User:
   - "Ja - Läuft perfekt"
   - "Freezed beim Starten" → Package-Fix Anleitung
   - "Eigene Antwort" → Problem-Analyse

**Log-Datei**:
```bash
/tmp/wanda_debug_XXXXXX.log
```

---

## Vollständige Neuinstallation

Bei schwerwiegenden Problemen:

```bash
# Komplett entfernen
rm -rf ~/.wanda-system
rm -f ~/.gemini/GEMINI.md ~/.gemini/settings.json
rm -f ~/.config/opencode/opencode.jsonc

# Shell Profile säubern (optional)
# Entferne WANDA Zeilen aus ~/.bashrc oder ~/.zshrc

# Neu installieren
curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
```

---

*WANDA v1.0.4 - AI Installation Guide*
