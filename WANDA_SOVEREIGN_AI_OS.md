# WANDA Sovereign AI OS – Final Product Blueprint 🌟🤖

> **Status:** Final Product Definition (Post-MVP)  
> **Version:** 1.0.1+  
> **Ziel:** Ein autarkes, souveränes KI-Betriebssystem, das 17 spezialisierte Agenten orchestriert, lokale Hardware (Ollama) maximal nutzt und über eine lebensechte Voice-Schnittstelle kommuniziert.

---

## 1) Die Vision: WANDA als "Sovereign OS"
WANDA entwickelt sich vom reinen Sprach-Wrapper (MVP) zu einem vollwertigen **Agentic OS**. Es ist das Gehirn deines Work-OS, verwaltet den Playground und delegiert Aufgaben an eine Flotte von Agenten.

### 1.1 Kern-Philosophie
- **Local-First, Remote-Hybrid:** Sensible Daten und Brainstorming lokal (Ollama), schwere Aufgaben remote (Antigravity/Gemini Pro).
- **Hardware-Agnotisch:** WANDA erkennt dein System und passt ihre Intelligenz-Dichte (Modellwahl) automatisch an.
- **Souveränität:** Volle Kontrolle über Plugins, Prompts und Agenten-Logik im GitHub Repo.

---

## 2) Das Gehirn: Multi-Agenten Orchestrierung 🧠

WANDA operiert in **7 Layern** mit insgesamt **17 Agenten**:

| Layer | Agenten | Primär-Modell (Vorschlag) |
|-------|---------|---------------------------|
| **Orchestration** | Sisyphus | Gemini 3 Flash / Ollama Mistral |
| **Ideation** | Brainstormer | Gemini 3 Pro / Ollama Gemma 2 |
| **Core** | Architect, Developer, Audit | Claude 4.5 / DeepSeek-R1 (Local) |
| **Specialist** | Oracle, Writer, Librarian | Gemini Pro |
| **Research** | Locator, Analyzer, Pattern-Finder | Gemini Flash |
| **Continuity** | Ledger, Artifact-Searcher | Gemini Flash |
| **Meta** | Metis, Momus | Claude Opus Thinking |

---

## 3) Die Stimme: Premium Audio & Soul 🎤🔊

Weg von der "Roboter-Stimme", hin zur personalisierten Partnerin.

### 3.1 Coqui XTTS-v2 (Premium-Pfad)
- **Voice Cloning:** Wanda erhält eine Stimme, die du mit einer 6-sekündigen Referenz (WAV) selbst definierst.
- **Lokale Ausführung:** Läuft vollständig offline (benötigt ~4-6GB VRAM für flüssige Latenz).
- **Emotionen:** XTTS-v2 unterstützt feine Nuancen in der Betonung.

### 3.2 Hardware-Adaptive Audiopfade
- **G (GPU):** XTTS-v2 (Full Quality)
- **M (CPU Mid):** Piper (High Quality Stimmen, z.B. Kerstin)
- **S (CPU Low):** Piper (Fast/Low Quality)

### 3.3 Audio-Interaktion
- **Interruptible:** Erhöhte Sensibilität für Unterbrechungen ("Wanda, halt kurz inne").
- **Ambient-Aware:** Lautstärke passt sich der Umgebung oder deiner Stimme an.

---

## 4) Deep Plugin Integration & Live Tracking 🔗

WANDA nutzt 4 Haupt-Plugins, deren Konfigurationen (Prompts & Settings) direkt im GitHub Repo liegen und per **Symlink** ins System eingebunden werden.

### 4.1 Die 4 Säulen
1. **OhMyOpencode:** Zentrale Orchestrierung der Layer.
2. **MiCode:** Die "Augen" des Systems für Code-Analysen (AST-basiert).
3. **Opencode-Orchestrator:** Koordiniert externe MCP Server und Tools.
4. **Wanda UI/UX:** Steuert den Orb und das visuelle Feedback.

### 4.2 Repo-Sync Workflow
Das Repo `wanda-agentic-system` ist die **Source of Truth**. Änderungen an einem Agenten-Prompt im Repo sind sofort im gesamten System aktiv. Kein manuelles Kopieren mehr.

---

## 5) Unified Hardware-Adaptive Installer ⚙️🚀

Der Installer v1.0.1+ ist ein intelligenter Assistent:

### 5.1 Audit-Phase
- Prüfung GPU (NVIDIA/AMD) und VRAM.
- Prüfung RAM und CPU-Cores.
- Prüfung der installierten Umgebungen (Node.js, Python, Docker).

### 5.2 Brain-Wizard
- **Ollama-Setup:** "Soll ich Ollama installieren?"
- **Modell-Vorschlag:**
  - `4GB VRAM` → Llama 3.2 (3b)
  - `8GB VRAM` → Gemma 2 (9b) / DeepSeek (8b)
  - `24GB+ VRAM` → Llama 3.3 (70b) / DeepSeek-R1 (Full)
- **Feature-Unlock:** Brainstorming/Research-Agenten werden erst bei ausreichender Hardware lokal "freigeschaltet".

### 5.3 Voice-Wizard
- Abspielen von Samples (Eva, Kerstin, Karlsson vs. XTTS-Clone).
- One-Click Installation der nötigen ONNX/Checkpoints.

---

## 6) Work-OS & Mobile Integration 📱🏢

### 6.1 Playground Management
Wanda kann via Sprache Projekte im Work-OS initialisieren:
- "Wanda, starte ein neues Experiment in Playground für eine Voice-App."
- Resultat: Ordnerstruktur nach JD-ID, README aus Template, Initialer Plan von Architect-Agent erstellt.

### 6.2 Mobile Gateway (Telegram)
- **VPS Hosting:** Der Telegram-Teil von Wanda läuft 24/7 auf dem VPS.
- **Push-to-Action:** Wanda schickt dir eine ntfy-Meldung aufs Handy, wenn ein Research-Task fertig ist. Du antwortest per Voice-Message: "Okay, bau darauf den ersten Prototyp."

---

## 7) Sicherheits-Architektur 🔒

- **Audit-Layer:** Bevor Wanda ein lokales Kommando vorschlägt, läuft es durch den `Audit`-Agenten.
- **Confirm-by-Voice:** "Soll ich den Docker-Container wirklich löschen?" – Bestätigung via Sprache.
- **Secrets-Shield:** Automatische Maskierung von API-Keys im Terminal und in den Logs.

---

## 8) Roadmap & Meilensteine

### v1.0.1 – The Sync & Voice Update
- [ ] Symlink-Architektur für Plugin-Configs.
- [ ] Hardware-Detection im Installer.
- [ ] Piper-Stimmenauswahl (Kerstin/Eva).

### v1.1.0 – The Soul Update
- [ ] Coqui XTTS-v2 Integration.
- [ ] Voice-Cloning Wizard.

### v1.5.0 – The Autonomous Layer
- [ ] Vollautomatische Research-Loops mit DeepSeek Integration.
- [ ] Proaktive Benachrichtigungen via Telegram.

---

**WANDA ist mehr als ein Programm – es ist dein digitaler Souverän.**
