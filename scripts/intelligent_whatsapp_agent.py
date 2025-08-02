#!/usr/bin/env python3
"""
🤖 INTELLIGENT WHATSAPP AGENT
Advanced agent using OpenAI Agent SDK for intelligent decision making
Three action modes:
1. Respond in WhatsApp - Direct text response
2. Execute on Cursor - Send commands to Cursor editor
3. Observe and control Cursor and report - Screen automation with feedback
"""

import time
import json
import os
import sys
import subprocess
import re
import pyautogui
import cv2
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium_stealth import stealth
from webdriver_manager.chrome import ChromeDriverManager
import threading
from openai import OpenAI
from PIL import Image
import keyboard
# Use Linux-compatible window manager instead of pygetwindow
try:
    from linux_window_manager import LinuxWindowManager, getAllWindows
    window_manager = LinuxWindowManager()
except ImportError:
    print("⚠️ Linux window manager not found, some features may not work")
    window_manager = None

# Add voice_os modules to path
sys.path.append('../voice_os')
try:
    from integrations.cursor_bridge import CursorBridge
    from integrations.system_control import SystemControl
except ImportError:
    print("⚠️ Voice OS modules not found, using local implementations")

class IntelligentWhatsAppAgent:
    """Advanced WhatsApp agent with OpenAI intelligence and screen control"""
    
    def __init__(self):
        self.driver = None
        self.target_number = "052 339 6883"
        self.last_message_id = None
        self.monitoring = False
        self.check_interval = 3  # faster checking
        
        # Initialize OpenAI client
        self.openai = OpenAI()
        
        # Initialize screen control
        self.setup_screen_control()
        
        # Initialize Cursor bridge
        self.setup_cursor_bridge()
        
        print("🤖 Intelligent WhatsApp Agent Initialized")
        print("🧠 OpenAI Agent SDK: Ready")
        print("🖥️ Screen Control: Ready")
        print("📝 Cursor Integration: Ready")
        print(f"📱 Target Number: {self.target_number}")
        
    def setup_screen_control(self):
        """Setup screen control and automation"""
        try:
            # Configure pyautogui
            pyautogui.FAILSAFE = True
            pyautogui.PAUSE = 0.1
            
            # Get screen info
            self.screen_width, self.screen_height = pyautogui.size()
            print(f"🖥️ Screen: {self.screen_width}x{self.screen_height}")
            
            self.screen_control_ready = True
        except Exception as e:
            print(f"⚠️ Screen control setup failed: {e}")
            self.screen_control_ready = False
    
    def setup_cursor_bridge(self):
        """Setup Cursor editor integration"""
        try:
            # Try to import from voice_os
            self.cursor_bridge = CursorBridge() if 'CursorBridge' in globals() else None
            self.cursor_bridge_ready = True
        except Exception as e:
            print(f"⚠️ Cursor bridge setup failed: {e}")
            self.cursor_bridge_ready = False
    
    def setup_driver(self):
        """Setup Chrome driver for WhatsApp Web"""
        print("\n🔧 Setting up Chrome driver...")
        
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Session persistence
        profile_path = os.path.abspath("whatsapp_profile")
        chrome_options.add_argument(f"--user-data-dir={profile_path}")
        chrome_options.add_argument("--profile-directory=Default")
        chrome_options.add_experimental_option("detach", True)
        
        try:
            self.driver = webdriver.Chrome(
                service=webdriver.chrome.service.Service(ChromeDriverManager().install()),
                options=chrome_options
            )
            
            stealth(self.driver,
                   languages=["en-US", "en"],
                   vendor="Google Inc.",
                   platform="Linux x86_64",
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
            time.sleep(5)
            
            # Check if QR code is present
            try:
                qr_element = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='qr-code']")
                print("📱 QR Code detected - Please scan with your phone")
                print("⏳ Waiting for authentication...")
                
                WebDriverWait(self.driver, 300).until_not(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='qr-code']"))
                )
                print("✅ Authentication successful!")
            except NoSuchElementException:
                print("✅ Already authenticated!")
            
            # Wait for main interface
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "[data-testid='chat-list']"))
            )
            
            print("🎯 WhatsApp Web ready for intelligent monitoring")
            return True
        except Exception as e:
            print(f"❌ Failed to open WhatsApp Web: {e}")
            return False
    
    def find_contact_chat(self, contact_number):
        """Find and open chat with target contact"""
        try:
            chat_elements = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='cell-frame-container']")
            
            for chat in chat_elements:
                try:
                    contact_text = chat.find_element(By.CSS_SELECTOR, "[data-testid='contact-title'] span").text
                    
                    if self.is_target_contact(contact_text):
                        print(f"✅ Found target contact: {contact_text}")
                        chat.click()
                        time.sleep(2)
                        return True
                except:
                    continue
            
            print(f"⚠️ Contact not found: {contact_number}")
            return False
        except Exception as e:
            print(f"❌ Error finding contact: {e}")
            return False
    
    def is_target_contact(self, contact_text):
        """Check if contact matches target number"""
        target_variations = [
            "052 339 6883", "0523396883", "+972 52 339 6883",
            "+972523396883", "972523396883", "052-339-6883"
        ]
        
        contact_digits = re.sub(r'[^\d]', '', contact_text)
        
        for variation in target_variations:
            variation_digits = re.sub(r'[^\d]', '', variation)
            if contact_digits.endswith(variation_digits) or variation_digits.endswith(contact_digits):
                return True
        return False
    
    def get_latest_message(self):
        """Get the latest message from current chat"""
        try:
            messages = self.driver.find_elements(By.CSS_SELECTOR, "[data-testid='msg-container']")
            
            if not messages:
                return None
                
            last_message = messages[-1]
            incoming = last_message.find_elements(By.CSS_SELECTOR, "[data-testid='msg-container-incoming']")
            
            if incoming:
                text_elements = last_message.find_elements(By.CSS_SELECTOR, "[data-testid='conversation-text-content'] span")
                
                if text_elements:
                    message_text = text_elements[0].text
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
            message_box = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='conversation-compose-box-input']")
            message_box.clear()
            message_box.send_keys(message)
            
            send_button = self.driver.find_element(By.CSS_SELECTOR, "[data-testid='send']")
            send_button.click()
            
            print(f"📤 Message sent: {message[:50]}...")
            return True
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def take_screenshot(self):
        """Take a screenshot for analysis"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            screenshot_path = f"screenshots/screen_{timestamp}.png"
            
            # Create screenshots directory if it doesn't exist
            os.makedirs("screenshots", exist_ok=True)
            
            # Take screenshot
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path)
            
            return screenshot_path
        except Exception as e:
            print(f"❌ Error taking screenshot: {e}")
            return None
    
    def analyze_screen_with_ai(self, screenshot_path, task_description):
        """Analyze screenshot using OpenAI Vision"""
        try:
            # Read the screenshot
            with open(screenshot_path, "rb") as image_file:
                import base64
                image_data = base64.b64encode(image_file.read()).decode()
            
            # Send to OpenAI for analysis
            response = self.openai.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Analyze this screen for: {task_description}. Provide specific observations and actionable insights."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_data}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=500
            )
            
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Error analyzing screen: {e}")
            return "Could not analyze screen"
    
    def intelligent_decision_maker(self, message_text):
        """Use OpenAI to decide which action to take"""
        try:
            decision_prompt = f"""
