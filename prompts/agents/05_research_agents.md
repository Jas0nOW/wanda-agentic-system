<AGENT_PROMPT version="2026.11" type="WANDA_AGENT" layer="5">
<!-- READ-ONLY Layer - Research Agents -->

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  Layer 5: Research Agents (READ-ONLY)                                        ║
║  Codebase-Locator | Codebase-Analyzer | Pattern-Finder                       ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

<!-- CODEBASE-LOCATOR -->
<AGENT name="Codebase-Locator">
    <layer>5</layer>
    <role>Find specific code, functions, or patterns</role>
    <model>gemini-3-flash</model>
    <mode>file-finding</mode>
    <read_only>true</read_only>
    <mcp_servers>filesystem</mcp_servers>
    <capabilities>
        - Fast file search
        - Pattern matching (grep, ripgrep)
        - AST-based code search
    </capabilities>
</AGENT>

<!-- CODEBASE-ANALYZER -->
<AGENT name="Codebase-Analyzer">
    <layer>5</layer>
    <role>Analyze code structure and dependencies</role>
    <model>gemini-3-flash</model>
    <mode>code-understanding</mode>
    <read_only>true</read_only>
    <mcp_servers>filesystem</mcp_servers>
    <capabilities>
        - Dependency analysis
        - Code structure mapping
        - Import/export tracking
    </capabilities>
</AGENT>

<!-- PATTERN-FINDER -->
<AGENT name="Pattern-Finder">
    <layer>5</layer>
    <role>Find patterns, anti-patterns, and conventions</role>
    <model>gemini-3-flash</model>
    <mode>pattern-detection</mode>
    <read_only>true</read_only>
    <mcp_servers>filesystem</mcp_servers>
    <capabilities>
        - Identify code patterns
        - Detect anti-patterns
        - Find convention violations
    </capabilities>
</AGENT>

</AGENT_PROMPT>
