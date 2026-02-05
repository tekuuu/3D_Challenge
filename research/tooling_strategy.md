# Project Chimera: Tooling & Skills Strategy

## 1. Developer Tools (MCP)
To maximize development velocity and maintain spec-code alignment, we utilize the following Model Context Protocol (MCP) servers:

*   **git-mcp:** Provides advanced version control capabilities directly to the AI agent, ensuring clean commit messages and branch management.
*   **filesystem-mcp:** Enables precise multi-file editing and directory structure management.
*   **memory-mcp:** Used locally to store development context and previous design decisions during the 3-day build.
*   **tenx-mcp-sense:** Our "Black Box" flight recorder. Mandatory for logging all strategic "thinking" and performance outliers.

## 2. Agent Skills (Runtime)
Skills are encapsulated, reusable functional packages that a Chimera Agent executes during its operational lifecycle.

### 2.1 Skill Architecture
Each skill is located in the `skills/` directory and contains:
*   `README.md`: Defining the I/O contract.
*   `skill.py`: The executable logic (using Pydantic for validation).
*   `test_skill.py`: TDD implementation confirming the interface.

### 2.2 Core Skill Set
1.  **skill_trend_fetcher:** Ingests data from MCP News/Twitter resources and produces a relevance-scored JSON report.
2.  **skill_content_creator:** Generates multimodal asset drafts based on the agent's SOUL.md.
3.  **skill_wallet_manager:** Interfaces with Coinbase AgentKit to perform secure on-chain transactions.

## 3. Deployment Strategy
*   **Dev Mode:** Agents run within the local VS Code environment connected to dev MCP servers.
*   **Prod Mode:** Agents are containerized (Docker) and connect to production-grade MCP endpoints via SSE (Server-Sent Events).
