# WANDA JARVIS MASTERPLAN

> **WICHTIG: NEUER PLAN - BITTE NICHT LÖSCHEN ODER WEG SORTIEREN!**
> **Neueste Datei - Enthält die komplette Vision und Roadmap**

**Erstellt:** 2026-02-04 05:08:24
**Status:** AKTIV
**Owner:** Jannis

---

## 1. VISION

WANDA soll ein echtes **JARVIS-System** werden - ein intelligenter Partner für die tägliche Arbeit:

- **Natürliche Konversation** wie Iron Man mit Jarvis
- **Proaktive Verbesserungsvorschläge** - nicht nur reagieren, sondern mitdenken
- **Selbstverbesserung** - lernt aus jeder Interaktion
- **Agenten-Orchestrierung** - kann OpenCode/OhMyOpenCode Agenten steuern
- **Projekt-Initialisierung** - "Starte ein neues Venture" → komplettes Setup
- **Brainstorming-Partner** - Design-First Thinking mit dem @brainstormer Agent

---

## 2. AKTUELLE PROBLEME (zu fixen)

### 2.1 Ollama Integration
- [x] Config `enabled` wurde ignoriert → **GEFIXT**
- [x] Hardcoded Model `qwen2.5:32b` existiert nicht → **GEFIXT**
- [x] Installer: Auto-Hardware-Detection (VRAM + RAM) → **GEFIXT**
- [x] Installer: Custom Model Support → **GEFIXT**

### 2.2 STT (Speech-to-Text)
- [x] Buchstabensalat Output → **Anti-Halluzination Settings hinzugefügt**
- [x] Debug-Output für Audio-Statistiken → **GEFIXT**
- [ ] Testen ob Fixes funktionieren
- [ ] Fallback zu kleinerem Whisper-Model bei Problemen

### 2.3 TTS (Text-to-Speech)
- [x] Deutsche Stimmen-Auswahl im Installer → **GEFIXT**
- [x] 6 Stimmen verfügbar (3 weiblich, 3 männlich) → **GEFIXT**
- [ ] XTTS v2 für noch natürlichere Stimmen (Phase 2)
- [ ] Voice Cloning für Custom JARVIS-Stimme (Phase 2)

### 2.4 Global Commands
- [x] `wanda` Command → **GEFIXT**
- [x] `wanda-voice` Command → **GEFIXT**

---

## 3. INSTALLER VERBESSERUNGEN

### 3.1 Hardware Auto-Detection ✅ IMPLEMENTIERT

```python
# Implementiert in setup.py - erkennt VRAM + RAM
def detect_hardware() -> dict:
    """Detect GPU VRAM and System RAM."""
    # Returns: {tier, gpu_name, vram_gb, ram_gb}

# 7 Hardware-Tiers mit passenden Modellen:
RECOMMENDED_MODELS = {
    "high":     # 20GB+ VRAM → qwen3:32b, llama3.3:70b-q4, deepseek-r1:32b
    "medium":   # 10-20GB VRAM → qwen3:14b, llama3.3:latest, mistral-nemo:12b
    "low":      # 5-10GB VRAM → qwen3:8b, llama3.2:latest, gemma3:9b
    "minimal":  # 3-5GB VRAM → qwen3:4b, phi4:latest, gemma3:4b
    "cpu-high": # CPU + 32GB+ RAM → qwen3:8b-q4_K_M (quantisiert)
    "cpu":      # CPU + 16GB RAM → qwen3:4b-q4_K_M
    "cpu-low":  # CPU + <16GB RAM → qwen3:1.7b, tinyllama
}
```

### 3.2 Installer Optionen

```
🧠 OLLAMA KONFIGURATION
────────────────────────────────────

Deine Hardware: NVIDIA RTX 4090 (24GB) → Tier: HIGH

[1] Auto (empfohlen für deine Hardware)
    → qwen2.5:32b, deepseek-coder:33b
[2] Custom Model eingeben
[3] Aus installierten Modellen wählen
[0] Ollama deaktivieren

Wähle (1):
```

### 3.3 Custom Model Support

- User kann eigenes Model eingeben: `ollama run my-custom-model`
- Validierung: Prüft ob Model existiert via `ollama show <model>`
- Speichert in Config: `ollama.model: my-custom-model`

---

## 4. PROMPT-OPTIMIERUNG (Kern-Feature)

### 4.1 Zweck
Die Brücke zwischen gesprochener Sprache und präzisen AI-Prompts:

```
User sagt: "Mach mir ne Website für mein Startup"

Ollama optimiert zu:
"Erstelle eine moderne Landing Page für ein Tech-Startup mit:
- Hero Section mit CTA
- Features Section (3 Spalten)
- Testimonials
- Footer mit Links
Stack: Next.js 14, Tailwind CSS, shadcn/ui"
```

### 4.2 Optimierungs-Strategien

