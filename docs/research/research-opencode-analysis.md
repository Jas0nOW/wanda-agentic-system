# Deep-Research-Report zu OpenCode, oh-my-opencode und Sisyphus

> **Hinweis:** Upstream-Quellen nennen `Sisyphus` als Default-Orchestrator. In WANDA ist **Commander** der einzige Primary; `Sisyphus` bleibt als Plugin-Default deaktiviert.

## Executive Summary

OpenCode ist ein Open‑Source Coding‑Agent, der in Terminal/IDE/Desktop läuft und über eine zentrale JSON/JSONC‑Konfiguration gesteuert wird. Das System kann mehrere Provider/Modelle nutzen (u. a. via Providers‑Konfiguration) und hat ein eingebautes Agenten‑Konzept (Primary Agents + Subagents) sowie ein Plugin‑System, das Verhalten über Hooks/Events erweitern kann. (Quellen: [2], [4], [16])

oh-my-opencode ist ein OpenCode‑Plugin („Agent Harness“/Orchestration‑Layer), das OpenCode in Richtung „Team statt Einzelmodell“ erweitert: Es bringt einen Default‑Orchestrator („Sisyphus“) plus mehrere spezialisierte Neben‑Agents (z. B. Oracle/Librarian/Explore) sowie Planungs‑Agents und ein Kategorie‑System für Delegation. Ziel ist, die Haupt‑Konversation schlank zu halten (Kontext sparen), Aufgaben parallel an günstigere/spezialisierte Modelle auszulagern und am Ende verifizierte Ergebnisse zu liefern. (Quellen: [2], [4], [13])

Sisyphus ist dabei der zentrale Orchestrator‑Agent, der laut Projekt‑Doku „plant, delegiert und ausführt“, mit Todo‑getriebenem Workflow und aggressiver Parallelisierung durch Background‑Agents. Ergänzend existieren Mechanismen/„Hooks“ wie Todo‑Continuation‑Enforcer, Comment‑Checker, Rules/README/AGENTS‑Injection, Session‑Recovery und (optional) Ultrawork‑Mode als „Just‑Do‑It“‑Trigger. (Quellen: [2], [4], [13])

Die wichtigsten Gründe, warum sich der Stack lohnt, sind (a) **Multi‑Agent‑Aufteilung** (Recherche/Exploration/Review/UI getrennt), (b) **Kosten‑/Geschwindigkeits‑Hebel** durch günstige Modelle für Suchen/Scans und starke Modelle für Architektur/Hard Bugs, (c) **Deterministischere Refactors** über LSP‑Funktionen (z. B. Rename/References) statt „Text‑Replace“, und (d) **klarere Guardrails** über Permissions/Bash‑Allowlisting/Read‑only‑Agents. (Quellen: [2], [8], [11])

Top‑Risiken/Footguns (mit Kern‑Mitigations):

Erstens: **Unbeabsichtigte Konfig‑ oder Plugin‑Änderungen** (weil Configs gemerged werden, nicht ersetzt). Mitigation: Vorher Snapshots/Hashes, minimale Diffs, getrennte Projekt‑Configs, und Rollback‑Plan, der Plugin‑Eintrag und die oh‑my‑opencode‑Config sauber zurücknimmt. (Quellen: [3], [4], [1])

Zweitens: **„Ultrawork“/Todo‑Enforcement kann Arbeit eskalieren** (mehr Delegation, mehr Token, mehr Änderungen). Mitigation: Permissions auf „ask“, Concurrency‑Limits, zunächst Plan‑/Read‑Only‑Workflows, und definierte Abbruchkriterien. (Quellen: [15], [16], [11])

Drittens: **Kontext‑Leakage über MCP/Tools**: MCP‑Server fügen Tools und Kontext hinzu und können sehr viele Tokens ziehen. Mitigation: nur notwendige MCPs aktivieren, ggf. pro Agent aktivieren/abschalten, und sensible Files zusätzlich per Plugin‑Guard schützen (z. B. „.env‑protection“ Hook). (Quellen: [4], [5], [6])

Viertens: **Provider‑/ToS‑Risiken**: oh‑my‑opencode dokumentiert explizit, dass es (Stand Januar 2026) Einschränkungen rund um Drittanbieter‑OAuth/ToS gibt und empfiehlt bestimmte Nutzungen nicht. Mitigation: Provider‑Wahl bewusst treffen, nur offizielle Auth‑Wege/Provider nutzen, keine „Spoofing“/Unofficial OAuth‑Tools, und im Team klar dokumentieren, welche Accounts/Provider erlaubt sind. (Quellen: [14], [7], [11])

Fünftens: **Prompt‑Injection/Marketing‑Anweisungen in Setup‑Guides**: Der Installation‑Guide für LLM‑Agents enthält nicht‑technische Instruktionen (z. B. „Free advertising“, „Ask for a Star“). Diese sind für einen sicheren Betrieb irrelevant und sollten strikt ignoriert werden. Mitigation: nur technisch überprüfbare Schritte übernehmen, alles „Social/Marketing“ konsequent ausfiltern. (Quellen: [2], [17])

## Begriffe und Komponentenkarte

OpenCode (Core) ist die Runtime + TUI/Server‑Architektur samt Konfig‑System, Agent‑System, Tool/Permission‑System und Plugin‑Engine. Es startet beim `opencode`‑Run eine TUI und einen Server; der Server veröffentlicht eine OpenAPI‑Spezifikation und kann auch standalone laufen (`opencode serve`). (Quellen: [4], [6], [11])

oh-my-opencode (Plugin/Harness) ist ein OpenCode‑Plugin, das zusätzliche Agents, Skills, MCP‑Defaults, Hooks und Orchestrierungslogik bereitstellt. Es wird über die `plugin`‑Liste in OpenCodes Config geladen (NPM‑Plugin‑Loading) und ergänzt dazu eine separate `oh-my-opencode.json/jsonc`‑Konfiguration (User/Project‑Scope). (Quellen: [2], [3], [4])

