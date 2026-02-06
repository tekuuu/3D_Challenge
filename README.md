# Project Chimera: The Autonomous Influencer Factory

**Status**: 🚀 Orchestrator Tier (Day 3 Complete)  
**Vision**: Building a sovereign fleet of AI agents using the FastRender pattern.

---

## 🧠 The Prime Directive
> **NEVER generate implementation code without checking `specs/` first.**  
> Specifications in `specs/` are the absolute source of truth. Every line of code must be traceable to a requirement in the blueprints.

---

## 🏛️ Architecture: FastRender Swarm
Project Chimera utilizes a **Planner-Worker-Judge** swarm pattern to ensure high-fidelity content generation and on-chain accountability.

| Role | Responsibility | Primary Tooling |
| :--- | :--- | :--- |
| **Planner** | Strategic Trend Analysis & Task DAG Decomposition | `mcp-server-twitter`, `specify-cli` |
| **Worker** | Content Synthesis & Action Execution | `skill_content_creator`, `Coinbase AgentKit` |
| **Judge** | Quality Control, LDNA Alignment & Consensus | `specs/SOUL.md`, Audit Logs |

---

## 🛠️ Tech Stack & Governance
- **Runtime**: Python 3.12 (Managed via `uv`)
- **Connectivity**: Model Context Protocol (MCP)
- **Financials**: Coinbase AgentKit (Base Network)
- **Storage**: Hybrid (PostgreSQL + Weaviate + Redis)
- **TDD Engine**: Pytest inside Docker
- **CI/CD**: GitHub Actions + CodeRabbit Governance

---

## 🚦 Operational Commands
This project uses a `Makefile` to standardize critical workflows:

```bash
# Initialize the environment and install dependencies
make setup

# Run the full TDD test suite inside Docker (Required for CI/CD)
make test

# Verify code alignment with Pydantic contracts and specifications
make spec-check
```

---

## 📜 Development Status
- [x] **Day 1: The Strategist** (Research & Architecture Strategy)
- [x] **Day 2: The Architect** (Master Specs, Rule Context & Skills Strategy)
- [x] **Day 3: The Governor** (Docker, Automations, CI/CD & Failing TDD Tests)

---
*Standardized via GitHub Spec Kit. Traceability active via Tenx MCP Sense.*
