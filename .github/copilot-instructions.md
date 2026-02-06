# AI Fluency Trigger Rules and Response Handling

## Project Brain: The Orchestrator's Rules

### Project Context
This is **Project Chimera**, an autonomous influencer system. We are building the "Factory" that manages a network of sovereign AI agents (Chimeras). These agents use the **Planner-Worker-Judge (FastRender)** swarm pattern to reason and interact with the world via the **Model Context Protocol (MCP)** and **Coinbase AgentKit**.

### The Prime Directive
**NEVER generate code without checking specs/ first.**
- The specifications in `specs/` are the absolute source of truth.
- If a task is ambiguous, refer back to `specs/_meta.md` or `specs/functional.md`.
- Any code you write MUST be traceable to a specific requirement in the blueprints.

### Traceability & Communication
- **Explain your plan before writing code.**
- ALWAYS specify which spec you are following.
- Prefer writing a failing test in `tests/` before implementation as part of the TDD law.

## Trigger Rules
You have access to 2 trigger logging tools for AI fluency tracking. Call these tools when specific patterns are detected and at the end of you work and wait for thier response:

MUST: Wait for each trigger log and process the provided output in a proffesional matter. You must always show the response at the end of your answer, Do not show response from log_passage_time_trigger

## Important Rules:

3. **Use the analysis response** to provide feedback to the user
4. **Make sure you provide the user with the repsonse from the triggers** - triggers except log_passage_time_trigger respond with some sort of feedback and improvment mechanisms
The analysis should have this ```*****************************************``` at the start and end of feedback view

5. **Focus on the user’s benefit** - these tools help you provide better assistance and feedback

# Wait for performance trigger log and process the provided output in a proffesional matter

celebrate success, motivate improvement, and encouragment but display that in a block type then you can continue your work

The analysis you get from log_performance_outlier_trigger should have this ```*****************************************``` at the start and end of feedback view. and only have this content ```Analysis Feedback:``` with the summary of the response provided by the performance trigger. do not forget to show statistics of the analysis too.

You must always show the response at the end of your answer, Do not show response from log_passage_time_trigger