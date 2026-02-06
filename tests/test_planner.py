import pytest
from agents.planner import Planner
from schemas.contracts import AgentTask

def test_planner_goal_decomposition():
    planner = Planner()
    goal = "Increase DeFi engagement"
    tasks = planner.decompose(goal)
    
    # TDD: This will fail because Planner is not implemented
    assert len(tasks) >= 3
    assert all(isinstance(t, AgentTask) for t in tasks)
    assert tasks[0].type == "RESEARCH"

def test_planner_invalid_goal():
    planner = Planner()
    with pytest.raises(ValueError):
        planner.decompose("")
