#!/bin/bash
# ==============================================================================
# GitHub Webhook Handler for VPS Auto-Deploy
# ==============================================================================
# This script is called by a simple HTTP listener when GitHub sends a webhook.
# Usage: ./deploy-hook.sh <repo_name> <branch>
# ==============================================================================

set -e

REPO_NAME="${1:-wanda-agentic-system}"
BRANCH="${2:-main}"
DEPLOY_DIR="/root/app"
LOG_FILE="/var/log/wanda-deploy.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "════════════════════════════════════════════════════════"
log "Deploy triggered for: $REPO_NAME ($BRANCH)"
log "════════════════════════════════════════════════════════"

# ──────────────────────────────────────────────────────────────────────────────
# WANDA Telegram Bot Deploy
# ──────────────────────────────────────────────────────────────────────────────
if [ "$REPO_NAME" = "wanda-agentic-system" ]; then
    log "Deploying WANDA Telegram Bot..."
    
    # Clone or pull latest
    if [ -d "$DEPLOY_DIR/wanda-agentic-system" ]; then
        cd "$DEPLOY_DIR/wanda-agentic-system"
        git fetch origin
        git reset --hard "origin/$BRANCH"
        log "Pulled latest from $BRANCH"
    else
        cd "$DEPLOY_DIR"
        git clone "https://github.com/jas0nOW/$REPO_NAME.git"
        log "Cloned $REPO_NAME"
    fi
    
    # Update telegram bot files
    cp "$DEPLOY_DIR/wanda-agentic-system/wanda_local/telegram_bot.py" "$DEPLOY_DIR/wanda-telegram/"
    cp "$DEPLOY_DIR/wanda-agentic-system/wanda_local/.env" "$DEPLOY_DIR/wanda-telegram/" 2>/dev/null || true
    
    # Restart PM2 process
    pm2 restart wanda-telegram
    log "PM2 restarted wanda-telegram"
    
    log "Deploy complete!"
fi

log "════════════════════════════════════════════════════════"
