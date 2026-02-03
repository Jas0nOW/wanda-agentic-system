#!/bin/bash
# ==============================================================================
# WANDA Agentic System - One-Command Installer
# https://github.com/jas0nOW/wanda-agentic-system
# ==============================================================================
# PERSONALIZED INSTALLATION - Asks for user name and workspace folder
# ==============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
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

# Banner
print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                          ║"
    echo "║   ██╗    ██╗ █████╗ ███╗   ██╗██████╗  █████╗                            ║"
    echo "║   ██║    ██║██╔══██╗████╗  ██║██╔══██╗██╔══██╗                           ║"
    echo "║   ██║ █╗ ██║███████║██╔██╗ ██║██║  ██║███████║                           ║"
    echo "║   ██║███╗██║██╔══██║██║╚██╗██║██║  ██║██╔══██║                           ║"
    echo "║   ╚███╔███╔╝██║  ██║██║ ╚████║██████╔╝██║  ██║                           ║"
    echo "║    ╚══╝╚══╝ ╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝                           ║"
    echo "║                                                                          ║"
    echo "║        Sovereign AI OS • 7 Primary Agents • 7 Layers • 7 MCP             ║"
    echo "║                                                                          ║"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# ══════════════════════════════════════════════════════════════════════════════
# PERSONALIZATION - Ask for user-specific configuration
# ══════════════════════════════════════════════════════════════════════════════

