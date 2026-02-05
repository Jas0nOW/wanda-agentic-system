# WANDA Sovereign AI OS – Der Master-Blueprint 🌟🤖🛡️

> **Dokumentenstatus:** Absoluter Single Source of Truth (SSOT)  
> **Version:** 1.0.0 (Visions-Release)  
> **Autor:** Antigravity (Assistent) für Jannis (Souverän)  
> **Vision:** Ein dezentrales, autonomes und persönliches KI-Betriebssystem, das die Lücke zwischen biologischem Denken und digitaler Ausführung durch eine mehrschichtige agentische Architektur schließt.

---

## 1. Zusammenfassung (Executive Summary)
WANDA (Wireless Agentic Networked Digital Assistant) ist mehr als ein Voice-Wrapper. Es ist ein **souveränes KI-Betriebssystem**, das das gesamte digitale Leben des Nutzers (Work-OS) über eine mehrschichtige Agenten-Architektur verwaltet. Priorität haben lokale Ausführung (Ollama), Privatsphäre (Souveräne Daten) und menschzentrierte Interaktion (Soul Voice).

---

## 2. Systemarchitektur: Der 7-Layer-Kernel

WANDA operiert über eine spezialisierte Hierarchie von **17 Agenten** in 7 funktionalen Schichten.

| Schicht | Ziel | Agenten | Schlüsseltechnologie |
|:---:|---|---|---|
| **Ideation** | Konzeptualisierung | Brainstormer | Gemini 3 Pro |
| **Orchestration** | Aufgaben-Routing | Sisyphus | Gemini 3 Flash / Ollama |
| **Core** | Technische Ausführung | Architect, Developer, Audit, UI-UX | Claude 4.5 / Sonnet |
| **Specialist** | Tiefenwissen | Oracle, Writer, Librarian | Gemini Pro / RAG |
| **Research** | Datensammlung | Locator, Analyzer, Pattern-Finder | Gemini Flash |
| **Continuity** | Kontexterhalt | Ledger, Artifact-Searcher | Lokale Vektor-DB |
| **Meta** | Plan-Optimierung | Metis, Momus | Claude Opus Thinking |

---

## 3. Die vier Säulen (Plugin-Ökosystem)

Das OS basiert auf vier fundamentalen Plugin-Modulen, die live über GitHub synchronisiert werden:

1.  **OhMyOpencode (Orchestrator):** Das zentrale Nervensystem. Veraltet Agenten-Lebenszyklen, Layer-Übergänge und Tool-Berechtigungen.
2.  **MiCode (Intelligence):** Die "Augen" des Systems. Nutzt AST-Parsing und semantische Analyse, um Codebasen besser zu verstehen als reiner Text.
3.  **Opencore (Tooling):** Die "Hände". Verwaltet MCP-Server (Docker, Filesystem, GitHub, Browser) für autonome Aktionen.
4.  **Wanda UI (Feedback):** Das "Gesicht". Ein hochwertiger, animierter Orb im Siri-Stil mit Mikro-Animationen, die den internen Status widerspiegeln (Zuhören, Denken, Sprechen).

---

## 4. Interaktion & Seele: Das Voice-Gateway 🎙️

WANDA strebt eine Konversationsqualität auf "JARVIS-Niveau" an.

### 4.1 Voice-Engines
- **Herz (Premium):** **Coqui XTTS-v2**. Lokales Voice-Cloning (~4-6GB VRAM) für 1:1 menschenähnliche Sprache.
- **Herz (Standard):** **Piper TTS**. Hochgeschwindigkeits-TTS mit hochwertigen deutschen Stimmen (Eva, Kerstin-Fallback).
- **Ohren:** **Faster-Whisper (Large-v3-Turbo)**. Transkription in unter einer Sekunde mit CUDA-Beschleunigung.
- **VAD:** **Silero VAD (SOTA)**. 95%+ Genauigkeit in lauten Umgebungen.

### 4.2 Interaktions-Loop
1.  **Hotkey/Wake-Word:** Aktivierung über "Hey Wanda" oder physische Taste.
2.  **Puls-Feedback:** Visuelle Orb-Welle + subtiler Audio-Cue.
3.  **Aktives Zuhören:** Dynamische VAD verhindert, dass der Nutzer unterbrochen wird.
4.  **Sende-Bestätigung:** Optionale Sprach- oder Terminal-Bestätigung vor rechenintensiven Aufgaben.
5.  **Live-Interrupt:** < 200ms Latenz, um das Sprechen sofort zu beenden, wenn der Nutzer zu reden beginnt.

---

## 5. Intelligenz: Das Hardware-adaptive Gehirn 🧠

WANDA nutzt kein einzelnes Modell, sondern eine dynamische Auswahl an "Brains" basierend auf deiner Hardware.

| System-Klasse | VRAM | Empfohlenes lokales LLM | Fähigkeiten |
|---|---|---|---|
| **S (Niedrig)** | < 4GB | Llama 3.2 (3B) | Basis-Aufgaben, Diktat |
| **M (Mittel)** | 6-8GB | **Gemma 2 (9B)** / DeepSeek (8B) | Research, Brainstorming |
| **G (Hoch)** | 16GB+ | DeepSeek-R1 / Llama 3.3 (70B) | Volle Autonomie, Architektur |

**Unified Installer:** Erkennt VRAM/RAM/CPU und installiert das optimale Gehirn automatisch.

---

## 6. Betriebsmodi

1.  **Aktiv (Partner):** Standardmäßiger interaktiver Modus. Wanda unterstützt dich während der Arbeit.
2.  **Pause (Standby):** Mikrofon geschlossen, System ruhig. "Hallo Wanda" zum Fortfahren.
3.  **CLI-Proxy:** Wanda injiziert Prompts direkt in Terminal-Tools (Opencode, Claude-Code).
4.  **Autonom (Wanda-Mode):** Du gibst ein High-Level-Ziel vor → Wanda plant, recherchiert und führt aus, während sie Status-Updates gibt.

---

## 7. Der Workflow: Souveräner Daten-Sync 🔄

Das Repo `jas0nOW/wanda-agentic-system` ist die **Source of Truth**.

- **Live-Configs:** `~/.config/opencode/` sind per Symlink mit dem Repo verbunden.
- **Agenten-Prompts:** `GEMINI.md` wird über alle Instanzen geteilt.
- **Installation:** Ein einziger Befehl installiert Node.js, Python, Docker, Ollama und WANDA.
  ```bash
  curl -fsSL https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/install.sh | bash
  ```

---

## 8. Sicherheit & Souveräne Schilde 🛡️

- **Audit-Layer:** Jede autonome Aktion wird von einem sekundären "Audit-Agenten" vor der Ausführung geprüft.
- **Sandboxing:** (Roadmap) Ausführung von nicht vertrauenswürdigem Code in Docker-Containern.
- **Privacy-Goggles:** Automatische Maskierung von API-Keys, Tokens und persönlichen Daten in Logs und Cloud-Prompts.

---

## 9. Roadmap zu v2.0 (Die autonome Zukunft)

- **v1.0.x (Aktuell):** Stabilisierung der plattformübergreifenden Installation, lokales Voice-Cloning und Symlink-Sync.
- **v1.5.0 (Intelligenz):** Vollständige Integration von DeepSeek-R1 für komplexe Überlegungen.
- **v2.0.0 (Autonomie):** Vollständige Aufgaben-Delegation über mehrere Terminals, bei der Wanda mehrere "Sub-Agenten" gleichzeitig steuert.

---

> "Wanda ist nicht nur ein Tool. Sie ist die Manifestation deiner souveränen digitalen Identität."
