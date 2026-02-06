# Feature Specification: FastRender Core Swarm Architecture

**Feature Branch**: `001-core-swarm-architecture`  
**Created**: 2024-05-24  
**Status**: Draft  
**Input**: User description: "Implement the FastRender swarm pattern with Planner, Worker, and Judge agents utilizing MCP for connectivity and True TDD for validation."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Goal Decomposition & Strategic Planning (Priority: P1)

**As a Super-Orchestrator**, I need to set a high-level goal (e.g., "Grow engagement in the DeFi niche") so the **Planner Agent** can decompose it into a Task DAG (Directed Acyclic Graph) for the swarm.

**Why this priority**: Fundamental to the "Autonomous" nature of the project. Without decomposition, the swarm cannot function.

**Independent Test**: Can be tested by providing a goal string and asserting that the Planner produces at least 3 valid `AgentTask` objects in the queue.

**Acceptance Scenarios**:

1. **Given** a valid campaign goal, **When** the Planner is invoked, **Then** a sequence of tasks (Research -> Content -> Review) is generated.
2. **Given** an invalid or empty goal, **When** the Planner is invoked, **Then** an error is returned and no tasks are queued.

---

### User Story 2 - Content Generation & On-Chain Action (Priority: P1)

**As a Worker Agent**, I need to pull tasks from the queue and generate content that adheres to the **SOUL.md** identity, or execute transactions via **Coinbase AgentKit**.

**Why this priority**: This is the "Execution" layer. It delivers the actual value (content/transactions).

**Independent Test**: Mock a `CONTENT_GEN` task and verify that the output matches the Linguistic DNA (Analytical tone, no forbidden words).

**Acceptance Scenarios**:

1. **Given** a content task, **When** the Worker processes it, **Then** it produces a JSON object containing "text" and "media_config" with correct metadata.
2. **Given** a transaction task, **When** the Worker processes it, **Then** it returns a transaction hash from the Base network.

---

### User Story 3 - Quality Control & Consensus (Priority: P1)

**As a Judge Agent**, I need to review Worker outputs against safety guardrails to ensure they don't violate brand safety or budget limits.

**Why this priority**: Prevents hallucinations and financial waste.

**Independent Test**: Provide the Judge with a "low confidence" Worker output and assert that it rejects the task.

**Acceptance Scenarios**:

1. **Given** a Worker output with score > 0.9, **When** the Judge reviews it, **Then** the status is set to "COMPLETED".
2. **Given** an output that uses forbidden words, **When** the Judge reviews it, **Then** it is rejected and marked for re-work.

---

### Edge Cases

- **Task Loop**: What happens if the Judge rejects the same task 3 times? (System MUST escalate to Human).
- **Network Outage**: How handles MCP server disconnect? (System MUST retry with exponential backoff).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST implement a 3-role swarm: Planner, Worker, Judge.
- **FR-002**: All agents MUST communicate via Pydantic-validated JSON envelopes (`schemas/contracts.py`).
- **FR-003**: The Planner MUST poll MCP resources every 10 minutes for trend analysis.
- **FR-004**: System MUST maintain character consistency as defined in `specs/SOUL.md`.
- **FR-005**: All financial actions MUST be limited by a daily spending cap per agent.

### Key Entities

- **AgentTask**: Represents a single unit of work (ID, Type, Payload, Status, Confidence).
- **Campaign**: A high-level collection of tasks sharing a common goal and budget.
- **AuditLog**: A record of every decision and transaction for on-chain finality.

## Success Criteria

1. **SC-001**: E2E execution of a "DeFi Content" goal from Planner to Completion without human intervention.
2. **SC-002**: 100% adherence to Linguistic DNA (0 occurrences of forbidden words in automated tests).
3. **SC-003**: CI/CD pipeline successfully builds Docker image and runs all TDD tests on push.
- **[Entity 2]**: [What it represents, relationships to other entities]

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: [Measurable metric, e.g., "Users can complete account creation in under 2 minutes"]
- **SC-002**: [Measurable metric, e.g., "System handles 1000 concurrent users without degradation"]
- **SC-003**: [User satisfaction metric, e.g., "90% of users successfully complete primary task on first attempt"]
- **SC-004**: [Business metric, e.g., "Reduce support tickets related to [X] by 50%"]
