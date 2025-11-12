"""
Settings Manager Module
Manages engine configuration and user preferences.
Generic settings system for render, audio, window, and performance.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional, List
import copy


class SettingsManager:
    """
    Generic settings manager for engine configuration.
    Handles loading, saving, and accessing engine settings.
    """
    
    def __init__(self, config_dir: str = "config", app_name: str = "engine"):
        """
        Initialize the settings manager.
        
        Args:
            config_dir: Directory for config files
            app_name: Application name for settings file
        """
        self.config_dir = Path(config_dir)
        self.app_name = app_name
        
        # Create config directory if it doesn't exist
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        # Settings files
        self.default_file = self.config_dir / "default_settings.json"
        self.user_file = self.config_dir / f"{app_name}_settings.json"
        
        # Settings storage
        self.settings: Dict[str, Any] = {}
        self.defaults: Dict[str, Any] = {}
        
        # Callbacks for when settings change
        self._callbacks: Dict[str, List[callable]] = {}
        
        # Load settings
        self._initialize()
    
    def _initialize(self):
        """Initialize and load settings."""
        # Get default settings
        self.defaults = self._get_default_settings()
        
        # Save defaults if file doesn't exist
        if not self.default_file.exists():
            self._save_json(self.default_file, self.defaults)
        
        # Start with defaults
        self.settings = copy.deepcopy(self.defaults)
        
        # Load and merge user settings
        if self.user_file.exists():
            try:
                user_data = self._load_json(self.user_file)
                self._merge_settings(self.settings, user_data)
                print(f"[OK] Loaded user settings from {self.user_file}")
            except Exception as e:
                print(f"[WARNING] Failed to load user settings: {e}")
                print(f"[INFO] Using default settings")
        else:
            print(f"[INFO] No user settings found, using defaults")
    
    def _get_default_settings(self) -> Dict[str, Any]:
        """Get default engine settings."""
        return {
            "engine": {
                "version": "1.0.0",
                "name": self.app_name,
                "debug_mode": False,
                "log_level": "info"  # debug, info, warning, error
            },
            
            "window": {
                "width": 1280,
                "height": 720,
                "fullscreen": False,
                "borderless": False,
                "resizable": True,
                "vsync": True,
                "title": "Engine Application"
            },
            
            "graphics": {
                # Performance
                "target_fps": 60,
                "fps_limit": True,
                
                # Quality
                "msaa_samples": 4,  # 0, 2, 4, 8, 16
                "anisotropic_filtering": 16,  # 1, 2, 4, 8, 16
                "texture_quality": 1.0,  # 0.5=low, 1.0=normal, 2.0=high
                
                # Shadows
                "shadows_enabled": True,
                "shadow_map_size": 2048,  # 512, 1024, 2048, 4096
                "shadow_cascades": 3,
                "shadow_distance": 100.0,
                
                # Post-processing
                "bloom": True,
                "bloom_intensity": 0.3,
                "tone_mapping": True,
                "gamma": 2.2,
                "exposure": 1.0,
                
                # Advanced
                "render_distance": 1000.0,
                "lod_bias": 1.0,
                "culling_enabled": True,
                "wireframe_mode": False
            },
            
            "audio": {
                # Volume levels (0.0 - 1.0)
                "master_volume": 0.8,
                "effects_volume": 0.7,
                "music_volume": 0.6,
                "ambient_volume": 0.5,
                
                # Settings
                "muted": False,
                "spatial_audio": True,
                "doppler_effect": True,
                "reverb": True,
                "max_sound_sources": 32,
                
                # Quality
                "sample_rate": 44100,  # 22050, 44100, 48000
                "bit_depth": 16  # 8, 16, 24
            },
            
            "input": {
                "mouse_sensitivity": 1.0,
                "mouse_smoothing": True,
                "mouse_invert_y": False,
                "mouse_invert_x": False,
                "keyboard_repeat": True,
                "gamepad_enabled": True,
                "gamepad_deadzone": 0.15
            },
            
            "ui": {
                "scale": 1.0,
                "font_size": 16,
                "show_fps": False,
                "show_debug_info": False,
                "fade_duration": 0.3,
                "tooltip_delay": 0.5
            },
            
            "performance": {
                "multithreading": True,
                "worker_threads": 4,
                "async_loading": True,
                "texture_streaming": True,
                "occlusion_culling": True,
                "frustum_culling": True,
                "memory_limit_mb": 2048
            }
        }
    
    def get(self, path: str, default: Any = None) -> Any:
        """
        Get a setting value by dot-separated path.
        
        Args:
            path: Dot-separated path (e.g., 'graphics.shadows_enabled')
            default: Default value if path not found
            
        Returns:
            Setting value or default
            
        Example:
            resolution = settings.get('window.width')
            bloom = settings.get('graphics.bloom', False)
        """
        keys = path.split('.')
        value = self.settings
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, path: str, value: Any, save: bool = False):
        """
        Set a setting value by dot-separated path.
        
        Args:
            path: Dot-separated path (e.g., 'graphics.bloom')
            value: New value
            save: Whether to immediately save to disk
            
        Example:
            settings.set('graphics.bloom', True)
            settings.set('audio.master_volume', 0.5, save=True)
        """
        keys = path.split('.')
        target = self.settings
        
        # Navigate to the parent
        for key in keys[:-1]:
            if key not in target:
                target[key] = {}
            target = target[key]
        
        # Set the value
        old_value = target.get(keys[-1])
        target[keys[-1]] = value
        
        # Trigger callbacks if value changed
        if old_value != value:
            self._trigger_callbacks(path, value, old_value)
        
        # Save if requested
        if save:
            self.save()
    
    def get_category(self, category: str) -> Dict[str, Any]:
        """
        Get all settings in a category.
        
        Args:
            category: Category name (e.g., 'graphics', 'audio')
            
        Returns:
            Dictionary of settings in that category
        """
        return self.settings.get(category, {})
    
    def set_category(self, category: str, values: Dict[str, Any], save: bool = False):
        """
        Set multiple settings in a category at once.
        
        Args:
            category: Category name
            values: Dictionary of setting values
            save: Whether to immediately save
            
        Example:
            settings.set_category('audio', {
                'master_volume': 0.7,
                'music_volume': 0.5
            })
        """
        if category not in self.settings:
            self.settings[category] = {}
        
        for key, value in values.items():
            self.set(f"{category}.{key}", value, save=False)
        
        if save:
            self.save()
    
    def save(self):
        """Save current settings to user settings file."""
        try:
            self._save_json(self.user_file, self.settings)
            print(f"[OK] Settings saved to {self.user_file}")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to save settings: {e}")
            return False
    
    def reset_to_defaults(self, category: Optional[str] = None):
        """
        Reset settings to defaults.
        
        Args:
            category: Optional category to reset (None = reset all)
            
        Example:
            settings.reset_to_defaults()  # Reset all
            settings.reset_to_defaults('graphics')  # Reset only graphics
        """
        if category:
            if category in self.defaults:
                self.settings[category] = copy.deepcopy(self.defaults[category])
                print(f"[OK] Reset '{category}' settings to defaults")
        else:
            self.settings = copy.deepcopy(self.defaults)
            print("[OK] Reset all settings to defaults")
        
        self.save()
    
    def register_callback(self, path: str, callback: callable):
        """
        Register a callback for when a setting changes.
        
        Args:
            path: Setting path to watch
            callback: Function(new_value, old_value) to call
            
        Example:
            def on_bloom_change(new_val, old_val):
                print(f"Bloom changed: {old_val} -> {new_val}")
            
            settings.register_callback('graphics.bloom', on_bloom_change)
        """
        if path not in self._callbacks:
            self._callbacks[path] = []
        self._callbacks[path].append(callback)
    
    def _trigger_callbacks(self, path: str, new_value: Any, old_value: Any):
        """Trigger callbacks for a setting change."""
        if path in self._callbacks:
            for callback in self._callbacks[path]:
                try:
                    callback(new_value, old_value)
                except Exception as e:
                    print(f"[ERROR] Callback error for '{path}': {e}")
    
    def _merge_settings(self, base: dict, override: dict):
        """Recursively merge override settings into base."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._merge_settings(base[key], value)
            else:
                base[key] = value
    
    def _load_json(self, filepath: Path) -> dict:
        """Load JSON from file."""
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _save_json(self, filepath: Path, data: dict):
        """Save JSON to file."""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    
    def print_all(self):
        """Print all current settings (for debugging)."""
        print("\n" + "="*60)
        print("ENGINE SETTINGS")
        print("="*60)
        self._print_dict(self.settings)
        print("="*60 + "\n")
    
    def _print_dict(self, d: dict, indent: int = 0):
        """Recursively print dictionary."""
        for key, value in d.items():
            if isinstance(value, dict):
                print("  " * indent + f"{key}:")
                self._print_dict(value, indent + 1)
            else:
                print("  " * indent + f"{key}: {value}")
    
    # Convenience properties for common categories
    @property
    def engine(self) -> dict:
        """Get engine settings."""
        return self.get_category('engine')
    
    @property
    def window(self) -> dict:
        """Get window settings."""
        return self.get_category('window')
    
    @property
    def graphics(self) -> dict:
        """Get graphics settings."""
        return self.get_category('graphics')
    
    @property
    def audio(self) -> dict:
        """Get audio settings."""
        return self.get_category('audio')
    
    @property
    def input(self) -> dict:
        """Get input settings."""
        return self.get_category('input')
    
    @property
    def ui(self) -> dict:
        """Get UI settings."""
        return self.get_category('ui')
    
    @property
    def performance(self) -> dict:
        """Get performance settings."""
        return self.get_category('performance')

