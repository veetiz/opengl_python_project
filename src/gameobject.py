"""
GameObject Module
Represents a game object with transform and model.
"""

import numpy as np
from typing import Optional, Tuple
from .entity import Entity
from .model import Model


class Transform:
    """Represents position, rotation, and scale of an object."""
    
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ):
        """
        Initialize transform.
        
        Args:
            position: Position (x, y, z)
            rotation: Rotation in degrees (pitch, yaw, roll)
            scale: Scale (x, y, z)
        """
        self.position = np.array(position, dtype=np.float32)
        self.rotation = np.array(rotation, dtype=np.float32)
        self.scale = np.array(scale, dtype=np.float32)
    
    def get_model_matrix(self) -> np.ndarray:
        """
        Calculate the model matrix from transform components.
        
        Returns:
            4x4 model matrix
        """
        # Translation matrix
        translation = np.identity(4, dtype=np.float32)
        translation[3, 0:3] = self.position
        
        # Rotation matrices (in radians)
        pitch = np.radians(self.rotation[0])
        yaw = np.radians(self.rotation[1])
        roll = np.radians(self.rotation[2])
        
        # Rotation around X axis (pitch)
        rotation_x = np.identity(4, dtype=np.float32)
        rotation_x[1, 1] = np.cos(pitch)
        rotation_x[1, 2] = -np.sin(pitch)
        rotation_x[2, 1] = np.sin(pitch)
        rotation_x[2, 2] = np.cos(pitch)
        
        # Rotation around Y axis (yaw)
        rotation_y = np.identity(4, dtype=np.float32)
        rotation_y[0, 0] = np.cos(yaw)
        rotation_y[0, 2] = np.sin(yaw)
        rotation_y[2, 0] = -np.sin(yaw)
        rotation_y[2, 2] = np.cos(yaw)
        
        # Rotation around Z axis (roll)
        rotation_z = np.identity(4, dtype=np.float32)
        rotation_z[0, 0] = np.cos(roll)
        rotation_z[0, 1] = -np.sin(roll)
        rotation_z[1, 0] = np.sin(roll)
        rotation_z[1, 1] = np.cos(roll)
        
        # Scale matrix
        scale_matrix = np.identity(4, dtype=np.float32)
        scale_matrix[0, 0] = self.scale[0]
        scale_matrix[1, 1] = self.scale[1]
        scale_matrix[2, 2] = self.scale[2]
        
        # Combine transformations: Translation * Rotation * Scale
        rotation = rotation_z @ rotation_y @ rotation_x
        model = translation @ rotation @ scale_matrix
        
        return model


class GameObject(Entity):
    """Represents a game object in the scene."""
    
    def __init__(
        self,
        name: str = "GameObject",
        model: Optional[Model] = None,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ):
        """
        Initialize a game object.
        
        Args:
            name: Object name for identification
            model: 3D model to render
            position: Initial position (x, y, z)
            rotation: Initial rotation in degrees (pitch, yaw, roll)
            scale: Initial scale (x, y, z)
        """
        # Initialize base Entity
        super().__init__(name)
        
        self.model = model
        self.transform = Transform(position, rotation, scale)
    
    def set_position(self, x: float, y: float, z: float):
        """Set the object's position."""
        self.transform.position = np.array([x, y, z], dtype=np.float32)
    
    def set_rotation(self, pitch: float, yaw: float, roll: float):
        """Set the object's rotation (in degrees)."""
        self.transform.rotation = np.array([pitch, yaw, roll], dtype=np.float32)
    
    def set_scale(self, x: float, y: float, z: float):
        """Set the object's scale."""
        self.transform.scale = np.array([x, y, z], dtype=np.float32)
    
    def rotate(self, pitch: float = 0.0, yaw: float = 0.0, roll: float = 0.0):
        """Rotate the object by the given amounts (in degrees)."""
        self.transform.rotation += np.array([pitch, yaw, roll], dtype=np.float32)
    
    def translate(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        """Move the object by the given amounts."""
        self.transform.position += np.array([x, y, z], dtype=np.float32)
    
    def get_model_matrix(self) -> np.ndarray:
        """Get the model matrix for this game object."""
        return self.transform.get_model_matrix()

