#!/bin/bash
# ==============================================================================
# WANDA Diagnostics Script
# ==============================================================================
# Checks system health and reports status.
# ==============================================================================

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

check_ok() { echo -e "${GREEN}[OK]${NC} $1"; }
check_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
check_fail() { echo -e "${RED}[FAIL]${NC} $1"; }

echo "=========================================="
echo "   WANDA System Diagnostics"
echo "=========================================="
echo ""

# Python
if command -v python3 &> /dev/null; then
    check_ok "Python3: $(python3 --version)"
else
    check_fail "Python3 not found"
fi

# Node
if command -v node &> /dev/null; then
    check_ok "Node.js: $(node --version)"
else
    check_fail "Node.js not found"
fi

# Bun
if command -v bun &> /dev/null; then
    check_ok "Bun: $(bun --version)"
else
    check_warn "Bun not found (optional)"
fi

# Ollama
if command -v ollama &> /dev/null; then
    check_ok "Ollama: installed"
    if pgrep -x "ollama" > /dev/null; then
        check_ok "Ollama service: running"
    else
        check_warn "Ollama service: not running (start with 'ollama serve')"
    fi
else
    check_fail "Ollama not found"
fi

# Docker
if command -v docker &> /dev/null; then
    check_ok "Docker: $(docker --version | cut -d ' ' -f 3)"
else
    check_warn "Docker not found (optional)"
fi

# OpenCode
if command -v opencode &> /dev/null; then
    check_ok "OpenCode: installed"
else
    check_warn "OpenCode not found (install with 'npm install -g opencode')"
fi

# Config symlink
CONFIG_FILE="$HOME/.config/opencode/opencode.jsonc"
if [ -L "$CONFIG_FILE" ]; then
    check_ok "OpenCode config: symlinked"
elif [ -f "$CONFIG_FILE" ]; then
    check_warn "OpenCode config: exists (not symlinked)"
else
    check_fail "OpenCode config: missing"
fi

# GPU
if command -v nvidia-smi &> /dev/null; then
    GPU_MEM=$(nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>/dev/null | head -1)
    check_ok "NVIDIA GPU: ${GPU_MEM}MB VRAM"
else
    check_warn "No NVIDIA GPU detected (CPU mode)"
fi

# RAM
TOTAL_RAM=$(free -g | awk '/^Mem:/{print $2}')
check_ok "RAM: ${TOTAL_RAM}GB"

# Ollama models
echo ""
echo "Ollama Models:"
if command -v ollama &> /dev/null; then
    ollama list 2>/dev/null || echo "  (Ollama not running)"
fi

echo ""
echo "=========================================="
echo "   Diagnostics Complete"
echo "=========================================="
