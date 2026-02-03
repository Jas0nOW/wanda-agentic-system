#!/bin/bash
# ==============================================================================
# WANDA Unified Installer v2.0 - install.sh
# ==============================================================================
# Complete installation: Dependencies, Configs, Plugins, Symlinks, Services.
# Places ALL files in the correct locations.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
CONFIG_DIR="$HOME/.config/opencode"
WANDA_CONFIG_DIR="$HOME/.config/wanda"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
MAGENTA='\033[0;35m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }
log_section() { echo -e "\n${MAGENTA}═══════════════════════════════════════════════════════════${NC}"; echo -e "${MAGENTA}  $1${NC}"; echo -e "${MAGENTA}═══════════════════════════════════════════════════════════${NC}\n"; }

# ==============================================================================
# STEP 1: Hardware Detection
# ==============================================================================
detect_hardware() {
    log_section "STEP 1: Hardware Detection"
    
    TOTAL_RAM_GB=$(free -g | awk '/^Mem:/{print $2}')
    
    if command -v nvidia-smi &> /dev/null; then
        GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -1)
        GPU_MEM_GB=$((GPU_MEM / 1024))
        log_info "NVIDIA GPU detected: ${GPU_MEM_GB}GB VRAM"
    else
        GPU_MEM_GB=0
        log_warn "No NVIDIA GPU detected. Using CPU mode."
    fi
    
    # Determine Tier
    if [ "$TOTAL_RAM_GB" -ge 64 ]; then
        TIER="G"; OLLAMA_MODEL="deepseek-v4"; TTS_PROFILE="premium"
    elif [ "$TOTAL_RAM_GB" -ge 40 ]; then
        TIER="MH"; OLLAMA_MODEL="brainstorm-36b"; TTS_PROFILE="premium"
    elif [ "$TOTAL_RAM_GB" -ge 16 ]; then
        TIER="M"; OLLAMA_MODEL="heretic-12b"; TTS_PROFILE="medium"
    else
        TIER="S"; OLLAMA_MODEL="qwen3:8b"; TTS_PROFILE="low"
    fi
    
    log_success "RAM: ${TOTAL_RAM_GB}GB | VRAM: ${GPU_MEM_GB}GB"
    log_success "System Tier: $TIER | Model: $OLLAMA_MODEL | TTS: $TTS_PROFILE"
}

# ==============================================================================
# STEP 2: Install Dependencies
# ==============================================================================
install_dependencies() {
    log_section "STEP 2: Installing Dependencies"
    
    # Python
    if ! command -v python3 &> /dev/null; then
        log_info "Installing Python..."
        sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv
    else
        log_success "Python3: $(python3 --version)"
    fi
    
    # Node.js
    if ! command -v node &> /dev/null; then
        log_info "Installing Node.js..."
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
        sudo apt-get install -y nodejs
    else
        log_success "Node.js: $(node --version)"
    fi
    
    # Bun
    if ! command -v bun &> /dev/null; then
        log_info "Installing Bun..."
        curl -fsSL https://bun.sh/install | bash
        export PATH="$HOME/.bun/bin:$PATH"
    else
        log_success "Bun: $(bun --version)"
    fi
    
    # Ollama
    if ! command -v ollama &> /dev/null; then
        log_info "Installing Ollama..."
        curl -fsSL https://ollama.com/install.sh | sh
    else
        log_success "Ollama: installed"
    fi
    
    # Docker
    if ! command -v docker &> /dev/null; then
        log_info "Installing Docker..."
        curl -fsSL https://get.docker.com | sh
        sudo usermod -aG docker $USER
    else
        log_success "Docker: $(docker --version | cut -d ' ' -f 3)"
    fi
}

# ==============================================================================
# STEP 3: Install OpenCode & Plugins
# ==============================================================================
install_opencode() {
    log_section "STEP 3: Installing OpenCode & Plugins"
    
    if ! command -v opencode &> /dev/null; then
        log_info "Installing OpenCode..."
        npm install -g opencode
    else
        log_success "OpenCode: already installed"
    fi
    
    log_info "Installing oh-my-opencode..."
    bunx oh-my-opencode install || log_warn "oh-my-opencode install had issues, continuing..."
    
    log_success "OpenCode setup complete."
}

