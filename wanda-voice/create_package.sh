#!/bin/bash
# Create Wanda distribution package (without secrets)

set -e

VERSION="3.0.0"
PACKAGE_NAME="wanda-jarvis-${VERSION}"
DIST_DIR="dist"

echo "📦 Creating Wanda distribution package..."

# Create dist directory
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR/$PACKAGE_NAME"

# Copy core files
cp -r adapters audio config conversation modes preprocess stt tts ui system \
    "$DIST_DIR/$PACKAGE_NAME/" 2>/dev/null || true

# Copy scripts and docs
cp main.py setup.py install.sh wanda.service requirements.txt README.md \
    "$DIST_DIR/$PACKAGE_NAME/" 2>/dev/null || true

# Create clean config (without secrets)
cat > "$DIST_DIR/$PACKAGE_NAME/wanda.config.yaml" << 'EOF'
# Wanda JARVIS Configuration
# Run setup.py to configure

mode: jarvis

audio:
  sample_rate: 16000
  vad_engine: silero

trigger:
  key: rightctrl

stt:
  model: large-v3-turbo
  device: auto

tts:
  voice: de_DE-eva_k-x_low
  mode: short

output:
  speak: true
  sounds_enabled: true

adapters:
  gemini_model: flash

# Ollama (configure via setup.py)
ollama:
  enabled: false
  model: ""
EOF

# Create init files for packages
for dir in adapters audio config conversation modes preprocess stt tts ui system; do
    touch "$DIST_DIR/$PACKAGE_NAME/$dir/__init__.py" 2>/dev/null || true
done

# Remove any sensitive files
find "$DIST_DIR/$PACKAGE_NAME" -name "*.pyc" -delete
find "$DIST_DIR/$PACKAGE_NAME" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find "$DIST_DIR/$PACKAGE_NAME" -name ".env*" -delete
find "$DIST_DIR/$PACKAGE_NAME" -name "*.key" -delete
find "$DIST_DIR/$PACKAGE_NAME" -name "*.secret" -delete

# Create INSTALL instructions
cat > "$DIST_DIR/$PACKAGE_NAME/INSTALL.md" << 'EOF'
# Wanda JARVIS Installation

## Prerequisites

### Required
1. **Python 3.10+**
   ```bash
   python3 --version
   ```

2. **Audio (PipeWire or PulseAudio)**
   ```bash
   pactl info
   ```

3. **At least one AI CLI tool:**
   - Gemini: `npm install -g @anthropic-ai/gemini`
   - OpenCode: `curl -fsSL https://opencode.ai/install.sh | sh`

### Optional
4. **Ollama (local LLM)**
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull qwen2.5:32b
   ```

5. **xdotool (for CLI injection)**
   ```bash
   sudo apt install xdotool  # Debian/Ubuntu
   ```

## Installation

```bash
# Extract package
unzip wanda-jarvis-*.zip
cd wanda-jarvis-*

# Run setup wizard
python3 setup.py

# Start Wanda
./wanda
```

## Permissions
```bash
# Audio access
sudo usermod -aG audio $USER

# Input access (for hotkey)
sudo usermod -aG input $USER

# Logout and login again
```

## First Start
1. Press RIGHT CTRL to start recording
2. Speak your request
3. Press RIGHT CTRL again to process
4. Wanda reads response

## Commands
- "Wanda Pause" - Sleep mode
- "Hallo Wanda" - Wake up
- "Vollautonom" - Autonomous mode
EOF

# Create ZIP
cd "$DIST_DIR"
zip -r "${PACKAGE_NAME}.zip" "$PACKAGE_NAME"
cd ..

echo ""
echo "✅ Package created: $DIST_DIR/${PACKAGE_NAME}.zip"
echo ""
echo "Contents:"
ls -la "$DIST_DIR/$PACKAGE_NAME" | head -20
