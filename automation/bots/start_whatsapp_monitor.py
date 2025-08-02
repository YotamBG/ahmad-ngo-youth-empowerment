#!/usr/bin/env python3
"""
🚀 WHATSAPP MONITOR LAUNCHER
Simple launcher for WhatsApp Web command monitoring
"""

import sys
import os
from pathlib import Path

# Add scripts directory to path
sys.path.append('scripts')

try:
    from whatsapp_monitor import WhatsAppCommandMonitor
    
    def main():
        print("🚀 LAUNCHING WHATSAPP COMMAND MONITOR")
        print("=" * 50)
        print("📱 Target Number: 052 339 6883 (or +972 52 339 6883)")
        print("🔄 Commands will be executed automatically")
        print("⏹️  Press Ctrl+C to stop monitoring")
        print("=" * 50)
        
        monitor = WhatsAppCommandMonitor()
        
        try:
            monitor.start_monitoring()
        except KeyboardInterrupt:
            print("\n⏹️ Monitor stopped by user")
        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            monitor.cleanup()
            print("👋 Goodbye!")

    if __name__ == "__main__":
        main()

except ImportError as e:
    print(f"❌ Import error: {e}")
    print("📦 Please ensure all dependencies are installed:")
    print("   pip3 install selenium selenium-stealth webdriver-manager")
    sys.exit(1) 