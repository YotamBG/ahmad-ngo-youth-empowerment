"""
Configuration Manager - Handles loading and managing application settings
"""

import yaml
import os
from typing import Any, Dict, Optional
from loguru import logger


class ConfigManager:
    """Manages application configuration loading and access"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config_path = config_path
        self.config = {}
        self.load_config()
    
    def load_config(self):
        """Load configuration from YAML file"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config = yaml.safe_load(f) or {}
                logger.info(f"Configuration loaded from {self.config_path}")
            else:
                logger.warning(f"Config file not found: {self.config_path}")
                self.config = {}
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            self.config = {}
    
    def reload_config(self):
        """Reload configuration from file"""
        self.load_config()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation"""
        try:
            keys = key.split('.')
            value = self.config
            
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            
            return value
        except Exception as e:
            logger.debug(f"Error getting config key '{key}': {e}")
            return default
    
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation"""
        try:
            keys = key.split('.')
            config = self.config
            
            # Navigate to the parent of the target key
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set the value
            config[keys[-1]] = value
            logger.debug(f"Set config key '{key}' to '{value}'")
            
        except Exception as e:
            logger.error(f"Error setting config key '{key}': {e}")
    
    def save_config(self, path: Optional[str] = None):
        """Save current configuration to file"""
        try:
            save_path = path or self.config_path
            os.makedirs(os.path.dirname(save_path), exist_ok=True)
            
            with open(save_path, 'w', encoding='utf-8') as f:
                yaml.dump(self.config, f, default_flow_style=False, indent=2)
            
            logger.info(f"Configuration saved to {save_path}")
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
    
    def get_section(self, section: str) -> Dict[str, Any]:
        """Get entire configuration section"""
        return self.get(section, {})
    
    def has_section(self, section: str) -> bool:
        """Check if configuration section exists"""
        return section in self.config
    
    def merge_config(self, other_config: Dict[str, Any]):
        """Merge another configuration dictionary"""
        try:
            self._merge_dicts(self.config, other_config)
            logger.info("Configuration merged successfully")
        except Exception as e:
            logger.error(f"Error merging configuration: {e}")
    
    def _merge_dicts(self, base: Dict, update: Dict):
        """Recursively merge dictionaries"""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_dicts(base[key], value)
            else:
                base[key] = value
    
    def validate_config(self) -> bool:
        """Validate configuration structure"""
        required_sections = ['voice', 'tts', 'system']
        
        for section in required_sections:
            if not self.has_section(section):
                logger.error(f"Missing required configuration section: {section}")
                return False
        
        return True
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration"""
        return self.config.copy()
    
    def export_config(self, path: str):
        """Export configuration to specified path"""
        try:
            self.save_config(path)
        except Exception as e:
            logger.error(f"Error exporting configuration: {e}")


class EnvironmentConfigManager(ConfigManager):
    """Configuration manager that also reads from environment variables"""
    
    def __init__(self, config_path: str = "config/settings.yaml"):
        super().__init__(config_path)
        self.load_environment_overrides()
    
    def load_environment_overrides(self):
        """Load configuration overrides from environment variables"""
        env_prefix = "VOICE_OS_"
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                # Convert environment variable name to config key
                config_key = key[len(env_prefix):].lower().replace('_', '.')
                
                # Try to convert value to appropriate type
                try:
                    # Try to convert to int
                    if value.isdigit():
                        value = int(value)
                    # Try to convert to float
                    elif value.replace('.', '').isdigit():
                        value = float(value)
                    # Try to convert to boolean
                    elif value.lower() in ['true', 'false']:
                        value = value.lower() == 'true'
                except ValueError:
                    pass  # Keep as string
                
                self.set(config_key, value)
                logger.debug(f"Environment override: {config_key} = {value}")
    
    def get_with_env_fallback(self, key: str, env_var: str, default: Any = None) -> Any:
        """Get config value with environment variable fallback"""
        # Try config first
        value = self.get(key, None)
        
        if value is not None:
            return value
        
        # Try environment variable
        env_value = os.environ.get(env_var)
        if env_value is not None:
            return env_value
        
        return default


def create_default_config() -> Dict[str, Any]:
    """Create default configuration structure"""
    return {
        'voice': {
            'engine': 'whisper',
            'language': 'en-US',
            'timeout': 5.0,
            'phrase_time_limit': 10.0,
            'ambient_noise_adjustment': True,
            'energy_threshold': 4000,
            'dynamic_energy_threshold': True
        },
        'tts': {
            'engine': 'pyttsx3',
            'voice_rate': 150,
            'voice_volume': 0.9,
            'voice_id': 'default'
        },
        'lenovo_ai': {
            'enabled': True,
            'api_endpoint': 'http://localhost:8080/api',
            'wake_word': 'Hey Lenovo',
            'shortcut_key': 'ctrl+shift+space'
        },
        'cursor': {
            'executable_path': 'C:\\Users\\%USERNAME%\\AppData\\Local\\Programs\\Cursor\\Cursor.exe',
            'api_enabled': True,
            'auto_focus': True,
            'command_prefix': '/'
        },
        'llm': {
            'local': {
                'enabled': True,
                'model': 'llama3',
                'endpoint': 'http://localhost:11434',
                'max_tokens': 2048,
                'temperature': 0.7
            },
            'cloud': {
                'provider': 'openai',
                'api_key': '',
                'model': 'gpt-4',
                'max_tokens': 4096,
                'temperature': 0.7
            }
        },
        'system': {
            'screenshot_dir': './screenshots',
            'log_level': 'INFO',
            'auto_save': True,
            'backup_enabled': True
        },
        'audio': {
            'input_device': 'default',
            'output_device': 'default',
            'sample_rate': 16000,
            'channels': 1,
            'chunk_size': 1024
        },
        'commands': {
            'confidence_threshold': 0.7,
            'fuzzy_matching': True,
            'auto_correction': True,
            'context_awareness': True
        },
        'logging': {
            'level': 'INFO',
            'file': 'voice_os.log',
            'max_size': '10MB',
            'backup_count': 5
        },
        'development': {
            'debug_mode': False,
            'hot_reload': True,
            'test_mode': False
        }
    }


def main():
    """Test the configuration manager"""
    # Create default config
    default_config = create_default_config()
    
    # Initialize config manager
    config = ConfigManager()
    
    # Test getting values
    print(f"Voice engine: {config.get('voice.engine')}")
    print(f"TTS rate: {config.get('tts.voice_rate')}")
    print(f"Wake word: {config.get('lenovo_ai.wake_word')}")
    
    # Test setting values
    config.set('test.new_key', 'test_value')
    print(f"Test value: {config.get('test.new_key')}")
    
    # Test environment config
    env_config = EnvironmentConfigManager()
    print(f"Environment config loaded: {env_config.get_all()}")


if __name__ == "__main__":
    main() 