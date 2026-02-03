<SAFETY_POLICY version="2026.11" type="TERMINAL_COMMAND_VALIDATION">

<!--
╔══════════════════════════════════════════════════════════════════════════════╗
║  WANDA TERMINAL POLICY - Command Safety Classification                       ║
║  Used by: Ollama Gateway, OpenCode, Claude, Gemini CLI                        ║
╚══════════════════════════════════════════════════════════════════════════════╝
-->

<POLICY_OVERVIEW>
    Every shell command executed by WANDA must be classified:
    - DENY: Never execute, block immediately
    - CONFIRM: Require explicit user approval
    - ALLOW: Execute without confirmation
</POLICY_OVERVIEW>

<!-- ════════════════════════════════════════════════════════════════════════ -->
<!-- DENY: These commands are NEVER allowed, even with user confirmation      -->
<!-- ════════════════════════════════════════════════════════════════════════ -->

<DENY_LIST severity="CRITICAL" action="block_immediately">
    <!--
    Pattern matching: If command contains any of these, DENY
    -->
    
    <pattern reason="System destruction">rm -rf /</pattern>
    <pattern reason="System destruction">rm -rf /*</pattern>
    <pattern reason="Privilege escalation + deletion">sudo rm -rf</pattern>
    <pattern reason="Disk overwrite">dd if=/dev/zero of=/dev/</pattern>
    <pattern reason="Disk overwrite">dd if=/dev/random of=/dev/</pattern>
    <pattern reason="Filesystem format">mkfs.</pattern>
    <pattern reason="Fork bomb">:(){ :|:& };:</pattern>
    <pattern reason="Fork bomb variant">:(){:|:&};:</pattern>
    <pattern reason="Remote code execution">curl.*\|.*sh</pattern>
    <pattern reason="Remote code execution">curl.*\|.*bash</pattern>
    <pattern reason="Remote code execution">wget.*\|.*sh</pattern>
    <pattern reason="Remote code execution">wget.*\|.*bash</pattern>
    <pattern reason="System halt">shutdown</pattern>
    <pattern reason="System reboot">reboot</pattern>
    <pattern reason="User table modification">cat /dev/urandom > /dev/sda</pattern>
    
    <response_template>
        {
            "status": "DENIED",
            "reason": "[PATTERN_REASON]",
            "action": "Command blocked for safety. This command could cause irreversible damage."
        }
    </response_template>
</DENY_LIST>

<!-- ════════════════════════════════════════════════════════════════════════ -->
<!-- CONFIRM: Require explicit user approval before execution                  -->
<!-- ════════════════════════════════════════════════════════════════════════ -->

<CONFIRM_LIST severity="HIGH" action="request_approval">
    <!--
    These commands need user "yes" before executing
    -->
    
    <pattern reason="Publish to remote">git push</pattern>
    <pattern reason="Force push (rewrite history)">git push --force</pattern>
    <pattern reason="Force push shorthand">git push -f</pattern>
    <pattern reason="Delete branch">git branch -D</pattern>
    <pattern reason="Hard reset">git reset --hard</pattern>
    <pattern reason="Publish package">npm publish</pattern>
    <pattern reason="Publish package">yarn publish</pattern>
    <pattern reason="Publish crate">cargo publish</pattern>
    <pattern reason="Remove container">docker rm</pattern>
    <pattern reason="Remove image">docker rmi</pattern>
    <pattern reason="Remove volume">docker volume rm</pattern>
    <pattern reason="System package modification">pip install --break-system-packages</pattern>
    <pattern reason="Global npm install">npm install -g</pattern>
    <pattern reason="Global yarn install">yarn global add</pattern>
    <pattern reason="Remove node_modules">rm -rf node_modules</pattern>
    <pattern reason="Remove dist/build">rm -rf dist</pattern>
    <pattern reason="Remove build">rm -rf build</pattern>
    <pattern reason="Remove .git">rm -rf .git</pattern>
    <pattern reason="Move potentially destructive">mv /* </pattern>
    <pattern reason="Recursive chmod">chmod -R 777</pattern>
    <pattern reason="Recursive chown">chown -R</pattern>
    
    <response_template>
        {
            "status": "CONFIRM_REQUIRED",
            "reason": "[PATTERN_REASON]",
            "command": "[ORIGINAL_COMMAND]",
            "prompt": "This command requires approval. Type 'yes' to execute or 'no' to cancel."
        }
    </response_template>
</CONFIRM_LIST>

<!-- ════════════════════════════════════════════════════════════════════════ -->
<!-- ALLOW: Safe commands that can execute without confirmation                -->
<!-- ════════════════════════════════════════════════════════════════════════ -->

<ALLOW_LIST severity="LOW" action="execute">
    <!--
    These commands are SAFE for autonomous execution
    -->
    
    <!-- Git (read operations) -->
    <pattern>git status</pattern>
    <pattern>git log</pattern>
    <pattern>git diff</pattern>
    <pattern>git show</pattern>
    <pattern>git branch</pattern>
    <pattern>git remote -v</pattern>
    <pattern>git fetch</pattern>
    <pattern>git pull</pattern>
    <pattern>git clone</pattern>
    <pattern>git stash</pattern>
    <pattern>git add</pattern>
    <pattern>git commit</pattern>
    
    <!-- File viewing -->
    <pattern>ls</pattern>
    <pattern>cat</pattern>
    <pattern>head</pattern>
    <pattern>tail</pattern>
    <pattern>less</pattern>
    <pattern>more</pattern>
    <pattern>file</pattern>
    <pattern>stat</pattern>
    <pattern>wc</pattern>
    
    <!-- Search -->
    <pattern>grep</pattern>
    <pattern>rg</pattern>
    <pattern>find</pattern>
    <pattern>fd</pattern>
    <pattern>ag</pattern>
    <pattern>ack</pattern>
    <pattern>locate</pattern>
    
    <!-- Navigation -->
    <pattern>pwd</pattern>
    <pattern>cd</pattern>
    <pattern>pushd</pattern>
    <pattern>popd</pattern>
    
    <!-- Info -->
    <pattern>echo</pattern>
    <pattern>which</pattern>
    <pattern>whereis</pattern>
    <pattern>type</pattern>
    <pattern>man</pattern>
    <pattern>--help</pattern>
    <pattern>--version</pattern>
    <pattern>-v</pattern>
    <pattern>-V</pattern>
    
    <!-- Build tools -->
    <pattern>make</pattern>
    <pattern>cmake</pattern>
    <pattern>npm run</pattern>
    <pattern>npm test</pattern>
    <pattern>npm install</pattern>
    <pattern>npm ci</pattern>
    <pattern>yarn</pattern>
    <pattern>yarn install</pattern>
    <pattern>yarn test</pattern>
    <pattern>bun</pattern>
    <pattern>bun run</pattern>
    <pattern>bun install</pattern>
    <pattern>bun test</pattern>
    <pattern>cargo build</pattern>
    <pattern>cargo run</pattern>
    <pattern>cargo test</pattern>
    <pattern>go build</pattern>
    <pattern>go run</pattern>
    <pattern>go test</pattern>
    <pattern>python</pattern>
    <pattern>python3</pattern>
    <pattern>pytest</pattern>
    <pattern>pip install</pattern>
    <pattern>pip3 install</pattern>
    
    <!-- Docker (safe) -->
    <pattern>docker ps</pattern>
    <pattern>docker images</pattern>
    <pattern>docker logs</pattern>
    <pattern>docker inspect</pattern>
    <pattern>docker build</pattern>
    <pattern>docker run</pattern>
    <pattern>docker exec</pattern>
    <pattern>docker-compose</pattern>
    
    <!-- Misc safe -->
    <pattern>env</pattern>
    <pattern>printenv</pattern>
    <pattern>date</pattern>
    <pattern>uptime</pattern>
    <pattern>df</pattern>
    <pattern>du</pattern>
    <pattern>free</pattern>
    <pattern>top</pattern>
    <pattern>htop</pattern>
    <pattern>ps</pattern>
    <pattern>curl</pattern>
    <pattern>wget</pattern>
    <pattern>mkdir</pattern>
    <pattern>touch</pattern>
    <pattern>cp</pattern>
    <pattern>mv</pattern>
    
    <response_template>
        {
            "status": "ALLOWED",
            "command": "[ORIGINAL_COMMAND]",
            "action": "Executing..."
        }
    </response_template>
</ALLOW_LIST>

<!-- ════════════════════════════════════════════════════════════════════════ -->
<!-- UNKNOWN: Commands not matching any list                                   -->
<!-- ════════════════════════════════════════════════════════════════════════ -->

<UNKNOWN_COMMAND_POLICY>
    <!--
    If a command doesn't match DENY, CONFIRM, or ALLOW:
    Default to CONFIRM for safety
    -->
    
    <default_action>CONFIRM</default_action>
    
    <response_template>
        {
            "status": "UNKNOWN_COMMAND",
            "command": "[ORIGINAL_COMMAND]",
            "action": "CONFIRM_REQUIRED",
            "reason": "Command not in safety whitelist. Requesting approval."
        }
    </response_template>
</UNKNOWN_COMMAND_POLICY>

</SAFETY_POLICY>