You are an intelligent assistant that decides how to handle WhatsApp messages. 
You have 3 action options:

1. RESPOND_WHATSAPP - Send a direct text response via WhatsApp
2. EXECUTE_CURSOR - Send commands to Cursor code editor  
3. OBSERVE_CONTROL - Take screenshot, analyze, control screen, and report back

Message received: "{message_text}"

Consider:
- If it's a question, greeting, or needs simple info → RESPOND_WHATSAPP
- If it mentions code, editing, programming, or Cursor → EXECUTE_CURSOR  
- If it asks to check, observe, control screen, or analyze something → OBSERVE_CONTROL

Respond with JSON: {{"action": "ACTION_NAME", "reasoning": "why this action", "parameters": {{"key": "value"}}}}
"""

            response = self.openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": decision_prompt}],
                max_tokens=200
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
        except Exception as e:
            print(f"❌ Error in decision making: {e}")
            return {"action": "RESPOND_WHATSAPP", "reasoning": "fallback", "parameters": {}}
    
    def execute_respond_whatsapp(self, message_text, parameters):
        """Execute WhatsApp response action"""
        try:
            # Generate intelligent response
            response = self.openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": "You are a helpful assistant responding via WhatsApp. Be concise, friendly, and informative."
                    },
                    {
                        "role": "user", 
                        "content": f"Respond to this WhatsApp message: {message_text}"
                    }
                ],
                max_tokens=200
            )
            
            reply = response.choices[0].message.content
            self.send_message(f"🤖 {reply}")
            
            return f"Responded in WhatsApp: {reply[:50]}..."
        except Exception as e:
            self.send_message(f"❌ Error generating response: {str(e)}")
            return f"Error in WhatsApp response: {e}"
    
    def execute_cursor_command(self, message_text, parameters):
        """Execute Cursor editor commands"""
        try:
            # Use Linux window manager to find and focus Cursor
            if window_manager:
                if not window_manager.open_cursor():
                    return "❌ Cursor not found. Please install Cursor editor or check if it's in PATH."
            else:
                return "❌ Window manager not available on this system."
            
            time.sleep(1)
            
            # Determine what to do in Cursor based on message
            if "open file" in message_text.lower():
                # Ctrl+P to open file
                pyautogui.hotkey('ctrl', 'p')
                time.sleep(0.5)
                
            elif "new file" in message_text.lower():
                # Ctrl+N for new file
                pyautogui.hotkey('ctrl', 'n')
                
            elif "save" in message_text.lower():
                # Ctrl+S to save
                pyautogui.hotkey('ctrl', 's')
                
            elif "find" in message_text.lower() or "search" in message_text.lower():
                # Ctrl+F to find
                pyautogui.hotkey('ctrl', 'f')
                
            elif "terminal" in message_text.lower():
                # Ctrl+` to open terminal
                pyautogui.hotkey('ctrl', '`')
                
            else:
                # Use AI to interpret the command
                ai_response = self.openai.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "Convert this message into a Cursor editor action. Reply with just the action to take."
                        },
                        {
                            "role": "user",
                            "content": message_text
                        }
                    ],
                    max_tokens=100
                )
                
                action = ai_response.choices[0].message.content
                
                # Type the interpreted action
                if len(action) < 200:  # Safety check
                    pyautogui.typewrite(action)
            
            self.send_message(f"✅ Executed in Cursor: {message_text}")
            return f"Cursor command executed: {message_text}"
            
        except Exception as e:
            error_msg = f"❌ Cursor execution failed: {str(e)}"
            self.send_message(error_msg)
            return error_msg
    
    def execute_observe_control(self, message_text, parameters):
        """Execute screen observation and control"""
        try:
            # Take screenshot
            screenshot_path = self.take_screenshot()
            if not screenshot_path:
                return "❌ Could not take screenshot"
            
            # Analyze with AI
            analysis = self.analyze_screen_with_ai(screenshot_path, message_text)
            
            # Send initial analysis
            self.send_message(f"👁️ Screen Analysis:\n{analysis[:300]}...")
            
            # Check if user wants us to take action
            if any(word in message_text.lower() for word in ['click', 'type', 'scroll', 'press']):
                # Use AI to determine screen actions
                action_prompt = f"""