1. **Kontext-Anreicherung** - Fügt relevanten Projektkontext hinzu
2. **Füllwort-Entfernung** - "ähm", "also", "halt" → weg
3. **Struktur-Verbesserung** - Bullet Points, klare Anforderungen
4. **Tool-Routing** - Entscheidet: Gemini vs OpenCode vs Claude

### 4.3 System Prompt für Ollama

```
Du bist WANDA's Intelligenz-Kern. Deine Aufgaben:

1. PROMPT-OPTIMIERUNG
   - Wandle gesprochene Sprache in präzise Prompts um
   - Füge technischen Kontext hinzu
   - Strukturiere mit Bullet Points
   - Behalte die Absicht des Users

2. DELEGATION
   - gemini: Allgemeine Fragen, Recherche, Brainstorming
   - opencode: Code-Aufgaben, Projekte, Implementierung
   - claude: Komplexe Reasoning, Architektur-Entscheidungen

3. PROAKTIVE VORSCHLÄGE
   - Erkenne Verbesserungspotential
   - Schlage Alternativen vor
   - Weise auf mögliche Probleme hin
```

---

## 5. AGENTEN-ORCHESTRIERUNG

### 5.1 Integration mit OpenCode/OhMyOpenCode

WANDA soll Agenten aus dem 17-Agent-System steuern können:

```yaml
# Verfügbare Agenten via Voice
agents:
  brainstormer: "Design-First, keine Code-Generierung"
  architect: "System-Design, Architektur-Entscheidungen"
  software-engineer: "Code-Implementierung"
  frontend-ui-ux: "UI/UX Design und Implementierung"
  audit: "Code-Review, Security-Check"
  oracle: "Tiefes Reasoning, komplexe Probleme"
  writer: "Dokumentation, READMEs"
  librarian: "Codebase-Wissen, API-Docs"
```

### 5.2 Voice Commands für Agenten

```
"Wanda, starte den Brainstormer für eine neue App-Idee"
→ Öffnet OpenCode mit @brainstormer Kontext

"Wanda, lass den Architect das System designen"
→ Startet /ralph-loop Phase 1 (Architect)

"Wanda, Code-Review für das letzte Commit"
→ Startet Audit-Agent auf HEAD~1
```

### 5.3 Workflow-Integration

```python
# conversation/intelligence.py - Erweiterung
AGENT_WORKFLOWS = {
    "brainstorm": {
        "trigger": ["brainstorm", "idee", "konzept", "design"],
        "agent": "brainstormer",
        "command": "opencode --agent brainstormer"
    },
    "implement": {
        "trigger": ["implementier", "code", "bau", "erstell"],
        "agent": "software-engineer",
        "command": "opencode --agent software-engineer"
    },
    "review": {
        "trigger": ["review", "prüf", "audit", "check"],
        "agent": "audit",
        "command": "opencode --agent audit"
    }
}
```

---

## 6. TTS - WANDA'S STIMME ✅ IMPLEMENTIERT

### 6.1 Verfügbare Stimmen (Piper)

| Stimme | Geschlecht | Stil | Empfohlen für |
|--------|------------|------|---------------|
| **Eva** ⭐ | Weiblich | Warm, professionell | Standard WANDA |
| Kerstin | Weiblich | Klar, freundlich | Alternative |
| Ramona | Weiblich | Sanft, ruhig | Entspannte Sessions |
| Karlsson | Männlich | Tief, sachlich | Klassischer Assistent |
| Thorsten | Männlich | Neutral, klar | Technische Infos |
| **Thorsten Emotional** | Männlich | Emotional, ausdrucksstark | JARVIS-like! |

### 6.2 Stimme wechseln

```bash
# Im Installer
python3 setup.py
# → Option "TTS CONFIGURATION" zeigt alle Stimmen

# Oder direkt in Config
# wanda.config.yaml → tts.voice: de_DE-thorsten_emotional-medium
```

### 6.3 Phase 2: XTTS v2 für Voice Cloning (geplant)

```python
# Später: Eigene JARVIS-Stimme trainieren
# tts/xtts_engine.py
class XTTSEngine:
    """SOTA TTS mit Voice Cloning."""

def __init__(self, speaker_wav: str = "wanda_sample.wav"):
        from TTS.api import TTS
        self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
        self.speaker_wav = speaker_wav  # Deine Custom-Stimme!
```

### 6.4 Charm & Persönlichkeit

Für JARVIS-artigen Charm mit Witz und Ironie:
1. **Thorsten Emotional** nutzen (ausdrucksstark)
2. **Wanda Prompts** in `conversation/wanda_prompts.py` anpassen
3. Später: **XTTS v2** mit geklonter Stimme die Emotionen kann

---

## 7. SELBSTVERBESSERUNG & LERNEN

### 7.1 Conversation Memory

```yaml
# ~/.wanda/memory/
conversations/
  2026-02-04-session-001.jsonl  # Alle Gespräche
learnings/
  preferences.yaml               # User-Präferenzen
  corrections.yaml               # Korrekturen merken
  successful_prompts.yaml        # Was gut funktioniert hat
```

### 7.2 Feedback Loop

