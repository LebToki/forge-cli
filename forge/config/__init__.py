"""Configuration management for FORGE CLI."""

import os
import json
from pathlib import Path
from typing import Optional, Any, Dict
import toml


class Config:
    """Configuration manager for FORGE."""
    
    DEFAULT_CONFIG = {
        "deepseek": {
            "api_key": "",
            "model": "deepseek-chat",
            "temperature": 0.7,
            "max_tokens": 4096
        },
        "github": {
            "token": "",
            "default_branch": "main"
        },
        "general": {
            "workspace": "",
            "auto_confirm": False,
            "verbose": False
        }
    }
    
    def __init__(self, config_path: Optional[Path] = None):
        """Initialize configuration.
        
        Args:
            config_path: Optional custom config file path.
        """
        self.config_dir = Path.home() / ".forge"
        self.config_file = config_path or self.config_dir / "config.toml"
        self._config: Dict[str, Any] = {}
        self._load_config()
    
    def _load_config(self) -> None:
        """Load configuration from file."""
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(exist_ok=True)
        
        # Load existing config or use defaults
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded = toml.load(f)
                    # Merge with defaults
                    self._config = self._deep_merge(self.DEFAULT_CONFIG.copy(), loaded)
            except Exception:
                self._config = self.DEFAULT_CONFIG.copy()
        else:
            self._config = self.DEFAULT_CONFIG.copy()
    
    def _deep_merge(self, base: Dict, update: Dict) -> Dict:
        """Deep merge two dictionaries."""
        for key, value in update.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                base[key] = self._deep_merge(base[key], value)
            else:
                base[key] = value
        return base
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        self.config_dir.mkdir(exist_ok=True)
        with open(self.config_file, 'w', encoding='utf-8') as f:
            toml.dump(self._config, f)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value using dot notation (e.g., 'deepseek.model').
        
        Args:
            key: Configuration key in dot notation.
            default: Default value if key not found.
            
        Returns:
            The configuration value.
        """
        keys = key.split('.')
        value = self._config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set a config value using dot notation.
        
        Args:
            key: Configuration key in dot notation.
            value: Value to set.
        """
        keys = key.split('.')
        target = self._config
        
        # Navigate to the correct nested level
        for k in keys[:-1]:
            if k not in target:
                target[k] = {}
            target = target[k]
        
        # Set the value
        target[keys[-1]] = value
        self._save_config()
    
    def get_deepseek_api_key(self) -> Optional[str]:
        """Get DeepSeek API key from config or environment.
        
        Returns:
            API key if found, None otherwise.
        """
        # First check environment variable
        env_key = os.getenv('DEEPSEEK_API_KEY')
        if env_key:
            return env_key
        
        # Then check config
        return self.get('deepseek.api_key')
    
    def get_github_token(self) -> Optional[str]:
        """Get GitHub token from config or environment.
        
        Returns:
            GitHub token if found, None otherwise.
        """
        # First check environment variable
        env_token = os.getenv('GITHUB_TOKEN')
        if env_token:
            return env_token
        
        # Then check config
        return self.get('github.token')
    
    def is_configured(self, service: str) -> bool:
        """Check if a service is configured.
        
        Args:
            service: Service name ('deepseek' or 'github').
            
        Returns:
            True if configured, False otherwise.
        """
        if service == 'deepseek':
            return bool(self.get_deepseek_api_key())
        elif service == 'github':
            return bool(self.get_github_token())
        return False
    
    def list_all(self) -> Dict[str, Any]:
        """Get all configuration values.
        
        Returns:
            Dictionary of all configuration values (sensitive data masked).
        """
        result = {}
        
        for section, values in self._config.items():
            if isinstance(values, dict):
                result[section] = {}
                for key, value in values.items():
                    # Mask sensitive values
                    if key in ('api_key', 'token', 'password', 'secret'):
                        if value:
                            result[section][key] = "***SET***"
                        else:
                            result[section][key] = ""
                    else:
                        result[section][key] = value
            else:
                result[section] = values
        
        return result
    
    def reset(self) -> None:
        """Reset configuration to defaults."""
        self._config = self.DEFAULT_CONFIG.copy()
        self._save_config()


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance.
    
    Returns:
        The global Config instance.
    """
    global _config
    if _config is None:
        _config = Config()
    return _config