collect_user_info() {
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}                  PERSONALIZATION SETUP${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Username
    echo -e "${BLUE}1. What's your name?${NC}"
    echo "   (This will be used in AI prompts and TTS greetings)"
    read -p "   Your name: " USER_NAME
    USER_NAME=${USER_NAME:-User}
    
    echo ""
    
    # Workspace
    echo -e "${BLUE}2. Where is your main workspace/projects folder?${NC}"
    echo "   (WANDA will primarily work within this directory)"
    echo "   Default: $HOME/Projects"
    read -p "   Workspace path: " USER_WORKSPACE
    USER_WORKSPACE=${USER_WORKSPACE:-$HOME/Projects}
    
    # Expand ~ if used
    USER_WORKSPACE="${USER_WORKSPACE/#\~/$HOME}"
    
    # Create workspace if it doesn't exist
    if [ ! -d "$USER_WORKSPACE" ]; then
        echo -e "   ${YELLOW}Creating workspace directory...${NC}"
        mkdir -p "$USER_WORKSPACE"
    fi
    
    echo ""
    
    # Language
    echo -e "${BLUE}3. Preferred language?${NC}"
    echo "   1) German (de)"
    echo "   2) English (en)"
    echo "   3) Spanish (es)"
    echo "   4) French (fr)"
    read -p "   Choice [1]: " lang_choice
    case ${lang_choice:-1} in
        1) USER_LANGUAGE="de";;
        2) USER_LANGUAGE="en";;
        3) USER_LANGUAGE="es";;
        4) USER_LANGUAGE="fr";;
        *) USER_LANGUAGE="de";;
    esac
    
    echo ""
    
    # Ollama Models (Custom)
    echo -e "${BLUE}4. Ollama Model Configuration${NC}"
    echo "   Which local models do you want to use?"
    echo ""
    echo "   a) Use DEFAULTS (brainstorm-36b, heretic-12b, qwen3:8b)"
    echo "   b) CUSTOM - I have my own models"
    echo ""
    read -p "   Choice [a]: " model_choice
    
    if [[ "${model_choice:-a}" =~ ^[Bb] ]]; then
        echo ""
        echo -e "${YELLOW}   Enter your Ollama model names:${NC}"
        echo "   (Leave blank to skip)"
        
        read -p "   Primary Voice Model [brainstorm-36b]: " OLLAMA_PRIMARY
        OLLAMA_PRIMARY=${OLLAMA_PRIMARY:-brainstorm-36b}
        
        read -p "   Fallback Model [heretic-12b]: " OLLAMA_FALLBACK
        OLLAMA_FALLBACK=${OLLAMA_FALLBACK:-heretic-12b}
        
        read -p "   Lightweight Model [qwen3:8b]: " OLLAMA_LIGHT
        OLLAMA_LIGHT=${OLLAMA_LIGHT:-qwen3:8b}
    else
        OLLAMA_PRIMARY="brainstorm-36b"
        OLLAMA_FALLBACK="heretic-12b"
        OLLAMA_LIGHT="qwen3:8b"
    fi
    
    echo ""
    
    # ══════════════════════════════════════════════════════════════════════════
    # STEP 5: Cloud Provider Subscriptions (Smart Model Assignment)
    # ══════════════════════════════════════════════════════════════════════════
    echo -e "${BLUE}5. Cloud Provider Subscriptions${NC}"
    echo "   Let's configure your AI provider access for optimal model assignment."
    echo ""
    
    # Claude
    echo -e "   ${YELLOW}Claude (Anthropic):${NC}"
    echo "   1) No Claude subscription"
    echo "   2) Claude Pro ($20/mo)"
    echo "   3) Claude Max ($100/mo - includes Opus)"
    read -p "   Your Claude tier [1]: " CLAUDE_TIER
    CLAUDE_TIER=${CLAUDE_TIER:-1}
    
    # Gemini
    echo ""
    echo -e "   ${YELLOW}Google Gemini:${NC}"
    echo "   1) No Gemini subscription (using Antigravity)"
    echo "   2) Gemini (free tier)"
    echo "   3) Gemini Advanced ($20/mo)"
    read -p "   Your Gemini tier [2]: " GEMINI_TIER
    GEMINI_TIER=${GEMINI_TIER:-2}
    
    # OpenAI
    echo ""
    echo -e "   ${YELLOW}OpenAI:${NC}"
    echo "   1) No OpenAI subscription"
    echo "   2) ChatGPT Plus ($20/mo)"
    echo "   3) ChatGPT Pro ($200/mo - includes Codex 5.2)"
    read -p "   Your OpenAI tier [1]: " OPENAI_TIER
    OPENAI_TIER=${OPENAI_TIER:-1}
    
    # Kimi
    echo ""
    echo -e "   ${YELLOW}Kimi (Moonshot):${NC}"
    echo "   1) Kimi K2.5 Free (always available via OpenCode)"
    echo "   2) Kimi K2P5 Paid (premium orchestration)"
    read -p "   Your Kimi tier [1]: " KIMI_TIER
    KIMI_TIER=${KIMI_TIER:-1}
    
    echo ""
    
    # ══════════════════════════════════════════════════════════════════════════
    # SMART MODEL ASSIGNMENT
    # ══════════════════════════════════════════════════════════════════════════
    assign_smart_models() {
        echo -e "${BLUE}   Configuring optimal model assignment...${NC}"
        
        # Defaults (free tier / no subs)
        ORCHESTRATOR_MODEL="kimi-k2.5-free"
        ORCHESTRATOR_FALLBACK="gemini-3-flash"
        ARCHITECT_MODEL="kimi-k2.5-free"
        LIBRARIAN_MODEL="gemini-3-flash"
        DEVELOPER_MODEL="gemini-3-flash"
        AUDIT_MODEL="gemini-3-flash"
        WRITER_MODEL="gemini-3-flash"
        
        # Kimi K2P5 for Orchestrator (premium)
        if [ "$KIMI_TIER" == "2" ]; then
            ORCHESTRATOR_MODEL="kimi-code-k2p5"
            ORCHESTRATOR_FALLBACK="kimi-k2.5-free"
        fi
        
        # Claude Max → Use Opus for Architect (big brain decisions)
        if [ "$CLAUDE_TIER" == "3" ]; then
            ARCHITECT_MODEL="claude-4.5-opus"
            AUDIT_MODEL="claude-4.5-sonnet"
        elif [ "$CLAUDE_TIER" == "2" ]; then
            ARCHITECT_MODEL="claude-4.5-sonnet"
        fi
        
        # OpenAI Pro → Use Codex for Developer
        if [ "$OPENAI_TIER" == "3" ]; then
            DEVELOPER_MODEL="openai/codex-5.2"
        elif [ "$OPENAI_TIER" == "2" ]; then
            DEVELOPER_MODEL="openai/gpt-5.1"
        fi
        
        # Gemini Advanced → Use Pro for research
        if [ "$GEMINI_TIER" == "3" ]; then
            LIBRARIAN_MODEL="gemini-3-pro"
        fi
        
        echo "   ✓ Models assigned based on your subscriptions"
    }
    
    assign_smart_models
    
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  Configuration:${NC}"
    echo -e "${GREEN}  • Name: $USER_NAME${NC}"
    echo -e "${GREEN}  • Workspace: $USER_WORKSPACE${NC}"
    echo -e "${GREEN}  • Language: $USER_LANGUAGE${NC}"
    echo -e "${GREEN}  • Ollama Primary: $OLLAMA_PRIMARY${NC}"
    echo -e "${GREEN}  • Ollama Fallback: $OLLAMA_FALLBACK${NC}"
    echo -e "${GREEN}  ────────────────────────────────────────────────────${NC}"
    echo -e "${GREEN}  • Sisyphus (Orch): $ORCHESTRATOR_MODEL${NC}"
    echo -e "${GREEN}  • Prometheus (Arch): $ARCHITECT_MODEL${NC}"
    echo -e "${GREEN}  • Atlas (Dev):     $DEVELOPER_MODEL${NC}"
    echo -e "${GREEN}  • Librarian:       $LIBRARIAN_MODEL${NC}"
    echo -e "${GREEN}  • Audit:           $AUDIT_MODEL${NC}"
    echo -e "${GREEN}  • Writer:          $WRITER_MODEL${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    read -p "Is this correct? [Y/n]: " confirm
    if [[ "${confirm:-y}" =~ ^[Nn] ]]; then
        collect_user_info
    fi
}

