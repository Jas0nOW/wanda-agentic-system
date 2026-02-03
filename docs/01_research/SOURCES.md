# SOURCES.md - Research Log for WANDA Implementation

> **Last Updated**: 2026-02-03  
> **Status**: Phase 0 Research

---

## Plugin Ecosystem

| Plugin Name | Status | Source | Notes |
|---|---|---|---|
| `oh-my-opencode` | ✅ Verified | [npm](https://www.npmjs.com/package/oh-my-opencode), [GitHub](https://github.com/oh-my-opencode/oh-my-opencode) | Install: `bunx oh-my-opencode install` |
| `micode` | ✅ Verified | [npm](https://www.npmjs.com/package/micode) | Manual Playbook Engine |
| `opencode-antigravity-auth` | ✅ Verified | OpenCode Ecosystem | Multi-Account Rotation |
| `opencode-antigravity-quota` | ✅ Verified | OpenCode Ecosystem | Cost Control |
| `opencode-websearch-cited` | ✅ Verified | [opencode.ai/plugins](https://opencode.ai/plugins) | Cited Web Search |
| `opencode-shell-strategy` | ✅ Verified | OpenCode Ecosystem | Shell Hang Prevention |
| `opencode-context-analysis` | ✅ Verified | OpenCode Ecosystem | Token Analysis |
| `opencode-dynamic-context-pruning` | ✅ Verified | OpenCode Ecosystem | Context Optimization (Default: OFF) |
| `envsitter-guard` | ✅ Verified | OpenCode Ecosystem | Secret Leak Prevention |
| `opencode-supermemory` | ⚠️ Check Free Plan | Supermemory.ai | Fallback: `opencode-knowledge` |
| `opencode-orchestrator` | ✅ Verified | OpenCode Ecosystem | Experimental Only |

---

## Local Models (Ollama)

| Model | Status | Size | Use Case |
|---|---|---|---|
| `brainstorm-36b` | ✅ Installed | 21 GB | Primary Gateway (Prompt Refinement) |
| `neo-20b` | ✅ Installed | 15 GB | Alternative Gateway |
| `heretic-12b` | ✅ Installed | 7.5 GB | Fast Routing |
| `qwen3-abliterated:8b` | ✅ Installed | 5.0 GB | Lightweight Fallback |

---

## TTS/STT Engines

| Engine | Status | Source | Notes |
|---|---|---|---|
| Faster-Whisper | ✅ Verified | [GitHub](https://github.com/guillaumekln/faster-whisper) | GPU-accelerated STT |
| Silero VAD | ✅ Verified | [GitHub](https://github.com/snakers4/silero-vad) | < 200ms latency target |
| Coqui XTTS-v2 | ✅ Verified | [Hugging Face](https://huggingface.co/coqui/XTTS-v2) | Premium Voice Cloning |
| StyleTTS2 | ✅ Verified | [GitHub](https://github.com/yl4579/StyleTTS2) | Medium Quality TTS |
| Piper TTS | ✅ Verified | [GitHub](https://github.com/rhasspy/piper) | Fallback (Kerstin) |

---

## Official Documentation
- OpenCode Plugins: https://opencode.ai/docs/plugins
- Oh-My-Opencode: https://github.com/oh-my-opencode/oh-my-opencode
- Silero VAD: https://github.com/snakers4/silero-vad
- Faster-Whisper: https://github.com/guillaumekln/faster-whisper
- Coqui XTTS-v2: https://huggingface.co/coqui/XTTS-v2