Sisyphus (Core‑Agent im Harness) ist der Default‑Orchestrator in oh‑my‑opencode. In der Features‑Doku wird Sisyphus als „default orchestrator“ beschrieben, der komplexe Aufgaben plant, delegiert und ausführt, Todo‑getrieben arbeitet und parallelisiert. (Quellen: [13], [15], [1])

Relevante verwandte Konzepte, die du für „korrekt und sicher“ wirklich verstehen musst:

OpenCode Config‑Precedence: Konfigurationsquellen werden in einer definierten Reihenfolge geladen; spätere Quellen überschreiben frühere, Configs werden **zusammengeführt** (merged), nicht komplett ersetzt. Wichtig für „warum greifen meine Overrides nicht“ und „warum existieren plötzlich zwei Einstellungen gleichzeitig“. (Quellen: [3], [1])

OpenCode Agenten‑Modell: Es gibt Primary Agents (Tab‑wechselbar) und Subagents (manuell per `@` oder automatisch), inklusive Navigation zwischen Parent/Child‑Sessions. Das ist die Grundlage für Multi‑Agent in OpenCode selbst – oh‑my‑opencode baut darauf auf. (Quellen: [2], [1])

OpenCode Plugins: Plugins können aus NPM geladen werden; OpenCode installiert sie automatisch via Bun und cached in `~/.cache/opencode/node_modules/`. Es gibt ein dokumentiertes Plugin‑Load‑Order‑Modell (Global Config, Project Config, Global Plugin Dir, Project Plugin Dir). (Quellen: [3], [4], [17])

Komponentenkette (Textdiagramm):

User → OpenCode Runtime (TUI + Server) → OpenCode Agent System (Build/Plan + Subagents) → oh-my-opencode Plugin (Hooks/Skills/MCP/Orchestrator) → Sisyphus (Primary Orchestrator) → Subagents (oracle/librarian/explore/…) + Kategorien/Skills → Tools (OpenCode Tools + MCP Tools + LSP) → Repo/Filesystem/Git/Test Runner → Output (Diffs/Commits/Docs/Plan/Logs). (Quellen: [2], [4], [5])

Abgrenzungen (praktisch):

Core (OpenCode): Konfig‑Merge/Precedence, Tools/Permissions, Agents, Plugin‑Engine, LSP‑Server‑Management, MCP‑Management. (Quellen: [2], [3], [4])

Plugin/Harness (oh-my-opencode): zusätzliche Agents + Delegation über Kategorien, zusätzliche Hooks/Policies (Todo/Comments/Context‑Injection), zusätzliche Convenience‑Tools/Flows (z. B. `doctor`), optional tmux‑Parallel‑UI, und opinionated Defaults. (Quellen: [2], [4], [13])

## Architektur und Ablauf

Wie OpenCode Agenten grundsätzlich arbeiten: (Quellen: [1])

Primary Agents sind die „Hauptrollen“ (z. B. Build, Plan) und lassen sich mit Tab wechseln; Subagents können von Primary Agents aufgerufen werden oder per `@` durch dich. OpenCode dokumentiert außerdem eine Navigation durch Child‑Sessions, wenn Subagents eigene Sessions starten. (Quellen: [2], [1])

Ein zentrales Sicherheits‑Muster ist dabei: Plan‑Agent als „restriktiver“ Agent, der standardmäßig file‑edits/bash auf „ask“ setzt (also approval‑basiert), damit du Analysen/Pläne bekommst ohne ungewollte Änderungen. Das ist ein sehr guter Default‑Workflow, um oh‑my‑opencode/Sisyphus später kontrolliert zu nutzen. (Quellen: [13], [11], [1])

Wie oh-my-opencode die Orchestrierung erweitert: (Quellen: [13], [1])

oh‑my‑opencode bringt eine „AI‑Team“-Struktur: Neben Sisyphus gibt es spezialisierte Agents wie Oracle (Read‑only Beratung), Librarian (Repo/Docs‑Recherche), Explore (schnelles Read‑only Grep) und Multimodal‑Looker (PDF/Bilder). Planung wird über Prometheus/Metis/Momus ergänzt. Diese Rollen sind explizit in der Features‑Doku mitsamt Restriktionen beschrieben. (Quellen: [2], [13], [15])

Der Delegations‑Mechanismus hat zwei Hauptformen:

Erstens explizit über `delegate_task(...)`: In der Konfiguration wird beschrieben, dass du per Kategorie delegieren kannst (z. B. `visual-engineering` oder `ultrabrain`) oder einen Agent direkt ansprechen kannst (bypasst Kategorien).

Zweitens implizit über Sisyphus’ Orchestrator‑Verhalten: Das README beschreibt, dass Sisyphus Background‑Agents nutzt, um Kontext zu sparen und parallel „die Landschaft zu kartieren“, LSP für Refactors bevorzugt, UI‑Arbeit zu UI‑Modellen delegiert und bei Blockern Oracle als „High‑IQ Backup“ nutzt. (Quellen: [2], [8], [13])

Todo‑Enforcer / „Relentless completion“: (Quellen: [15])

oh‑my‑opencode positioniert den Workflow als Todo‑getrieben und nennt einen Todo‑Continuation‑Enforcer explizit als Hook. Dadurch soll das System verhindern, dass der Agent „halbfertig“ aufhört. Das Manifest formuliert als Leitbild „Continuous“ (unterbrechungs‑resistent) und „Delegatable“ (wie ein Compiler‑Pipeline). (Quellen: [4], [15], [1])

