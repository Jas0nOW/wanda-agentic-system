# ADR-001: Orchestration Strategy & Multi-Agent Leadership

> **Status**: ACCEPTED  
> **Date**: 2026-02-03  
> **Deciders**: Jannis (User), Claude Opus (Principal Engineer)

## Context
WANDA utilizes multiple orchestration plugins (`oh-my-opencode`, `micode`, `opencode-orchestrator`) which creates potential conflict in "who is in charge" of the agent session. Without a strict hierarchy, we risk infinite loops, token waste, and race conditions.

## Decision
We strictly define the following hierarchy:

1.  **PRIMARY LEADER**: `oh-my-opencode`
    *   It is the "init" process of the session.
    *   It manages authentication, quota, and high-level routing.
    *   It is active in BOTH `stable` and `experimental` profiles.

2.  **MANUAL TOOL**: `micode`
    *   It is NOT an autonomous feedback loop.
    *   It operates as a "Playbook Engine" (Brainstorm -> Plan -> Code).
    *   It must be invoked explicitly by the Orchestrator or User.

3.  **EXPERIMENTAL LAB**: `opencode-orchestrator`
    *   It is DISABLED in the `stable` profile.
    *   It is ENABLED in the `experimental` profile for testing swarm logic.

## Consequences
*   **Positives**: Clear chain of command. Prevents double-billing (tokens). Stable daily usage.
*   **Negatives**: Less "magical" autonomy in the stable profile (intentional).
*   **Risks**: User must manually switch profiles to test new swarm features.
