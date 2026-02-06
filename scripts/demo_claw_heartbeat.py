#!/usr/bin/env python3
"""Demo script to show local Claw integration.

Usage:
  # Simulated (safe):
  python3 scripts/demo_claw_heartbeat.py

  # Live local demo (only if you run clawdbot locally and want to POST):
  CLAW_ENDPOINT=http://localhost:8080/heartbeat python3 scripts/demo_claw_heartbeat.py --live
"""
import asyncio
import os
import argparse
from skills.claw_integration import ClawIntegrationSkill, ClawHeartbeatInput


async def main(live: bool):
    skill = ClawIntegrationSkill()
    input_data = ClawHeartbeatInput(simulate=not live)
    result = await skill.execute(input_data)
    print("Heartbeat result:")
    print(result.model_dump())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Attempt to POST to CLAW_ENDPOINT")
    args = parser.parse_args()
    asyncio.run(main(args.live))
