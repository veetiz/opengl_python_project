"""
Game Engine
A modular OpenGL game engine with comprehensive features.
Organized by functional categories.
"""

# Core
from .core import Application, Window, Input, Keyboard, Mouse

# Rendering
from .rendering import OpenGLRenderer, ShadowMap

# Graphics
from .graphics import (
    Material, Texture, Mesh, Vertex, Model, ModelLoader,
    Light, DirectionalLight, PointLight, SpotLight
)

# Audio
from .audio import (
    AudioManager, AudioClip, AudioSource, AudioListener,
    Audio2D, Audio3D
)

# UI
from .ui import (
    TextRenderer, Text2D, Text3DRenderer, Text3D,
    Font, Glyph, FontLoader,
    UIElement, Anchor, UIManager, UIButton, UILabel,
    UISlider, UICheckbox, UIDropdown, UIPanel
)

# Scene
from .scene import (
    Scene, SplashScene, Entity, GameObject, Transform,
    GameScript, Camera
)

# Systems
from .systems import (
    SettingsManager, SettingsPresets,
    ThreadingManager, TaskPriority,
    AssetLoader, AssetCache
)

# Effects
from .effects import (
    Particle, ParticleEmitter, ParticleRenderer,
    ParticleSystem, ParticlePresets
)

__all__ = [
    # Core
    'Application',
    'Window',
    'Input',
    'Keyboard',
    'Mouse',
    
    # Rendering
    'OpenGLRenderer',
    'ShadowMap',
    
    # Graphics
    'Material',
    'Texture',
    'Mesh',
    'Vertex',
    'Model',
    'ModelLoader',
    'Light',
    'DirectionalLight',
    'PointLight',
    'SpotLight',
    
    # Audio
    'AudioManager',
    'AudioClip',
    'AudioSource',
    'AudioListener',
    'Audio2D',
    'Audio3D',
    
    # UI
    'TextRenderer',
    'Text2D',
    'Text3DRenderer',
    'Text3D',
    'Font',
    'Glyph',
    'FontLoader',
    'UIElement',
    'Anchor',
    'UIManager',
    'UIButton',
    'UILabel',
    'UISlider',
    'UICheckbox',
    'UIDropdown',
    'UIPanel',
    
    # Scene
    'Scene',
    'SplashScene',
    'Entity',
    'GameObject',
    'Transform',
    'GameScript',
    'Camera',
    
    # Systems
    'SettingsManager',
    'SettingsPresets',
    'ThreadingManager',
    'TaskPriority',
    'AssetLoader',
    'AssetCache',
    
    # Effects
    'Particle',
    'ParticleEmitter',
    'ParticleRenderer',
    'ParticleSystem',
    'ParticlePresets',
]

__version__ = '2.0.0'
