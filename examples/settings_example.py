"""
Example usage of the Settings Manager
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from engine.src.systems.settings_manager import SettingsManager
from engine.src.systems.settings_presets import SettingsPresets


def example_basic_usage():
    """Basic settings usage."""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Usage")
    print("="*60)
    
    # Create settings manager
    settings = SettingsManager(app_name="my_game")
    
    # Get settings
    width = settings.get('window.width')
    height = settings.get('window.height')
    print(f"Window size: {width}x{height}")
    
    # Get with default
    fov = settings.get('graphics.fov', 75)
    print(f"FOV: {fov}")
    
    # Set settings
    settings.set('graphics.bloom', False)
    settings.set('audio.master_volume', 0.5)
    
    # Save changes
    settings.save()
    
    print("\n[OK] Basic usage complete")


def example_categories():
    """Working with setting categories."""
    print("\n" + "="*60)
    print("EXAMPLE 2: Categories")
    print("="*60)
    
    settings = SettingsManager(app_name="test_app")
    
    # Get entire category
    graphics = settings.graphics
    print(f"Bloom enabled: {graphics['bloom']}")
    print(f"Shadow resolution: {graphics['shadow_map_size']}")
    
    # Set multiple settings at once
    settings.set_category('audio', {
        'master_volume': 0.8,
        'music_volume': 0.6,
        'effects_volume': 0.9
    }, save=True)
    
    print("\n[OK] Category operations complete")


def example_presets():
    """Using quality presets."""
    print("\n" + "="*60)
    print("EXAMPLE 3: Quality Presets")
    print("="*60)
    
    settings = SettingsManager(app_name="preset_test")
    
    # Apply low quality preset
    print("\nApplying LOW quality preset...")
    SettingsPresets.apply_graphics_preset(settings, "low")
    print(f"  Shadow resolution: {settings.get('graphics.shadow_map_size')}")
    print(f"  MSAA: {settings.get('graphics.msaa_samples')}")
    
    # Apply ultra quality preset
    print("\nApplying ULTRA quality preset...")
    SettingsPresets.apply_graphics_preset(settings, "ultra")
    print(f"  Shadow resolution: {settings.get('graphics.shadow_map_size')}")
    print(f"  MSAA: {settings.get('graphics.msaa_samples')}")
    
    print("\n[OK] Preset operations complete")


def example_callbacks():
    """Using callbacks for setting changes."""
    print("\n" + "="*60)
    print("EXAMPLE 4: Callbacks")
    print("="*60)
    
    settings = SettingsManager(app_name="callback_test")
    
    # Register callback
    def on_vsync_change(new_value, old_value):
        print(f"  VSync changed: {old_value} -> {new_value}")
        if new_value:
            print("  -> Enabling VSync in renderer...")
        else:
            print("  -> Disabling VSync in renderer...")
    
    settings.register_callback('window.vsync', on_vsync_change)
    
    # Change setting (triggers callback)
    print("\nChanging VSync setting:")
    settings.set('window.vsync', False)
    
    print("\nChanging again:")
    settings.set('window.vsync', True)
    
    print("\n[OK] Callback example complete")


def example_engine_integration():
    """Example of integrating with engine systems."""
    print("\n" + "="*60)
    print("EXAMPLE 5: Engine Integration")
    print("="*60)
    
    settings = SettingsManager(app_name="engine_test")
    
    # Simulated engine initialization
    print("\nInitializing engine systems with settings:")
    
    # Window system
    print(f"\n[Window]")
    print(f"  Resolution: {settings.get('window.width')}x{settings.get('window.height')}")
    print(f"  Fullscreen: {settings.get('window.fullscreen')}")
    print(f"  VSync: {settings.get('window.vsync')}")
    
    # Graphics system
    print(f"\n[Graphics]")
    print(f"  Shadows: {settings.get('graphics.shadows_enabled')}")
    print(f"  Shadow Resolution: {settings.get('graphics.shadow_map_size')}")
    print(f"  Bloom: {settings.get('graphics.bloom')}")
    print(f"  Target FPS: {settings.get('graphics.target_fps')}")
    
    # Audio system
    print(f"\n[Audio]")
    print(f"  Master Volume: {settings.get('audio.master_volume')}")
    print(f"  Spatial Audio: {settings.get('audio.spatial_audio')}")
    print(f"  Max Sources: {settings.get('audio.max_sound_sources')}")
    
    # Performance
    print(f"\n[Performance]")
    print(f"  Multithreading: {settings.get('performance.multithreading')}")
    print(f"  Worker Threads: {settings.get('performance.worker_threads')}")
    print(f"  Async Loading: {settings.get('performance.async_loading')}")
    
    print("\n[OK] Engine systems initialized")


def example_reset():
    """Resetting settings."""
    print("\n" + "="*60)
    print("EXAMPLE 6: Reset Settings")
    print("="*60)
    
    settings = SettingsManager(app_name="reset_test")
    
    # Modify settings
    print("\nModifying settings...")
    settings.set('graphics.bloom', False)
    settings.set('audio.master_volume', 0.3)
    print(f"  Bloom: {settings.get('graphics.bloom')}")
    print(f"  Master Volume: {settings.get('audio.master_volume')}")
    
    # Reset specific category
    print("\nResetting graphics to defaults...")
    settings.reset_to_defaults('graphics')
    print(f"  Bloom: {settings.get('graphics.bloom')}")
    
    # Reset all
    print("\nResetting all settings to defaults...")
    settings.reset_to_defaults()
    print(f"  Master Volume: {settings.get('audio.master_volume')}")
    
    print("\n[OK] Reset complete")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("SETTINGS MANAGER EXAMPLES")
    print("="*60)
    
    example_basic_usage()
    example_categories()
    example_presets()
    example_callbacks()
    example_engine_integration()
    example_reset()
    
    print("\n" + "="*60)
    print("ALL EXAMPLES COMPLETE")
    print("="*60 + "\n")

