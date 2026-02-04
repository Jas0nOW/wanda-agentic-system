#!/bin/sh
# ==============================================================================
# WANDA Agentic System - One-Command Installer
# https://github.com/jas0nOW/wanda-agentic-system
# ==============================================================================
# PERSONALIZED INSTALLATION - Asks for user name and workspace folder
# ==============================================================================
# POSIX-compliant version - works with bash, zsh, dash, and other POSIX shells

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
# LANGUAGE SELECTION (First thing after banner)
# ══════════════════════════════════════════════════════════════════════════════

select_language() {
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║     🌍 Select Language / Sprache wählen                       ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "   1) 🇩🇪 Deutsch (German)"
    echo "   2) 🇬🇧 English"
    echo ""
    read -p "   Choice / Auswahl [1]: " lang_init
    
    case "${lang_init:-1}" in
        2)
            INSTALLER_LANG="en"
            USER_LANGUAGE="en"
            echo ""
            echo -e "   ${GREEN}✓ Language set to English${NC}"
            ;;
        *)
            INSTALLER_LANG="de"
            USER_LANGUAGE="de"
            echo ""
            echo -e "   ${GREEN}✓ Sprache auf Deutsch gesetzt${NC}"
            ;;
    esac
}

# Localized text helper
msg() {
    local key=$1
    case "$INSTALLER_LANG" in
        en)
            case "$key" in
                "title_personalization") echo "PERSONALIZATION SETUP";;
                "q_name") echo "What's your name?";;
                "q_name_hint") echo "(This will be used in AI prompts and TTS greetings)";;
                "q_workspace") echo "Where is your main workspace/projects folder?";;
                "q_workspace_hint") echo "(WANDA will primarily work within this directory)";;
                "creating_workspace") echo "Creating workspace directory...";;
                *) echo "$key";;
            esac
            ;;
        *)
            case "$key" in
                "title_personalization") echo "PERSONALISIERUNG";;
                "q_name") echo "Wie heißt du?";;
                "q_name_hint") echo "(Wird in AI-Prompts und TTS-Begrüßungen verwendet)";;
                "q_workspace") echo "Wo ist dein Haupt-Workspace/Projekte-Ordner?";;
                "q_workspace_hint") echo "(WANDA arbeitet hauptsächlich in diesem Verzeichnis)";;
                "creating_workspace") echo "Erstelle Workspace-Verzeichnis...";;
                *) echo "$key";;
            esac
            ;;
    esac
}

# ══════════════════════════════════════════════════════════════════════════════
# PERSONALIZATION - Ask for user-specific configuration
# ══════════════════════════════════════════════════════════════════════════════

