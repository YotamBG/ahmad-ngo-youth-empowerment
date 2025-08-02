#!/usr/bin/env python3
"""
MOBILE RESPONSIVE & READABILITY TESTING SUITE - 2025 STANDARDS
Tests Ahmad NGO website across all device breakpoints with visual verification
Based on latest mobile-first design best practices from research
"""

import os
import time
import json
import threading
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class MobileResponsiveTracker:
    def __init__(self):
        self.test_id = f"MOBILE_RESPONSIVE_{int(time.time())}"
        self.evidence_dir = f"MOBILE_EVIDENCE_{self.test_id}"
        os.makedirs(self.evidence_dir, exist_ok=True)
        
        # 2025 MOBILE BREAKPOINTS (based on research)
        self.device_configs = {
            "Mobile_Portrait_320": {"width": 320, "height": 568, "type": "mobile"},
            "Mobile_Portrait_360": {"width": 360, "height": 800, "type": "mobile"},  # Samsung Galaxy
            "Mobile_Portrait_375": {"width": 375, "height": 812, "type": "mobile"},  # iPhone X
            "Mobile_Portrait_390": {"width": 390, "height": 844, "type": "mobile"},  # iPhone 12
            "Mobile_Portrait_393": {"width": 393, "height": 873, "type": "mobile"},  # Pixel 6a
            "Mobile_Portrait_412": {"width": 412, "height": 915, "type": "mobile"},  # Galaxy Note
            "Tablet_Portrait_768": {"width": 768, "height": 1024, "type": "tablet"},
            "Tablet_Landscape_1024": {"width": 1024, "height": 768, "type": "tablet"},
            "Desktop_Small_1280": {"width": 1280, "height": 800, "type": "desktop"},
            "Desktop_Large_1920": {"width": 1920, "height": 1080, "type": "desktop"}
        }
        
        # 2025 READABILITY STANDARDS
        self.readability_standards = {
            "min_font_size": 16,  # Minimum for readability
            "mobile_min_font_size": 18,  # Research shows 18px+ for mobile
            "min_line_height": 1.5,  # WCAG standard
            "mobile_line_height": 1.7,  # Better for mobile reading
            "min_touch_target": 44,  # 44x44px minimum touch target
            "optimal_touch_target": 48,  # Optimal for fat fingers
            "max_line_length": 70,  # Characters per line for readability
            "min_contrast_ratio": 4.5  # WCAG AA standard
        }
        
        self.test_results = {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "critical_issues": [],
            "warnings": [],
            "device_results": {},
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"🔍 MOBILE RESPONSIVE TESTING SUITE - 2025 STANDARDS")
        print(f"📁 Evidence: {self.evidence_dir}")
        print(f"📱 Testing {len(self.device_configs)} device configurations")

    def setup_driver(self, width, height):
        """Setup Chrome driver with mobile emulation"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument(f'--window-size={width},{height}')
        
        # Mobile user agent for mobile devices
        if width <= 480:
            options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1')
        
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(width, height)
        return driver

    def test_device_responsiveness(self, device_name, config, url):
        """Test website responsiveness on specific device"""
        device_results = {
            "device": device_name,
            "config": config,
            "tests": {},
            "screenshot": None,
            "critical_issues": [],
            "warnings": []
        }
        
        print(f"\n📱 Testing {device_name} ({config['width']}x{config['height']})")
        
        driver = None
        try:
            driver = self.setup_driver(config['width'], config['height'])
            driver.get(url)
            
            # Wait for page load
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)  # Let CSS animations settle
            
            # Take screenshot
            screenshot_path = f"{self.evidence_dir}/{device_name}_screenshot.png"
            driver.save_screenshot(screenshot_path)
            device_results["screenshot"] = screenshot_path
            print(f"📸 Screenshot saved: {screenshot_path}")
            
            # Test viewport meta tag
            device_results["tests"]["viewport_meta"] = self.test_viewport_meta(driver)
            
            # Test font sizes and readability
            device_results["tests"]["font_readability"] = self.test_font_readability(driver, config)
            
            # Test touch targets (for mobile devices)
            if config['type'] == 'mobile':
                device_results["tests"]["touch_targets"] = self.test_touch_targets(driver)
            
            # Test navigation accessibility
            device_results["tests"]["navigation"] = self.test_navigation_mobile(driver, config)
            
            # Test content overflow
            device_results["tests"]["content_overflow"] = self.test_content_overflow(driver)
            
            # Test form usability
            device_results["tests"]["form_usability"] = self.test_form_usability(driver, config)
            
            # Test image responsiveness
            device_results["tests"]["image_responsiveness"] = self.test_image_responsiveness(driver)
            
            # Calculate overall score
            passed_tests = sum(1 for test in device_results["tests"].values() if test.get("passed", False))
            total_tests = len(device_results["tests"])
            device_results["score"] = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
            
            print(f"✅ {device_name}: {device_results['score']:.1f}% ({passed_tests}/{total_tests} tests passed)")
            
        except Exception as e:
            device_results["error"] = str(e)
            device_results["critical_issues"].append(f"Failed to load on {device_name}: {e}")
            print(f"❌ {device_name}: CRITICAL FAILURE - {e}")
            
        finally:
            if driver:
                driver.quit()
        
        return device_results

    def test_viewport_meta(self, driver):
        """Test if viewport meta tag is properly configured"""
        try:
            viewport_meta = driver.find_element(By.CSS_SELECTOR, 'meta[name="viewport"]')
            content = viewport_meta.get_attribute('content')
            
            # Check for essential viewport properties
            has_width_device = 'width=device-width' in content
            has_initial_scale = 'initial-scale=1' in content
            
            result = {
                "passed": has_width_device and has_initial_scale,
                "content": content,
                "has_width_device": has_width_device,
                "has_initial_scale": has_initial_scale
            }
            
            if not result["passed"]:
                result["issue"] = "Missing or improper viewport meta tag"
                
            return result
            
        except NoSuchElementException:
            return {
                "passed": False,
                "issue": "No viewport meta tag found",
                "recommendation": "Add: <meta name='viewport' content='width=device-width, initial-scale=1'>"
            }

    def test_font_readability(self, driver, config):
        """Test font sizes and readability standards"""
        results = {
            "passed": True,
            "issues": [],
            "elements_tested": 0
        }
        
        # Test different text elements
        selectors = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', '.lead', 'body', 'li', 'a', 'button']
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)[:3]  # Test first 3 of each type
                
                for element in elements:
                    if element.is_displayed():
                        # Get computed styles
                        font_size_str = driver.execute_script(
                            "return window.getComputedStyle(arguments[0]).fontSize;", element
                        )
                        line_height_str = driver.execute_script(
                            "return window.getComputedStyle(arguments[0]).lineHeight;", element
                        )
                        
                        font_size = float(font_size_str.replace('px', ''))
                        
                        # Check font size standards
                        min_font_size = (self.readability_standards['mobile_min_font_size'] 
                                       if config['type'] == 'mobile' 
                                       else self.readability_standards['min_font_size'])
                        
                        if font_size < min_font_size:
                            results["passed"] = False
                            results["issues"].append(f"{selector}: {font_size}px (min: {min_font_size}px)")
                        
                        # Check line height
                        if line_height_str != 'normal':
                            try:
                                line_height = float(line_height_str.replace('px', ''))
                                line_height_ratio = line_height / font_size
                                min_line_height = (self.readability_standards['mobile_line_height'] 
                                                 if config['type'] == 'mobile' 
                                                 else self.readability_standards['min_line_height'])
                                
                                if line_height_ratio < min_line_height:
                                    results["passed"] = False
                                    results["issues"].append(f"{selector}: line-height {line_height_ratio:.1f} (min: {min_line_height})")
                            except:
                                pass
                        
                        results["elements_tested"] += 1
                        
            except Exception as e:
                results["issues"].append(f"Error testing {selector}: {e}")
        
        return results

    def test_touch_targets(self, driver):
        """Test touch target sizes for mobile devices"""
        results = {
            "passed": True,
            "issues": [],
            "elements_tested": 0
        }
        
        # Test interactive elements
        selectors = ['button', 'a', 'input[type="submit"]', '.btn', '[onclick]']
        
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                
                for element in elements:
                    if element.is_displayed():
                        size = element.size
                        width = size['width']
                        height = size['height']
                        
                        min_target = self.readability_standards['min_touch_target']
                        
                        if width < min_target or height < min_target:
                            results["passed"] = False
                            results["issues"].append(f"{selector}: {width}x{height}px (min: {min_target}x{min_target}px)")
                        
                        results["elements_tested"] += 1
                        
            except Exception as e:
                results["issues"].append(f"Error testing {selector}: {e}")
        
        return results

    def test_navigation_mobile(self, driver, config):
        """Test mobile navigation functionality"""
        results = {
            "passed": True,
            "issues": [],
            "has_mobile_menu": False
        }
        
        try:
            # Check for mobile menu button
            mobile_menu_selectors = ['.hamburger', '.mobile-menu-toggle', '.nav-toggle', '[aria-label*="menu"]']
            
            for selector in mobile_menu_selectors:
                try:
                    menu_button = driver.find_element(By.CSS_SELECTOR, selector)
                    if menu_button.is_displayed():
                        results["has_mobile_menu"] = True
                        
                        # Test if menu button is clickable
                        try:
                            menu_button.click()
                            time.sleep(1)
                            results["menu_clickable"] = True
                        except:
                            results["menu_clickable"] = False
                            results["issues"].append("Mobile menu button not clickable")
                        
                        break
                except NoSuchElementException:
                    continue
            
            # Check navigation visibility on small screens
            if config['width'] <= 768:
                nav_elements = driver.find_elements(By.CSS_SELECTOR, 'nav, .nav, .navigation')
                for nav in nav_elements:
                    if nav.is_displayed():
                        nav_width = nav.size['width']
                        if nav_width > config['width']:
                            results["passed"] = False
                            results["issues"].append(f"Navigation width ({nav_width}px) exceeds screen width ({config['width']}px)")
            
        except Exception as e:
            results["issues"].append(f"Navigation test error: {e}")
        
        return results

    def test_content_overflow(self, driver):
        """Test for horizontal overflow issues"""
        results = {
            "passed": True,
            "issues": [],
            "elements_checked": 0
        }
        
        try:
            # Check body and main containers for horizontal scroll
            body_width = driver.execute_script("return document.body.scrollWidth;")
            window_width = driver.execute_script("return window.innerWidth;")
            
            if body_width > window_width:
                results["passed"] = False
                results["issues"].append(f"Horizontal overflow detected: content {body_width}px > viewport {window_width}px")
            
            # Check specific elements that commonly cause overflow
            overflow_selectors = ['img', '.container', '.row', 'table', 'pre', 'code']
            
            for selector in overflow_selectors:
                try:
                    elements = driver.find_elements(By.CSS_SELECTOR, selector)[:5]  # Test first 5
                    
                    for element in elements:
                        if element.is_displayed():
                            element_width = element.size['width']
                            if element_width > window_width:
                                results["passed"] = False
                                results["issues"].append(f"{selector}: width {element_width}px > viewport {window_width}px")
                            
                            results["elements_checked"] += 1
                            
                except Exception:
                    continue
                    
        except Exception as e:
            results["issues"].append(f"Overflow test error: {e}")
        
        return results

    def test_form_usability(self, driver, config):
        """Test form usability on mobile devices"""
        results = {
            "passed": True,
            "issues": [],
            "forms_tested": 0
        }
        
        try:
            forms = driver.find_elements(By.TAG_NAME, 'form')
            
            for form in forms:
                if form.is_displayed():
                    results["forms_tested"] += 1
                    
                    # Test input field sizes
                    inputs = form.find_elements(By.CSS_SELECTOR, 'input, textarea, select')
                    for input_elem in inputs:
                        if input_elem.is_displayed():
                            height = input_elem.size['height']
                            min_height = self.readability_standards['min_touch_target']
                            
                            if height < min_height:
                                results["passed"] = False
                                results["issues"].append(f"Input field too small: {height}px (min: {min_height}px)")
                    
                    # Test form button sizes (already covered in touch targets but double-check)
                    buttons = form.find_elements(By.CSS_SELECTOR, 'button, input[type="submit"]')
                    for button in buttons:
                        if button.is_displayed():
                            size = button.size
                            min_target = self.readability_standards['min_touch_target']
                            
                            if size['width'] < min_target or size['height'] < min_target:
                                results["passed"] = False
                                results["issues"].append(f"Form button too small: {size['width']}x{size['height']}px")
                                
        except Exception as e:
            results["issues"].append(f"Form usability test error: {e}")
        
        return results

    def test_image_responsiveness(self, driver):
        """Test if images are responsive"""
        results = {
            "passed": True,
            "issues": [],
            "images_tested": 0
        }
        
        try:
            images = driver.find_elements(By.TAG_NAME, 'img')[:10]  # Test first 10 images
            
            for img in images:
                if img.is_displayed():
                    results["images_tested"] += 1
                    
                    # Check if image has max-width: 100% or similar responsive styling
                    max_width = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).maxWidth;", img
                    )
                    width = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).width;", img
                    )
                    
                    # Check for responsive image styling
                    if max_width not in ['100%', '100vw'] and 'calc(' not in str(width):
                        # Check if image overflows container
                        img_width = img.size['width']
                        container = driver.execute_script("return arguments[0].parentElement;", img)
                        container_width = container.size['width'] if container else driver.execute_script("return window.innerWidth;")
                        
                        if img_width > container_width:
                            results["passed"] = False
                            results["issues"].append(f"Image overflow: {img_width}px > container {container_width}px")
                            
        except Exception as e:
            results["issues"].append(f"Image responsiveness test error: {e}")
        
        return results

    def run_comprehensive_test(self, url="http://localhost:8000"):
        """Run comprehensive mobile responsiveness test"""
        print(f"\n🚀 STARTING COMPREHENSIVE MOBILE RESPONSIVENESS TEST")
        print(f"🎯 Target URL: {url}")
        print(f"📋 Testing against 2025 mobile-first standards")
        
        start_time = time.time()
        
        # Test each device configuration
        for device_name, config in self.device_configs.items():
            device_result = self.test_device_responsiveness(device_name, config, url)
            self.test_results["device_results"][device_name] = device_result
            self.test_results["total_tests"] += 1
            
            if device_result.get("score", 0) >= 80:
                self.test_results["passed_tests"] += 1
            else:
                self.test_results["failed_tests"] += 1
                
            # Collect critical issues
            if device_result.get("critical_issues"):
                self.test_results["critical_issues"].extend(device_result["critical_issues"])
        
        # Generate comprehensive report
        self.generate_comprehensive_report()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"\n🏆 MOBILE RESPONSIVENESS TEST COMPLETE!")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"✅ Devices Passed: {self.test_results['passed_tests']}/{self.test_results['total_tests']}")
        print(f"❌ Critical Issues: {len(self.test_results['critical_issues'])}")
        
        return self.test_results

    def generate_comprehensive_report(self):
        """Generate detailed HTML report with all test results"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile Responsiveness Test Report - 2025 Standards</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .summary {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .device-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
        .device-card {{ background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #ccc; }}
        .device-card.passed {{ border-left-color: #4CAF50; }}
        .device-card.failed {{ border-left-color: #f44336; }}
        .screenshot {{ max-width: 100%; height: auto; border: 1px solid #ddd; }}
        .test-details {{ margin-top: 10px; }}
        .test-item {{ padding: 5px; margin: 3px 0; border-radius: 3px; }}
        .test-passed {{ background: #e8f5e8; color: #2e7d32; }}
        .test-failed {{ background: #ffeaea; color: #c62828; }}
        .critical-issues {{ background: #fff3cd; border: 1px solid #ffeaa7; padding: 15px; border-radius: 5px; }}
        .score {{ font-size: 24px; font-weight: bold; }}
        .score.good {{ color: #4CAF50; }}
        .score.poor {{ color: #f44336; }}
        .timestamp {{ color: #666; font-size: 12px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📱 Mobile Responsiveness Test Report</h1>
        <h2>2025 Standards Compliance</h2>
        <p class="timestamp">Generated: {self.test_results['timestamp']}</p>
    </div>
    
    <div class="summary">
        <h3>📊 Test Summary</h3>
        <p><strong>Total Devices Tested:</strong> {self.test_results['total_tests']}</p>
        <p><strong>Devices Passed (≥80%):</strong> {self.test_results['passed_tests']}</p>
        <p><strong>Devices Failed (<80%):</strong> {self.test_results['failed_tests']}</p>
        <p><strong>Overall Success Rate:</strong> {(self.test_results['passed_tests']/self.test_results['total_tests']*100):.1f}%</p>
    </div>
"""

        # Critical Issues Section
        if self.test_results['critical_issues']:
            html_content += """
    <div class="critical-issues">
        <h3>🚨 Critical Issues</h3>
        <ul>"""
            for issue in self.test_results['critical_issues'][:10]:  # Show top 10
                html_content += f"<li>{issue}</li>"
            html_content += "</ul></div>"

        # Device Results Grid
        html_content += '<div class="device-grid">'
        
        for device_name, result in self.test_results['device_results'].items():
            score = result.get('score', 0)
            status_class = 'passed' if score >= 80 else 'failed'
            score_class = 'good' if score >= 80 else 'poor'
            
            html_content += f"""
    <div class="device-card {status_class}">
        <h4>{device_name}</h4>
        <p><strong>Resolution:</strong> {result['config']['width']}x{result['config']['height']}</p>
        <p><strong>Type:</strong> {result['config']['type'].title()}</p>
        <div class="score {score_class}">{score:.1f}%</div>
"""
            
            # Screenshot
            if result.get('screenshot'):
                screenshot_filename = os.path.basename(result['screenshot'])
                html_content += f'<img src="{screenshot_filename}" alt="{device_name} screenshot" class="screenshot">'
            
            # Test Details
            html_content += '<div class="test-details">'
            for test_name, test_result in result.get('tests', {}).items():
                status = 'passed' if test_result.get('passed', False) else 'failed'
                html_content += f'<div class="test-item test-{status}">{test_name.replace("_", " ").title()}: {"✅" if status == "passed" else "❌"}</div>'
                
                # Show issues if any
                if test_result.get('issues'):
                    for issue in test_result['issues'][:3]:  # Show first 3 issues
                        html_content += f'<div style="font-size: 12px; color: #666; margin-left: 10px;">• {issue}</div>'
            
            html_content += '</div></div>'
        
        html_content += '</div></body></html>'
        
        # Save report
        report_path = f"{self.evidence_dir}/mobile_responsiveness_report.html"
        with open(report_path, 'w') as f:
            f.write(html_content)
        
        # Save JSON results
        json_path = f"{self.evidence_dir}/test_results.json"
        with open(json_path, 'w') as f:
            json.dump(self.test_results, f, indent=2, default=str)
        
        print(f"📋 Detailed report: {report_path}")
        print(f"📄 JSON results: {json_path}")

def main():
    """Main testing function"""
    print("🚀 MOBILE RESPONSIVENESS TESTING - 2025 STANDARDS")
    
    tracker = MobileResponsiveTracker()
    
    # Test local server
    test_url = "file:///home/yotambg/Documents/ahmad-ngo/index.html"
    
    print(f"🎯 Testing: {test_url}")
    print(f"📱 Based on 2025 mobile-first research:")
    print(f"   • 70%+ mobile traffic requires mobile-first design")
    print(f"   • Minimum 16px font size (18px+ for mobile)")
    print(f"   • 44x44px minimum touch targets")
    print(f"   • 1.5x line height for readability")
    print(f"   • Fluid grids and responsive images")
    
    # Run comprehensive test
    results = tracker.run_comprehensive_test(test_url)
    
    # Skeptical Analysis
    print(f"\n🔍 SKEPTICAL ANALYSIS:")
    if results['passed_tests'] < results['total_tests']:
        print(f"⚠️  WEBSITE FAILS MOBILE STANDARDS!")
        print(f"   • {results['failed_tests']} devices failed responsiveness tests")
        print(f"   • Critical issues found: {len(results['critical_issues'])}")
        print(f"   • Mobile users will have poor experience")
        print(f"   • SEO rankings will suffer")
        print(f"   • Conversion rates will drop")
    else:
        print(f"✅ WEBSITE MEETS 2025 MOBILE STANDARDS!")
        print(f"   • All devices pass responsiveness tests")
        print(f"   • Ready for mobile-first world")
    
    return len(results['critical_issues']) == 0

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n⚠️  Testing interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Critical testing error: {e}")
        exit(1) 