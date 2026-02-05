# Chimera Agent Skills Directory

This directory contains the "Skills" (Runtime capabilities) for Project Chimera agents. Unlike MCP Servers (External Bridges), Skills are internal logic packages executed by Workers.

## 1. Skill: `skill_trend_fetcher`
Decomposes raw data into actionable content opportunities.

**Input Contract:**
```json
{
  "source_data": "string (RAW text from MCP Resource)",
  "agent_niche": "string",
  "min_relevance": "float (0.0 - 1.0)"
}
```

**Output Contract:**
```json
{
  "top_trends": [
    { "topic": "string", "signal_strength": "float", "suggested_action": "string" }
  ],
  "timestamp": "ISO-8601"
}
```

## 2. Skill: `skill_content_creator`
Generates high-fidelity drafts aligned with the agent's persona.

**Input Contract:**
```json
{
  "trend_topic": "string",
  "platform": "enum (twitter, instagram)",
  "voice_ref": "path/to/SOUL.md"
}
```

**Output Contract:**
```json
{
  "text_content": "string (max 280 for twitter)",
  "media_prompt": "string (for DALL-E/Midjourney)",
  "confidence_score": "float"
}
```

## 3. Skill: `skill_wallet_manager`
Executes secure financial transactions via Coinbase AgentKit.

**Input Contract:**
```json
{
  "action": "enum (TRANSFER, CHECK_BALANCE)",
  "params": {
    "to_address": "string (optional)",
    "amount": "float (optional)",
    "asset": "string (e.g., 'USDC')"
  }
}
```

**Output Contract:**
```json
{
  "success": "boolean",
  "transaction_hash": "string (if success)",
  "error": "string (if failed)"
}
```