collect_user_info() {
    echo ""
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}                  $(msg title_personalization)${NC}"
    echo -e "${YELLOW}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    # Username
    echo -e "${BLUE}1. $(msg q_name)${NC}"
    echo "   $(msg q_name_hint)"
    read -p "   Name: " USER_NAME
    USER_NAME=${USER_NAME:-User}
    
    echo ""
    
    # Workspace
    echo -e "${BLUE}2. $(msg q_workspace)${NC}"
    echo "   $(msg q_workspace_hint)"
    echo "   Default: $HOME/Projects"
    read -p "   Workspace: " USER_WORKSPACE
    USER_WORKSPACE=${USER_WORKSPACE:-$HOME/Projects}
    
    # Expand ~ if used
    USER_WORKSPACE="${USER_WORKSPACE/#\~/$HOME}"
    
    # Create workspace if it doesn't exist
    if [ ! -d "$USER_WORKSPACE" ]; then
        echo -e "   ${YELLOW}$(msg creating_workspace)${NC}"
        mkdir -p "$USER_WORKSPACE"
    fi
    
    # Language already selected at start - skip this step
    # USER_LANGUAGE is already set from select_language()
    
    echo ""
    
    # ══════════════════════════════════════════════════════════════════════════
    # STEP 4: Ollama Configuration (ENHANCER + DIRECT ANSWERER)
    # ══════════════════════════════════════════════════════════════════════════
    echo -e "${BLUE}4. Ollama Configuration${NC}"
    echo "   Ollama makes WANDA smarter (prompt optimization, direct answers, TTS preprocessing)."
    echo "   WANDA works 100% without Ollama - it's an optional enhancer."
    echo ""
    echo "   a) Skip Ollama (Cloud-only mode)"
    echo "   b) Use RECOMMENDED models (based on your hardware: $HARDWARE_PROFILE)"
    echo "   c) Use DEFAULTS (brainstorm-36b, heretic-12b, qwen3:8b)"
    echo "   d) CUSTOM - I have my own models"
    echo ""
    read -p "   Choice [b]: " ollama_choice
    
    case "${ollama_choice:-b}" in
        [Aa])
            USE_OLLAMA=0
            OLLAMA_PRIMARY=""
            OLLAMA_FALLBACK=""
            OLLAMA_LIGHT=""
            OLLAMA_DIRECT_ANSWER=0
            echo "   ✓ Ollama skipped (Cloud-only mode)"
            ;;
        [Bb])
            USE_OLLAMA=1
            OLLAMA_DIRECT_ANSWER=1
            # Use hardware-based recommendation
            OLLAMA_PRIMARY="${RECOMMENDED_OLLAMA%% /*}"  # First model
            OLLAMA_FALLBACK="qwen3:8b"
            OLLAMA_LIGHT="llama-3.2:3b"
            echo "   ✓ Using recommended: $OLLAMA_PRIMARY"
            ;;
        [Cc])
            USE_OLLAMA=1
            OLLAMA_DIRECT_ANSWER=1
            OLLAMA_PRIMARY="brainstorm-36b"
            OLLAMA_FALLBACK="heretic-12b"
            OLLAMA_LIGHT="qwen3:8b"
            echo "   ✓ Using defaults"
            ;;
        [Dd])
            USE_OLLAMA=1
            OLLAMA_DIRECT_ANSWER=1
            echo ""
            echo -e "   ${YELLOW}Enter your Ollama model names:${NC}"
            read -p "   Primary Model: " OLLAMA_PRIMARY
            OLLAMA_PRIMARY=${OLLAMA_PRIMARY:-brainstorm-36b}
            read -p "   Fallback Model: " OLLAMA_FALLBACK
            OLLAMA_FALLBACK=${OLLAMA_FALLBACK:-heretic-12b}
            read -p "   Lightweight Model: " OLLAMA_LIGHT
            OLLAMA_LIGHT=${OLLAMA_LIGHT:-qwen3:8b}
            ;;
        *)
            USE_OLLAMA=1
            OLLAMA_DIRECT_ANSWER=1
            OLLAMA_PRIMARY="${RECOMMENDED_OLLAMA%% /*}"
            OLLAMA_FALLBACK="qwen3:8b"
            OLLAMA_LIGHT="llama-3.2:3b"
            ;;
    esac
    
    # Direct Answerer Toggle (if Ollama enabled)
    if [ "$USE_OLLAMA" = "1" ]; then
        echo ""
        echo -e "   ${YELLOW}Enable Direct Answering?${NC}"
        echo "   (Simple questions like 'What's the weather?' answered by Ollama without agents)"
        read -p "   Enable Direct Answers? [Y/n]: " direct_ans
        case "${direct_ans:-y}" in
            [Nn]*) OLLAMA_DIRECT_ANSWER=0 ;;
        esac
    fi
    
    echo ""
    
    # ══════════════════════════════════════════════════════════════════════════
    # STEP 5: Cloud Provider Subscriptions (Smart Model Assignment)
    # ══════════════════════════════════════════════════════════════════════════
    echo -e "${BLUE}5. Cloud Provider Subscriptions${NC}"
    echo "   Configure your AI provider access for optimal model assignment."
    echo ""
    
    # Claude
    echo -e "   ${YELLOW}Claude (Anthropic):${NC}"
    echo "   1) None"
    echo "   2) Normal (Sonnet access)"
    echo "   3) Max (Sonnet + Opus access)"
    read -p "   Your Claude tier [1]: " CLAUDE_TIER
    CLAUDE_TIER=${CLAUDE_TIER:-1}
    
    # Gemini
    echo ""
    echo -e "   ${YELLOW}Google Gemini:${NC}"
    echo "   1) Antigravity (OAuth - Flash+Pro auf CLI+Antigravity Limits)"
    echo "   2) Free tier (nur Flash)"
    echo "   3) Advanced API KEY (Flash + Pro mit extra Quota - API Key nötig!)"
    read -p "   Your Gemini tier [1]: " GEMINI_TIER
    GEMINI_TIER=${GEMINI_TIER:-1}
    
    # OpenAI
    echo ""
    echo -e "   ${YELLOW}OpenAI:${NC}"
    echo "   1) None"
    echo "   2) Normal (Codex + GPT-5.2 - günstiger für Code)"
    echo "   3) Max (GPT-5.2 only - teurer, aber stärker)"
    read -p "   Your OpenAI tier [1]: " OPENAI_TIER
    OPENAI_TIER=${OPENAI_TIER:-1}
    
    # Kimi
    echo ""
    echo -e "   ${YELLOW}Kimi (Moonshot):${NC}"
    echo "   1) Free (K2.5 via OpenCode)"
    echo "   2) Paid (K2P5 Coding - premium)"
    read -p "   Your Kimi tier [1]: " KIMI_TIER
    KIMI_TIER=${KIMI_TIER:-1}
    
    # GitHub Copilot
    echo ""
    echo -e "   ${YELLOW}GitHub Copilot:${NC}"
    echo "   1) None"
    echo "   2) Active (OAuth)"
    read -p "   Your Copilot tier [1]: " COPILOT_TIER
    COPILOT_TIER=${COPILOT_TIER:-1}
    
    echo ""
    
    # ══════════════════════════════════════════════════════════════════════════
    # STEP 6: Agent Model Configuration (17 Agents)
    # ══════════════════════════════════════════════════════════════════════════
    echo -e "${BLUE}6. Agent Model Configuration${NC}"
    echo "   Configure models for all 17 agents."
    echo ""
    echo "   1) WANDA DEFAULTS (Jas0n's optimized setup)"
    echo "   2) SUBSCRIPTION-BASED (auto-assign from your tiers)"
    echo "   3) CUSTOM (configure each agent manually)"
    echo ""
    read -p "   Choice [1]: " agent_menu_choice
    
    case "${agent_menu_choice:-1}" in
        1)
            # WANDA DEFAULTS - Jas0n's optimized 17-agent configuration
            echo -e "   ${GREEN}✓ Using WANDA DEFAULTS${NC}"
            
            # Primary Agents
            ORCHESTRATOR_MODEL="kimi-code-k2p5"
            ORCHESTRATOR_FALLBACK="kimi-k2.5-free"
            BRAINSTORMER_MODEL="kimi-k2.5-free"
            BRAINSTORMER_FALLBACK="gemini-3-flash"
            ARCHITECT_MODEL="claude-4.5-sonnet"
            ARCHITECT_FALLBACK="kimi-k2.5-free"
            DEVELOPER_MODEL="claude-4.5-sonnet"
            DEVELOPER_FALLBACK="kimi-code-k2p5"
            AUDIT_MODEL="codex-5.2"
            AUDIT_FALLBACK="kimi-k2.5-free"
            LIBRARIAN_MODEL="gemini-3-flash-preview"
            LIBRARIAN_FALLBACK="kimi-k2.5-free"
            WRITER_MODEL="gemini-3-flash-preview"
            WRITER_FALLBACK="kimi-k2.5-free"
            
            # Sub Agents
            FRONTEND_MODEL="gemini-3-pro-preview"
            FRONTEND_FALLBACK="kimi-k2.5-free"
            ORACLE_MODEL="claude-4.5-opus"
            ORACLE_FALLBACK="gemini-3-pro-preview"
            EXPLORE_MODEL="gemini-3-flash-preview"
            EXPLORE_FALLBACK="kimi-k2.5-free"
            LOOKER_MODEL="kimi-k2.5-free"
            LOOKER_FALLBACK="gemini-3-flash-preview"
            LOCATOR_MODEL="gemini-3-flash-preview"
            LOCATOR_FALLBACK="kimi-k2.5-free"
            ANALYZER_MODEL="codex-5.2"
            ANALYZER_FALLBACK="kimi-k2.5-free"
            PATTERN_MODEL="codex-5.2"
            PATTERN_FALLBACK="kimi-k2.5-free"
            LEDGER_MODEL="gemini-3-flash-preview"
            LEDGER_FALLBACK="kimi-k2.5-free"
            ARTIFACT_MODEL="gemini-3-flash-preview"
            ARTIFACT_FALLBACK="kimi-k2.5-free"
            META_MODEL="gemini-3-flash-preview"
            META_FALLBACK="kimi-k2.5-free"
            ;;
        2)
            # SUBSCRIPTION-BASED - auto-assign from tiers
            echo -e "   ${GREEN}✓ Assigning based on subscriptions${NC}"
            
            # Defaults
            ORCHESTRATOR_MODEL="kimi-k2.5-free"
            ORCHESTRATOR_FALLBACK="gemini-3-flash"
            BRAINSTORMER_MODEL="kimi-k2.5-free"
            BRAINSTORMER_FALLBACK="gemini-3-flash"
            ARCHITECT_MODEL="kimi-k2.5-free"
            ARCHITECT_FALLBACK="gemini-3-flash"
            DEVELOPER_MODEL="gemini-3-flash"
            DEVELOPER_FALLBACK="kimi-k2.5-free"
            AUDIT_MODEL="gemini-3-flash"
            AUDIT_FALLBACK="kimi-k2.5-free"
            LIBRARIAN_MODEL="gemini-3-flash"
            LIBRARIAN_FALLBACK="kimi-k2.5-free"
            WRITER_MODEL="gemini-3-flash"
            WRITER_FALLBACK="kimi-k2.5-free"
            
            # Apply subscription upgrades
            [ "$KIMI_TIER" == "2" ] && ORCHESTRATOR_MODEL="kimi-code-k2p5"
            [ "$CLAUDE_TIER" == "3" ] && ARCHITECT_MODEL="claude-4.5-opus" && AUDIT_MODEL="claude-4.5-sonnet"
            [ "$CLAUDE_TIER" == "2" ] && ARCHITECT_MODEL="claude-4.5-sonnet"
            [ "$OPENAI_TIER" == "3" ] && DEVELOPER_MODEL="codex-5.2" && AUDIT_MODEL="codex-5.2"
            [ "$OPENAI_TIER" == "2" ] && DEVELOPER_MODEL="gpt-5.2"
            [ "$GEMINI_TIER" == "3" ] && LIBRARIAN_MODEL="gemini-3-pro"
            
            # Sub-agents use same as primaries
            FRONTEND_MODEL="$DEVELOPER_MODEL"; FRONTEND_FALLBACK="kimi-k2.5-free"
            ORACLE_MODEL="$ARCHITECT_MODEL"; ORACLE_FALLBACK="gemini-3-flash"
            EXPLORE_MODEL="$LIBRARIAN_MODEL"; EXPLORE_FALLBACK="kimi-k2.5-free"
            LOOKER_MODEL="kimi-k2.5-free"; LOOKER_FALLBACK="gemini-3-flash"
            LOCATOR_MODEL="$LIBRARIAN_MODEL"; LOCATOR_FALLBACK="kimi-k2.5-free"
            ANALYZER_MODEL="$AUDIT_MODEL"; ANALYZER_FALLBACK="kimi-k2.5-free"
            PATTERN_MODEL="$AUDIT_MODEL"; PATTERN_FALLBACK="kimi-k2.5-free"
            LEDGER_MODEL="gemini-3-flash"; LEDGER_FALLBACK="kimi-k2.5-free"
            ARTIFACT_MODEL="gemini-3-flash"; ARTIFACT_FALLBACK="kimi-k2.5-free"
            META_MODEL="gemini-3-flash"; META_FALLBACK="kimi-k2.5-free"
            ;;
        3)
            # CUSTOM - manual configuration
            echo ""
            echo -e "   ${YELLOW}Configure each agent manually:${NC}"
            echo ""
            read -p "   Sisyphus (Orchestrator) model: " ORCHESTRATOR_MODEL
            ORCHESTRATOR_MODEL=${ORCHESTRATOR_MODEL:-kimi-k2.5-free}
            read -p "   Prometheus (Architect) model: " ARCHITECT_MODEL
            ARCHITECT_MODEL=${ARCHITECT_MODEL:-kimi-k2.5-free}
            read -p "   Atlas (Developer) model: " DEVELOPER_MODEL
            DEVELOPER_MODEL=${DEVELOPER_MODEL:-gemini-3-flash}
            read -p "   Audit model: " AUDIT_MODEL
            AUDIT_MODEL=${AUDIT_MODEL:-gemini-3-flash}
            read -p "   Librarian model: " LIBRARIAN_MODEL
            LIBRARIAN_MODEL=${LIBRARIAN_MODEL:-gemini-3-flash}
            read -p "   Writer model: " WRITER_MODEL
            WRITER_MODEL=${WRITER_MODEL:-gemini-3-flash}
            echo "   (Sub-agents will use same as their parent)"
            
            ORCHESTRATOR_FALLBACK="kimi-k2.5-free"
            BRAINSTORMER_MODEL="kimi-k2.5-free"; BRAINSTORMER_FALLBACK="gemini-3-flash"
            ARCHITECT_FALLBACK="kimi-k2.5-free"
            DEVELOPER_FALLBACK="kimi-k2.5-free"
            AUDIT_FALLBACK="kimi-k2.5-free"
            LIBRARIAN_FALLBACK="kimi-k2.5-free"
            WRITER_FALLBACK="kimi-k2.5-free"
            FRONTEND_MODEL="$DEVELOPER_MODEL"; FRONTEND_FALLBACK="kimi-k2.5-free"
            ORACLE_MODEL="$ARCHITECT_MODEL"; ORACLE_FALLBACK="gemini-3-flash"
            EXPLORE_MODEL="$LIBRARIAN_MODEL"; EXPLORE_FALLBACK="kimi-k2.5-free"
            LOOKER_MODEL="kimi-k2.5-free"; LOOKER_FALLBACK="gemini-3-flash"
            LOCATOR_MODEL="$LIBRARIAN_MODEL"; LOCATOR_FALLBACK="kimi-k2.5-free"
            ANALYZER_MODEL="$AUDIT_MODEL"; ANALYZER_FALLBACK="kimi-k2.5-free"
            PATTERN_MODEL="$AUDIT_MODEL"; PATTERN_FALLBACK="kimi-k2.5-free"
            LEDGER_MODEL="gemini-3-flash"; LEDGER_FALLBACK="kimi-k2.5-free"
            ARTIFACT_MODEL="gemini-3-flash"; ARTIFACT_FALLBACK="kimi-k2.5-free"
            META_MODEL="gemini-3-flash"; META_FALLBACK="kimi-k2.5-free"
            ;;
        *)
            # Default to WANDA DEFAULTS
            ORCHESTRATOR_MODEL="kimi-code-k2p5"
            ORCHESTRATOR_FALLBACK="kimi-k2.5-free"
            BRAINSTORMER_MODEL="kimi-k2.5-free"
            BRAINSTORMER_FALLBACK="gemini-3-flash"
            ARCHITECT_MODEL="claude-4.5-sonnet"
            ARCHITECT_FALLBACK="kimi-k2.5-free"
            DEVELOPER_MODEL="claude-4.5-sonnet"
            DEVELOPER_FALLBACK="kimi-code-k2p5"
            AUDIT_MODEL="codex-5.2"
            AUDIT_FALLBACK="kimi-k2.5-free"
            LIBRARIAN_MODEL="gemini-3-flash-preview"
            LIBRARIAN_FALLBACK="kimi-k2.5-free"
            WRITER_MODEL="gemini-3-flash-preview"
            WRITER_FALLBACK="kimi-k2.5-free"
            FRONTEND_MODEL="gemini-3-pro-preview"; FRONTEND_FALLBACK="kimi-k2.5-free"
            ORACLE_MODEL="claude-4.5-opus"; ORACLE_FALLBACK="gemini-3-pro-preview"
            EXPLORE_MODEL="gemini-3-flash-preview"; EXPLORE_FALLBACK="kimi-k2.5-free"
            LOOKER_MODEL="kimi-k2.5-free"; LOOKER_FALLBACK="gemini-3-flash-preview"
            LOCATOR_MODEL="gemini-3-flash-preview"; LOCATOR_FALLBACK="kimi-k2.5-free"
            ANALYZER_MODEL="codex-5.2"; ANALYZER_FALLBACK="kimi-k2.5-free"
            PATTERN_MODEL="codex-5.2"; PATTERN_FALLBACK="kimi-k2.5-free"
            LEDGER_MODEL="gemini-3-flash-preview"; LEDGER_FALLBACK="kimi-k2.5-free"
            ARTIFACT_MODEL="gemini-3-flash-preview"; ARTIFACT_FALLBACK="kimi-k2.5-free"
            META_MODEL="gemini-3-flash-preview"; META_FALLBACK="kimi-k2.5-free"
            ;;
    esac
    
    echo "   ✓ Agent models configured"
    echo ""
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}  WANDA Configuration Summary:${NC}"
    echo -e "${GREEN}  ────────────────────────────────────────────────────${NC}"
    echo -e "${GREEN}  • Name: $USER_NAME${NC}"
    echo -e "${GREEN}  • Workspace: $USER_WORKSPACE${NC}"
    echo -e "${GREEN}  • Language: $USER_LANGUAGE${NC}"
    echo -e "${GREEN}  • Hardware Profile: ${HARDWARE_PROFILE:-Unknown}${NC}"
    echo -e "${GREEN}  ────────────────────────────────────────────────────${NC}"
    if [ "$USE_OLLAMA" = "1" ]; then
        echo -e "${GREEN}  • Ollama: ENABLED (Direct Answer: ${OLLAMA_DIRECT_ANSWER:-1})${NC}"
        echo -e "${GREEN}    Primary: $OLLAMA_PRIMARY${NC}"
    else
        echo -e "${GREEN}  • Ollama: DISABLED (Cloud-only mode)${NC}"
    fi
    echo -e "${GREEN}  ────────────────────────────────────────────────────${NC}"
    echo -e "${GREEN}  7 PRIMARY AGENTS:${NC}"
    echo -e "${GREEN}  • Sisyphus (Orch):   $ORCHESTRATOR_MODEL${NC}"
    echo -e "${GREEN}  • Brainstormer:      $BRAINSTORMER_MODEL${NC}"
    echo -e "${GREEN}  • Prometheus (Arch): $ARCHITECT_MODEL${NC}"
    echo -e "${GREEN}  • Atlas (Dev):       $DEVELOPER_MODEL${NC}"
    echo -e "${GREEN}  • Audit:             $AUDIT_MODEL${NC}"
    echo -e "${GREEN}  • Librarian:         $LIBRARIAN_MODEL${NC}"
    echo -e "${GREEN}  • Writer:            $WRITER_MODEL${NC}"
    echo -e "${GREEN}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
    
    read -p "Is this correct? [Y/n]: " confirm
    case "${confirm:-y}" in
        [Nn]*) collect_user_info ;;
    esac
}

