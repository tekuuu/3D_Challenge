import pytest
from agents.worker import Worker
from schemas.contracts import AgentTask

def test_worker_soul_compliance():
    worker = Worker()
    task = AgentTask(task_id="123", type="CONTENT_GEN", payload={"topic": "yield farming"}, status="PENDING")
    
    result = worker.execute(task)
    
    # TDD: This will fail because worker doesn't exist/implement execute
    # Linguistic DNA check: Analytical tone, no forbidden words ('Vibe')
    assert "vibe" not in result.payload["text"].lower()
    assert len(result.payload["text"]) > 50

def test_worker_transaction_limit():
    worker = Worker()
    task = AgentTask(task_id="456", type="TRANSACTION", payload={"amount_usd": 1000000}, status="PENDING")
    
    with pytest.raises(PermissionError):
        worker.execute(task)
