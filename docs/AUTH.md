# AuthN / AuthZ, Secrets & Rate Limiting

Auth model (overview):
- Service accounts for internal agent-to-agent communication using JWTs signed with a project key pair.
- External user flows use OAuth2 (authorization code) when human accounts are required.

Secrets management:
- Recommended: store secrets in HashiCorp Vault or AWS Secrets Manager.
- For local/dev, use environment variables via a `.env` file (keep out of VCS) and use `python-dotenv` in dev only.
- Rotation: rotate service keys quarterly; maintain a migration path for key roll-over using key IDs and dual-signing grace period.

AuthZ / RBAC:
- Roles: `super_orchestrator`, `planner`, `worker`, `judge`, `readonly`.
- Enforce RBAC in application code and via DB roles for sensitive operations (see `docs/DB_SCHEMA.md`).

Rate limiting & containment:
- Per-endpoint rate limits configured at API gateway / sidecar (Envoy + global rate limit). Default example: 60 requests/min per agent for control endpoints, adjustable.
- Use token bucket with burst allowance for short spikes.

Content moderation & escalation pipeline:
- Judge validates content against `SOUL.md` and safety rules.
- If content is rejected 3x, emit an escalation event to `audit_logs` and alert `super_orchestrator` via configured channel (email/Slack/MCP message).

Secrets rotation & access:
- Use Vault policies to scope secrets per environment and per-role.
- CI stores only short-lived tokens or uses `vault login` step to fetch secrets during workflow run.