# Hardware Detection & Profile Assignment
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
    
    # Assign Hardware Profile (S/M/M-High/High)
    if [ "$VRAM_GB" -ge 16 ] || [ "$RAM_GB" -ge 48 ]; then
        HARDWARE_PROFILE="High"
        RECOMMENDED_OLLAMA="deepseek-r1:32b / qwen-2.5-coder:32b"
        TTS_MODEL="xtts-v2"
    elif [ "$VRAM_GB" -ge 10 ] || [ "$RAM_GB" -ge 32 ]; then
        HARDWARE_PROFILE="M-High"
        RECOMMENDED_OLLAMA="qwen-2.5-coder:14b"
        TTS_MODEL="xtts-v2"
    elif [ "$VRAM_GB" -ge 6 ] || [ "$RAM_GB" -ge 16 ]; then
        HARDWARE_PROFILE="M"
        RECOMMENDED_OLLAMA="gemma-3:9b / mistral:7b"
        TTS_MODEL="piper-fast"
    else
        HARDWARE_PROFILE="S"
        RECOMMENDED_OLLAMA="llama-3.2:3b (Lightweight)"
        TTS_MODEL="piper-fast"
    fi
    
    echo ""
    echo -e "${CYAN}╔═══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║  Hardware Profile: ${GREEN}${HARDWARE_PROFILE}${CYAN}                                        ║${NC}"
    echo -e "${CYAN}╠═══════════════════════════════════════════════════════════════╣${NC}"
    echo -e "${CYAN}║  Recommended Ollama: ${GREEN}${RECOMMENDED_OLLAMA}${NC}"
    echo -e "${CYAN}║  TTS Engine: ${GREEN}${TTS_MODEL}${NC}"
    echo -e "${CYAN}╚═══════════════════════════════════════════════════════════════╝${NC}"
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
        case "$OS" in
            linux)
                if command -v apt-get >/dev/null 2>&1; then
                    echo "  sudo apt install python3 python3-pip git gh"
                elif command -v dnf >/dev/null 2>&1; then
                    echo "  sudo dnf install python3 python3-pip git gh"
                elif command -v pacman >/dev/null 2>&1; then
                    echo "  sudo pacman -S python python-pip git github-cli"
                else
                    echo "  Install python3, pip, git, and GitHub CLI using your package manager"
                fi
                echo "  (For gh: see https://github.com/cli/cli/blob/trunk/docs/install_linux.md)"
                ;;
            macos)
                echo "  brew install python3 git gh"
                ;;
            *)
                echo "  Install python3, pip, git, and GitHub CLI"
                ;;
        esac
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
    
    # Create wanda CLI immediately so it's available even if install fails later
    create_wanda_cli
    
    echo -e "${GREEN}✓ Repository ready${NC}"
}

