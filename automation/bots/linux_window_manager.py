#!/usr/bin/env python3
"""
Linux Window Manager - X11-based window control for Linux systems
Replacement for PyGetWindow which doesn't support Linux
"""

import subprocess
import time
import os
from typing import List, Optional, Dict

class LinuxWindow:
    """Represents a window on Linux"""
    
    def __init__(self, window_id: str, title: str, pid: str = ""):
        self.id = window_id
        self.title = title
        self.pid = pid
    
    def activate(self):
        """Activate/focus this window"""
        try:
            # Use wmctrl to activate window
            subprocess.run(['wmctrl', '-i', '-a', self.id], check=True)
            time.sleep(0.5)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            try:
                # Fallback to xdotool
                subprocess.run(['xdotool', 'windowactivate', self.id], check=True)
                time.sleep(0.5)
                return True
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False
    
    def close(self):
        """Close this window"""
        try:
            subprocess.run(['wmctrl', '-i', '-c', self.id], check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

class LinuxWindowManager:
    """Linux window manager using X11 tools"""
    
    def __init__(self):
        self.check_dependencies()
    
    def check_dependencies(self):
        """Check if required tools are available"""
        self.has_wmctrl = self.command_exists('wmctrl')
        self.has_xdotool = self.command_exists('xdotool')
        self.has_xwininfo = self.command_exists('xwininfo')
        
        if not (self.has_wmctrl or self.has_xdotool):
            print("⚠️ Window management tools not found. Install with:")
            print("   sudo apt install wmctrl xdotool")
    
    def command_exists(self, command: str) -> bool:
        """Check if a command exists"""
        try:
            subprocess.run(['which', command], check=True, 
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_all_windows(self) -> List[LinuxWindow]:
        """Get all open windows"""
        windows = []
        
        if self.has_wmctrl:
            try:
                result = subprocess.run(['wmctrl', '-l'], capture_output=True, text=True, check=True)
                
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(None, 3)
                        if len(parts) >= 4:
                            window_id = parts[0]
                            title = parts[3]
                            windows.append(LinuxWindow(window_id, title))
                            
            except subprocess.CalledProcessError:
                pass
        
        return windows
    
    def find_windows_by_title(self, title_pattern: str) -> List[LinuxWindow]:
        """Find windows matching title pattern"""
        all_windows = self.get_all_windows()
        matching_windows = []
        
        for window in all_windows:
            if title_pattern.lower() in window.title.lower():
                matching_windows.append(window)
        
        return matching_windows
    
    def find_cursor_window(self) -> Optional[LinuxWindow]:
        """Find Cursor IDE window"""
        cursor_patterns = ['cursor', 'Cursor']
        
        for pattern in cursor_patterns:
            windows = self.find_windows_by_title(pattern)
            if windows:
                return windows[0]  # Return first match
        
        return None
    
    def activate_cursor(self) -> bool:
        """Activate Cursor window"""
        cursor_window = self.find_cursor_window()
        if cursor_window:
            return cursor_window.activate()
        return False
    
    def open_cursor(self) -> bool:
        """Open Cursor if not already open"""
        # Check if Cursor is already open
        if self.find_cursor_window():
            return self.activate_cursor()
        
        # Try to launch Cursor
        cursor_commands = [
            'cursor',
            '/usr/bin/cursor',
            '/usr/local/bin/cursor',
            '/snap/bin/cursor',
            os.path.expanduser('~/.local/bin/cursor')
        ]
        
        for cmd in cursor_commands:
            try:
                subprocess.Popen([cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                time.sleep(3)  # Wait for Cursor to start
                
                # Check if it opened
                if self.find_cursor_window():
                    return self.activate_cursor()
                    
            except FileNotFoundError:
                continue
        
        return False

# Compatibility wrapper to mimic PyGetWindow interface
def getAllWindows():
    """Get all windows - compatibility function"""
    manager = LinuxWindowManager()
    return manager.get_all_windows()

# Create global manager instance
window_manager = LinuxWindowManager() 