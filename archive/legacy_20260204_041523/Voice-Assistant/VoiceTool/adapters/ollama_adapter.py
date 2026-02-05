# Wanda Voice Assistant - Ollama Adapter
"""Local LLM integration via Ollama for prompt optimization and delegation."""

import subprocess
import json
from typing import Optional, List, Dict, Any

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


# Ollama System Prompt for Wanda Tasks
OLLAMA_SYSTEM_PROMPT = """Du bist Wanda's lokaler Intelligenz-Kern. Du hilfst bei:

1. PROMPT-OPTIMIERUNG:
   - Verbessere Prompts für CLI-AI-Tools (Gemini, Opencode, Claude)
   - Sei präzise, füge Kontext hinzu, entferne Füllwörter
   - Behalte die Absicht des Users bei

2. DELEGATION:
   - Entscheide welches Tool am besten passt:
     * "gemini" → Allgemeine Fragen, Brainstorming
     * "opencode" → Code-Aufgaben, Projekte
     * "claude" → Komplexe Reasoning-Tasks
   - Gib nur das Tool-Keyword zurück

3. ZUSAMMENFASSUNG:
   - Fasse Konversationen kurz zusammen
   - Behalte wichtige Details
   - Max 2-3 Sätze

Antworte IMMER auf Deutsch, kurz und präzise."""


class OllamaAdapter:
    """
    Local LLM via Ollama for:
    - Prompt optimization
    - Delegation decisions
    - Briefing generation
    - Context summarization
    """
    
    def __init__(
        self, 
        model: str = "qwen2.5:32b",
        api_url: str = "http://localhost:11434",
        timeout: int = 30
    ):
        self.model = model
        self.api_url = api_url
        self.timeout = timeout
        self.available = False
        self.models: List[str] = []
        
        self._check_ollama()
    
    def _check_ollama(self):
        """Check if Ollama is running and get models."""
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                self.available = True
                # Parse model list
                lines = result.stdout.strip().split("\n")[1:]  # Skip header
                self.models = [line.split()[0] for line in lines if line]
                print(f"[Ollama] Available models: {self.models}")
            else:
                print("[Ollama] Not running")
        except FileNotFoundError:
            print("[Ollama] Not installed")
        except Exception as e:
            print(f"[Ollama] Error: {e}")
    
    def generate(self, prompt: str, system: str = OLLAMA_SYSTEM_PROMPT) -> Optional[str]:
        """Generate response from Ollama."""
        if not self.available or not REQUESTS_AVAILABLE:
            return None
        
        try:
            response = requests.post(
                f"{self.api_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "system": system,
                    "stream": False
                },
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json().get("response", "").strip()
            else:
                print(f"[Ollama] Error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"[Ollama] Request failed: {e}")
            return None
    
    def optimize_prompt(self, raw_prompt: str, target_tool: str = "gemini") -> str:
        """Optimize prompt for target tool."""
        if not self.available:
            return raw_prompt  # Fallback: return original
        
        optimization_prompt = f"""Optimiere diesen Prompt für {target_tool}:

Original: "{raw_prompt}"

Gib NUR den optimierten Prompt zurück, keine Erklärung."""

        result = self.generate(optimization_prompt)
        return result if result else raw_prompt
    
    def decide_delegation(self, user_input: str, context: str = "") -> str:
        """Decide which CLI tool to use."""
        if not self.available:
            return "gemini"  # Default fallback
        
        delegation_prompt = f"""Welches Tool passt am besten?

User sagt: "{user_input}"
Kontext: {context}

Antworte NUR mit: gemini, opencode, oder claude"""

        result = self.generate(delegation_prompt)
        
        # Parse result
        if result:
            result_lower = result.lower()
            if "opencode" in result_lower:
                return "opencode"
            elif "claude" in result_lower:
                return "claude"
        
        return "gemini"
    
    def generate_briefing(self, session_data: Dict[str, Any]) -> str:
        """Generate startup briefing."""
        if not self.available:
            return self._fallback_briefing(session_data)
        
        briefing_prompt = f"""Erstelle ein kurzes Startup-Briefing basierend auf:

{json.dumps(session_data, indent=2)}

Format: 2-3 Sätze, freundlich, informativ."""

        result = self.generate(briefing_prompt)
        return result if result else self._fallback_briefing(session_data)
    
    def summarize_context(self, messages: List[Dict]) -> str:
        """Summarize conversation for context preservation."""
        if not self.available or not messages:
            return ""
        
        text = "\n".join(f"{m['role']}: {m['content'][:100]}" for m in messages[-10:])
        
        summary_prompt = f"""Fasse diese Konversation in 1-2 Sätzen zusammen:

{text}"""

        result = self.generate(summary_prompt)
        return result if result else ""
    
    def _fallback_briefing(self, data: Dict) -> str:
        """Fallback briefing without Ollama."""
        last = data.get("last_session", {})
        if last:
            age_min = int(last.get("age", 0) / 60)
            return f"Letzte Session vor {age_min} Minuten. Womit sollen wir starten?"
        return "Bereit für eine neue Session. Wie kann ich helfen?"
    
    def get_best_model(self, task: str = "general") -> str:
        """Get best available model for task."""
        if not self.models:
            return self.model
        
        # Prefer larger models for complex tasks
        preferred = {
            "reasoning": ["qwen2.5:32b", "deepseek:33b", "mixtral:8x7b"],
            "fast": ["qwen2.5:7b", "mistral:7b", "llama3.1:8b"],
            "general": self.models
        }
        
        for model in preferred.get(task, self.models):
            if model in self.models:
                return model
        
        return self.models[0] if self.models else self.model


if __name__ == "__main__":
    print("Testing Ollama Adapter...")
    adapter = OllamaAdapter()
    
    if adapter.available:
        print(f"✅ Ollama available, models: {adapter.models}")
        
        # Test prompt optimization
        result = adapter.optimize_prompt("mach mir ne website", "opencode")
        print(f"Optimized: {result}")
    else:
        print("❌ Ollama not available")
