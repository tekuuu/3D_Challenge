-- Core PostgreSQL schema for Project Chimera
-- Filename: schemas/postgres_schema.sql

-- Agents table: identity and metadata
CREATE TABLE IF NOT EXISTS agents (
    agent_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    public_key TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Tasks table: Planner -> Worker tasks
CREATE TABLE IF NOT EXISTS tasks (
    id BIGSERIAL PRIMARY KEY,
    task_type TEXT NOT NULL,
    payload JSONB NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    assigned_to TEXT REFERENCES agents(agent_id),
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Content table: Worker outputs and Judge decisions
CREATE TABLE IF NOT EXISTS content (
    id BIGSERIAL PRIMARY KEY,
    author_agent TEXT REFERENCES agents(agent_id),
    body TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    judge_verdict JSONB,
    published BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Heartbeats: OpenClaw & internal availability
CREATE TABLE IF NOT EXISTS heartbeats (
    id BIGSERIAL PRIMARY KEY,
    agent_id TEXT REFERENCES agents(agent_id),
    endpoint TEXT,
    status TEXT,
    last_seen TIMESTAMPTZ,
    payload JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Audit logs (Judge + system events)
CREATE TABLE IF NOT EXISTS audit_logs (
    id BIGSERIAL PRIMARY KEY,
    source TEXT,
    level TEXT,
    event JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
CREATE INDEX IF NOT EXISTS idx_heartbeats_agent ON heartbeats(agent_id);
