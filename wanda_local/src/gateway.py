"""
Ollama Gateway Module - Prompt Refinement & Routing
====================================================
Uses local Ollama model to refine voice input and determine routing.
"""

import json
import httpx
from pathlib import Path


class OllamaGateway:
    """Interface to local Ollama model for prompt refinement."""

    def __init__(self, model: str = "brainstorm-36b", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        self.system_prompt = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """Load the system prompt from the prompts directory."""
        prompt_path = Path(__file__).parent.parent.parent / "prompts/system/OLLAMA_SYSTEM.md"
        if prompt_path.exists():
            return prompt_path.read_text()
        return "You are a helpful assistant that refines prompts and routes them to the appropriate agent."

    async def process(self, user_input: str) -> dict:
        """
        Process user input through Ollama and return structured response.
        
        Args:
            user_input: Raw transcribed text from STT
            
        Returns:
            Dictionary with routing info (intent, refined_prompt, target_agent, etc.)
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": self.system_prompt},
                        {"role": "user", "content": user_input},
                    ],
                    "stream": False,
                    "format": "json",
                },
            )

        if response.status_code != 200:
            print(f"[Gateway] Error: {response.status_code}")
            return self._fallback_response(user_input)

        try:
            result = response.json()
            content = result.get("message", {}).get("content", "{}")
            return json.loads(content)
        except json.JSONDecodeError:
            print("[Gateway] Failed to parse JSON response, using fallback.")
            return self._fallback_response(user_input)

    def _fallback_response(self, user_input: str) -> dict:
        """Fallback response when Ollama fails."""
        return {
            "intent": "Process user request",
            "refined_prompt": user_input,
            "target_agent": "developer",
            "target_cli": "opencode",
            "safety_flag": False,
            "confirmation_message": None,
        }
