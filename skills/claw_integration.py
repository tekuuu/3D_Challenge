from skills.base import ChimeraSkill
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
import os
import json
import asyncio
import time

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


class HeartbeatManager:
    """Async heartbeat manager that periodically pings the OpenClaw endpoint.

    Provides start/stop and status helpers for other components.
    """

    def __init__(self, endpoint: Optional[str], interval: int = 60, token_env: str = "CLAW_AUTH_TOKEN"):
        self.endpoint = endpoint
        self.interval = interval
        self._task: Optional[asyncio.Task] = None
        self._client: Optional[httpx.AsyncClient] = None
        self._alive = False
        self._last_seen: Optional[float] = None
        self._running = False
        self._consecutive_failures = 0
        self._token_env = token_env

    @property
    def is_alive(self) -> bool:
        return self._alive

    @property
    def last_seen(self) -> Optional[float]:
        return self._last_seen

    async def _ping_once(self):
        if not self.endpoint or httpx is None:
            # simulation: mark alive and set last_seen
            self._alive = True
            self._last_seen = time.time()
            return

        if self._client is None:
            self._client = httpx.AsyncClient(timeout=5.0)

        token = os.getenv(self._token_env)
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        try:
            url = self.endpoint
            # ensure /heartbeat path
            if not url.endswith("/heartbeat"):
                url = url.rstrip("/") + "/heartbeat"

            resp = await self._client.post(url, json={}, headers=headers)
            resp.raise_for_status()
            self._alive = True
            self._last_seen = time.time()
            self._consecutive_failures = 0
        except Exception:
            self._consecutive_failures += 1
            self._alive = False

    async def _loop(self):
        self._running = True
        backoff = 1
        max_backoff = min(30, self.interval)
        try:
            while self._running:
                await self._ping_once()
                if self._alive:
                    backoff = 1
                    await asyncio.sleep(self.interval)
                else:
                    # exponential backoff on failures
                    await asyncio.sleep(backoff)
                    backoff = min(max_backoff, backoff * 2)
        finally:
            self._running = False

    def start(self):
        if self._task and not self._task.done():
            return
        loop = asyncio.get_event_loop()
        self._task = loop.create_task(self._loop())

    def stop(self):
        self._running = False
        if self._task and not self._task.done():
            self._task.cancel()


class ClawIntegrationSkill(ChimeraSkill):
    def __init__(self):
        super().__init__()
        self._hb_manager: Optional[HeartbeatManager] = None

    @property
    def name(self) -> str:
        return "claw_integration"

    async def execute(self, input_data: ClawHeartbeatInput) -> HeartbeatPayload:
        """Return a heartbeat payload; this is a single-call helper (keeps compatibility).

        For continuous background heartbeats, use `start_heartbeat()` / `stop_heartbeat()`.
        """
        endpoint = os.getenv("CLAW_ENDPOINT")
        payload = HeartbeatPayload()

        # If simulation requested or no endpoint, return simulated payload
        if input_data.simulate or not endpoint:
            return payload

        # Try an async POST probe
        if httpx is None:
            raise RuntimeError("httpx is required for live CLAW_ENDPOINT calls")

        token = os.getenv("CLAW_AUTH_TOKEN")
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        async with httpx.AsyncClient(timeout=3.0) as client:
            try:
                resp = await client.post(endpoint, json=payload.model_dump(), headers=headers)
                resp.raise_for_status()
                data = resp.json()
                return HeartbeatPayload(**{**payload.model_dump(), **data})
            except Exception:
                # fallback: try a GET probe
                try:
                    base_endpoint = endpoint.replace("/heartbeat", "")
                    resp = await client.get(base_endpoint, headers=headers)
                    resp.raise_for_status()
                    data = resp.json()
                    payload.status = f"active_node (running={data.get('running')})"
                    if data.get('cdpUrl'):
                        payload.endpoint = data.get('cdpUrl')
                    return payload
                except Exception:
                    return payload

    def start_heartbeat(self, interval: int = 60):
        endpoint = os.getenv("CLAW_ENDPOINT")
        if self._hb_manager is None:
            self._hb_manager = HeartbeatManager(endpoint=endpoint, interval=interval)
        self._hb_manager.start()

    def stop_heartbeat(self):
        if self._hb_manager:
            self._hb_manager.stop()

    def heartbeat_status(self) -> dict:
        if not self._hb_manager:
            return {"running": False, "alive": False}
        return {"running": self._hb_manager._running, "alive": self._hb_manager.is_alive, "last_seen": self._hb_manager.last_seen}

    def _sign_payload(self, payload: dict) -> str:
        try:
            import hashlib
            token = os.getenv("CLAW_AUTH_TOKEN", "")
            raw = json.dumps(payload, sort_keys=True) + token
            return hashlib.sha256(raw.encode("utf-8")).hexdigest()
        except Exception:
            return "0xDEADBEEF"

    async def publish(self, title: str, body: str) -> dict:
        """Attempt to publish content to the OpenClaw node.

        Falls back to simulated response if publishing is not available.
        """
        endpoint = os.getenv("CLAW_ENDPOINT")
        token = os.getenv("CLAW_AUTH_TOKEN")
        headers = {"Authorization": f"Bearer {token}"} if token else {}

        payload = {
            "agent_id": HeartbeatPayload().agent_id,
            "title": title,
            "body": body,
            "timestamp": datetime.now().isoformat(),
        }
        payload["signature"] = self._sign_payload(payload)

        if not endpoint or httpx is None:
            return {"status": "simulated", "response": payload}

        async with httpx.AsyncClient(timeout=5.0) as client:
            # try direct publish candidates
            candidates = [
                endpoint.rstrip("/") + "/publish",
                endpoint.rstrip("/") + "/posts",
                endpoint.rstrip("/") + "/api/publish",
                endpoint.rstrip("/") + "/api/posts",
            ]
            for url in candidates:
                try:
                    resp = await client.post(url, json=payload, headers=headers)
                    if resp.status_code in (200, 201):
                        try:
                            data = resp.json()
                        except Exception:
                            data = {"raw": resp.text}
                        return {"status": "ok", "response": data, "url": url}
                except Exception:
                    continue

        return {"status": "fallback", "response": payload}
