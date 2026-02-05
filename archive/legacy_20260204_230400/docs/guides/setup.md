# WANDA System Setup Guide

This guide details the installation and configuration of the WANDA Sovereign AI OS, including the OpenCode core and the Moltbot voice gateway.

## 1. Prerequisites

*   **OS:** Linux (Ubuntu/Debian preferred) or macOS.
*   **Runtime:** Bun (latest), Node.js >= 22.
*   **Git:** Installed and configured.

## 2. Core Installation (OpenCode)

1.  **Install Bun:**
    ```bash
    curl -fsSL https://bun.sh/install | bash
    source ~/.bashrc
    ```

2.  **Install OpenCode:**
    ```bash
    bun add -g opencode@latest
    opencode --version
    ```

3.  **Install oh-my-opencode Harness:**
    ```bash
    bunx oh-my-opencode install
    # Select options: Claude=yes, OpenAI=yes, Gemini=yes
    ```

4.  **Configure Auth:**
    *   Set up `~/.antigravity/` for Google Auth Bridge.
    *   Verify `~/.config/opencode/opencode.json` contains the `oh-my-opencode` plugin.

## 3. Gateway Installation (Moltbot)

1.  **Install Moltbot:**
    ```bash
    # (Assuming npm package availability or local build)
    npm install -g moltbot
    moltbot onboard --install-daemon
    ```

2.  **Configure Gateway (`~/.clawdbot/moltbot.json`):**
    *   **Auth:** Set `gateway.auth.token` (generate a secure token).
    *   **Channels:** Configure `channels.whatsapp` with `dmPolicy: allowlist` and your number.
    *   **Tools:** Set `tools.deny: ["exec", "browser"]` for the Frontdoor agent.

3.  **Install Voice Plugin:**
    ```bash
    moltbot plugins install @moltbot/voice-call
    ```
    *   Configure Twilio/Telnyx credentials in `config`.
    *   Set `inboundPolicy: allowlist`.

## 4. Project Initialization

To start a new WANDA-compliant project:

```bash
mkdir my-new-project && cd my-new-project
opencode
# Inside OpenCode TUI:
/init-deep
```

## 5. Verification

Run the system doctor to ensure all components are wired correctly:

```bash
bunx oh-my-opencode doctor --verbose
```

**Expected Result:**
*   Model Resolution: OK
*   Providers: Connected
*   Plugins: Loaded

## 6. Known Issues & Performance Tuning

### 6.1 RAM Explosion (n8n/MCP)
Some MCP servers (like n8n or heavy Node processes) can exceed default memory limits.
*   **Fix:** Use `--max-old-space-size=2048` in your MCP configuration commands.

### 6.2 Vercel "Failed to process error response"
The local Vercel MCP server might fail with large buffers.
*   **Fix:** Use the remote bridge: `npx -y mcp-remote https://mcp.vercel.com`

### 6.3 Linux Wayland (GUI Issues)
If you experience display issues with the OpenCode TUI/GUI on Linux:
*   **Fix:** Set `ELECTRON_OZONE_PLATFORM_HINT=auto` or `wayland` in your environment variables.
