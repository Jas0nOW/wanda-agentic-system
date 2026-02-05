# WANDA TDD Guide - Test Driven Development

> **Version:** 1.0  
> **Last Updated:** 2026-02-05  
> **Purpose:** Guide for writing tests using TDD methodology

---

## 1. TDD Principles

### The TDD Cycle

```
1. RED    → Write a failing test
2. GREEN  → Write minimal code to pass
3. REFACTOR → Improve code while keeping tests green
```

### Golden Rules

1. **Write tests FIRST** - Always write the test before the implementation
2. **One concept per test** - Each test should verify one thing
3. **Tests are documentation** - Tests should explain what the code does
4. **Fast feedback** - Tests should run in < 1 second (unit tests)
5. **Independent tests** - Tests should not depend on each other

---

## 2. Test Structure

### AAA Pattern

```python
def test_wake_word_detection():
    # ARRANGE - Set up test data and conditions
    detector = WakeWordDetector()
    test_input = "wanda"
    
    # ACT - Execute the code being tested
    result = detector.detect(test_input)
    
    # ASSERT - Verify the result
    assert result is True
```

### Given-When-Then (Alternative)

```python
def test_audio_recording():
    """Given audio recorder is initialized
    When recording is started
    Then audio data should be captured
    """
    # Given
    recorder = AudioRecorder()
    
    # When
    audio = recorder.record(duration=1.0)
    
    # Then
    assert len(audio) > 0
```

---

## 3. Test Categories

### Unit Tests (`tests/unit/`)

- **Scope:** Single function/class
- **Speed:** < 1ms
- **Dependencies:** Mocked
- **Example:** Wake word detection, command parsing

```python
@pytest.mark.unit
def test_wake_word_exact_match():
    """Test exact wake word matching."""
    assert is_wake_word("wanda") is True
```

### Integration Tests (`tests/integration/`)

- **Scope:** Multiple components working together
- **Speed:** < 5s
- **Dependencies:** Real (but test instances)
- **Example:** Audio pipeline (VAD → STT → TTS)

```python
@pytest.mark.integration
def test_audio_pipeline():
    """Test complete audio processing pipeline."""
    pipeline = AudioPipeline()
    result = pipeline.process(b"audio_data")
    assert result.text is not None
```

### E2E Tests (`tests/e2e/`)

- **Scope:** Complete user flow
- **Speed:** < 30s
- **Dependencies:** Full system
- **Example:** Voice interaction from wake to response

```python
@pytest.mark.e2e
def test_full_voice_interaction():
    """Test complete voice interaction flow."""
    assistant = VoiceAssistant()
    assistant.process_wake_word()
    assistant.process_command("öffne firefox")
    assert assistant.last_command == "open_firefox"
```

### Regression Tests (`tests/regression/`)

- **Purpose:** Prevent bugs from reoccurring
- **Documentation:** Each test documents a fixed bug
- **Example:** Previously fixed wake word variations

```python
@pytest.mark.regression
def test_bug_001_wake_word_wander():
    """REGRESSION: Wake word 'wander' should trigger Wanda
    
    Bug: Wake word detection failed for 'wander', 'wanderer' variations
    Date: 2026-02-01
    Fixed: Added phonetic similarity matching
    """
    detector = WakeWordDetector()
    assert detector.detect("wander") is True
```

### Performance Tests (`tests/performance/`)

- **Purpose:** Catch performance regressions
- **Metrics:** Latency, throughput, memory
- **Thresholds:** Documented in test

```python
@pytest.mark.performance
def test_wake_word_detection_speed():
    """Benchmark: Wake word detection should be < 100ms."""
    start = time.perf_counter()
    is_wake_word("wanda")
    elapsed_ms = (time.perf_counter() - start) * 1000
    
    assert elapsed_ms < 100
```

---

## 4. Writing Good Tests

### DO ✅

```python
# DO: Use descriptive names
def test_wake_word_detects_phonetic_variations():
    """Test that phonetically similar words trigger detection."""
    variations = ["wander", "wanderer", "waller"]
    for variant in variations:
        assert is_wake_word(variant), f"Failed for: {variant}"

# DO: Test one concept per test
def test_command_parser_recognizes_send():
    """Test send command recognition."""
    assert parse_command("abschicken") == Command.SEND

def test_command_parser_recognizes_cancel():
    """Test cancel command recognition."""
    assert parse_command("abbrechen") == Command.CANCEL

# DO: Use fixtures for common setup
@pytest.fixture
def audio_recorder():
    """Provide configured audio recorder."""
    return AudioRecorder(silence_timeout=2.5)

def test_recording_duration(audio_recorder):
    """Test audio recording duration."""
    audio = audio_recorder.record(duration=3.0)
    assert len(audio) > 0

# DO: Document bugs in regression tests
def test_bug_003_audio_cutoff():
    """REGRESSION: Audio should not cut off prematurely
    
    Bug: Audio recording stopped after 1.2s silence
    Date: 2026-02-03
    Fixed: Increased silence_timeout to 2.5s
    """
    recorder = AudioRecorder(silence_timeout=2.5)
    audio = recorder.record()
    assert audio.duration >= 2.5
```

