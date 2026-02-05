<CONTEXT_FILE version="2026.11" type="WANDA_MCP_TOOL_MAPPING">

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  WANDA MCP TOOL MAPPING - Complete Reference                                 ║
║  Maps: Agent → MCP Server → Tools → Use Cases                                ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

<MCP_SERVERS provider="Docker MCP Gateway">
    <!--
    All servers run via: docker mcp gateway run
    Configured in: ~/.gemini/settings.json (mcpServers key)
    Canonical list: docs/SSOT/MCP_AND_PLUGIN_INVENTORY.md
    -->

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- CORE SERVERS (Always Active)                                          -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <server name="filesystem" category="core">
        <purpose>File operations, directory traversal, content management</purpose>
        <tools>
            <tool name="read_file">Read file contents</tool>
            <tool name="write_file">Create/overwrite files</tool>
            <tool name="list_directory">List directory contents</tool>
            <tool name="create_directory">Create directories</tool>
            <tool name="move_file">Move/rename files</tool>
            <tool name="search_files">Search by pattern</tool>
        </tools>
        <used_by>All agents</used_by>
    </server>

    <server name="memory" category="core">
        <purpose>Persistent context and learning storage</purpose>
        <tools>
            <tool name="create_entities">Store new knowledge entities</tool>
            <tool name="create_relations">Link entities together</tool>
            <tool name="read_graph">Retrieve full knowledge graph</tool>
            <tool name="search_nodes">Search stored knowledge</tool>
            <tool name="delete_entities">Remove outdated knowledge</tool>
        </tools>
        <used_by>Ledger-Creator, Artifact-Searcher, all agents for context</used_by>
    </server>

    <server name="supermemory" category="core">
        <purpose>External long-term memory store (optional)</purpose>
        <tools>
            <tool name="search">Search memories</tool>
            <tool name="add">Add memory entries</tool>
            <tool name="list">List stored memories</tool>
        </tools>
        <used_by>System state persistence</used_by>
    </server>

    <server name="docker" category="core">
        <purpose>Container management and MCP gateway</purpose>
        <tools>
            <tool name="list_containers">List running containers</tool>
            <tool name="run_container">Start new container</tool>
            <tool name="stop_container">Stop container</tool>
            <tool name="logs">Read container logs</tool>
            <tool name="mcp-find">Search MCP catalog</tool>
            <tool name="mcp-add">Add MCP server</tool>
            <tool name="mcp-exec">Execute MCP tool</tool>
        </tools>
        <used_by>DevOps tasks, MCP orchestration</used_by>
    </server>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- DEVELOPMENT SERVERS                                                   -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <server name="github" category="development">
        <purpose>Repository operations, issues, PRs</purpose>
        <tools>
            <tool name="create_repository">Create new repo</tool>
            <tool name="get_file_contents">Read repo files</tool>
            <tool name="create_or_update_file">Commit changes</tool>
            <tool name="push_files">Push multiple files</tool>
            <tool name="create_issue">Create issues</tool>
            <tool name="create_pull_request">Create PRs</tool>
            <tool name="search_repositories">Search repos</tool>
        </tools>
        <used_by>Software-Engineer, Architect</used_by>
        <requires_secret>GITHUB_TOKEN</requires_secret>
    </server>

    <server name="github-official" category="development">
        <purpose>Official GitHub MCP (alternative)</purpose>
        <tools>
            <tool name="get_pull_request">Get PR details</tool>
            <tool name="create_pull_request">Create PRs</tool>
        </tools>
        <used_by>Software-Engineer, Architect (optional)</used_by>
        <requires_secret>GITHUB_TOKEN</requires_secret>
    </server>

    <server name="git" category="development">
        <purpose>Local git operations</purpose>
        <tools>
            <tool name="status">Git status</tool>
            <tool name="diff">Show changes</tool>
            <tool name="commit">Commit changes</tool>
            <tool name="log">View history</tool>
            <tool name="branch">Branch management</tool>
        </tools>
        <used_by>Software-Engineer</used_by>
    </server>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- RESEARCH SERVERS                                                      -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <server name="brave" category="research">
        <purpose>Web search with citations</purpose>
        <tools>
            <tool name="web_search">Search the web</tool>
            <tool name="local_search">Search local businesses</tool>
        </tools>
        <used_by>Oracle, Research Layer agents</used_by>
        <requires_secret>BRAVE_API_KEY</requires_secret>
    </server>

    <server name="context7" category="research">
        <purpose>Library/framework documentation lookup</purpose>
        <tools>
            <tool name="resolve-library-id">Find library in catalog</tool>
            <tool name="get-library-docs">Fetch documentation</tool>
        </tools>
        <used_by>Software-Engineer, Librarian</used_by>
    </server>

    <server name="firecrawl" category="research">
        <purpose>Web scraping and content extraction</purpose>
        <tools>
            <tool name="scrape">Scrape single page</tool>
            <tool name="crawl">Crawl website</tool>
            <tool name="map">Generate sitemap</tool>
        </tools>
        <used_by>Oracle, Research tasks</used_by>
        <requires_secret>FIRECRAWL_API_KEY</requires_secret>
    </server>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- AUTOMATION SERVERS                                                    -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <server name="playwright" category="automation">
        <purpose>Browser automation and testing</purpose>
        <tools>
            <tool name="navigate">Open URL</tool>
            <tool name="click">Click element</tool>
            <tool name="fill">Fill form field</tool>
            <tool name="screenshot">Take screenshot</tool>
            <tool name="evaluate">Run JavaScript</tool>
        </tools>
        <used_by>Frontend-UI-UX, Multimodal-Looker</used_by>
    </server>

    <server name="n8n" category="automation">
        <purpose>Workflow automation</purpose>
        <tools>
            <tool name="search_nodes">Search n8n nodes</tool>
            <tool name="get_workflow">Get workflow details</tool>
            <tool name="execute_workflow">Trigger workflow</tool>
        </tools>
        <used_by>Automation tasks</used_by>
    </server>

    <server name="n8n-instance" category="automation">
        <purpose>Instance-specific automation endpoints</purpose>
        <tools>
            <tool name="list_workflows">List workflows</tool>
            <tool name="get_workflow">Get workflow details</tool>
        </tools>
        <used_by>Automation tasks (optional)</used_by>
    </server>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- DATABASE SERVERS                                                      -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <server name="supabase" category="database">
        <purpose>Supabase project management</purpose>
        <tools>
            <tool name="list_projects">List projects</tool>
            <tool name="execute_sql">Run SQL queries</tool>
            <tool name="list_tables">List database tables</tool>
        </tools>
        <used_by>Backend development</used_by>
        <requires_secret>SUPABASE_ACCESS_TOKEN</requires_secret>
    </server>

    <server name="postgres" category="database">
        <purpose>Direct PostgreSQL operations</purpose>
        <tools>
            <tool name="query">Execute SQL</tool>
            <tool name="describe">Describe table</tool>
        </tools>
        <used_by>Backend development</used_by>
    </server>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- DEPLOYMENT SERVERS                                                    -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <server name="vercel" category="deployment">
        <purpose>Vercel deployment management</purpose>
        <tools>
            <tool name="list_projects">List projects</tool>
            <tool name="deploy">Deploy project</tool>
            <tool name="get_deployments">List deployments</tool>
        </tools>
        <used_by>Frontend-UI-UX, DevOps</used_by>
        <requires_secret>VERCEL_API_TOKEN</requires_secret>
    </server>

    <server name="hostinger-mcp-server" category="deployment">
        <purpose>Hostinger platform operations (optional)</purpose>
        <tools>
            <tool name="hosting_listWebsites">List websites</tool>
            <tool name="hosting_listOrders">List hosting orders</tool>
        </tools>
        <used_by>DevOps tasks (optional)</used_by>
        <requires_secret>HOSTINGER_API_TOKEN</requires_secret>
    </server>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- PAYMENT SERVERS                                                       -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <server name="stripe" category="payments">
        <purpose>Stripe payment operations</purpose>
        <tools>
            <tool name="retrieve_balance">Get account balance</tool>
            <tool name="search_stripe_documentation">Search Stripe docs</tool>
            <tool name="update_dispute">Handle disputes</tool>
        </tools>
        <used_by>Payment integration tasks</used_by>
        <requires_secret>STRIPE_API_KEY</requires_secret>
    </server>

    <!-- ════════════════════════════════════════════════════════════════════ -->
    <!-- REASONING SERVERS                                                     -->
    <!-- ════════════════════════════════════════════════════════════════════ -->

    <server name="sequentialthinking" category="reasoning">
        <purpose>Step-by-step problem solving</purpose>
        <tools>
            <tool name="sequentialthinking">Multi-step reasoning with revision support</tool>
        </tools>
        <used_by>Architect, Audit, complex problem solving</used_by>
    </server>

