#!/bin/bash
# WANDA Voice Setup Script
# Automatische Installation aller Dependencies

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

VOICE_DIR="$HOME/.wanda-system/wanda-voice"

echo -e "${CYAN}============================================${NC}"
echo -e "${CYAN}  WANDA Voice - Setup Script${NC}"
echo -e "${CYAN}============================================${NC}"
echo ""

# Check if running in wanda-voice directory
if [ ! -f "voice_to_text.py" ]; then
    if [ -d "$VOICE_DIR" ]; then
        cd "$VOICE_DIR"
    else
        echo -e "${RED}Error: voice_to_text.py not found${NC}"
        echo "Please run this script from the wanda-voice directory"
        exit 1
    fi
fi

echo -e "${CYAN}Installing system dependencies...${NC}"
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
    ffmpeg

echo -e "${CYAN}Creating Python virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip

echo -e "${CYAN}Installing Python packages...${NC}"
pip install \
    sounddevice \
    numpy \
    vosk \
    faster-whisper \
    edge-tts \
    piper-tts \
    openwakeword \
    evdev \
    PyGObject

echo -e "${CYAN}Downloading Vosk German model...${NC}"
if [ ! -d "model" ] || [ ! -f "model/final.mdl" ]; then
    mkdir -p model
    cd model
    wget https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip
    unzip -q vosk-model-small-de-0.15.zip
    mv vosk-model-small-de-0.15/* .
    rm -rf vosk-model-small-de-0.15 vosk-model-small-de-0.15.zip
    cd ..
    echo -e "${GREEN}✓ Model installed${NC}"
else
    echo -e "${GREEN}✓ Model already exists${NC}"
fi

echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  Setup Complete!${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "Usage:"
echo "  source venv/bin/activate"
echo "  wanda voice"
echo ""
