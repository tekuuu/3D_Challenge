import asyncio
from skills.claw_integration import ClawIntegrationSkill, ClawHeartbeatInput, HeartbeatPayload


def test_openclaw_heartbeat_shape():
    skill = ClawIntegrationSkill()
    result = asyncio.run(skill.execute(ClawHeartbeatInput()))
    assert isinstance(result, HeartbeatPayload)
    assert result.agent_id == "chimera-z01"
    assert result.status == "ready_for_collaboration"
