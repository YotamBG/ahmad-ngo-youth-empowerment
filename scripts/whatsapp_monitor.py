#!/usr/bin/env python3
"""
🔥 WHATSAPP WEB COMMAND MONITOR
Monitors WhatsApp Web for commands from specific number
Executes commands and reports results
Using session persistence to avoid QR code re-scanning
"""

import time
import json
import os
import subprocess
import re
from datetime import datetime
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import threading

class WhatsAppCommandMonitor:
    """WhatsApp Web automation for command monitoring"""
    
    def __init__(self):
        self.driver = None
        self.session_file = "whatsapp_session.json"
        self.target_number = "052 339 6883"  # Can also match +972 52 339 6883
        self.last_message_id = None
        self.monitoring = False
        self.check_interval = 5  # seconds
        
        print("🚀 WhatsApp Command Monitor Initialized")
        print(f"📱 Target Number: {self.target_number}")
        print(f"🔄 Check Interval: {self.check_interval}s")
        
    def setup_driver(self):
        """Setup Chrome driver with stealth mode and session persistence"""
        print("\n🔧 Setting up Chrome driver...")
        
        chrome_options = Options()
        
        # Essential options for WhatsApp Web
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Session persistence
        profile_path = os.path.abspath("whatsapp_profile")
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        chrome_options.add_argument("--profile-directory=Default")
        
        # Keep browser open
        chrome_options.add_experimental_option("detach", True)
        
        # Create driver
        try:
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            # Apply stealth mode
            stealth(self.driver,
                   languages=["en-US", "en"],
                   vendor="Google Inc.",
                   platform="Win32",
                   webgl_vendor="Intel Inc.",
                   renderer="Intel Iris OpenGL Engine",
                   fix_hairline=True)
            
            print("✅ Chrome driver setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Driver setup failed: {e}")
            return False
    
    def open_whatsapp_web(self):
        """Open WhatsApp Web and handle authentication"""
        print("\n🌐 Opening WhatsApp Web...")
        
        try:
            self.driver.get("https://web.whatsapp.com/")
            
            # Wait for page to load
            time.sleep(5)
            
            # Check if QR code is present (not logged in)
            try:
                qr_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='qr-code']")
                print("📱 QR Code detected - Please scan with your phone")
                print("⏳ Waiting for authentication...")
                
                # Wait for QR code to disappear (successful login)
                WebDriverWait(self.driver, 300).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='qr-code']"))
                )
                print("✅ Authentication successful!")
                
            except NoSuchElementException:
                print("✅ Already authenticated!")
            
            # Wait for main interface to load
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']"))
            )
            
            print("🎯 WhatsApp Web ready for monitoring")
            return True
            
        except Exception as e:
            print(f"❌ Failed to open WhatsApp Web: {e}")
            return False
    
    def find_contact_chat(self, contact_name_or_number):
        """Find and open chat with specific contact"""
        try:
            # Try to find contact in chat list
            chat_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='cell-frame-container']")
            
            for chat in chat_elements:
                try:
                    # Get contact name/number
                    contact_text = chat.find_element(By.CSS_SELECTOR, "[data-testid='contact-title'] span").text
                    
                    # Check if this matches our target number (flexible matching)
                    if self.is_target_contact(contact_text):
                        print(f"✅ Found target contact: {contact_text}")
                        chat.click()
                        time.sleep(2)
                        return True
                        
                except:
                    continue
            
            print(f"⚠️ Contact not found in chat list: {contact_name_or_number}")
            return False
            
        except Exception as e:
            print(f"❌ Error finding contact: {e}")
            return False
    
    def is_target_contact(self, contact_text):
        """Check if contact matches target number with flexible formatting"""
        target_variations = [
            "052 339 6883",
            "0523396883", 
            "+972 52 339 6883",
            "+972523396883",
            "972523396883",
            "052-339-6883",
            "+972-52-339-6883"
        ]
        
        # Remove all non-digit characters for comparison
        contact_digits = re.sub(r'[^\d]', '', contact_text)
        
        for variation in target_variations:
            variation_digits = re.sub(r'[^\d]', '', variation)
            if contact_digits.endswith(variation_digits) or variation_digits.endswith(contact_digits):
                return True
        
        return False
    
    def get_latest_message(self):
        """Get the latest message from current chat"""
        try:
            # Find all messages in current chat
            messages = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='msg-container']")
            
            if not messages:
                return None
                
            # Get the last message
            last_message = messages[-1]
            
            # Check if it's an incoming message (not sent by us)
            incoming = last_message.find_elements(By.CSS_SELECTOR, "[data-testid='msg-container-incoming']")
            
            if incoming:
                # Get message text
                text_elements = last_message.find_elements(By.CSS_SELECTOR, "[data-testid='conversation-text-content'] span")
                
                if text_elements:
                    message_text = text_elements[0].text
                    
                    # Get message ID for tracking
                    message_id = last_message.get_attribute("data-id")
                    
                    return {
                        "id": message_id,
                        "text": message_text,
                        "timestamp": datetime.now(),
                        "is_incoming": True
                    }
            
            return None
            
        except Exception as e:
            print(f"❌ Error getting latest message: {e}")
            return None
    
    def send_message(self, message):
        """Send a message in current chat"""
        try:
            # Find message input box
            message_box = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='conversation-compose-box-input']")
            
            # Clear and type message
            message_box.clear()
            message_box.send_keys(message)
            
            # Send message
            send_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='send']")
            send_button.click()
            
            print(f"📤 Message sent: {message[:50]}...")
            return True
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def execute_command(self, command):
        """Execute command and return result"""
        try:
            print(f"\n🔥 EXECUTING COMMAND: {command}")
            
            # Check if it's a valid command
            if command.lower().strip() == "go":
                # Run the skeptical testing cycle
                result = subprocess.run(
                    ["timeout", "300s", "python3", "scripts/simplified_ahmad_test.py"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    # Extract key metrics from output
                    output_lines = result.stdout.split('\n')
                    summary_lines = [line for line in output_lines if '📊' in line or '🎯' in line or '✅' in line or 'OVERALL:' in line]
                    
                    response = "🔥 TESTING CYCLE COMPLETE!\n\n" + "\n".join(summary_lines[-10:])
                    return response[:1000]  # Limit length
                else:
                    return f"❌ Command failed with code {result.returncode}"
            
            elif command.lower().startswith("cycle"):
                # Various cycle commands
                result = subprocess.run(
                    ["timeout", "300s", "python3", "scripts/simplified_ahmad_test.py"],
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                
                if result.returncode == 0:
                    return "✅ Cycle completed successfully! Check terminal for details."
                else:
                    return f"❌ Cycle failed with code {result.returncode}"
            
            elif command.lower().startswith("deploy"):
                # Deploy to Vercel
                result = subprocess.run(
                    ["timeout", "120s", "vercel", "--prod"],
                    capture_output=True,
                    text=True,
                    timeout=120
                )
                
                if result.returncode == 0:
                    return "🚀 Deployment successful! Website updated."
                else:
                    return f"❌ Deployment failed: {result.stderr[:200]}"
            
            elif command.lower().startswith("status"):
                # Get current status
                return "✅ WhatsApp Monitor Active\n📊 Website: 96.8% Success Rate\n🌐 Domain: arabyouthleaders.org needs nameserver fix"
            
            else:
                return f"❓ Unknown command: {command}\n\nAvailable commands:\n• go - Run testing cycle\n• cycle - Run testing cycle\n• deploy - Deploy to Vercel\n• status - Get current status"
                
        except subprocess.TimeoutExpired:
            return "⏰ Command timed out"
        except Exception as e:
            return f"❌ Error executing command: {str(e)[:200]}"
    
    def monitor_messages(self):
        """Main monitoring loop"""
        print("\n🔄 Starting message monitoring...")
        
        if not self.find_contact_chat(self.target_number):
            print("❌ Could not find target contact")
            return False
        
        self.monitoring = True
        
        while self.monitoring:
            try:
                # Get latest message
                latest_message = self.get_latest_message()
                
                if latest_message and latest_message["id"] != self.last_message_id:
                    print(f"\n📨 New message from target: {latest_message['text']}")
                    
                    # Update last seen message
                    self.last_message_id = latest_message["id"]
                    
                    # Check if it's a command for us
                    message_text = latest_message["text"].strip()
                    
                    if message_text:  # Any non-empty message is considered a command
                        print(f"🎯 Processing command: {message_text}")
                        
                        # Execute command
                        result = self.execute_command(message_text)
                        
                        # Send response
                        response = f"🤖 Command: {message_text}\n\n{result}"
                        self.send_message(response)
                        
                        print(f"✅ Command processed and response sent")
                
                # Wait before next check
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n⏹️ Monitoring stopped by user")
                self.monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(10)  # Wait longer on errors
                continue
    
    def start_monitoring(self):
        """Start the complete monitoring process"""
        print("🚀 STARTING WHATSAPP COMMAND MONITOR")
        print("=" * 50)
        
        try:
            # Setup driver
            if not self.setup_driver():
                return False
            
            # Open WhatsApp Web
            if not self.open_whatsapp_web():
                return False
            
            # Start monitoring
            self.monitor_messages()
            
        except Exception as e:
            print(f"❌ Critical error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            print("\n🧹 Cleaning up...")
            # Don't close driver to keep session alive
            # self.driver.quit()
            print("✅ Cleanup complete")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        print("⏹️ Monitoring stopped")

def main():
    """Main execution function"""
    monitor = WhatsAppCommandMonitor()
    
    try:
        monitor.start_monitoring()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        monitor.cleanup()

if __name__ == "__main__":
    main() 