# Hardware Detection
check_hardware() {
    echo -e "${BLUE}Auditing System Hardware...${NC}"
    
    # RAM
    if [ "$OS" = "linux" ]; then
        TOTAL_RAM=$(grep MemTotal /proc/meminfo | awk '{print $2}')
        RAM_GB=$((TOTAL_RAM / 1024 / 1024))
    elif [ "$OS" = "macos" ]; then
        TOTAL_RAM=$(sysctl -n hw.memsize)
        RAM_GB=$((TOTAL_RAM / 1024 / 1024 / 1024))
    else
        RAM_GB=16
    fi
    
    # VRAM (NVIDIA)
    if command -v nvidia-smi &> /dev/null; then
        VRAM_MB=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -n 1)
        VRAM_GB=$((VRAM_MB / 1024))
        GPU_TYPE="NVIDIA"
    else
        VRAM_GB=0
        GPU_TYPE="None/iGPU"
    fi
    
    echo "   - RAM: ${RAM_GB}GB"
    echo "   - GPU: ${GPU_TYPE} (${VRAM_GB}GB VRAM)"
    
    # Recommend Brain
    echo -e "${YELLOW}Recommended Local Brain (SOTA 2026):${NC}"
    if [ "$VRAM_GB" -ge 16 ] || [ "$RAM_GB" -ge 64 ]; then
        RECOMMENDED_MODEL="DeepSeek V4 / Qwen 3 (235B)"
    elif [ "$RAM_GB" -ge 48 ]; then
        RECOMMENDED_MODEL="Qwen 2.5 Coder (32B) / Llama 4 Maverick"
    elif [ "$VRAM_GB" -ge 8 ] || [ "$RAM_GB" -ge 16 ]; then
        RECOMMENDED_MODEL="Gemma 3 (27B) / Llama 4 Scout"
    else
        RECOMMENDED_MODEL="Llama 4 Scout (17B MoE - Lightweight)"
    fi
    echo -e "   → ${GREEN}$RECOMMENDED_MODEL${NC}"
}