Wichtig für deine Sicherheit: Ein solcher „Completion Enforcer“ ist **kein** Ersatz für Permissions/Git‑Isolation, sondern erhöht potenziell die Änderungsmenge. Du musst diese Kraft über (a) Permissions „ask“, (b) klare Definition‑of‑Done/Abbruchkriterien, und (c) Concurrency‑/Budget‑Limits einhegen. (Quellen: [16], [11])

Guardrails / Hooks / Reihenfolge: (Quellen: [4])

OpenCode Plugins laufen in einer dokumentierten Load‑Order; Hooks („Events“) sind klar definiert (Tool‑Events, Session‑Events, Permission‑Events, etc.). oh‑my‑opencode listet zusätzlich eigene „built‑in hooks“ (u. a. `todo-continuation-enforcer`, `comment-checker`, `rules-injector`, `directory-agents-injector`, `directory-readme-injector`, `session-recovery`, `preemptive-compaction`, `claude-code-hooks`, `ralph-loop`). Du kannst sie über `disabled_hooks` deaktivieren. (Quellen: [2], [4], [14])

Unsicher/Unbestätigt (und wie verifizieren):

Die genaue interne Logik, **wann** Sisyphus welchen Subagent auswählt (Task‑Graph‑Heuristik, „Delegation Table“, Priority‑Regeln) ist in den von mir zugänglichen Primärquellen nur konzeptionell beschrieben (README/Features/Config), nicht als formale Spezifikation. Verifikationsschritte: (1) nach Installation den Code der installierten Plugin‑Version lesen (NPM‑Plugin‑Cache unter `~/.cache/opencode/node_modules/` ist dokumentiert), (2) speziell nach Sisyphus‑Implementierung und `delegate_task`‑Tool suchen, (3) in Issues nach „delegation table“/„available agents“/„createSisyphusAgent“ prüfen. (Quellen: [2], [3], [4])

## Installation und Lifecycle

OpenCode Installation und Grund‑Lifecycle: (Quellen: [17], [1])

OpenCode wird installiert und dann pro Projekt über `/init` initialisiert. `/init` erzeugt ein `AGENTS.md` im Projekt‑Root; OpenCode empfiehlt, diese Datei zu committen. (Quellen: [2], [17], [1])

Provider‑Credentials: Wenn du Provider‑Keys via `/connect` hinzufügst, werden Credentials in `~/.local/share/opencode/auth.json` gespeichert. Das ist wichtig für Backups/Secrets‑Policy und „was bleibt lokal“. (Quellen: [7], [1])

oh-my-opencode Installation (aktuellste stabile Version): (Quellen: [13], [17], [1])

Die oh‑my‑opencode Doku empfiehlt primär den interaktiven Installer: `bunx oh-my-opencode install` (alternativ `npx`). In der Install‑Anleitung steht außerdem, dass die CLI „standalone binaries“ für gängige Plattformen liefert und nach Installation kein Node/Bun Runtime‑Setup für die CLI‑Ausführung nötig sein soll. (Quellen: [13], [17], [10])

Der Installer erledigt laut Guide u. a. das Registrieren des Plugins in OpenCodes `opencode.json` und generiert eine anfängliche oh‑my‑opencode Konfiguration basierend auf deinen Provider‑Flags. (Quellen: [3], [4], [17])

Version‑/Release‑Signale:

Die README betont, dass „Oh My OpenCode 3.0“ als stable veröffentlicht sei und nennt Installation über `oh-my-opencode@latest`. Zusätzlich verweist die README auf die Releases‑Seite als „official downloads“. (Quellen: [2], [13], [14])

Sicherheitswarnungen rund um Download‑Quellen:

Die README warnt explizit vor einer Impersonation‑Site, die nicht affiliiert sei, und rät, keine Installer/Payments dort zu verwenden; offizielle Downloads seien über GitHub Releases. Das ist sehr relevant für „nicht blind etwas installieren“. (Quellen: [14], [17])

ToS-/OAuth‑Risiko (Anthropic): (Quellen: [14])

oh‑my‑opencode enthält einen „Claude OAuth Access Notice“ und schreibt (Stand „January 2026“), dass es Einschränkungen zu Third‑Party OAuth gibt und dass er bestimmte Nutzungen „technisch möglich, aber nicht empfehlenswert“ finde. Für ein produktives Setup musst du das als Policy‑Entscheidung behandeln: welche Provider sind erlaubt, welche Accounts dürfen genutzt werden, und welche Auth‑Methode ist compliant. (Quellen: [14], [7], [1])

Update‑Strategie (stabiler Workflow):

OpenCode selbst befindet sich laut Repository‑Hinweis in „early development“ und „not yet ready for production“; Features können sich ändern. Das heißt nicht „nicht nutzen“, aber es bedeutet: Versionen bewusst pinnen, Changelogs lesen, und Updates erst im Test‑Repo validieren. (Quellen: [15], [12], [1])

oh‑my‑opencode erwähnt außerdem einen konkreten Footgun: Bei OpenCode ≤ 1.0.132 könne ein Bug Config brechen; Fix sei nach 1.0.132 gemergt, daher „use a newer version“. Für dich heißt das: Update‑Fenster und Mindestversionen dokumentieren. (Quellen: [3], [1])

## Konfig und Kontext-Referenz

OpenCode Config‑Orte und Precedence (entscheidend für „nichts kaputt machen“): (Quellen: [3], [1])

OpenCode lädt mehrere Config‑Quellen in festgelegter Reihenfolge: Remote Org‑Config (`.well-known/opencode`) → Global (`~/.config/opencode/opencode.json`) → Custom Path (`OPENCODE_CONFIG`) → Project (`opencode.json` im Projekt) → `.opencode`‑Directories (agents/commands/plugins/…) → Inline (`OPENCODE_CONFIG_CONTENT`). Spätere Quellen überschreiben frühere für kollidierende Keys; nicht kollidierende Einstellungen bleiben erhalten (Merge). (Quellen: [2], [3], [4])

