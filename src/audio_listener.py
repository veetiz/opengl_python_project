"""
AudioListener Module
Represents the position of the audio listener (usually attached to camera).
"""

import numpy as np
from typing import Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .camera import Camera


class AudioListener:
    """
    Audio listener - represents the ears of the player.
    Usually attached to the active camera.
    """
    
    def __init__(self, camera: 'Camera' = None):
        """
        Initialize audio listener.
        
        Args:
            camera: Camera to attach to (if None, uses position (0,0,0))
        """
        self.camera = camera
        self._position = np.array([0.0, 0.0, 0.0], dtype=np.float32)
        self._forward = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self._up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
        self._right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    
    def attach_to_camera(self, camera: 'Camera'):
        """
        Attach listener to a camera.
        
        Args:
            camera: Camera to attach to
        """
        self.camera = camera
    
    def detach(self):
        """Detach from camera."""
        self.camera = None
    
    def update(self):
        """Update listener position and orientation from attached camera."""
        if self.camera:
            self._position = self.camera.position.copy()
            self._forward = self.camera.forward.copy()
            self._up = self.camera.up.copy()
            self._right = self.camera.right.copy()
    
    @property
    def position(self) -> np.ndarray:
        """Get listener position."""
        if self.camera:
            return self.camera.position
        return self._position
    
    @property
    def forward(self) -> np.ndarray:
        """Get listener forward vector."""
        if self.camera:
            return self.camera.forward
        return self._forward
    
    @property
    def up(self) -> np.ndarray:
        """Get listener up vector."""
        if self.camera:
            return self.camera.up
        return self._up
    
    @property
    def right(self) -> np.ndarray:
        """Get listener right vector (for stereo panning)."""
        if self.camera:
            return self.camera.right
        return self._right
    
    def __repr__(self) -> str:
        cam_name = self.camera.name if self.camera else "None"
        return f"AudioListener(camera='{cam_name}', pos={tuple(self.position)})"

