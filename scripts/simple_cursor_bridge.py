#!/usr/bin/env python3
"""
Simple Cursor Bridge - Basic integration with Cursor IDE
Fallback implementation without voice_os dependencies
"""

import subprocess
import os
import time
import pyautogui
import pygetwindow as gw
from typing import Optional, List

class SimpleCursorBridge:
    """Simple bridge for controlling Cursor IDE"""
    
    def __init__(self):
        self.cursor_window = None
        self.cursor_paths = [
            "cursor",  # Try PATH first
            "/usr/bin/cursor",
            "/usr/local/bin/cursor",
            "/snap/bin/cursor",
            os.path.expanduser("~/.local/bin/cursor"),
        ]
        
        print("✅ Simple Cursor Bridge initialized")
    
    def find_cursor_window(self):
        """Find Cursor window"""
        try:
            cursor_windows = [w for w in gw.getAllWindows() if 'cursor' in w.title.lower()]
            if cursor_windows:
                self.cursor_window = cursor_windows[0]
                return True
            return False
        except Exception as e:
            print(f"❌ Error finding Cursor window: {e}")
            return False
    
    def open_cursor(self):
        """Open Cursor IDE"""
        try:
            for path in self.cursor_paths:
                try:
                    subprocess.Popen([path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    time.sleep(3)  # Wait for Cursor to start
                    if self.find_cursor_window():
                        print("✅ Cursor opened successfully")
                        return True
                except FileNotFoundError:
                    continue
            
            print("❌ Could not find Cursor executable")
            return False
        except Exception as e:
            print(f"❌ Error opening Cursor: {e}")
            return False
    
    def focus_cursor(self):
        """Focus Cursor window"""
        try:
            if not self.cursor_window and not self.find_cursor_window():
                return self.open_cursor()
            
            if self.cursor_window:
                self.cursor_window.activate()
                time.sleep(0.5)
                return True
            return False
        except Exception as e:
            print(f"❌ Error focusing Cursor: {e}")
            return False
    
    def send_command(self, command: str):
        """Send a command to Cursor"""
        try:
            if not self.focus_cursor():
                return False
                
            # Common Cursor commands
            if command.lower() in ['new file', 'new']:
                pyautogui.hotkey('ctrl', 'n')
            elif command.lower() in ['open file', 'open']:
                pyautogui.hotkey('ctrl', 'o')
            elif command.lower() in ['save', 'save file']:
                pyautogui.hotkey('ctrl', 's')
            elif command.lower() in ['find', 'search']:
                pyautogui.hotkey('ctrl', 'f')
            elif command.lower() in ['terminal', 'console']:
                pyautogui.hotkey('ctrl', '`')
            elif command.lower() in ['command palette', 'palette']:
                pyautogui.hotkey('ctrl', 'shift', 'p')
            else:
                # Type the command directly
                pyautogui.typewrite(command)
            
            return True
        except Exception as e:
            print(f"❌ Error sending command to Cursor: {e}")
            return False 