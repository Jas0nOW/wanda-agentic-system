# WANDA Deep Testing Strategy
## Automated Bug Prevention & System Validation

> **Version:** 1.0  
> **Created:** 2026-02-05  
> **Purpose:** Prevent recurring bugs through automated testing

---

## 1. Overview

This document defines a comprehensive testing strategy to catch bugs BEFORE they reach production. Based on the recent voice system issues (wake word, send commands, audio cutoff), we need automated tests that verify:

- Voice recognition accuracy
- Command parsing robustness  
- Audio handling reliability
- System integration stability

---

## 2. Test Categories

### 2.1 Unit Tests (Fast - < 1s each)

**Wake Word Detection Tests:**
```python
def test_wake_word_variations():
    """Test phonetic similarity matching"""
    variations = ["wanda", "wander", "wanderer", "waller", "vanda"]
    for variant in variations:
        assert is_wake_word(variant), f"Failed for: {variant}"

def test_false_positives():
    """Ensure non-wake words don't trigger"""
    negatives = ["wonder", "winter", "water", "hello"]
    for word in negatives:
        assert not is_wake_word(word), f"False positive: {word}"
```

**Command Confirmation Tests:**
```python
def test_send_command_variations():
    """Test German send command variations"""
    commands = [
        "abschicken", "abschike", "abschik", "schick",
        "senden", "sende", "bestätigen"
    ]
    for cmd in commands:
        assert detect_confirmation(cmd) == "send", f"Failed: {cmd}"
```

**Input Sanitization Tests:**
```python
def test_dangerous_input_blocked():
    """Ensure malicious input is sanitized"""
    dangerous = [
        "; rm -rf /",
        "$(whoami)",
        "`cat /etc/passwd`",
        "<script>alert(1)</script>"
    ]
    for input in dangerous:
        sanitized = sanitize_input(input)
        assert ";" not in sanitized
        assert "`" not in sanitized
        assert "$" not in sanitized
```

### 2.2 Integration Tests (Medium - 1-5s each)

**Audio Pipeline Tests:**
```python
def test_audio_recording_duration():
    """Ensure audio doesn't cut off prematurely"""
    recorder = AudioRecorder()
    start_time = time.time()
    audio = recorder.record(max_duration=5.0)
    duration = time.time() - start_time
    assert duration >= 4.5, "Audio cut off too early"
    assert duration <= 5.5, "Audio exceeded max duration"

def test_silence_detection():
    """Test silence timeout behavior"""
    recorder = AudioRecorder(silence_timeout=2.5)
    # Simulate audio with silence
    audio = recorder.record_with_silence_detection()
    assert recorder.silence_detected
    assert audio.duration > 0
```

**Provider Fallback Tests:**
```python
def test_gemini_429_fallback():
    """Test fallback to local model on rate limit"""
    provider = GeminiProvider()
    # Mock 429 error
    with patch('requests.post', side_effect=RateLimitError()):
        result = provider.generate("test prompt", fallback=True)
        assert result.source == "local_fallback"
```

### 2.3 End-to-End Tests (Slow - 5-30s each)

**Voice Flow Tests:**
```python
def test_full_voice_interaction():
    """Test complete voice interaction flow"""
    voice = VoiceAssistant()
    
    # Simulate wake word
    voice.process_audio("wanda")
    assert voice.state == "listening"
    
    # Simulate command
    voice.process_audio("öffne firefox")
    assert voice.state == "processing"
    
    # Verify command execution
    assert voice.last_command == "open_firefox"
```

**Race Condition Tests:**
```python
def test_concurrent_voice_commands():
    """Ensure no race conditions with rapid commands"""
    import threading
    
    results = []
    def send_command(cmd):
        result = voice.process(cmd)
        results.append(result)
    
    # Send multiple commands rapidly
    threads = [
        threading.Thread(target=send_command, args=("wanda",)),
        threading.Thread(target=send_command, args=("stop",)),
        threading.Thread(target=send_command, args=("wanda",))
    ]
    
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    # Should not crash or hang
    assert len(results) == 3
```

---

## 3. Automated Test Runner

### 3.1 Pre-Commit Hooks

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: wanda-unit-tests
        name: WANDA Unit Tests
        entry: pytest tests/unit/ -xvs
        language: system
        pass_filenames: false
        
      - id: wanda-integration-tests
        name: WANDA Integration Tests  
        entry: pytest tests/integration/ -xvs
        language: system
        pass_filenames: false
        stages: [push]
```

### 3.2 CI/CD Pipeline

```yaml
# .github/workflows/test.yml
name: WANDA Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run Unit Tests
        run: pytest tests/unit/ -v --tb=short
      
      - name: Run Integration Tests  
        run: pytest tests/integration/ -v --tb=short
      
      - name: Run E2E Tests
        run: pytest tests/e2e/ -v --tb=short
        timeout-minutes: 10
      
      - name: Generate Coverage Report
        run: pytest --cov=wanda --cov-report=xml
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
```

---

## 4. Test Data & Fixtures

### 4.1 Audio Test Samples

```python
# tests/fixtures/audio_samples.py
TEST_AUDIO_SAMPLES = {
    "wake_word": [
        "wanda_clear.wav",
        "wanda_noisy.wav", 
        "wander_variation.wav",
        "wanderer_variation.wav"
    ],
    "commands": [
        "abschicken_clear.wav",
        "abschicken_muffled.wav",
        "stop_command.wav",
        "cancel_command.wav"
    ],
    "background_noise": [
        "typing_noise.wav",
        "music_background.wav",
        "conversation_bg.wav"
    ]
}
```

