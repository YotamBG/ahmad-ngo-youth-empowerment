#!/usr/bin/env python3
"""
🤖 SIMPLE & RELIABLE WHATSAPP BOT
Based on best practices from online research and existing implementations
Three action modes: Respond, Execute Commands, Observe & Control
"""

import time
import json
import os
import sys
import subprocess
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import signal
import threading

# Core libraries for WhatsApp automation
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys

# For AI decision making (optional - falls back to simple rules)
try:
    from openai import OpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False
    print("⚠️ OpenAI not available - using rule-based decisions")

# Screen automation libraries (optional)
try:
    import pyautogui
    import cv2
    import numpy as np
    HAS_SCREEN_CONTROL = True
    # Configure pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
except ImportError:
    HAS_SCREEN_CONTROL = False
    print("⚠️ Screen control libraries not available")

class SimpleWhatsAppBot:
    """Simple and reliable WhatsApp bot with three action modes"""
    
    def __init__(self, target_number="052 339 6883"):
        self.target_number = target_number
        self.driver = None
        self.last_message_id = None
        self.monitoring = False
        self.check_interval = 3
        self.session_path = "whatsapp_session"
        
        # Initialize OpenAI if available
        self.openai = None
        if HAS_OPENAI and os.getenv('OPENAI_API_KEY'):
            try:
                self.openai = OpenAI()
                print("🧠 AI decision making enabled")
            except Exception as e:
                print(f"⚠️ OpenAI initialization failed: {e}")
        
        print("🤖 Simple WhatsApp Bot Initialized")
        print(f"📱 Target Number: {self.target_number}")
        print("🎯 Three Action Modes: Respond | Execute | Observe")
        
    def setup_driver_with_timeout(self, timeout=30):
        """Setup Chrome driver with proven reliability patterns"""
        print(f"\n🔧 Setting up Chrome driver (timeout: {timeout}s)...")
        
        try:
            # Use absolute path for session
            session_path = os.path.abspath(self.session_path)
            os.makedirs(session_path, exist_ok=True)
            
            chrome_options = Options()
            
            # CRITICAL: Session persistence to avoid QR scanning
            chrome_options.add_argument(f"--user-data-dir={session_path}")
            chrome_options.add_argument("--profile-directory=Default")
            
            # Anti-detection options (from research)
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            chrome_options.add_experimental_option("detach", True)
            
            # Performance options
            chrome_options.add_argument("--disable-extensions")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-features=VizDisplayCompositor")
            
            # Timeout handling for driver creation
            def create_driver():
                return webdriver.Chrome(options=chrome_options)
            
            # Use timeout for driver creation [[memory:4846922]]
            driver_thread = threading.Thread(target=lambda: setattr(self, '_temp_driver', create_driver()))
            driver_thread.daemon = True
            driver_thread.start()
            driver_thread.join(timeout=timeout)
            
            if hasattr(self, '_temp_driver'):
                self.driver = self._temp_driver
                delattr(self, '_temp_driver')
            else:
                raise TimeoutException(f"Driver creation timed out after {timeout}s")
            
            print("✅ Chrome driver setup complete")
            return True
            
        except Exception as e:
            print(f"❌ Driver setup failed: {e}")
            return False
    
    def open_whatsapp_web_with_timeout(self, timeout=60):
        """Open WhatsApp Web with timeout and QR handling"""
        print("\n🌐 Opening WhatsApp Web...")
        
        try:
            # Navigate with timeout
            self.driver.set_page_load_timeout(timeout)
            self.driver.get("https://web.whatsapp.com/")
            
            # Check for QR code
            try:
                qr_element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='qr-code']"))
                )
                print("📱 QR Code detected - Please scan with your phone")
                print(f"⏳ Waiting up to {timeout}s for authentication...")
                
                # Wait for QR code to disappear (authentication complete)
                WebDriverWait(self.driver, timeout).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='qr-code']"))
                )
                print("✅ Authentication successful!")
                
            except TimeoutException:
                # Check if already authenticated
                try:
                    WebDriverWait(self.driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']"))
                    )
                    print("✅ Already authenticated!")
                except TimeoutException:
                    print("❌ Authentication timeout - please try again")
                    return False
            
            # Wait for main interface
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']"))
            )
            
            print("🎯 WhatsApp Web ready for monitoring")
            return True
            
        except Exception as e:
            print(f"❌ Failed to open WhatsApp Web: {e}")
            return False
    
    def find_target_contact(self):
        """Find and open chat with target contact"""
        try:
            # Multiple strategies to find contact
            contact_selectors = [
                f"[title*='{self.target_number}']",
                f"[data-testid='cell-frame-container'] span[title*='{self.target_number}']",
                f"[data-testid='contact-title'] span[title*='{self.target_number}']"
            ]
            
            for selector in contact_selectors:
                try:
                    contact = self.driver.find_element(By.CSS_SELECTOR, selector)
                    contact.click()
                    print(f"✅ Found and opened contact: {self.target_number}")
                    time.sleep(2)
                    return True
                except NoSuchElementException:
                    continue
            
            # Fallback: search for contact
            try:
                search_box = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='chat-list-search']")
                search_box.click()
                search_box.send_keys(self.target_number)
                time.sleep(2)
                
                # Click first result
                first_result = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='cell-frame-container']")
                first_result.click()
                print(f"✅ Found contact via search: {self.target_number}")
                return True
            except Exception as e:
                print(f"❌ Search fallback failed: {e}")
            
            print(f"⚠️ Contact not found: {self.target_number}")
            return False
            
        except Exception as e:
            print(f"❌ Error finding contact: {e}")
            return False
    
    def get_latest_message(self):
        """Get the latest incoming message"""
        try:
            # Wait for messages to load
            time.sleep(1)
            
            # Multiple selectors for message containers
            message_selectors = [
                "[data-testid='msg-container']",
                ".message-in",
                "[data-testid='conversation-panel-messages'] > div > div"
            ]
            
            messages = []
            for selector in message_selectors:
                try:
                    messages = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    if messages:
                        break
                except:
                    continue
            
            if not messages:
                return None
            
            # Get the last message
            last_message = messages[-1]
            
            # Check if it's incoming (not sent by us)
            incoming_indicators = [
                "[data-testid='msg-container-incoming']",
                ".message-in",
                ".msg-incoming"
            ]
            
            is_incoming = False
            for indicator in incoming_indicators:
                if last_message.find_elements(By.CSS_SELECTOR, indicator):
                    is_incoming = True
                    break
            
            if not is_incoming:
                return None
            
            # Extract message text
            text_selectors = [
                "[data-testid='conversation-text-content'] span",
                ".message-text",
                ".selectable-text"
            ]
            
            message_text = ""
            for selector in text_selectors:
                try:
                    text_elements = last_message.find_elements(By.CSS_SELECTOR, selector)
                    if text_elements:
                        message_text = text_elements[0].text
                        break
                except:
                    continue
            
            if message_text:
                message_id = last_message.get_attribute("data-id") or str(time.time())
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
            # Multiple selectors for message input
            input_selectors = [
                "[data-testid='conversation-compose-box-input']",
                "[contenteditable='true'][data-tab='10']",
                "div[contenteditable='true']"
            ]
            
            message_box = None
            for selector in input_selectors:
                try:
                    message_box = self.driver.find_element(By.CSS_SELECTOR, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not message_box:
                print("❌ Could not find message input box")
                return False
            
            # Clear and type message
            message_box.clear()
            message_box.send_keys(message)
            
            # Send message
            message_box.send_keys(Keys.ENTER)
            
            print(f"📤 Message sent: {message[:50]}...")
            return True
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def decide_action(self, message_text):
        """Decide which action to take based on message content"""
        
        # Use AI decision making if available
        if self.openai:
            try:
                response = self.openai.chat.completions.create(
                    model="gpt-4",
                    messages=[{
                        "role": "user",
                        "content": f"""Analyze this WhatsApp message and decide the action:
                        
Message: "{message_text}"

Choose ONE action:
1. RESPOND - for questions, greetings, general conversation
2. EXECUTE - for commands like "open file", "run code", "cursor", "terminal"  
3. OBSERVE - for "screenshot", "check screen", "what's on screen", "analyze"

Respond with just the action name."""
                    }],
                    max_tokens=10
                )
                
                action = response.choices[0].message.content.strip().upper()
                if action in ["RESPOND", "EXECUTE", "OBSERVE"]:
                    return action
                    
            except Exception as e:
                print(f"⚠️ AI decision failed: {e}")
        
        # Fallback: Rule-based decisions
        message_lower = message_text.lower()
        
        # EXECUTE keywords
        execute_keywords = [
            "cursor", "code", "file", "terminal", "command", "run", "execute", 
            "open", "save", "edit", "programming", "script", "git"
        ]
        
        # OBSERVE keywords  
        observe_keywords = [
            "screenshot", "screen", "see", "show", "check", "look", "view",
            "observe", "analyze", "what's on", "click", "control"
        ]
        
        # Check for keywords
        for keyword in execute_keywords:
            if keyword in message_lower:
                return "EXECUTE"
        
        for keyword in observe_keywords:
            if keyword in message_lower:
                return "OBSERVE"
        
        # Default to RESPOND
        return "RESPOND"
    
    def action_respond(self, message_text):
        """Generate and send a response"""
        try:
            if self.openai:
                # AI-generated response
                response = self.openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful WhatsApp bot. Be concise, friendly, and informative. Use emojis sparingly."
                        },
                        {
                            "role": "user",
                            "content": f"Respond to: {message_text}"
                        }
                    ],
                    max_tokens=150
                )
                
                reply = response.choices[0].message.content
            else:
                # Simple rule-based responses
                message_lower = message_text.lower()
                
                if any(word in message_lower for word in ["hello", "hi", "hey"]):
                    reply = "👋 Hello! I'm your WhatsApp bot assistant. How can I help you?"
                elif any(word in message_lower for word in ["how are you", "how's it going"]):
                    reply = "🤖 I'm running smoothly! Ready to assist with coding, automation, or general questions."
                elif any(word in message_lower for word in ["help", "what can you do"]):
                    reply = """🎯 I can help with:
• 💬 Answer questions and chat
• 📝 Execute code/cursor commands  
• 👁️ Take screenshots and control screen
• 🔧 Development assistance

Just send me a message!"""
                elif "status" in message_lower:
                    reply = f"✅ Bot Status: Online and monitoring\n🕒 Time: {datetime.now().strftime('%H:%M:%S')}\n📍 Ready for commands!"
                else:
                    reply = "🤖 I received your message! For specific actions, try keywords like 'cursor', 'screenshot', or 'help'."
            
            return self.send_message(f"🤖 {reply}")
            
        except Exception as e:
            error_msg = f"❌ Response generation failed: {str(e)}"
            print(error_msg)
            return self.send_message(error_msg)
    
    def action_execute(self, message_text):
        """Execute commands on the system"""
        try:
            message_lower = message_text.lower()
            
            # Simple command mapping
            if "cursor" in message_lower:
                if "open" in message_lower or "new" in message_lower:
                    result = subprocess.run(["cursor", "."], capture_output=True, text=True, timeout=10)
                    self.send_message("✅ Cursor opened in current directory")
                elif "terminal" in message_lower:
                    # Focus Cursor and open terminal
                    if HAS_SCREEN_CONTROL:
                        pyautogui.hotkey('ctrl', '`')
                        self.send_message("✅ Cursor terminal opened")
                    else:
                        self.send_message("⚠️ Screen control not available")
                else:
                    self.send_message("📝 Cursor command executed. Common actions: 'open cursor', 'cursor terminal'")
            
            elif "git" in message_lower:
                if "status" in message_lower:
                    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, timeout=10)
                    if result.stdout.strip():
                        self.send_message(f"📊 Git Status:\n{result.stdout[:200]}...")
                    else:
                        self.send_message("✅ Git: No changes to commit")
                else:
                    self.send_message("🔧 Git command recognized. Try 'git status' for repository info.")
            
            elif any(word in message_lower for word in ["run", "execute", "start"]):
                self.send_message("🚀 Execution command received. For safety, specify exactly what to run.")
            
            else:
                # AI interpretation if available
                if self.openai:
                    response = self.openai.chat.completions.create(
                        model="gpt-4",
                        messages=[{
                            "role": "user",
                            "content": f"Convert this into a simple terminal command: {message_text}"
                        }],
                        max_tokens=50
                    )
                    interpreted_cmd = response.choices[0].message.content
                    self.send_message(f"🔧 Interpreted as: {interpreted_cmd}\n(Not executed for safety)")
                else:
                    self.send_message("📝 Command received but not recognized. Try 'cursor', 'git status', or be more specific.")
            
            return True
            
        except subprocess.TimeoutExpired:
            return self.send_message("⏰ Command timed out")
        except Exception as e:
            error_msg = f"❌ Execution failed: {str(e)}"
            print(error_msg)
            return self.send_message(error_msg)
    
    def action_observe(self, message_text):
        """Take screenshots and analyze screen"""
        try:
            if not HAS_SCREEN_CONTROL:
                return self.send_message("❌ Screen control not available. Install: pip install pyautogui opencv-python")
            
            # Take screenshot
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/screen_{timestamp}.png"
            
            os.makedirs("screenshots", exist_ok=True)
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            # Basic analysis
            message_lower = message_text.lower()
            
            if "cursor" in message_lower:
                analysis = "📸 Screenshot taken. Looking for Cursor IDE windows..."
                # Could add window detection logic here
            elif "terminal" in message_lower:
                analysis = "📸 Screenshot taken. Checking for terminal windows..."
            else:
                analysis = f"📸 Screenshot saved: {screenshot_path}\n🖥️ Screen captured at {datetime.now().strftime('%H:%M:%S')}"
            
            # AI analysis if available
            if self.openai and "analyze" in message_lower:
                analysis += "\n🧠 AI analysis would require image upload capability"
            
            return self.send_message(analysis)
            
        except Exception as e:
            error_msg = f"❌ Screen observation failed: {str(e)}"
            print(error_msg)
            return self.send_message(error_msg)
    
    def process_message(self, message_text):
        """Process incoming message with action decision"""
        try:
            print(f"\n📨 Processing: {message_text}")
            
            # Decide action
            action = self.decide_action(message_text)
            print(f"🎯 Action decided: {action}")
            
            # Execute action
            if action == "RESPOND":
                return self.action_respond(message_text)
            elif action == "EXECUTE":
                return self.action_execute(message_text)
            elif action == "OBSERVE":
                return self.action_observe(message_text)
            else:
                return self.send_message("❓ Unsure how to handle that. Try 'help' for available actions.")
            
        except Exception as e:
            error_msg = f"❌ Message processing failed: {str(e)}"
            print(error_msg)
            return self.send_message(error_msg)
    
    def monitor_messages(self):
        """Main monitoring loop with timeout handling"""
        print(f"\n🤖 Starting message monitoring (check every {self.check_interval}s)...")
        
        if not self.find_target_contact():
            print("❌ Could not find target contact")
            return False
        
        self.monitoring = True
        consecutive_errors = 0
        max_errors = 5
        
        while self.monitoring:
            try:
                # Use timeout for message checking [[memory:4846922]]
                def check_message():
                    return self.get_latest_message()
                
                message_thread = threading.Thread(target=lambda: setattr(self, '_temp_message', check_message()))
                message_thread.daemon = True
                message_thread.start()
                message_thread.join(timeout=10)  # 10 second timeout
                
                latest_message = getattr(self, '_temp_message', None)
                if hasattr(self, '_temp_message'):
                    delattr(self, '_temp_message')
                
                if latest_message and latest_message["id"] != self.last_message_id:
                    print(f"\n📨 New message: {latest_message['text']}")
                    
                    self.last_message_id = latest_message["id"]
                    message_text = latest_message["text"].strip()
                    
                    if message_text:
                        # Process with timeout
                        process_thread = threading.Thread(target=lambda: self.process_message(message_text))
                        process_thread.daemon = True
                        process_thread.start()
                        process_thread.join(timeout=30)  # 30 second timeout for processing
                        
                        consecutive_errors = 0  # Reset error count on success
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n⏹️ Monitoring stopped by user")
                self.monitoring = False
                break
            except Exception as e:
                consecutive_errors += 1
                print(f"❌ Monitoring error ({consecutive_errors}/{max_errors}): {e}")
                
                if consecutive_errors >= max_errors:
                    print("💥 Too many consecutive errors - stopping monitor")
                    break
                
                time.sleep(10)  # Wait longer on errors
                continue
    
    def start_monitoring(self):
        """Start the complete monitoring system with timeout handling"""
        print("🚀 STARTING SIMPLE WHATSAPP BOT")
        print("=" * 60)
        
        try:
            # Setup with timeout [[memory:4846922]]
            if not self.setup_driver_with_timeout(30):
                print("❌ Driver setup failed")
                return False
            
            if not self.open_whatsapp_web_with_timeout(120):
                print("❌ WhatsApp Web setup failed")
                return False
            
            # Start monitoring
            self.monitor_messages()
            
        except Exception as e:
            print(f"❌ Critical error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n🧹 Cleaning up...")
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
        print("✅ Cleanup complete")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        print("⏹️ Monitoring stopped")

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    print(f"\n🛑 Received signal {signum}")
    if hasattr(signal_handler, 'bot'):
        signal_handler.bot.stop_monitoring()
    sys.exit(0)

def main():
    """Main execution function"""
    
    # Handle Ctrl+C gracefully
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🤖 SIMPLE & RELIABLE WHATSAPP BOT")
    print("=" * 60)
    print("🎯 Three Action Modes:")
    print("   💬 RESPOND - Chat and answer questions")
    print("   📝 EXECUTE - Run commands and control cursor")
    print("   👁️ OBSERVE - Take screenshots and analyze screen")
    print("=" * 60)
    
    # Create bot instance
    bot = SimpleWhatsAppBot()
    signal_handler.bot = bot  # For signal handling
    
    try:
        bot.start_monitoring()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        bot.cleanup()

if __name__ == "__main__":
    main() 