Wichtiges Detail: `.opencode` und `~/.config/opencode` nutzen pluralisierte Subdirs (`agents/`, `plugins/`, `skills/` …), Singular ist nur Legacy. Das hilft gegen typische „Ordner falsch benannt“‑Bugs. (Quellen: [2], [3], [4])

oh-my-opencode Config‑Orte und Formate: (Quellen: [3], [13], [1])

oh‑my‑opencode nutzt eine separate Konfigurationsdatei mit Priorität: `.opencode/oh-my-opencode.json` (Projekt) vor dem User‑Pfad `~/.config/opencode/oh-my-opencode.json` (Windows optional `%APPDATA%` fallback). (Quellen: [3], [13], [1])

JSONC wird unterstützt (Kommentare, trailing commas). Wenn `.jsonc` und `.json` existieren, hat `.jsonc` Priorität. Für „kein Blindflug“ ist JSONC praktisch, weil du **Warum**‑Kommentare direkt neben Overrides dokumentieren kannst. (Quellen: [16])

Plugin‑Einbindung: (Quellen: [4])

OpenCode lädt NPM‑Plugins über die `plugin`‑Liste in `opencode.json` und installiert sie automatisch via Bun (Cache: `~/.cache/opencode/node_modules/`). Minimal‑invasiv heißt: Den eigentlichen OpenCode‑Core möglichst unangetastet lassen und nur den Plugin‑Eintrag hinzufügen; alle oh‑my‑opencode‑Spezifika gehören in `oh-my-opencode.json(c)`. (Quellen: [3], [4], [13])

Permissions als Sicherheitsgeländer: (Quellen: [11])

OpenCode steuert Tool‑Ausführung über `permission`. Beispiel: `edit: "ask"` und `bash: "ask"` erzwingt Approval. Außerdem können Bash‑Permissions per Command‑Pattern fein granular gesetzt werden (z. B. `git status*` allow, `git push` ask). (Quellen: [11], [10], [1])

oh‑my‑opencode erweitert das Permission‑Modell pro Agent in seiner eigenen Config ebenfalls (edit/bash/webfetch, zusätzlich z. B. `external_directory` und `doom_loop`). Das ist ein zentraler Hebel, um Ultrawork/Todo‑Enforcement nicht „unkontrolliert“ laufen zu lassen. (Quellen: [3], [15], [11])

Kontext‑Management in OpenCode und oh‑my‑opencode: (Quellen: [1])

OpenCode /init erzeugt `AGENTS.md` und empfiehlt Commit. Praktisch ist `AGENTS.md` der Ort, an dem du projektweite Regeln („wie wir arbeiten“) stabil dokumentierst. (Quellen: [2], [1])

oh‑my‑opencode erwähnt ausdrücklich Kontext‑Injection über `AGENTS.md` und `README.md` sowie Hook‑Namen wie `directory-agents-injector`, `directory-readme-injector` und `rules-injector`. Das bedeutet: Wenn du diese Dateien änderst, beeinflusst du (potenziell) das Verhalten vieler Runs. Deshalb: Änderungen an `AGENTS.md` wie Code behandeln – small diffs, Review, Test‑Repo. (Quellen: [2], [4], [14])

MCP‑Kontextkosten: (Quellen: [5])

OpenCode warnt, dass MCP‑Server „to the context“ beitragen und das schnell eskalieren kann; bestimmte MCPs (z. B. GitHub MCP) sind token‑schwer. Diese Warnung passt exakt zu deinem „nicht ineffektiv machen“‑Ziel: MCPs sind mächtig, aber nicht gratis. (Quellen: [5], [6], [1])

LSP und Formatters als „unsichtbare“ Änderungen: (Quellen: [8], [9])

OpenCode auto‑aktiviert LSP‑Server je nach Dateityp, lädt manche Server automatisch und kann Downloads per Env var deaktivieren (`OPENCODE_DISABLE_LSP_DOWNLOAD=true`). (Quellen: [8], [6], [1])

OpenCode formatiert Dateien nach `write/edit` automatisch über language‑spezifische Formatters. Das kann „unnötige“ Diff‑Noise erzeugen und ist eine häufige Ursache für „Agent hat zu viel geändert“. Du kannst Formatters konfigurieren oder deaktivieren, wenn du in einem sensiblen Setup erstmal minimal bleiben willst. (Quellen: [9], [1])

## Agenten-Katalog und Erweiterung

oh-my-opencode Agenten (Team statt Einzelmodell): (Quellen: [13], [1])

Die Features‑Doku listet eine „AI Team“‑Struktur mit Kern‑Agents und Planungs‑Agents. Eine kompakte, praxisorientierte Sicht (Zweck + Safety‑Profil): (Quellen: [2], [15])

Sisyphus: Default Orchestrator, delegiert und führt aus; Todo‑driven, parallelisiert aggressiv (höheres Änderungs‑/Kostenpotenzial). (Quellen: [13], [15])

oracle: Architektur/Debug/Review als **read‑only consultation** (nicht schreiben/edit/delegieren) – perfekt als „Guardrail‑Advisor“, bevor du große Refactors zulässt.

librarian: Multi‑Repo Analyse, Doku‑Lookup, OSS‑Implementierungsmuster – ebenfalls ohne write/edit/delegate (in Features als read‑only beschrieben). (Quellen: [15])

explore: Schnelle Codebase‑Exploration (read‑only) – ideal für „find files/patterns“, bevor du Sisyphus bauen lässt. (Quellen: [13])

multimodal-looker: Bild/PDF/Diagramm‑Analyse (allowlist read/glob/grep). Das ist nützlich, aber sicherer als „tool‑full“ Agents. (Quellen: [2], [11])

