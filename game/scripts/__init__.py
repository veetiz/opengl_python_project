"""
Game Scripts
Game-specific script implementations.
"""

from .example_scripts import (
    RotateScript,
    OscillateScript,
    FPSCounterScript,
    CameraOrbitScript
)
from .camera_movement import CameraMovementScript

__all__ = [
    'RotateScript',
    'OscillateScript',
    'FPSCounterScript',
    'CameraOrbitScript',
    'CameraMovementScript'
]

