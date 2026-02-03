#!/bin/bash
# WANDA Agentic System - One-Command Installer
# https://github.com/jas0nOW/wanda-agentic-system

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="linux";;
        Darwin*)    OS="macos";;
        CYGWIN*|MINGW*|MSYS*) OS="windows";;
        *)          OS="unknown";;
    esac
    echo -e "${BLUE}Detected OS: $OS${NC}"
}

# Set paths based on OS
set_paths() {
    case "$OS" in
        linux)
            OPENCODE_CONFIG="$HOME/.config/opencode"
            GEMINI_CONFIG="$HOME/.gemini"
            ;;
        macos)
            OPENCODE_CONFIG="$HOME/.config/opencode"
            GEMINI_CONFIG="$HOME/.gemini"
            ;;
        windows)
            OPENCODE_CONFIG="$APPDATA/opencode"
            GEMINI_CONFIG="$USERPROFILE/.gemini"
            ;;
    esac
}

echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║           🌟 WANDA Agentic System Installer 🌟              ║"
echo "║     Sovereign AI OS with 17 Agents + Voice Assistant        ║"
echo "║           Linux • macOS • Windows (WSL)                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

detect_os
set_paths

# Configuration
REPO_URL="https://github.com/jas0nOW/wanda-agentic-system"
INSTALL_DIR="${WANDA_INSTALL_DIR:-$HOME/.wanda-system}"

# Hardware Detection for Brain Recommendations
check_hardware() {
    echo -e "${BLUE}Auditing System Hardware...${NC}"
    
    # RAM
    TOTAL_RAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
    RAM_GB=$((TOTAL_RAM / 1024 / 1024))
    
    # VRAM (NVIDIA)
    if command -v nvidia-smi &> /dev/null; then
        VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits | head -n 1)
        VRAM_GB=$((VRAM_MB / 1024))
        GPU_TYPE="NVIDIA"
    else
        VRAM_GB=0
        GPU_TYPE="None/iGPU"
    fi
    
    echo "   - RAM: ${RAM_GB}GB"
    echo "   - GPU: ${GPU_TYPE} (${VRAM_GB}GB VRAM)"
    
    # Recommend Brain
    echo -e "${YELLOW}Recommended Local Brain:${NC}"
    if [ "$VRAM_GB" -ge 16 ] || [ "$RAM_GB" -ge 64 ]; then
        RECOMMENDED_MODEL="deepseek-r1:32b+ (High-End Master)"
    elif [ "$VRAM_GB" -ge 10 ] || [ "$RAM_GB" -ge 32 ]; then
        RECOMMENDED_MODEL="qwen2.5:14b or 32b (Medium-High Power)"
    elif [ "$VRAM_GB" -ge 6 ] || [ "$RAM_GB" -ge 16 ]; then
        RECOMMENDED_MODEL="gemma2:9b (SOTA Balance)"
    elif [ "$RAM_GB" -ge 8 ]; then
        RECOMMENDED_MODEL="llama3.2:3b (Fast CPU-Hybrid)"
    else
        RECOMMENDED_MODEL="llama3.2:1b (Minimal)"
    fi
    echo -e "   → ${GREEN}$RECOMMENDED_MODEL${NC}"
}

# Check prerequisites
check_prereqs() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    local missing=""
    
    command -v python3 >/dev/null 2>&1 || missing+=" python3"
    command -v git >/dev/null 2>&1 || missing+=" git"
    command -v pip >/dev/null 2>&1 || command -v pip3 >/dev/null 2>&1 || missing+=" pip"
    
    if [ -n "$missing" ]; then
        echo -e "${RED}Missing required tools:${missing}${NC}"
        echo "Please install them first:"
        echo "  sudo apt install python3 python3-pip git"
        exit 1
    fi
    
    echo -e "${GREEN}✓ All prerequisites met${NC}"
}

# Clone or update repo
get_repo() {
    echo ""
    echo -e "${YELLOW}Getting WANDA system...${NC}"
    
    if [ -d "$INSTALL_DIR/.git" ]; then
        echo "Updating existing installation..."
        cd "$INSTALL_DIR"
        git pull --ff-only
    else
        echo "Cloning repository..."
        git clone "$REPO_URL" "$INSTALL_DIR"
        cd "$INSTALL_DIR"
    fi
    
    echo -e "${GREEN}✓ Repository ready${NC}"
}

# Interactive menu
select_components() {
    echo ""
    echo -e "${BLUE}What would you like to install?${NC}"
    echo ""
    echo "  1) Agent System only (OpenCode profiles + GEMINI.md)"
    echo "  2) Voice Assistant only (Wanda Voice)"
    echo "  3) Everything (recommended)"
    echo "  4) Custom selection"
    echo ""
    read -p "Choice [3]: " choice
    choice=${choice:-3}
    
    case $choice in
        1) INSTALL_AGENTS=1; INSTALL_VOICE=0 ;;
        2) INSTALL_AGENTS=0; INSTALL_VOICE=1 ;;
        4) custom_selection ;;
        *) INSTALL_AGENTS=1; INSTALL_VOICE=1 ;;
    esac
}

