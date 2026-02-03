# X10 Deep Research: WANDA System Optimization (2026)

> **Status:** ANALYSIS COMPLETE
> **Ziel:** Validierung der 18-Agenten-Architektur, Modell-Optimierung und Eliminierung von Redundanzen.
> **Methode:** Vergleich gegen "Factory Standards" und SOTA-Architektur-Prinzipien.

---

## 1. Baseline: Der "Factory Standard" (Referenz)

### OpenCode (Core)
*   **Architektur:** Config-agnostisch.
*   **Standard:** Keine festen Agenten, nutzt `systemDefaultModel`.

### Oh-My-OpenCode (Plugin)
*   **Architektur:** Team-basiert (9 Agenten).
*   **Standard-Stack:**
> **Hinweis:** Upstream-Quellen nennen `Sisyphus` als Default-Orchestrator. In WANDA ist **Commander** der einzige Primary; `Sisyphus` bleibt als Plugin-Default deaktiviert.

*   Orchestrator: **Sisyphus** (Claude)
    *   Think Tank: **Oracle** (GPT)
    *   Research: **Librarian** (GLM/Sonnet)
    *   Mapping: **Explore** (Haiku)

---

## 2. WANDA Analyse (Ist-Zustand vs. Soll)

*Basierend auf Codebase-Scan (Feb 2026).*

### 🚨 Kritische Befunde
1.  **Orchestrator Mismatch:** `Commander` nutzt `gpt-5.2-codex`.
    *   *Problem:* Codex-Modelle sind auf Code-Vervollständigung trainiert, nicht auf Task-Routing. Sie sind teuer und haben oft kleinere Kontext-Fenster als Flash-Modelle.
    *   *Empfehlung:* Wechsel auf **Gemini 3 Flash** (Massive Context + Speed) oder **Claude Haiku 4.5**.
2.  **Redundanz-Cluster "Suche":**
    *   `Codebase-Locator` (Findet Pfade) vs. `Explore` (Mappt Struktur).
    *   *Empfehlung:* Merge zu **Explore** (mit Locator-Tools).
3.  **Redundanz-Cluster "Planung":**
    *   `Metis` (Pre-Plan) + `Architect` (Plan) + `Momus` (Review) + `Oracle` (Strategie).
    *   *Problem:* 4 Agenten für eine Aufgabe (Denken). Das erzeugt Latenz und Kosten ("Bureaucracy Bloat").
    *   *Empfehlung:* Reduktion auf **Architect** (Planung) und **Oracle** (Strategie/Review).

### ✅ Stärken (Behalten!)
1.  **Builder:** `Software-Engineer` auf `Claude Sonnet 4.5` ist absolut SOTA. Beste Wahl.
2.  **Audit:** `Audit` auf `Claude Opus 4.5` (Thinking) ist exzellent für Security-Reviews.
3.  **Ideation:** `Brainstormer` auf `Gemini 3 Pro` nutzt die Kreativität der Gemini-Familie optimal.

---

## 3. Modell-Matrix (SOTA 2026 Optimization)

Welches Modell gewinnt in welcher Disziplin?

| Disziplin | Modell-Empfehlung | Grund | WANDA Status |
| :--- | :--- | :--- | :--- |
| **Orchestration** | **Gemini 3 Flash** | Unschlagbarer Kontext (Memory) & Speed. | ❌ (Nutzt GPT-5.2) |
| **Coding** | **Claude Sonnet 4.5** | Höchste Präzision, wenig Halluzination. | ✅ |
| **Reasoning** | **Claude Opus 4.5** | Bestes "Deep Thinking" für Architektur. | ✅ |
| **Strategie** | **GPT-5.2** | Stark in abstrakter Logik & Instruktionen. | ✅ (Oracle) |
| **Vision/UI** | **Gemini 3 Pro** | Multimodalität & kreatives Design. | ✅ |

---

## 4. Redundanz-Check & Optimierung

Wir können das System von 18 auf **14 Agenten** straffen, ohne Funktionalität zu verlieren.

### Empfohlene Konsolidierung
1.  **Explore + Locator** -> **Explore** (Mapper).
2.  **Librarian + Artifact-Searcher** -> **Librarian** (Researcher).
3.  **Metis + Momus** -> **Oracle** (Strategie & Review).
4.  **Commander + Sisyphus** -> **Sisyphus** (Unified Orchestrator). *Der Name "Sisyphus" ist im Plugin hartcodiert, "Commander" ist ein Wrapper. Nutzung des nativen Sisyphus spart Overhead.*

---

## 5. MCP & Plugin Audit

*   **Context7:** SOTA für Docs. Behalten.
*   **n8n-pro:** Essenziell für die Vision. Behalten.
*   **Supabase:** Standard für Backend. Behalten.
*   **Git:** Standard.
*   **Brave Search:** Standard.

*Keine kritischen Lücken im Tool-Stack gefunden.*
