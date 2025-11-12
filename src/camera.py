"""
Camera Module
Provides a 3D camera with view and projection matrices.
"""

import numpy as np
from typing import Tuple
from .entity import Entity


class Camera(Entity):
    """3D Camera with view and projection transformations."""
    
    def __init__(
        self,
        name: str = "Camera",
        position: Tuple[float, float, float] = (0.0, 0.0, 3.0),
        target: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        up: Tuple[float, float, float] = (0.0, 1.0, 0.0),
        fov: float = 45.0,
        aspect_ratio: float = 800.0 / 600.0,
        near: float = 0.1,
        far: float = 100.0
    ):
        """
        Initialize the camera.
        
        Args:
            name: Camera name for identification
            position: Camera position (x, y, z)
            target: Point the camera is looking at
            up: Up vector
            fov: Field of view in degrees
            aspect_ratio: Aspect ratio (width/height)
            near: Near clipping plane
            far: Far clipping plane
        """
        # Initialize base Entity
        super().__init__(name)
        
        self.position = np.array(position, dtype=np.float32)
        self.target = np.array(target, dtype=np.float32)
        self.up = np.array(up, dtype=np.float32)
        
        # Projection parameters
        self.fov = fov
        self.aspect_ratio = aspect_ratio
        self.near = near
        self.far = far
        
        # Camera vectors
        self.front = np.array([0.0, 0.0, -1.0], dtype=np.float32)
        self.right = np.array([1.0, 0.0, 0.0], dtype=np.float32)
        self.world_up = np.array(up, dtype=np.float32)
        
        # Euler angles
        self.yaw = -90.0  # Looking towards -Z
        self.pitch = 0.0
        
        self._update_camera_vectors()
    
    def get_view_matrix(self) -> np.ndarray:
        """
        Get the view matrix (lookAt matrix).
        
        Returns:
            4x4 view matrix
        """
        return self._look_at(self.position, self.position + self.front, self.up)
    
    def get_projection_matrix(self) -> np.ndarray:
        """
        Get the projection matrix (perspective).
        
        Returns:
            4x4 projection matrix
        """
        return self._perspective(self.fov, self.aspect_ratio, self.near, self.far)
    
    @property
    def forward(self) -> np.ndarray:
        """Get forward vector (alias for front)."""
        return self.front
    
    def move_forward(self, amount: float):
        """Move camera forward by amount."""
        self.position += self.front * amount
    
    def move_backward(self, amount: float):
        """Move camera backward by amount."""
        self.position -= self.front * amount
    
    def move_left(self, amount: float):
        """Move camera left by amount."""
        self.position -= self.right * amount
    
    def move_right(self, amount: float):
        """Move camera right by amount."""
        self.position += self.right * amount
    
    def move_up(self, amount: float):
        """Move camera up by amount."""
        self.position += self.up * amount
    
    def move_down(self, amount: float):
        """Move camera down by amount."""
        self.position -= self.up * amount
    
    def rotate(self, yaw_delta: float, pitch_delta: float, constrain_pitch: bool = True):
        """
        Rotate camera by the given amounts.
        
        Args:
            yaw_delta: Change in yaw (degrees)
            pitch_delta: Change in pitch (degrees)
            constrain_pitch: Limit pitch to avoid gimbal lock
        """
        self.yaw += yaw_delta
        self.pitch += pitch_delta
        
        # Constrain pitch to avoid flipping
        if constrain_pitch:
            if self.pitch > 89.0:
                self.pitch = 89.0
            if self.pitch < -89.0:
                self.pitch = -89.0
        
        self._update_camera_vectors()
    
    def zoom(self, amount: float):
        """
        Zoom camera (adjust FOV).
        
        Args:
            amount: Amount to zoom (negative = zoom in, positive = zoom out)
        """
        self.fov -= amount
        if self.fov < 1.0:
            self.fov = 1.0
        if self.fov > 120.0:
            self.fov = 120.0
    
    def set_aspect_ratio(self, width: float, height: float):
        """Update camera aspect ratio."""
        if height > 0:
            self.aspect_ratio = width / height
    
    def _update_camera_vectors(self):
        """Update camera direction vectors from Euler angles."""
        # Calculate new front vector
        front = np.array([
            np.cos(np.radians(self.yaw)) * np.cos(np.radians(self.pitch)),
            np.sin(np.radians(self.pitch)),
            np.sin(np.radians(self.yaw)) * np.cos(np.radians(self.pitch))
        ], dtype=np.float32)
        self.front = front / np.linalg.norm(front)
        
        # Recalculate right and up vectors
        self.right = np.cross(self.front, self.world_up)
        self.right = self.right / np.linalg.norm(self.right)
        
        self.up = np.cross(self.right, self.front)
        self.up = self.up / np.linalg.norm(self.up)
    
    @staticmethod
    def _look_at(eye: np.ndarray, center: np.ndarray, up: np.ndarray) -> np.ndarray:
        """
        Create a lookAt view matrix.
        
        Args:
            eye: Camera position
            center: Target position
            up: Up vector
            
        Returns:
            4x4 view matrix
        """
        f = center - eye
        f = f / np.linalg.norm(f)
        
        s = np.cross(f, up)
        s = s / np.linalg.norm(s)
        
        u = np.cross(s, f)
        
        result = np.identity(4, dtype=np.float32)
        result[0, 0] = s[0]
        result[1, 0] = s[1]
        result[2, 0] = s[2]
        result[0, 1] = u[0]
        result[1, 1] = u[1]
        result[2, 1] = u[2]
        result[0, 2] = -f[0]
        result[1, 2] = -f[1]
        result[2, 2] = -f[2]
        result[3, 0] = -np.dot(s, eye)
        result[3, 1] = -np.dot(u, eye)
        result[3, 2] = np.dot(f, eye)
        
        return result
    
    @staticmethod
    def _perspective(fov: float, aspect: float, near: float, far: float) -> np.ndarray:
        """
        Create a perspective projection matrix.
        
        Args:
            fov: Field of view in degrees
            aspect: Aspect ratio
            near: Near clipping plane
            far: Far clipping plane
            
        Returns:
            4x4 projection matrix
        """
        f = 1.0 / np.tan(np.radians(fov) / 2.0)
        
        result = np.zeros((4, 4), dtype=np.float32)
        result[0, 0] = f / aspect
        result[1, 1] = f
        result[2, 2] = (far + near) / (near - far)
        result[2, 3] = -1.0
        result[3, 2] = (2.0 * far * near) / (near - far)
        
        return result