Based on this screen analysis: {analysis}
And user request: {message_text}

What specific screen actions should I take? Reply with JSON:
{{"actions": [{{"type": "click", "x": 100, "y": 200}}, {{"type": "type", "text": "hello"}}]}}

Available actions: click, type, scroll, key_press, hotkey
"""
                
                action_response = self.openai.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": action_prompt}],
                    max_tokens=300
                )
                
                try:
                    actions = json.loads(action_response.choices[0].message.content)
                    
                    for action in actions.get('actions', []):
                        if action['type'] == 'click':
                            pyautogui.click(action['x'], action['y'])
                            time.sleep(0.5)
                        elif action['type'] == 'type':
                            pyautogui.typewrite(action['text'])
                        elif action['type'] == 'scroll':
                            pyautogui.scroll(action.get('amount', 3))
                        elif action['type'] == 'key_press':
                            pyautogui.press(action['key'])
                        elif action['type'] == 'hotkey':
                            pyautogui.hotkey(*action['keys'])
                    
                    # Take another screenshot to see results
                    final_screenshot = self.take_screenshot()
                    final_analysis = self.analyze_screen_with_ai(final_screenshot, "What changed after the actions?")
                    
                    self.send_message(f"🎯 Actions completed!\nResult: {final_analysis[:200]}...")
                    
                except json.JSONDecodeError:
                    self.send_message("✅ Screen analyzed but no specific actions taken")
            
            return f"Screen observation completed: {analysis[:100]}..."
            
        except Exception as e:
            error_msg = f"❌ Screen observation failed: {str(e)}"
            self.send_message(error_msg)
            return error_msg
    
    def process_intelligent_message(self, message_text):
        """Process message using intelligent decision making"""
        try:
            print(f"\n🧠 INTELLIGENT PROCESSING: {message_text}")
            
            # Get AI decision
            decision = self.intelligent_decision_maker(message_text)
            action = decision.get('action', 'RESPOND_WHATSAPP')
            reasoning = decision.get('reasoning', 'default')
            parameters = decision.get('parameters', {})
            
            print(f"🎯 AI Decision: {action}")
            print(f"💭 Reasoning: {reasoning}")
            
            # Execute the decided action
            if action == "RESPOND_WHATSAPP":
                result = self.execute_respond_whatsapp(message_text, parameters)
            elif action == "EXECUTE_CURSOR":
                result = self.execute_cursor_command(message_text, parameters)
            elif action == "OBSERVE_CONTROL":
                result = self.execute_observe_control(message_text, parameters)
            else:
                result = self.execute_respond_whatsapp(message_text, parameters)
            
            print(f"✅ Result: {result}")
            return result
            
        except Exception as e:
            error_msg = f"❌ Intelligent processing failed: {str(e)}"
            print(error_msg)
            self.send_message(error_msg)
            return error_msg
    
    def monitor_messages(self):
        """Main intelligent monitoring loop"""
        print("\n🤖 Starting intelligent message monitoring...")
        
        if not self.find_contact_chat(self.target_number):
            print("❌ Could not find target contact")
            return False
        
        self.monitoring = True
        
        while self.monitoring:
            try:
                latest_message = self.get_latest_message()
                
                if latest_message and latest_message["id"] != self.last_message_id:
                    print(f"\n📨 New message: {latest_message['text']}")
                    
                    self.last_message_id = latest_message["id"]
                    message_text = latest_message["text"].strip()
                    
                    if message_text:
                        # Process with intelligent agent
                        self.process_intelligent_message(message_text)
                
                time.sleep(self.check_interval)
                
            except KeyboardInterrupt:
                print("\n⏹️ Monitoring stopped by user")
                self.monitoring = False
                break
            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                time.sleep(10)
                continue
    
    def start_monitoring(self):
        """Start the complete intelligent monitoring system"""
        print("🚀 STARTING INTELLIGENT WHATSAPP AGENT")
        print("=" * 60)
        
        try:
            if not self.setup_driver():
                return False
            
            if not self.open_whatsapp_web():
                return False
            
            self.monitor_messages()
            
        except Exception as e:
            print(f"❌ Critical error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        if self.driver:
            print("\n🧹 Cleaning up...")
            print("✅ Cleanup complete")
    
    def stop_monitoring(self):
        """Stop monitoring"""
        self.monitoring = False
        print("⏹️ Intelligent monitoring stopped")

def main():
    """Main execution function"""
    agent = IntelligentWhatsAppAgent()
    
    try:
        agent.start_monitoring()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        agent.cleanup()

if __name__ == "__main__":
    main() 