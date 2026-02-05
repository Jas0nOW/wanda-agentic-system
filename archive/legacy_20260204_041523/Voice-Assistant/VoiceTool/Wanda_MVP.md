# Wanda – Voice Wrapper für Gemini CLI (MVP) 🎙️🖥️

> **Ziel:** Im Terminal **sprechen statt tippen** – mit **Bestätigung vor dem Senden**, **Prompt-Optimierung** (Brainstorm/Research/Task) und **Vorlesen** der Antworten.  
> **Prio:** 1) Gemini CLI → 2) OpenCode (Adapter).

---

## 0) MVP

1) **Send-Confirmation**: Transkript wird **vor dem Senden** angezeigt (Edit/Redo/Cancel).  
2) **Prompt-Preprocessor**: automatische **Intent-Erkennung** + **Prompt-Verbesserung** (z. B. Brainstorm-Modus).  
3) **Trigger → Tooling/Agent-Features**: Wanda reagiert auf kurze Trigger („mach Research“, „brainstorm“, „fix bug“) und setzt passende Anweisungen/Kommandos.  
4) **Hardware-Wizard**: Auto-Detect oder Profilwahl → **STT/TTS Empfehlung** + manuelles Override.

---

## 1) Zielbild (User Experience)
### 1.1 Interaktionsloop (Default)
1. Hotkey/Trigger aktiviert Aufnahme (hold oder toggle)
2. Audio wird aufgenommen (mit optionalem *Start/Stop*-Sound)
3. STT transkribiert → Text erscheint im Terminal
4. **Bestätigung vor Senden**  
   - `ENTER` = Senden  
   - `e` = Edit (Text im Editor/Inline)  
   - `r` = Redo (neu aufnehmen)  
   - `c` = Cancel
   - Optinal Stimmen Bestätigung und bearbeitung
5. Prompt-Preprocessor optimiert den Text (Intent + Format)
6. Übergabe an Gemini CLI
7. Antwort:
   - Volltext im Terminal
   - TTS liest (Kurz- oder Vollfassung)
8. Loop

### 1.2 Modi (Intent)
Wanda kennt **Modi**, die per Triggerwort oder Auto-Intent gesetzt werden:

- **Brainstorm**: Ideen, Optionen, keine „Task-Liste“ unless requested
- **Research**: Quellen sammeln, vergleichen, nächste Schritte
- **Build/Fix**: konkrete Schritte/Kommandos, Debug-Plan
- **Dictation**: nur transkribieren (kein LLM)
- **Command (später!)**: lokale Shell-Kommandos ausführen **nur mit Confirm + Allowlist** (Non-Goal fürs MVP)

---

## 2) Scope ✅ / Non-Goals ❌
### Muss (MVP)
- Voice Input → STT → **Confirm** → Prompt-Preprocess → Gemini CLI → TTS
- Terminal zeigt immer vollständigen Text (kein Voice-only)
- Linux-first (Pop!_OS/COSMIC/Wayland) – aber portierbar
- Hardware-Wizard (Auto-Detect oder Profilwahl) + Empfehlung + Override
- Basic History (letzte N Turns) für Konversationsfluss (ohne Gemini CLI “Memory” vorauszusetzen)

### Soll (direkt danach)
- Streaming: Antwort während Ausgabe chunkweise vorlesen (fühlt sich „live“ an)
- Push-to-talk global (Wayland-friendly), falls verfügbar
- Optional: „Native Audio“-Pfad (ein Modell statt STT+TTS) über Gemini Live API (später)

### Nicht im MVP
- Automatisches lokales Command-Execution ohne Confirm
- Voller Multi-Agent-Orchestrator (Claude/Codex/etc.) – kommt im großen Projekt

---

## 3) Architektur 🧩 (komponentisiert, adapterfähig)

```
[Trigger/Hotkey]
   |
[Recorder] -> audio.wav
   |
[STT Engine] -> transcript.txt
   |
[Confirm + Edit]
   |
[Prompt Preprocessor] -> final_prompt.txt
   |
[LLM Adapter] -> response.txt (+ raw stdout/stderr)
   |
[TTS Engine] -> speaker out
```

