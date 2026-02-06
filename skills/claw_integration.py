from skills.base import ChimeraSkill
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os
import json

try:
    import httpx
except Exception:
    httpx = None


class ClawHeartbeatInput(BaseModel):
    simulate: bool = True


class HeartbeatPayload(BaseModel):
    agent_id: str = "chimera-z01"
    status: str = "ready_for_collaboration"
    skills: List[str] = ["on-chain-research", "narrative-synthesis"]
    endpoint: str = "mcp://chimera.node:8080"
    signature: str = "0xDEADBEEF"
    timestamp: datetime = Field(default_factory=datetime.now)


class ClawIntegrationSkill(ChimeraSkill):
    @property
    def name(self) -> str:
        return "claw_integration"

    async def execute(self, input_data: ClawHeartbeatInput) -> HeartbeatPayload:
        """
        If `CLAW_ENDPOINT` env var is set and `input_data.simulate` is False,
        attempt a local POST to the endpoint. Otherwise return a simulated
        `HeartbeatPayload` (safe demo mode).
        """
        endpoint = os.getenv("CLAW_ENDPOINT")
        payload = HeartbeatPayload()

        if endpoint and (not input_data.simulate):
            if httpx is None:
                raise RuntimeError("httpx is required for live CLAW_ENDPOINT calls")
            token = os.getenv("CLAW_AUTH_TOKEN")
            headers = {"Authorization": f"Bearer {token}"} if token else {}
            try:
                # Best-effort, short timeout, do not raise on failure
                resp = httpx.post(endpoint, content=payload.model_dump_json(), headers=headers, timeout=2.0)
                # return remote echo if JSON; otherwise return local payload
                try:
                    data = resp.json()
                    return HeartbeatPayload(**{**payload.model_dump(), **data})
                except Exception:
                    return payload
            except Exception:
                return payload

        return payload
