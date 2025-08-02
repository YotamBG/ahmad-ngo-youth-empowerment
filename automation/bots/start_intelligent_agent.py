#!/usr/bin/env python3
"""
🤖 INTELLIGENT WHATSAPP AGENT LAUNCHER
Advanced AI-powered WhatsApp agent with three action modes:
1. Respond in WhatsApp - Direct intelligent responses
2. Execute on Cursor - Send commands to code editor
3. Observe and control Cursor and report - Screen automation with AI analysis
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
sys.path.append('scripts')

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'openai', 'selenium', 'selenium-stealth', 'webdriver-manager',
        'pyautogui', 'opencv-python', 'pillow', 'pygetwindow', 'keyboard'
    ]
    
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install with:")
        print(f"   pip3 install {' '.join(missing)}")
        return False
    
    return True

def check_openai_key():
    """Check if OpenAI API key is available"""
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("⚠️ OpenAI API key not found!")
        print("📝 Set your API key:")
        print("   export OPENAI_API_KEY='your-api-key-here'")
        return False
    return True

def create_directories():
    """Create necessary directories"""
    dirs = ['screenshots', 'logs', 'config']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)

def main():
    print("🤖 LAUNCHING INTELLIGENT WHATSAPP AGENT")
    print("=" * 60)
    print("🧠 AI-Powered Decision Making")
    print("📱 WhatsApp Web Integration") 
    print("🖥️ Screen Control & Automation")
    print("📝 Cursor Editor Integration")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies first")
        return 1
    
    # Check OpenAI API key
    if not check_openai_key():
        print("\n⚠️ Please set your OpenAI API key")
        return 1
    
    # Create directories
    create_directories()
    
    # Import and run the agent
    try:
        from intelligent_whatsapp_agent import IntelligentWhatsAppAgent
        
        print("\n🚀 Starting Intelligent Agent...")
        print("📋 Three Action Modes:")
        print("   1. 💬 Respond in WhatsApp - Direct AI responses")  
        print("   2. 📝 Execute on Cursor - Code editor commands")
        print("   3. 👁️ Observe & Control - Screen automation + analysis")
        print("\n⏹️ Press Ctrl+C to stop monitoring")
        print("=" * 60)
        
        agent = IntelligentWhatsAppAgent()
        
        try:
            agent.start_monitoring()
        except KeyboardInterrupt:
            print("\n⏹️ Agent stopped by user")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            agent.cleanup()
            print("👋 Goodbye!")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("📁 Make sure all files are in the scripts/ directory")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 