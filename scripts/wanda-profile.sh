#!/bin/bash
# ==============================================================================
# WANDA Profile Switcher
# ==============================================================================
# Quick switch between OpenCode profiles
# Usage: wanda-profile [stable|experimental|status]
# ==============================================================================

PROFILES_DIR="$HOME/.wanda-system/wanda_cloud/profiles"
OPENCODE_CONFIG="$HOME/.config/opencode/opencode.jsonc"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

show_status() {
    echo ""
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo -e "${BLUE}  WANDA Profile Status${NC}"
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    
    if [ -L "$OPENCODE_CONFIG" ]; then
        current=$(readlink -f "$OPENCODE_CONFIG")
        if [[ "$current" == *"stable"* ]]; then
            echo -e "  Current: ${GREEN}STABLE${NC}"
            echo "  ✓ MiCode, oh-my-opencode, core plugins"
            echo "  ✓ Conservative permissions (bash: ask)"
        elif [[ "$current" == *"experimental"* ]]; then
            echo -e "  Current: ${YELLOW}EXPERIMENTAL${NC}"
            echo "  ✓ ALL plugins enabled (max stack)"
            echo "  ✓ Permissive mode (bash: allow)"
        else
            echo "  Current: Unknown profile"
        fi
        echo ""
        echo "  Path: $current"
    else
        echo "  No profile linked!"
        echo "  Run: wanda-profile stable"
    fi
    echo -e "${BLUE}═══════════════════════════════════════════════════════════════${NC}"
    echo ""
}

switch_stable() {
    ln -sf "$PROFILES_DIR/stable/opencode.jsonc" "$OPENCODE_CONFIG"
    echo -e "${GREEN}✓ Switched to STABLE profile${NC}"
    echo ""
    echo "  Plugins: oh-my-opencode, micode, ..."
    echo "  Permissions: bash=ask, edit=allow, read=allow"
    echo ""
    echo "  Restart opencode to apply changes."
}

switch_experimental() {
    ln -sf "$PROFILES_DIR/experimental/opencode.jsonc" "$OPENCODE_CONFIG"
    echo -e "${YELLOW}✓ Switched to EXPERIMENTAL profile${NC}"
    echo ""
    echo "  Plugins: ALL enabled (orchestrator, scheduler, ...)"
    echo "  Permissions: bash=allow, edit=allow, read=allow"
    echo ""
    echo "  ⚠️  WARNING: May have conflicts. Use for testing only."
    echo ""
    echo "  Restart opencode to apply changes."
}

show_help() {
    echo ""
    echo "WANDA Profile Switcher"
    echo ""
    echo "Usage: wanda-profile [command]"
    echo ""
    echo "Commands:"
    echo "  stable       Switch to STABLE profile (daily driver)"
    echo "  experimental Switch to EXPERIMENTAL profile (all features)"
    echo "  status       Show current profile status"
    echo "  help         Show this help"
    echo ""
    echo "Profiles:"
    echo "  STABLE"
    echo "    - MiCode + oh-my-opencode"
    echo "    - Core plugins only"
    echo "    - Conservative permissions"
    echo ""
    echo "  EXPERIMENTAL"
    echo "    - ALL plugins enabled"
    echo "    - ALL MCP servers active"
    echo "    - Permissive mode"
    echo ""
}

case "${1:-status}" in
    stable)
        switch_stable
        ;;
    experimental|exp)
        switch_experimental
        ;;
    status)
        show_status
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "Unknown command: $1"
        show_help
        ;;
esac
