# WANDA Voice Mode - Troubleshooting

## Common Issues

### No audio input detected
- Check `pavucontrol` or `wpctl status` for correct input device
- Verify microphone permissions
- Try: `python -c "import sounddevice; print(sounddevice.query_devices())"`

### STT produces gibberish/hallucinations
- Ensure `silence_threshold` is set correctly (default 0.01)
- Increase `min_seconds` to avoid processing noise-only clips
- Check audio levels: very quiet audio gets boosted and may hallucinate
- The anti-hallucination filters (no_speech_threshold, compression_ratio) should catch most cases

### Gemini CLI timeout
- Default timeout is 90s with 2 retries
- Check internet connection
- Check `gemini --version` works
- Increase timeout: `providers.gemini_timeout: 120`
- Enable Ollama as fallback: `providers.ollama_as_fallback: true`

### GTK/Orb not showing
- Install PyGObject: `pip install PyGObject`
- On Wayland: ensure `GDK_BACKEND=wayland` is set
- Fallback: use `--simple` mode which works without GTK
- COSMIC desktop: Orb uses `Gtk.WindowType.POPUP` which works on most compositors

### Hotkey not working (Wayland)
- evdev requires read access to `/dev/input/event*`
- Add user to `input` group: `sudo usermod -aG input $USER`
- Log out and back in
- Or run with `sudo` (not recommended for daily use)

### Ollama not starting
- Check if Ollama is installed: `ollama --version`
- Start manually: `ollama serve`
- Check port 11434: `curl http://localhost:11434/api/tags`
- Ensure model is pulled: `ollama pull qwen3:8b`

### Voice confirmation not working
- Ensure microphone is still active after first recording
- Increase `confirmation.timeout` if you need more time
- Say clearly: "Abschicken", "Verändern", "Nochmal", or "Abbrechen"
- Check STT output in LogWindow for what was actually transcribed

### TTS silent / no audio output
- Check speaker/headphone output
- Edge TTS requires internet; fallback to Piper for offline
- Piper needs model downloaded: check `~/.local/share/piper-voices/`
- Test: `python -c "from tts.piper_engine import PiperEngine; PiperEngine().speak('Test')"`

### API returns errors
- Ensure API is enabled: `api.enabled: true`
- Default port: 8370
- Check with: `curl http://localhost:8370/v1/health`
- API only binds to localhost by default

### High memory usage
- Whisper large-v3-turbo uses ~2-4GB
- Ollama models vary (qwen3:8b ~5GB)
- Reduce model size: `stt.model: base` for low-memory systems
- Ollama auto-unloads after 120s idle

## Logs

- Console output shows all pipeline stages
- LogWindow (GUI mode) shows real-time events
- Run artifacts saved to `~/.wanda/voice_runs/`
- Each run has `events.jsonl` and `summary.json`
