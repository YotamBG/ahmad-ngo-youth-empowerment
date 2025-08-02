#!/usr/bin/env python3
"""
WEBSITE READABILITY DEBUGGER & FIXER
Identifies and fixes readability issues on Ahmad NGO website
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebsiteReadabilityFixer:
    def __init__(self):
        self.issues_found = []
        self.fixes_applied = []
        
    def setup_driver(self, width=1920, height=1080):
        """Setup Chrome driver for testing"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--window-size={width},{height}')
        
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(width, height)
        return driver

    def debug_readability_issues(self, url):
        """Debug and identify readability issues"""
        print("🔍 DEBUGGING WEBSITE READABILITY ISSUES...")
        
        driver = self.setup_driver()
        issues = []
        
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(2)
            
            # Take screenshot for debugging
            driver.save_screenshot("debug_before_fix.png")
            print("📸 Screenshot saved: debug_before_fix.png")
            
            # Check font sizes
            print("\n📝 CHECKING FONT SIZES...")
            text_elements = driver.find_elements(By.CSS_SELECTOR, 'p, h1, h2, h3, h4, h5, h6, li, a, span, div')
            
            for element in text_elements[:20]:  # Check first 20 elements
                if element.is_displayed() and element.text.strip():
                    font_size_str = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).fontSize;", element
                    )
                    color = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).color;", element
                    )
                    bg_color = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).backgroundColor;", element
                    )
                    
                    font_size = float(font_size_str.replace('px', ''))
                    
                    if font_size < 14:
                        issues.append(f"Font too small: {element.tag_name} - {font_size}px")
                        print(f"❌ Font too small: {element.tag_name} - {font_size}px")
                    
                    # Check if text is invisible or same color as background
                    if color == bg_color:
                        issues.append(f"Text invisible: same color as background")
                        print(f"❌ Text invisible: same color as background")
            
            # Check for overlapping elements
            print("\n🔍 CHECKING FOR OVERLAPPING ELEMENTS...")
            containers = driver.find_elements(By.CSS_SELECTOR, '.hero, .container, .section, main, nav')
            for container in containers:
                if container.is_displayed():
                    z_index = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).zIndex;", container
                    )
                    position = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).position;", container
                    )
                    
                    if z_index != 'auto' and position in ['absolute', 'fixed']:
                        print(f"⚠️  Potential overlap: {container.tag_name} with z-index {z_index}")
            
            # Check viewport meta tag
            print("\n📱 CHECKING MOBILE READABILITY...")
            try:
                viewport_meta = driver.find_element(By.CSS_SELECTOR, 'meta[name="viewport"]')
                viewport_content = viewport_meta.get_attribute('content')
                print(f"✅ Viewport meta: {viewport_content}")
            except:
                issues.append("Missing viewport meta tag")
                print("❌ Missing viewport meta tag")
            
            # Check for CSS that might be broken
            print("\n🎨 CHECKING CSS LOADING...")
            stylesheets = driver.find_elements(By.CSS_SELECTOR, 'link[rel="stylesheet"]')
            for stylesheet in stylesheets:
                href = stylesheet.get_attribute('href')
                print(f"📄 Stylesheet: {href}")
            
            self.issues_found = issues
            
        except Exception as e:
            print(f"❌ Error during debugging: {e}")
            self.issues_found.append(f"Debug error: {e}")
        
        finally:
            driver.quit()
        
        return self.issues_found

    def apply_emergency_fixes(self):
        """Apply emergency CSS fixes for readability"""
        print("\n🚨 APPLYING EMERGENCY READABILITY FIXES...")
        
        emergency_css = """
/* EMERGENCY READABILITY FIXES */
* {
    box-sizing: border-box !important;
}

html {
    font-size: 18px !important;
    scroll-behavior: smooth !important;
}

body {
    font-family: 'Inter', Arial, sans-serif !important;
    font-size: 18px !important;
    line-height: 1.8 !important;
    color: #1a1a1a !important;
    background: #ffffff !important;
    margin: 0 !important;
    padding: 0 !important;
    min-height: 100vh !important;
}

/* FORCE READABLE TEXT */
h1, h2, h3, h4, h5, h6 {
    color: #1a1a1a !important;
    font-weight: 700 !important;
    line-height: 1.3 !important;
    margin-bottom: 1rem !important;
    word-wrap: break-word !important;
}

h1 { font-size: clamp(2rem, 5vw, 3.5rem) !important; }
h2 { font-size: clamp(1.75rem, 4vw, 2.5rem) !important; }
h3 { font-size: clamp(1.5rem, 3vw, 2rem) !important; }
h4 { font-size: clamp(1.25rem, 2.5vw, 1.75rem) !important; }
h5 { font-size: clamp(1.125rem, 2vw, 1.5rem) !important; }
h6 { font-size: clamp(1rem, 1.5vw, 1.25rem) !important; }

p, li, a, span, div {
    font-size: clamp(1rem, 2vw, 1.25rem) !important;
    line-height: 1.8 !important;
    color: #1a1a1a !important;
    margin-bottom: 1rem !important;
    max-width: 70ch !important;
}

/* FORCE READABLE LINKS */
a {
    color: #006d77 !important;
    text-decoration: underline !important;
    font-weight: 500 !important;
}

a:hover, a:focus {
    color: #004d52 !important;
    text-decoration: underline !important;
}

/* FORCE READABLE BUTTONS */
button, .btn, input[type="submit"] {
    font-size: clamp(1rem, 2vw, 1.25rem) !important;
    padding: 12px 24px !important;
    background: #006d77 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    cursor: pointer !important;
    font-weight: 600 !important;
    min-height: 48px !important;
    text-decoration: none !important;
    display: inline-block !important;
}

button:hover, .btn:hover {
    background: #004d52 !important;
    color: white !important;
}

/* FORCE CONTAINER READABILITY */
.container, .section, main {
    max-width: 1200px !important;
    margin: 0 auto !important;
    padding: 20px !important;
    background: white !important;
}

/* NAVIGATION FIXES */
nav, .nav, .navigation {
    background: white !important;
    border-bottom: 1px solid #ddd !important;
    padding: 10px 20px !important;
}

nav a, .nav a, .navigation a {
    color: #1a1a1a !important;
    font-size: 1.125rem !important;
    font-weight: 500 !important;
    padding: 10px 15px !important;
    text-decoration: none !important;
}

nav a:hover, .nav a:hover {
    color: #006d77 !important;
    background: #f0f0f0 !important;
}

/* HERO SECTION FIXES */
.hero {
    background: linear-gradient(135deg, #006d77, #83c5be) !important;
    color: white !important;
    padding: 60px 20px !important;
    text-align: center !important;
    min-height: 60vh !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}

.hero h1, .hero h2, .hero h3, .hero h4, .hero h5, .hero h6 {
    color: white !important;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
}

.hero p, .hero div, .hero span {
    color: rgba(255,255,255,0.95) !important;
    font-size: clamp(1.125rem, 2.5vw, 1.5rem) !important;
    text-shadow: 1px 1px 2px rgba(0,0,0,0.3) !important;
}

/* FORM FIXES */
input, textarea, select {
    font-size: 1.125rem !important;
    padding: 12px !important;
    border: 2px solid #ddd !important;
    border-radius: 6px !important;
    background: white !important;
    color: #1a1a1a !important;
    min-height: 48px !important;
    width: 100% !important;
    max-width: 500px !important;
}

label {
    font-size: 1.125rem !important;
    font-weight: 600 !important;
    color: #1a1a1a !important;
    margin-bottom: 8px !important;
    display: block !important;
}

/* MOBILE RESPONSIVENESS */
@media (max-width: 768px) {
    html { font-size: 20px !important; }
    body { font-size: 20px !important; }
    
    h1 { font-size: clamp(2.5rem, 8vw, 4rem) !important; }
    h2 { font-size: clamp(2rem, 6vw, 3rem) !important; }
    h3 { font-size: clamp(1.75rem, 5vw, 2.5rem) !important; }
    
    p, li, div, span {
        font-size: clamp(1.25rem, 4vw, 1.75rem) !important;
        max-width: 100% !important;
    }
    
    button, .btn {
        font-size: 1.25rem !important;
        padding: 16px 32px !important;
        min-height: 56px !important;
    }
    
    .container, .section {
        padding: 15px !important;
    }
}

/* FORCE HIGH CONTRAST */
::selection {
    background: #006d77 !important;
    color: white !important;
}

/* FORCE FOCUS VISIBILITY */
*:focus {
    outline: 3px solid #006d77 !important;
    outline-offset: 2px !important;
}

/* REMOVE ANY POTENTIALLY PROBLEMATIC STYLES */
.overlay, .background-overlay {
    display: none !important;
}

/* ENSURE IMAGES DON'T BREAK LAYOUT */
img {
    max-width: 100% !important;
    height: auto !important;
    display: block !important;
    margin: 0 auto !important;
}
"""
        
        # Read current CSS file
        try:
            with open('styles.css', 'r') as f:
                current_css = f.read()
            
            # Append emergency fixes
            with open('styles.css', 'w') as f:
                f.write(current_css + '\n\n' + emergency_css)
            
            print("✅ Emergency CSS fixes applied to styles.css")
            self.fixes_applied.append("Emergency CSS fixes")
            
        except Exception as e:
            print(f"❌ Error applying CSS fixes: {e}")
        
        # Also create a separate emergency CSS file
        with open('emergency_fixes.css', 'w') as f:
            f.write(emergency_css)
        print("✅ Emergency fixes saved to emergency_fixes.css")

    def verify_fixes(self, url):
        """Verify that fixes have improved readability"""
        print("\n🔍 VERIFYING READABILITY FIXES...")
        
        driver = self.setup_driver()
        improvements = []
        
        try:
            driver.get(url)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(3)  # Let CSS load
            
            # Take screenshot after fixes
            driver.save_screenshot("debug_after_fix.png")
            print("📸 After-fix screenshot: debug_after_fix.png")
            
            # Check font sizes again
            readable_count = 0
            total_count = 0
            
            text_elements = driver.find_elements(By.CSS_SELECTOR, 'p, h1, h2, h3, h4, h5, h6, li, a')
            
            for element in text_elements[:15]:
                if element.is_displayed() and element.text.strip():
                    total_count += 1
                    font_size_str = driver.execute_script(
                        "return window.getComputedStyle(arguments[0]).fontSize;", element
                    )
                    font_size = float(font_size_str.replace('px', ''))
                    
                    if font_size >= 16:
                        readable_count += 1
            
            if total_count > 0:
                readability_score = (readable_count / total_count) * 100
                print(f"📊 Readability Score: {readability_score:.1f}% ({readable_count}/{total_count} elements readable)")
                
                if readability_score >= 80:
                    improvements.append(f"✅ Good readability: {readability_score:.1f}%")
                else:
                    improvements.append(f"⚠️  Needs work: {readability_score:.1f}%")
            
            # Test mobile view
            driver.set_window_size(375, 812)  # iPhone size
            time.sleep(2)
            driver.save_screenshot("debug_mobile_after_fix.png")
            print("📱 Mobile screenshot: debug_mobile_after_fix.png")
            
        except Exception as e:
            print(f"❌ Error during verification: {e}")
        
        finally:
            driver.quit()
        
        return improvements

def main():
    print("🚨 EMERGENCY WEBSITE READABILITY FIXER")
    print("=" * 50)
    
    fixer = WebsiteReadabilityFixer()
    url = "file:///home/yotambg/Documents/ahmad-ngo/index.html"
    
    # Step 1: Debug issues
    issues = fixer.debug_readability_issues(url)
    
    print(f"\n📋 ISSUES FOUND: {len(issues)}")
    for issue in issues:
        print(f"  • {issue}")
    
    # Step 2: Apply emergency fixes
    fixer.apply_emergency_fixes()
    
    # Step 3: Verify fixes
    improvements = fixer.verify_fixes(url)
    
    print(f"\n✅ FIXES APPLIED: {len(fixer.fixes_applied)}")
    for fix in fixer.fixes_applied:
        print(f"  • {fix}")
    
    print(f"\n📈 IMPROVEMENTS:")
    for improvement in improvements:
        print(f"  • {improvement}")
    
    print(f"\n🎯 WEBSITE READABILITY FIXING COMPLETE!")
    
    return len(issues) == 0

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Critical error: {e}")
        exit(1) 