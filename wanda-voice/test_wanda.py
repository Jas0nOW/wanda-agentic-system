#!/usr/bin/env python3
"""Wanda Interactive Test Suite - Validate before deployment."""

import sys
import os

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print('='*60)

def print_result(name, passed, details=""):
    icon = "✅" if passed else "❌"
    print(f"{icon} {name}")
    if details:
        print(f"   → {details}")
    return passed

def ask_user(prompt):
    """Ask user for confirmation."""
    try:
        response = input(f"\n{prompt} [y/n]: ").strip().lower()
        return response in ['y', 'yes', 'j', 'ja']
    except:
        return False

def test_imports():
    """Test all module imports."""
    print_header("1. MODULE IMPORTS")
    
    modules = [
        ("config.config", "Config"),
        ("audio.recorder", "AudioRecorder"),
        ("stt.faster_whisper_engine", "FasterWhisperEngine"),
        ("tts.piper_engine", "PiperEngine"),
        ("adapters.gemini_cli", "GeminiCLIAdapter"),
        ("conversation.state_machine", "StateMachine"),
        ("ui.orb", "WandaOrb"),
        ("mobile.notifier", "WandaNotifier"),
        ("mobile.project_init", "ProjectInitializer"),
    ]
    
    passed = 0
    for mod, cls in modules:
        try:
            m = __import__(mod, fromlist=[cls])
            print_result(f"{mod}", True)
            passed += 1
        except Exception as e:
            print_result(f"{mod}", False, str(e)[:50])
    
    return passed == len(modules)

def test_config():
    """Test config loading."""
    print_header("2. CONFIGURATION")
    
    try:
        from config.config import Config
        config = Config()
        
        checks = [
            ("Audio sample_rate", config.audio_config.get("sample_rate") == 16000),
            ("STT engine", config.stt.get("engine") == "faster-whisper"),
            ("TTS engine", config.tts.get("engine") == "piper"),
        ]
        
        all_passed = True
        for name, passed in checks:
            print_result(name, passed)
            all_passed = all_passed and passed
        
        return all_passed
    except Exception as e:
        print_result("Config loading", False, str(e))
        return False

def test_wayland():
    """Test Wayland/display detection."""
    print_header("3. DISPLAY SERVER")
    
    try:
        from system.active_window import detect_display_server, ActiveWindowDetector
        
        display = detect_display_server()
        print_result(f"Display: {display}", display in ["x11", "wayland"])
        
        detector = ActiveWindowDetector()
        window = detector.get_active_window()
        print_result(f"Active window: {window['name'][:30]}", window["name"] != "unknown")
        
        return True
    except Exception as e:
        print_result("Display detection", False, str(e))
        return False

def test_audio():
    """Test audio device."""
    print_header("4. AUDIO DEVICE")
    
    try:
        import sounddevice as sd
        
        devices = sd.query_devices()
        input_device = sd.query_devices(kind='input')
        
        print_result(f"Input device: {input_device['name'][:40]}", True)
        print_result(f"Sample rate: {int(input_device['default_samplerate'])}Hz", True)
        
        return True
    except Exception as e:
        print_result("Audio device", False, str(e))
        return False

def test_stt():
    """Test STT engine initialization."""
    print_header("5. STT (WHISPER)")
    
    try:
        from stt.faster_whisper_engine import FasterWhisperEngine
        
        print("   Loading model (this may take a moment)...")
        stt = FasterWhisperEngine(model_name="tiny", device="cpu")
        
        print_result("Whisper loaded (tiny model)", True)
        return True
    except Exception as e:
        print_result("STT initialization", False, str(e))
        return False

def test_tts():
    """Test TTS engine."""
    print_header("6. TTS (PIPER)")
    
    try:
        from tts.piper_engine import PiperEngine
        
        tts = PiperEngine()
        print_result(f"Piper voice: {tts.voice}", True)
        
        # Ask if user wants to test audio
        if ask_user("Test audio output? (will speak 'Wanda bereit')"):
            tts.speak("Wanda bereit", mode="short")
            print_result("Audio playback", ask_user("Did you hear 'Wanda bereit'?"))
        
        return True
    except Exception as e:
        print_result("TTS initialization", False, str(e))
        return False

def test_state_machine():
    """Test state machine."""
    print_header("7. STATE MACHINE")
    
    try:
        from conversation.state_machine import StateMachine, WandaMode
        
        sm = StateMachine()
        
        # Test transitions
        tests = [
            (WandaMode.PAUSED, "Aktiv→Paused"),
            (WandaMode.AKTIV, "Paused→Aktiv"),
            (WandaMode.AUTONOMOUS, "Aktiv→Autonomous"),
            (WandaMode.AKTIV, "Autonomous→Aktiv"),
        ]
        
        all_passed = True
        for target, name in tests:
            result = sm.transition(target)
            passed = sm.mode == target
            print_result(name, passed)
            all_passed = all_passed and passed
        
        return all_passed
    except Exception as e:
        print_result("State machine", False, str(e))
        return False

def test_project_init():
    """Test project initializer."""
    print_header("8. PROJECT INITIALIZER")
    
    try:
        from mobile.project_init import ProjectInitializer
        
        pi = ProjectInitializer()
        
        # Test parsing
        tests = [
            ("Erstelle Projekt TestApp", "create_project"),
            ("Neue Idee: Eine coole App", "capture_idea"),
        ]
        
        all_passed = True
        for text, expected in tests:
            result = pi.parse_command(text)
            passed = result and result["action"] == expected
            print_result(f'Parse "{text[:25]}..."', passed)
            all_passed = all_passed and passed
        
        return all_passed
    except Exception as e:
        print_result("ProjectInit", False, str(e))
        return False

def run_all_tests():
    """Run all tests."""
    print("\n" + "="*60)
    print("   🔧 WANDA INTERACTIVE TEST SUITE")
    print("="*60)
    
    results = {
        "Imports": test_imports(),
        "Config": test_config(),
        "Display": test_wayland(),
        "Audio": test_audio(),
        "STT": test_stt(),
        "TTS": test_tts(),
        "StateMachine": test_state_machine(),
        "ProjectInit": test_project_init(),
    }
    
    # Summary
    print_header("SUMMARY")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        print_result(name, result)
    
    print(f"\n{'='*60}")
    if passed == total:
        print(f"  ✅ ALL TESTS PASSED ({passed}/{total})")
        print(f"  🚀 Wanda is ready to run!")
    else:
        print(f"  ⚠️ {passed}/{total} tests passed")
        print(f"  Review failed tests before deployment.")
    print('='*60)
    
    return passed == total

if __name__ == "__main__":
    try:
        success = run_all_tests()
        
        if success:
            print("\n📌 Next steps:")
            print("   1. Run: ./wanda")
            print("   2. Click the orb for Daily Start")
            print("   3. Test voice commands")
            print("   4. Optional: Setup Telegram bot")
        
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest aborted.")
        sys.exit(1)
