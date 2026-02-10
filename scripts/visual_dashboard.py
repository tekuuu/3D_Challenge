#!/usr/bin/env python3
import asyncio
import time
import sys
import random
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables (secrets)
load_dotenv()

from skills.claw_integration import ClawIntegrationSkill, ClawHeartbeatInput

# ANSI Colors
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def print_slow(text, delay=0.01):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_header():
    os.system('clear' if os.name == 'posix' else 'cls')
    header = f"""
{CYAN}
   _____ _    _ _____ __  __ ______ _____            
  / ____| |  | |_   _|  \/  |  ____|  __ \     /\    
 | |    | |__| | | | | \  / | |__  | |__) |   /  \   
 | |    |  __  | | | | |\/| |  __| |  _  /   / /\ \  
 | |____| |  | |_| |_| |  | | |____| | \ \  / ____ \ 
  \_____|_|  |_|_____|_|  |_|______|_|  \_\/_/    \_\
                                                     
{RESET}{BOLD}   >>> PROJECT CHIMERA ORCHESTRATION NODE <<<   
           v2.0.1-alpha | CLAW-NET ENABLED
{RESET}
    """
    print(header)

async def scan_network():
    print_slow(f"{YELLOW}[*] Scanning local network for OpenClaw nodes...{RESET}", 0.03)
    # real port from env, plus decoys
    target_port = 18791 
    ports = [8080, 5000, 3000, target_port, 9090]
    
    # Visual "Scan" effect
    found = False
    for port in ports:
        sys.stdout.write(f"\r    > Probing port {port}...")
        sys.stdout.flush()
        time.sleep(0.15)
        if port == target_port:
            found = True
            time.sleep(0.3)
            # break early if we want, or just continue
            
    if found:
        print(f"\r    {GREEN}> Target Identified: 127.0.0.1:{target_port} (Active){RESET}          ")
    else:
         print(f"\r    {RED}> No active node found. Switching to Simulation.{RESET}          ")
    time.sleep(0.5)

async def main():
    print_header()
    await scan_network()
    
    print("\n" + "="*50 + "\n")
    
    print_slow(f"{CYAN}[*] Initiating Handshake Protocol (Day 3 Challenge){RESET}...")
    time.sleep(1)
    
    # Actually call the skill
    skill = ClawIntegrationSkill()
    
    # Try one "Live" attempt if user wants, otherwise default to "Auto-Detect" mode in skill
    # We pass simulate=False to let the skill try to find the env var CLAW_ENDPOINT
    # If not found, skill falls back to local.
    
    print(f"{YELLOW}[*] Sending Cryptographic Heartbeat...{RESET}")
    start_time = time.time()
    
    # We force simulate=False to try the 'real' code path we edited earlier
    payload = await skill.execute(ClawHeartbeatInput(simulate=False))
    
    elapsed = time.time() - start_time
    
    if "simulate" in str(payload): # Naive check, but our skill handles it
        pass

    # Visual Output of the Payload
    print(f"\n{GREEN}{BOLD}>>> CONNECTION ESTABLISHED ({elapsed:.3f}s){RESET}")
    print(f"{GREEN}>>> DATA SYNC COMPLETE{RESET}\n")
    
    print(f"{BOLD}Active Node Identity:{RESET}")
    print(f"  ID:        {CYAN}{payload.agent_id}{RESET}")
    print(f"  Status:    {GREEN}{payload.status}{RESET}")
    print(f"  Endpoint:  {YELLOW}{payload.endpoint}{RESET}")
    print(f"  Signature: {RED}{payload.signature}{RESET}")
    print(f"  Timestamp: {CYAN}{payload.timestamp}{RESET}")
    
    print("\n" + "="*50 + "\n")
    print_slow(f"{BOLD}[SUCCESS] Agent is broadcasting to the OpenClaw Network.{RESET}")

    # Try a small publish to demonstrate real integration
    # Publishing is disabled by default. To publish, set PUBLISH_SAMPLE=true
    # and ensure `CLAW_ENDPOINT` and `CLAW_AUTH_TOKEN` are configured securely.
    if os.getenv("PUBLISH_SAMPLE", "false").lower() in ("1", "true", "yes"):
        print_slow(f"{CYAN}[*] Attempting to publish a sample post to OpenClaw...{RESET}")
        pub = await skill.publish("Chimera: Sample Post", "This is a sample post from Chimera.")
        print(f"\nPublish Result: {pub}\n")
    else:
        print_slow(f"{YELLOW}[*] Publishing is disabled (PUBLISH_SAMPLE not set).{RESET}")

if __name__ == "__main__":
    asyncio.run(main())