# Create the wanda CLI command
create_wanda_cli() {
    mkdir -p "$INSTALL_DIR/bin"
    
    cat > "$INSTALL_DIR/bin/wanda" << 'WANDA_EOF'
#!/bin/sh
# WANDA CLI - Main entry point

WANDA_DIR="${WANDA_INSTALL_DIR:-$HOME/.wanda-system}"
VERSION_FILE="$WANDA_DIR/.wanda-version"

    case "${1:-}" in
    update|--update|-u)
        echo "Checking for WANDA updates..."
        if [ -d "$WANDA_DIR" ]; then
            cd "$WANDA_DIR" && git pull --ff-only
            echo "WANDA updated!"
            echo "Run 'wanda' to see available commands"
        else
            echo "Error: WANDA directory not found at $WANDA_DIR"
            exit 1
        fi
        ;;
    status|--status|-s)
        echo "WANDA System Status"
        echo "==================="
        echo "Install directory: $WANDA_DIR"
        if [ -f "$VERSION_FILE" ]; then
            echo "Version: $(cat "$VERSION_FILE")"
        fi
        if [ -d "$WANDA_DIR/.git" ]; then
            cd "$WANDA_DIR"
            echo "Git branch: $(git branch --show-current 2>/dev/null || echo 'unknown')"
            echo "Last commit: $(git log -1 --format=%h 2>/dev/null || echo 'unknown')"
        fi
        ;;
    voice|--voice|-v)
        echo "Starting WANDA Voice Assistant..."
        if [ -f "$WANDA_DIR/wanda_local/main.py" ]; then
            cd "$WANDA_DIR/wanda_local" && python3 main.py
        else
            echo "Voice assistant not installed."
            echo "Try: wanda update"
            exit 1
        fi
        ;;
    opencode|agent)
        if command -v opencode >/dev/null 2>&1; then
            opencode "$@"
        else
            echo "opencode CLI not found. Run 'wanda reinstall' to install it."
            exit 1
        fi
        ;;
    reinstall|--reinstall)
        echo "Reinstalling WANDA..."
        if [ -f "$WANDA_DIR/install.sh" ]; then
            cd "$WANDA_DIR" && sh install.sh
        else
            echo "Install script not found. Run: wanda update"
            exit 1
        fi
        ;;
    help|--help|-h)
        echo "WANDA - Sovereign AI OS"
        echo ""
        echo "Usage: wanda [command]"
        echo ""
        echo "Commands:"
        echo "  wanda              Start Agent System (default)"
        echo "  wanda update       Update WANDA from git"
        echo "  wanda status       Show system status"
        echo "  wanda voice        Start voice assistant"
        echo "  wanda opencode     Run opencode CLI"
        echo "  wanda reinstall    Run installer again"
        echo "  wanda help         Show this help"
        ;;
    *)
        # Try finding opencode in PATH or default locations
        OPENCODE_BIN=""
        if command -v opencode >/dev/null 2>&1; then
            OPENCODE_BIN="opencode"
        elif [ -f "$HOME/.opencode/bin/opencode" ]; then
            OPENCODE_BIN="$HOME/.opencode/bin/opencode"
        fi

        if [ -n "$OPENCODE_BIN" ]; then
            "$OPENCODE_BIN"
        else
            echo "WANDA is installed at: $WANDA_DIR"
            echo ""
            echo "Note: opencode CLI not found. Run 'wanda reinstall' to install it."
            echo "Or run 'source ~/.zshrc' if you just installed it."
            echo ""
            echo "Run 'wanda help' for more commands."
        fi
        ;;
