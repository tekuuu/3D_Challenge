# ADR 0002: Migration Strategy

Status: Accepted

Decision
- Use Alembic for migrations. Store `alembic/versions/` in repo.
- CI will run `alembic upgrade head` against the test DB as part of `make test`.

Consequences
- Developers must add migration scripts for schema changes and include rollback instructions in the migration message.
