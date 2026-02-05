# Cleanup Report

Date: 2026-02-04
Scope: documentation consolidation and archiving (no deletions).

## Completed
- Archived SSOT source inputs from docs/save/ to the archive area.
- Archived duplicate guides and skill mirrors from docs/guides/.
- Archived runtime artifacts from wanda-voice/ (__pycache__ and diag.log).
- Archived local dot-directories that should not live in repo (.claude, .ruff_cache).
- Archived remaining docs/guides entries for consolidation.
- Archived local opencode.json containing secrets.
- Redacted Hostinger API tokens in archived opencode.json snapshots.

## Archive Mapping
Archive root: archive/legacy_20260204_230400/

| Source | Archived Location | Reason |
| --- | --- | --- |
| docs/save/README.md | archive/legacy_20260204_230400/docs/save/README.md | Preserve SSOT input snapshot |
| docs/save/Notizen.md | archive/legacy_20260204_230400/docs/save/Notizen.md | Preserve SSOT input snapshot |
| docs/guides/INSTALLATION.md | archive/legacy_20260204_230400/docs/guides/INSTALLATION.md | Duplicate of docs/INSTALLATION.md |
| docs/guides/AI_INSTALLATION.md | archive/legacy_20260204_230400/docs/guides/AI_INSTALLATION.md | Duplicate of docs/AI_INSTALLATION.md |
| docs/guides/AI_INSTALL_PROMPT.md | archive/legacy_20260204_230400/docs/guides/AI_INSTALL_PROMPT.md | Duplicate of docs/AI_INSTALL_PROMPT.md |
| docs/guides/WANDA_SYSTEM_STATE.md | archive/legacy_20260204_230400/docs/guides/WANDA_SYSTEM_STATE.md | Duplicate of docs/WANDA_SYSTEM_STATE.md |
| docs/guides/WANDA_FINAL_BLUEPRINT.md | archive/legacy_20260204_230400/docs/guides/WANDA_FINAL_BLUEPRINT.md | Duplicate of docs/WANDA_FINAL_BLUEPRINT.md |
| docs/guides/WANDA_HANDBOOK.html | archive/legacy_20260204_230400/docs/guides/WANDA_HANDBOOK.html | Duplicate of docs/WANDA_HANDBOOK.html |
| docs/guides/v0-scripting-mastery.yaml | archive/legacy_20260204_230400/docs/guides/v0-scripting-mastery.yaml | Duplicate of skills/v0-scripting-mastery.yaml |
| docs/guides/v0-automation-no-ai.yaml | archive/legacy_20260204_230400/docs/guides/v0-automation-no-ai.yaml | Duplicate of skills/v0-automation-no-ai.yaml |
| docs/guides/v0-agents-chatbots.yaml | archive/legacy_20260204_230400/docs/guides/v0-agents-chatbots.yaml | Duplicate of skills/v0-agents-chatbots.yaml |
| docs/guides/v0-n8n-development.yaml | archive/legacy_20260204_230400/docs/guides/v0-n8n-development.yaml | Duplicate of skills/v0-n8n-development.yaml |
| docs/guides/v0-webdevelopment.yaml | archive/legacy_20260204_230400/docs/guides/v0-webdevelopment.yaml | Duplicate of skills/v0-webdevelopment.yaml |
| wanda-voice/__pycache__ | archive/legacy_20260204_230400/runtime/wanda-voice/__pycache__ | Runtime cache artifact |
| wanda-voice/adapters/__pycache__ | archive/legacy_20260204_230400/runtime/wanda-voice/adapters/__pycache__ | Runtime cache artifact |
| wanda-voice/mobile/__pycache__ | archive/legacy_20260204_230400/runtime/wanda-voice/mobile/__pycache__ | Runtime cache artifact |
| wanda-voice/preprocess/__pycache__ | archive/legacy_20260204_230400/runtime/wanda-voice/preprocess/__pycache__ | Runtime cache artifact |
| wanda-voice/stt/__pycache__ | archive/legacy_20260204_230400/runtime/wanda-voice/stt/__pycache__ | Runtime cache artifact |
| wanda-voice/system/__pycache__ | archive/legacy_20260204_230400/runtime/wanda-voice/system/__pycache__ | Runtime cache artifact |
| wanda-voice/tts/__pycache__ | archive/legacy_20260204_230400/runtime/wanda-voice/tts/__pycache__ | Runtime cache artifact |
| wanda-voice/diag.log | archive/legacy_20260204_230400/runtime/wanda-voice/diag.log | Runtime log artifact |
| .claude/ | archive/legacy_20260204_230400/runtime/.claude | Local runtime directory |
| .ruff_cache/ | archive/legacy_20260204_230400/runtime/.ruff_cache | Local lint cache |
| docs/guides/AGENT_ROSTER.md | archive/legacy_20260204_230400/docs/guides/AGENT_ROSTER.md | Legacy agent roster snapshot |
| docs/guides/opencode.json | archive/legacy_20260204_230400/docs/guides/opencode.json | Contains secrets; archive only |
| docs/guides/oh-my-opencode.json | archive/legacy_20260204_230400/docs/guides/oh-my-opencode.json | Legacy config snapshot |
| docs/guides/system-handbook.md | archive/legacy_20260204_230400/docs/guides/system-handbook.md | Legacy handbook snapshot |
| docs/guides/setup.md | archive/legacy_20260204_230400/docs/guides/setup.md | Legacy setup guide |
| docs/guides/contributing.md | archive/legacy_20260204_230400/docs/guides/contributing.md | Legacy contribution guide |
| opencode.json | archive/legacy_20260204_230400/runtime/opencode.json | Local config containing secrets |

## Pending Candidates (Not Moved Yet)
None.

## Notes
- No files were deleted.
- Runtime files and secrets remain outside the repo boundary.
