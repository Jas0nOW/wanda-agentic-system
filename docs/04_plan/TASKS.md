# WANDA Implementation Tasks (Tickets)

> **Sprint Goal**: Establish the Doppel-Wanda Foundation (Local Gateway + Cloud Core).

## 🕵️ Phase 0: Research & Verification
- [ ] **T-001**: Verify Plugin Existence & Versions. `(DoD: SOURCES.md populated)`
- [ ] **T-002**: Verify Local Model paths (`brainstorm-36b`, `XTTS-v2`). `(DoD: Paths confirmed)`
- [ ] **T-003**: Init Repo Structure. `(DoD: All folders created)`

## 🛡️ Phase 1: OpenCode STABLE Profile
- [ ] **T-101**: Create `profiles/stable/opencode.jsonc`. `(DoD: Valid JSON, essential plugins only)`
- [ ] **T-102**: Configure `antigravity-auth` rotation. `(DoD: Switches to next key on 429)`
- [ ] **T-103**: Setup `envsitter-guard`. `(DoD: Committing .env fails)`

## 🧪 Phase 2: OpenCode EXPERIMENTAL Profile
- [ ] **T-201**: Create `profiles/experimental/opencode.jsonc`. `(DoD: Includes orchestration plugins)`
- [ ] **T-202**: Create `ROUTING_MAP.md`. `(DoD: Conflict resolution flowchart)`

## 🗣️ Phase 3: Voice Gateway (Local Service)
- [ ] **T-301**: Implement `wanda_local/src/vad.py` (Silero). `(DoD: Detects silence < 200ms)`
- [ ] **T-302**: Implement `wanda_local/src/stt.py` (Whisper). `(DoD: Returns text)`
- [ ] **T-303**: Implement `wanda_local/src/gateway.py` (Ollama). `(DoD: Refines "Make website" to JSON spec)`
- [ ] **T-304**: Implement `wanda_local/src/tts.py` (XTTS-v2). `(DoD: Speaks text with Wanda voice)`
- [ ] **T-305**: Build `install.sh` selector logic. `(DoD: Selects xtts for 50GB RAM)`

## 📱 Phase 4: Remote
- [ ] **T-401**: Telegram Bot Setup. `(DoD: Echoes message)`
- [ ] **T-402**: Voice Note Handler. `(DoD: Audio -> Text -> Task)`

## 🚀 Phase 5: Hardening
- [ ] **T-501**: Add Circuit Breaker. `(DoD: Fallback response when cloud 500s)`
- [ ] **T-502**: Run Smoke Tests. `(DoD: All pass)`