</MCP_SERVERS>

<AGENT_TO_MCP_MAPPING>
    <!--
    Quick reference: Which agent uses which MCP servers
    -->
    
    <agent name="Brainstormer" servers="memory"/>
    <agent name="Sisyphus" servers="memory, docker"/>
    <agent name="Architect" servers="memory, github, sequentialthinking"/>
    <agent name="Software-Engineer" servers="filesystem, github, git, context7"/>
    <agent name="Frontend-UI-UX" servers="filesystem, playwright, vercel"/>
    <agent name="Audit" servers="filesystem, sequentialthinking"/>
    <agent name="Oracle" servers="brave, firecrawl, context7"/>
    <agent name="Writer" servers="filesystem, memory"/>
    <agent name="Librarian" servers="memory, context7"/>
    <agent name="Explore" servers="filesystem, github"/>
    <agent name="Multimodal-Looker" servers="playwright"/>
    <agent name="Codebase-Locator" servers="filesystem" mode="READ-ONLY"/>
    <agent name="Codebase-Analyzer" servers="filesystem" mode="READ-ONLY"/>
    <agent name="Pattern-Finder" servers="filesystem" mode="READ-ONLY"/>
    <agent name="Ledger-Creator" servers="memory"/>
    <agent name="Artifact-Searcher" servers="memory, filesystem"/>
    <agent name="Metis" servers="memory, sequentialthinking"/>
    <agent name="Momus" servers="memory, sequentialthinking"/>
</AGENT_TO_MCP_MAPPING>

<ACTIVATION_GUIDE>
    <!--
    How to add/remove MCP servers
    -->
    
    <add_server>
        1. Use: docker mcp gateway catalog  (list available)
        2. Use: docker mcp gateway run --server=NAME (start server)
        3. Add to ~/.gemini/settings.json mcpServers section
        4. Restart Gemini CLI
    </add_server>
    
    <required_secrets>
        Configure in environment or .env:
        - GITHUB_TOKEN
        - BRAVE_API_KEY
        - FIRECRAWL_API_KEY
        - SUPABASE_ACCESS_TOKEN
        - VERCEL_API_TOKEN
        - STRIPE_API_KEY
        - HOSTINGER_API_TOKEN
    </required_secrets>
</ACTIVATION_GUIDE>

</CONTEXT_FILE>
