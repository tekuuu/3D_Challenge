# Tasks: Core Swarm Architecture

## Phase 1: Foundation & TDD
- [ ] **Task 1**: Create failing tests for Planner goal decomposition. (`tests/test_planner.py`)
- [ ] **Task 2**: Create failing tests for Worker SOUL-compliance. (`tests/test_worker.py`)
- [ ] **Task 3**: Create failing tests for Judge consensus logic. (`tests/test_judge.py`)

## Phase 2: Implementation
- [ ] **Task 4**: Implement `agents/planner.py` with Pydantic validation.
- [ ] **Task 5**: Implement `agents/worker.py` with MCP integration.
- [ ] **Task 6**: Implement `agents/judge.py` with OCC and confidence scoring.

## Phase 3: Infrastructure
- [ ] **Task 7**: Update `Makefile` to include `make test-full`.
- [ ] **Task 8**: Verify Dockerized runs of the swarm.
