# Notizen.md — Wanda / OpenCode Stack (SSOT)
Stand: 2026-02-04 (Europe/Berlin)

Ziel:
- Keine Infos verlieren ✅
- Aktuelle Probleme + Ursachen-Hypothesen + Fix-Strategien dokumentieren
- Backlog/Tasks so formulieren, dass sie 1:1 in Issues / Agent-Briefs gehen
- Research-Notes direkt an passenden Stellen ergänzen (mit [Sx]-Markern → Quellen unten im Chat)

---

## 0) Kurz-Lagebild 🧭
Wir bauen eine stabile OpenCode-Basis + Plugin-Stack:
- Core: OpenCode
- Plugins: oh-my-opencode@3.2.1, micode@latest (+ optional Orchestrator)
- Zusätzlich: opencode-context-analysis@latest, opencode-shell-strategy@latest, opencode-notifier@latest
- Zielzustand: Keine doppelten Agenten, keine stillen Konflikte, cross-OS lauffähig, Installer/Update-UX sauber.

---

## 1) Aktuelle & bekannte Probleme (Incidents / Risiken)

### P0 — Agenten-Overlaps / Config-Overrides werden „zurückgesetzt“
Symptom:
- Bei oh-my-opencode und micode ist unklar, ob System-/Plugin-Agenten sauber deaktiviert/umgestellt werden können.
- Änderungen (z. B. Agent-Namen/Modelle) scheinen beim Start wieder rückgängig gemacht zu werden.

Impact:
- Unvorhersehbares Routing
- Token-/Zeitverschwendung durch doppelte Rollen
- Debugging schwer, weil „drift“ (Config ≠ Laufzeit)

Research-Note:
- oh-my-opencode unterstützt explizit „Agents Configuration“ inkl. enabled/disabled pro Agent + replace_plan-Mechanik. [S1]
- Es gibt Issues, dass bestimmte Agent-Overrides ignoriert werden/Defaults gewinnen. (Hinweis: config keys/position kann entscheidend sein). [S12][S13]

To-Do (Fix-Strategie):
1) Standardisieren, WO konfiguriert wird (global vs project) und in welcher Reihenfolge geladen wird:
   - Plugin Load Order: global opencode.json → project opencode.json → global plugins dir → project plugins dir. [S2]
2) Reproduzierbaren „Config-Lock“ einführen:
   - Eine einzige „Source of Truth“ pro Layer:
     - Core (opencode.json / opencode.jsonc)
     - oh-my-opencode.json
     - micode.json
   - Keine Duplikate derselben Agent-Definition in mehreren Files.
3) Prüfen, ob Overwrite/Rewrite beim Start passiert durch:
   - Directory-injector Hooks (oh-my)
   - Auto-Generators (micode fragments/compaction)
   - Projekt-spezifische Agent-Injection

---

### P0 — micode verursacht (scheinbar) Anthropic Credential Errors
Symptom:
- „micode@latest“ verändert scheinbar Anthropic API → Credential Fehler bei Anthropic-Modellen.

Wichtig: Erst isolieren, bevor wir micode „schuldig“ machen.
Research-Notes:
- micode ist primär ein Workflow-/Hook-/Agent-Framework; liest Default-Modell aus opencode.json und erlaubt per-agent overrides in micode.json. [S6]
- „This credential is only authorized for use with Claude Code …“ ist ein wiederkehrender Fehler, der auch ohne micode vorkommt und versions-/auth-bezogen sein kann (OpenCode/Anthropic auth). [S7][S8]

Hypothesen (geordnet):
H1) OpenCode/Anthropic Provider/Auth Plugin Version-Bug (z. B. Regression) → Credentials brechen unabhängig von micode.
H2) Claude Code OAuth / Subscription-Creds sind für Dritt-Requests eingeschränkt → OpenCode darf sie nicht so nutzen (je nach Endpoint/Token). [S8]
H3) micode triggert andere Provider-/Model-Resolution (falsches provider/model Format) → Auth-Pfad ändert sich.
H4) micode + oh-my zusammen erzeugen doppelte Provider-Konfig oder überschreiben model-id.

