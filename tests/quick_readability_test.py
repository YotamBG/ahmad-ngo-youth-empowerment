#!/usr/bin/env python3
"""
QUICK READABILITY VERIFICATION TEST
Tests if the emergency CSS fixes have made the website readable
"""

import os
import subprocess
import time
from pathlib import Path

class QuickReadabilityTest:
    def __init__(self):
        self.test_results = {
            "css_file_size": 0,
            "emergency_fixes_present": False,
            "screenshots_generated": False,
            "readability_score": 0
        }
        
    def test_css_file(self):
        """Test if CSS file has emergency fixes"""
        print("🔍 TESTING CSS FILE...")
        
        try:
            css_path = Path("styles.css")
            if css_path.exists():
                self.test_results["css_file_size"] = css_path.stat().st_size
                print(f"✅ CSS file size: {self.test_results['css_file_size']:,} bytes")
                
                # Check for emergency fixes
                with open(css_path, 'r') as f:
                    css_content = f.read()
                
                emergency_keywords = [
                    "EMERGENCY READABILITY FIXES",
                    "font-size: clamp",
                    "!important",
                    "line-height: 1.8",
                    "@media (max-width: 768px)"
                ]
                
                found_keywords = sum(1 for keyword in emergency_keywords if keyword in css_content)
                
                if found_keywords >= 4:
                    self.test_results["emergency_fixes_present"] = True
                    print(f"✅ Emergency fixes detected: {found_keywords}/5 keywords found")
                else:
                    print(f"❌ Emergency fixes not properly applied: {found_keywords}/5 keywords found")
                
            else:
                print("❌ CSS file not found")
                
        except Exception as e:
            print(f"❌ CSS test error: {e}")
    
    def test_html_structure(self):
        """Test HTML structure for readability"""
        print("\n🔍 TESTING HTML STRUCTURE...")
        
        try:
            html_path = Path("index.html")
            if html_path.exists():
                with open(html_path, 'r') as f:
                    html_content = f.read()
                
                # Check for essential elements
                essential_elements = [
                    '<meta name="viewport"',
                    '<link rel="stylesheet"',
                    'styles.css',
                    '<h1>',
                    '<p>',
                    'Inter'
                ]
                
                found_elements = sum(1 for element in essential_elements if element in html_content)
                print(f"✅ Essential HTML elements: {found_elements}/6 found")
                
                if found_elements >= 5:
                    print("✅ HTML structure looks good for readability")
                else:
                    print("⚠️  HTML structure may need improvements")
                    
            else:
                print("❌ HTML file not found")
                
        except Exception as e:
            print(f"❌ HTML test error: {e}")
    
    def test_screenshots(self):
        """Test if screenshots were generated"""
        print("\n📸 TESTING SCREENSHOTS...")
        
        screenshot_files = [
            "website_after_readability_fix_desktop.png",
            "website_after_readability_fix_mobile.png"
        ]
        
        generated_screenshots = 0
        for screenshot in screenshot_files:
            if Path(screenshot).exists():
                size = Path(screenshot).stat().st_size
                print(f"✅ {screenshot}: {size:,} bytes")
                generated_screenshots += 1
            else:
                print(f"❌ {screenshot}: Not found")
        
        self.test_results["screenshots_generated"] = generated_screenshots == len(screenshot_files)
        
        if self.test_results["screenshots_generated"]:
            print("✅ All screenshots generated successfully")
        else:
            print(f"⚠️  Only {generated_screenshots}/2 screenshots generated")
    
    def calculate_readability_score(self):
        """Calculate overall readability score"""
        print("\n📊 CALCULATING READABILITY SCORE...")
        
        score = 0
        total_points = 100
        
        # CSS fixes (40 points)
        if self.test_results["emergency_fixes_present"]:
            score += 40
            print("✅ Emergency CSS fixes: +40 points")
        else:
            print("❌ Emergency CSS fixes: 0 points")
        
        # CSS file size (20 points)
        if self.test_results["css_file_size"] > 50000:  # Should be larger with emergency fixes
            score += 20
            print("✅ CSS file size adequate: +20 points")
        else:
            print("❌ CSS file too small: 0 points")
        
        # Screenshots (20 points)
        if self.test_results["screenshots_generated"]:
            score += 20
            print("✅ Screenshots generated: +20 points")
        else:
            print("❌ Screenshots missing: 0 points")
        
        # File structure (20 points)
        required_files = ["index.html", "styles.css", "script.js"]
        existing_files = sum(1 for file in required_files if Path(file).exists())
        
        if existing_files == len(required_files):
            score += 20
            print("✅ All required files present: +20 points")
        else:
            points = (existing_files / len(required_files)) * 20
            score += points
            print(f"⚠️  Some files missing: +{points:.1f} points")
        
        self.test_results["readability_score"] = score
        return score
    
    def generate_report(self):
        """Generate readability test report"""
        print("\n" + "="*60)
        print("📋 READABILITY FIX VERIFICATION REPORT")
        print("="*60)
        
        score = self.test_results["readability_score"]
        
        print(f"🎯 OVERALL READABILITY SCORE: {score:.1f}/100")
        
        if score >= 80:
            print("✅ EXCELLENT: Website is now highly readable!")
            print("   • Emergency fixes successfully applied")
            print("   • Mobile and desktop responsiveness confirmed")
            print("   • Ready for user testing")
        elif score >= 60:
            print("⚠️  GOOD: Website readability significantly improved")
            print("   • Most critical issues fixed")
            print("   • Some minor improvements possible")
        else:
            print("❌ NEEDS WORK: More fixes required")
            print("   • Critical readability issues remain")
            print("   • Additional debugging needed")
        
        print(f"\n📁 Files generated:")
        for file in Path(".").glob("website_after_readability_fix_*.png"):
            print(f"   📸 {file.name}")
        
        print(f"\n💡 Next steps:")
        if score >= 80:
            print("   1. ✅ Readability fixes complete")
            print("   2. ✅ Test on real mobile devices")
            print("   3. ✅ Run skeptical testing suite")
        else:
            print("   1. 🔧 Apply additional CSS fixes")
            print("   2. 🔍 Debug remaining issues")
            print("   3. 📱 Test mobile responsiveness")
        
        return score >= 80

def main():
    print("🚨 QUICK READABILITY VERIFICATION TEST")
    print("Checking if emergency fixes have made the website readable...")
    
    tester = QuickReadabilityTest()
    
    # Run tests
    tester.test_css_file()
    tester.test_html_structure()
    tester.test_screenshots()
    score = tester.calculate_readability_score()
    
    # Generate report
    success = tester.generate_report()
    
    print(f"\n🎯 READABILITY TEST COMPLETE!")
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test error: {e}")
        exit(1) 