# Prerequisites check
check_prereqs() {
    echo -e "${YELLOW}Checking prerequisites...${NC}"
    
    local missing=""
    
    command -v python3 >/dev/null 2>&1 || missing+=" python3"
    command -v git >/dev/null 2>&1 || missing+=" git"
    command -v pip >/dev/null 2>&1 || command -v pip3 >/dev/null 2>&1 || missing+=" pip"
    command -v gh >/dev/null 2>&1 || missing+=" gh (GitHub CLI)"
    
    if [ -n "$missing" ]; then
        echo -e "${RED}Missing required tools:${missing}${NC}"
        echo "Please install them first:"
        if [ "$OS" = "linux" ]; then
            echo "  sudo apt install python3 python3-pip git gh"
            echo "  (For gh: see https://github.com/cli/cli/blob/trunk/docs/install_linux.md)"
        elif [ "$OS" = "macos" ]; then
            echo "  brew install python3 git gh"
        fi
        exit 1
    fi
    
    # Check gh auth
    if command -v gh >/dev/null 2>&1; then
        if ! gh auth status >/dev/null 2>&1; then
            echo -e "${YELLOW}Warning: GitHub CLI not logged in.${NC}"
            echo "Run 'gh auth login' later to enable GitHub Agent capabilities."
            sleep 2
        fi
    fi
    
    echo -e "${GREEN}✓ All prerequisites met${NC}"
}

# Clone or update repo
REPO_URL="https://github.com/jas0nOW/wanda-agentic-system"
INSTALL_DIR="${WANDA_INSTALL_DIR:-$HOME/.wanda-system}"

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
        1) INSTALL_AGENTS=1; INSTALL_VOICE=0; INSTALL_TELEGRAM=0 ;;
        2) INSTALL_AGENTS=0; INSTALL_VOICE=1; INSTALL_TELEGRAM=0 ;;
        4) custom_selection ;;
        *) INSTALL_AGENTS=1; INSTALL_VOICE=1; INSTALL_TELEGRAM=1 ;;
    esac
}

custom_selection() {
    INSTALL_AGENTS=0
    INSTALL_VOICE=0
    INSTALL_TELEGRAM=0
    
    read -p "Install Agent System? [Y/n]: " ans
    [[ "${ans:-y}" =~ ^[Yy] ]] && INSTALL_AGENTS=1
    
    read -p "Install Voice Assistant? [Y/n]: " ans
    [[ "${ans:-y}" =~ ^[Yy] ]] && INSTALL_VOICE=1
    
    read -p "Install Telegram Bot? [y/N]: " ans
    [[ "$ans" =~ ^[Yy] ]] && INSTALL_TELEGRAM=1
}

# ══════════════════════════════════════════════════════════════════════════════
# TEMPLATE PROCESSING - Replace {{TOKENS}} with user values
# ══════════════════════════════════════════════════════════════════════════════

