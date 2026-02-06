# Implementation Plan: FastRender Core Swarm Architecture

**Branch**: `001-core-swarm-architecture` | **Date**: 2024-05-24 | **Spec**: [specs/001-core-swarm-architecture/spec.md](specs/001-core-swarm-architecture/spec.md)
**Input**: Feature specification from `/specs/001-core-swarm-architecture/spec.md`

## Summary
Implement the base swarm orchestration logic allowing the Planner to decompose goals, Workers to generate content/actions, and Judges to validate outputs. This follows the FastRender (Planner-Worker-Judge) pattern to ensure consistency and guardrails.

## Technical Context

**Language/Version**: Python 3.12 (uv)  
**Primary Dependencies**: `mcp`, `pydantic`, `pytest`, `docker`, `redis`  
**Storage**: Redis (Tasks), PostgreSQL (Transactional), Weaviate (Memory)  
**Testing**: `pytest` + `pytest-asyncio` inside Docker  
**Target Platform**: Linux (Docker)  
**Project Type**: Single project
**Performance Goals**: 100% test coverage for swarm state transitions
**Constraints**: MCP SDK compliance, <1s latency for local state updates
**Scale/Scope**: Initial fleet of 3 core agents

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] Swarm-First: All logic assigned to Planner, Worker, or Judge.
- [x] MCP-Native: External tools use MCP.
- [x] True TDD: Tests defined in `tests/` before implementation.
- [x] DNA Integrity: `specs/SOUL.md` referenced in Worker tests.

## Project Structure

### Documentation (this feature)

```text
specs/001-core-swarm-architecture/
├── plan.md              # This file
├── spec.md              # Feature specification
├── data-model.md        # Entity definitions
├── quickstart.md        # Setup guide
└── tasks.md             # Task breakdown
```

### Source Code (repository root)

```text
main.py              # Orchestration entrypoint
schemas/
└── contracts.py     # Pydantic models
agents/
├── planner.py
├── worker.py
└── judge.py
tests/
├── test_planner.py
├── test_worker.py
└── test_judge.py
Dockerfile
Makefile
```

**Structure Decision**: Single Project (Option 1) for rapid prototyping of the core swarm.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
