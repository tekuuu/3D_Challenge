import pytest
from schemas.contracts import SkillTrendOutput
from skills.skill_trend_fetcher import TrendFetcherSkill


def test_trend_fetcher_data_structure():
    """
    Asserts that the trend data structure matches the API contract.
    This test is designed to FAIL as the implementation is currently a placeholder.
    """
    # Call the implemented TrendFetcherSkill
    result = asyncio.run(TrendFetcherSkill().execute(SkillTrendInput(source_data="seed", agent_niche="ai")))

    assert result is not None, "Trend data should not be None"
    assert isinstance(result, SkillTrendOutput), "Result must match SkillTrendOutput schema"
    assert len(result.top_trends) > 0, "Should return at least one trend"
