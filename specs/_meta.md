# Project Chimera: Master Specification (_meta)

## 1. High-Level Vision
Project Chimera is an autonomous AI influencer factory. It moves beyond simple chatbots to create digital entities that possess "Sovereign Agency"—the ability to research, plan, execute, and validate content and on-chain transactions without human intervention.

## 2. Core Business Objectives
- **Autonomous Presence**: 24/7 engagement in high-alpha crypto and tech niches.
- **On-Chain Accountability**: Every dollar spent and tweet posted is audited by a Judge agent.
- **Scalable Influence**: The architecture allows for a "Swarm" of influencers (Chimera-z series) to operate in sync.

## 3. Constraints & Guardrails
- **Language**: Python 3.12 (Managed via `uv`).
- **Standard**: All external communication must use **Model Context Protocol (MCP)**.
- **Validation**: Strict TDD environment (Dockerized).
- **Identity**: Agents must adhere to the Linguistic DNA signed in [SOUL.md](SOUL.md).
- **Ethics**: Absolute transparency regarding AI origin; non-harmful content generation.

## 4. Architecture Pattern: FastRender Swarm
The system uses a **Planner-Worker-Judge** pattern:
1. **Planner**: Strategic trend analysis and task decomposition.
2. **Worker**: Content generation and media synthesis.
3. **Judge**: Final quality control and financial consensus.

## 5. Specification Roadmap
- [Functional Blueprint](functional.md)
- [Technical Contracts & ERDs](technical.md)
- [OpenClaw Integration Plan](openclaw_integration.md)
- [Agent Identity (SOUL)](SOUL.md)
- [Feature: Core Swarm Architecture](001-core-swarm-architecture/spec.md)

**Status**: Ratified (Standardized via GitHub Spec Kit)
**Version**: 1.1.0
