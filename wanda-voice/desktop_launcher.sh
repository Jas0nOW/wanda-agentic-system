#!/bin/bash
# WANDA Desktop Launcher - Wayland Robust
# Dieses Skript findet automatisch den besten Weg, WANDA zu starten

set -e

INSTALL_DIR="${WANDA_INSTALL_DIR:-$HOME/.wanda-system}"
VOICE_DIR="$INSTALL_DIR/wanda-voice"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  WANDA Voice Launcher${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# Detect session type
SESSION_TYPE=${XDG_SESSION_TYPE:-unknown}
DESKTOP=${XDG_CURRENT_DESKTOP:-unknown}
echo "Session: $SESSION_TYPE"
echo "Desktop: $DESKTOP"
echo ""

# Check if voice is installed
if [ ! -d "$VOICE_DIR/venv" ]; then
    echo -e "${RED}Voice Assistant not installed!${NC}"
    echo "Running setup..."
    if [ -f "$VOICE_DIR/setup_voice.sh" ]; then
        cd "$VOICE_DIR"
        bash setup_voice.sh
    else
        echo -e "${RED}Setup script not found!${NC}"
        exit 1
    fi
fi

# Function to find best terminal
find_terminal() {
    # Priority order for COSMIC and Wayland
    TERMS=("cosmic-term" "kgx" "gnome-terminal" "alacritty" "kitty" "foot" "konsole" "xfce4-terminal" "xterm")
    
    for term in "${TERMS[@]}"; do
        if command -v "$term" &> /dev/null; then
            echo "$term"
            return
        fi
    done
    
    echo ""
}

# Function to launch in terminal
launch_in_terminal() {
    local term=$(find_terminal)
    
    if [ -z "$term" ]; then
        echo -e "${RED}No terminal emulator found!${NC}"
        echo "Please install: cosmic-term, alacritty, kitty, or gnome-terminal"
        exit 1
    fi
    
    echo -e "${CYAN}Using terminal: $term${NC}"
    
    cd "$VOICE_DIR"
    
    case "$term" in
        cosmic-term)
            cosmic-term -- bash -c "source venv/bin/activate && python voice_wrapper.py; read -p 'Press Enter to close...'"
            ;;
        kgx|gnome-terminal)
            $term -- bash -c "source venv/bin/activate && python voice_wrapper.py; read -p 'Press Enter to close...'"
            ;;
        alacritty|kitty|foot)
            $term -e bash -c "source venv/bin/activate && python voice_wrapper.py; read -p 'Press Enter to close...'"
            ;;
        *)
            $term -e "cd $VOICE_DIR && source venv/bin/activate && python voice_wrapper.py"
            ;;
    esac
}

# Main launch logic
if [ "$SESSION_TYPE" = "wayland" ]; then
    echo -e "${CYAN}Wayland detected - using terminal mode${NC}"
    echo ""
    launch_in_terminal
else
    echo -e "${CYAN}X11 detected${NC}"
    echo ""
    launch_in_terminal
fi
