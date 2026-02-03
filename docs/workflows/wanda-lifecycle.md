# WANDA Development Lifecycle (The 8-Step Protocol)

> **Zweck:** Standardisierter Workflow für jedes Feature und Projekt.
> **Status:** Mandatory (Verbindlich).
> **Ziel:** Maximale Qualität durch erzwungene Planungs- und Test-Phasen.

---

## Phase 1: Brainstorming & Mini-Plan
**Agent:** `Brainstormer` (Category: `visual-engineering` / `artistry`)
**Input:** Vage Idee des Users.
**Aktivität:**
*   Ideen-Ping-Pong.
*   Erste Skizzen (UI oder Architektur).
*   Grobe Machbarkeits-Prüfung.
**Output:** Ein "Concept Draft" (kurzer Text).

---

## Phase 2: Deep Research (The "Huge" Research)
**Agent:** `Librarian` & `Oracle` (Category: `ultrabrain`)
**Input:** Concept Draft.
**Aktivität:**
*   **SOTA-Check:** Gibt es neue Libraries (2025/2026)?
*   **Tech-Stack:** Was passt am besten? (Vergleichs-Analyse).
*   **Security:** Bekannte Angriffsvektoren prüfen.
*   **Architektur:** Pattern-Analyse durch `Pattern-Hunter`.
**Output:** Ein detailliertes "Architecture Spec" & "Research Report".

---

## Phase 3: Initialization & Structure
**Agent:** `Commander` (delegiert, Category: `deep`)
**Input:** Architecture Spec.
**Aktivität:**
*   Projekt/Ordner-Struktur anlegen.
*   Konfigurations-Dateien (Boilerplate) schreiben.
*   **Dokumenten-Sortierung:** Sicherstellen, dass Docs dort liegen, wo sie hingehören.
**Output:** Ein leeres, aber lauffähiges "Skeleton" Projekt.

---

## Phase 4: Implementation (Dev)
**Agent:** `Commander` (delegiert, Category: `deep` oder `visual-engineering`)
**Input:** Skeleton + Spec.
**Aktivität:**
*   Backend-Logik implementieren.
*   Frontend-Components bauen.
*   **Ultrawork:** Parallelisierung von unabhängigen Modulen.
**Output:** Feature-Complete Code (aber vielleicht noch buggy).

---

## Phase 5: Comprehensive Testing
**Agent:** `Quality-Gate` (Category: `ultrabrain`)
**Input:** Code.
**Aktivität:**
*   **Unit Tests:** Logik prüfen.
*   **Integration Tests:** API-Endpunkte prüfen.
*   **E2E Tests:** User-Flows simulieren.
*   **UI/UX Review:** Visuelle Prüfung (durch Multimodal Model).
**Output:** Test-Report & Bug-Liste.

---

## Phase 6: Refactoring & Optimization
**Agent:** `Pattern-Hunter` & `Commander` (Category: `deep`)
**Input:** Bug-Liste + Code.
**Aktivität:**
*   Code Smells beseitigen.
*   Performance-Engpässe finden (Profiling).
*   Einhaltung der `.mindmodel` Patterns erzwingen.
**Output:** Clean Code (Production Ready).

---

## Phase 7: Deployment & Monitoring
**Agent:** `Commander` (Ops Mode)
**Input:** Clean Code.
**Aktivität:**
*   Build-Pipeline ausführen.
*   Docker-Container bauen.
*   Deployment auf Staging/Prod.
*   Monitoring-Hooks setzen.
**Output:** Live-System.

---

## Phase 8: Loop & Documentation
**Agent:** `Librarian` (Category: `writing`)
**Input:** Das fertige System.
**Aktivität:**
*   READMEs updaten.
*   API-Docs generieren.
*   User-Feedback einholen.
*   **Iterative Loop:** Zurück zu Phase 1 für das nächste Feature.
**Output:** Vollständige Dokumentation & Learnings (Memory).
