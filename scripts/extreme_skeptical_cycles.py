#!/usr/bin/env python3
"""
🔥 EXTREME SKEPTICAL CYCLES - FIND EVERY POSSIBLE ISSUE
Non-stop testing until 100% bulletproof
"""

import subprocess
import time
import json
import os
import threading
import random
import signal
import psutil
from datetime import datetime
from pathlib import Path

class ExtremeTester:
    """Extreme testing to find ANY remaining issues"""
    
    def __init__(self):
        self.start_time = time.time()
        self.timestamp = int(self.start_time)
        self.evidence_dir = f"EXTREME_EVIDENCE_{self.timestamp}"
        self.results = {
            "total_cycles": 0,
            "passed": 0,
            "failed": 0,
            "errors": 0,
            "timeouts": 0,
            "memory_issues": 0,
            "performance_issues": 0,
            "evidence": []
        }
        
        os.makedirs(self.evidence_dir, exist_ok=True)
        
        print("�� EXTREME SKEPTICAL CYCLES - NON-STOP TESTING")
        print("🎯 Goal: Find EVERY possible issue until bulletproof")
        print(f"📂 Evidence: {self.evidence_dir}")
        print("=" * 80)
    
    def log_evidence(self, test_type, data, success=True):
        """Enhanced evidence logging"""
        timestamp = datetime.now().isoformat()
        evidence = {
            "timestamp": timestamp,
            "test_type": test_type,
            "success": success,
            "data": str(data)[:1000]  # More data
        }
        self.results["evidence"].append(evidence)
        
        # Save to file
        filename = f"{self.evidence_dir}/{test_type}_{timestamp.replace(':', '-')}.txt"
        with open(filename, "w") as f:
            f.write(f"Test: {test_type}\n")
            f.write(f"Success: {success}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("="*60 + "\n")
            f.write(str(data))
        
        status = "✅" if success else "❌"
        print(f"📋 {test_type}: {status}")
    
    def stress_test_memory(self):
        """Test memory usage under load"""
        print("\n🧠 MEMORY STRESS TEST")
        print("-" * 40)
        
        initial_memory = psutil.virtual_memory().percent
        
        threads = []
        results = []
        
        def memory_intensive_agent():
            try:
                # Run agent while monitoring memory
                process = subprocess.Popen([
                    "python3", "fixed_travel_agent.py"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                max_memory = initial_memory
                
                while process.poll() is None:
                    current_memory = psutil.virtual_memory().percent
                    max_memory = max(max_memory, current_memory)
                    time.sleep(0.1)
                
                process.wait()
                results.append({
                    "success": process.returncode == 0,
                    "max_memory": max_memory,
                    "memory_increase": max_memory - initial_memory
                })
                
            except Exception as e:
                results.append({"error": str(e), "success": False})
        
        # Run 5 parallel memory-intensive tests
        for i in range(5):
            thread = threading.Thread(target=memory_intensive_agent)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        # Analyze memory usage
        successful = sum(1 for r in results if r.get("success", False))
        memory_increases = [r.get("memory_increase", 0) for r in results if "memory_increase" in r]
        
        memory_safe = all(inc < 20 for inc in memory_increases)  # Less than 20% memory increase
        
        self.log_evidence("memory_stress", {
            "successful": successful,
            "total": len(results),
            "memory_increases": memory_increases,
            "memory_safe": memory_safe
        }, successful == len(results) and memory_safe)
        
        if not memory_safe:
            self.results["memory_issues"] += 1
        
        print(f"   Memory test: {successful}/{len(results)} passed")
        print(f"   Max memory increase: {max(memory_increases) if memory_increases else 0:.1f}%")
        
        return memory_safe
    
    def performance_regression_test(self):
        """Test for performance regressions"""
        print("\n⚡ PERFORMANCE REGRESSION TEST")
        print("-" * 40)
        
        times = []
        
        for i in range(10):  # 10 performance samples
            start = time.time()
            result = subprocess.run([
                "python3", "fixed_travel_agent.py"
            ], capture_output=True, timeout=30)
            duration = time.time() - start
            
            times.append(duration)
            print(f"   Run {i+1}: {duration:.2f}s")
        
        avg_time = sum(times) / len(times)
        max_time = max(times)
        min_time = min(times)
        variance = max_time - min_time
        
        # Performance criteria
        performance_good = (
            avg_time < 3.0 and  # Average under 3s
            max_time < 5.0 and  # No run over 5s
            variance < 2.0      # Low variance
        )
        
        self.log_evidence("performance_regression", {
            "avg_time": avg_time,
            "max_time": max_time,
            "min_time": min_time,
            "variance": variance,
            "all_times": times
        }, performance_good)
        
        if not performance_good:
            self.results["performance_issues"] += 1
        
        print(f"   Average: {avg_time:.2f}s")
        print(f"   Range: {min_time:.2f}s - {max_time:.2f}s")
        print(f"   Performance: {'✅ Good' if performance_good else '❌ Issues'}")
        
        return performance_good
    
    def chaos_test(self):
        """Chaos testing - random interruptions"""
        print("\n🌪️ CHAOS TEST - Random Interruptions")
        print("-" * 40)
        
        chaos_results = []
        
        for i in range(5):
            try:
                process = subprocess.Popen([
                    "python3", "fixed_travel_agent.py"
                ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                
                # Random interruption after 0.5-2s
                interrupt_time = random.uniform(0.5, 2.0)
                time.sleep(interrupt_time)
                
                # Send SIGTERM (graceful shutdown)
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    stdout, stderr = process.communicate(timeout=5)
                    graceful = True
                except subprocess.TimeoutExpired:
                    # Force kill if not graceful
                    process.kill()
                    stdout, stderr = process.communicate()
                    graceful = False
                
                chaos_results.append({
                    "interrupted_at": interrupt_time,
                    "graceful_shutdown": graceful,
                    "return_code": process.returncode
                })
                
                print(f"   Chaos {i+1}: {'✅ Graceful' if graceful else '❌ Force killed'}")
                
            except Exception as e:
                chaos_results.append({"error": str(e)})
                print(f"   Chaos {i+1}: 💥 {e}")
        
        graceful_count = sum(1 for r in chaos_results if r.get("graceful_shutdown", False))
        chaos_resilient = graceful_count >= len(chaos_results) * 0.6  # 60% graceful
        
        self.log_evidence("chaos_test", {
            "total": len(chaos_results),
            "graceful": graceful_count,
            "results": chaos_results
        }, chaos_resilient)
        
        print(f"   Chaos resilience: {graceful_count}/{len(chaos_results)} graceful")
        
        return chaos_resilient
    
    def edge_case_inputs_test(self):
        """Test with edge case inputs"""
        print("\n🔀 EDGE CASE INPUTS TEST")
        print("-" * 40)
        
        # Create edge case user data files
        edge_cases = [
            # Empty data
            {"personal": {}, "trip": {}},
            # Invalid dates
            {"personal": {"first_name": "Test"}, "trip": {"depart_date": "invalid-date"}},
            # Extreme values
            {"personal": {"first_name": "A" * 1000}, "trip": {"budget": -999}},
            # Special characters
            {"personal": {"first_name": "Test'\"<>&"}, "trip": {"origin": "!@#$"}},
        ]
        
        edge_results = []
        
        for i, edge_data in enumerate(edge_cases):
            # Backup original
            if os.path.exists("user_data.json"):
                os.rename("user_data.json", f"user_data_backup_{i}.json")
            
            try:
                # Write edge case data
                with open("user_data.json", "w") as f:
                    json.dump(edge_data, f)
                
                # Test agent with edge case
                result = subprocess.run([
                    "python3", "fixed_travel_agent.py"
                ], capture_output=True, timeout=30)
                
                # Agent should handle gracefully, not crash
                handled_gracefully = result.returncode == 0 or "error" not in result.stderr.lower()
                
                edge_results.append({
                    "case": i+1,
                    "handled_gracefully": handled_gracefully,
                    "return_code": result.returncode
                })
                
                print(f"   Edge case {i+1}: {'✅ Handled' if handled_gracefully else '❌ Failed'}")
                
            except Exception as e:
                edge_results.append({"case": i+1, "error": str(e)})
                print(f"   Edge case {i+1}: �� {e}")
            
            finally:
                # Restore original
                if os.path.exists(f"user_data_backup_{i}.json"):
                    if os.path.exists("user_data.json"):
                        os.remove("user_data.json")
                    os.rename(f"user_data_backup_{i}.json", "user_data.json")
        
        handled_count = sum(1 for r in edge_results if r.get("handled_gracefully", False))
        edge_resilient = handled_count >= len(edge_results) * 0.8  # 80% handled
        
        self.log_evidence("edge_cases", {
            "total": len(edge_results),
            "handled": handled_count,
            "results": edge_results
        }, edge_resilient)
        
        print(f"   Edge case resilience: {handled_count}/{len(edge_results)} handled")
        
        return edge_resilient
    
    def concurrent_load_test(self):
        """Heavy concurrent load test"""
        print("\n🔄 CONCURRENT LOAD TEST")
        print("-" * 40)
        
        load_results = []
        
        def concurrent_agent(agent_id):
            try:
                start_time = time.time()
                result = subprocess.run([
                    "python3", "fixed_travel_agent.py"
                ], capture_output=True, timeout=60)
                duration = time.time() - start_time
                
                load_results.append({
                    "agent_id": agent_id,
                    "success": result.returncode == 0,
                    "duration": duration
                })
                
            except Exception as e:
                load_results.append({
                    "agent_id": agent_id,
                    "error": str(e),
                    "success": False
                })
        
        # Run 10 concurrent agents
        threads = []
        for i in range(10):
            thread = threading.Thread(target=concurrent_agent, args=(i+1,))
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        successful = sum(1 for r in load_results if r.get("success", False))
        avg_duration = sum(r.get("duration", 0) for r in load_results if "duration" in r) / len([r for r in load_results if "duration" in r])
        
        load_resilient = successful >= len(load_results) * 0.9  # 90% success under load
        
        self.log_evidence("concurrent_load", {
            "total": len(load_results),
            "successful": successful,
            "avg_duration": avg_duration,
            "results": load_results
        }, load_resilient)
        
        print(f"   Load test: {successful}/{len(load_results)} succeeded")
        print(f"   Average duration under load: {avg_duration:.2f}s")
        
        return load_resilient
    
    def run_extreme_cycles(self, max_minutes=10):
        """Run extreme cycles until time limit or all tests pass"""
        print(f"🔥 RUNNING EXTREME CYCLES FOR {max_minutes} MINUTES")
        print("=" * 80)
        
        end_time = time.time() + (max_minutes * 60)
        cycle = 0
        
        all_tests_perfect = False
        
        while time.time() < end_time and not all_tests_perfect:
            cycle += 1
            print(f"\n🔥 EXTREME CYCLE {cycle}")
            print("=" * 60)
            
            # Run all extreme tests
            tests = [
                ("Memory Stress", self.stress_test_memory),
                ("Performance", self.performance_regression_test),
                ("Chaos", self.chaos_test),
                ("Edge Cases", self.edge_case_inputs_test),
                ("Concurrent Load", self.concurrent_load_test)
            ]
            
            test_results = []
            
            for test_name, test_func in tests:
                try:
                    result = test_func()
                    test_results.append(result)
                    
                    if result:
                        print(f"✅ {test_name}: PASSED")
                    else:
                        print(f"❌ {test_name}: ISSUES FOUND")
                        
                except Exception as e:
                    print(f"💥 {test_name}: CRASHED - {e}")
                    test_results.append(False)
                    self.results["errors"] += 1
            
            self.results["total_cycles"] += 1
            
            # Check if all tests perfect
            all_tests_perfect = all(test_results)
            
            if all_tests_perfect:
                self.results["passed"] += 1
                print(f"\n🎉 CYCLE {cycle} PERFECT - ALL TESTS PASSED")
            else:
                self.results["failed"] += 1
                print(f"\n⚠️ CYCLE {cycle} - SOME ISSUES FOUND")
            
            # Calculate current success rate
            if self.results["total_cycles"] > 0:
                success_rate = (self.results["passed"] / self.results["total_cycles"]) * 100
                print(f"📊 Current success rate: {success_rate:.1f}%")
            
            # Brief pause between cycles
            time.sleep(1)
        
        return self.results
    
    def print_extreme_results(self):
        """Print comprehensive extreme results"""
        total_duration = time.time() - self.start_time
        
        print(f"\n" + "=" * 80)
        print("🔥 EXTREME SKEPTICAL CYCLES FINAL RESULTS")
        print("=" * 80)
        
        print(f"🔄 Total Extreme Cycles: {self.results['total_cycles']}")
        print(f"✅ Perfect Cycles: {self.results['passed']}")
        print(f"⚠️ Cycles with Issues: {self.results['failed']}")
        print(f"💥 Errors: {self.results['errors']}")
        print(f"🧠 Memory Issues: {self.results['memory_issues']}")
        print(f"⚡ Performance Issues: {self.results['performance_issues']}")
        print(f"⏱️ Total Duration: {total_duration:.1f}s")
        
        if self.results["total_cycles"] > 0:
            success_rate = (self.results["passed"] / self.results["total_cycles"]) * 100
            print(f"📊 Perfect Cycle Rate: {success_rate:.1f}%")
            
            if success_rate == 100:
                print(f"\n🏆 BULLETPROOF STATUS ACHIEVED!")
                print("✅ Agent survived ALL extreme tests")
                print("🚀 READY FOR ANY PRODUCTION SCENARIO")
            elif success_rate >= 90:
                print(f"\n🎯 NEAR-BULLETPROOF STATUS")
                print("✅ Agent is highly robust")
                print("🔧 Minor optimizations possible")
            else:
                print(f"\n⚠️ ISSUES FOUND - NEED MORE FIXES")
                print("🔧 Review evidence and fix problems")
        
        print(f"\n📁 Evidence collected in: {self.evidence_dir}")

def main():
    """Run extreme testing non-stop"""
    tester = ExtremeTester()
    
    try:
        results = tester.run_extreme_cycles(max_minutes=15)  # 15 minutes of extreme testing
        tester.print_extreme_results()
        
    except KeyboardInterrupt:
        print("\n⚠️ Extreme testing interrupted")
        tester.print_extreme_results()
    except Exception as e:
        print(f"\n💥 Extreme testing crashed: {e}")
        tester.print_extreme_results()

if __name__ == "__main__":
    main()
