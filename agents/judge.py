from schemas.contracts import AgentTask, TaskStatus
import re


class Judge:
    FORBIDDEN_WORDS = ["vibe"]

    def review(self, task: AgentTask) -> AgentTask:
        """Simple judge logic:
        - Reject content containing forbidden words.
        - Approve high-confidence content (>=0.9).
        - Otherwise leave in REVIEW.
        """
        # only operate on content generation tasks
        if task.type == "CONTENT_GEN" or str(task.type) == "CONTENT_GEN":
            text = ""
            if isinstance(task.payload, dict):
                text = task.payload.get("text", "")

            # moderation
            lowered = text.lower()
            for w in self.FORBIDDEN_WORDS:
                if re.search(r"\b" + re.escape(w) + r"\b", lowered):
                    task.status = TaskStatus.FAILED
                    # attach moderation error detail to payload for diagnostics
                    if isinstance(task.payload, dict):
                        task.payload.setdefault("error", f"SOUL violation: forbidden word '{w}'")
                    return task

            # confidence-based approval
            if getattr(task, "confidence_score", 0.0) >= 0.9:
                task.status = TaskStatus.COMPLETED
                return task

        return task