Isolations-Testplan (minimal, deterministisch):
1) Snapshot: aktuelle Configs + auth.json sichern (read-only Kopie).
2) Matrix-Test (je 1 kurzer Request „/models“ + 1 Prompt):
   A) OpenCode ohne Plugins
   B) nur micode
   C) nur oh-my-opencode
   D) micode + oh-my
3) Pro Test: Log-Pfad/Fehlertext sichern; Ergebnis in Tabelle.
4) Wenn Fehler erst bei B/D: micode config resolution checken (provider/model Syntax). [S6]

---

### P0 — BunInstallFailedError / Multi-OS „Plugin-Verlust“-Risiko
Symptom:
- Bun failed / BunInstallFailedError beim Start/bei Plugin-Install.
- Explizit betroffen (dein Stack):
  - opencode-context-analysis@latest
  - opencode-shell-strategy@latest
  - opencode-notifier@latest
- Du brauchst Multi-OS Lösung (Cosmic Wayland | Linux | Windows | macOS) ohne Plugins zu verlieren.

Research-Notes:
- OpenCode nutzt bun install für Plugin/Dependency Install bei Startup (wenn package.json im config dir). [S2]
- Windows: „Support for installing OpenCode on Windows using Bun is currently in progress“ → Risiko erhöht. [S5]
- BunInstallFailedError wird real u. a. für opencode-notifier gemeldet. [S9]
- Offizielles Troubleshooting: Plugins deaktivieren / Cache löschen / neu aufbauen. [S10]

Workaround-Strategie (Design-Ziel: „No Surprises“):
1) Version Pinning (statt @latest) für kritische Plugins (vor allem auf Windows/macOS).
2) „Offline/Cache-stable“ Install-Flow:
   - definierte Cache-Pfade
   - definierte „Update Script“ Schritte (Cache + node_modules Reset)
3) Netzwerk-/Proxy Awareness:
   - BunInstallFailedError oft proxy/registry/cert-bedingt → in Installer aufnehmen: Diagnose + Hinweis + Retry.
4) Cross-OS: bevorzugt OpenCode via offiziellen Installer/Release-Binary (nicht bun global install) auf Windows. [S5]

---

### P1 — Google Modelle via „normalem Google OAuth“ (nicht Antigravity) → API Probleme
Symptom:
- Bei Google-Modellen über normalen OAuth (CLI Modelle, nicht Antigravity) treten API-Probleme auf.
- Unklar ob Fallback über Plugin wirklich greift.

Research-Notes:
- Provider-/Credential Handling: /connect speichert keys in ~/.local/share/opencode/auth.json; Provider-Konfig in opencode.json. [S4]
- Antigravity Auth Plugins existieren; Plugin-Updates sind nicht automatisch → Cache Clear nötig, sonst bleibt man „stuck“ auf broken Versionen. [S11]
- Ökosystem listet Google Antigravity OAuth Plugins explizit. [S14]

To-Do:
1) Klar definieren „Primary Google Path“:
   - Entweder: Gemini via regulären Provider (/connect google) ODER Antigravity OAuth Plugin als Standard.
2) Verifizieren, ob „Fallback“ technisch wirklich greift:
   - Wenn primary provider failt: wird model automatisch zu Antigravity umgeroutet?
   - Oder müssen wir das explizit in Agent/Router-Logic abbilden?

---

## 2) Merged Notizen → Epics / Tasks (Issue-ready)

### EPIC A — Docs/UX: AI_INSTALLATION.md als „One True Install Doc“
Ziel:
- README.md enthält nur eine 2-Zeilen-Kurzanweisung → verweist auf AI_INSTALLATION.md
- AI_INSTALL_PROMPT.md wird ultra-kurz (max. 3 Zeilen) und delegiert komplett an AI_INSTALLATION.md
- Nutzer können Installation:
  1) manuell (curl etc.)
  2) automatisch (über CLI-Agenten/Prompt)