process_templates() {
    echo -e "${BLUE}Processing templates with your configuration...${NC}"
    
    # Process PROJECT_CONTEXT.md
    if [ -f "$INSTALL_DIR/prompts/context/PROJECT_CONTEXT.md.template" ]; then
        sed -e "s|{{USERNAME}}|$USER_NAME|g" \
            -e "s|{{WORKSPACE}}|$USER_WORKSPACE|g" \
            -e "s|{{LANGUAGE}}|$USER_LANGUAGE|g" \
            -e "s|{{AGENTS_INSTALLED}}|$INSTALL_AGENTS|g" \
            -e "s|{{VOICE_INSTALLED}}|$INSTALL_VOICE|g" \
            -e "s|{{TELEGRAM_INSTALLED}}|$INSTALL_TELEGRAM|g" \
            -e "s|{{MCP_INSTALLED}}|${MCP_INSTALLED:-0}|g" \
            "$INSTALL_DIR/prompts/context/PROJECT_CONTEXT.md.template" \
            > "$INSTALL_DIR/prompts/context/PROJECT_CONTEXT.md"
    fi
    
    # Process GEMINI.md (personalized system prompt)
    if [ -f "$INSTALL_DIR/templates/GEMINI.md.template" ]; then
        sed -e "s|{{USERNAME}}|$USER_NAME|g" \
            -e "s|{{WORKSPACE}}|$USER_WORKSPACE|g" \
            -e "s|{{LANGUAGE}}|$USER_LANGUAGE|g" \
            "$INSTALL_DIR/templates/GEMINI.md.template" \
            > "$GEMINI_CONFIG/GEMINI.md"
    fi
    
    # Process agents.yaml (Smart Model Assignment)
    if [ -f "$INSTALL_DIR/config/agents.yaml.template" ]; then
        echo "  - Configuring agents with: "
        echo "    Orch: $ORCHESTRATOR_MODEL"
        echo "    Arch: $ARCHITECT_MODEL"
        echo "    Dev:  $DEVELOPER_MODEL"
        
        sed -e "s|{{ORCHESTRATOR_MODEL}}|$ORCHESTRATOR_MODEL|g" \
            -e "s|{{ORCHESTRATOR_FALLBACK}}|$ORCHESTRATOR_FALLBACK|g" \
            -e "s|{{ARCHITECT_MODEL}}|$ARCHITECT_MODEL|g" \
            -e "s|{{DEVELOPER_MODEL}}|$DEVELOPER_MODEL|g" \
            -e "s|{{LIBRARIAN_MODEL}}|$LIBRARIAN_MODEL|g" \
            -e "s|{{AUDIT_MODEL}}|$AUDIT_MODEL|g" \
            -e "s|{{WRITER_MODEL}}|$WRITER_MODEL|g" \
            "$INSTALL_DIR/config/agents.yaml.template" \
            > "$INSTALL_DIR/config/agents.yaml"
    fi
    
    # Process oh-my-opencode config
    if [ -f "$INSTALL_DIR/plugins/oh-my-opencode/config.yaml.template" ]; then
        sed -e "s|{{ORCHESTRATOR_MODEL}}|$ORCHESTRATOR_MODEL|g" \
            -e "s|{{ORCHESTRATOR_FALLBACK}}|$ORCHESTRATOR_FALLBACK|g" \
            -e "s|{{ARCHITECT_MODEL}}|$ARCHITECT_MODEL|g" \
            -e "s|{{DEVELOPER_MODEL}}|$DEVELOPER_MODEL|g" \
            -e "s|{{LIBRARIAN_MODEL}}|$LIBRARIAN_MODEL|g" \
            -e "s|{{AUDIT_MODEL}}|$AUDIT_MODEL|g" \
            -e "s|{{WRITER_MODEL}}|$WRITER_MODEL|g" \
            "$INSTALL_DIR/plugins/oh-my-opencode/config.yaml.template" \
            > "$INSTALL_DIR/plugins/oh-my-opencode/config.yaml"
    fi

    # Process MiCode config (UI)
    if [ -f "$INSTALL_DIR/plugins/micode/config.json.template" ]; then
        sed -e "s|{{USERNAME}}|$USER_NAME|g" \
            "$INSTALL_DIR/plugins/micode/config.json.template" \
            > "$INSTALL_DIR/plugins/micode/config.json"
    fi
    
    echo -e "${GREEN}✓ Templates processed${NC}"
}

