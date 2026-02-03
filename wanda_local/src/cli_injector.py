"""
CLI Injector Module - Execute Commands in Target CLI
====================================================
Injects prompts/commands into opencode, claude, or terminal.
"""

import subprocess
import json


class CLIInjector:
    """Injects prompts into various CLI tools."""

    async def inject(self, target: str, prompt: str, agent: str = None) -> dict:
        """
        Inject a prompt into the target CLI.
        
        Args:
            target: "opencode", "claude", or "terminal"
            prompt: The refined prompt to inject
            agent: Optional agent name for routing (opencode only)
            
        Returns:
            Dictionary with execution result
        """
        if target == "opencode":
            return await self._inject_opencode(prompt, agent)
        elif target == "claude":
            return await self._inject_claude(prompt)
        elif target == "terminal":
            return await self._inject_terminal(prompt)
        else:
            return {"error": f"Unknown target: {target}"}

    async def _inject_opencode(self, prompt: str, agent: str = None) -> dict:
        """Inject into opencode CLI."""
        cmd = ["opencode", "prompt"]
        if agent:
            cmd.extend(["--agent", agent])
        cmd.append(prompt)

        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            return {
                "success": result.returncode == 0,
                "summary": result.stdout[:500] if result.stdout else "Command executed.",
                "error": result.stderr if result.returncode != 0 else None,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out."}
        except FileNotFoundError:
            return {"success": False, "error": "opencode not found. Please install it."}

    async def _inject_claude(self, prompt: str) -> dict:
        """Inject into claude CLI."""
        try:
            result = subprocess.run(
                ["claude", "-p", prompt],
                capture_output=True,
                text=True,
                timeout=300,
            )
            return {
                "success": result.returncode == 0,
                "summary": result.stdout[:500] if result.stdout else "Command executed.",
            }
        except FileNotFoundError:
            return {"success": False, "error": "claude not found."}

    async def _inject_terminal(self, command: str) -> dict:
        """Execute a raw terminal command."""
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=60,
            )
            return {
                "success": result.returncode == 0,
                "summary": result.stdout[:500] if result.stdout else "Done.",
                "error": result.stderr if result.returncode != 0 else None,
            }
        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Command timed out."}
