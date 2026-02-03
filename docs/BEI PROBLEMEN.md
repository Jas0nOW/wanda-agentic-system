# WICHTIGE RESEARCHES BEI PROBLEMEN

OPENCODE CONFIGURE:

https://opencode.ai/docs/plugins/
https://opencode.ai/docs/tools/
https://opencode.ai/docs/rules/
https://opencode.ai/docs/agents/
https://opencode.ai/docs/models/
https://opencode.ai/docs/formatters/
https://opencode.ai/docs/permissions/
https://opencode.ai/docs/lsp/
https://opencode.ai/docs/mcp-servers/
https://opencode.ai/docs/acp/
https://opencode.ai/docs/skills/
https://opencode.ai/docs/custom-tools/


OHMYOPENCODE CONFIGURE:

https://ohmyopencode.com/documentation/
https://ohmyopencode.com/configuration/
https://ohmyopencode.com/features/


MICODE CONFIGURE:

https://github.com/vtemian/micode?tab=readme-ov-file


OPENCODE-ORCHESTRATOR:

https://www.npmjs.com/package/opencode-orchestrator

---

Plugin-Reihenfolge & doppelte Installationen
OpenCode lädt Plugins aus mehreren Quellen (Global config → Project config → globale Plugin-Dir → Projekt-Plugin-Dir). Hooks laufen sequenziell; gleiches npm-Paket (Name+Version) nur einmal, aber lokales Plugin + npm-Plugin werden beide geladen. Das kann “doppelte” Effekte machen.