### 4.2 Mock Providers

```python
# tests/mocks/providers.py
class MockGeminiProvider:
    """Mock Gemini provider for testing"""
    
    def __init__(self, fail_rate=0.0):
        self.fail_rate = fail_rate
        self.call_count = 0
    
    def generate(self, prompt):
        self.call_count += 1
        if random.random() < self.fail_rate:
            raise RateLimitError("429 Too Many Requests")
        return MockResponse(text="Mock response")
```

---

## 5. Bug Regression Tests

For every bug found, create a regression test:

```python
# tests/regression/test_voice_bugs.py

class TestVoiceBugRegressions:
    """Tests for previously fixed voice bugs"""
    
    def test_bug_001_wake_word_wander(self):
        """REGRESSION: Wake word 'wander' should trigger Wanda
        
        Bug: Wake word detection failed for 'wander', 'wanderer' variations
        Fixed: Added phonetic similarity matching in wake_word.py
        """
        detector = WakeWordDetector()
        assert detector.detect("wander")
        assert detector.detect("wanderer") 
        assert detector.detect("waller")
    
    def test_bug_002_send_command_fuzzy(self):
        """REGRESSION: Send command variations should work
        
        Bug: 'abschike', 'abschik' not recognized as send commands
        Fixed: Added fuzzy matching with 80% threshold
        """
        parser = CommandParser()
        for variant in ["abschike", "abschik", "abschicken"]:
            assert parser.parse(variant) == Command.SEND
    
    def test_bug_003_audio_cutoff(self):
        """REGRESSION: Audio should not cut off prematurely
        
        Bug: Audio recording stopped after 1.2s silence
        Fixed: Increased silence_timeout to 2.5s
        """
        recorder = AudioRecorder(silence_timeout=2.5)
        audio = recorder.record_silence_test(duration=3.0)
        assert audio.duration >= 2.5, "Audio cut off too early"
    
    def test_bug_004_mic_mute_detection(self):
        """REGRESSION: Should detect if microphone is muted
        
        Bug: Voice system didn't check if mic was muted
        Fixed: Added _is_mic_muted() check in recorder.py
        """
        recorder = AudioRecorder()
        # Mock muted mic
        with patch('subprocess.run', return_value=Mock(stdout='yes')):
            assert recorder._is_mic_muted()
            with pytest.raises(MicMutedError):
                recorder.record()
```

---

## 6. Performance Benchmarks

```python
# tests/performance/test_benchmarks.py

class TestPerformanceBenchmarks:
    """Performance tests to catch regressions"""
    
    def test_wake_word_detection_speed(self):
        """Wake word detection should be < 100ms"""
        detector = WakeWordDetector()
        
        start = time.perf_counter()
        result = detector.detect("wanda")
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 100, f"Too slow: {elapsed:.2f}ms"
    
    def test_command_parsing_speed(self):
        """Command parsing should be < 50ms"""
        parser = CommandParser()
        
        start = time.perf_counter()
        result = parser.parse("öffne firefox")
        elapsed = (time.perf_counter() - start) * 1000
        
        assert elapsed < 50, f"Too slow: {elapsed:.2f}ms"
    
    def test_memory_usage(self):
        """Memory usage should stay below 500MB"""
        import psutil
        process = psutil.Process()
        
        # Run voice system for 1 minute
        voice = VoiceAssistant()
        voice.start()
        time.sleep(60)
        
        mem_mb = process.memory_info().rss / 1024 / 1024
        assert mem_mb < 500, f"Memory too high: {mem_mb:.1f}MB"
```

---

## 7. Test Execution

### 7.1 Local Development

```bash
# Run all tests
pytest

# Run only unit tests (fast)
pytest tests/unit/ -v

# Run with coverage
pytest --cov=wanda --cov-report=html

# Run specific test file
pytest tests/unit/test_wake_word.py -v

# Run tests matching pattern
pytest -k "wake_word" -v
```

### 7.2 Continuous Integration

Tests run automatically on:
- Every commit
- Every pull request
- Nightly builds

---

## 8. Test Maintenance

### 8.1 Adding New Tests

For every new feature or bug fix:
1. Write test FIRST (TDD)
2. Run test to confirm it fails
3. Implement fix/feature
4. Run test to confirm it passes
5. Add to regression suite

### 8.2 Updating Tests

When behavior intentionally changes:
1. Update test to reflect new behavior
2. Document reason in test docstring
3. Ensure backward compatibility if possible

---

## 9. Success Metrics

- **Code Coverage:** > 90%
- **Test Pass Rate:** 100% on main branch
- **Bug Escape Rate:** < 1% (bugs caught in production)
- **Test Execution Time:** < 5 minutes for full suite

---

## 10. Next Steps

1. [ ] Implement unit tests for wake word detection
2. [ ] Implement integration tests for audio pipeline
3. [ ] Set up CI/CD pipeline with GitHub Actions
4. [ ] Add pre-commit hooks
5. [ ] Create test fixtures and mock data
6. [ ] Document test writing guidelines
7. [ ] Train team on TDD practices

---

**Remember:** Tests are not optional - they are the safety net that prevents bugs from reaching users!
