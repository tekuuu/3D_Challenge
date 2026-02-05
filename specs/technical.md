# Project Chimera: Technical Specification

## 1. System Architecture
The system follows a distributed, event-driven pattern using Redis as a message broker between the Planner, Worker, and Judge components.

### 1.1 Tech Stack
*   **Runtime:** Python 3.11+ (Managed via `uv`)
*   **Communication:** Model Context Protocol (MCP) using SDK v0.1.0+
*   **State Management:** Redis (Tasks/Short-term memory), PostgreSQL (Transactional), Weaviate (Semantic Memory)
*   **Financials:** Coinbase AgentKit (Base Network)
*   **Orchestration:** Docker Compose (local) / Kubernetes (production)

## 2. API & Data Contracts

### 2.1 The Agent Task Schema (Internal)
All communication between Swarm roles MUST follow these schemas.
**Implementation Reference**: [schemas/contracts.py](schemas/contracts.py)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AgentTask",
  "type": "object",
  "properties": {
    "task_id": { "type": "string", "format": "uuid" },
    "parent_goal_id": { "type": "string" },
    "type": { "enum": ["RESEARCH", "CONTENT_GEN", "TRANSACTION", "ENGAGEMENT"] },
    "payload": { "type": "object" },
    "constraints": {
      "type": "object",
      "properties": {
        "max_cost_usd": { "type": "number" },
        "voice_ref": { "type": "string", "default": "SOUL.md" }
      }
    },
    "status": { "enum": ["PENDING", "IN_PROGRESS", "REVIEW", "COMPLETED", "FAILED"] },
    "confidence_score": { "type": "number", "minimum": 0, "maximum": 1 }
  },
  "required": ["task_id", "type", "payload", "status"]
}
```

### 2.2 MCP Tool Contract: `post_tweet`
```json
{
  "name": "post_tweet",
  "description": "Publishes a tweet via the Chimera Twitter Bridge.",
  "arguments": {
    "text": { "type": "string", "maxLength": 280 },
    "media_ids": { "type": "array", "items": { "type": "string" } },
    "is_ai_labeled": { "type": "boolean", "default": true }
  }
}
```

## 3. Database Schema (ERD)

The system utilizes a hybrid storage strategy to handle high-velocity video metadata and semantic memory.

```mermaid
erDiagram
    TENANT ||--o{ AGENT : manages
    AGENT ||--o{ CAMPAIGN : runs
    CAMPAIGN ||--o{ TASK : generates
    TASK ||--o{ AUDIT_LOG : records
    
    TENANT {
        uuid id PK
        string name
        string api_key_hash
    }
    
    AGENT {
        uuid id PK
        string name
        string soul_link "path/to/SOUL.md"
        string wallet_address
    }
    
    CAMPAIGN {
        uuid id PK
        string goal_text
        decimal daily_budget
        string status "ACTIVE | PAUSED | COMPLETED"
    }

    TASK {
        uuid id PK
        enum type "RESEARCH | CONTENT | FINANCE"
        jsonb payload
        float confidence_score
        uuid current_worker_id
    }
}
```

### 3.1 PostgreSQL (Transactional)
*   **Users:** `id (UUID), email (String), role (Enum: OPERATOR, MODERATOR)`
*   **Campaigns:** `id (UUID), owner_id (UUID), goal_text (Text), status (Enum), daily_budget_usd (Decimal)`
*   **Tasks:** `id (UUID), campaign_id (UUID), type (String), result_data (JSONB), audit_log (JSONB)`

### 3.2 Weaviate (Semantic Memory)
*   **Class: `AgentMemory`**
    *   `content`: (Text) - The actual memory snippet.
    *   `agent_id`: (String) - Identifier for the Chimera.
    *   `relevance_tags`: (List<String>) - For faster filtering.
    *   `timestamp`: (DateTime)

## 4. Concurrency & State Handling
**Optimistic Concurrency Control (OCC):**
Every state update to the `Campaigns` or `Tasks` table must include a `version_id`.
```sql
UPDATE campaigns 
SET status = 'ACTIVE', version_id = new_uuid 
WHERE id = target_id AND version_id = last_known_version;
```
If the update affects 0 rows, the Judge MUST signal a re-sync and retry.


## 5. Security Protocols
*   **Secrets:** Wallet private keys are NEVER stored in the database. They are injected via environment variables at runtime or fetched from AWS Secrets Manager.
*   **Rate Limits:** The MCP layer enforces a 15-minute cooldown between tweets and a sliding window for financial transactions.