### Komponenten (Module-Interface)
- `trigger/`: focus_hotkey, (später: global shortcuts portal / keyd)
- `audio/`: record, device selection, level meter (optional)
- `stt/`: engines (faster-whisper, whisper.cpp, remote)
- `preprocess/`: intent detect, rewrite, guardrails
- `adapters/`: gemini_cli, opencode (später), dry-run
- `tts/`: piper (lokal), remote (optional)
- `ui/`: terminal UI (confirm/edit), minimal curses/tty
- `config/`: wizard, profiles, persistence
- `security/`: sandbox flags, allowlist policy, redaction

---

## 4) Gemini CLI Integration (warum Session-Mode wichtig ist)
Gemini CLI ist nicht nur „ein Prompt rein, Text raus“, sondern ein **Agent**:  
- nutzt einen ReAct-Loop
- hat **Built-in Tools**
- kann lokale/remote **MCP Server** einbinden citeturn2search7turn2search19turn2search2

### Zwei Integrationsmodi
**A) Stateless (einfach)**
- pro Turn: Prozess starten → Prompt senden → Output lesen → Prozess beenden
- Wanda verwaltet selbst den Kontext (History)

**B) Session (empfohlen für “Live”-Gefühl)**
- Wanda startet Gemini CLI in einer PTY (Pseudo-Terminal)
- sendet Prompts in dieselbe Session (Tools/Slash-Commands bleiben verfügbar)
- fühlt sich am nächsten an “Live Voice” an

**MVP Empfehlung:** Session-Mode als Default, Stateless als Fallback.

---

## 5) Prompt-Preprocessor (Intent → Rewrite → Guardrails)
### 5.1 Ziele
- Aus „gesprochener Sprache“ wird ein **klarer Arbeitsauftrag**
- „Mini-Trigger“ steuern Verhalten (Brainstorm/Research/Build)
- Sicherheits- & UX-Gates: nichts wird heimlich ausgeführt oder gesendet

### 5.2 Pipeline
1) **Normalize**
   - Füllwörter entfernen (optional), Satzzeichen ergänzen
2) **Intent Detect**
   - Regel-basiert (MVP): Keywords / einfache Heuristik
   - Optional später: Mini-LLM-Classifier (z. B. Gemini Flash)
3) **Rewrite**
   - Templates pro Intent (siehe unten)
4) **Guardrails**
   - Sensitive Strings redaction (Tokens, Keys, Pfade optional maskieren)
   - Hard stop bei “execute/delete/format” → Confirm-Dialog erzwingen

### 5.3 Trigger-Regeln (MVP-Heuristik)
- Wenn User sagt: „brainstorm“ / „Ideen“ / „nur brainstormen“ → `mode=brainstorm`
- Wenn User sagt: „recherchiere“ / „mach research“ / „finde Quellen“ → `mode=research`
- Wenn User sagt: „fix“ / „bug“ / „error“ / „stacktrace“ → `mode=buildfix`
- Wenn User sagt: „diktieren“ → `mode=dictation` (kein LLM)

### 5.4 Rewrite-Templates (Beispiel)
**Brainstorm**
- „Du bist ein Brainstorm-Partner. Liefere Optionen + Tradeoffs. Keine Aufgabenliste, außer ich frage danach.“

**Research**
- „Finde verlässliche Quellen, nenne Links und fasse zusammen. Gib danach konkrete Next Steps.“

**Build/Fix**
- „Stelle zuerst Diagnosefragen nur wenn nötig, sonst gib direkte Schritte, Kommandos und DoD.“

---

## 6) STT/TTS – Default-Stack & Optionen 🔊
### 6.1 STT (lokal)
**Option 1: faster-whisper (CTranslate2)**
- schnell, GPU/CPU, quantization, lädt Modelle vom Hub citeturn0search6

**Option 2: whisper.cpp**
- sehr portable CLI, gut als “single binary”-Pfad citeturn0search6

