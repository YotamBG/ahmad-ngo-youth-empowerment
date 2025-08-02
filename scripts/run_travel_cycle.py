#!/usr/bin/env python3
"""
🚀 Run Travel Agent with Skeptical Cycles
Based on jarvis project methodology
"""

import subprocess
import time
import os
from pathlib import Path

def run_travel_cycle():
    """Run a single travel search cycle"""
    try:
        result = subprocess.run([
            "python3", "travel_agent.py"
        ], capture_output=True, text=True, timeout=120)
        
        output = result.stdout + result.stderr
        success = "TRAVEL SEARCH COMPLETED SUCCESSFULLY" in output
        
        return success, output
    except Exception as e:
        return False, str(e)

def main():
    print("🚀 RUNNING TRAVEL AGENT SKEPTICAL CYCLES")
    print("=" * 60)
    
    cycle_count = 0
    max_cycles = 5
    
    while cycle_count < max_cycles:
        cycle_count += 1
        print(f"\n🔄 CYCLE {cycle_count}/{max_cycles}")
        print("-" * 40)
        
        start_time = time.time()
        success, output = run_travel_cycle()
        duration = time.time() - start_time
        
        if success:
            print(f"✅ SUCCESS in {duration:.1f}s")
            print("🎉 FLIGHT SEARCH COMPLETED!")
            break
        else:
            print(f"❌ FAILED in {duration:.1f}s")
            print(f"Error: {output[-200:]}")  # Last 200 chars
        
        # Wait between cycles
        if cycle_count < max_cycles:
            print(f"⏳ Waiting 10s before retry...")
            time.sleep(10)
    
    print(f"\n�� FINAL RESULTS:")
    print(f"📊 Cycles Run: {cycle_count}")
    print(f"🎯 Success: {'Yes' if success else 'No'}")

if __name__ == "__main__":
    main()