### DON'T ❌

```python
# DON'T: Test multiple concepts
def test_everything():  # ❌ Bad name
    """Test all the things."""  # ❌ Vague description
    assert is_wake_word("wanda")
    assert parse_command("abschicken")
    assert AudioRecorder().record()

# DON'T: Have logic in tests (keep them simple)
def test_with_logic():  # ❌ Too complex
    for i in range(10):
        if i % 2 == 0:
            assert something(i)
        else:
            assert something_else(i)

# DON'T: Depend on test order
def test_one():
    global state
    state = "modified"

def test_two():  # ❌ Depends on test_one
    assert state == "modified"

# DON'T: Ignore edge cases
def test_wake_word():  # ❌ Missing edge cases
    assert is_wake_word("wanda")
    # Missing: empty string, None, very long string, special chars
```

---

## 5. Test Data

### Fixtures (`conftest.py`)

```python
# tests/conftest.py

@pytest.fixture
def mock_audio_data():
    """Generate mock audio data."""
    return {
        "sample_rate": 16000,
        "channels": 1,
        "duration": 3.0,
        "data": bytes([0] * 16000 * 3 * 2),
    }

@pytest.fixture
def mock_wake_word_variations():
    """Wake word variations for testing."""
    return {
        "exact": ["wanda", "Wanda", "WANDA"],
        "phonetic": ["wander", "wanderer", "waller"],
        "false_positives": ["wonder", "winter", "water"],
    }
```

### Parametrized Tests

```python
@pytest.mark.parametrize("variant", [
    "wanda", "Wanda", "WANDA",
    "wander", "wanderer", "waller"
])
def test_wake_word_variations(variant):
    """Test various wake word spellings."""
    assert is_wake_word(variant) is True

@pytest.mark.parametrize("command,expected", [
    ("abschicken", Command.SEND),
    ("abschike", Command.SEND),
    ("abbrechen", Command.CANCEL),
    ("stop", Command.CANCEL),
])
def test_command_parsing(command, expected):
    """Test command parsing with various inputs."""
    assert parse_command(command) == expected
```

---

## 6. Running Tests

### Local Development

```bash
# Run all tests
pytest

# Run only unit tests (fast)
pytest tests/unit/ -v

# Run with coverage
pytest --cov=wanda_voice_core --cov-report=html

# Run specific test file
pytest tests/unit/test_wake_word.py -v

# Run tests matching pattern
pytest -k "wake_word" -v

# Run tests by marker
pytest -m "unit" -v
pytest -m "not slow" -v  # Exclude slow tests

# Run with debugger on failure
pytest --pdb

# Run with detailed output
pytest -xvs  # Exit on first failure, verbose, no capture
```

### Pre-commit

Tests run automatically before each commit:

```bash
# Install pre-commit hooks
pre-commit install

# Run manually
pre-commit run --all-files
```

### CI/CD

Tests run automatically on:
- Every push to main/develop
- Every pull request
- Nightly at 2 AM UTC

---

## 7. Test Checklist

Before submitting code:

- [ ] Tests are written BEFORE implementation (TDD)
- [ ] All tests pass locally (`pytest`)
- [ ] New code has > 90% coverage
- [ ] Regression tests added for bug fixes
- [ ] Performance tests pass (no regressions)
- [ ] Tests are documented (docstrings explain "why")
- [ ] No test depends on another test
- [ ] Tests use fixtures, not duplicated setup
- [ ] Edge cases are covered
- [ ] CI/CD pipeline passes

---

## 8. Common Patterns

### Mocking External Services

```python
from unittest.mock import Mock, patch

def test_provider_with_mock():
    """Test with mocked external provider."""
    mock_provider = Mock()
    mock_provider.generate.return_value = Mock(text="Mock response")
    
    service = VoiceService(provider=mock_provider)
    result = service.process("test")
    
    assert result == "Mock response"
    mock_provider.generate.assert_called_once_with("test")

@patch('wanda_voice_core.providers.gemini.requests.post')
def test_provider_with_patch(mock_post):
    """Test with patched HTTP request."""
    mock_post.return_value.json.return_value = {"text": "response"}
    
    result = gemini_provider.generate("prompt")
    
    assert result.text == "response"
```

### Testing Exceptions

```python
def test_recorder_raises_on_muted_mic():
    """Test that muted mic raises exception."""
    recorder = AudioRecorder()
    
    with patch.object(recorder, '_is_mic_muted', return_value=True):
        with pytest.raises(MicMutedError):
            recorder.record()
```

### Testing Asynchronous Code

```python
import pytest

@pytest.mark.asyncio
async def test_async_voice_command():
    """Test async voice command processing."""
    assistant = AsyncVoiceAssistant()
    
    result = await assistant.process_command("test")
    
    assert result.success is True
```

---

## 9. Resources

- [pytest Documentation](https://docs.pytest.org/)
- [Python Testing 101](https://realpython.com/python-testing/)
- [TDD Best Practices](https://testdriven.io/blog/modern-tdd/)
- [WANDA Test Strategy](../testing/DEEP_TESTING_STRATEGY.md)

---

**Remember:** Tests are not optional - they are the safety net that prevents bugs from reaching users!
