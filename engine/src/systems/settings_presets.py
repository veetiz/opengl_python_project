"""
Settings Presets Module
Provides quality presets and utility functions for settings.
"""

from typing import Dict, Any


class SettingsPresets:
    """Predefined quality presets for graphics settings."""
    
    # Graphics quality presets
    GRAPHICS_PRESETS = {
        "low": {
            "msaa_samples": 0,
            "anisotropic_filtering": 1,
            "texture_quality": 0.5,
            "shadows_enabled": True,
            "shadow_map_size": 512,
            "shadow_cascades": 1,
            "shadow_distance": 50.0,
            "bloom": False,
            "bloom_intensity": 0.0,
            "render_distance": 500.0,
            "lod_bias": 2.0,
            "culling_enabled": False
        },
        
        "medium": {
            "msaa_samples": 2,
            "anisotropic_filtering": 4,
            "texture_quality": 0.75,
            "shadows_enabled": True,
            "shadow_map_size": 1024,
            "shadow_cascades": 2,
            "shadow_distance": 75.0,
            "bloom": True,
            "bloom_intensity": 0.2,
            "render_distance": 750.0,
            "lod_bias": 1.5,
            "culling_enabled": False
        },
        
        "high": {
            "msaa_samples": 4,
            "anisotropic_filtering": 8,
            "texture_quality": 1.0,
            "shadows_enabled": True,
            "shadow_map_size": 2048,
            "shadow_cascades": 3,
            "shadow_distance": 100.0,
            "bloom": True,
            "bloom_intensity": 0.3,
            "render_distance": 1000.0,
            "lod_bias": 1.0,
            "culling_enabled": False
        },
        
        "ultra": {
            "msaa_samples": 8,
            "anisotropic_filtering": 16,
            "texture_quality": 2.0,
            "shadows_enabled": True,
            "shadow_map_size": 4096,
            "shadow_cascades": 4,
            "shadow_distance": 150.0,
            "bloom": True,
            "bloom_intensity": 0.4,
            "render_distance": 1500.0,
            "lod_bias": 0.5,
            "culling_enabled": False  # Disabled - model has incorrect winding order
        },
        
        "custom": {}  # User-defined preset
    }
    
    @staticmethod
    def apply_graphics_preset(settings_manager, preset_name: str):
        """
        Apply a graphics quality preset.
        
        Args:
            settings_manager: SettingsManager instance
            preset_name: Preset name ('low', 'medium', 'high', 'ultra')
        """
        if preset_name not in SettingsPresets.GRAPHICS_PRESETS:
            print(f"[WARNING] Unknown preset: {preset_name}")
            return False
        
        preset = SettingsPresets.GRAPHICS_PRESETS[preset_name]
        settings_manager.set_category('graphics', preset, save=True)
        print(f"[OK] Applied '{preset_name}' graphics preset")
        return True
    
    @staticmethod
    def detect_recommended_preset() -> str:
        """
        Auto-detect recommended graphics preset based on system.
        Returns preset name suggestion.
        """
        # TODO: Implement system detection
        # For now, return 'high' as default
        return "high"
    
    @staticmethod
    def get_resolution_presets() -> Dict[str, tuple]:
        """Get common resolution presets."""
        return {
            "720p": (1280, 720),
            "900p": (1600, 900),
            "1080p": (1920, 1080),
            "1440p": (2560, 1440),
            "4K": (3840, 2160)
        }
    
    @staticmethod
    def validate_settings(settings: dict) -> bool:
        """
        Validate settings values are within acceptable ranges.
        
        Args:
            settings: Settings dictionary to validate
            
        Returns:
            True if valid, False otherwise
        """
        # Validate ranges
        validations = [
            # Audio volumes should be 0.0 - 1.0
            ('audio.master_volume', 0.0, 1.0),
            ('audio.effects_volume', 0.0, 1.0),
            ('audio.music_volume', 0.0, 1.0),
            ('audio.ambient_volume', 0.0, 1.0),
            
            # Graphics values
            ('graphics.bloom_intensity', 0.0, 1.0),
            ('graphics.gamma', 1.0, 3.0),
            ('graphics.exposure', 0.1, 5.0),
            
            # Input
            ('input.mouse_sensitivity', 0.1, 5.0),
            ('input.gamepad_deadzone', 0.0, 0.5),
            
            # UI
            ('ui.scale', 0.5, 2.0),
        ]
        
        # TODO: Implement actual validation
        return True

