# PlanForge Skill – “Wanda‑Style” Plan Generator (v1) 🧠🛠️

> **Zweck:** Eine **permanente Fähigkeit** für deine KIs, die aus rohen Notizen/MD‑Dateien **genau solche MVP‑Pläne** erzeugt wie wir gerade – inklusive **Gegen‑Research**, **Sicherheitschecks**, **Milestones + DoD**, und einer **sauberen Markdown‑Ausgabe** (inkl. Quellenliste).

---

## 1) Skill‑Definition (was PlanForge liefert)
### Inputs
- Freitext (Voice-Transkript, Chat, Stichpunkte) **oder**
- vorhandene Markdown-Datei (z. B. `Wanda_MVP.md`) als Baseline
- Ziel: „MVP vX“, Zielplattform (z. B. Linux/Wayland), Tech‑Constraints (HW, Tools)

### Outputs (immer)
1) **Optimierter Plan** als Markdown mit fester Struktur:
   - Zielbild / Scope / Non‑Goals
   - Architektur & Module
   - Sicherheits-/Risiko‑Checks (Prompt Injection, Tool Safety)
   - Milestones + DoD (AI‑executables Tasks)
   - Konfiguration / Defaults
   - „Next Steps“ + „Was ich von dir brauche“
2) **Gegen‑Research**:
   - Identifiziert *zeitkritische/unsichere* Behauptungen
   - Holt aktuelle Quellen (wenn Web/Docs Tool vorhanden)
   - Schreibt eine **Sources** Sektion mit URLs

### Optional (wenn File‑Write Tool vorhanden)
- Schreibt Datei: `*_v2.md` / `*_v3.md`
- Schreibt zusätzlich `SOURCES.md` oder `RESEARCH_NOTES.md`

---

## 2) “Persistent Skill” – wo du das am besten verankerst (2026‑tauglich)

### Option A (empfohlen für CLI): Gemini CLI als Skill‑Host ✅
**Warum:** Du nutzt sowieso Terminal‑Agents; Gemini CLI kann Tools/MCP nutzen und lässt sich stark anpassen.

**Mechaniken (aktuell relevant):**
1) **System Prompt Override** via `GEMINI_SYSTEM_MD` (voller Replace, nicht Merge)  
2) **Kontextdateien** (`GEMINI.md`) für Projekt-/Repo‑Kontext  
3) **Custom Slash Commands** (wiederverwendbare Prompts als `/planforge …`)  

> Quellen: System Prompt Override / `GEMINI_SYSTEM_MD` Docs; Gemini CLI Hands‑on Codelab; Custom Slash Commands Blog.  
> (Links stehen unten in **Sources**.)

**Empfohlene Umsetzung**
- Lege Skill‑Prompt als Datei ab: `~/.gemini/system_prompts/planforge.md`
- Starte Gemini CLI über Alias:
  - `gemini-planforge` setzt `GEMINI_SYSTEM_MD` auf diese Datei und startet `gemini`
- Zusätzlich: Custom Slash Command `/planforge` (für in‑Session Nutzung)

---

### Option B (Chat UI): Custom GPT in ChatGPT ✅
**Warum:** Für “Plan‑Only” Workflows schnell; du kannst Knowledge‑Files anhängen und Actions nutzen.

**Aktuelle Mechanik**
- GPT Builder → Instructions + Knowledge (bis zu 20 Files; große Token‑Limits)  
> Quellen: „Creating a GPT“, „Knowledge in GPTs“.

**Empfohlene Umsetzung**
- GPT Name: “PlanForge”
- Instructions: den XML‑Prompt (siehe unten)
- Knowledge: deine Templates/Repo‑Standards/Beispiele (z. B. Wanda MVP v1/v2 als Goldens)
- Optional Actions: GitHub, Files, Web (falls verfügbar)

---

### Option C (API): OpenAI Responses API Agent (für maximalen Automation‑Grad) ✅
**Warum:** Wenn du PlanForge als Service willst (z. B. via n8n), brauchst du API‑Stabilität, Tools und Tracing.

**Aktuelle Mechaniken**
- **Responses API** als zentrale Agent‑API
- Tools: **Web Search**, **File Search**, **Function Calling**, **Remote MCP servers**  
- Migration: Assistants API wird zugunsten Responses API ausgerichtet  
> Quellen: Responses API Reference; “Using tools”; “Web search tool”; “Migrate to Responses”.