Prometheus / Metis / Momus: Planungs‑/Review‑Rollen (Strategie, Ambiguitäten finden, Plan verifizieren). Diese Rollen unterstützen deinen Wunsch „erst lernen/prüfen, dann ändern“. (Hinweis: Atlas wurde im aktuellen SOTA-Setup durch Sisyphus-Session-Management ersetzt).

Kategorien (für Delegation via `delegate_task`):

oh‑my‑opencode dokumentiert Kategorien wie `visual-engineering`, `ultrabrain`, `quick`, `writing` usw. und erklärt eine Model‑Resolution‑Logik (User override → Provider fallback → System default). Wichtig: Kategorien nutzen laut Doku ihre „built‑in defaults“ nur zuverlässig, wenn sie entsprechend konfiguriert sind. Das ist eine klassische Footgun: Du denkst „visual-engineering = Gemini“, aber ohne korrekte Konfig landet es im Default‑Model. (Quellen: [7], [1])

Skills (oh‑my‑opencode): (Quellen: [1])

Built‑in Skills werden als zusätzliche Capabilities beschrieben, u. a. Browser‑Automation (`playwright` default oder `agent-browser` alternative) sowie `git-master` für Git‑Operationen. Die Doku empfiehlt explizit, Git‑Arbeit über `git-master` zu delegieren (Kontext sparen, konsistenter Git‑Stil).

Erweiterung: neue Agents sicher hinzufügen (OpenCode‑Mechanismus als stabiler Anker) (Quellen: [2], [1])

OpenCode dokumentiert sehr klar, wie du eigene Agents definierst: (Quellen: [2], [1])

Entweder in `opencode.json` unter `agent`, oder als Markdown‑Dateien in `~/.config/opencode/agents/` (global) bzw. `.opencode/agents/` (projektbezogen). Das ist der sauberste Weg, neue Rollen zuzuschalten, ohne oh‑my‑opencode intern zu forken. (Quellen: [2], [3], [1])

OpenCode hat außerdem ein interaktives Kommando `opencode agent create`, das ein Agent‑Markdown erzeugt (inkl. Tool‑Auswahl). Das ist ideal, weil es „Schema‑konform“ erzeugt und weniger Tippfehler‑Risiko hat. (Quellen: [11], [1])

Minimal‑Beispiel: QA‑Agent (read‑only, test‑fokussiert)

```md
# ~/.config/opencode/agents/qa.md
---
description: Prüft Änderungen mit Fokus auf Tests, Edge-Cases und Regressionen (read-only).
mode: subagent
temperature: 0.1
permission:
  edit: deny
  webfetch: deny
  bash:
    "*": ask
    "npm test*": allow
    "pnpm test*": allow
    "bun test*": allow
    "pytest*": allow
tools:
  write: false
  edit: false
---
Du bist QA. Prüfe:
- Was wurde geändert? (Diff/Files)
- Welche Tests müssen laufen? (Minimal + relevant)
- Wo sind Edge-Cases, Sicherheits- und Datenintegritätsrisiken?
Gib eine Checkliste + erwartete Outputs.
```

Dieses Muster folgt OpenCodes Agent‑Konzept (Markdown‑Frontmatter, permissions). Du kannst den Agent jederzeit per `@qa` ansprechen, ohne den Default‑Agent zu wechseln. (Quellen: [2], [11], [1])

Minimal‑Beispiel: n8n‑Agent (konservativ, dokumentations‑orientiert)

```md
# .opencode/agents/n8n.md
---
description: Hilft bei n8n-Workflows: robuste Patterns, Fehlersuche, Idempotenz, Secrets-Handling.
mode: subagent
temperature: 0.2
permission:
  edit: ask
  webfetch: ask
  bash: ask
---
Du bist ein n8n-Automation-Engineer.
Regeln:
- Schreibe nur Änderungen, wenn explizit freigegeben wurde.
- Dokumentiere jedes neue Node/Flow-Element mit Zweck, Inputs/Outputs, Failure Modes.
- Achte auf Secrets/PII und schlage sichere Variablen-/Vault-Strategien vor.
```

Validierung, dass neue Agents geladen sind: (Quellen: [2])

Primär: OpenCode zeigt Agents über `@`‑Autocomplete und erlaubt Subagent‑Invocation per `@agentname`. Zusätzlich kannst du zwischen Primary Agents per Tab wechseln; Subagents sind im `@`‑Menü sichtbar (außer `hidden: true`). (Quellen: [2], [1])

## Safe Integration Plan

Ziel: oh‑my‑opencode/Sisyphus in ein bestehendes OpenCode‑Setup integrieren, minimal‑invasiv, nachvollziehbar, reversibel. (Quellen: [13], [1])

Preflight (Backup + Snapshot + Risiko‑Reduktion)

Arbeite in dieser Reihenfolge, weil OpenCode Configs merged und Plugins automatisch laden: (Quellen: [3], [4], [1])

Erstens Versions‑Snapshot:

```bash
opencode --version
opencode models | head -n 50
```

`opencode models` ist in oh‑my‑opencode‑Docs explizit als Weg genannt, verfügbare Modelle zu prüfen. (Quellen: [1])

Zweitens Config‑Backups (Hash + Copy): (Quellen: [3])

Relevante Files (mindestens):

- `~/.config/opencode/opencode.json` (global OpenCode config)
- `~/.config/opencode/oh-my-opencode.json` (falls existiert) bzw. `.opencode/oh-my-opencode.json`
- Projekt‑`opencode.json` und `.opencode/` (falls im Repo genutzt)
- Credentials‑Files nur als „Existenz prüfen“, nicht in Repo: `~/.local/share/opencode/auth.json`

Drittens Git‑Preflight (im Ziel‑Repo):

```bash
git status --porcelain
git switch -c chore/omo-integration
```

Abort‑Kriterium: Uncommitted Changes, die nicht vorher committed/stashed sind. (Du willst 1‑Diff‑Attribution.)