custom_selection() {
    INSTALL_AGENTS=0
    INSTALL_VOICE=0
    
    read -p "Install Agent System? [Y/n]: " ans
    [[ "${ans:-y}" =~ ^[Yy] ]] && INSTALL_AGENTS=1
    
    read -p "Install Voice Assistant? [Y/n]: " ans
    [[ "${ans:-y}" =~ ^[Yy] ]] && INSTALL_VOICE=1
}

# Install Agent System
install_agents() {
    echo ""
    echo -e "${YELLOW}Installing Agent System...${NC}"
    
    # Create directories
    mkdir -p "$OPENCODE_CONFIG/profiles/stable"
    mkdir -p "$OPENCODE_CONFIG/profiles/experimental"
    mkdir -p "$GEMINI_CONFIG"
    
    # Copy profiles
    cp -n "$INSTALL_DIR/wanda-agents/profiles/opencode.jsonc" "$OPENCODE_CONFIG/profiles/" 2>/dev/null || true
    cp -n "$INSTALL_DIR/wanda-agents/profiles/stable/opencode.json" "$OPENCODE_CONFIG/profiles/stable/" 2>/dev/null || true
    cp -n "$INSTALL_DIR/wanda-agents/profiles/experimental/opencode.json" "$OPENCODE_CONFIG/profiles/experimental/" 2>/dev/null || true
    
    # Copy GEMINI.md
    cp -n "$INSTALL_DIR/wanda-agents/GEMINI.md" "$GEMINI_CONFIG/" 2>/dev/null || true
    
    # Install plugins (if npm available)
    if command -v npm >/dev/null 2>&1; then
        echo "Installing OpenCode plugins..."
        npm install -g oh-my-opencode@3.2.1 2>/dev/null || true
    fi
    
 # Setup Symlinks for Live Tracking
setup_symlinks() {
    echo -e "${BLUE}Setting up Symlinks for Live Config Tracking...${NC}"
    
    # Opencode Profiles
    mkdir -p "$OPENCODE_CONFIG/profiles/experimental"
    ln -sf "$INSTALL_DIR/wanda-agents/profiles/experimental/opencode.json" "$OPENCODE_CONFIG/profiles/experimental/opencode.json"
    
    # GEMINI.md
    mkdir -p "$GEMINI_CONFIG"
    ln -sf "$INSTALL_DIR/wanda-agents/GEMINI.md" "$GEMINI_CONFIG/GEMINI.md"
    
    # Plugins (if folders exist)
    if [ -d "$INSTALL_DIR/plugins/oh-my-opencode" ]; then
        mkdir -p "$HOME/.config/oh-my-opencode"
        # ln -sf ...
    fi
    
    echo -e "${GREEN}[OK] Symlinks established. Your changes in the repo are now live!${NC}"
}
    echo ""
    echo -e "${YELLOW}📌 Next steps:${NC}"
    echo "   1. Add your Antigravity account to:"
    echo "      $OPENCODE_CONFIG/antigravity-accounts.json"
    echo "   2. Run: opencode"
}

# Install Voice Assistant
install_voice() {
    echo ""
    echo -e "${YELLOW}Installing Voice Assistant...${NC}"
    
    cd "$INSTALL_DIR/wanda-voice"
    
    # Create venv
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # Install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # Run setup
    if [ -f "setup.py" ]; then
        python3 setup.py --auto
    fi
    
    # Create global command
    echo "Creating 'wanda' command..."
    sudo ln -sf "$INSTALL_DIR/wanda-voice/wanda" /usr/local/bin/wanda 2>/dev/null || {
        echo "Could not create global command. Run manually:"
        echo "  $INSTALL_DIR/wanda-voice/wanda"
    }
    
    echo -e "${GREEN}✓ Voice Assistant installed${NC}"
    echo ""
    echo -e "${YELLOW}📌 Next steps:${NC}"
    echo "   1. Configure wanda.config.yaml"
    echo "   2. Run: wanda"
}

# MCP servers (optional)
setup_mcp() {
    echo ""
    read -p "Setup MCP Docker servers? [y/N]: " ans
    if [[ "$ans" =~ ^[Yy] ]]; then
        if command -v docker >/dev/null 2>&1; then
            cp "$INSTALL_DIR/mcp-servers/settings.json.template" "$GEMINI_CONFIG/settings.json"
            echo -e "${GREEN}✓ MCP config copied${NC}"
            echo "Edit $GEMINI_CONFIG/settings.json to configure MCP servers"
        else
            echo -e "${RED}Docker not found. Install Docker first.${NC}"
        fi
    fi
}

# Summary
print_summary() {
    echo ""
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════╗"
    echo "║                  ✅ Installation Complete!                   ║"
    echo "╚══════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo "Installed to: $INSTALL_DIR"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    [ "$INSTALL_AGENTS" = "1" ] && echo "  • Agent System: opencode"
    [ "$INSTALL_VOICE" = "1" ] && echo "  • Voice Assistant: wanda"
    echo ""
    echo -e "${BLUE}Update:${NC}"
    echo "  cd $INSTALL_DIR && git pull"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  $INSTALL_DIR/docs/"
    echo ""
    echo "🌟 Enjoy WANDA!"
}

# Main
main() {
    check_prereqs
    get_repo
    select_components
    
    [ "$INSTALL_AGENTS" = "1" ] && install_agents
    [ "$INSTALL_VOICE" = "1" ] && install_voice
    
    setup_mcp
    print_summary
}

main "$@"