- inkl. Edge Cases + Fixes + „create Issue“ wenn nichts geht

Deliverables:
- /README.md (kurz)
- /docs/AI_INSTALLATION.md (lang, vollständig, troubleshooting-first)
- /docs/AI_INSTALL_PROMPT.md (3 Zeilen, „run this prompt“)
- Issue-Template „Installation Problem“ + Log-Anleitung

Akzeptanzkriterien:
- Ein neuer Nutzer findet in <60s den richtigen Install-Weg
- Recovery Steps sind klar (disable plugins, clear cache, pin versions, logs)
- Keine Doppel-Inhalte, keine widersprüchlichen Anweisungen (SSOT)

---

### EPIC B — „Alles in Einklang bringen“ (State Audit + Gegen-Research + SOTA Upgrades)
Ziel:
- Aktueller Stand aller Dateien/Configs wird erfasst und gegen „Soll“ gemappt.
- Agenten-Setup wird korrekt verstanden und dokumentiert (wo liegt was, wer überschreibt wen).

Agent-Rollen (geplant):
1) Auditor: liest alle relevanten Dateien, baut Inventory (Datei → Zweck → Owner).
2) Compatibility Researcher: OS-Kompatibilitäten, known issues (bun/plugin/auth).
3) SOTA Upgrader: moderne Prompt-Strukturen (z. B. klare sections/tags), ohne Overengineering.
4) Agent-Config Expert (wichtig): erklärt korrekt:
   - Agenten definieren/override/deaktivieren
   - Config-Paths + Load-Order
   - Plugin-Agenten vs OpenCode built-ins
   - „Wie bringe ich oh-my + micode + orchestrator in Einklang?“

Output:
- INVENTORY.md (Configs, Agents, Plugins, Versions)
- CONFLICTS.md (Overlaps, Overrides, Gewinner/Verlierer)
- DECISIONS.md (mit „warum“)
- TASKS.md (priorisiert)

---

### EPIC C — Wanda Doppel-System funktionsfähig (single + dual mode)
Ziel:
- 3 Modi sauber:
  - "wanda voice"
  - "wanda code"
  - "wanda" (dual)

Cross-OS Anforderungen:
- Cosmic Wayland
- GNOME Linux
- Windows
- macOS (Problemkind)
- Apple Silicon (M4) + ältere Macs

Akzeptanzkriterien:
- Gleiches CLI UX Pattern auf allen OS
- deterministische Config-Pfade + Installer erkennt OS und setzt korrekt
- Voice Flow stabil (inkl. Ollama optional)
- Code Flow stabil (OpenCode stack)

---

### EPIC D — Installer: Fresh Install / Reinstall / Update (UX-first)
Ziel:
- Installer deckt ab:
  1) Fresh Install: deps + packages
  2) Plugin/Tool Setup: opencode + plugins + auth/connect + defaults
  3) Guided Setup: name, Work-OS, API keys, Ollama integration, MCP hub, Stimmenwahl + Demos, Defaults + Empfehlungen
  4) Reinstall: ohne Tokens/Settings zwingend zu löschen (opt-in reset)
  5) Update Mode: `wanda update`
     - check beim Start
     - wenn Update verfügbar → beim nächsten Start Auto-Update (ohne extra command)

Wichtige Edge Cases:
- BunInstallFailedError (proxy/registry/cert, windows bun support in progress) [S5][S9]
- Plugin Cache „stuck“ → definierte Cache-Clear/Update-Skripte [S10][S11]
- Provider creds /connect / auth.json location [S4]

Akzeptanzkriterien:
- Installer ist idempotent (mehrfach laufen = kein Chaos)
- Jede Action hat „undo“ oder safe rollback
- Logs + klare Fehlermeldungen + Issue link/Template

---