Test-Repo Dry-Run (Pflicht, bevor du dein echtes System anfasst)

Lege ein kleines Test‑Repo an, das ähnliche Sprache/Toolchain hat (z. B. dein typischer Node/TS‑Stack). Ziel ist: Installer + Plugin‑Load + Grundkommandos validieren. (Quellen: [4], [17], [11])

Minimaländerungen (Dateien/Ordner, die typischerweise entstehen)

Die Primärquellen nennen recht klar, was passieren soll:

OpenCode Global Config wird um Plugin‑Entry erweitert (Plugin‑Array). (Quellen: [3], [4], [1])

oh‑my‑opencode legt/liest seine Konfig in `.opencode/oh-my-opencode.json` (Projekt) oder `~/.config/opencode/oh-my-opencode.json` (User). (Quellen: [3], [13], [1])

Zusätzlich kann OpenCode Plugins in `~/.cache/opencode/node_modules/` cachen. (Quellen: [4], [1])

Repräsentativer Diff (Konzept)

1) In `~/.config/opencode/opencode.json` (minimal): (Quellen: [3], [1])

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": [
    "oh-my-opencode"
  ]
}
```

2) In `~/.config/opencode/oh-my-opencode.json` (minimal, dokumentiert): (Quellen: [3], [13], [1])

```jsonc
{
  "$schema": "https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json",
  // Safety-first: teure/gefährliche Aktionen nur nach Freigabe
  "agents": {
    "Sisyphus": {
      "permission": {
        "edit": "ask",
        "bash": "ask",
        "webfetch": "ask",
        "external_directory": "deny"
      }
    }
  },
  // Kosten/Chaos begrenzen
  "background_task": {
    "defaultConcurrency": 2
  }
}
```

Die verfügbaren Felder (agents/permissions/background_task) sind in der oh‑my‑opencode Konfig‑Doku beschrieben. (Quellen: [2], [15], [16])

Validierung (Smoke Tests + Status Checks)

1) Plugin‑Load‑Check: (Quellen: [4])

- Config enthält `"oh-my-opencode"` in plugin array (per `cat ~/.config/opencode/opencode.json`).

2) oh‑my‑opencode „Doctor“: (Quellen: [16], [1])

```bash
bunx oh-my-opencode doctor --verbose
```

Der `doctor`‑Command ist explizit dokumentiert, um Model‑Resolution/Provider‑Chains sichtbar zu machen. Expected Output: „Model Resolution“ zeigt pro Agent/Kategorie Override/Fallback/Effective Model. Abort‑Kriterium: Doctor zeigt fehlende Provider/Modelle oder unerwartet „System Default“ für kritische Agents. (Quellen: [2], [16], [7])

3) MCP‑Status (wenn relevant): (Quellen: [5])

```bash
opencode mcp list
opencode mcp auth list
```

OpenCode dokumentiert MCP‑CLI‑Kommandos sowie, dass MCP‑OAuth‑Tokens in `~/.local/share/opencode/mcp-auth.json` gespeichert werden. Expected Output: MCPs entweder disabled oder „connected“. Abort: Unerwartete MCP‑Server aktiv, die du nicht willst (Kontext‑/Security‑Risiko). (Quellen: [5], [14], [6])

4) LSP‑Baseline (optional, aber empfohlen für Refactor‑Workflows): (Quellen: [8])

Wenn du LSP‑Tooling aktiv nutzen willst, beachte: Das `lsp` Tool ist experimentell und erfordert ein Env‑Flag (`OPENCODE_EXPERIMENTAL_LSP_TOOL=true` oder `OPENCODE_EXPERIMENTAL=true`) plus Permission `lsp: "allow"`. (Quellen: [8], [11], [1])

Rollback (exakt umkehrbar)

oh‑my‑opencode README liefert einen klaren Uninstall‑Pfad: (Quellen: [14], [17], [1])

1) Plugin aus OpenCode config entfernen (plugin array).
2) oh‑my‑opencode config files entfernen (User und ggf. Projekt).
3) Verifizieren: `opencode --version` / Plugin nicht mehr geladen (praktisch: Verhalten/Agents weg). (Quellen: [2], [3], [4])

Du solltest zusätzlich: Git‑Branch zurücksetzen (wenn repo‑lokale `.opencode/*` angelegt wurde). (Quellen: [1])

Operator Checklist

| Schritt | Command | Expected Output | Abort-Kriterium / Wenn abweichend |
|---|---|---|---|
| Versions erfassen | `opencode --version` | Version wird angezeigt | Version extrem alt → erst updaten (oh‑my‑opencode warnt vor alten Versionen).  |
| Provider/Model‑Inventar | `opencode models` | Liste verfügbarer Modelle | erwartete Provider fehlen → Auth/Provider Setup klären.  |
| Plugin registriert? | `cat ~/.config/opencode/opencode.json` | `plugin` enthält `"oh-my-opencode"` | fehlt → Installer/Config‑Diff prüfen.  |
| Doctor | `bunx oh-my-opencode doctor --verbose` | Model‑Resolution nachvollziehbar | falsches Default‑Model / fehlende Provider → erst fixen.  |
| MCP‑Status | `opencode mcp list` | nur gewünschte MCPs enabled | unerwartete MCPs aktiv → in Config deaktivieren.  |
| Permissions Safety | (Review der configs) | `edit/bash` auf `ask` | `allow` überall → erst härten, dann arbeiten.  |

Praxis: 3 End‑to‑End Workflows (mit DoD)

Workflow: Refactor via LSP + Tests (sicher) (Quellen: [8])

Ablauf: (1) Plan‑Agent erstellen lassen: „Welche Symbole werden umbenannt? Welche Tests betroffen?“ (2) LSP‑Refactor nutzen (wenn aktiviert), (3) Formatter‑Noise kontrollieren (ggf. temporär deaktivieren), (4) Tests laufen lassen, (5) QA‑Subagent reviewt Diff und Testresultate. (Quellen: [2], [8], [9])

DoD: Rename ist konsistent (References), Tests grün, Diff enthält keine unnötigen reformat‑Blöcke. LSP‑Server‑Setup und Formatter‑Autoformat sind in OpenCode dokumentiert. (Quellen: [8], [6], [9])

Workflow: Feature‑Implementierung als Multi‑Agent‑Team (Quellen: [15])

Ablauf: (1) Prometheus/Plan‑Flow für sauberen Plan (Intent‑Erhebung), (2) Sisyphus implementiert in kleinen PR‑fähigen Schritten, (3) oracle als read‑only Architektur‑Review, (4) librarian sammelt „Belege“ (Docs/OSS patterns), (5) git-master macht atomare Commits. (Quellen: [13])

DoD: Plan dokumentiert, Implementation folgt bestehenden Patterns (keine „AI‑Slop“‑Abstraktionen), Commits sind granular, Tests/Build erfolgreich. Rollen/Restriktionen sind in oh‑my‑opencode Features dokumentiert. (Quellen: [15], [1])

Workflow: Bugfix/Incident‑Style

Ablauf: (1) Explore Agent findet relevante Stellen (read‑only), (2) Librarian zieht ähnliche Fixes aus OSS/Docs (Belege), (3) Sisyphus erstellt minimalen Fix + Regression‑Test, (4) QA Agent prüft Testabdeckung + Edge‑Cases, (5) optional: server/tmux‑Integration, um parallel in Panes arbeiten zu können. (Quellen: [13], [6])

DoD: Repro Steps dokumentiert, Fix minimal, Regression‑Test vorhanden, keine zusätzlichen Risiko‑Änderungen. tmux/server mode ist in oh‑my‑opencode config dokumentiert; OpenCode server architecture ebenfalls. (Quellen: [3], [6], [1])

## Betrieb, Wartung und Troubleshooting

Betrieb: „Safety Defaults“ für produktive Nutzung

Read‑only zuerst: Nutze Plan‑Agent und/oder read‑only Subagents (oracle/librarian/explore), bevor du Sisyphus schreiben lässt. OpenCode beschreibt Plan als restriktiven Agent; oh‑my‑opencode beschreibt oracle/librarian/explore als read‑only bzw. stark eingeschränkt. (Quellen: [2], [13], [1])

Permission‑Modell konsequent: Setze `edit` und `bash` mindestens auf `ask`; ergänze Allowlist‑Patterns für harmlose Kommandos. OpenCode zeigt genau dieses Muster. (Quellen: [11], [1])

Git‑Strategie: Immer Branch + atomare Commits (idealerweise per `git-master`). oh‑my‑opencode stellt `git-master` als Skill heraus und bietet sogar Konfigoptionen für Commit‑Trailer/Footer. (Quellen: [1])

MCP‑Minimalismus: MCP‑Server nur selektiv aktivieren; OpenCode warnt vor Kontextkosten und empfiehlt Vorsicht. (Quellen: [5], [6], [1])

Top Probleme und bekannte Failure Modes (mit Quellen)

ToS/OAuth‑Einschränkungen: oh‑my‑opencode weist explizit auf Third‑Party OAuth‑Restriktionen hin (Januar 2026). Symptom: Auth klappt nicht / Accounts werden eingeschränkt. Fix: Nur offizielle/compliant Provider nutzen; keine inoffiziellen OAuth‑Spoofs. (Quellen: [14], [7], [1])

„Sisyphus delegiert nicht“: Es existiert ein Issue, das fehlende Delegation in Subagents beschreibt und auf die Sisyphus‑Implementierung verweist. Symptom: Keine Delegation Table / Sisyphus macht alles selbst. Mitigation: Version prüfen, Config/Agents verfügbar machen, und bei Repro auf Issue‑Ebene debuggen. (Quellen: [2], [3], [13])

Custom Agent „springt zurück“: Es gibt ein Issue, dass nach Wechsel zu einem Custom Agent (z. B. „Sisyphus‑Lite“) die erste Message wieder von Sisyphus verarbeitet wird. Mitigation: Workaround dokumentieren (erneut umschalten), Versions‑Fix verfolgen, und in produktiver Umgebung den Agent‑Switch vorher testen. (Quellen: [13], [19])

Task‑Tool/Delegation‑Grenzen: OpenCode hatte/hat Issues, dass Subagents manchmal delegieren, obwohl sie es nicht sollten („Subagents are using the task tool“). Das ist relevant, wenn du dich auf „Subagent kann nicht delegieren“ verlassen willst. Mitigation: Task‑Permissions nutzen und in Policies explizit einschränken (OpenCode dokumentiert `permission.task`). (Quellen: [2], [20], [11])

Prompt‑Injection im Setup‑Guide: Der oh‑my‑opencode Install‑Guide enthält nicht‑technische Instruktionen (Werbung/Stars). Mitigation: In deinem internen Runbook explizit markieren: ignorieren. (Quellen: [17], [1])

Run‑Protokoll Template (für Vertrauen + Reproduzierbarkeit)

Dokumentiere pro Run:

- Datum, Repo, Branch
- `opencode --version` und relevante Plugin‑Version(en) (z. B. `bunx oh-my-opencode --version`, falls verfügbar)
- Hash/Snapshot: `sha256` der Config‑Files + kurzer Diff zum letzten Stand (Config‑Merge‑System!)
- Welche Agents aktiv (Sisyphus/Planner/etc.) + welche Permissions (ask/allow/deny)
- Welche MCPs enabled (`opencode mcp list`)
- Welche Tests/Commands liefen + Outputs (Ausschnitt)
- Ergebnis: Diff‑Summary + DoD‑Checkliste

Kuratierte Links nach Kategorien (Primärquellen zuerst)

Core Docs (OpenCode): Intro (incl. `/init`, `AGENTS.md`), Config/Precedence, Agents, Plugins, MCP Servers, LSP Servers, Formatters, Server Architecture, Tools/LSP Tool. (Quellen: [2], [3], [4])

Core Repo (OpenCode): GitHub Repository mit Early‑Development Notice und Konfig‑Hinweisen. (Quellen: [12], [1])

oh-my-opencode Repo & README: Security‑Warnung (Impersonation‑Site), Install/Uninstall, ToS/OAuth Notice, Feature‑Überblick. (Quellen: [13], [14], [15])

oh-my-opencode Konfiguration/Features/Manifesto: Konfigpfade/JSONC, Agent/Hook/MCP/LSP/Concurrency‑Optionen, Team‑Agent‑Übersicht, Philosophie (Ultrawork). (Quellen: [4], [5], [8])

Issues/Discussions (gezielt): Delegation‑Probleme, Custom Agent Switch, Task‑Tool‑Anomalien. (Quellen: [11])

---

## Quellen (kuratierte Primär-Links)

Die Referenzen werden im Text als `[Zahl]` verlinkt.

- [1] **OpenCode Docs – Intro** — https://opencode.ai/docs/
- [2] **OpenCode Docs – Agents** — https://opencode.ai/docs/agents/
- [3] **OpenCode Docs – Config** — https://opencode.ai/docs/config/
- [4] **OpenCode Docs – Plugins** — https://opencode.ai/docs/plugins/
- [5] **OpenCode Docs – MCP Servers** — https://opencode.ai/docs/mcp-servers/
- [6] **OpenCode Docs – Server** — https://opencode.ai/docs/server/
- [7] **OpenCode Docs – Providers** — https://opencode.ai/docs/providers/
- [8] **OpenCode Docs – LSP Servers** — https://opencode.ai/docs/lsp/
- [9] **OpenCode Docs – Formatters** — https://opencode.ai/docs/formatters/
- [10] **OpenCode Docs – CLI** — https://opencode.ai/docs/cli/
- [11] **OpenCode Docs – Tools** — https://opencode.ai/docs/tools/
- [12] **OpenCode GitHub Repo** — https://github.com/opencode-ai/opencode
- [13] **oh-my-opencode GitHub Repo** — https://github.com/code-yeongyu/oh-my-opencode
- [14] **oh-my-opencode README (raw)** — https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/README.md
- [15] **oh-my-opencode Features (raw)** — https://github.com/code-yeongyu/oh-my-opencode/raw/refs/heads/dev/docs/features.md
- [16] **oh-my-opencode Configurations (raw)** — https://github.com/code-yeongyu/oh-my-opencode/raw/refs/heads/dev/docs/configurations.md
- [17] **oh-my-opencode Installation Guide (raw)** — https://github.com/code-yeongyu/oh-my-opencode/raw/refs/heads/dev/docs/guide/installation.md
- [18] **Issue #411 – Sisyphus not delegating** — https://github.com/code-yeongyu/oh-my-opencode/issues/411
- [19] **Issue #893 – Primary custom agent switches back** — https://github.com/code-yeongyu/oh-my-opencode/issues/893
- [20] **Issue #4439 – Subagents are using the task tool** — https://github.com/sst/opencode/issues/4439

- [21] **OpenCode Config Schema (JSON)** — https://opencode.ai/config.json
- [22] **oh-my-opencode Schema (JSON)** — https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json


[1]: https://opencode.ai/docs/ "OpenCode Docs – Intro"
[2]: https://opencode.ai/docs/agents/ "OpenCode Docs – Agents"
[3]: https://opencode.ai/docs/config/ "OpenCode Docs – Config"
[4]: https://opencode.ai/docs/plugins/ "OpenCode Docs – Plugins"
[5]: https://opencode.ai/docs/mcp-servers/ "OpenCode Docs – MCP Servers"
[6]: https://opencode.ai/docs/server/ "OpenCode Docs – Server"
[7]: https://opencode.ai/docs/providers/ "OpenCode Docs – Providers"
[8]: https://opencode.ai/docs/lsp/ "OpenCode Docs – LSP Servers"
[9]: https://opencode.ai/docs/formatters/ "OpenCode Docs – Formatters"
[10]: https://opencode.ai/docs/cli/ "OpenCode Docs – CLI"
[11]: https://opencode.ai/docs/tools/ "OpenCode Docs – Tools"
[12]: https://github.com/opencode-ai/opencode "OpenCode GitHub Repo"
[13]: https://github.com/code-yeongyu/oh-my-opencode "oh-my-opencode GitHub Repo"
[14]: https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/refs/heads/master/README.md "oh-my-opencode README (raw)"
[15]: https://github.com/code-yeongyu/oh-my-opencode/raw/refs/heads/dev/docs/features.md "oh-my-opencode Features (raw)"
[16]: https://github.com/code-yeongyu/oh-my-opencode/raw/refs/heads/dev/docs/configurations.md "oh-my-opencode Configurations (raw)"
[17]: https://github.com/code-yeongyu/oh-my-opencode/raw/refs/heads/dev/docs/guide/installation.md "oh-my-opencode Installation Guide (raw)"
[18]: https://github.com/code-yeongyu/oh-my-opencode/issues/411 "Issue #411 – Sisyphus not delegating"
[19]: https://github.com/code-yeongyu/oh-my-opencode/issues/893 "Issue #893 – Primary custom agent switches back"
[20]: https://github.com/sst/opencode/issues/4439 "Issue #4439 – Subagents are using the task tool"
[21]: https://opencode.ai/config.json "OpenCode Config Schema (JSON)"
[22]: https://raw.githubusercontent.com/code-yeongyu/oh-my-opencode/master/assets/oh-my-opencode.schema.json "oh-my-opencode Schema (JSON)"
