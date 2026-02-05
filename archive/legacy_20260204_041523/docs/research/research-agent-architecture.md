# X10 Research: Agent System Architecture (SOTA 2026)

> **Ziel:** Blueprint für eine skalierbare, sichere Multi-Agenten-Architektur.

## 1. Schichten-Modell (The 7 Layers)
Das System ist streng hierarchisch organisiert, um Chaos zu vermeiden.

1.  **Ideation:** Reines Denken, keine Side-Effects. (Brainstormer)
2.  **Orchestration:** Routing & Management. (Sisyphus)
3.  **Core:** Die "Arbeiter". (Architect, Dev, Audit)
4.  **Specialist:** Experten auf Abruf. (Oracle, Writer)
5.  **Research:** Informationsbeschaffung (Read-Only). (Librarian, Explore)
6.  **Continuity:** Gedächtnis & State. (Ledger)
7.  **Meta:** Überwachung & Strategie. (Metis, Momus)

> **Hinweis:** Upstream-Quellen nennen `Sisyphus` als Default-Orchestrator. In WANDA ist **Commander** der einzige Primary; `Sisyphus` bleibt als Plugin-Default deaktiviert.

## 2. Kommunikationsprotokoll (MCP)
Das **Model Context Protocol (MCP)** ist der Standard für Inter-Agent- und Agent-Tool-Kommunikation.
*   **Vorteil:** Standardisierte Schnittstellen. Ein Agent muss nicht wissen, *wie* ein Tool in Python implementiert ist, er muss nur das Schema kennen.
*   **Async:** Für langlaufende Tasks (z.B. Crawling) Nutzung von Queues (RabbitMQ/NATS für Enterprise, lokale Job-Files für Single-User).

## 3. Skalierbarkeit & Deployment
*   **Containerisierung:** Jeder Agent/MCP-Server in einem Docker-Container.
*   **Isolierung:** Verhindert Dependency-Hölle.
*   **Auto-Scaling:** Bei hoher Last (z.B. Batch-Processing von 100 Files) können Worker-Agenten skaliert werden (Kubernetes/Docker Swarm).

## 4. Sicherheit (Zero-Trust)
*   **Input Validation:** Traue keinem User-Input und keinem LLM-Output ungeprüft.
*   **Least Privilege:** Ein Research-Agent darf nicht schreiben. Ein Dev-Agent darf nicht deployen (ohne Approval).
*   **Secrets:** Niemals im Code oder Prompt. Nutzung von Environment Variables oder Vaults.
*   **Sandboxing:** Code-Execution (z.B. Python Interpreter) immer in isolierter Sandbox.

## 5. Monitoring & Observability
*   **Tracing:** Verfolge den "Gedankengang" über mehrere Agenten hinweg (OpenTelemetry).
*   **Cost Tracking:** Token-Verbrauch pro Agent/Task.
*   **Quality Metrics:** Erfolgsrate von Fixes, Anzahl der Iterationen.
*   **Alerting:** Bei API-Ausfällen oder Budget-Überschreitung.