esac
WANDA_EOF
    chmod +x "$INSTALL_DIR/bin/wanda"
    
    # Add to PATH immediately for this session
    export WANDA_INSTALL_DIR="$INSTALL_DIR"
    export PATH="$INSTALL_DIR/bin:$PATH"
    
    # Add to shell profile for persistence
    SHELL_PROFILE=""
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_PROFILE="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_PROFILE="$HOME/.bashrc"
    elif [ -f "$HOME/.bash_profile" ]; then
        SHELL_PROFILE="$HOME/.bash_profile"
    fi
    
    if [ -n "$SHELL_PROFILE" ]; then
        if ! grep -q "WANDA_INSTALL_DIR" "$SHELL_PROFILE" 2>/dev/null; then
            echo "" >> "$SHELL_PROFILE"
            echo "# WANDA System" >> "$SHELL_PROFILE"
            echo "export WANDA_INSTALL_DIR=\"$INSTALL_DIR\"" >> "$SHELL_PROFILE"
            echo "export PATH=\"\$WANDA_INSTALL_DIR/bin:\$PATH\"" >> "$SHELL_PROFILE"
        fi
    fi
    
    # Create version file
    echo "1.0.4" > "$INSTALL_DIR/.wanda-version"
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
    case "${ans:-y}" in
        [Yy]*) INSTALL_AGENTS=1 ;;
    esac
    
    read -p "Install Voice Assistant? [Y/n]: " ans
    case "${ans:-y}" in
        [Yy]*) INSTALL_VOICE=1 ;;
    esac
    
    read -p "Install Telegram Bot? [y/N]: " ans
    case "$ans" in
        [Yy]*) INSTALL_TELEGRAM=1 ;;
    esac
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
            -e "s|{{AGENTS_CONFIG_PATH}}|$INSTALL_DIR/config/agents.yaml|g" \
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
        
        # Enforce Single Profile Policy
        if [ -f "$OPENCODE_CONFIG/opencode.json" ]; then
            rm "$OPENCODE_CONFIG/opencode.json"
            echo "  ✓ Verified Single Profile (removed legacy opencode.json)"
        fi
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
    
    if ! command -v opencode >/dev/null 2>&1; then
        echo "  - opencode CLI not found. Installing..."
        case "$OS" in
            macos)
                if curl -fsSL https://opencode.ai/install | sh; then
                    if [ -f "$HOME/.opencode/bin/opencode" ]; then
                        xattr -dr com.apple.quarantine "$HOME/.opencode/bin/opencode" 2>/dev/null || true
                    fi
                fi
                ;;
            *)
                curl -fsSL https://opencode.ai/install | sh
                ;;
        esac
    fi

    echo -e "${GREEN}✓ Agent System installed (with all plugins)${NC}"
}

