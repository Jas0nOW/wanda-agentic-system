# OVOS Bridge for WANDA Voice Core

Connects [OpenVoiceOS](https://openvoiceos.org/) to WANDA's voice engine via REST API.

## Architecture

```
OVOS (Mycroft-compatible) -> wanda_bridge_skill -> WANDA API (localhost:8370)
```

## Setup

1. Start WANDA API:
   ```bash
   python -m wanda_voice_core.api
   ```

2. Install the bridge skill into your OVOS instance:
   ```bash
   cp -r wanda_bridge_skill/ ~/.local/share/mycroft/skills/wanda-bridge.wanda/
   ```

3. Configure `settings.json`:
   ```json
   {
     "wanda_api_url": "http://localhost:8370"
   }
   ```

## Docker (Optional)

For a full OVOS stack, use `docker-compose.yml`:
```bash
docker compose up -d
```

## How It Works

- OVOS captures user speech via its own STT pipeline
- The bridge skill forwards utterances to WANDA's `/v1/utterance` endpoint
- WANDA processes (route -> refine -> provider) and returns response text
- OVOS speaks the response via its TTS engine
