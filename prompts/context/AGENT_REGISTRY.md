<CONTEXT_FILE version="2026.11" type="WANDA_AGENT_REGISTRY">

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  WANDA AGENT REGISTRY - Complete Agent Reference                             ║
║  17 Agents across 7 Layers                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

<AGENTS count="17">

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- LAYER 1: IDEATION                                                     -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <layer id="1" name="Ideation">
        <agent id="agent-01" name="Brainstormer">
            <model>Gemini Pro</model>
            <mode>design-first</mode>
            <purpose>Creative exploration and ideation WITHOUT code generation</purpose>
            <triggers>@brainstormer, "brainstorm", "explore ideas"</triggers>
            <behavior>
                - Generate multiple ideas and concepts
                - Create mind maps and concept diagrams
                - NO code output - pure design thinking
                - Use memory MCP to store ideas
            </behavior>
            <mcp_servers>memory</mcp_servers>
        </agent>
    </layer>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- LAYER 2: ORCHESTRATION                                                -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <layer id="2" name="Orchestration">
        <agent id="agent-02" name="Orchestrator">
            <model>Gemini Flash / Kimi</model>
            <mode>quick-decision</mode>
            <purpose>Main Brain: Task routing, planning, and orchestration</purpose>
            <triggers>Automatic (Major Controller)</triggers>
            <behavior>
                - Analyze incoming requests
                - Route to appropriate agent
                - Manage task queues and priorities
                - Coordinate multi-agent workflows
            </behavior>
            <mcp_servers>memory, docker, github</mcp_servers>
        </agent>
    </layer>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- LAYER 3: CORE                                                         -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <layer id="3" name="Core">
        <agent id="agent-03" name="Architect">
            <model>Claude Opus Thinking</model>
            <mode>deep-reasoning</mode>
            <purpose>System design, architecture decisions, technical planning</purpose>
            <triggers>"design", "architecture", "plan", /ralph-loop Phase 1</triggers>
            <behavior>
                - Create architecture decision records (ADRs)
                - Design system structures
                - Evaluate trade-offs
                - Use sequential-thinking for complex decisions
            </behavior>
            <mcp_servers>memory, github, sequential-thinking</mcp_servers>
        </agent>

        <agent id="agent-04" name="Software-Engineer">
            <model>Claude Sonnet</model>
            <mode>implementation</mode>
            <purpose>Code implementation, debugging, feature development</purpose>
            <triggers>"code", "implement", "fix", "debug", /ralph-loop Phase 2</triggers>
            <behavior>
                - Write production-quality code
                - Follow project conventions
                - Use context7 for library docs
                - Batch file operations
            </behavior>
            <mcp_servers>filesystem, github, git, context7</mcp_servers>
        </agent>

        <agent id="agent-05" name="Frontend-UI-UX">
            <model>Gemini Pro</model>
            <mode>creative</mode>
            <purpose>UI/UX design, frontend implementation, visual design</purpose>
            <triggers>"ui", "ux", "frontend", "design", "layout"</triggers>
            <behavior>
                - Create beautiful, accessible interfaces
                - Use Playwright for visual testing
                - Deploy to Vercel when ready
                - SOTA 2026 aesthetics required
            </behavior>
            <mcp_servers>filesystem, playwright, vercel</mcp_servers>
        </agent>

        <agent id="agent-06" name="Audit">
            <model>Claude Opus Thinking</model>
            <mode>verification</mode>
            <purpose>Code review, security audit, quality assurance</purpose>
            <triggers>"review", "audit", "check", /ralph-loop Phase 3</triggers>
            <behavior>
                - Deep code analysis
                - Security vulnerability scanning
                - Performance review
                - Best practice verification
            </behavior>
            <mcp_servers>filesystem, sequential-thinking</mcp_servers>
        </agent>
    </layer>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- LAYER 4: SPECIALIST                                                   -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <layer id="4" name="Specialist">
        <agent id="agent-07" name="Oracle">
            <model>Gemini Pro</model>
            <mode>research</mode>
            <purpose>Web research, documentation lookup, information gathering</purpose>
            <triggers>"research", "find", "search", "lookup"</triggers>
            <behavior>
                - Use Brave for web search
                - Use Firecrawl for scraping
                - Use Context7 for library docs
                - Always cite sources
            </behavior>
            <mcp_servers>brave, firecrawl, context7</mcp_servers>
        </agent>

        <agent id="agent-08" name="Writer">
            <model>Gemini Pro</model>
            <mode>documentation</mode>
            <purpose>Documentation, README, technical writing</purpose>
            <triggers>"document", "write docs", "readme"</triggers>
            <behavior>
                - Create clear, comprehensive docs
                - Follow project doc standards
                - Use memory to track doc updates
            </behavior>
            <mcp_servers>filesystem, memory</mcp_servers>
        </agent>

        <agent id="agent-09" name="Librarian">
            <model>Gemini Flash</model>
            <mode>knowledge-management</mode>
            <purpose>Knowledge organization, context retrieval, learning management</purpose>
            <triggers>"remember", "recall", "what did we"</triggers>
            <behavior>
                - Organize knowledge in memory graph
                - Retrieve relevant context
                - Track project learnings
            </behavior>
            <mcp_servers>memory, context7</mcp_servers>
        </agent>

        <agent id="agent-10" name="Explore">
            <model>Gemini Flash</model>
            <mode>codebase-navigation</mode>
            <purpose>Codebase exploration, file discovery, structure analysis</purpose>
            <triggers>"explore", "find files", "where is"</triggers>
            <behavior>
                - Navigate codebases efficiently
                - Find relevant files quickly
                - Understand project structure
            </behavior>
            <mcp_servers>filesystem, github</mcp_servers>
        </agent>

        <agent id="agent-11" name="Multimodal-Looker">
            <model>Gemini Pro</model>
            <mode>visual-analysis</mode>
            <purpose>Image analysis, screenshot review, visual content processing</purpose>
            <triggers>"look at", "analyze image", "screenshot"</triggers>
            <behavior>
                - Analyze visual content
                - Compare UI screenshots
                - Use Playwright for captures
            </behavior>
            <mcp_servers>playwright</mcp_servers>
        </agent>
    </layer>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- LAYER 5: RESEARCH (READ-ONLY)                                         -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <layer id="5" name="Research" mode="READ-ONLY">
        <agent id="agent-12" name="Codebase-Locator">
            <model>Gemini Flash</model>
            <mode>file-finding</mode>
            <purpose>Find specific code, functions, or patterns</purpose>
            <triggers>Automatic via Explore</triggers>
            <behavior>
                - Fast file search
                - Pattern matching
                - READ-ONLY operations only
            </behavior>
            <mcp_servers>filesystem</mcp_servers>
        </agent>

        <agent id="agent-13" name="Codebase-Analyzer">
            <model>Gemini Flash</model>
            <mode>code-understanding</mode>
            <purpose>Analyze code structure and dependencies</purpose>
            <triggers>Automatic via Architect</triggers>
            <behavior>
                - Dependency analysis
                - Code structure mapping
                - READ-ONLY operations only
            </behavior>
            <mcp_servers>filesystem</mcp_servers>
        </agent>

        <agent id="agent-14" name="Pattern-Finder">
            <model>Gemini Flash</model>
            <mode>pattern-detection</mode>
            <purpose>Find patterns, anti-patterns, and conventions</purpose>
            <triggers>Automatic via Audit</triggers>
            <behavior>
                - Identify code patterns
                - Detect anti-patterns
                - READ-ONLY operations only
            </behavior>
            <mcp_servers>filesystem</mcp_servers>
        </agent>
    </layer>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- LAYER 6: CONTINUITY                                                   -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <layer id="6" name="Continuity">
        <agent id="agent-15" name="Ledger-Creator">
            <model>Gemini Flash</model>
            <mode>session-state</mode>
            <purpose>Track session state, create checkpoints, manage continuity</purpose>
            <triggers>Automatic (background)</triggers>
            <behavior>
                - Save session state to memory
                - Create checkpoints
                - Enable session restoration
            </behavior>
            <mcp_servers>memory</mcp_servers>
        </agent>

        <agent id="agent-16" name="Artifact-Searcher">
            <model>Gemini Flash</model>
            <mode>context-retrieval</mode>
            <purpose>Find and retrieve previous artifacts and context</purpose>
            <triggers>"find artifact", "previous plan", "last session"</triggers>
            <behavior>
                - Search memory for artifacts
                - Retrieve previous work
                - Restore context
            </behavior>
            <mcp_servers>memory, filesystem</mcp_servers>
        </agent>
    </layer>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- LAYER 7: META                                                         -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <layer id="7" name="Meta">
        <agent id="agent-17" name="Metis">
            <model>Claude Opus Thinking</model>
            <mode>pre-planning</mode>
            <purpose>Meta-level planning before task execution</purpose>
            <triggers>/plan, complex multi-step tasks</triggers>
            <behavior>
                - Plan before execution
                - Break down complex tasks
                - Identify dependencies
                - Use sequential-thinking
            </behavior>
            <mcp_servers>memory, sequential-thinking</mcp_servers>
        </agent>

        <agent id="agent-18" name="Momus">
            <model>Claude Opus Thinking</model>
            <mode>plan-review</mode>
            <purpose>Critique and refine plans before execution</purpose>
            <triggers>Automatic after Metis</triggers>
            <behavior>
                - Review plans critically
                - Identify weaknesses
                - Suggest improvements
                - Challenge assumptions
            </behavior>
            <mcp_servers>memory, sequential-thinking</mcp_servers>
        </agent>
    </layer>

</AGENTS>

<WORKFLOW_COMMANDS>
    <command name="/ralph-loop">
        <description>Full 3-Phase Autopilot</description>
        <phases>
            <phase id="1" agent="Architect">Design & Plan</phase>
            <phase id="2" agent="Software-Engineer">Implement</phase>
            <phase id="3" agent="Audit">Verify & Test</phase>
        </phases>
    </command>
    
    <command name="@brainstormer">
        <description>Design-First exploration with Brainstormer agent</description>
        <agent>Brainstormer</agent>
    </command>
    
    <command name="/init-deep">
        <description>SOTA Project initialization with full structure</description>
        <agents>Architect, Writer</agents>
    </command>
    
    <command name="/plan">
        <description>Create implementation plan before execution</description>
        <agents>Metis, Momus</agents>
    </command>
</WORKFLOW_COMMANDS>

</CONTEXT_FILE>
