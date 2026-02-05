# X10 Research: Agent Creation Best Practices (SOTA 2026)

> **Ziel:** Standardisiertes Playbook zur Erstellung robuster, skalierbarer AI-Agenten für WANDA OS.
> **Stack:** Python (Preferred), OpenCode Integration, MCP.

## 1. Definition & Purpose
Bevor Code geschrieben wird, muss der Agent definiert sein.
*   **Input:** Was kommt rein? (Text, Datei, Event)
*   **Output:** Was kommt raus? (Code, JSON, Bericht, Aktion)
*   **Side-Effects:** Darf er schreiben? Löschen? Deployen? (Permissions)

## 2. Modell-Auswahl (The Engine)
Wähle das Modell nach **Funktion**, nicht nach Hype.

| Anforderung | Modell-Empfehlung | Provider-Optionen |
| :--- | :--- | :--- |
| **High Speed / Low Cost** | Gemini 3 Flash | Google, Antigravity |
| **Max Reasoning / Architecture** | Claude Opus 4.5 Thinking | Anthropic, Antigravity |
| **Coding / Implementation** | Claude Sonnet 4.5 | Anthropic, Antigravity |
| **Creativity / UI** | Gemini 3 Pro | Google, Antigravity |
| **Fallback / Generalist** | GPT-5.2 | OpenAI |

## 3. Implementierung (Python-First)
Obwohl OpenCode Node.js nutzt, ist Python für Agenten-Logik (Data Science, RAG) oft überlegen.

### Tech Stack
*   **Framework:** LangChain (Orchestration) oder LlamaIndex (Data).
*   **Dependency Mgmt:** `poetry` oder `uv` (schneller als pip).
*   **Interface:** MCP Server (um den Agenten an OpenCode anzubinden).

### Code-Struktur (Best Practice)
```python
# agent_core.py
class AgentLogic:
    def __init__(self, model_client, tools):
        self.model = model_client
        self.tools = tools
        self.memory = []

    def run(self, prompt):
        # 1. Context Retrieval
        # 2. Reasoning (ReAct Loop)
        # 3. Tool Execution
        # 4. Response Generation
        pass
```

## 4. Tool-Integration & MCP
Agenten sollten nicht monolithisch sein. Sie nutzen Tools via **Model Context Protocol (MCP)**.
*   **Standard:** Definiere Tools als JSON-Schema.
*   **Verbindung:** Agent -> MCP Client -> MCP Server -> Tool.

## 5. State Management & Memory
*   **Short-Term:** Chat-History (im Context Window).
*   **Long-Term:** Vector DB (für RAG) oder Knowledge Graph (Memory MCP).
*   **Session:** Ledger-Files (Markdown) für Transparenz.

## 6. Fehlerbehandlung (Robustness)
*   **Retry:** Exponentielles Backoff bei API-Fehlern.
*   **Fallback:** Wenn Modell A versagt, nutze Modell B.
*   **Output Validation:** Prüfe JSON-Schema des Outputs (Pydantic).

## 7. Testing Strategy
*   **Unit Tests:** Logik ohne LLM (Mocks).
*   **Eval Tests:** Fixes Prompt-Set gegen das echte LLM (teuer, aber nötig).
*   **Regression:** Hat sich die Qualität verschlechtert?

## 8. Documentation Standards
*   `README.md`: Zweck, Install, Usage.
*   `API Docs`: Swagger/OpenAPI für Tools.
*   `Docstrings`: Google-Style oder NumPy-Style.
