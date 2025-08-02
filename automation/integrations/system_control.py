#!/usr/bin/env python3
"""
Linux-Compatible System Control Module
"""

import os
import sys
import subprocess
import platform
from typing import Dict, List, Optional
from loguru import logger

try:
    import psutil
except ImportError:
    psutil = None

class SystemControl:
    """Linux-compatible system control functions"""
    
    def __init__(self):
        self.platform = platform.system()
        logger.info(f"SystemControl initialized for {self.platform}")
    
    def get_system_info(self) -> Dict[str, str]:
        """Get basic system information"""
        try:
            info = {
                'system': self.platform,
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version()
            }
            
            # Get additional Linux-specific info
            if self.platform == "Linux":
                try:
                    # Get OS version
                    with open('/etc/os-release', 'r') as f:
                        for line in f:
                            if line.startswith('PRETTY_NAME'):
                                info['os_version'] = line.split('=')[1].strip().strip('"')
                                break
                except:
                    info['os_version'] = "Unknown"
            
            return info
        except Exception as e:
            logger.error(f"Error getting system info: {e}")
            return {'system': 'Unknown'}
    
    def take_screenshot(self, filename: str = "screenshot.png") -> Optional[str]:
        """Take a screenshot using Linux-compatible methods"""
        try:
            # Try different screenshot tools
            tools = [
                ["gnome-screenshot", "-f", filename],
                ["import", "-window", "root", filename],
                ["scrot", filename],
                ["maim", filename]
            ]
            
            for tool in tools:
                try:
                    result = subprocess.run(tool, capture_output=True, timeout=10)
                    if result.returncode == 0 and os.path.exists(filename):
                        logger.info(f"Screenshot taken with {tool[0]}: {filename}")
                        return filename
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    continue
            
            logger.warning("No screenshot tool available")
            return None
            
        except Exception as e:
            logger.error(f"Error taking screenshot: {e}")
            return None
    
    def get_running_processes(self) -> List[Dict[str, str]]:
        """Get list of running processes"""
        try:
            if psutil:
                processes = []
                for proc in psutil.process_iter(['pid', 'name', 'status']):
                    try:
                        processes.append({
                            'pid': str(proc.info['pid']),
                            'name': proc.info['name'],
                            'status': proc.info['status']
                        })
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        continue
                return processes
            else:
                # Fallback using ps command
                result = subprocess.run(['ps', 'aux'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]  # Skip header
                    processes = []
                    for line in lines:
                        parts = line.split()
                        if len(parts) >= 11:
                            processes.append({
                                'pid': parts[1],
                                'name': parts[10],
                                'status': parts[7] if len(parts) > 7 else 'Unknown'
                            })
                    return processes
                else:
                    return []
        except Exception as e:
            logger.error(f"Error getting processes: {e}")
            return []
    
    def launch_application(self, app_name: str) -> bool:
        """Launch an application"""
        try:
            # Try different methods to launch apps
            methods = [
                [app_name],
                ["xdg-open", app_name],
                ["gnome-open", app_name],
                ["kde-open", app_name]
            ]
            
            for method in methods:
                try:
                    result = subprocess.run(method, capture_output=True, timeout=10)
                    if result.returncode == 0:
                        logger.info(f"Application launched: {app_name}")
                        return True
                except (subprocess.TimeoutExpired, FileNotFoundError):
                    continue
            
            logger.warning(f"Could not launch application: {app_name}")
            return False
            
        except Exception as e:
            logger.error(f"Error launching application: {e}")
            return False
    
    def execute_command(self, command: str) -> Dict[str, any]:
        """Execute a system command"""
        try:
            result = subprocess.run(
                command.split(),
                capture_output=True,
                text=True,
                timeout=30
            )
            
            return {
                'success': result.returncode == 0,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'stdout': '',
                'stderr': 'Command timed out',
                'returncode': -1
            }
        except Exception as e:
            return {
                'success': False,
                'stdout': '',
                'stderr': str(e),
                'returncode': -1
            }
    
    def get_memory_usage(self) -> Dict[str, float]:
        """Get memory usage information"""
        try:
            if psutil:
                memory = psutil.virtual_memory()
                return {
                    'total': memory.total / (1024**3),  # GB
                    'available': memory.available / (1024**3),  # GB
                    'used': memory.used / (1024**3),  # GB
                    'percent': memory.percent
                }
            else:
                # Fallback using /proc/meminfo
                with open('/proc/meminfo', 'r') as f:
                    lines = f.readlines()
                
                mem_info = {}
                for line in lines:
                    if ':' in line:
                        key, value = line.split(':', 1)
                        mem_info[key.strip()] = int(value.strip().split()[0])
                
                total = mem_info.get('MemTotal', 0) / 1024  # MB
                available = mem_info.get('MemAvailable', 0) / 1024  # MB
                used = total - available
                
                return {
                    'total': total / 1024,  # GB
                    'available': available / 1024,  # GB
                    'used': used / 1024,  # GB
                    'percent': (used / total * 100) if total > 0 else 0
                }
                
        except Exception as e:
            logger.error(f"Error getting memory usage: {e}")
            return {'total': 0, 'available': 0, 'used': 0, 'percent': 0}
    
    def get_disk_usage(self) -> Dict[str, float]:
        """Get disk usage information"""
        try:
            if psutil:
                disk = psutil.disk_usage('/')
                return {
                    'total': disk.total / (1024**3),  # GB
                    'used': disk.used / (1024**3),  # GB
                    'free': disk.free / (1024**3),  # GB
                    'percent': (disk.used / disk.total * 100) if disk.total > 0 else 0
                }
            else:
                # Fallback using df command
                result = subprocess.run(['df', '/'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    lines = result.stdout.strip().split('\n')[1:]  # Skip header
                    if lines:
                        parts = lines[0].split()
                        if len(parts) >= 4:
                            total = int(parts[1]) / 1024  # MB to GB
                            used = int(parts[2]) / 1024  # MB to GB
                            free = int(parts[3]) / 1024  # MB to GB
                            return {
                                'total': total,
                                'used': used,
                                'free': free,
                                'percent': (used / total * 100) if total > 0 else 0
                            }
                
                return {'total': 0, 'used': 0, 'free': 0, 'percent': 0}
                
        except Exception as e:
            logger.error(f"Error getting disk usage: {e}")
            return {'total': 0, 'used': 0, 'free': 0, 'percent': 0} 