# ==============================================================================
# STEP 4: Create Directory Structure & Symlinks
# ==============================================================================
setup_configs() {
    log_section "STEP 4: Setting up Configs & Symlinks"
    
    # Create directories
    mkdir -p "$CONFIG_DIR"
    mkdir -p "$WANDA_CONFIG_DIR"
    mkdir -p "$CONFIG_DIR/plugins"
    mkdir -p "$CONFIG_DIR/skills"
    mkdir -p "$CONFIG_DIR/command"
    mkdir -p "$SYSTEMD_USER_DIR"
    
    # ─────────────────────────────────────────────────────────────────────────
    # OpenCode Config (MAIN)
    # ─────────────────────────────────────────────────────────────────────────
    log_info "Symlinking OpenCode profile (stable)..."
    ln -sf "$REPO_DIR/wanda_cloud/profiles/stable/opencode.jsonc" "$CONFIG_DIR/opencode.jsonc"
    
    # ─────────────────────────────────────────────────────────────────────────
    # Prompts & System Files
    # ─────────────────────────────────────────────────────────────────────────
    log_info "Symlinking system prompts..."
    ln -sf "$REPO_DIR/prompts" "$WANDA_CONFIG_DIR/prompts"
    
    # ─────────────────────────────────────────────────────────────────────────
    # Skills Directory
    # ─────────────────────────────────────────────────────────────────────────
    if [ -d "$REPO_DIR/wanda_cloud/skills" ]; then
        log_info "Symlinking skills..."
        for skill in "$REPO_DIR/wanda_cloud/skills"/*; do
            if [ -d "$skill" ]; then
                skill_name=$(basename "$skill")
                ln -sf "$skill" "$CONFIG_DIR/skills/$skill_name"
            fi
        done
    fi
    
    # ─────────────────────────────────────────────────────────────────────────
    # WANDA Local Config
    # ─────────────────────────────────────────────────────────────────────────
    log_info "Writing WANDA local config..."
    cat > "$WANDA_CONFIG_DIR/config.json" << EOF
{
    "version": "1.0.0",
    "tier": "$TIER",
    "ollama_model": "$OLLAMA_MODEL",
    "tts_profile": "$TTS_PROFILE",
    "repo_path": "$REPO_DIR",
    "voice_gateway": {
        "enabled": true,
        "stt_model": "large-v3-turbo",
        "vad_threshold_ms": 200
    },
    "telegram": {
        "enabled": true,
        "bot_name": "@wandavoice_bot"
    }
}
EOF
    
    log_success "All configs and symlinks created."
}

# ==============================================================================
# STEP 5: Install Python Dependencies
# ==============================================================================
install_python_deps() {
    log_section "STEP 5: Installing Python Voice Gateway"
    
    cd "$REPO_DIR/wanda_local"
    
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    
    pip install --upgrade pip -q
    pip install -q \
        faster-whisper \
        torch \
        numpy \
        sounddevice \
        soundfile \
        httpx \
        python-telegram-bot \
        python-dotenv
    
    if [ "$TTS_PROFILE" = "premium" ]; then
        log_info "Installing XTTS-v2 (Premium TTS)..."
        pip install -q TTS || log_warn "TTS install failed, using fallback."
    fi
    
    deactivate
    log_success "Python dependencies installed."
}

# ==============================================================================
# STEP 6: Pull Ollama Model
# ==============================================================================
pull_ollama_model() {
    log_section "STEP 6: Pulling Ollama Model"
    
    if ollama list | grep -q "$OLLAMA_MODEL"; then
        log_success "Model $OLLAMA_MODEL already present."
    else
        log_info "Pulling $OLLAMA_MODEL (this may take a while)..."
        ollama pull "$OLLAMA_MODEL" || log_warn "Model pull failed. Pull manually: ollama pull $OLLAMA_MODEL"
    fi
}

# ==============================================================================
# STEP 7: Create Systemd Services (Auto-Start)
# ==============================================================================
setup_systemd() {
    log_section "STEP 7: Setting up Auto-Start Services"
    
    # ─────────────────────────────────────────────────────────────────────────
    # Ollama Service (usually managed by system, but ensure it starts)
    # ─────────────────────────────────────────────────────────────────────────
    log_info "Ensuring Ollama starts on boot..."
    sudo systemctl enable ollama 2>/dev/null || log_warn "Ollama systemd not available."
    
    # ─────────────────────────────────────────────────────────────────────────
    # WANDA Voice Gateway Service
    # ─────────────────────────────────────────────────────────────────────────
    log_info "Creating WANDA Voice Gateway service..."
    cat > "$SYSTEMD_USER_DIR/wanda-voice.service" << EOF
[Unit]
Description=WANDA Voice Gateway
After=network.target ollama.service

[Service]
Type=simple
WorkingDirectory=$REPO_DIR/wanda_local
ExecStart=$REPO_DIR/wanda_local/venv/bin/python $REPO_DIR/wanda_local/main.py
Restart=on-failure
RestartSec=5
Environment="PATH=$REPO_DIR/wanda_local/venv/bin:/usr/bin"

[Install]
WantedBy=default.target
EOF

    # ─────────────────────────────────────────────────────────────────────────
    # WANDA Telegram Bot Service
    # ─────────────────────────────────────────────────────────────────────────
    log_info "Creating WANDA Telegram Bot service..."
    cat > "$SYSTEMD_USER_DIR/wanda-telegram.service" << EOF
[Unit]
Description=WANDA Telegram Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=$REPO_DIR/wanda_local
ExecStart=$REPO_DIR/wanda_local/venv/bin/python $REPO_DIR/wanda_local/telegram_bot.py
Restart=on-failure
RestartSec=5
Environment="PATH=$REPO_DIR/wanda_local/venv/bin:/usr/bin"

[Install]
WantedBy=default.target
EOF

    # Reload and enable
    systemctl --user daemon-reload
    systemctl --user enable wanda-voice.service 2>/dev/null || true
    systemctl --user enable wanda-telegram.service 2>/dev/null || true
    
    log_success "Systemd services created. Enable with:"
    log_info "  systemctl --user start wanda-voice"
    log_info "  systemctl --user start wanda-telegram"
}

# ==============================================================================
# STEP 8: Prevent PC Sleep (Power Settings)
# ==============================================================================
setup_power() {
    log_section "STEP 8: Configuring Power Settings"
    
    # Disable suspend on lid close (if laptop)
    if [ -f /etc/systemd/logind.conf ]; then
        log_info "Configuring to prevent sleep when WANDA is active..."
        log_warn "To prevent PC sleep, run: sudo systemctl mask sleep.target suspend.target hibernate.target hybrid-sleep.target"
    fi
    
    # Create a caffeine script
    cat > "$REPO_DIR/scripts/keep-awake.sh" << 'EOF'
#!/bin/bash
# Keep system awake while WANDA services are running
# Run this script in background: nohup ./keep-awake.sh &

echo "[WANDA] Keeping system awake..."
while true; do
    # Simulate user activity to prevent sleep
    xdotool key --clearmodifiers shift 2>/dev/null || true
    # Alternative: Use caffeine-ng or systemd-inhibit
    sleep 300  # Every 5 minutes
done
EOF
    chmod +x "$REPO_DIR/scripts/keep-awake.sh"
    
    log_success "Power configuration complete."
}

# ==============================================================================
# MAIN
# ==============================================================================
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║       WANDA Sovereign AI OS - Unified Installer v2.0             ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo ""
    
    detect_hardware
    install_dependencies
    install_opencode
    setup_configs
    install_python_deps
    pull_ollama_model
    setup_systemd
    setup_power
    
    echo ""
    log_section "INSTALLATION COMPLETE!"
    echo ""
    echo "┌─────────────────────────────────────────────────────────────────────┐"
    echo "│  Quick Start Commands:                                              │"
    echo "├─────────────────────────────────────────────────────────────────────┤"
    echo "│  Start Voice Gateway:                                               │"
    echo "│    systemctl --user start wanda-voice                               │"
    echo "│                                                                     │"
    echo "│  Start Telegram Bot:                                                │"
    echo "│    systemctl --user start wanda-telegram                            │"
    echo "│                                                                     │"
    echo "│  Open Dashboard:                                                    │"
    echo "│    xdg-open $REPO_DIR/docs/WANDA_HANDBOOK.html                      │"
    echo "│                                                                     │"
    echo "│  Switch to Experimental Profile:                                    │"
    echo "│    ln -sf $REPO_DIR/wanda_cloud/profiles/experimental/opencode.jsonc ~/.config/opencode/opencode.jsonc │"
    echo "└─────────────────────────────────────────────────────────────────────┘"
    echo ""
    echo "Config locations:"
    echo "  OpenCode: $CONFIG_DIR/opencode.jsonc"
    echo "  WANDA:    $WANDA_CONFIG_DIR/config.json"
    echo "  Prompts:  $WANDA_CONFIG_DIR/prompts/"
    echo ""
}

main "$@"
