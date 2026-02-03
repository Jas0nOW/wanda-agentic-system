# WANDA Sovereign AI OS – Der Master-Blueprint 🌟🤖🛡️

> **Dokumentenstatus:** Absoluter Single Source of Truth (SSOT)  
> **Version:** 1.0.0 (Visions-Release)  
> **Autor:** Jas0n 
> **Vision:** Ein dezentrales, autonomes und persönliches KI-Betriebssystem, das die Lücke zwischen biologischem Denken und digitaler Ausführung durch eine mehrschichtige agentische Architektur schließt.

---

## 1. Zusammenfassung (Executive Summary)
WANDA (Wireless Agentic Networked Digital Assistant) ist mehr als ein Voice-Wrapper. Es ist ein **souveränes KI-Betriebssystem**, das das gesamte digitale Leben des Nutzers (Work-OS) über eine mehrschichtige Agenten-Architektur verwaltet. Priorität haben lokale Ausführung (Ollama), Privatsphäre (Souveräne Daten) und menschzentrierte Interaktion (Soul Voice).

---

## 2. Systemarchitektur: Der 7-Layer-Kernel

WANDA operiert über eine spezialisierte Hierarchie von **17 Agenten** in 7 funktionalen Schichten.

| Schicht | Ziel | Agenten | Schlüsseltechnologie |
|:---:|---|---|---|
| **Ideation** | Konzeptualisierung | Brainstormer | Gemini 3 Flash |
| **Orchestration** | Aufgaben-Routing | Sisyphus | Gemini 3 Flash / Ollama |
| **Core** | Technische Ausführung | Architect, Developer, Audit, UI-UX | Claude 4.5 / Sonnet |
| **Specialist** | Tiefenwissen | Oracle, Writer, Librarian | Gemini Pro / RAG |
| **Research** | Datensammlung | Locator, Analyzer, Pattern-Finder | Gemini 3 Flash |
| **Continuity** | Kontexterhalt | Ledger, Artifact-Searcher | Lokale Vektor-DB |
| **Meta** | Plan-Optimierung | Metis, Momus | Claude Sonnet Thinking |

---

## 3. Die vier Säulen (Plugin-Ökosystem)

3.  Das OS basiert auf einer strikten Plugin-Hierarchie (SSOT 2026):

1.  **OhMyOpencode (Chefdirigent):** Das **primäre** Orchestrierungs-Plugin. Verwaltet Session, Auth und Token-Budget. "Der Boss".
2.  **MiCode (Playbook):** Eine **manuelle** Workflow-Engine für komplexe Tasks (Brainstorm → Plan → Code). Wird bewusst aufgerufen, ist *kein* dauerhafter Hintergrund-Orchestrator.
3.  **Opencode-Orchestrator (Experimentell):** Nur im `experimental` Profil aktiv. Dient als Testlabor für Multi-Agent-Schwärme.
4.  **Wanda Voice (Interface):** Das lokale Gateway (Ollama + XTTS). Es injiziert Befehle direkt in die CLI.

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

WANDA ist ein hybrider Organismus, der Cloud-Intelligenz für tiefes Denken und lokale Modelle für Echtzeit-Interaktion nutzt.

### 5.1 Der Agenten-Kern (Cloud SOTA) 🧠
Der Kern besteht aus **17 Agenten**, die deine 5 Cloud-Abonnements nutzen, um maximale Präzision zu erreichen.

| Schicht | Agenten | Primäres Modell (Cloud) | Fokus |
|---|---|---|---|
| **Ideation** | Brainstormer | Gemini 3 Pro | Konzepte, UX Mapping |
| **Core Coding** | Architect, Developer, Audit | Claude 4.5 Sonnet / Opus | TDD, Refactoring, Struktur |
| **Specialist** | Oracle, Writer, Librarian | Gemini Pro / Claude 4.5 | Recherche & Dokumentation |
| **Meta-Review** | Metis, Momus | Claude 4.5 Opus Thinking | Sicherheit & Plan-Prüfung |

### 5.2 Voice-Gateway & Lokaler Sicherheits-Layer (Ollama) 🛡️
Wanda ist mehr als nur Sprache. Das lokale Ollama-Modell fungiert als **Middleware** zwischen dir und dem Cloud-System:

1.  **Prompt-Optimierung**: Dein gesprochener Befehl wird von `brainstorm-36b` in einen präzisen technischen Prompt verwandelt.
2.  **Sicherheits-Check**: Bevor ein Befehl an die Cloud-Agenten geht, prüft Ollama auf destruktive Aktionen (z.B. `rm -rf`).
3.  **Readback & Briefing**: Wanda fasst komplexe Pläne mündlich zusammen ("Soll ich das so ausführen?") und gibt morgens ein Briefing.

**Hardware-Specs für den Installer (Lokale Modelle):**

| System-Klasse | RAM/VRAM | Empfohlenes lokales LLM (Gehirn) | Fähigkeiten |
|---|---|---|---|
| **S (Niedrig)** | < 8GB RAM / 4GB | **Llama 4 Scout (17B MoE)** | Schnelles Routing, Tags |
| **M (Mittel)** | 16GB RAM / 8GB | **Gemma 3 (27B)** | Voice-Interaktion & VAD |
| **MH (Mittel-Hoch)** | 50GB+ RAM / 8GB | **Qwen 2.5 Coder (32B)** / **Llama 4 Maverick** | **Dein Setup:** Deep Context, Prompt Refinement |
| **G (Hoch)** | 64GB+ RAM / 24GB | **DeepSeek V4** / **Qwen 3 (235B)** | Vollständige lokale Autonomie |

### 5.3 Wanda Voice Profiles (Installer Auswahl) 🗣️
Zusätzlich zum "Gehirn" wählst du die "Stimme" von Wanda. Alle drei Optionen sind hochwertig und **weiblich**:

| Audio-Klasse | Engine | Modell-Name | Charakteristik |
|---|---|---|---|
| **Premium** | **Coqui XTTS-v2** | "Wanda Cinema" | Emotional, atmend, ultra-realistisch. (Benötigt ~4GB VRAM) |
| **Medium** | **StyleTTS2** | "Wanda Flow" | Sehr flüssig, geringe Latenz, dynamisch. |
| **Low** | **VITS Hi-Fi** | "Wanda Spark" | Kristallklar, ressourcensparend (Besser als Standard). |
| *Fallback* | *Piper* | *Kerstin (Low)* | *Notfall-System bei Hardware-Fehlern.* |

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