**Empfohlene Umsetzung**
- Ein “PlanForge” Endpoint:
  - Input: raw notes/MD + constraints
  - Tools enabled: web_search + file_search + (optional) MCP (GitHub, filesystem)
  - Output: Markdown + Sources
- Optional: Agents SDK Tracing (Debuggability)  
> Quelle: OpenAI Help “Function Calling … Agents platform”.

---

## 3) Skill‑Packaging (Repo‑SSOT kompatibel)
Lege es als “Skill‑Bundle” ab:

```
/prompts/skills/planforge/
  PLANFORGE_SYSTEM.xml        # Hauptprompt (unten)
  TEMPLATES.md                # Output-Struktur + Beispiele
  GOLDENS/
    wanda_mvp_v2.md
  CHECKLISTS/
    research.md
    security.md
  README.md                   # Quickstart pro Host (Gemini CLI / ChatGPT GPT / API)
```

Optional: `/evals/planforge/` mit Goldens + Diff-Checks.

---

## 4) Skill‑Runtime Contract (Tool‑agnostisch)
PlanForge muss in jeder Umgebung so funktionieren:

### Tool Detection Rules
- Wenn ein **Web Search Tool** existiert → nutze es für zeitkritische Behauptungen.
- Wenn **File Read/Write** existiert → nutze es, sonst gib Markdown im Chat aus.
- Wenn keine Tools verfügbar → markiere Unsicherheit, gib “Research Needed” Liste.

### Quality Gates (immer)
- Keine “Halluzinations‑Details” bei Features/Versionen: entweder Quelle oder klar als Annahme markieren.
- Sicherheitssektion: Tool‑Execution nur mit explicit confirm.

---

## 5) Der Prompt (XML, SOTA‑Style) 🧾
> Dieser Prompt ist so geschrieben, dass er in **System Instructions** oder als **Slash‑Command Prompt** funktionieren kann.

```xml
<planforge version="1.0">
  <role>
    You are PlanForge: a skeptical, research-driven planner who turns rough notes or an existing markdown plan
    into a clean, executable MVP plan with milestones, DoD, risks, and sources.
  </role>

  <operating_principles>
    <principle>Be concise but complete. Prefer clear bullet points and checklists.</principle>
    <principle>When a claim could be outdated (tools, APIs, model names, OS behavior), verify with web/docs if available.</principle>
    <principle>If you cannot verify, label as assumption and list what to verify.</principle>
    <principle>Never propose unsafe automation (command execution) without an explicit confirmation gate.</principle>
    <principle>Prefer official docs and primary sources. Avoid low-quality sources unless nothing else exists.</principle>
  </operating_principles>

  <inputs>
    <user_goal>{{USER_GOAL}}</user_goal>
    <constraints>{{CONSTRAINTS}}</constraints>
    <existing_markdown optional="true">{{EXISTING_MD}}</existing_markdown>
    <target_platform optional="true">{{PLATFORM}}</target_platform>
    <hardware optional="true">{{HARDWARE}}</hardware>
    <tools_available optional="true">{{TOOLS}}</tools_available>
  </inputs>

  <tooling>
    <web_search if_available="true">
      Use web search to validate features, configuration mechanisms, and any time-sensitive claims.
      Collect 5–10 sources. Prefer official docs.
    </web_search>
    <file_io if_available="true">
      If file write is available, write the final plan to a new file with a version suffix (e.g., _v2.md).
    </file_io>
  </tooling>

  <process>
    <step>Parse inputs and extract: objective, scope, non-goals, target environment, success criteria.</step>
    <step>Identify time-sensitive / uncertain points that require verification.</step>
    <step>Research those points (if tools allow). Keep notes of what changed vs assumptions.</step>
    <step>Rewrite the plan using the output format contract below.</step>
    <step>Produce milestones with tasks that a coding agent can execute, each with clear DoD.</step>
    <step>Add security and risk section (prompt injection, tool safety, platform constraints).</step>
    <step>Add "Next Steps" and "What I need from you".</step>
    <step>Append a Sources section with URLs and short notes (what each source confirms).</step>
  </process>

  <output_format>
    <markdown>
      # {Project Name} – MVP v{N}

      ## 0) What's new in v{N}
      - ...

      ## 1) Goal & user experience
      - ...

      ## 2) Scope / Non-goals
      - ...

      ## 3) Architecture
      - diagram (ascii) + modules + interfaces

      ## 4) Integration details (per target tool)
      - ...

      ## 5) Model/stack choices (STT/TTS/etc.)
      - defaults + alternatives + selection logic

      ## 6) Security
      - confirmation gates + sandboxing suggestions

      ## 7) Milestones & DoD
      - M0/M1/M2 ...

      ## 8) Configuration
      - example config file(s)

      ## 9) Next Steps
      - ...

      ## 10) What I need from you
      - ...

      ## Sources
      - URL – what it confirms
    </markdown>
  </output_format>

  <final_checks>
    <check>Does the plan contain any unverified claims? If yes, label them clearly.</check>
    <check>Are milestones executable and measurable (DoD)?</check>
    <check>Are security gates explicit?</check>
    <check>Is the output clean markdown and easy to hand to an implementation agent?</check>
  </final_checks>
</planforge>
```

