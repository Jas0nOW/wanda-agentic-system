#!/bin/bash
# ==============================================================================
# WANDA Update System
# ==============================================================================
# Checks for updates and applies them automatically
# ==============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

INSTALL_DIR="${WANDA_INSTALL_DIR:-$HOME/.wanda-system}"
REPO_URL="https://github.com/jas0nOW/wanda-agentic-system"
VERSION_FILE="$INSTALL_DIR/.wanda-version"

# Get current local version
get_local_version() {
    if [ -f "$VERSION_FILE" ]; then
        cat "$VERSION_FILE"
    else
        echo "0.0.0"
    fi
}

# Get remote version from GitHub
get_remote_version() {
    curl -s "https://raw.githubusercontent.com/jas0nOW/wanda-agentic-system/main/VERSION" 2>/dev/null || echo "0.0.0"
}

# Compare versions (returns 0 if update available)
version_gt() {
    test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"
}

# Check for updates
check_update() {
    echo -e "${BLUE}Checking for WANDA updates...${NC}"
    
    LOCAL_VERSION=$(get_local_version)
    REMOTE_VERSION=$(get_remote_version)
    
    echo "  Local:  v$LOCAL_VERSION"
    echo "  Remote: v$REMOTE_VERSION"
    
    if version_gt "$REMOTE_VERSION" "$LOCAL_VERSION"; then
        echo -e "${GREEN}✨ Update available: v$LOCAL_VERSION → v$REMOTE_VERSION${NC}"
        return 0
    else
        echo -e "${GREEN}✓ WANDA is up to date${NC}"
        return 1
    fi
}

# Apply update
apply_update() {
    echo -e "${YELLOW}Updating WANDA...${NC}"
    
    if [ ! -d "$INSTALL_DIR/.git" ]; then
        echo -e "${RED}Error: WANDA not installed via git. Please reinstall.${NC}"
        exit 1
    fi
    
    cd "$INSTALL_DIR"
    
    # Stash local changes
    git stash -q 2>/dev/null || true
    
    # Pull latest
    git fetch origin main
    git reset --hard origin/main
    
    # Update version file
    if [ -f "$INSTALL_DIR/VERSION" ]; then
        cp "$INSTALL_DIR/VERSION" "$VERSION_FILE"
    fi
    
    echo -e "${GREEN}✓ WANDA updated to v$(get_local_version)${NC}"
    echo ""
    echo -e "${YELLOW}Changed files:${NC}"
    git log --oneline -5
}

# Interactive update prompt
prompt_update() {
    if check_update; then
        echo ""
        read -p "Update now? [Y/n]: " ans
        if [[ "${ans:-y}" =~ ^[Yy] ]]; then
            apply_update
        else
            echo "Update skipped. Run 'wanda update' anytime."
        fi
    fi
}

# Silent check (for startup)
silent_check() {
    LOCAL_VERSION=$(get_local_version)
    REMOTE_VERSION=$(get_remote_version)
    
    if version_gt "$REMOTE_VERSION" "$LOCAL_VERSION"; then
        echo -e "${CYAN}💡 WANDA update available: v$LOCAL_VERSION → v$REMOTE_VERSION${NC}"
        echo -e "   Run ${GREEN}wanda update${NC} to upgrade"
    fi
}

auto_update() {
    echo -e "${BLUE}WANDA Auto-Update Mode${NC}"
    echo ""
    
    LOCAL_VERSION=$(get_local_version)
    REMOTE_VERSION=$(get_remote_version)
    
    echo "  Local:  v$LOCAL_VERSION"
    echo "  Remote: v$REMOTE_VERSION"
    
    if version_gt "$REMOTE_VERSION" "$LOCAL_VERSION"; then
        echo -e "${YELLOW}🔄 Auto-updating WANDA...${NC}"
        apply_update
        echo ""
        echo -e "${GREEN}✅ WANDA has been automatically updated!${NC}"
        echo -e "${CYAN}Please restart WANDA to use the new version.${NC}"
        return 0
    else
        echo -e "${GREEN}✓ WANDA is already up to date${NC}"
        return 1
    fi
}

check_and_auto_update() {
    LOCAL_VERSION=$(get_local_version)
    REMOTE_VERSION=$(get_remote_version)
    
    if version_gt "$REMOTE_VERSION" "$LOCAL_VERSION"; then
        echo -e "${CYAN}🔄 Auto-updating WANDA v$LOCAL_VERSION → v$REMOTE_VERSION...${NC}"
        apply_update > /dev/null 2>&1
        return 0
    fi
    return 1
}

case "${1:-check}" in
    check)
        check_update
        ;;
    apply|update)
        if check_update; then
            apply_update
        fi
        ;;
    prompt)
        prompt_update
        ;;
    silent)
        silent_check
        ;;
    auto)
        auto_update
        ;;
    auto-silent)
        check_and_auto_update
        ;;
    *)
        echo "Usage: $0 {check|update|prompt|silent|auto|auto-silent}"
        exit 1
        ;;
esac
