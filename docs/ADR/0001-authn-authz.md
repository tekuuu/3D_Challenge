# ADR 0001: AuthN / AuthZ Model

Status: Accepted

Context
- Agents require machine-to-machine auth and humans require OAuth2.

Decision
- Use JWT-based service accounts for agent-to-agent communication.
- OAuth2 Authorization Code for human flows.
- Store secrets in Vault; enforce role-based access in code and DB.

Consequences
- Simple token rotation with key IDs is required. Tests must include auth flows.
