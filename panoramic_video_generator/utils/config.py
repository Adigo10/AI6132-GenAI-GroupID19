"""Configuration utilities for panoramic video generation."""

import yaml
from typing import Dict, Any, Optional
import os


class Config:
    """Configuration manager for panoramic video generation."""
    
    DEFAULT_CONFIG = {
        'video': {
            'fps': 30,
            'num_frames': 120,
            'output_size': [1920, 1080],
            'codec': 'mp4v',
        },
        'camera': {
            'radius': 5.0,
            'height': 10.0,
            'start_angle': 0.0,
            'trajectory_type': 'circular',  # 'circular' or 'top_view'
        },
        'character': {
            'scale': 1.0,
            'target_size': None,  # Auto-scale if None
        },
        'environment': {
            'type': 'color',  # 'image', 'color', or 'gradient'
            'color': [135, 206, 235],  # Sky blue
            'gradient_top': [135, 206, 235],
            'gradient_bottom': [34, 139, 34],
        }
    }
    
    def __init__(self, config_dict: Optional[Dict[str, Any]] = None):
        """
        Initialize configuration.
        
        Args:
            config_dict: Optional dictionary with configuration values
        """
        self.config = self.DEFAULT_CONFIG.copy()
        if config_dict:
            self._update_config(config_dict)
    
    def _update_config(self, updates: Dict[str, Any]) -> None:
        """Recursively update configuration."""
        for key, value in updates.items():
            if key in self.config and isinstance(self.config[key], dict) and isinstance(value, dict):
                self.config[key].update(value)
            else:
                self.config[key] = value
    
    @classmethod
    def from_yaml(cls, yaml_path: str) -> 'Config':
        """
        Load configuration from YAML file.
        
        Args:
            yaml_path: Path to YAML configuration file
            
        Returns:
            Config object
        """
        with open(yaml_path, 'r') as f:
            config_dict = yaml.safe_load(f)
        return cls(config_dict)
    
    def save_yaml(self, yaml_path: str) -> None:
        """
        Save configuration to YAML file.
        
        Args:
            yaml_path: Path to save YAML configuration
        """
        os.makedirs(os.path.dirname(yaml_path) or '.', exist_ok=True)
        with open(yaml_path, 'w') as f:
            yaml.dump(self.config, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by key path (e.g., 'video.fps').
        
        Args:
            key: Configuration key path
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value
    
    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value by key path.
        
        Args:
            key: Configuration key path
            value: Value to set
        """
        keys = key.split('.')
        config = self.config
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        config[keys[-1]] = value
