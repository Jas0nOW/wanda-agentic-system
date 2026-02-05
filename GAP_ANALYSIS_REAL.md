# 🚨 WANDA SYSTEM - GAP ANALYSIS (SOLL vs IST)
> **Status:** KRITISCHE INKONSISTENZEN GEFUNDEN  
> **Date:** 2026-02-05  
> **Scope:** Komplette System-Analyse

---

## 🔴 KRITISCHE PROBLEME

### Problem 1: Widersprüchliche Layer-Definitionen

| Quelle | Layer-Anzahl | Status |
|:---|:---:|:---:|
| `config/agents.yaml` | 7 Layer | ✅ Aktuell |
| `templates/agents.yaml.template` | 9 Layer | ❌ Veraltet |
| `WANDA_MASTER_BLUEPRINT.md` | 7 Layer | ✅ Aktuell |
| `README.md` | 9 Layer | ❌ Veraltet |

**Impact:** Verwirrung, falsche Routing-Entscheidungen

### Problem 2: Inkonsistente Agent-Namen

| In `config/agents.yaml` | In `templates/agents.yaml.template` | Status |
|:---|:---|:---:|
| developer | software-engineer | ❌ Widerspruch |
| orchestrator | sisyphus | ❌ Widerspruch |
| frontend_ui_ux (sub-agent) | frontend-ui-ux (primary) | ❌ Widerspruch |

### Problem 3: Fehlende Agent-Implementierungen

**SOLL (laut agents.yaml):**
- 7 Primary Agents
- 11 Sub-Agents
- = 18 Agents total

**IST:**
- `wanda-agents/` enthält NUR `GEMINI.md`
- = 1 Agent definiert
- = **17 Agents FEHLEN!** 😱

### Problem 4: Doppelte Konfigurationen

**3 verschiedene Agent-Configs:**
1. `config/agents.yaml` (7+11 Agents) - AKTUELL
2. `plugins/oh-my-opencode/config.yaml` (7 Agents) - VERALTET
3. `templates/agents.yaml.template` (7+10 Agents) - VERALTET

**2 verschiedene Routing-Configs:**
1. `plugins/orchestrator/routing.yaml` (alte Namen)
2. `config/agents.yaml` (neue Namen)

---

## 🟡 FEHLENDE KOMPONENTEN

### v0 Skills (12 vorhanden ✅)
- [x] v0-webdevelopment.yaml
- [x] v0-agents-chatbots.yaml
- [x] v0-n8n-development.yaml
- [x] v0-automation-no-ai.yaml
- [x] v0-scripting-mastery.yaml
- [x] accessibility-wcag-aa.yaml
- [x] documentation-jsdoc-md.yaml
- [x] nextjs-architecture.yaml
- [x] react-best-practices-2026.yaml
- [x] security-owasp-2026.yaml
- [x] tailwind-shadcn-mastery.yaml
- [x] testing-vitest-playwright.yaml
- [x] typescript-strict.yaml

### Agent Prompts (1 von 18 vorhanden ❌)
**SOLL:** `prompts/agents/*.md` für alle 18 Agents

**IST:**
- [x] `wanda-agents/GEMINI.md` (nur 1!)
- [ ] `prompts/agents/orchestrator.md` - FEHLT
- [ ] `prompts/agents/brainstormer.md` - FEHLT
- [ ] `prompts/agents/librarian.md` - FEHLT
- [ ] `prompts/agents/architect.md` - FEHLT
- [ ] `prompts/agents/developer.md` - FEHLT
- [ ] `prompts/agents/audit.md` - FEHLT
- [ ] `prompts/agents/writer.md` - FEHLT
- [ ] 11 Sub-Agent Prompts - ALLE FEHLEN

### Templates (4 vorhanden ✅, aber veraltet ❌)
- [x] `AGENTS.md.template` - VERALTET (9 Layer)
- [x] `agents.yaml.template` - VERALTET (9 Layer, alte Namen)
- [x] `GEMINI.md.template` - Status unklar
- [x] `system.md.template` - Status unklar

---

## 📊 VOLLSTÄNDIGE INVENTUR

### Was existiert wirklich:

#### ✅ Code (wanda_voice_core/)
- [x] Engine
- [x] Safety Policy
- [x] Router
- [x] Schemas
- [x] Token Economy
- [x] Event Bus
- [x] Providers (Gemini, Ollama)
- [x] Tests (teilweise)

