# Installer Flow Spec (SSOT)

Last updated: 2026-02-05

Purpose: deterministic, reversible installer flow with full coverage of features, keys, and edge cases.

Sources:
- docs/AI_INSTALLATION.md
- docs/INSTALLATION.md
- docs/save/Notizen.md
- install.sh (repo root)

---

## 1) Goals

- Fresh install, reinstall, update paths
- Idempotent (safe to rerun)
- Hardware‑adaptive defaults
- Provider/Auth coverage with clear prompts
- Safe skip/back navigation at every step
- Explicit verification steps

---

## 2) Phased Flow (State Machine)

### Phase 0 — Preflight
- Detect OS, shell, package manager
- Check internet connectivity
- Validate permissions (write access to ~/.config, ~/.local, ~/.cache)
- Detect Docker availability
- Check Node/Python versions
- Show summary and confirm

### Phase 1 — Mode Selection
- Fresh install
- Reinstall (keep configs)
- Update (no destructive actions)

### Phase 2 — User Profile
- Name, workspace, language
- Confirm target paths
- Allow back/skip

### Phase 3 — Hardware Profile
- Auto‑detect RAM/VRAM/CPU
- Choose profile: S / M / M‑High / High
- Confirm or override

### Phase 4 — Provider/Auth Setup
- Choose providers (Google, Anthropic, OpenAI, etc.)
- Use `/connect` or explicit API key input
- Store in `~/.local/share/opencode/auth.json`
- Validate with `/models`

### Phase 5 — Model Assignment
- Select default mapping (from MODEL_ASSIGNMENT_MATRIX)
- Allow per‑agent overrides
- Save mapping (future: config file)

### Phase 6 — Components
- Agentic system
- Voice system
- Telegram (optional)
- Allow skip per component

### Phase 7 — MCP Setup
- Docker MCP Gateway (default)
- npx fallback
- Skip
- Verify with `docker mcp gateway status`

### Phase 8 — Ollama Setup (Local)
- Enable/disable
- Install Ollama if missing
- Pull default models (brainstorm‑36b, neo‑20b, heretic‑12b, qwen3:8b)
- Allow custom model input
- Validate with `ollama show <model>`

### Phase 9 — Finalization
- Write config files
- Create symlinks
- Run smoke checks
- Display next steps

---

## 3) Required Back/Skip Behavior

- Every phase must support:
  - Back
  - Skip (with explicit warning)
  - Retry
- Skips must be recorded in an install summary

---

## 4) Verification Checklist

- OpenCode runs: `opencode --version`
- Providers visible: `/models`
- MCP status: `docker mcp gateway status`
- Ollama running: `curl http://localhost:11434/api/tags`
- Voice components importable (python venv ok)

---

## 5) Edge Cases (Must Handle)

- BunInstallFailedError (proxy/registry/cert)
- No Docker permission / daemon not running
- GPU drivers missing or VRAM too low
- Missing Python 3.10+
- Windows path + permission quirks
- Auth key invalid or revoked
- Corporate proxy blocks downloads
- Ollama streaming NDJSON incompatibility (disable streaming if using Ollama as provider)

---

## 6) Logging & Rollback

- Install log to /tmp or ~/.local/state
- Pre‑change snapshots of configs
- Rollback mode to revert to previous configs

---

## 7) Linkage

- Model mapping: docs/SSOT/MODEL_ASSIGNMENT_MATRIX.md
- Auth strategy: docs/SSOT/AUTH_MATRIX.md
- Plugin inventory: docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md
- LSP: docs/SSOT/LSP_INVENTORY.md