### EPIC E — Fehlende Features implementieren + Hardening (Owner-mode)
Ziel:
- Projekt wird behandelt wie eigenes Produkt, release-ready:
  - Sicherheit, Edge Cases, Reliability, Performance, Token-Effizienz
  - Clean Code + Docs + Tests/Smoke Tests
  - Keine stillen Konflikte (Plugins/Agenten)

Definition:
- Jede Änderung dokumentiert (Changelog/Decisions)
- Keine „magischen“ Defaults ohne Erklärung
- Performance: Token-Aware (compaction/truncation) ohne Qualität zu zerstören

---

### EPIC F — Agenten & Plugins harmonisieren (Overlaps eliminieren)
Ziel:
- Vollständige Agent-Liste pro Quelle + Dedup:
  - OpenCode (core agents)
  - oh-my-opencode
  - opencode-orchestrator
  - micode
- Cluster nach Funktion: Planner, Router, Coder, Reviewer, Researcher, Ops
- Gewinner bestimmen und Duplikate deaktivieren, nicht „blind“ löschen.

Research-Notes:
- OpenCode built-ins: Build/Plan (primary), General/Explore (subagents). [S3]
- oh-my-opencode: Agent enable/disable + replace_plan. [S1]
- Plugin Load-Order & Duplicate rules: gleiche npm pkg+version nur einmal; lokale + npm plugins können parallel laden. [S2]
- micode: per-agent overrides + model resolution priority. [S6]

Output-Artefakte:
- AGENTS_INVENTORY.md (Tabelle)
- AGENTS_CLUSTERING.md (Funktionen → Kandidaten)
- AGENTS_FINAL.md (Final aktiv/deaktiviert, inkl. Begründung)
- CONFIG_MAP.md (welche config wo liegt, wer gewinnt)

---

### EPIC G — Finale „V0 Skills“
Ziel:
- v0-Style Skills/Workflows als wiederverwendbare Pipelines:
  - (1) Web/App Code Generation
  - (2) n8n Workflow Generation/Deploy/Fix
  - plus: Repo hardening, install+update, incident triage

Status:
- Beispiele gesammelt, Inhalt noch nicht validiert → muss reviewed werden.

---

## 3) Clean Plan (einfach & original) — konsolidiert

### 0) Ziel
Stabile OpenCode-Basis mit OhMyOpenCode, OpenCode-Orchestrator und MiCode.
Keine doppelten Agenten, keine stillen Konflikte.

### 1) Bekannte Fehler entschärfen
- Anthropic/JSON vorsichtig:
  - JSON/JSONC strikt valide
  - keine „cleveren Overrides“, die schema brechen
- Credential-Errors erst isolieren (siehe P0 micode/anthropic).

### 2) Plugins zu einer Basis verschmelzen
2.1 Ist-Zustand erfassen
- Agenten aus:
  - OpenCode core
  - OhMyOpenCode
  - OpenCode-Orchestrator
  - MiCode
- Pro Agent:
  - Name
  - Aufgabe
  - Quelle
  - Overlap ja/nein
  - Tools/Permissions
  - Default Model + overrides

2.2 Redundanzen finden
- Cluster: Planner / Router / Coder / Reviewer / Research / Ops
- Ziel: pro Funktion darf es mehrere Agenten geben, aber nicht 2 mit identischer Aufgabe.

2.3 Gewinner bestimmen
Behalte Agent, der:
- am nächsten am Routing/Orchestrator sitzt
- die meisten Tools nativ integriert
- die wenigsten Nebenwirkungen hat
- die stabilste Config/Override-Story hat

2.4 Finale Basis-Konfig
- Aktive Plugins
- Aktive Agenten
- Explizit deaktivierte Agenten
- Default-Modell + Fallbacks
- Prompt-Hardening (SOTA 2026) als eigenes Artefakt:
  - NICHT „nur behaupten“, sondern mit Research & Beispielen dokumentieren.

---

