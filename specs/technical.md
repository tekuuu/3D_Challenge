# Project Chimera: Technical Specification

## 1. System ERD (Database Schema)

The system utilizes PostgreSQL for transactional state and Weaviate for semantic memory.

```mermaid
erDiagram
    TENANT ||--o{ AGENT : manages
    AGENT ||--o{ CAMPAIGN : runs
    CAMPAIGN ||--o{ TASK : generates
    TASK ||--o{ AUDIT_LOG : records
    
    AGENT {
        uuid id PK
        string name
        string soul_link "path/to/SOUL.md"
        string wallet_address
        decimal daily_budget
    }
    
    TASK {
        uuid id PK
        enum type "RESEARCH | CONTENT | FINANCE"
        jsonb payload
        float confidence_score
        uuid current_worker_id
        string status "PENDING | IN_PROGRESS | REVIEW | COMPLETED | FAILED"
    }

    AUDIT_LOG {
        uuid id PK
        uuid task_id FK
        string action
        timestamp created_at
        jsonb metadata
    }
```

## 2. API & Data Contracts

### 2.1 AgentTask Schema
All agents must adhere to the validated Pydantic model in `schemas/contracts.py`.

```json
{
  "title": "AgentTask",
  "type": "object",
  "properties": {
    "task_id": { "type": "string", "format": "uuid" },
    "type": { "enum": ["RESEARCH", "CONTENT_GEN", "TRANSACTION", "ENGAGEMENT"] },
    "payload": { "type": "object" },
    "status": { "type": "string" },
    "confidence_score": { "type": "number" }
  },
  "required": ["task_id", "type", "payload", "status"]
}
```

### 2.2 MCP Tool Contract: `get_market_trend`
```json
{
  "name": "get_market_trend",
  "description": "Fetches top 10 trends for a specified niche via MCP.",
  "arguments": {
    "niche": { "type": "string", "enum": ["DEFI", "NFT", "AI", "MACRO"] },
    "limit": { "type": "integer", "default": 5 }
  }
}
```

## 3. Tech Stack
- **Runtime**: Python 3.12 (uv)
- **Messaging**: Redis (Pub/Sub)
- **DB**: PostgreSQL + Weaviate
- **Orchestration**: Docker + Kubernetes
- **Intelligence**: Gemini 3 Flash (via MCP)
