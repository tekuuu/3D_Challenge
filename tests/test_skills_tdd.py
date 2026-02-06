import asyncio
from skills.skill_trend_fetcher import TrendFetcherSkill
from skills.skill_content_creator import ContentCreatorSkill, ContentCreatorInput, ContentCreatorOutput
from skills.skill_wallet_manager import WalletManagerSkill
from schemas.contracts import SkillTrendInput, SkillTrendOutput, SkillWalletInput, WalletAction


def test_trend_fetcher_should_return_skilltrendoutput():
    skill = TrendFetcherSkill()
    result = asyncio.run(skill.execute(SkillTrendInput(source_data="seed", agent_niche="ai")))
    assert isinstance(result, SkillTrendOutput), "TrendFetcher must return SkillTrendOutput (TDD failing test)"


def test_content_creator_should_return_output_model():
    skill = ContentCreatorSkill()
    input_data = ContentCreatorInput(trend_data={}, platform="twitter", voice_ref="specs/SOUL.md")
    result = asyncio.run(skill.execute(input_data))
    assert isinstance(result, ContentCreatorOutput), "ContentCreator must return ContentCreatorOutput (TDD failing test)"


def test_wallet_manager_should_return_walletoutput():
    skill = WalletManagerSkill()
    input_data = SkillWalletInput(action=WalletAction.CHECK_BALANCE)
    result = asyncio.run(skill.execute(input_data))
    # We expect a pydantic-like response; exact fields will be implemented in Day 3
    assert hasattr(result, 'success'), "WalletManager must return an object with 'success' field (TDD failing test)"
