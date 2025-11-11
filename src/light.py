"""
Light Module
Base Light class and specific light types for illuminating scenes.
"""

from typing import Tuple
from .entity import Entity
import numpy as np


class Light(Entity):
    """
    Base light class that all light types inherit from.
    """
    
    def __init__(
        self,
        name: str = "Light",
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        intensity: float = 1.0,
        active: bool = True
    ):
        """
        Initialize a light.
        
        Args:
            name: Light name
            color: RGB color of the light (0.0-1.0)
            intensity: Light intensity/brightness
            active: Whether the light is active
        """
        super().__init__(name=name)
        self.color = color
        self.intensity = intensity
        self.active = active
    
    def set_color(self, color: Tuple[float, float, float]):
        """Set light color."""
        self.color = color
    
    def set_intensity(self, intensity: float):
        """Set light intensity."""
        self.intensity = intensity
    
    def get_light_data(self) -> dict:
        """
        Get light data for shader uniforms.
        Should be overridden by subclasses.
        
        Returns:
            Dictionary of light parameters
        """
        return {
            'color': self.color,
            'intensity': self.intensity,
            'active': self.active
        }


class DirectionalLight(Light):
    """
    Directional light (like the sun) - parallel rays from a direction.
    """
    
    def __init__(
        self,
        name: str = "DirectionalLight",
        direction: Tuple[float, float, float] = (0.0, -1.0, 0.0),
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        intensity: float = 1.0,
        active: bool = True
    ):
        """
        Initialize a directional light.
        
        Args:
            name: Light name
            direction: Direction vector (will be normalized)
            color: RGB color (0.0-1.0)
            intensity: Light intensity
            active: Whether light is active
        """
        super().__init__(name, color, intensity, active)
        self.direction = np.array(direction, dtype=np.float32)
        # Normalize direction
        length = np.linalg.norm(self.direction)
        if length > 0:
            self.direction = self.direction / length
    
    def set_direction(self, direction: Tuple[float, float, float]):
        """Set light direction (will be normalized)."""
        self.direction = np.array(direction, dtype=np.float32)
        length = np.linalg.norm(self.direction)
        if length > 0:
            self.direction = self.direction / length
    
    def get_light_data(self) -> dict:
        """Get directional light data for shaders."""
        data = super().get_light_data()
        data['type'] = 'directional'
        data['direction'] = self.direction.tolist()
        return data


class PointLight(Light):
    """
    Point light (like a light bulb) - radiates in all directions from a point.
    """
    
    def __init__(
        self,
        name: str = "PointLight",
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        intensity: float = 1.0,
        constant: float = 1.0,
        linear: float = 0.09,
        quadratic: float = 0.032,
        active: bool = True
    ):
        """
        Initialize a point light.
        
        Args:
            name: Light name
            position: World position of the light
            color: RGB color (0.0-1.0)
            intensity: Light intensity
            constant: Constant attenuation factor
            linear: Linear attenuation factor
            quadratic: Quadratic attenuation factor
            active: Whether light is active
        """
        super().__init__(name, color, intensity, active)
        self.position = np.array(position, dtype=np.float32)
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
    
    def set_position(self, position: Tuple[float, float, float]):
        """Set light position."""
        self.position = np.array(position, dtype=np.float32)
    
    def set_attenuation(self, constant: float, linear: float, quadratic: float):
        """Set attenuation factors for distance falloff."""
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
    
    def get_light_data(self) -> dict:
        """Get point light data for shaders."""
        data = super().get_light_data()
        data['type'] = 'point'
        data['position'] = self.position.tolist()
        data['constant'] = self.constant
        data['linear'] = self.linear
        data['quadratic'] = self.quadratic
        return data


class SpotLight(Light):
    """
    Spot light (like a flashlight) - cone of light from a position in a direction.
    """
    
    def __init__(
        self,
        name: str = "SpotLight",
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        direction: Tuple[float, float, float] = (0.0, -1.0, 0.0),
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        intensity: float = 1.0,
        inner_cutoff: float = 12.5,  # degrees
        outer_cutoff: float = 17.5,  # degrees
        constant: float = 1.0,
        linear: float = 0.09,
        quadratic: float = 0.032,
        active: bool = True
    ):
        """
        Initialize a spot light.
        
        Args:
            name: Light name
            position: World position of the light
            direction: Direction the spotlight is pointing (will be normalized)
            color: RGB color (0.0-1.0)
            intensity: Light intensity
            inner_cutoff: Inner cone angle in degrees (full brightness)
            outer_cutoff: Outer cone angle in degrees (starts fading)
            constant: Constant attenuation factor
            linear: Linear attenuation factor
            quadratic: Quadratic attenuation factor
            active: Whether light is active
        """
        super().__init__(name, color, intensity, active)
        self.position = np.array(position, dtype=np.float32)
        self.direction = np.array(direction, dtype=np.float32)
        
        # Normalize direction
        length = np.linalg.norm(self.direction)
        if length > 0:
            self.direction = self.direction / length
        
        # Convert angles to cosines for shader
        self.inner_cutoff = np.cos(np.radians(inner_cutoff))
        self.outer_cutoff = np.cos(np.radians(outer_cutoff))
        
        # Attenuation
        self.constant = constant
        self.linear = linear
        self.quadratic = quadratic
    
    def set_position(self, position: Tuple[float, float, float]):
        """Set light position."""
        self.position = np.array(position, dtype=np.float32)
    
    def set_direction(self, direction: Tuple[float, float, float]):
        """Set light direction (will be normalized)."""
        self.direction = np.array(direction, dtype=np.float32)
        length = np.linalg.norm(self.direction)
        if length > 0:
            self.direction = self.direction / length
    
    def set_cutoff(self, inner_degrees: float, outer_degrees: float):
        """Set spotlight cone angles in degrees."""
        self.inner_cutoff = np.cos(np.radians(inner_degrees))
        self.outer_cutoff = np.cos(np.radians(outer_degrees))
    
    def get_light_data(self) -> dict:
        """Get spot light data for shaders."""
        data = super().get_light_data()
        data['type'] = 'spot'
        data['position'] = self.position.tolist()
        data['direction'] = self.direction.tolist()
        data['inner_cutoff'] = float(self.inner_cutoff)
        data['outer_cutoff'] = float(self.outer_cutoff)
        data['constant'] = self.constant
        data['linear'] = self.linear
        data['quadratic'] = self.quadratic
        return data

