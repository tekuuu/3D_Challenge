# Architectural Logic: Hierarchical State Machine (HSM)
**System Pattern:** FastRender Swarm
**Primary Objective:** Deterministic Autonomous Execution

## 1. Swarm Hierarchy
* **Orchestrator (The Leader):** Maintains global state, handles conflict resolution, and verifies safety guardrails before any on-chain action.
* **Scout-1 (Market Intelligence):** Sub-agent specialized in scraping X (Twitter), tracking BTC/ETH price oracles, and identifying "alpha."
* **Actor-1 (Execution):** Sub-agent specialized in generating social content and executing trades via Coinbase AgentKit.

## 2. Global State Machine (Mermaid)
```mermaid
stateDiagram-v2
    [*] --> IDLE
    IDLE --> SENSING : Interval Trigger
    SENSING --> THINKING : Context Packets Received
    
    state THINKING {
        direction LR
        AnalyzeData --> EvaluateCausalImpact
        EvaluateCausalImpact --> FormulateStrategy
    }
    
    THINKING --> VALIDATING : Strategy Proposed
    
    state VALIDATING {
        direction LR
        CheckGuardrails --> VerifyBalance
        VerifyBalance --> FinalApproval
    }
    
    VALIDATING --> ACTING : Approved
    VALIDATING --> LOGGING : Rejected
    
    ACTING --> LOGGING : Success/Failure
    LOGGING --> IDLE : MCP Sense Synced