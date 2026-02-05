#!/bin/bash
# Wanda Voice Assistant - Global Installation Script

set -e

INSTALL_DIR="/opt/wanda"
BIN_LINK="/usr/local/bin/wanda"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "🚀 Installing Wanda to $INSTALL_DIR..."

# Check if running as root or with sudo
if [ "$EUID" -ne 0 ]; then
    echo "❌ Please run with sudo: sudo ./install.sh"
    exit 1
fi

# Get the actual user (not root)
REAL_USER="${SUDO_USER:-$USER}"

# Create install directory
mkdir -p "$INSTALL_DIR"

# Copy files (excluding venv, will be recreated)
echo "📦 Copying files..."
rsync -a --exclude='venv' --exclude='__pycache__' --exclude='*.pyc' \
    "$SCRIPT_DIR/" "$INSTALL_DIR/"

# Set ownership
chown -R "$REAL_USER:$REAL_USER" "$INSTALL_DIR"

# Run setup as the real user
echo "⚙️  Running setup..."
sudo -u "$REAL_USER" bash -c "cd $INSTALL_DIR && python3 setup.py"

# Create global symlink
ln -sf "$INSTALL_DIR/wanda" "$BIN_LINK"
chmod +x "$BIN_LINK"

echo ""
echo "✅ Wanda installed successfully!"
echo ""
echo "Run from anywhere: wanda"
echo "Config location: $INSTALL_DIR/wanda.config.yaml"
