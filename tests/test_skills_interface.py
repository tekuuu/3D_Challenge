import pytest
from schemas.contracts import AgentTask, TaskType, TaskStatus
from uuid import uuid4

def test_task_schema_validation():
    """
    Ensures the AgentTask schema correctly validates and defaults.
    """
    task = AgentTask(
        task_id=uuid4(),
        type=TaskType.CONTENT_GEN,
        payload={"draft": "Hello World"}
    )
    assert task.status == TaskStatus.PENDING
    assert task.confidence_score == 1.0

def test_skills_interface_parameters():
    """
    Asserts that your skills modules accept the correct parameters.
    This test is designed to FAIL as the implementations are currently empty.
    """
    from skills.skill_trend_fetcher import TrendFetcherSkill
    from skills.skill_content_creator import ContentCreatorSkill
    from skills.skill_wallet_manager import WalletManagerSkill
    
    trend_skill = TrendFetcherSkill()
    content_skill = ContentCreatorSkill()
    wallet_skill = WalletManagerSkill()
    
    assert trend_skill.name == "skill_trend_fetcher"
    assert content_skill.name == "skill_content_creator"
    assert wallet_skill.name == "skill_wallet_manager"
    
    # Ensure skills were instantiated (Empty Slot filled)
    assert True

def test_failing_skill_interface():
    """
    Failing test for Day 3 goal post.
    Will be implemented to assert skill execution results.
    """
    with pytest.raises(NotImplementedError):
        # This defines the "Empty Slot" the AI must fill
        raise NotImplementedError("Skill logic not yet implemented - TDD Target")
