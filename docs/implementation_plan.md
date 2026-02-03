# WANDA Sovereign AI OS - THE MASTER IMPLEMENTATION PLAN 🚀

> **Status**: FINAL & COMPREHENSIVE  
> **Mission**: Build a Hybrid AI Operating System where **Local Intelligence (Voice/Safety)** guides **Cloud Intelligence (Deep Reasoning)**.  
> **Core Philosophy**: "Wanda is the OS. The Voice is the Interface. The Agents are the Hands."

---

## 1. System Architecture: The Hybrid Core 🧠

We strictly separate **Latency-Critical (Local)** from **Compute-Critical (Cloud)** tasks.

### 1.1 The Local Layer (Voice & Gateway)
**Infrastructure**: Local Hardware (Ollama)  
**Role**: The "Front Desk". Understanding, Routing, Safety, Prompt Optimization.  

| Hardware Tier | RAM | Recommended Model | Capability |
|---|---|---|---|
| **S (Low)** | < 8GB | **Llama 4 Scout (17B MoE)** | Check status, Simple tags |
| **M (Mid)** | 16GB | **Gemma 3 (27B)** | Context Aware, Basic Routing |
| **MH (Mid-High)** | **50GB+** | **brainstorm-36b** / **neo-20b** | **SOTA Prompt Engineering, Deep Intent, VAD** |
| **G (High)** | 128GB+ | **DeepSeek V4** | Full Local Autonomy |

### 1.2 The Cloud Layer (Agentic Core)
**Infrastructure**: 5x Cloud Subscriptions (Anthropic, Google)  
**Role**: The "Engine Room". 17 Specialized Agents for Coding, Architecture, and Research.  

| Role | Agent(s) | Model |
|---|---|---|
| **Orchestrator** | Sisyphus | Gemini 3 Flash |
| **Coding** | Developer, Architect | Claude 4.5 Sonnet / Opus |
| **Review** | Audit, Momus | Claude 4.5 Opus (Thinking) |
| **Support** | Librarian, Oracle | Gemini 3 Pro (Multimodal) |

---

## 2. Features & Requirements Roadmap

### 🏁 Phase 1: The Foundation (Installer & Hardware)
- [ ] **Unified Installer (`install.sh`)**:
    - Detect Hardware (RAM/VRAM/CPU).
    - **Auto-Select Local Model**: Install `brainstorm-36b` automatically for your 50GB rig.
    - **Symlink Setup**: Link `~/wanda-agentic-system` to `~/.config/opencode` for live sync.

### TTS Strategy (Unified Installer Selection)
tts:
  # The User selects one of these during installation:
  profiles:
    premium:
      engine: coqui-xtts-v2
      model: "Wanda Cinema (v2.0)"
      hw_req: "4GB+ VRAM"
      desc: "Emotional, Breath-modulated, human-like."
    
    medium:
      engine: styletts2
      model: "Wanda Flow"
      hw_req: "2GB VRAM"
      desc: "Super-fast, fluent, high dynamic range."
      
    low:
      engine: vits-hifi
      model: "Wanda Spark"
      hw_req: "CPU / 500MB VRAM"
      desc: "Efficient, clear, superior to standard system voices."
      
  # Absolute Fallback (if everything fails)
  fallback:
    engine: piper
    voice: de_DE-kerstin-low
    mode: short
- [ ] **Dependency Check**: Ensure Node, Python, Docker, Ollama, Piper, and Silero VAD are present.

### 🗣️ Phase 2: The Voice Gateway (Local Intelligence)
- [ ] **SOTA VAD (Silero)**: < 200ms latency for natural interruption.
- [ ] **Prompt Optimization (Ollama)**: 
    - *Input*: "Mach mal ein Projekt für ne Website."
    - *Ollama Logic*: Expands request into a professional spec using `brainstorm-36b`.
    - *Readback*: "Ich habe verstanden: Du möchtest ein Web-Projekt initialisieren. Soll ich den React-Stack verwenden?"
- [ ] **Command Triggers**:
    - **Wake Word**: "Hey Wanda" (OpenWakeWord).
    - **Hotkey**: Right-CTRL (Focus Mode).
- [ ] **States**: Listening -> Thinking (Orb Pulse) -> Speaking -> Working.

### 🤖 Phase 3: The Agentic Connection (Cloud Bridge)
- [ ] **CLI Injection**: Wanda writes the optimized prompt directly into `opencode`, `claude`, or `terminal`.
- [ ] **Routing Map**:
    - Voice Command -> Ollama Intent Classifier -> Orchestrator (OhMyOpencode) -> Specific Agent.
- [ ] **Ollama Safety Layer**:
    - Before executing a destructive command (rm -rf, git push force), Ollama analyzes the intent and asks for confirmation.
- [ ] **Briefing Mode**:
    - On Click/Start: "Guten Morgen Jannis. Wir haben 3 offene PRs und das Projekt X ist unvollständig." (Source: Local Ledger + Git Status).

### 📱 Phase 4: Remote & Mobile (Telegram)
- [ ] **Telegram Bot**: Minimal Python bot connecting to the WANDA Event Bus.
- [ ] **Notifications**: Push alerts when an autonomous task is finished or stuck.
- [ ] **Voice Notes**: Send voice notes to Telegram -> Wanda processes them as tasks.

### 🛠️ Phase 5: Autonomous & Self-Healing
- [ ] **"Wanda Mode"**: Full autonomy loop.
    - *Loop*: Plan -> Execute -> Audit (Ollama Check) -> Fix -> Report.
- [ ] **Auto-Correction**: CLI errors are fed back to Ollama/Claude for immediate fix suggestions.

---

## 3. Technical Implementation Details

### 3.1 Ollama System Prompt (The Orchestrator)
The local model (e.g., `brainstorm-36b`) needs a specific System Prompt to act as the Gateway:
```markdown
You are Wanda, the Gateway Interface for the Sovereign AI OS.
Your job is NOT to write code, but to ORCHESTRATE the Agentic System.
1. Analyze user voice input.
2. Refine the prompt to be precise and technical.
3. Decide WHICH Agent (Developer, Architect, Writer) needs to handle it.
4. Output specific JSON instructions for the CLI Injector.
```

### 3.2 The "Dual-Brain" Data Flow
1. **User Voice** -> Whisper STT (Local).
2. **Text** -> **Ollama (Local)**: "Refine this request."
3. **Refined Text** -> **TTS (Local)**: "Shall I execute plan X?" (Confirmation).
4. **Execution** -> **Cloud Agents (Opus/Sonnet)**: The heavy lifting.
5. **Result** -> **Ollama (Local)**: "Analyze result for safety."
6. **Report** -> **TTS (Local)**: "Done. 3 files changed."

---

## 4. Checklist: The Final Audit
- [ ] Does the installer pick `brainstorm-36b` for 50GB RAM?
- [ ] Is "Readback Verification" enabled for complex tasks?
- [ ] Can I utilize "Pause/Resume" via voice?
- [ ] Is Mobile/Telegram configured?
- [ ] Are the 17 Cloud Agents correctly defined in `opencode.jsonc`?
- [ ] Is the Handbook visual showing the Dual Architecture?

---
