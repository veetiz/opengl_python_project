"""
Text3D Module
Represents individual 3D text objects with properties.
"""

from typing import Optional, Tuple, TYPE_CHECKING
from .font import Font
from ..scene.entity import Entity
from ..scene.gameobject import Transform

if TYPE_CHECKING:
    pass


class Text3D(Entity):
    """
    Represents a 3D text object that can be placed in world space.
    Supports billboard mode (always faces camera) or world-oriented mode.
    """
    
    def __init__(
        self,
        label: str,
        text: str = "",
        font: Optional[Font] = None,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        scale: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        size: float = 0.1,  # Size in world units
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        billboard: bool = True,  # Always face camera?
        visible: bool = True
    ):
        """
        Initialize Text3D object.
        
        Args:
            label: Unique identifier for this text object (also used as entity name)
            text: The actual text content to display
            font: Font to use for rendering (can be set later)
            position: Position in 3D world space
            rotation: Rotation in degrees (only used if billboard=False)
            scale: Scale factors (x, y, z)
            size: Base size of text in world units
            color: RGB color tuple (0.0-1.0)
            billboard: If True, text always faces camera; if False, uses rotation
            visible: Whether this text should be rendered
        """
        # Initialize Entity base class
        super().__init__(name=label)
        
        # Set transform
        self.transform = Transform(position=position, rotation=rotation, scale=scale)
        
        # Text-specific properties
        self.label = label
        self.text = text
        self.font = font
        self.size = size
        self.color = color
        self.billboard = billboard
        
        # Override entity active with visible
        self.active = visible
    
    @property
    def visible(self) -> bool:
        """Get visibility (alias for active)."""
        return self.active
    
    @visible.setter
    def visible(self, value: bool):
        """Set visibility (alias for active)."""
        self.active = value
    
    @property
    def position(self) -> Tuple[float, float, float]:
        """Get position (shortcut to transform)."""
        return tuple(self.transform.position)
    
    @position.setter
    def position(self, value: Tuple[float, float, float]):
        """Set position (shortcut to transform)."""
        self.transform.set_position(*value)
    
    def set_text(self, text: str):
        """
        Update the text content.
        
        Args:
            text: New text content
        """
        self.text = text
    
    def set_color(self, color: Tuple[float, float, float]):
        """
        Update the color.
        
        Args:
            color: RGB color tuple (0.0-1.0)
        """
        self.color = color
    
    def set_font(self, font: Font):
        """
        Set or update the font.
        
        Args:
            font: Font to use
        """
        self.font = font
    
    def set_billboard(self, billboard: bool):
        """
        Set billboard mode.
        
        Args:
            billboard: If True, text always faces camera
        """
        self.billboard = billboard
    
    def show(self):
        """Make this text visible."""
        self.visible = True
    
    def hide(self):
        """Hide this text."""
        self.visible = False
    
    def toggle_visibility(self):
        """Toggle visibility."""
        self.visible = not self.visible
    
    def __repr__(self) -> str:
        return f"Text3D(label='{self.label}', text='{self.text[:20]}...', pos={self.position}, billboard={self.billboard}, visible={self.visible})"

