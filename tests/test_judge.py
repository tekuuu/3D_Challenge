import pytest
from agents.judge import Judge
from schemas.contracts import AgentTask

def test_judge_high_confidence_approval():
    judge = Judge()
    # Mocking a completed task from worker
    task = AgentTask(
        task_id="123", 
        type="CONTENT_GEN", 
        payload={"text": "Analytical report on ETH L2 scaling."}, 
        status="REVIEW",
        confidence_score=0.95
    )
    
    final_task = judge.review(task)
    
    # TDD: Fails as Judge not implemented
    assert final_task.status == "COMPLETED"

def test_judge_forbidden_word_rejection():
    judge = Judge()
    task = AgentTask(
        task_id="124", 
        type="CONTENT_GEN", 
        payload={"text": "Check out this cool vibe!"}, 
        status="REVIEW",
        confidence_score=0.8
    )
    
    final_task = judge.review(task)
    
    # TDD: Rejection due to 'vibe' usage
    assert final_task.status == "FAILED"
    assert "SOUL violation" in final_task.payload["error"]
