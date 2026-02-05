Gemini 3 Pro braucht einen "Run Brief"

Für Gemini 3 Pro ist „mit XML“ meistens besser — aber nur, wenn du es richtig einsetzt. ✅
Google empfiehlt explizit, Prompts zu strukturieren (z. B. mit XML-Tags oder klaren Prefixes), damit das Modell Abschnitte sauber trennt und Anforderungen zuverlässiger befolgt.

Empfehlung (bestes Ergebnis in der Praxis) 🧠

A) Agent/System Prompt = XML (stabil, deterministisch)

XML ist perfekt für: Identity, BANNED/REQUIRED, Output-Format, Guardrails, Tooling

Vorteil: weniger “Instruction bleed”, bessere Wiederholbarkeit bei langen Specs.

B) Run/Projekt-Brief = kurz & clean (optional XML, aber minimal)

Der Brief sollte nicht wieder 200 Regeln enthalten.

Entweder ohne XML (plain text), oder als ein Block im XML (<RUN_BRIEF>…</RUN_BRIEF>), aber ohne Tag-Nesting-Hölle.

Warum nicht immer XML?

XML hilft beim Trennen von Blöcken, aber zu viel XML-Overhead kann Kreativität einschränken und führt oft zu “Schema-Abarbeitung”. Deshalb: XML für Regeln/Output, kurzer Brief für Content. (Das ist Best-Practice-Reasoning, die offiziellen Docs betonen vor allem: klar, spezifisch, strukturiert.)

RUN_BRIEF
PROJECT: Jannis Portfolio “Sovereign Terminal”
BASELINE: https://portfolio.lazytechlab.de/
MODE: IMMERSIVE
INTENSITY: Balanced
GOAL: looks senior + personal; Case Files; one signature effect; fast + accessible
MUST KEEP: WANDA, n8n automation, light-saas, sovereignty
DELIVERABLE: spec + code
WORKDIR: /home/jannis/Schreibtisch/Work-OS/10_LTL_Core/11_Products/11.03_Portfolio