**Turbo / large-v3-turbo**
- es gibt „large-v3-turbo“ Varianten, inkl. CTranslate2-Konvertierungen citeturn0search10turn1search6  
- bei whisper.cpp existieren quantisierte Artefakte (z. B. large-v3-turbo q5_0 ~1.17 GB) citeturn1search10  
  *(Hinweis: Größe hängt stark von Quantisierung/Format ab.)*

### 6.2 TTS (lokal)
**Piper (piper1-gpl / piper-tts)**
- lokal, schnell, viele Stimmen, pip-installable citeturn0search3turn0search15

### 6.3 Alternative (später): “Native Audio” statt STT+TTS
Google bietet eine Live API für low-latency Voice/Video, inkl. nativer Audio-Modelle (Gemini 2.5 Flash Native Audio). citeturn1search5turn1search1turn0search4  
Das ist optional (Remote), kann aber „echtes Live Voice“-Feeling bringen.

---

## 7) Hardware-Wizard & Empfehlungen ⚙️
### 7.1 Profile
- **S (Low)**: CPU-only, wenig RAM
- **M (Mid)**: starke CPU, genug RAM
- **G (GPU)**: GPU verfügbar (z. B. RTX 3070)

### 7.2 Auto-Detect (MVP)
- VRAM: `nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits`
- RAM: `/proc/meminfo`
- Threads: `nproc`

### 7.3 Empfehlung (MVP-Regeln)
- **S**: whisper.cpp `base`/`small` + piper
- **M**: faster-whisper `small`/`medium` (CPU) oder whisper.cpp `small/medium`
- **G**: faster-whisper `medium` oder `large-v3-turbo` testen (Quality/Latenz abwägen) citeturn0search6turn0search10
- Immer: manuelles Override

---

## 8) Wayland Hotkeys / Push-to-talk Realität ⚠️
Unter Wayland sind globale Hotkeys absichtlich eingeschränkt (Security).  
Es gibt Portals/Ansätze für globale Shortcuts, aber Unterstützung hängt vom Desktop/Portal-Backend ab. citeturn1search4turn1search12turn1search11

**MVP Entscheidung (robust):**
- Default: **PTT nur bei Terminal-Fokus** (funktioniert immer)
- Optional später:
  - Global Shortcuts Portal (wenn DE es sauber unterstützt)
  - System-Layer Workaround (z. B. keyd/evdev/uinput) – nur als optionaler “Power User”-Pfad

---

## 9) Security & Sandbox 🔒 (wichtig bei Agent-Tools)
Gemini CLI ist ein Agent mit Tools/Commands/MCP – das ist mächtig, aber Sicherheitsrisiko bei untrusted Inputs. citeturn2search7turn2search2

Es gab reale Angriffe via Prompt Injection + Allowlist/UX-Probleme, die zu stiller Command-Ausführung führen konnten (Tracebit). citeturn2search0turn2search5turn2news39

**Wanda Policy (MVP)**
- Kein “YOLO/Auto-Run” standardmäßig
- Confirm-Gates für alles, was nach “execute/run/delete” klingt
- Optional: Gemini CLI in Sandbox laufen lassen (Docker/Podman), wenn Tools aktiv sind citeturn2news39
- Log Redaction (Keys/Tokens maskieren)

---

## 10) Konfiguration 📄
### 10.1 `wanda.config.yaml` (Vorschlag)
```yaml
mode: chat                        # chat | dictation
intent: auto                      # auto | brainstorm | research | buildfix
trigger:
  type: focus_hotkey              # focus_hotkey | global_portal (later) | keyd (later)
  key: rightctrl
audio:
  backend: pipewire               # pipewire | alsa | portaudio
  sample_rate: 16000
  max_seconds: 15
stt:
  engine: faster-whisper          # faster-whisper | whisper.cpp | remote
  model: medium                   # tiny|base|small|medium|large-v3|large-v3-turbo
  device: cuda                    # cuda|cpu
confirm:
  enabled: true
  edit_mode: inline               # inline | $EDITOR
preprocess:
  enabled: true
  rewrite: template               # template | llm (later)
tts:
  engine: piper
  voice: de_DE-thorsten           # example
output:
  speak: true
  speak_style: short              # short|full
history:
  max_turns: 12
  persist: false
adapters:
  target: gemini_cli              # gemini_cli | opencode (later)
security:
  sandbox: off                    # off | docker | podman
  redact_secrets: true
```