# Install Agent System
install_agents() {
    echo ""
    echo -e "${YELLOW}Installing Agent System...${NC}"
    
    # Create directories
    mkdir -p "$OPENCODE_CONFIG"
    mkdir -p "$GEMINI_CONFIG"
    mkdir -p "$OPENCODE_CONFIG/plugins"
    
    # Copy OpenCode profiles (symlink for live updates)
    if [ -f "$INSTALL_DIR/wanda_cloud/profiles/stable/opencode.jsonc" ]; then
        ln -sf "$INSTALL_DIR/wanda_cloud/profiles/stable/opencode.jsonc" "$OPENCODE_CONFIG/opencode.jsonc"
        echo "  ✓ OpenCode profile symlinked"
    fi
    
    # Copy/process GEMINI.md
    if [ -f "$INSTALL_DIR/templates/GEMINI.md.template" ]; then
        process_templates
    else
        # Fallback: copy default and personalize inline
        cp "$INSTALL_DIR/prompts/system/OPENCODE_SYSTEM.md" "$GEMINI_CONFIG/GEMINI.md" 2>/dev/null || true
    fi
    
    # Copy settings.json for MCP
    if [ -f "$INSTALL_DIR/mcp-servers/settings.json.template" ]; then
        cp "$INSTALL_DIR/mcp-servers/settings.json.template" "$GEMINI_CONFIG/settings.json"
    fi
    
    # ══════════════════════════════════════════════════════════════════════════
    # PLUGIN DEPLOYMENT - Copy plugin configs to correct locations
    # ══════════════════════════════════════════════════════════════════════════
    echo -e "${BLUE}  Deploying plugin configurations...${NC}"
    
    # oh-my-opencode plugin
    if [ -d "$INSTALL_DIR/plugins/oh-my-opencode" ]; then
        mkdir -p "$OPENCODE_CONFIG/plugins/oh-my-opencode"
        cp "$INSTALL_DIR/plugins/oh-my-opencode/"*.yaml "$OPENCODE_CONFIG/plugins/oh-my-opencode/" 2>/dev/null || true
        echo "    ✓ oh-my-opencode config deployed"
    fi
    
    # MiCode plugin
    if [ -d "$INSTALL_DIR/plugins/micode" ]; then
        mkdir -p "$OPENCODE_CONFIG/plugins/micode"
        cp "$INSTALL_DIR/plugins/micode/"*.json "$OPENCODE_CONFIG/plugins/micode/" 2>/dev/null || true
        echo "    ✓ MiCode config deployed"
    fi
    
    # Orchestrator plugin
    if [ -d "$INSTALL_DIR/plugins/orchestrator" ]; then
        mkdir -p "$OPENCODE_CONFIG/plugins/orchestrator"
        cp "$INSTALL_DIR/plugins/orchestrator/"*.yaml "$OPENCODE_CONFIG/plugins/orchestrator/" 2>/dev/null || true
        echo "    ✓ Orchestrator routing deployed"
    fi
    
    # Symlink agent prompts for reference
    if [ -d "$INSTALL_DIR/prompts/agents" ]; then
        ln -sf "$INSTALL_DIR/prompts/agents" "$OPENCODE_CONFIG/agents"
        echo "    ✓ Agent prompts linked"
    fi
    
    # Copy AGENT_ROSTER for quick reference
    if [ -f "$INSTALL_DIR/prompts/AGENT_ROSTER.md" ]; then
        cp "$INSTALL_DIR/prompts/AGENT_ROSTER.md" "$OPENCODE_CONFIG/"
        echo "    ✓ Agent roster copied"
    fi
    
    echo -e "${GREEN}✓ Agent System installed (with all plugins)${NC}"
}

# Install Voice Assistant
install_voice() {
    echo ""
    echo -e "${YELLOW}Installing Voice Assistant...${NC}"
    
    VOICE_DIR="$INSTALL_DIR/wanda_local"
    
    if [ ! -d "$VOICE_DIR" ]; then
        echo -e "${RED}Voice module not found${NC}"
        return
    fi
    
    cd "$VOICE_DIR"
    
    # Create venv if not exists
    if [ ! -d "venv" ]; then
        python3 -m venv venv
    fi
    
    # Install dependencies
    source venv/bin/activate
    pip install --upgrade pip --quiet
    pip install -r requirements.txt --quiet 2>/dev/null || {
        pip install python-telegram-bot python-dotenv httpx --quiet
    }
    
    # Create personalized config
    cat > "$VOICE_DIR/config.yaml" <<EOF
# WANDA Voice Configuration
# Generated by install.sh

user:
  name: "$USER_NAME"
  language: "$USER_LANGUAGE"

workspace: "$USER_WORKSPACE"

tts:
  engine: auto  # auto, xtts, siri (macOS), piper
  voice: ${USER_LANGUAGE}-1

ollama:
  model: $OLLAMA_PRIMARY
  fallback: $OLLAMA_FALLBACK
  lightweight: $OLLAMA_LIGHT
EOF
    
    echo -e "${GREEN}✓ Voice Assistant installed${NC}"
}

