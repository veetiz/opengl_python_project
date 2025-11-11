"""
Material Module
Defines surface material properties for lighting calculations.
"""

from typing import Tuple, Optional
from .texture import Texture


class Material:
    """
    Material class defining surface properties for lighting.
    Based on Phong/Blinn-Phong lighting model.
    """
    
    def __init__(
        self,
        name: str = "Material",
        ambient: Tuple[float, float, float] = (0.2, 0.2, 0.2),
        diffuse: Tuple[float, float, float] = (0.8, 0.8, 0.8),
        specular: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        shininess: float = 32.0,
        texture: Optional[Texture] = None,
        normal_map: Optional[Texture] = None
    ):
        """
        Initialize a material.
        
        Args:
            name: Material name
            ambient: Ambient color (how much ambient light affects this material)
            diffuse: Diffuse color (main surface color)
            specular: Specular color (highlight color)
            shininess: Shininess factor (higher = smaller, sharper highlights)
            texture: Optional diffuse/albedo texture
            normal_map: Optional normal map texture for surface detail
        """
        self.name = name
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.texture = texture
        self.normal_map = normal_map
    
    def set_ambient(self, ambient: Tuple[float, float, float]):
        """Set ambient color."""
        self.ambient = ambient
    
    def set_diffuse(self, diffuse: Tuple[float, float, float]):
        """Set diffuse color."""
        self.diffuse = diffuse
    
    def set_specular(self, specular: Tuple[float, float, float]):
        """Set specular color."""
        self.specular = specular
    
    def set_shininess(self, shininess: float):
        """Set shininess factor."""
        self.shininess = max(1.0, shininess)  # Clamp to minimum of 1
    
    def set_texture(self, texture: Optional[Texture]):
        """Set or update the diffuse texture."""
        self.texture = texture
    
    def set_normal_map(self, normal_map: Optional[Texture]):
        """Set or update the normal map texture."""
        self.normal_map = normal_map
    
    @staticmethod
    def create_default() -> 'Material':
        """Create a default material with standard properties."""
        return Material(
            name="Default",
            ambient=(0.2, 0.2, 0.2),
            diffuse=(0.8, 0.8, 0.8),
            specular=(1.0, 1.0, 1.0),
            shininess=32.0
        )
    
    @staticmethod
    def create_matte() -> 'Material':
        """Create a matte material (no specular highlights)."""
        return Material(
            name="Matte",
            ambient=(0.2, 0.2, 0.2),
            diffuse=(0.8, 0.8, 0.8),
            specular=(0.0, 0.0, 0.0),
            shininess=1.0
        )
    
    @staticmethod
    def create_shiny() -> 'Material':
        """Create a shiny material (strong specular)."""
        return Material(
            name="Shiny",
            ambient=(0.1, 0.1, 0.1),
            diffuse=(0.7, 0.7, 0.7),
            specular=(1.0, 1.0, 1.0),
            shininess=128.0
        )
    
    @staticmethod
    def create_metal() -> 'Material':
        """Create a metallic material."""
        return Material(
            name="Metal",
            ambient=(0.05, 0.05, 0.05),
            diffuse=(0.4, 0.4, 0.4),
            specular=(0.8, 0.8, 0.8),
            shininess=256.0
        )
    
    def __repr__(self) -> str:
        return f"Material(name='{self.name}', shininess={self.shininess})"

