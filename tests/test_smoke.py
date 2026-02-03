"""
WANDA Smoke Tests
=================
Basic tests to verify the voice pipeline and safety systems.
"""

import pytest
from pathlib import Path


class TestSafetyChecker:
    """Tests for the command safety validation."""

    def test_denylist_blocks_rm_rf_root(self):
        """Ensure rm -rf / is blocked."""
        from wanda_local.src.safety import SafetyChecker, SafetyLevel
        
        checker = SafetyChecker()
        result = checker.check("rm -rf /")
        assert result.level == SafetyLevel.DENY

    def test_denylist_blocks_cat_shadow(self):
        """Ensure cat /etc/shadow is blocked."""
        from wanda_local.src.safety import SafetyChecker, SafetyLevel
        
        checker = SafetyChecker()
        result = checker.check("cat /etc/shadow")
        assert result.level == SafetyLevel.DENY

    def test_confirmlist_requires_confirmation_for_git_force(self):
        """Ensure git push --force requires confirmation."""
        from wanda_local.src.safety import SafetyChecker, SafetyLevel
        
        checker = SafetyChecker()
        result = checker.check("git push --force")
        assert result.level == SafetyLevel.CONFIRM

    def test_allowlist_allows_git_status(self):
        """Ensure git status is allowed."""
        from wanda_local.src.safety import SafetyChecker, SafetyLevel
        
        checker = SafetyChecker()
        result = checker.check("git status")
        assert result.level == SafetyLevel.ALLOW

    def test_allowlist_allows_npm_install(self):
        """Ensure npm install is allowed."""
        from wanda_local.src.safety import SafetyChecker, SafetyLevel
        
        checker = SafetyChecker()
        result = checker.check("npm install")
        assert result.level == SafetyLevel.ALLOW


class TestOllamaGateway:
    """Tests for the Ollama gateway (requires running Ollama)."""

    @pytest.mark.asyncio
    @pytest.mark.skip(reason="Requires running Ollama service")
    async def test_gateway_returns_valid_json(self):
        """Ensure gateway returns structured JSON."""
        from wanda_local.src.gateway import OllamaGateway
        
        gateway = OllamaGateway(model="brainstorm-36b")
        result = await gateway.process("Create a new React app")
        
        assert "intent" in result
        assert "refined_prompt" in result
        assert "target_agent" in result


class TestFileStructure:
    """Tests for project structure integrity."""

    def test_prompts_directory_exists(self):
        """Ensure prompts directory is present."""
        prompts_dir = Path(__file__).parent.parent / "prompts"
        assert prompts_dir.exists()

    def test_ollama_system_prompt_exists(self):
        """Ensure OLLAMA_SYSTEM.md is present."""
        prompt_path = Path(__file__).parent.parent / "prompts/system/OLLAMA_SYSTEM.md"
        assert prompt_path.exists()

    def test_terminal_policy_exists(self):
        """Ensure TERMINAL_POLICY.md is present."""
        policy_path = Path(__file__).parent.parent / "prompts/system/TERMINAL_POLICY.md"
        assert policy_path.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
