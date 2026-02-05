import asyncio
import uuid
from typing import List
from schemas.contracts import AgentTask, SkillTrendInput, SkillWalletInput
from skills.skill_trend_fetcher import TrendFetcher
from skills.skill_content_creator import ContentCreator
from skills.skill_wallet_manager import WalletManager

class ChimeraOrchestrator:
    """
    The 'Brain' of Project Chimera. 
    Implements the FastRender Swarm Pattern: Planner -> Worker -> Judge.
    """
    
    def __init__(self):
        self.planner = TrendFetcher()
        self.worker = ContentCreator()
        self.judge = WalletManager()
        self.session_id = uuid.uuid4()

    async def run_campaign_cycle(self, goal: str):
        print(f"[*] Initializing Campaign Cycle: {self.session_id}")
        print(f"[!] Goal: {goal}")

        # 1. PLANNER: Identify Trends
        print("[1] Planner: Fetching market sentiment...")
        trends = await self.planner.execute(SkillTrendInput(topic=goal, timeframe="24h"))
        
        # 2. WORKER: Generate Content based on Trends
        print(f"[2] Worker: Synthesizing content for trends: {trends.get('trends', [])}")
        content_task = AgentTask(
            task_id=uuid.uuid4(),
            type="CONTENT_GEN",
            payload={"source_trends": trends["trends"], "voice": "SOUL.md"},
            status="IN_PROGRESS"
        )
        content_result = await self.worker.execute(content_task)

        # 3. JUDGE: Quality Control & On-Chain Settlement
        print("[3] Judge: Reviewing content and signing transaction...")
        judgement = await self.judge.execute(SkillWalletInput(
            action="SIGN_CONTENT_HASH",
            payload={"content": content_result["generated_text"]}
        ))

        if judgement["status"] == "SUCCESS":
            print("[+] Cycle Complete: Content verified and signed for OpenClaw.")
        else:
            print("[-] Cycle Failed: Judge rejected the output.")

async def main():
    orchestrator = ChimeraOrchestrator()
    await orchestrator.run_campaign_cycle("AI Agent Sovereignty & The Future of Work")

if __name__ == "__main__":
    asyncio.run(main())