### 10.2 Wizard (Start-Flow)
1) Audio device wählen (Test: “hörst du mich?”)
2) Profil wählen (S/M/G) oder Auto-Detect
3) Empfehlung anzeigen (STT/TTS)
4) Confirm aktivieren (default: on)
5) Start “Session-Mode” oder “Stateless” (default: Session)

---

## 11) Milestones & DoD 🧱 (AI-executable)
### M0 – Voice Loop Proof
**Tasks**
- Recorder + STT “Hello test”
- TTS “Hello test”
- Gemini Adapter (stateless) “ping” test

**DoD**
- 3/3 laufen auf Zielsystem, ohne manuelle Eingriffe

### M1 – MVP v2 “Terminal Voice Chat”
**Tasks**
- Session-Mode PTY Integration
- Confirm/Edit UI
- Intent Detect + Template Rewrite
- Speak short/full mode

**DoD**
- 10-Min Gespräch möglich (>= 20 Turns), keine Abstürze, Latenz akzeptabel

### M1.1 – Hardware Wizard
**Tasks**
- Auto-Detect + Profil-UI
- Empfehlung + Override
- “doctor” command (Audio/STT/TTS/Gemini smoke tests)

**DoD**
- Frischer Rechner: `wanda doctor` gibt klare Hinweise, Setup < 5 Minuten

### M2 – Gemini CLI nathlos

- Gemini Cli Agenten im Terminal standard aufrufbar. Ziel ist es mehrere Agenten steuern zu können über das neue "Gemini-3-flash-Preview" Model im Terminal. Dadurch kann man mehrere Aufgaben agentisch und einfach verteilen.

### M3 – OpenCode Adapter
**Tasks**
- Adapter Interface implementieren
- OpenCode als Target
- Regression Tests

**DoD**
- Gleiche Wanda Config läuft mit `target=opencode`

---

## 12) Optional: Roadmap Richtung “großes Projekt” 🚀
### 12.1 Orchestrator Mode (Gemini 3 Flash)
- “Flash” als Brainstorm/Orchestrator, delegiert schwere Tasks
- Gemini 3 Flash ist als Speed/Frontier-Speed Modell positioniert citeturn0search8turn0search0

### 12.2 Externe Agenten (Deep Research/Coding)
- Delegation an spezialisierte Modelle (Claude/Codex/Gemini Pro)
- OhMyOpencode/OpenCode/MiCode/Opencode-Orchestrator Agenten als Basis (in getrennten Adaptern)
- Gemini Cli Agenten im Terminal

*(Nicht MVP, aber die Schnittstellen sind vorbereitet.)*

---

## 13) Quellen / Research Links
- Gemini 3 Flash (Google Blog): https://blog.google/products-and-platforms/products/gemini/gemini-3-flash/ citeturn0search8
- Gemini Model Lifecycle / Deprecations: https://ai.google.dev/gemini-api/docs/deprecations citeturn0search0
- Gemini CLI (Google Cloud Docs): https://docs.cloud.google.com/gemini/docs/codeassist/gemini-cli citeturn2search7
- Gemini CLI MCP / Tools API: https://geminicli.com/docs/tools/mcp-server/ citeturn2search2
- Gemini CLI Customization (Codelab, GEMINI.md): https://codelabs.developers.google.com/gemini-cli-hands-on citeturn2search14
- Tracebit Gemini CLI Hijack: https://tracebit.com/blog/code-exec-deception-gemini-ai-cli-hijack citeturn2search0
- Live API (Gemini Developer API): https://ai.google.dev/gemini-api/docs/live citeturn1search5
- Vertex Live API (2.5 Flash Native Audio): https://docs.cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash-live-api citeturn1search1
- faster-whisper: https://github.com/SYSTRAN/faster-whisper citeturn0search6
- whisper.cpp artefacts: https://huggingface.co/ggerganov/whisper.cpp/tree/main citeturn1search10
- Piper TTS: https://github.com/OHF-Voice/piper1-gpl citeturn0search3

