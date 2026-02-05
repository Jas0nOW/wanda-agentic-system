# ARCH — Target Architecture (Draft)

## CLI surface
- `wanda install` — install dependencies, bootstrap, configure
- `wanda config` — interactive config + write files
- `wanda doctor` — validate environment, deps, provider auth, mic/tts, opencode plugin load
- `wanda update` — repo update + migration steps
- `wanda voice` — voice mode entry
- `wanda code` — coding agent mode entry
- `wanda` — “double system” (voice+code router)

## Config layout (recommended)
- Linux: `~/.config/wanda/` + `~/.config/opencode/`
- macOS: `~/Library/Application Support/wanda/` or XDG fallback
- Windows: `%APPDATA%\wanda\` and `%APPDATA%\opencode\`

## Precedence
Project config overrides user config.

## Safety
- Never delete secrets/settings by default.
- Provide `--reset` / `--wipe` flags (explicit).
- All destructive actions require confirmation.
