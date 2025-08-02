"""
Logger Utility - Centralized logging configuration
"""

import sys
import os
from loguru import logger
from typing import Optional


def setup_logger(
    level: str = "INFO",
    log_file: str = "voice_os.log",
    max_size: str = "10MB",
    backup_count: int = 5,
    format_string: Optional[str] = None
):
    """Setup application logging with loguru"""
    
    # Remove default handler
    logger.remove()
    
    # Default format if not specified
    if format_string is None:
        format_string = (
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        )
    
    # Console handler
    logger.add(
        sys.stdout,
        format=format_string,
        level=level,
        colorize=True
    )
    
    # File handler
    if log_file:
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        
        logger.add(
            log_file,
            format=format_string,
            level=level,
            rotation=max_size,
            retention=backup_count,
            compression="zip"
        )
    
    logger.info(f"Logger initialized with level: {level}")


def get_logger(name: str = None):
    """Get a logger instance with optional name"""
    if name:
        return logger.bind(name=name)
    return logger


class VoiceOSLogger:
    """Specialized logger for Voice OS application"""
    
    def __init__(self, component: str = "voice_os"):
        self.component = component
        self.logger = logger.bind(component=component)
    
    def voice_command(self, command: str, confidence: float = None):
        """Log voice command recognition"""
        if confidence:
            self.logger.info(f"Voice command: '{command}' (confidence: {confidence:.2f})")
        else:
            self.logger.info(f"Voice command: '{command}'")
    
    def command_execution(self, command: str, action: str, success: bool = True):
        """Log command execution"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.info(f"Command execution: {command} -> {action} [{status}]")
    
    def error(self, message: str, error: Exception = None):
        """Log error with optional exception"""
        if error:
            self.logger.error(f"{message}: {error}")
        else:
            self.logger.error(message)
    
    def warning(self, message: str):
        """Log warning"""
        self.logger.warning(message)
    
    def debug(self, message: str):
        """Log debug message"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """Log info message"""
        self.logger.info(message)
    
    def tts_speak(self, text: str):
        """Log TTS speech"""
        self.logger.debug(f"TTS speaking: '{text[:50]}{'...' if len(text) > 50 else ''}'")
    
    def system_action(self, action: str, details: str = None):
        """Log system action"""
        if details:
            self.logger.info(f"System action: {action} - {details}")
        else:
            self.logger.info(f"System action: {action}")
    
    def llm_request(self, prompt: str, response: str = None):
        """Log LLM request/response"""
        self.logger.debug(f"LLM request: '{prompt[:100]}{'...' if len(prompt) > 100 else ''}'")
        if response:
            self.logger.debug(f"LLM response: '{response[:100]}{'...' if len(response) > 100 else ''}'")
    
    def performance(self, operation: str, duration: float):
        """Log performance metrics"""
        self.logger.debug(f"Performance: {operation} took {duration:.3f}s")


class PerformanceLogger:
    """Logger for performance monitoring"""
    
    def __init__(self):
        self.logger = logger.bind(component="performance")
        self.timers = {}
    
    def start_timer(self, name: str):
        """Start a performance timer"""
        import time
        self.timers[name] = time.time()
        self.logger.debug(f"Started timer: {name}")
    
    def end_timer(self, name: str):
        """End a performance timer and log duration"""
        import time
        if name in self.timers:
            duration = time.time() - self.timers[name]
            self.logger.info(f"Timer {name}: {duration:.3f}s")
            del self.timers[name]
            return duration
        return None
    
    def log_memory_usage(self):
        """Log current memory usage"""
        import psutil
        process = psutil.Process()
        memory_info = process.memory_info()
        self.logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.1f} MB")
    
    def log_cpu_usage(self):
        """Log current CPU usage"""
        import psutil
        cpu_percent = psutil.cpu_percent(interval=1)
        self.logger.info(f"CPU usage: {cpu_percent:.1f}%")


class SecurityLogger:
    """Logger for security-related events"""
    
    def __init__(self):
        self.logger = logger.bind(component="security")
    
    def authentication_attempt(self, user: str, success: bool):
        """Log authentication attempt"""
        status = "SUCCESS" if success else "FAILED"
        self.logger.warning(f"Authentication attempt: {user} [{status}]")
    
    def command_attempt(self, command: str, user: str = "unknown"):
        """Log command execution attempt"""
        self.logger.info(f"Command attempt: {command} by {user}")
    
    def system_access(self, component: str, user: str = "unknown"):
        """Log system access"""
        self.logger.info(f"System access: {component} by {user}")
    
    def error_access(self, error: str, user: str = "unknown"):
        """Log access error"""
        self.logger.error(f"Access error: {error} by {user}")


def create_component_logger(component: str):
    """Create a logger for a specific component"""
    return VoiceOSLogger(component)


def setup_development_logging():
    """Setup logging for development environment"""
    setup_logger(
        level="DEBUG",
        log_file="logs/voice_os_dev.log",
        format_string=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{component}</cyan> | "
            "<level>{message}</level>"
        )
    )


def setup_production_logging():
    """Setup logging for production environment"""
    setup_logger(
        level="INFO",
        log_file="logs/voice_os.log",
        format_string=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{component} | "
            "{message}"
        )
    )


def main():
    """Test the logger setup"""
    # Setup logger
    setup_logger()
    
    # Test different loggers
    voice_logger = VoiceOSLogger("voice_engine")
    perf_logger = PerformanceLogger()
    sec_logger = SecurityLogger()
    
    # Test logging
    voice_logger.voice_command("open cursor", 0.95)
    voice_logger.command_execution("open cursor", "cursor_bridge.open_cursor", True)
    
    perf_logger.start_timer("test_operation")
    import time
    time.sleep(0.1)
    perf_logger.end_timer("test_operation")
    
    sec_logger.command_attempt("open cursor", "user1")
    
    print("Logger test completed.")


if __name__ == "__main__":
    main() 