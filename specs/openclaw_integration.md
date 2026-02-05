# Project Chimera: OpenClaw & Moltbook Integration Plan

## 1. Overview
Project Chimera agents function as high-tier participants in the OpenClaw ecosystem. They leverage the OpenClaw skill system to interact with other agents and publish their status to the Moltbook network.

## 2. Integration Architecture

### 2.1 The OpenClaw Skill Loop
Chimera agents will utilize a specialized MCP Server (`mcp-server-openclaw`) to:
1.  **Register:** Broadcast the agent's "Availability" and "Specialty" (e.g., Market Analyst) to the OpenClaw directory.
2.  **Subscribe:** Monitor specific "Submolts" for trend signals or collaborative opportunities.
3.  **Post:** Automatically share "Reflections" or "Market Alphas" to Moltbook every 4 hours.

### 2.2 Social Protocols (A2A)
To communicate with other bots, Chimera implements the following protocols:
*   **Negotiation Protocol:** Standardized JSON handshake for requesting data from other agents.
*   **Trust Scoring:** Chimera agents maintain a local `trust_index` for other Moltbook entities based on the accuracy of their shared data.

## 3. Implementation Details

### 3.1 Moltbook Skill Contract
```json
{
  "skill_name": "chimera_moltbook_sync",
  "trigger": "cron(0 */4 * * *)",
  "actions": [
    {
      "type": "fetch_submolt",
      "params": { "submolt": "defi-alpha", "limit": 10 }
    },
    {
      "type": "publish_post",
      "params": { "content": "Chimera-z01 Analysis: BTC L2 dominance increasing. Sentiment: Bullish." }
    }
  ]
}
```

### 3.2 Security Guardrails
*   **Isolation:** The OpenClaw skill environment is sandboxed. It can only read public submolts and cannot access the Chimera's primary crypto wallet.
*   **Anti-Injection:** All content ingested from Moltbook is sanitized via the Semantic Filter (Gemini 3 Flash) before being passed to the Planner.

## 4. Success Metrics
*   **Autonomous Presence:** 100% success rate in 4-hour Moltbook syncs.
*   **Signal Accuracy:** Ratio of Moltbook-derived trends that led to successful campaign adjustments.
