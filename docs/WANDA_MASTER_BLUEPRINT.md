# WANDA Sovereign AI OS – The Master Blueprint 🌟🤖🛡️

> **Document Status:** Absolute Single Source of Truth (SSOT)  
> **Version:** 1.0.0 (Full Vision Release)  
> **Author:** Jas0n 
> **Vision:** A decentralized, autonomous, and personal AI Operating System that bridges the gap between biological thought and digital execution.

---

## 1. Executive Summary
WANDA (Wireless Agentic Networked Digital Assistant) is more than a voice wrapper. It is a **Sovereign AI OS** designed to manage the user's entire digital life (Work-OS) through a multi-layered agentic architecture. It prioritizes local execution (Ollama), privacy (Sovereign Data), and human-centric interaction (Soul Voice).

---

## 2. System Architecture: The 7-Layer Kernel

WANDA operates through a specialized hierarchy of **17 agents** across 7 functional layers.

| Layer | Goal | Agents | Key Technology |
|:---:|---|---|---|
| **Ideation** | Conceptualization | Brainstormer | Gemini 3 Flash |
| **Orchestration** | Task Routing | Sisyphus | Gemini 3 Flash / Ollama |
| **Core** | Technical Execution | Architect, Developer, Audit, UI-UX | Claude 4.5 / Sonnet |
| **Specialist** | Deep Knowledge | Oracle, Writer, Librarian | Gemini Pro / RAG |
| **Research** | Data Gathering | Locator, Analyzer, Pattern-Finder | Gemini 3 Flash |
| **Continuity** | Context Preservation | Ledger, Artifact-Searcher | Local Vector DB |
| **Meta** | Plan Optimization | Metis, Momus | Claude Opus Thinking |

---

## 3. The Four Pillars (Plugin Ecosystem)

The OS is built upon four fundamental plugin modules that are synced live via GitHub:

1.  **OhMyOpencode (Orchestrator):** The central nervous system. Manages agent lifecycles, layer transitions, and tool permissions.
2.  **MiCode (Intelligence):** The "eyes" of the system. Uses AST-parsing and semantic analysis to understand codebases better than raw text.
3.  **Opencore (Tooling):** The "hands". Manages MCP servers (Docker, Filesystem, GitHub, Browser) for autonomous actions.
4.  **Wanda UI (Feedback):** The "face". A premium, Siri-style animated orb with micro-animations reflecting the internal state (Listening, Thinking, Speaking).

---

## 4. Interaction & Soul: The Voice Gateway 🎙️

WANDA aims for "JARVIS-level" conversational mastery.

### 4.1 Voice Engines
- **Heart (Premium):** **Coqui XTTS-v2**. Local voice cloning (~4-6GB VRAM) for 1:1 human-like speech.
- **Heart (Standard):** **Piper TTS**. High-speed, high-quality German voices (Eva, Kerstin fallback).
- **Ears:** **Faster-Whisper (Large-v3-Turbo)**. Sub-second transcription with CUDA acceleration.
- **VAD:** **Silero VAD (SOTA)**. 95%+ accuracy in noisy environments.

### 4.2 Interaction Loop
1.  **Hotkey/Wake-Word:** Activation via "Hey Wanda" or Physical Key.
2.  **Pulse Feedback:** Visual orb ripple + subtle audio cue.
3.  **Active Listening:** Dynamic VAD avoids cutting off the user.
4.  **Send-Confirmation:** Optional voice or terminal confirm before expensive tasks.
5.  **Live Interrupt:** < 200ms latency to stop speaking when the user starts.

---

## 5. Intelligence: The Hardware-Adaptive Brain 🧠

WANDA isn't one model; she is a dynamic selection of brains based on your hardware.

| System Class | RAM/VRAM | Recommended Local LLM | Capabilities |
|---|---|---|---|
| **S (Low)** | < 8GB RAM / 4GB V| Llama 3.2 (3B) | Basic Tasks, Dictation |
| **M (Mid)** | 16GB RAM / 8GB V | **Gemma 2 (9B)** / Mistral (7B) | Research, Brainstorming |
| **MH (Mid-High)** | 32GB+ RAM / 12GB V | **Qwen 2.5 (14B/32B)** / Command-R | Complex Reasoning, Deep Research |
| **G (High)** | 64GB+ RAM / 24GB V | DeepSeek-R1 / Llama 3.3 (70B) | Full Autonomy, Architecture |

**Unified Installer:** Detects VRAM/RAM/CPU and installs the optimal "Brain" automatically.

---

## 6. Operational Modes

1.  **Aktiv (Partner):** Standard interactive mode. Wanda assists while you work.
2.  **Paused (Standby):** Mic closed, system quiet. "Hallo Wanda" to resume.
3.  **CLI-Proxy:** Wanda injects prompts directly into terminal tools (Opencode, Claude-Code).
4.  **Autonomous (Wanda-Mode):** You give a high-level goal → Wanda plans, researches, and executes while giving progress updates.

---

## 7. The Workflow: Sovereign Data Sync 🔄

The repo `jas0nOW/wanda-agentic-system` is the **Source of Truth**.

- **Live Configs:** `~/.config/opencode/` are symlinked to the Repo.
- **Agent Prompts:** `GEMINI.md` is shared across all instances.
- **Installation:** A single command installs Node.js, Python, Docker, Ollama, and WANDA.
  ```bash
  curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
  ```

---

## 8. Safety & Sovereign Shields 🛡️

- **Audit Layer:** Every autonomous action is reviewed by a secondary "Audit-Agent" before execution.
- **Sandboxing:** (Roadmap) Execution of untrusted code in Docker containers.
- **Privacy Goggles:** Automated redaction of API keys, tokens, and personal data from logs and cloud-sent prompts.

---

## 9. Roadmap to v2.0 (The Autonomous Future)

- **v1.0.x (Current):** Stabilize cross-platform installation, local voice cloning, and symlink sync.
- **v1.5.0 (Intelligence):** DeepSeek-R1 full integration for complex reasoning.
- **v2.0.0 (Autonomy):** Full cross-terminal task delegation where Wanda manages multiple "sub-agent" terminals simultaneously.

---

> "Wanda ist nicht nur ein Tool. Sie ist die Manifestation deiner souveränen digitalen Identität."