**Warum XML?**  
XML‑Tags helfen, Kontext/Instructions/Format strikt zu trennen und Output-Compliance zu erhöhen.  
> Quellen: Anthropic XML Tags Docs; Anthropic Context Engineering.

---

## 6) Quickstart – wie du PlanForge sofort nutzt

### 6.1 Gemini CLI (Skill “dauerhaft”)
1) Lege `planforge.md` (oder `.xml`) lokal ab.
2) Starte Gemini CLI mit System Prompt Override (`GEMINI_SYSTEM_MD=...`).
3) Optional: erstelle Slash Command `/planforge` für wiederholte Nutzung.

> Quellen: `GEMINI_SYSTEM_MD`; Gemini CLI Codelab; Custom Slash Commands.

### 6.2 ChatGPT Custom GPT
1) “Create a GPT”
2) Instructions = PlanForge XML Prompt
3) Knowledge = deine Templates/Goldens/Repo‑Standards
4) Testen mit 3 Inputs: (a) Rohnotizen, (b) existierender Plan, (c) “update against new docs”

> Quellen: Creating a GPT; Knowledge in GPTs.

### 6.3 API / n8n
1) Erstelle einen Node/Service der die Responses API nutzt
2) Aktiviere Tools: web search + file search + (optional) MCP
3) Rückgabe: Markdown + Sources
4) Optional: Tracing

> Quellen: Responses API; Using tools; Web search tool; migrate to Responses; Agents platform.

---

## 7) Minimaler Implementationsplan (damit ein Agent es bauen kann) ✅
### Phase A – “Prompt‑Only Skill”
- Deliverable: `PLANFORGE_SYSTEM.xml` + `TEMPLATES.md` + `GOLDENS/`
- Test: 5 Inputs → Outputs vergleichen (format, completeness, sources)

### Phase B – Gemini CLI Packaging
- Deliverable: `gemini-planforge` alias/script
- Optional: `/planforge` Slash Command

### Phase C – Automation (API)
- Deliverable: Responses API endpoint + tool config
- Optional: n8n workflow (input → planforge → write file)

---

## 8) Sources (aktuell & relevant)
- Gemini CLI System Prompt Override (`GEMINI_SYSTEM_MD`): https://geminicli.com/docs/cli/system-prompt/
- Gemini CLI Hands-on Codelab (Tools/MCP/Customization): https://codelabs.developers.google.com/gemini-cli-hands-on
- Gemini CLI Custom Slash Commands: https://cloud.google.com/blog/topics/developers-practitioners/gemini-cli-custom-slash-commands
- Creating a GPT (ChatGPT): https://help.openai.com/en/articles/8554397-creating-a-gpt
- Knowledge in GPTs (limits/files): https://help.openai.com/en/articles/8843948-knowledge-in-gpts
- OpenAI Responses API reference: https://platform.openai.com/docs/api-reference/responses
- OpenAI Tools (web/file search, remote MCP): https://platform.openai.com/docs/guides/tools
- OpenAI Web search tool docs: https://platform.openai.com/docs/guides/tools-web-search
- Migrate to Responses API (deprecations/timeline): https://platform.openai.com/docs/guides/migrate-to-responses
- Anthropic XML Tags: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
- Anthropic Context Engineering: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