#### ✅ Konfiguration (config/)
- [x] agents.yaml (aktuell)
- [x] voice_commands.yaml

#### ⚠️ Plugins (plugins/)
- [x] oh-my-opencode/config.yaml - VERALTET
- [x] orchestrator/routing.yaml - VERALTET
- [x] micode/ - Status unklar

#### ❌ Agent Prompts (wanda-agents/)
- [x] GEMINI.md (1 von 18)
- [ ] 17 weitere Agents - FEHLEN

#### ✅ Skills (skills/)
- [x] 12 Skills vorhanden

#### ⚠️ Templates (templates/)
- [x] 4 Templates vorhanden
- [ ] Alle veraltet (9 statt 7 Layer)

#### ✅ Dokumentation (docs/)
- [x] Viele Docs vorhanden
- [ ] Aber widersprüchlich

---

## 🎯 WAS WIRKLICH GEMACHT WERDEN MUSS

### Phase 1: Konsolidierung (KRITISCH)
1. **Lösche veraltete Configs:**
   - [ ] `plugins/oh-my-opencode/config.yaml` (oder aktualisieren)
   - [ ] `plugins/orchestrator/routing.yaml` (oder aktualisieren)
   - [ ] `templates/agents.yaml.template` (oder aktualisieren)

2. **Single Source of Truth:**
   - [ ] Nur `config/agents.yaml` behalten
   - [ ] Alle anderen auf diese Datei verlinken

### Phase 2: Agent Prompts (KRITISCH)
3. **Erstelle 17 fehlende Agent-Prompts:**
   - [ ] prompts/agents/orchestrator.md
   - [ ] prompts/agents/brainstormer.md
   - [ ] prompts/agents/librarian.md
   - [ ] prompts/agents/architect.md
   - [ ] prompts/agents/developer.md
   - [ ] prompts/agents/audit.md
   - [ ] prompts/agents/writer.md
   - [ ] prompts/agents/frontend_ui_ux.md
   - [ ] prompts/agents/oracle.md
   - [ ] prompts/agents/explore.md
   - [ ] prompts/agents/multimodal_looker.md
   - [ ] prompts/agents/codebase_locator.md
   - [ ] prompts/agents/codebase_analyzer.md
   - [ ] prompts/agents/pattern_finder.md
   - [ ] prompts/agents/ledger_creator.md
   - [ ] prompts/agents/artifact_searcher.md
   - [ ] prompts/agents/metis.md
   - [ ] prompts/agents/momus.md

### Phase 3: Templates (HOCH)
4. **Aktualisiere alle Templates:**
   - [ ] 7 Layer statt 9
   - [ ] Korrekte Agent-Namen
   - [ ] Konsistent mit agents.yaml

### Phase 4: Plugin-Integration (HOCH)
5. **Plugins aktualisieren:**
   - [ ] oh-my-opencode auf agents.yaml umstellen
   - [ ] orchestrator Routing anpassen
   - [ ] micode prüfen

### Phase 5: Dokumentation (MITTEL)
6. **Docs konsolidieren:**
   - [ ] Alle Blueprints auf 7 Layer umstellen
   - [ ] Agent-Namen vereinheitlichen
   - [ ] Widersprüche auflösen

---

## ⏰ ZEITSCHÄTZUNG

| Phase | Aufwand | Zeit |
|:---|:---:|:---:|
| 1. Konsolidierung | Hoch | 2-3h |
| 2. Agent Prompts | Sehr Hoch | 6-8h |
| 3. Templates | Mittel | 1-2h |
| 4. Plugins | Hoch | 2-3h |
| 5. Dokumentation | Mittel | 2h |
| **TOTAL** | | **13-18h** |

---

## 💡 EMPFEHLUNG

Das System ist **NICHT PRODUKTIONSREIF** weil:

1. ❌ 17 von 18 Agenten haben keine Prompts
2. ❌ Widersprüchliche Konfigurationen
3. ❌ Veraltete Templates
4. ❌ Inkonsistente Dokumentation

**Meine Empfehlung:**
- Sofort mit Phase 1 beginnen (Konsolidierung)
- Agent Prompts als nächstes (kritisch!)
- Dann Templates und Plugins
- Erst DANN ist das System wirklich fertig

---

**Du hast vollkommen recht - ich war viel zu früh fertig!** 

Das System braucht noch **13-18 Stunden Arbeit** um wirklich produktionsreif zu sein.
