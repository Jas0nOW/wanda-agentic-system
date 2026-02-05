# WANDA Voice - OVOS Integration Guide

## Overview

The OVOS (OpenVoiceOS) bridge connects WANDA's voice engine to the OVOS ecosystem, enabling WANDA as a fallback handler for any utterance that OVOS's built-in skills don't handle.

## Prerequisites

- Running OVOS instance (bare-metal or Docker)
- WANDA Voice Core API running on same machine
- Python 3.10+ with `requests` package

## Setup

### 1. Start WANDA API

```bash
# Enable API in config
# wanda_voice.yaml:
# api:
#   enabled: true
#   port: 8370

python -m wanda_voice_core.api
```

### 2. Install Bridge Skill

```bash
# Copy skill to OVOS skills directory
cp -r ovos_bridge/wanda_bridge_skill/ \
  ~/.local/share/mycroft/skills/wanda-bridge.wanda/
```

### 3. Configure

Create `~/.local/share/mycroft/skills/wanda-bridge.wanda/settings.json`:

```json
{
  "wanda_api_url": "http://localhost:8370"
}
```

### 4. Restart OVOS

```bash
# Bare-metal
systemctl --user restart ovos-core

# Docker
docker restart ovos-core
```

## Docker Deployment

A `docker-compose.yml` is provided in `ovos_bridge/` for running OVOS + WANDA together:

```bash
cd ovos_bridge
docker compose up -d
```

## How It Works

1. User speaks to OVOS microphone
2. OVOS STT processes audio
3. OVOS intent system tries to match a skill
4. If no skill matches, `wanda_bridge_skill` catches it (priority 90)
5. Bridge POSTs to WANDA API `/v1/utterance`
6. WANDA processes through full pipeline (router -> refiner -> provider)
7. Response text returned to OVOS
8. OVOS TTS speaks the response

## Architecture

```
User Speech
    |
    v
OVOS STT (Whisper/Vosk)
    |
    v
OVOS Intent Engine
    |
    ├── Built-in skills (weather, timer, etc.)
    |
    └── Fallback (priority 90)
         |
         v
    wanda_bridge_skill
         |
         v (HTTP POST)
    WANDA API :8370
         |
         v
    WandaVoiceEngine
         |
         v
    Response Text
         |
         v
    OVOS TTS -> Speaker
```

## Limitations

- Bridge uses text-only mode (no audio streaming)
- Confirmation flow is skipped (API mode)
- OVOS handles its own TTS (not WANDA's TTS)
- Requires both systems running simultaneously
