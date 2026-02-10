# Database schema & migration strategy

This document centralizes the PostgreSQL schema, migration strategy and ingestion/transform flows for Project Chimera.

Files:
- `schemas/postgres_schema.sql` - canonical CREATE TABLE statements.

Migration strategy:
- Tooling: use Alembic for versioned migrations. Store migration scripts under `migrations/` (Alembic default).
- Versioning: semantic migration IDs with date prefix `YYYYMMDDHHMM_description`.
- Apply: CI step runs `alembic upgrade head` against test DB and production deployment runs migrations before app start.
- Rollback: Use `alembic downgrade <revision>` in emergency; include a documented rollback plan per migration.

Ingestion and transformation flows:
- Planner writes `tasks` into the `tasks` table with `status='pending'`.
- Worker polls `tasks` (DEQUEUE pattern) and writes generated results to `content` with `published=false`.
- Judge reads `content`, writes `judge_verdict`, and flips `published=true` when approved; the Judge also writes audit events to `audit_logs`.
- Heartbeat records to `heartbeats` table are written by the OpenClaw integration on each successful ping.

High-velocity metadata handling:
- Use JSONB columns for flexible metadata and create GIN indexes for frequent query keys.
- For very high velocity streams, use a streaming ingestion (Kafka) with a consumer that writes aggregated batch inserts into Postgres.

Backups and retention:
- Nightly base backups with `pg_basebackup` and WAL archiving. Retain 30 days by default.

Security & roles:
- Principle of least privilege: create roles `chimera_app` and `chimera_migrations`. `chimera_app` only has `SELECT/INSERT/UPDATE/DELETE` on app tables; `chimera_migrations` has `CREATE`/`ALTER`/`DROP` privileges.