# Install Telegram Bot (optional)
install_telegram() {
    echo ""
    echo -e "${YELLOW}Setting up Telegram Bot...${NC}"
    
    read -p "Do you have a Telegram Bot token? [y/N]: " has_token
    if [[ ! "$has_token" =~ ^[Yy] ]]; then
        echo "  Skipping Telegram setup. Get a token from @BotFather later."
        return
    fi
    
    read -p "Enter your Telegram Bot Token: " TELEGRAM_TOKEN
    
    cat > "$INSTALL_DIR/wanda_local/.env" <<EOF
# WANDA Telegram Bot Configuration
WANDA_TELEGRAM_BOT_TOKEN=$TELEGRAM_TOKEN
WANDA_TELEGRAM_BOT_NAME=@wandavoice_bot
WANDA_USER_NAME=$USER_NAME
EOF
    
    echo -e "${GREEN}✓ Telegram Bot configured${NC}"
}

# MCP setup
setup_mcp() {
    echo ""
    read -p "Setup MCP Docker servers? [y/N]: " ans
    if [[ "$ans" =~ ^[Yy] ]]; then
        MCP_INSTALLED=1
        if command -v docker >/dev/null 2>&1; then
            if [ -f "$INSTALL_DIR/mcp-servers/settings.json.template" ]; then
                sed -e "s|{{HOME}}|$HOME|g" \
                    "$INSTALL_DIR/mcp-servers/settings.json.template" \
                    > "$GEMINI_CONFIG/settings.json"
            fi
            echo -e "${GREEN}✓ MCP config created${NC}"
            echo "Edit $GEMINI_CONFIG/settings.json to add API keys"
        else
            echo -e "${RED}Docker not found. Install Docker first.${NC}"
            MCP_INSTALLED=0
        fi
    else
        MCP_INSTALLED=0
    fi
}

# Summary
print_summary() {
    echo ""
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════════════════════════╗"
    echo "║                      ✅ Installation Complete!                           ║"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
    echo ""
    echo -e "  ${CYAN}Welcome, $USER_NAME!${NC}"
    echo ""
    echo "  Installed to: $INSTALL_DIR"
    echo "  Workspace: $USER_WORKSPACE"
    echo ""
    echo -e "${BLUE}Quick Start:${NC}"
    [ "$INSTALL_AGENTS" = "1" ] && echo "  • Agent System: opencode or gemini"
    [ "$INSTALL_VOICE" = "1" ] && echo "  • Voice Assistant: cd $INSTALL_DIR/wanda_local && python main.py"
    [ "$INSTALL_TELEGRAM" = "1" ] && echo "  • Telegram Bot: pm2 start wanda_local/telegram_bot.py"
    echo ""
    echo -e "${BLUE}Update:${NC}"
    echo "  cd $INSTALL_DIR && git pull"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  $INSTALL_DIR/docs/"
    echo ""
    echo "🌟 Enjoy WANDA, $USER_NAME!"
}

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

main() {
    print_banner
    detect_os
    set_paths
    check_prereqs
    
    # PERSONALIZATION
    collect_user_info
    
    check_hardware
    get_repo
    select_components
    
    [ "$INSTALL_AGENTS" = "1" ] && install_agents
    [ "$INSTALL_VOICE" = "1" ] && install_voice
    [ "$INSTALL_TELEGRAM" = "1" ] && install_telegram
    
    setup_mcp
    process_templates
    print_summary
}

main "$@"
