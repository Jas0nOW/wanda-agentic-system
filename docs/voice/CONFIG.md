# WANDA Voice Mode - Configuration Reference

Config file: `wanda_voice.yaml` (searched in CWD, `~/.wanda/voice.yaml`, `~/.wanda-system/wanda-voice/wanda.config.yaml`)

## Profiles

| Profile | Orb | LogWindow | TTS | Provider |
|---------|-----|-----------|-----|----------|
| `gui` (default) | Yes | Yes | Edge | Gemini |
| `simple` | No | No | Piper | Gemini |
| `offline` | No | No | Piper | Ollama |

## All Config Options

### audio
| Key | Default | Description |
|-----|---------|-------------|
| `audio.backend` | `pipewire` | Audio backend |
| `audio.sample_rate` | `16000` | Sample rate in Hz |
| `audio.max_seconds` | `60` | Max recording duration |
| `audio.silence_timeout` | `1.2` | Silence before auto-stop (seconds) |
| `audio.silence_threshold` | `0.01` | Amplitude threshold for silence |
| `audio.min_seconds` | `1.0` | Minimum recording duration |

### vad
| Key | Default | Description |
|-----|---------|-------------|
| `vad.engine` | `silero` | VAD engine (silero/energy) |
| `vad.min_silence_duration_ms` | `500` | Min silence for VAD trigger |

### stt
| Key | Default | Description |
|-----|---------|-------------|
| `stt.engine` | `faster-whisper` | STT engine |
| `stt.model` | `large-v3-turbo` | Whisper model |
| `stt.device` | `auto` | Device (auto/cuda/cpu) |
| `stt.language` | `de` | Transcription language |

### router
| Key | Default | Description |
|-----|---------|-------------|
| `router.use_ollama` | `false` | Use Ollama for routing |
| `router.confidence_threshold` | `0.6` | Minimum confidence |

### refiner
| Key | Default | Description |
|-----|---------|-------------|
| `refiner.enabled` | `true` | Enable prompt refinement |
| `refiner.model` | `qwen3:8b` | Ollama model for refinement |
| `refiner.timeout` | `30` | Timeout in seconds |

### providers
| Key | Default | Description |
|-----|---------|-------------|
| `providers.primary` | `gemini_cli` | Primary LLM provider |
| `providers.gemini_model` | `flash` | Gemini model variant |
| `providers.gemini_timeout` | `90` | Gemini timeout (seconds) |
| `providers.gemini_max_retries` | `2` | Max retry attempts |
| `providers.gemini_fallback_model` | `pro` | Fallback model |
| `providers.ollama_model` | `qwen3:8b` | Ollama model |
| `providers.ollama_enabled` | `false` | Enable Ollama |
| `providers.ollama_as_fallback` | `false` | Use Ollama as fallback |

### tts
| Key | Default | Description |
|-----|---------|-------------|
| `tts.engine` | `edge` | TTS engine (edge/piper) |
| `tts.voice` | `katja` | Voice name |
| `tts.mode` | `short` | Speaking mode |
| `tts.piper_voice` | `de_DE-kerstin-low` | Piper fallback voice |
| `tts.interruptable` | `true` | Allow barge-in |

### safety
| Key | Default | Description |
|-----|---------|-------------|
| `safety.command_execution` | `false` | Allow command execution |
| `safety.risk_threshold_voice` | `3` | Voice confirm threshold |
| `safety.risk_threshold_gui` | `6` | GUI confirm threshold |
| `safety.redact_secrets` | `true` | Redact sensitive data |

### token_economy
| Key | Default | Description |
|-----|---------|-------------|
| `token_economy.max_context_chars` | `8000` | Max context size |
| `token_economy.max_turns` | `12` | Max conversation turns |
| `token_economy.max_output_tokens` | `2048` | Max output tokens |

### ui
| Key | Default | Description |
|-----|---------|-------------|
| `ui.orb` | `true` | Show visual orb |
| `ui.log_window` | `true` | Show log window |
| `ui.orb_size` | `60` | Orb diameter in pixels |

### hotkey
| Key | Default | Description |
|-----|---------|-------------|
| `hotkey.key` | `rightctrl` | Hotkey for recording |
| `hotkey.mode` | `toggle` | Mode (toggle/hold) |

### confirmation
| Key | Default | Description |
|-----|---------|-------------|
| `confirmation.enabled` | `true` | Enable voice confirmation |
| `confirmation.timeout` | `10` | Response timeout (seconds) |
| `confirmation.readback` | `true` | Read back improved text |

### api
| Key | Default | Description |
|-----|---------|-------------|
| `api.enabled` | `false` | Enable REST API |
| `api.port` | `8370` | API port |
| `api.host` | `127.0.0.1` | API bind address |
