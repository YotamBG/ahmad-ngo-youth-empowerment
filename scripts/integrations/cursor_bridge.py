"""
Cursor IDE Bridge - Integration with Cursor IDE for voice control
"""

import subprocess
import os
import time
import pyautogui
import pygetwindow as gw
from typing import Optional, List, Dict, Any
from loguru import logger

from utils.config_manager import ConfigManager
from utils.logger import VoiceOSLogger


class CursorBridge:
    """Bridge for controlling Cursor IDE via voice commands"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = ConfigManager(config_path)
        self.logger = VoiceOSLogger("cursor_bridge")
        self.cursor_window = None
        self.cursor_process = None
        
        # Get Cursor executable path
        self.cursor_path = self.config.get("cursor.executable_path", "")
        if "%USERNAME%" in self.cursor_path:
            self.cursor_path = self.cursor_path.replace("%USERNAME%", os.getenv("USERNAME", ""))
        
        self.logger.info("Cursor Bridge initialized")
    
    def open_cursor(self, command: str = ""):
        """Open Cursor IDE"""
        try:
            if not os.path.exists(self.cursor_path):
                # Try alternative paths
                alternative_paths = [
                    "C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Cursor\\Cursor.exe",
                    "C:\\Program Files\\Cursor\\Cursor.exe",
                    "cursor",  # Try PATH
                ]
                
                for path in alternative_paths:
                    if "%USERNAME%" in path:
                        path = path.replace("%USERNAME%", os.getenv("USERNAME", ""))
                    
                    if os.path.exists(path) or path == "cursor":
                        self.cursor_path = path
                        break
                else:
                    raise FileNotFoundError("Cursor executable not found")
            
            # Launch Cursor
            if self.cursor_path == "cursor":
                self.cursor_process = subprocess.Popen(["cursor"])
            else:
                self.cursor_process = subprocess.Popen([self.cursor_path])
            
            # Wait for window to appear
            time.sleep(2)
            
            # Find Cursor window
            self._find_cursor_window()
            
            self.logger.command_execution("open cursor", "cursor_bridge.open_cursor", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to open Cursor: {e}")
            return False
    
    def _find_cursor_window(self):
        """Find and store Cursor window reference"""
        try:
            windows = gw.getAllTitles()
            for window_title in windows:
                if "cursor" in window_title.lower():
                    self.cursor_window = gw.getWindowsWithTitle(window_title)[0]
                    self.logger.debug(f"Found Cursor window: {window_title}")
                    return True
            
            self.logger.warning("Cursor window not found")
            return False
            
        except Exception as e:
            self.logger.error(f"Error finding Cursor window: {e}")
            return False
    
    def focus_cursor(self):
        """Focus Cursor window"""
        try:
            if self._find_cursor_window() and self.cursor_window:
                self.cursor_window.activate()
                self.logger.debug("Cursor window focused")
                return True
            return False
        except Exception as e:
            self.logger.error(f"Error focusing Cursor: {e}")
            return False
    
    def open_file(self, file_path: str):
        """Open a file in Cursor"""
        try:
            if not os.path.exists(file_path):
                self.logger.error(f"File not found: {file_path}")
                return False
            
            # Focus Cursor first
            if not self.focus_cursor():
                return False
            
            # Use Ctrl+O to open file
            pyautogui.hotkey('ctrl', 'o')
            time.sleep(0.5)
            
            # Type file path
            pyautogui.write(file_path)
            time.sleep(0.5)
            
            # Press Enter
            pyautogui.press('enter')
            
            self.logger.command_execution(f"open file {file_path}", "cursor_bridge.open_file", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error opening file: {e}")
            return False
    
    def save_file(self):
        """Save current file"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 's')
            self.logger.command_execution("save file", "cursor_bridge.save_file", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving file: {e}")
            return False
    
    def save_all_files(self):
        """Save all open files"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 'shift', 's')
            self.logger.command_execution("save all files", "cursor_bridge.save_all_files", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error saving all files: {e}")
            return False
    
    def close_file(self):
        """Close current file"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 'w')
            self.logger.command_execution("close file", "cursor_bridge.close_file", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error closing file: {e}")
            return False
    
    def new_file(self):
        """Create new file"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 'n')
            self.logger.command_execution("new file", "cursor_bridge.new_file", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating new file: {e}")
            return False
    
    def find_text(self, search_text: str):
        """Find text in current file"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 'f')
            time.sleep(0.5)
            pyautogui.write(search_text)
            
            self.logger.command_execution(f"find text {search_text}", "cursor_bridge.find_text", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error finding text: {e}")
            return False
    
    def replace_text(self, search_text: str, replace_text: str):
        """Replace text in current file"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 'h')
            time.sleep(0.5)
            pyautogui.write(search_text)
            pyautogui.press('tab')
            pyautogui.write(replace_text)
            
            self.logger.command_execution(f"replace text", "cursor_bridge.replace_text", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error replacing text: {e}")
            return False
    
    def go_to_line(self, line_number: int):
        """Go to specific line number"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 'g')
            time.sleep(0.5)
            pyautogui.write(str(line_number))
            pyautogui.press('enter')
            
            self.logger.command_execution(f"go to line {line_number}", "cursor_bridge.go_to_line", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error going to line: {e}")
            return False
    
    def toggle_comment(self):
        """Toggle comment on current line"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', '/')
            self.logger.command_execution("toggle comment", "cursor_bridge.toggle_comment", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error toggling comment: {e}")
            return False
    
    def format_document(self):
        """Format current document"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('shift', 'alt', 'f')
            self.logger.command_execution("format document", "cursor_bridge.format_document", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error formatting document: {e}")
            return False
    
    def run_terminal(self):
        """Open integrated terminal"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', '`')
            self.logger.command_execution("run terminal", "cursor_bridge.run_terminal", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error opening terminal: {e}")
            return False
    
    def toggle_sidebar(self):
        """Toggle sidebar"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 'b')
            self.logger.command_execution("toggle sidebar", "cursor_bridge.toggle_sidebar", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error toggling sidebar: {e}")
            return False
    
    def zoom_in(self):
        """Zoom in"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', '=')
            self.logger.command_execution("zoom in", "cursor_bridge.zoom_in", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error zooming in: {e}")
            return False
    
    def zoom_out(self):
        """Zoom out"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', '-')
            self.logger.command_execution("zoom out", "cursor_bridge.zoom_out", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error zooming out: {e}")
            return False
    
    def execute_command(self, command: str):
        """Execute Cursor command palette command"""
        try:
            if not self.focus_cursor():
                return False
            
            pyautogui.hotkey('ctrl', 'shift', 'p')
            time.sleep(0.5)
            pyautogui.write(command)
            pyautogui.press('enter')
            
            self.logger.command_execution(f"execute command {command}", "cursor_bridge.execute_command", True)
            return True
            
        except Exception as e:
            self.logger.error(f"Error executing command: {e}")
            return False
    
    def get_current_file_info(self) -> Dict[str, Any]:
        """Get information about current file"""
        try:
            # This would require more sophisticated integration
            # For now, return basic info
            return {
                "has_focus": self.cursor_window is not None and self.cursor_window.isActive,
                "window_title": self.cursor_window.title if self.cursor_window else None
            }
        except Exception as e:
            self.logger.error(f"Error getting file info: {e}")
            return {}
    
    def is_cursor_running(self) -> bool:
        """Check if Cursor is running"""
        try:
            if self.cursor_process:
                return self.cursor_process.poll() is None
            return self._find_cursor_window()
        except Exception as e:
            self.logger.error(f"Error checking Cursor status: {e}")
            return False


def main():
    """Test the Cursor bridge"""
    bridge = CursorBridge()
    
    # Test Cursor status check
    is_running = bridge.is_cursor_running()
    print(f"Cursor running: {is_running}")
    
    # Test window finding
    found_window = bridge._find_cursor_window()
    print(f"Cursor window found: {found_window}")
    
    print("Cursor bridge test completed.")


if __name__ == "__main__":
    main() 