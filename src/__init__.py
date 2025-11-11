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
from .camera import Camera
from .input import Input, Keyboard, Mouse
from .gamescript import GameScript
from .texture import Texture
from .model_loader import ModelLoader

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
    'Camera',
    'Input',
    'Keyboard',
    'Mouse',
    'GameScript',
    'Texture',
    'ModelLoader'
]
__version__ = '2.0.0'