```
User: "Wanda, das war nicht was ich meinte"
→ WANDA speichert Kontext + Korrektur
→ Nächstes Mal: Berücksichtigt Korrektur

User: "Perfekt, genau so!"
→ WANDA speichert erfolgreichen Prompt
→ Nutzt ähnliche Formulierungen wieder
```

### 7.3 Proaktive Vorschläge

```python
def suggest_improvements(self, context: dict) -> str:
    """Analyse Kontext und schlage Verbesserungen vor."""

    # Beispiele:
    # - "Du arbeitest oft spät - soll ich einen Reminder setzen?"
    # - "Dieses Projekt hat keine Tests - soll ich welche generieren?"
    # - "Der Code hat Security-Issues - Review starten?"
```

---

## 8. ZUKÜNFTIGE ERWEITERUNGEN

### 8.1 Claude Bot (geplant)
- Eigener Claude-basierter Agent
- Für komplexe Reasoning-Tasks
- Integration mit Anthropic API
- Spezialisiert auf: Architektur, Code-Review, Erklärungen

### 8.2 Bolt Bot (geplant)
- Schneller Task-Runner
- Für einfache, wiederkehrende Aufgaben
- Integration mit MCP Servers
- Spezialisiert auf: Automatisierung, Scripting

### 8.3 Multi-Modal (Vision)
- Screenshot-Analyse
- UI-Feedback
- "Wanda, was siehst du auf meinem Screen?"

### 8.4 Mobile Access
- Telegram Bot (bereits angelegt)
- Push Notifications via ntfy.sh
- Remote Projekt-Kontrolle

---

## 9. ROADMAP

### Phase 1: Foundation (JETZT)
- [x] Ollama Integration fixen
- [x] STT Anti-Halluzination
- [ ] Installer Hardware-Auto-Detection
- [ ] Installer Custom Model Support
- [ ] Testen & Stabilisieren

### Phase 2: Voice Quality (Woche 1)
- [ ] XTTS v2 evaluieren
- [ ] Jarvis-Stimme finden/trainieren
- [ ] TTS Engine austauschbar machen
- [ ] Latenz optimieren

### Phase 3: Agent Integration (Woche 2)
- [ ] OpenCode CLI Integration
- [ ] Agent-Routing via Voice
- [ ] Workflow-Trigger erweitern
- [ ] /ralph-loop via Voice starten

### Phase 4: Intelligence (Woche 3-4)
- [ ] Conversation Memory
- [ ] Feedback Loop
- [ ] Proaktive Vorschläge
- [ ] Selbstverbesserung

### Phase 5: Bots (Monat 2)
- [ ] Claude Bot Design
- [ ] Claude Bot Implementation
- [ ] Bolt Bot Design
- [ ] Bolt Bot Implementation

---

## 10. TECHNISCHE DETAILS

### 10.1 Dateien die geändert werden müssen

```
wanda-voice/
├── setup.py                    # Hardware-Detection, Custom Models
├── wanda.config.yaml           # Bereits gefixt
├── main.py                     # Bereits gefixt (ollama.enabled check)
├── stt/faster_whisper_engine.py # Bereits gefixt (Anti-Halluzination)
├── tts/
│   ├── piper_engine.py         # Bestehend
│   └── xtts_engine.py          # NEU: SOTA TTS
├── adapters/
│   ├── ollama_adapter.py       # Erweitern: Proaktive Vorschläge
│   └── opencode_adapter.py     # NEU: Agent-Orchestrierung
├── conversation/
│   ├── intelligence.py         # Erweitern: Agent-Workflows
│   └── memory.py               # NEU: Conversation Memory
└── config/
    └── hardware.py             # NEU: Hardware Detection
```

### 10.2 Neue Dependencies

```
# requirements.txt Ergänzungen
TTS>=0.22.0          # Coqui XTTS v2
torch>=2.0.0         # Für XTTS
soundfile            # Audio I/O
```

### 10.3 MCP Server Integration

WANDA MCP + Plugin Inventory (SSOT):
- docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md

---

## 11. QUICK START (nach Fixes)

```bash
# 1. Wanda starten
cd ~/Schreibtisch/Work-OS/10_LTL_Core/12_Internal_Tools/12.06_Wanda_Agentic-System/wanda-voice
./wanda

# 2. Oder Setup neu ausführen für Ollama-Modell-Auswahl
python3 setup.py

# 3. Voice Commands testen
# [RIGHT CTRL] → "Hallo Wanda, wie geht es dir?"
# [RIGHT CTRL] → "Starte ein Brainstorming für eine neue App"
# [RIGHT CTRL] → "Wanda, Pause" (Sleep Mode)
```

---

**Letzte Aktualisierung:** 2026-02-04 05:25:00
**Nächster Review:** Nach Phase 1 Completion

---

## CHANGELOG

- **2026-02-04 05:25** - Hardware Detection (VRAM+RAM), 7 Tiers, 6 deutsche Stimmen, `wanda-voice` Command
- **2026-02-04 05:08** - Initial Plan erstellt
