"""
OpenGL Window Project
A modular OpenGL application with proper game engine architecture.
"""

from .window import Window
from .renderer import OpenGLRenderer
from .app import Application
from .vertex import Vertex
from .mesh import Mesh
from .model import Model
from .entity import Entity
from .gameobject import GameObject, Transform
from .scene import Scene
from .splash_scene import SplashScene
from .camera import Camera
from .input import Input, Keyboard, Mouse
from .gamescript import GameScript
from .texture import Texture
from .model_loader import ModelLoader
from .font import Font, Glyph
from .font_loader import FontLoader
from .text_renderer import TextRenderer
from .text2d import Text2D
from .text3d import Text3D
from .text3d_renderer import Text3DRenderer
from .light import Light, DirectionalLight, PointLight, SpotLight
from .material import Material
from .shadow_map import ShadowMap

__all__ = [
    'Window',
    'OpenGLRenderer',
    'Application',
    'Vertex',
    'Mesh',
    'Model',
    'Entity',
    'GameObject',
    'Transform',
    'Scene',
    'SplashScene',
    'Camera',
    'Input',
    'Keyboard',
    'Mouse',
    'GameScript',
    'Texture',
    'ModelLoader',
    'Font',
    'Glyph',
    'FontLoader',
    'TextRenderer',
    'Text2D',
    'Text3D',
    'Text3DRenderer',
    'Light',
    'DirectionalLight',
    'PointLight',
    'SpotLight',
    'Material',
    'ShadowMap',
]
__version__ = '2.0.0'
