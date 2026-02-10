from skills.base import ChimeraSkill
from schemas.contracts import SkillTrendInput, SkillTrendOutput, TrendItem


class TrendFetcherSkill(ChimeraSkill):
    @property
    def name(self) -> str:
        return "skill_trend_fetcher"

    async def execute(self, input_data: SkillTrendInput) -> SkillTrendOutput:
        """Minimal, test-focused implementation returning a deterministic trend output.

        This is a lightweight stub used to satisfy TDD tests and can be
        replaced with LLM/connector logic in later iterations.
        """
        # Produce a single trend item derived from the provided seed
        topic = f"{input_data.agent_niche} - signal from {input_data.source_data}"
        item = TrendItem(topic=topic, signal_strength=0.85, suggested_action="RESEARCH")
        return SkillTrendOutput(top_trends=[item])
