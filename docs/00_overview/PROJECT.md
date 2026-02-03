# WANDA Sovereign AI OS - Project Summary 🚀

> **Mission**: Build a secure, autonomous, "Doppel-Wanda" System combining a **Local Voice Gateway** (Latency/Privacy) with a **Cloud Agentic Core** (Deep Reasoning).

## 1. The "Doppel-Wanda" Architecture
We split the system into two distinct domains to maximize both **privacy** and **intelligence**:

*   **🟢 Local Gateway (The Body)**:
    *   **Hardware**: 50GB RAM Workstation.
    *   **Role**: Understanding, Safety, Routing.
    *   **Stack**: `Faster-Whisper` → `Ollama (brainstorm-36b)` → `Silero VAD` → `Coqui XTTS-v2`.
    *   **Focus**: < 200ms latency, "Destructive Command" interception.

*   **🔵 Cloud Core (The Mind)**:
    *   **Role**: Deep Coding, Architecture, Complex Planning.
    *   **Stack**: `OpenCode` + 17 Agent Personas (Claude 4.5 / Gemini 3).
    *   **Orchestration**: `oh-my-opencode` plugin (Primary).

## 2. Hard Constraints (Locked)
*   **Orchestration**: `oh-my-opencode` is the ONLY default leader. `micode` is a manual playbook.
*   **Profiles**: `Stable` (Daily) vs `Experimental` (Multi-Agent Swarms).
*   **Token Policy**: Summarize & Prune. Do not persist raw tool output.
*   **Cost**: Use existing subsciptions. No new paid APIs.

## 3. Success Metrics (DoD)
*   ✅ **Installer**: One-click setup detects 50GB RAM & installs `XTTS-v2`.
*   ✅ **Safety**: `rm -rf` via voice triggers a "Are you sure?" dialog.
*   ✅ **Mobile**: Voice Note sent to Telegram appears as a Task in OpenCode.
*   ✅ **Resilience**: System functions (locally) even if internet is down.
