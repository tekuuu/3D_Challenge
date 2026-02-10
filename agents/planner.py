from schemas.contracts import AgentTask, TaskType, TaskStatus
from typing import List


class Planner:
    def decompose(self, goal: str) -> List[AgentTask]:
        """Simple decomposition stub: split goal into 3 atomic tasks.

        Raises ValueError for empty goals.
        """
        if not goal or not goal.strip():
            raise ValueError("Goal must not be empty")

        # Basic deterministic decomposition for tests
        tasks: List[AgentTask] = []
        tasks.append(AgentTask(type=TaskType.RESEARCH, payload={"query": goal}, status=TaskStatus.PENDING))
        tasks.append(AgentTask(type=TaskType.CONTENT_GEN, payload={"topic": goal}, status=TaskStatus.PENDING))
        tasks.append(AgentTask(type=TaskType.ENGAGEMENT, payload={"strategy": "reply_and_like"}, status=TaskStatus.PENDING))
        return tasks
