#!/usr/bin/env python3
"""
🚀 WHATSAPP BOT LAUNCHER
Simple launcher with dependency checking and setup guidance
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}")
    return True

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'selenium',
        'webdriver_manager'
    ]
    
    optional_packages = [
        'openai',
        'pyautogui', 
        'cv2',
        'PIL'
    ]
    
    missing_required = []
    missing_optional = []
    
    print("\n📦 Checking dependencies...")
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package}")
        except ImportError:
            missing_required.append(package)
            print(f"   ❌ {package} (required)")
    
    for package in optional_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"   ✅ {package} (optional)")
        except ImportError:
            missing_optional.append(package)
            print(f"   ⚠️ {package} (optional)")
    
    if missing_required:
        print(f"\n❌ Missing required packages: {', '.join(missing_required)}")
        print("📥 Install with:")
        print("   pip3 install -r requirements_bot.txt")
        return False
    
    if missing_optional:
        print(f"\n⚠️ Missing optional packages: {', '.join(missing_optional)}")
        print("💡 For full functionality, install with:")
        print("   pip3 install -r requirements_bot.txt")
    
    return True

def check_chrome():
    """Check if Chrome is installed"""
    try:
        result = subprocess.run(['google-chrome', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Chrome: {result.stdout.strip()}")
            return True
    except:
        pass
    
    try:
        result = subprocess.run(['chromium-browser', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Chromium: {result.stdout.strip()}")
            return True
    except:
        pass
    
    print("❌ Chrome/Chromium not found")
    print("📥 Install Chrome:")
    print("   sudo apt update && sudo apt install google-chrome-stable")
    return False

def check_openai_key():
    """Check if OpenAI API key is set"""
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("✅ OpenAI API key found")
        return True
    else:
        print("⚠️ OpenAI API key not found")
        print("💡 For AI features, set your API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False

def setup_environment():
    """Create necessary directories"""
    directories = ['screenshots', 'whatsapp_session', 'logs']
    
    print("\n📁 Setting up directories...")
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"   ✅ {directory}/")

def print_usage_guide():
    """Print usage instructions"""
    print("\n" + "="*60)
    print("🤖 WHATSAPP BOT USAGE GUIDE")
    print("="*60)
    print("""
🎯 Three Action Modes:

1. 💬 RESPOND MODE
   Send: "Hello", "How are you?", "Status", "Help"
   → Bot responds with AI-generated or rule-based replies

2. 📝 EXECUTE MODE  
   Send: "Open cursor", "Git status", "Run terminal"
   → Bot executes commands on your system

3. 👁️ OBSERVE MODE
   Send: "Screenshot", "Check screen", "Analyze display"
   → Bot takes screenshots and analyzes your screen

📱 Target Number: 052 339 6883 (customizable in code)

🔧 First Run:
   1. Bot opens Chrome with WhatsApp Web
   2. Scan QR code with your phone (one time only)
   3. Session is saved for future runs
   4. Bot starts monitoring messages

⚠️ Important:
   - Keep Chrome window open while bot runs
   - Press Ctrl+C to stop monitoring
   - Session data is saved in whatsapp_session/

💡 Optional Features:
   - Set OPENAI_API_KEY for AI responses
   - Install screen control libraries for automation
   - Use selenium-stealth to avoid detection
""")
    print("="*60)

def main():
    """Main launcher function"""
    print("🚀 WHATSAPP BOT LAUNCHER")
    print("=" * 60)
    
    # Check system requirements
    if not check_python_version():
        return 1
    
    if not check_dependencies():
        return 1
    
    if not check_chrome():
        return 1
    
    # Optional checks
    check_openai_key()
    
    # Setup environment
    setup_environment()
    
    # Print usage guide
    print_usage_guide()
    
    # Ask to launch
    try:
        launch = input("\n🚀 Launch WhatsApp bot now? (y/N): ").lower().strip()
        
        if launch in ['y', 'yes']:
            print("\n🎯 Starting WhatsApp bot...")
            
            # Import and run the bot
            try:
                from simple_whatsapp_bot import SimpleWhatsAppBot
                
                bot = SimpleWhatsAppBot()
                bot.start_monitoring()
                
            except ImportError as e:
                print(f"❌ Import error: {e}")
                print("📁 Make sure simple_whatsapp_bot.py is in the same directory")
                return 1
            except KeyboardInterrupt:
                print("\n👋 Bot stopped by user")
            except Exception as e:
                print(f"❌ Error: {e}")
                return 1
        else:
            print("👋 Bot not launched. Run again when ready!")
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 