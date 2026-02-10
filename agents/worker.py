from schemas.contracts import AgentTask, TaskType


class Worker:
    def execute(self, task: AgentTask) -> AgentTask:
        """Simple worker behavior for tests:
        - CONTENT_GEN: produce `text` in payload without forbidden words.
        - TRANSACTION: enforce a transaction limit and raise PermissionError if exceeded.
        """
        # Content generation
        if task.type == "CONTENT_GEN" or str(task.type) == "CONTENT_GEN":
            topic = task.payload.get("topic") or task.payload.get("text") or "general"
            task.payload["text"] = f"Analytical writeup on {topic}."
            return task

        # Transaction handling
        if task.type == "TRANSACTION" or str(task.type) == "TRANSACTION":
            amount = task.payload.get("amount_usd", 0)
            # enforce a conservative limit for the worker
            if amount and amount > 100000:
                raise PermissionError("Transaction exceeds worker limit")
            # simulate submission
            task.payload["tx_hash"] = "0xSIMULATED"
            return task

        return task
