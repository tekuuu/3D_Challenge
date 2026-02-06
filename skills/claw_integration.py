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
                # 1. Attempt Standard POST Heartbeat
                resp = httpx.post(endpoint, content=payload.model_dump_json(), headers=headers, timeout=2.0)
                resp.raise_for_status()
                data = resp.json()
                print(f"✅ [LIVE] Successfully synced with OpenClaw Node at {endpoint}")
                return HeartbeatPayload(**{**payload.model_dump(), **data})

            except Exception as post_error:
                # 2. Fallback: Try GET Status (Probe) if POST fails (e.g. we are talking to a Control Node)
                try:
                    # Remove /heartbeat if present for the GET probe
                    base_endpoint = endpoint.replace("/heartbeat", "")
                    resp = httpx.get(base_endpoint, headers=headers, timeout=2.0)
                    resp.raise_for_status()
                    data = resp.json()
                    
                    # Log success and map real data to our payload
                    print(f"✅ [LIVE] Connected to OpenClaw Control Plane at {base_endpoint}")
                    print(f"   > Remote Status: Enabled={data.get('enabled')}, Running={data.get('running')}")
                    
                    # Update payload with real network status
                    payload.status = f"active_node (running={data.get('running')})"
                    if data.get('cdpUrl'):
                         payload.endpoint = data.get('cdpUrl')  # Real specialized endpoint
                    
                    return payload
                except Exception as get_error:
                     print(f"⚠️ [LIVE] Integration Warning: POST failed ({post_error}) AND GET failed ({get_error}). Falling back to local signature.")
                     return payload
                
            except Exception as e:
                print(f"⚠️ [LIVE] Connection Failed: {e}. Falling back to local signature.")
                return payload

        return payload

    def _sign_payload(self, payload: dict) -> str:
        """Create a simple deterministic signature placeholder.

        In production this should use a real keypair/signing method.
        We include the `CLAW_AUTH_TOKEN` in the HMAC if present to demonstrate
        a signed payload for the control plane.
        """
        try:
            import hashlib
            token = os.getenv("CLAW_AUTH_TOKEN", "")
            raw = json.dumps(payload, sort_keys=True) + token
            return hashlib.sha256(raw.encode("utf-8")).hexdigest()
        except Exception:
            return "0xDEADBEEF"

    async def publish(self, title: str, body: str) -> dict:
        """Attempt to publish content to the OpenClaw node.

        This method tries several common publish endpoints and falls back
        safely to a local simulation response. It returns a dict with
        `status` and `response` keys to make assertions easy in tests.
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

        # Try a list of common publish paths
        # First, attempt to discover a publish URL from the control plane root
        try:
            base = endpoint.rstrip("/")
            probe = httpx.get(base, headers=headers, timeout=2.0)
            try:
                info = probe.json()
            except Exception:
                info = None

            if isinstance(info, dict):
                # Look for fields that might indicate a publish endpoint
                for key in ("publishUrl", "publish_url", "postsUrl", "controlUrl", "cdpUrl", "control_url"):
                    if key in info and info[key]:
                        candidate = info[key]
                        # if it's a base control URL, try common subpaths
                        if candidate.endswith("/"):
                            candidate = candidate.rstrip("/")
                        pub_candidates = [candidate, candidate + "/publish", candidate + "/posts", candidate + "/api/publish"]
                        for url in pub_candidates:
                            try:
                                resp = httpx.post(url, json=payload, headers=headers, timeout=3.0)
                                if resp.status_code in (200, 201):
                                    try:
                                        data = resp.json()
                                    except Exception:
                                        data = {"raw": resp.text}
                                    print(f"✅ [PUBLISH] Successfully posted to {url} (status={resp.status_code})")
                                    return {"status": "ok", "response": data, "url": url}
                                else:
                                    print(f"⚠️ [PUBLISH] {url} returned {resp.status_code}")
                            except Exception as e:
                                print(f"⚠️ [PUBLISH] Failed to POST to {url}: {e}")

        except Exception:
            # ignore probe failures and fallback to brute candidates below
            pass

        # Try a list of common publish paths relative to the configured endpoint
        candidates = [
            endpoint.rstrip("/") + "/publish",
            endpoint.rstrip("/") + "/posts",
            endpoint.rstrip("/") + "/api/publish",
            endpoint.rstrip("/") + "/api/posts",
        ]

        for url in candidates:
            try:
                resp = httpx.post(url, json=payload, headers=headers, timeout=3.0)
                if resp.status_code in (200, 201):
                    try:
                        data = resp.json()
                    except Exception:
                        data = {"raw": resp.text}
                    print(f"✅ [PUBLISH] Successfully posted to {url} (status={resp.status_code})")
                    return {"status": "ok", "response": data, "url": url}
                else:
                    print(f"⚠️ [PUBLISH] {url} returned {resp.status_code}")
            except Exception as e:
                # Try next candidate
                print(f"⚠️ [PUBLISH] Failed to POST to {url}: {e}")

        # If all publish attempts fail, return simulated result
        return {"status": "fallback", "response": payload}
