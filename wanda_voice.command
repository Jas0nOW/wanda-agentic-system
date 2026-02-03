#!/bin/bash
# WANDA Launcher for macOS
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
TERM_APP="Terminal"

if [ -f "$HOME/.wanda-system/bin/wanda" ]; then
    "$HOME/.wanda-system/bin/wanda" voice
else
    echo "WANDA not installed."
    exit 1
fi
