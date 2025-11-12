# Engine Settings System

## Overview

A generic, flexible settings system for managing engine configuration including graphics, audio, window, input, UI, and performance settings.

## Features

✅ **JSON-based** - Human-readable config files
✅ **Hierarchical** - Organized by category
✅ **Type-safe** - Dot-notation access
✅ **Persistent** - Auto-save user preferences
✅ **Callbacks** - React to setting changes
✅ **Presets** - Quality presets (low/medium/high/ultra)
✅ **Defaults** - Always has fallback values
✅ **Generic** - Works with any engine/game

---

## Quick Start

### Basic Usage

```python
from src import SettingsManager

# Create settings manager
settings = SettingsManager(app_name="my_game")

# Get settings
width = settings.get('window.width')
bloom = settings.get('graphics.bloom')

# Set settings
settings.set('audio.master_volume', 0.7)
settings.set('graphics.shadows_enabled', False, save=True)

# Get entire category
graphics = settings.graphics  # Returns dict
audio = settings.audio
```

### Using Presets

```python
from src import SettingsManager, SettingsPresets

settings = SettingsManager()

# Apply quality preset
SettingsPresets.apply_graphics_preset(settings, "low")      # Low quality
SettingsPresets.apply_graphics_preset(settings, "high")     # High quality
SettingsPresets.apply_graphics_preset(settings, "ultra")    # Ultra quality
```

---

## Integration with Engine

### 1. Application Initialization

```python
# src/app.py

from .settings_manager import SettingsManager

class Application:
    def __init__(self, ...):
        # Initialize settings first
        self.settings = SettingsManager(app_name="my_game")
        
        # Use settings for window creation
        width = self.settings.get('window.width')
        height = self.settings.get('window.height')
        fullscreen = self.settings.get('window.fullscreen')
        
        self.window = Window(width, height, fullscreen)
```

### 2. Renderer Integration

```python
# src/renderer.py

class OpenGLRenderer:
    def __init__(self, settings: SettingsManager):
        self.settings = settings
        
        # Apply graphics settings
        self._apply_graphics_settings()
    
    def _apply_graphics_settings(self):
        # VSync
        if self.settings.get('window.vsync'):
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)
        
        # MSAA
        samples = self.settings.get('graphics.msaa_samples')
        if samples > 0:
            glEnable(GL_MULTISAMPLE)
        
        # Shadows
        if self.settings.get('graphics.shadows_enabled'):
            shadow_res = self.settings.get('graphics.shadow_map_size')
            self.setup_shadows(shadow_res)
        
        # Bloom
        if self.settings.get('graphics.bloom'):
            intensity = self.settings.get('graphics.bloom_intensity')
            self.enable_bloom(intensity)
```

### 3. Audio Manager Integration

```python
# src/audio_manager.py

class AudioManager:
    def __init__(self, settings: SettingsManager):
        self.settings = settings
        
        # Apply audio settings
        self.set_master_volume(settings.get('audio.master_volume'))
        self.set_music_volume(settings.get('audio.music_volume'))
        self.set_effects_volume(settings.get('audio.effects_volume'))
        
        # Enable/disable features
        if settings.get('audio.spatial_audio'):
            self.enable_spatial_audio()
```

### 4. Using Callbacks for Live Updates

```python
# Register callback for when bloom changes
def on_bloom_change(new_value, old_value):
    if new_value:
        renderer.enable_bloom()
    else:
        renderer.disable_bloom()

settings.register_callback('graphics.bloom', on_bloom_change)

# Now when user changes setting, renderer updates automatically
settings.set('graphics.bloom', False)  # Triggers callback
```

---

## Settings Categories

### Engine
```python
engine.version          # Engine version
engine.debug_mode       # Debug mode flag
engine.log_level        # Logging level
```

### Window
```python
window.width            # Window width
window.height           # Window height
window.fullscreen       # Fullscreen mode
window.vsync            # VSync enabled
window.resizable        # Resizable window
```

### Graphics
```python
graphics.target_fps             # Target FPS
graphics.msaa_samples           # MSAA samples (0,2,4,8,16)
graphics.anisotropic_filtering  # Anisotropic filtering
graphics.shadows_enabled        # Enable shadows
graphics.shadow_map_size        # Shadow resolution
graphics.bloom                  # Bloom effect
graphics.bloom_intensity        # Bloom strength
graphics.gamma                  # Gamma correction
graphics.render_distance        # Max render distance
```

### Audio
```python
audio.master_volume     # Master volume (0.0-1.0)
audio.music_volume      # Music volume
audio.effects_volume    # SFX volume
audio.muted             # Mute all audio
audio.spatial_audio     # 3D spatial audio
audio.reverb            # Reverb effects
```

