# Project Chimera: Functional Specification

## 1. User Stories

### 1.1 For the Super-Orchestrator (Human)
*   **As a Super-Orchestrator**, I need to set a high-level goal (e.g., "Grow engagement in the DeFi niche") so the system can decompose it into tasks.
*   **As a Super-Orchestrator**, I need to approve or reject high-value transactions or low-confidence content to ensure brand safety.
*   **As a Super-Orchestrator**, I need to monitor the fleet's financial health and wallet balances via a centralized dashboard.

### 1.2 For the Planner Agent (AI)
*   **As a Planner**, I need to ingest trend data from MCP resources to identify content opportunities.
*   **As a Planner**, I need to generate a Task DAG for Workers based on the current campaign goal and global state.
*   **As a Planner**, I need to re-plan if a Worker fails a task or the market context shifts significantly.

### 1.3 For the Worker Agent (AI)
*   **As a Worker**, I need to pull atomic tasks (e.g., "Draft a tweet") from the Redis queue.
*   **As a Worker**, I need to access the Agent's SOUL.md to ensure voice consistency in content generation.
*   **As a Worker**, I need to call Coinbase AgentKit tools to execute on-chain payments when instructed.

### 1.4 For the Judge Agent (AI)
*   **As a Judge**, I need to validate Worker outputs against safety guardrails and persona constraints.
*   **As a Judge**, I need to assign a confidence score to outputs to determine if human intervention is required.
*   **As a Judge**, I need to implement Optimistic Concurrency Control (OCC) to prevent writing obsolete state to the database.

## 2. Core Functional Requirements (FR)

### 2.1 Perception System
*   **FR-P1:** The system SHALL poll MCP Resources (Twitter mentions, news feeds) every 10 minutes.
*   **FR-P2:** The system SHALL perform semantic filtering to score relevance before triggering tasks.

### 2.2 Reasoning & Swarm
*   **FR-R1:** The system SHALL implement a 3-role swarm: Planner, Worker, Judge.
*   **FR-R2:** The Planner SHALL support dynamic re-planning based on feedback loops.

### 2.3 Creation & Action
*   **FR-A1:** All social posts SHALL be executed via `mcp-server-twitter` tools.
*   **FR-A2:** All financial actions SHALL be executed via `mcp-server-coinbase` (AgentKit).
*   **FR-A3:** The system SHALL enforce character consistency in multimodal content (images/video).

### 2.4 Governance
*   **FR-G1:** The system SHALL escalate any task with a confidence score < 0.70 to the HITL queue.
*   **FR-G2:** The system SHALL enforce a daily spending limit for each agent's wallet.
