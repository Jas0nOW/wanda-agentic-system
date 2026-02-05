# SSOT Inventory

| Path | Zweck | Kernaussagen | Abhaengigkeiten | Offene Fragen / Konflikte |
| --- | --- | --- | --- | --- |
| `README.md` | Einstieg, Doku-Index | SSOT-Struktur, Quickstart, `/ralph-loop` | OpenCode, `.v0` | `/ralph-loop` Quelle/Plugin unklar |
| `docs/01.02 - DeepResearch.md` | Vorab-SSOT Plan | Implementation-Plan, Coverage, Konflikte | OpenCode, MCP, `.v0` | Enthält Annahmen/Links, nicht final |
| `docs/WANDA_FINAL_BLUEPRINT.md` | Master Blueprint | Roster, Skills, Frontdoor, 8-Phasen | OpenCode, Moltbot | Fallback-Logik vs B1; `~/.v0` vs `.v0/` |
| `docs/WANDA_HANDBOOK.html` | Gesamtbeschreibung | Commander primary, Skill Registry, Gateway | OpenCode | Modellnamen teils als Labels |
| `docs/BEI PROBLEMEN.md` | Troubleshooting Links | OpenCode/Plugin Links, Plugin Load Order | Web-Quellen | Redundanz zu Blueprint |
| `docs/workflows/wanda-lifecycle.md` | Prozess | 8-Phasen-Workflow, Agents je Phase | OpenCode | Muss SSOT-Policy werden |
| `docs/guides/setup.md` | Setup | Bun/Node, OpenCode, Moltbot, Doctor | Bun, Node, Moltbot | Kommandos/Versionen verifizieren |
| `docs/guides/contributing.md` | Governance | Patch Protocol, Fix-Loop, Secrets | Git, Lint/Test | Regeln in Skills/Gates spiegeln |
| `docs/architecture/vision.md` | Vision | v0-fuer-alles, Skills, Frontdoor | `.v0`, Moltbot | Konkrete Artefakte festlegen |
| `docs/architecture/technical.md` | Architektur | `.v0/` Struktur, Runner, Memory | `.v0` | Konflikt zu `~/.v0` |
| `docs/architecture/agents.md` | Agents | Commander primary, Dual-Quota, MCPs | OpenCode Plugins | Fallback-Chain vs B1 |
| `docs/architecture/agent-roster.md` | Roster | Commander primary, Subagenten, deaktivierte Main | MiCode, oh-my-opencode | Muss kanonisch bleiben |
| `docs/architecture/plugin-standards.md` | Plugin Inventar | 15 Plugins, Defaults, Konflikte | OpenCode Plugins | opencode-orchestrator Bedeutung |
| `docs/research/research-agent-architecture.md` | Research | 7-Layer Modell, Security | MCP | Konzeptual, nicht SSOT |
| `docs/research/research-agent-creation-guide.md` | Research | Agent-Build Playbook | MCP, LangChain | Konzeptual |
| `docs/research/research-agent-reduction.md` | Research | Reduzierte Flotte (14) | oh-my-opencode | Konflikt zu Roster/Template |
| `docs/research/research-opencode-analysis.md` | Research | OpenCode/oh-my-opencode Analyse | OpenCode Docs | Tool-Sprawl, Orchestrator-Konflikt |
| `docs/research/research-plugin-analysis.md` | Research | Plugin/Agent Analyse | OpenCode Ecosystem | SSOT-Entscheidungen ableiten |
| `docs/research/research-sota-optimization.md` | Research | Konsolidierung, MCP Audit | MCP | Empfehlungen in SSOT ueberfuehren |
| `docs/research/research-v0-builder-platform.md` | Research | v0 Skills, Contracts, Router | `.v0` | Umsetzung in echte Struktur |
| `docs/research/research-voice-gateway.md` | Research | Voice Gateway Specs | Moltbot/Clawdbot | Rebrand/CLI verifizieren |
| `docs/research/research-sources.md` | Research | Quellenliste | Web | Dedup + Aktualisierung |
| `templates/AGENTS.md.template` | Template | 17 Agents, Sisyphus orchestrator | oh-my-opencode | Widerspricht Roster |