### Input
```python
input.mouse_sensitivity  # Mouse sensitivity
input.mouse_invert_y    # Invert Y axis
input.gamepad_enabled   # Enable gamepad
input.gamepad_deadzone  # Analog stick deadzone
```

### UI
```python
ui.scale                # UI scale factor
ui.font_size            # Font size
ui.show_fps             # Show FPS counter
ui.show_debug_info      # Show debug overlay
```

### Performance
```python
performance.multithreading   # Enable multithreading
performance.worker_threads   # Number of threads
performance.async_loading    # Async asset loading
performance.memory_limit_mb  # Memory limit
```

---

## API Reference

### SettingsManager

#### Methods

```python
get(path: str, default: Any = None) -> Any
```
Get a setting value by dot-separated path.

```python
set(path: str, value: Any, save: bool = False)
```
Set a setting value.

```python
get_category(category: str) -> Dict
```
Get all settings in a category.

```python
set_category(category: str, values: Dict, save: bool = False)
```
Set multiple settings in a category.

```python
save()
```
Save settings to disk.

```python
reset_to_defaults(category: Optional[str] = None)
```
Reset to default settings.

```python
register_callback(path: str, callback: callable)
```
Register callback for setting changes.

#### Properties

```python
settings.engine      # Engine settings dict
settings.window      # Window settings dict
settings.graphics    # Graphics settings dict
settings.audio       # Audio settings dict
settings.input       # Input settings dict
settings.ui          # UI settings dict
settings.performance # Performance settings dict
```

---

## File Structure

```
config/
├── default_settings.json     # Default engine settings
└── my_game_settings.json     # User overrides (auto-created)
```

**Note:** Add `config/*_settings.json` to `.gitignore` (keep defaults, ignore user files)

---

## Examples

### Example 1: Settings Menu

```python
def create_settings_menu(settings: SettingsManager):
    # Graphics menu
    def on_quality_change(quality: str):
        SettingsPresets.apply_graphics_preset(settings, quality)
    
    def on_shadow_toggle(enabled: bool):
        settings.set('graphics.shadows_enabled', enabled, save=True)
    
    def on_bloom_toggle(enabled: bool):
        settings.set('graphics.bloom', enabled, save=True)
    
    # Audio menu
    def on_volume_change(volume: float):
        settings.set('audio.master_volume', volume, save=True)
```

### Example 2: Auto-apply on Launch

```python
class Application:
    def init(self):
        # Load settings
        self.settings = SettingsManager()
        
        # Apply all settings to engine
        self._apply_all_settings()
    
    def _apply_all_settings(self):
        self.renderer.apply_settings(self.settings)
        self.audio.apply_settings(self.settings)
        self.input.apply_settings(self.settings)
```

### Example 3: Performance Presets

```python
# Detect system and apply appropriate preset
def auto_configure():
    settings = SettingsManager()
    
    # Detect GPU/CPU
    if is_low_end_system():
        SettingsPresets.apply_graphics_preset(settings, "low")
    elif is_mid_range_system():
        SettingsPresets.apply_graphics_preset(settings, "medium")
    else:
        SettingsPresets.apply_graphics_preset(settings, "high")
```

---

## Best Practices

1. **Load settings early** - Before creating window/renderer
2. **Use callbacks** - For live setting updates
3. **Save on close** - Call `settings.save()` on app exit
4. **Provide presets** - Let users quickly choose quality levels
5. **Validate input** - Check ranges before setting values
6. **Use categories** - Organize settings logically
7. **Document settings** - Add comments to defaults

---

## Adding Custom Settings

### For Game-Specific Settings

```python
# Extend the defaults in your game
settings = SettingsManager(app_name="my_game")

# Add custom game settings
settings.set_category('gameplay', {
    'difficulty': 'normal',
    'auto_save': True,
    'save_slot': 1
})

# Save new structure
settings.save()
```

### For New Engine Features

Edit `settings_manager.py` → `_get_default_settings()`:

```python
def _get_default_settings(self):
    return {
        # ... existing categories ...
        
        "new_feature": {
            "enabled": True,
            "quality": "high",
            "custom_param": 42
        }
    }
```

---

## Troubleshooting

**Q: Settings not persisting?**
A: Call `settings.save()` or use `save=True` parameter in `set()`

**Q: Settings not loading?**
A: Check that `config/` directory exists and files are valid JSON

**Q: Want to force reset?**
A: Delete user settings file or call `reset_to_defaults()`

**Q: Callbacks not firing?**
A: Make sure you register callbacks BEFORE changing settings

---

## Summary

The settings system provides:
- ✅ Complete engine configuration
- ✅ User preference persistence
- ✅ Quality presets
- ✅ Live updates via callbacks
- ✅ Easy integration
- ✅ Generic and extensible

Perfect for any game or engine built on this framework!