## 4) Definition of Done ✅
- OpenCode startet ohne Konflikte
- Alle Plugins laufen zusammen
- Keine überlappenden Agenten (core + 3 Plugins) ohne bewusste Entscheidung
- Deaktivierungen dokumentiert
- Änderungen dokumentiert
- Keine redundanten Infos / keine Drift (SSOT)
- Modernes, konsistentes Prompting über alle Agents/Subagents
- V0 Skills vorhanden, nutzbar, logisch aufgebaut, performance-orientiert
- Installer: fresh/reinstall/update stabil + cross-OS

---

## 5) Quellen & Research Entry Points (aus deinen Notizen)
Offizielle/primäre Dokus:
- https://github.com/vtemian/micode
- https://github.com/code-yeongyu/oh-my-opencode/blob/dev/docs/configurations.md
- https://www.npmjs.com/package/opencode-orchestrator
- https://opencode.ai/docs/ecosystem/

---

## 6) Nächste Schritte (ohne neue Infos möglich)
1) Agenten-Inventar erstellen (core + alle Plugins)
2) Duplikate clustern (Planner/Router/Coder/Reviewer/Research/Ops)
3) „Winner set“ definieren + deaktivieren (explizit)
4) Smoke-Test Matrix (Linux/Windows/macOS) + Auth Matrix (Anthropic/Google/Antigravity)
5) Installer-Doc/UX (README → AI_INSTALLATION.md) umstellen

---

## 7) Was ich dafür von dir brauche (nur falls du es willst)
- 1) Aktueller Config-Tree (Dateinamen + Pfade) aus:
     ~/.config/opencode/
     ~/.cache/opencode/ (nur Struktur, keine Secrets)
- 2) Deine aktuelle Plugin-Liste + Versions (aus opencode.json)
- 3) 1–2 Log-Snippets zu:
     - Anthropic Credential Error
     - BunInstallFailedError
     
     
Quellen-Mapping der [Sx]-Marker (für Nachweis/Research, nicht zum Kopieren):
[S1] oh-my-opencode Agent enable/disable + replace_plan + hooks: https://ohmyopencode.com/configuration/
[S2] OpenCode Plugin Load-Order + bun install behavior + duplicate rules: https://opencode.ai/docs/plugins/
[S3] OpenCode built-in Agents (Build/Plan + Subagents): https://opencode.ai/docs/agents/
[S4] OpenCode Providers + /connect + auth.json path: https://opencode.ai/docs/providers/
[S5] OpenCode Hinweis: Windows Bun Support „in progress“: https://opencode.ai/docs/
[S6] micode config (opencode.json + micode.json, model resolution): https://github.com/vtemian/micode
[S7] OpenCode Issue: Anthropic credential error & Downgrade workaround: https://github.com/anomalyco/opencode/issues/11039?utm_source=chatgpt.com
[S8] Claude Code Issue: credential restriction message Kontext: https://github.com/anthropics/claude-code/issues/8046?utm_source=chatgpt.com
[S9] BunInstallFailedError Beispiel opencode-notifier: https://github.com/different-ai/openwork/issues/125?utm_source=chatgpt.com
[S10] Cache/Plugin Troubleshooting (clear cache etc.): https://opencode.ai/docs/troubleshooting/?utm_source=chatgpt.com
[S11] Antigravity auth plugin: keine Auto-Updates, Cache clear nötig + Update-Anleitung: https://github.com/shekohex/opencode-google-antigravity-auth?utm_source=chatgpt.com
[S12] oh-my-opencode Issue: agent override wird ignoriert (config drift): https://github.com/code-yeongyu/oh-my-opencode/issues/472?utm_source=chatgpt.com
[S13] oh-my-opencode Issue: disabled_agents / Sisyphus optional Diskussion: https://github.com/code-yeongyu/oh-my-opencode/issues/836?utm_source=chatgpt.com
[S14] OpenCode Ecosystem listet Antigravity OAuth Plugins: https://opencode.ai/docs/ecosystem/?utm_source=chatgpt.com
