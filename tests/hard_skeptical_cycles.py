#!/usr/bin/env python3
"""
🔥 HARD SKEPTICAL CYCLES FOR TRAVEL AGENT
Based on jarvis project methodology - aggressive testing until 100% verified
"""

import subprocess
import time
import json
import os
import threading
from datetime import datetime
from pathlib import Path

class HardSkepticalTester:
    """Aggressive skeptical testing against the travel agent"""
    
    def __init__(self):
        self.start_time = time.time()
        self.timestamp = int(self.start_time)
        self.evidence_dir = f"HARD_SKEPTICAL_EVIDENCE_{self.timestamp}"
        self.results = {
            "cycles_run": 0,
            "passed": 0, 
            "failed": 0,
            "errors": 0,
            "evidence": [],
            "performance_metrics": []
        }
        
        os.makedirs(self.evidence_dir, exist_ok=True)
        
        print("🔥 HARD SKEPTICAL CYCLES STARTED")
        print(f"📂 Evidence collection: {self.evidence_dir}")
        print(f"🕐 Start time: {datetime.now().isoformat()}")
        print("=" * 80)
    
    def log_evidence(self, cycle, test_name, evidence_type, data, success=True):
        """Log evidence for each test"""
        evidence_entry = {
            "timestamp": datetime.now().isoformat(),
            "cycle": cycle,
            "test": test_name,
            "type": evidence_type,
            "success": success,
            "data": str(data)[:500]
        }
        self.results["evidence"].append(evidence_entry)
        
        # Save to file
        evidence_file = f"{self.evidence_dir}/cycle_{cycle}_{test_name}_{evidence_type}_{self.timestamp}.txt"
        with open(evidence_file, "w") as f:
            f.write(f"Cycle: {cycle}\n")
            f.write(f"Test: {test_name}\n")
            f.write(f"Type: {evidence_type}\n") 
            f.write(f"Success: {success}\n")
            f.write(f"Timestamp: {evidence_entry['timestamp']}\n")
            f.write("="*50 + "\n")
            f.write(str(data))
        
        status = "✅" if success else "❌"
        print(f"📋 Cycle {cycle}: {test_name} - {evidence_type} - {status}")
    
    def run_travel_agent_cycle(self, cycle_num, timeout=120):
        """Run single travel agent cycle with aggressive testing"""
        try:
            print(f"\n🔄 HARD CYCLE {cycle_num} - AGGRESSIVE TESTING")
            print("-" * 60)
            
            start_time = time.time()
            
            # Run the travel agent with timeout
            result = subprocess.run([
                "python3", "simple_robust_travel_agent.py"
            ], capture_output=True, text=True, timeout=timeout)
            
            duration = time.time() - start_time
            output = result.stdout + result.stderr
            
            # Performance metrics
            performance = {
                "cycle": cycle_num,
                "duration": duration,
                "return_code": result.returncode,
                "output_length": len(output),
                "timestamp": datetime.now().isoformat()
            }
            self.results["performance_metrics"].append(performance)
            
            # Log performance evidence
            self.log_evidence(cycle_num, "performance", "timing", 
                            f"Duration: {duration:.2f}s, Return code: {result.returncode}")
            
            # Analyze output for success indicators
            success_indicators = [
                "SIMPLE TRAVEL AGENT INITIALIZED",
                "STARTING FLIGHT SEARCH", 
                "AI analyzing flight options",
                "Travel agent completed successfully"
            ]
            
            failure_indicators = [
                "failed:",
                "error:",
                "exception:",
                "traceback",
                "❌"
            ]
            
            success_count = sum(1 for indicator in success_indicators if indicator.lower() in output.lower())
            failure_count = sum(1 for indicator in failure_indicators if indicator.lower() in output.lower())
            
            # Determine overall success
            cycle_success = (
                result.returncode == 0 and
                success_count >= 2 and
                failure_count == 0 and
                duration < timeout
            )
            
            # Log detailed analysis
            analysis = {
                "success_indicators": success_count,
                "failure_indicators": failure_count,
                "return_code": result.returncode,
                "duration": duration,
                "output_sample": output[-300:] if output else "No output"
            }
            
            self.log_evidence(cycle_num, "analysis", "output_analysis", analysis, cycle_success)
            
            # Update results
            self.results["cycles_run"] += 1
            if cycle_success:
                self.results["passed"] += 1
                print(f"✅ CYCLE {cycle_num} PASSED ({duration:.2f}s)")
            else:
                self.results["failed"] += 1
                print(f"❌ CYCLE {cycle_num} FAILED ({duration:.2f}s)")
                print(f"   Success indicators: {success_count}")
                print(f"   Failure indicators: {failure_count}")
                print(f"   Return code: {result.returncode}")
            
            return cycle_success, duration, output
            
        except subprocess.TimeoutExpired:
            self.results["cycles_run"] += 1
            self.results["errors"] += 1
            self.log_evidence(cycle_num, "timeout", "process_timeout", f"Timeout after {timeout}s", False)
            print(f"⏰ CYCLE {cycle_num} TIMED OUT after {timeout}s")
            return False, timeout, "TIMEOUT"
            
        except Exception as e:
            self.results["cycles_run"] += 1
            self.results["errors"] += 1
            self.log_evidence(cycle_num, "exception", "unexpected_error", str(e), False)
            print(f"💥 CYCLE {cycle_num} CRASHED: {e}")
            return False, 0, str(e)
    
    def stress_test_parallel(self, num_parallel=3):
        """Run multiple agents in parallel for stress testing"""
        print(f"\n🔥 STRESS TEST: {num_parallel} PARALLEL AGENTS")
        print("-" * 60)
        
        results = []
        threads = []
        
        def run_agent(agent_id):
            try:
                start_time = time.time()
                result = subprocess.run([
                    "python3", "simple_robust_travel_agent.py"
                ], capture_output=True, text=True, timeout=60)
                duration = time.time() - start_time
                
                success = result.returncode == 0
                results.append({
                    "agent_id": agent_id,
                    "success": success,
                    "duration": duration,
                    "return_code": result.returncode
                })
                
                print(f"   Agent {agent_id}: {'✅' if success else '❌'} ({duration:.2f}s)")
                
            except Exception as e:
                results.append({
                    "agent_id": agent_id,
                    "success": False,
                    "duration": 0,
                    "error": str(e)
                })
                print(f"   Agent {agent_id}: 💥 {e}")
        
        # Start parallel threads
        for i in range(num_parallel):
            thread = threading.Thread(target=run_agent, args=(i+1,))
            threads.append(thread)
            thread.start()
        
        # Wait for all to complete
        for thread in threads:
            thread.join()
        
        # Analyze results
        successful = sum(1 for r in results if r.get("success", False))
        total = len(results)
        
        self.log_evidence("STRESS", "parallel_test", "stress_results", 
                         f"Successful: {successful}/{total}", successful == total)
        
        print(f"🎯 STRESS TEST RESULT: {successful}/{total} agents succeeded")
        return successful == total
    
    def run_hard_cycles(self, max_cycles=20, target_success_rate=95.0):
        """Run hard skeptical cycles until target achieved"""
        print(f"🔥 RUNNING HARD SKEPTICAL CYCLES")
        print(f"🎯 Target: {target_success_rate}% success rate")
        print(f"📊 Max cycles: {max_cycles}")
        print("=" * 80)
        
        consecutive_failures = 0
        max_consecutive_failures = 3
        
        for cycle in range(1, max_cycles + 1):
            success, duration, output = self.run_travel_agent_cycle(cycle)
            
            if success:
                consecutive_failures = 0
            else:
                consecutive_failures += 1
                
                # Fail-fast logic
                if consecutive_failures >= max_consecutive_failures:
                    print(f"\n💥 FAIL-FAST TRIGGERED: {consecutive_failures} consecutive failures")
                    break
            
            # Calculate current success rate
            if self.results["cycles_run"] > 0:
                current_success_rate = (self.results["passed"] / self.results["cycles_run"]) * 100
                print(f"📊 Current success rate: {current_success_rate:.1f}%")
                
                # Check if target achieved
                if current_success_rate >= target_success_rate and self.results["cycles_run"] >= 5:
                    print(f"\n🎉 TARGET ACHIEVED! {current_success_rate:.1f}% success rate")
                    break
            
            # Stress test every 5 cycles
            if cycle % 5 == 0:
                stress_success = self.stress_test_parallel()
                if not stress_success:
                    print("⚠️ Stress test failed - agent may not be robust enough")
            
            # Brief pause between cycles
            time.sleep(1)
        
        # Run final comprehensive test
        print(f"\n🧪 FINAL COMPREHENSIVE TEST")
        final_stress = self.stress_test_parallel(5)  # 5 parallel agents
        
        return self.results
    
    def print_final_results(self):
        """Print comprehensive final results"""
        total_duration = time.time() - self.start_time
        
        print(f"\n" + "=" * 80)
        print("🏆 HARD SKEPTICAL CYCLES FINAL RESULTS")
        print("=" * 80)
        
        # Basic stats
        print(f"🔄 Total Cycles: {self.results['cycles_run']}")
        print(f"✅ Passed: {self.results['passed']}")
        print(f"❌ Failed: {self.results['failed']}")
        print(f"💥 Errors: {self.results['errors']}")
        print(f"⏱️ Total Duration: {total_duration:.1f}s")
        
        # Success rate
        if self.results["cycles_run"] > 0:
            success_rate = (self.results["passed"] / self.results["cycles_run"]) * 100
            print(f"📊 Final Success Rate: {success_rate:.1f}%")
        
        # Performance analysis
        if self.results["performance_metrics"]:
            durations = [m["duration"] for m in self.results["performance_metrics"]]
            avg_duration = sum(durations) / len(durations)
            min_duration = min(durations)
            max_duration = max(durations)
            
            print(f"\n📈 PERFORMANCE ANALYSIS:")
            print(f"   Average cycle time: {avg_duration:.2f}s")
            print(f"   Fastest cycle: {min_duration:.2f}s")
            print(f"   Slowest cycle: {max_duration:.2f}s")
        
        # Evidence summary
        print(f"\n📁 EVIDENCE COLLECTED:")
        print(f"   📂 Evidence directory: {self.evidence_dir}")
        print(f"   📋 Evidence entries: {len(self.results['evidence'])}")
        
        # Final verdict
        if self.results["cycles_run"] > 0:
            success_rate = (self.results["passed"] / self.results["cycles_run"]) * 100
            if success_rate >= 95:
                print(f"\n🎉 TRAVEL AGENT VERIFIED: {success_rate:.1f}% success rate")
                print("✅ READY FOR PRODUCTION USE")
            elif success_rate >= 80:
                print(f"\n⚠️ TRAVEL AGENT NEEDS IMPROVEMENT: {success_rate:.1f}% success rate")
                print("🔧 REQUIRES OPTIMIZATION BEFORE PRODUCTION")
            else:
                print(f"\n❌ TRAVEL AGENT FAILED VERIFICATION: {success_rate:.1f}% success rate")
                print("🚫 NOT SUITABLE FOR PRODUCTION")

def main():
    """Main hard skeptical testing function"""
    tester = HardSkepticalTester()
    
    try:
        # Run hard cycles
        results = tester.run_hard_cycles(max_cycles=15, target_success_rate=90.0)
        
        # Print results
        tester.print_final_results()
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted by user")
        tester.print_final_results()
    except Exception as e:
        print(f"\n💥 Testing crashed: {e}")
        tester.print_final_results()

if __name__ == "__main__":
    main()
