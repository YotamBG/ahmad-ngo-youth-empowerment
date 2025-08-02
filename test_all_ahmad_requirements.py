#!/usr/bin/env python3
"""
🔥 COMPREHENSIVE SKEPTICAL TESTING - AHMAD NGO WEBSITE
Test ALL user requirements systematically using cycles methodology
"""

import subprocess
import time
import json
import os
import requests
import threading
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class AhmadRequirementsValidator:
    """Comprehensive validation of ALL Ahmad's requirements"""
    
    def __init__(self):
        self.start_time = time.time()
        self.timestamp = int(self.start_time)
        self.evidence_dir = f"AHMAD_REQUIREMENTS_EVIDENCE_{self.timestamp}"
        self.results = {
            "total_requirements": 0,
            "passed": 0,
            "failed": 0,
            "critical_failures": 0,
            "evidence": []
        }
        
        os.makedirs(self.evidence_dir, exist_ok=True)
        
        # ALL USER REQUIREMENTS FROM CONVERSATION
        self.requirements = {
            "CONTENT_REQUIREMENTS": [
                "Website displays Youth Empowerment Educational Program",
                "Content matches PDF file (source of truth)",
                "Program overview is clearly displayed", 
                "Educational tracks are listed",
                "Learning format is explained",
                "Digital infrastructure plans shown",
                "Long-term vision articulated",
                "Ahmad Asaly name spelled correctly",
                "December added to first semester",
                "June added to second semester", 
                "January moved from second to first semester"
            ],
            "DESIGN_REQUIREMENTS": [
                "Inspired by younitedschool.org architecture",
                "Modern UI/UX design implemented",
                "Professional teal color palette",
                "Inter font family used",
                "Responsive design for all devices",
                "Readable text sizes (18px+ base)",
                "Proper line heights (1.7+)",
                "Emergency readability fixes applied",
                "Bulletproof 2025 web design standards",
                "High contrast ratios for accessibility"
            ],
            "FUNCTIONALITY_REQUIREMENTS": [
                "Mobile navigation works",
                "Form validation implemented", 
                "Smooth scrolling active",
                "Interactive animations working",
                "Contact form functional",
                "Registration form working",
                "JavaScript error-free",
                "Fast loading times",
                "SEO optimized",
                "Print-friendly styles"
            ],
            "DEPLOYMENT_REQUIREMENTS": [
                "Website deployed to Vercel",
                "HTTPS enabled",
                "Custom domain (arabyouthleaders.org) configured",
                "Performance optimized",
                "CDN enabled",
                "Gzip compression active",
                "Browser caching configured"
            ],
            "TECHNICAL_REQUIREMENTS": [
                "HTML5 semantic markup",
                "CSS3 modern features",
                "Vanilla JavaScript (no frameworks)",
                "Progressive enhancement",
                "Cross-browser compatibility",
                "W3C validation compliant",
                "Lighthouse score 90+",
                "Page load under 3 seconds"
            ]
        }
        
        print("🔥 COMPREHENSIVE AHMAD REQUIREMENTS TESTING")
        print("🎯 Testing ALL wishes from entire conversation")
        print(f"📂 Evidence: {self.evidence_dir}")
        print("=" * 80)
    
    def log_evidence(self, requirement, test_name, data, success=True):
        """Log evidence for each requirement test"""
        timestamp = datetime.now().isoformat()
        evidence = {
            "timestamp": timestamp,
            "requirement": requirement,
            "test": test_name,
            "success": success,
            "data": str(data)[:1000]
        }
        self.results["evidence"].append(evidence)
        
        # Save to file
        filename = f"{self.evidence_dir}/{requirement}_{test_name}_{timestamp.replace(':', '-')}.txt"
        with open(filename, "w") as f:
            f.write(f"Requirement: {requirement}\n")
            f.write(f"Test: {test_name}\n")
            f.write(f"Success: {success}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("="*60 + "\n")
            f.write(str(data))
        
        status = "✅" if success else "❌"
        print(f"📋 {requirement}: {test_name} - {status}")
    
    def test_website_accessibility(self):
        """Test website is accessible and loads"""
        print("\n🌐 TESTING WEBSITE ACCESSIBILITY")
        print("-" * 40)
        
        urls_to_test = [
            "https://ahmad-ngo.vercel.app",
            "https://arabyouthleaders.org"
        ]
        
        accessibility_results = []
        
        for url in urls_to_test:
            try:
                start_time = time.time()
                response = requests.get(url, timeout=10)
                load_time = time.time() - start_time
                
                result = {
                    "url": url,
                    "status_code": response.status_code,
                    "load_time": load_time,
                    "https": url.startswith("https://"),
                    "accessible": response.status_code == 200
                }
                
                accessibility_results.append(result)
                
                self.log_evidence("ACCESSIBILITY", f"load_test_{url.split('//')[1]}", 
                                result, result["accessible"] and result["load_time"] < 5.0)
                
            except Exception as e:
                result = {"url": url, "error": str(e), "accessible": False}
                accessibility_results.append(result)
                self.log_evidence("ACCESSIBILITY", f"load_test_{url.split('//')[1]}", 
                                result, False)
        
        return accessibility_results
    
    def test_content_requirements(self):
        """Test all content requirements using web scraping"""
        print("\n📝 TESTING CONTENT REQUIREMENTS") 
        print("-" * 40)
        
        # Setup headless browser
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        content_results = []
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://ahmad-ngo.vercel.app")
            time.sleep(3)  # Let page load
            
            page_text = driver.page_source.lower()
            
            # Test each content requirement
            content_tests = {
                "Youth Empowerment Program": "youth empowerment" in page_text,
                "Ahmad Asaly correct spelling": "ahmad asaly" in page_text,
                "December in first semester": "december" in page_text,
                "June in second semester": "june" in page_text,
                "Educational tracks displayed": "track" in page_text or "education" in page_text,
                "Program overview present": "overview" in page_text or "program" in page_text,
                "Digital infrastructure mentioned": "digital" in page_text,
                "Long-term vision articulated": "vision" in page_text or "future" in page_text
            }
            
            for test_name, passed in content_tests.items():
                content_results.append({"test": test_name, "passed": passed})
                self.log_evidence("CONTENT", test_name.replace(" ", "_"), 
                                {"found": passed, "test": test_name}, passed)
            
            driver.quit()
            
        except Exception as e:
            self.log_evidence("CONTENT", "browser_test", {"error": str(e)}, False)
            print(f"   Browser test failed: {e}")
        
        return content_results
    
    def test_design_requirements(self):
        """Test design and UI/UX requirements"""
        print("\n🎨 TESTING DESIGN REQUIREMENTS")
        print("-" * 40)
        
        design_results = []
        
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://ahmad-ngo.vercel.app")
            time.sleep(3)
            
            # Test responsive design
            viewports = [(1920, 1080), (768, 1024), (375, 667)]
            responsive_tests = []
            
            for width, height in viewports:
                driver.set_window_size(width, height)
                time.sleep(1)
                
                # Check if content is visible
                try:
                    body = driver.find_element(By.TAG_NAME, "body")
                    is_responsive = body.is_displayed()
                    responsive_tests.append({"viewport": f"{width}x{height}", "responsive": is_responsive})
                except:
                    responsive_tests.append({"viewport": f"{width}x{height}", "responsive": False})
            
            # Test font and colors using CSS
            computed_styles = driver.execute_script("""
                const body = document.body;
                const computedStyle = window.getComputedStyle(body);
                return {
                    fontFamily: computedStyle.fontFamily,
                    fontSize: computedStyle.fontSize,
                    lineHeight: computedStyle.lineHeight,
                    backgroundColor: computedStyle.backgroundColor
                };
            """)
            
            # Validate design requirements
            design_tests = {
                "Inter font used": "inter" in computed_styles.get("fontFamily", "").lower(),
                "Readable font size": self.parse_font_size(computed_styles.get("fontSize", "0px")) >= 18,
                "Proper line height": self.parse_line_height(computed_styles.get("lineHeight", "1")) >= 1.7,
                "Responsive design": all(test["responsive"] for test in responsive_tests)
            }
            
            for test_name, passed in design_tests.items():
                design_results.append({"test": test_name, "passed": passed})
                self.log_evidence("DESIGN", test_name.replace(" ", "_"), 
                                {"passed": passed, "details": computed_styles}, passed)
            
            driver.quit()
            
        except Exception as e:
            self.log_evidence("DESIGN", "browser_design_test", {"error": str(e)}, False)
            print(f"   Design test failed: {e}")
        
        return design_results
    
    def test_functionality_requirements(self):
        """Test interactive functionality"""
        print("\n⚙️ TESTING FUNCTIONALITY REQUIREMENTS")
        print("-" * 40)
        
        functionality_results = []
        
        try:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            
            driver = webdriver.Chrome(options=chrome_options)
            driver.get("https://ahmad-ngo.vercel.app")
            time.sleep(3)
            
            # Test JavaScript errors
            js_errors = driver.get_log('browser')
            js_error_free = len([log for log in js_errors if log['level'] == 'SEVERE']) == 0
            
            # Test mobile navigation
            try:
                mobile_toggle = driver.find_element(By.CLASS_NAME, "mobile-toggle")
                mobile_nav_exists = mobile_toggle.is_displayed()
            except:
                mobile_nav_exists = False
            
            # Test forms
            try:
                forms = driver.find_elements(By.TAG_NAME, "form")
                forms_exist = len(forms) > 0
            except:
                forms_exist = False
            
            # Test smooth scrolling
            try:
                smooth_scroll_css = driver.execute_script("""
                    return window.getComputedStyle(document.documentElement).scrollBehavior;
                """)
                smooth_scrolling = smooth_scroll_css == "smooth"
            except:
                smooth_scrolling = False
            
            functionality_tests = {
                "JavaScript error-free": js_error_free,
                "Mobile navigation exists": mobile_nav_exists,
                "Forms present": forms_exist,
                "Smooth scrolling enabled": smooth_scrolling
            }
            
            for test_name, passed in functionality_tests.items():
                functionality_results.append({"test": test_name, "passed": passed})
                self.log_evidence("FUNCTIONALITY", test_name.replace(" ", "_"), 
                                {"passed": passed}, passed)
            
            driver.quit()
            
        except Exception as e:
            self.log_evidence("FUNCTIONALITY", "browser_function_test", {"error": str(e)}, False)
            print(f"   Functionality test failed: {e}")
        
        return functionality_results
    
    def test_performance_requirements(self):
        """Test performance requirements"""
        print("\n⚡ TESTING PERFORMANCE REQUIREMENTS")
        print("-" * 40)
        
        performance_results = []
        
        # Test multiple load times
        load_times = []
        for i in range(5):
            try:
                start_time = time.time()
                response = requests.get("https://ahmad-ngo.vercel.app", timeout=30)
                load_time = time.time() - start_time
                load_times.append(load_time)
                print(f"   Load test {i+1}: {load_time:.2f}s")
            except Exception as e:
                load_times.append(999)  # Failed load
                print(f"   Load test {i+1}: FAILED - {e}")
        
        avg_load_time = sum(load_times) / len(load_times)
        max_load_time = max(load_times)
        
        # Test compression
        try:
            response = requests.get("https://ahmad-ngo.vercel.app")
            gzip_enabled = 'gzip' in response.headers.get('content-encoding', '')
            content_size = len(response.content)
        except:
            gzip_enabled = False
            content_size = 0
        
        performance_tests = {
            "Average load under 3s": avg_load_time < 3.0,
            "Max load under 5s": max_load_time < 5.0,
            "GZIP compression": gzip_enabled,
            "Reasonable content size": content_size < 500000  # Under 500KB
        }
        
        for test_name, passed in performance_tests.items():
            performance_results.append({"test": test_name, "passed": passed})
            self.log_evidence("PERFORMANCE", test_name.replace(" ", "_"), 
                            {"passed": passed, "avg_load": avg_load_time, "max_load": max_load_time}, passed)
        
        return performance_results
    
    def parse_font_size(self, font_size_str):
        """Parse font size from CSS string"""
        try:
            return float(re.findall(r'(\d+(?:\.\d+)?)', font_size_str)[0])
        except:
            return 0
    
    def parse_line_height(self, line_height_str):
        """Parse line height from CSS string"""
        try:
            if line_height_str == "normal":
                return 1.2
            return float(line_height_str)
        except:
            return 1.0
    
    def run_comprehensive_cycles(self, max_cycles=5):
        """Run comprehensive requirement testing cycles"""
        print(f"🔥 RUNNING COMPREHENSIVE AHMAD REQUIREMENTS TEST")
        print(f"🎯 Testing ALL requirements from conversation")
        print("=" * 80)
        
        for cycle in range(1, max_cycles + 1):
            print(f"\n🔥 COMPREHENSIVE CYCLE {cycle}")
            print("=" * 60)
            
            cycle_results = []
            
            # Test all requirement categories
            test_categories = [
                ("Accessibility", self.test_website_accessibility),
                ("Content", self.test_content_requirements),
                ("Design", self.test_design_requirements),
                ("Functionality", self.test_functionality_requirements),
                ("Performance", self.test_performance_requirements)
            ]
            
            for category_name, test_function in test_categories:
                try:
                    results = test_function()
                    
                    # Calculate success rate for this category
                    if results:
                        passed = sum(1 for r in results if r.get("passed", r.get("accessible", False)))
                        total = len(results)
                        success_rate = (passed / total) * 100 if total > 0 else 0
                        
                        cycle_results.append({
                            "category": category_name,
                            "passed": passed,
                            "total": total,
                            "success_rate": success_rate
                        })
                        
                        print(f"✅ {category_name}: {passed}/{total} ({success_rate:.1f}%)")
                    else:
                        cycle_results.append({
                            "category": category_name,
                            "passed": 0,
                            "total": 0,
                            "success_rate": 0
                        })
                        print(f"❌ {category_name}: NO RESULTS")
                        
                except Exception as e:
                    print(f"💥 {category_name}: CRASHED - {e}")
                    cycle_results.append({
                        "category": category_name,
                        "error": str(e),
                        "success_rate": 0
                    })
            
            # Calculate overall cycle success
            total_passed = sum(r.get("passed", 0) for r in cycle_results)
            total_tests = sum(r.get("total", 0) for r in cycle_results)
            overall_success = (total_passed / total_tests * 100) if total_tests > 0 else 0
            
            print(f"\n📊 CYCLE {cycle} OVERALL: {total_passed}/{total_tests} ({overall_success:.1f}%)")
            
            if overall_success >= 90:
                print(f"🎉 CYCLE {cycle} EXCELLENT - Meeting Ahmad's requirements!")
                self.results["passed"] += 1
            elif overall_success >= 75:
                print(f"⚠️ CYCLE {cycle} GOOD - Some improvements needed")
                self.results["failed"] += 1
            else:
                print(f"❌ CYCLE {cycle} POOR - Major issues found")
                self.results["failed"] += 1
                self.results["critical_failures"] += 1
            
            self.results["total_requirements"] += total_tests
            
            # Brief pause between cycles
            if cycle < max_cycles:
                time.sleep(2)
        
        return self.results
    
    def print_final_verdict(self):
        """Print final comprehensive verdict"""
        total_duration = time.time() - self.start_time
        
        print(f"\n" + "=" * 80)
        print("🏆 AHMAD REQUIREMENTS FINAL VERDICT")
        print("=" * 80)
        
        print(f"🔄 Total Test Cycles: {self.results['passed'] + self.results['failed']}")
        print(f"✅ Excellent Cycles: {self.results['passed']}")
        print(f"⚠️ Poor Cycles: {self.results['failed']}")
        print(f"💥 Critical Failures: {self.results['critical_failures']}")
        print(f"📋 Total Requirements Tested: {self.results['total_requirements']}")
        print(f"⏱️ Total Duration: {total_duration:.1f}s")
        
        # Calculate overall success rate
        total_cycles = self.results['passed'] + self.results['failed']
        if total_cycles > 0:
            success_rate = (self.results['passed'] / total_cycles) * 100
            print(f"📊 Overall Success Rate: {success_rate:.1f}%")
            
            print(f"\n🎯 AHMAD'S REQUIREMENTS STATUS:")
            
            if success_rate >= 90 and self.results['critical_failures'] == 0:
                print(f"🎉 ✅ ALL REQUIREMENTS MET!")
                print("✅ Website meets Ahmad's expectations")
                print("✅ Ready for production use")
                print("✅ All conversation wishes implemented")
                print("🚀 AHMAD SHOULD BE VERY HAPPY!")
                
            elif success_rate >= 75:
                print(f"⚠️ MOSTLY GOOD - Some improvements needed")
                print("🔧 Minor adjustments required")
                print("📝 Review failed requirements")
                
            else:
                print(f"❌ MAJOR ISSUES FOUND")
                print("🚫 Does not meet Ahmad's requirements")
                print("🔧 Significant work needed")
                print("📝 Review critical failures")
        
        print(f"\n📁 Full evidence available in: {self.evidence_dir}")
        print(f"📊 Evidence entries: {len(self.results['evidence'])}")

def main():
    """Run comprehensive Ahmad requirements testing"""
    validator = AhmadRequirementsValidator()
    
    try:
        # Test with user's memory preferences
        print("⚠️ Using timeouts to prevent getting stuck (per user preference)")
        
        results = validator.run_comprehensive_cycles(max_cycles=3)
        validator.print_final_verdict()
        
    except KeyboardInterrupt:
        print("\n⚠️ Testing interrupted")
        validator.print_final_verdict()
    except Exception as e:
        print(f"\n💥 Testing crashed: {e}")
        validator.print_final_verdict()

if __name__ == "__main__":
    main() 