# Install Voice Assistant
install_voice() {
    echo ""
    echo -e "${YELLOW}Installing Voice Assistant...${NC}"
    
    VOICE_DIR="$INSTALL_DIR/wanda-voice"
    
    if [ ! -d "$VOICE_DIR" ]; then
        echo -e "${RED}Voice module not found at $VOICE_DIR${NC}"
        return
    fi
    
    cd "$VOICE_DIR"
    
    # Install system dependencies (OS-specific)
    echo -e "${CYAN}Installing system dependencies...${NC}"
    case "$OS" in
        linux)
            if command -v apt-get >/dev/null 2>&1; then
                sudo apt-get update
                sudo apt-get install -y \
                    libgirepository1.0-dev \
                    libgirepository-2.0-dev \
                    gcc \
                    libcairo2-dev \
                    pkg-config \
                    python3-dev \
                    gir1.2-gtk-3.0 \
                    portaudio19-dev \
                    libportaudio2 \
                    2>/dev/null || echo -e "${YELLOW}Some system packages may already be installed${NC}"
            elif command -v dnf >/dev/null 2>&1; then
                sudo dnf install -y gcc cairo-devel pkgconfig python3-devel portaudio-devel || echo -e "${YELLOW}Some packages may already be installed${NC}"
            elif command -v pacman >/dev/null 2>&1; then
                sudo pacman -S --noconfirm gcc cairo pkgconf python portaudio || echo -e "${YELLOW}Some packages may already be installed${NC}"
            else
                echo -e "${YELLOW}Could not detect package manager. Please install dependencies manually.${NC}"
            fi
            ;;
        macos)
            if command -v brew >/dev/null 2>&1; then
                brew install pkg-config portaudio || echo -e "${YELLOW}Some packages may already be installed${NC}"
            else
                echo -e "${YELLOW}Homebrew not found. Install from https://brew.sh${NC}"
                echo -e "${YELLOW}Voice Assistant may not work without portaudio${NC}"
            fi
            ;;
        *)
            echo -e "${YELLOW}Unknown OS. Please install dependencies manually.${NC}"
            ;;
    esac
    
    # Create venv if not exists
    if [ ! -d "venv" ]; then
        echo -e "${CYAN}Creating Python virtual environment...${NC}"
        python3 -m venv venv
    fi
    
    # Install dependencies
    echo -e "${CYAN}Installing Python packages...${NC}"
    source venv/bin/activate
    pip install --upgrade pip --quiet
    pip install \
        sounddevice \
        numpy \
        vosk \
        faster-whisper \
        piper-tts \
        evdev \
        PyGObject \
        --quiet 2>/dev/null || echo -e "${YELLOW}Some packages may have warnings${NC}"
    
    # Download Vosk model
    if [ ! -d "model" ] || [ ! -f "model/final.mdl" ]; then
        echo -e "${CYAN}Downloading Vosk German model...${NC}"
        mkdir -p model
        cd model
        # Use curl (available on both Linux and macOS) instead of wget
        curl -fsSL --progress-bar -o vosk-model-small-de-0.15.zip https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
        unzip -q vosk-model-small-de-0.15.zip
        mv vosk-model-small-de-0.15/* . 2>/dev/null || true
        rm -rf vosk-model-small-de-0.15 vosk-model-small-de-0.15.zip
        cd ..
    fi
    
    echo -e "${GREEN}✓ Voice Assistant installed${NC}"
    echo -e "${CYAN}Usage: wanda voice${NC}"
}

# Install Telegram Bot (optional)
install_telegram() {
    echo ""
    echo -e "${YELLOW}Setting up Telegram Bot...${NC}"
    
    read -p "Do you have a Telegram Bot token? [y/N]: " has_token
    case "$has_token" in
        [Yy]*) ;;
        *)
            echo "  Skipping Telegram setup. Get a token from @BotFather later."
            return
            ;;
    esac
    
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
    echo -e "${BLUE}MCP Server Configuration${NC}"
    echo "   MCP servers provide WANDA with additional capabilities."
    echo ""
    
    if command -v docker >/dev/null 2>&1; then
        echo -e "   ${GREEN}✓ Docker detected${NC}"
        echo ""
        echo "   1) Install Docker MCP Gateway (recommended)"
        echo "   2) Use npx fallback (no Docker containers)"
        echo "   3) Skip MCP setup"
        read -p "   Choice [1]: " mcp_choice
        
        case "${mcp_choice:-1}" in
            1)
                USE_DOCKER_MCP=1
                echo ""
                echo -e "${YELLOW}Starting Docker MCP Gateway...${NC}"
                
                # Pull and run MCP gateway
                docker pull mcp/gateway:latest 2>/dev/null || true
                docker rm -f mcp-gateway 2>/dev/null || true
                docker run -d --name mcp-gateway \
                    -p 3100:3100 \
                    -v "$HOME/.mcp:/root/.mcp" \
                    mcp/gateway:latest 2>/dev/null && \
                    echo -e "${GREEN}✓ MCP Gateway running on port 3100${NC}" || \
                    echo -e "${YELLOW}⚠ MCP Gateway container not available, using config only${NC}"
                
                # API Key collection
                echo ""
                echo -e "${BLUE}API Keys (optional, press Enter to skip):${NC}"
                echo "   Du kannst diese später in $GEMINI_CONFIG/settings.json ändern"
                echo ""
                
                echo -e "   ${CYAN}GitHub PAT:${NC} https://github.com/settings/tokens"
                read -p "   GitHub Token: " GITHUB_TOKEN_INPUT
                
                echo -e "   ${CYAN}Brave Search:${NC} https://api-dashboard.search.brave.com/app/keys"
                read -p "   Brave API Key: " BRAVE_API_KEY_INPUT
                
                echo -e "   ${CYAN}Vercel:${NC} https://vercel.com/account/settings/tokens"
                read -p "   Vercel Token: " VERCEL_TOKEN_INPUT
                
                echo -e "   ${CYAN}Supabase:${NC} https://supabase.com/dashboard/account/tokens"
                read -p "   Supabase Token: " SUPABASE_TOKEN_INPUT
                
                echo -e "   ${CYAN}Stripe:${NC} https://dashboard.stripe.com/apikeys"
                read -p "   Stripe Secret Key: " STRIPE_KEY_INPUT
                
                echo -e "   ${CYAN}n8n (optional):${NC} Deine Instanz /settings/api"
                read -p "   n8n API Key: " N8N_KEY_INPUT
                
                # Process settings.json with API keys
                if [ -f "$INSTALL_DIR/mcp-servers/settings.json.template" ]; then
                    sed -e "s|{{HOME}}|$HOME|g" \
                        -e "s|{{GITHUB_TOKEN}}|${GITHUB_TOKEN_INPUT:-YOUR_GITHUB_TOKEN}|g" \
                        -e "s|{{BRAVE_API_KEY}}|${BRAVE_API_KEY_INPUT:-YOUR_BRAVE_KEY}|g" \
                        -e "s|{{VERCEL_TOKEN}}|${VERCEL_TOKEN_INPUT:-YOUR_VERCEL_TOKEN}|g" \
                        -e "s|{{SUPABASE_TOKEN}}|${SUPABASE_TOKEN_INPUT:-YOUR_SUPABASE_TOKEN}|g" \
                        -e "s|{{STRIPE_SECRET_KEY}}|${STRIPE_KEY_INPUT:-YOUR_STRIPE_KEY}|g" \
                        -e "s|{{N8N_API_KEY}}|${N8N_KEY_INPUT:-YOUR_N8N_KEY}|g" \
                        "$INSTALL_DIR/mcp-servers/settings.json.template" \
                        > "$GEMINI_CONFIG/settings.json"
                fi
                
                MCP_INSTALLED=1
                echo -e "${GREEN}✓ MCP Docker config complete${NC}"
                ;;
            2)
                USE_DOCKER_MCP=0
                echo ""
                echo -e "${YELLOW}Setting up npx-based MCP servers...${NC}"
                
                # Minimal npx config
                cat > "$GEMINI_CONFIG/settings.json" << 'EOF'
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@anthropic/mcp-server-filesystem", "$HOME"]
    }
  }
}
EOF
                # Cross-platform sed (macOS needs -i '', Linux needs just -i)
                if [ "$OS" = "macos" ]; then
                    sed -i '' "s|\$HOME|$HOME|g" "$GEMINI_CONFIG/settings.json"
                else
                    sed -i "s|\$HOME|$HOME|g" "$GEMINI_CONFIG/settings.json"
                fi
                
                MCP_INSTALLED=1
                echo -e "${GREEN}✓ npx MCP fallback configured${NC}"
                ;;
            *)
                MCP_INSTALLED=0
                echo "   Skipped MCP setup"
                ;;
        esac
    else
        echo -e "   ${YELLOW}Docker not found - using npx fallback${NC}"
        USE_DOCKER_MCP=0
        
        read -p "   Setup npx-based MCP servers? [Y/n]: " ans
        case "${ans:-y}" in
            [Yy]*)
                cat > "$GEMINI_CONFIG/settings.json" << 'EOF'
{
  "mcpServers": {
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
EOF
                MCP_INSTALLED=1
                echo -e "${GREEN}✓ npx MCP configured${NC}"
                ;;
            *)
                MCP_INSTALLED=0
                ;;
        esac
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
    
    if [ "$INSTALL_AGENTS" = "1" ] && ! command -v opencode >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  opencode CLI not found${NC}"
        case "$OS" in
            macos)
                echo "Installing opencode via curl (recommended for macOS M-series)..."
                if curl -fsSL https://opencode.ai/install | sh; then
                    echo -e "${GREEN}✓ opencode installed successfully${NC}"
                    if [ -f "$HOME/.opencode/bin/opencode" ]; then
                        xattr -dr com.apple.quarantine "$HOME/.opencode/bin/opencode" 2>/dev/null || true
                        echo "  ✓ Removed macOS quarantine attributes"
                    fi
                else
                    echo -e "${RED}✗ opencode installation failed${NC}"
                    echo "Try manually: curl -fsSL https://opencode.ai/install | sh"
                fi
                ;;
            *)
                echo "Install it with:"
                echo "  curl -fsSL https://opencode.ai/install | sh"
                ;;
        esac
        echo ""
    fi
    
    echo -e "${BLUE}Update:${NC}"
    echo "  cd $INSTALL_DIR && git pull"
    echo ""
    echo -e "${BLUE}Documentation:${NC}"
    echo "  $INSTALL_DIR/docs/"
    echo ""
    
    # wanda CLI was already created in get_repo() and should be working now
    echo -e "${GREEN}✓ 'wanda' command is ready to use${NC}"
    
    echo ""
    echo -e "${CYAN}Commands:${NC}"
    echo "  wanda          - Show status"
    echo "  wanda update   - Update WANDA from git"
    echo "  wanda status   - Show detailed status"
    echo "  wanda voice    - Start voice assistant"
    echo "  wanda help     - Show all commands"
    
    echo ""
    echo -e "${YELLOW}⚠️  Note: If 'wanda' command not found, run:${NC}"
    echo -e "   ${CYAN}source ~/.zshrc${NC}  (or ${CYAN}source ~/.bashrc${NC})"
    echo -e "   ${CYAN}# Or restart your terminal${NC}"
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
    
    # LANGUAGE SELECTION (First!)
    select_language
    
    # PERSONALIZATION
    collect_user_info
    
    check_hardware
    get_repo
    select_components
    
    [ "$INSTALL_AGENTS" = "1" ] && install_agents
    [ "$INSTALL_VOICE" = "1" ] && install_voice
    [ "$INSTALL_TELEGRAM" = "1" ] && install_telegram
    
    setup_mcp
    
    # REBRANDING
    if [ -f "$INSTALL_DIR/scripts/rebrand_binary.py" ]; then
        echo -e "${BLUE}Applying WANDA Branding...${NC}"
        python3 "$INSTALL_DIR/scripts/rebrand_binary.py" || true
    fi
    
    process_templates
    print_summary
}

main "$@"
