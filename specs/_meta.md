# Project Chimera: Meta Specification

## 1. High-Level Vision
Project Chimera aims to build a robust, autonomous influencer network where "Intent is the Source of Truth." We are moving beyond simple content scheduling to create sovereign digital entities (Chimeras) capable of:
*   **Perception:** Sensing market trends through MCP resources.
*   **Reasoning:** Decomposing goals using a Planner-Worker-Judge swarm (FastRender).
*   **Action:** Executing social engagement and on-chain transactions (Coinbase AgentKit).

### 1.1 System Flow Architecture

```mermaid
sequenceDiagram
    participant S as Super-Orchestrator
    participant P as Planner Agent
    participant W as Worker Swarm
    participant J as Judge Agent
    participant M as MCP Sense (Audit)

    S->>P: Set Campaign Goal
    P->>M: Log Intent (log_passage_time)
    loop Task Execution
        P->>W: Assign Atomic Task
        W->>W: Execute via MCP Tools/Skills
        W->>J: Submit for Review
        J->>J: Apply OCC & Safety Checks
        alt Confidence > 0.9
            J->>P: Success (Commit State)
        else Confidence < 0.7
            J->>P: Retry (Refine Prompt)
        else Escalation Required
            J->>S: Manual Intervention Request
        end
    end

## 2. Specification Index
*   **Vision & Prime Directive**: `specs/_meta.md` (Current)
*   **Linguistic DNA**: [specs/SOUL.md](specs/SOUL.md)
*   **User Journeys**: [specs/functional.md](specs/functional.md)
*   **Architecture & Contracts**: [specs/technical.md](specs/technical.md)
*   **Social Connectivity**: [specs/openclaw_integration.md](specs/openclaw_integration.md)
*   **Fleet Governance**: [AGENTS.md](AGENTS.md)
*   **Strategic Tooling**: [research/tooling_strategy.md](research/tooling_strategy.md)

            J->>S: Request HITL Approval
        end
    end
    P->>M: Log Performance (log_outlier)
```

## 2. The Prime Directive
**NEVER generate implementation code without checking specs/ first.** 
The codebase is a reflection of the ratified specifications. Any changes to the system logic must start with an update to the relevant spec file.

## 3. Core Constraints
*   **Standardization:** All external world interactions MUST use the Model Context Protocol (MCP).
*   **Traceability:** Every action must be logged via Tenx Sense MCP for auditability.
*   **Safety:** Human-in-the-Loop (HITL) is mandatory for low-confidence or high-risk actions (e.g., transactions > $50).
*   **Integrity:** SOUL.md is the immutable DNA of the agent persona.

## 4. Key Performance Indicators (KPIs)
*   **Spec Fidelity:** 100% alignment between implementation and `specs/`.
*   **Autonomy Velocity:** Ability to handle 1,000+ concurrent agents with minimal human oversight.
*   **Economic Agency:** Successful execution of non-custodial wallet transactions.

## 5. Stakeholders
*   **Super-Orchestrator:** Human lead setting high-level strategy.
*   **Manager Agents:** AI entities overseeing specialized swarms.
*   **Chimera Workers:** Small, focused agents executing atomic tasks.
