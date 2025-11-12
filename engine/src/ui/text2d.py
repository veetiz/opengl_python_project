"""
Text2D Module
Represents individual 2D text objects with properties.
"""

from typing import Optional, Tuple, TYPE_CHECKING
from .font import Font
from ..scene.entity import Entity

if TYPE_CHECKING:
    from .base_text import BaseText


class Text2D(Entity):
    """
    Represents a 2D text object with content, position, styling, and identification.
    This is a simple data object - rendering is handled by BaseText.
    """
    
    def __init__(
        self,
        label: str,
        text: str = "",
        font: Optional[Font] = None,
        x: float = 0.0,
        y: float = 0.0,
        size: float = 24.0,
        scale: float = 1.0,
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        visible: bool = True
    ):
        """
        Initialize Text2D object.
        
        Args:
            label: Unique identifier for this text object (also used as entity name)
            text: The actual text content to display
            font: Font to use for rendering (can be set later)
            x: X position in pixels (left edge)
            y: Y position in pixels (top edge)
            size: Font size in pixels
            scale: Additional scale factor (1.0 = normal)
            color: RGB color tuple (0.0-1.0)
            visible: Whether this text should be rendered
        """
        # Initialize Entity base class
        super().__init__(name=label)
        
        # Text-specific properties
        self.label = label
        self.text = text
        self.font = font
        self.x = x
        self.y = y
        self.size = size
        self.scale = scale
        self.color = color
        
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
    
    def set_text(self, text: str):
        """
        Update the text content.
        
        Args:
            text: New text content
        """
        self.text = text
    
    def set_position(self, x: float, y: float):
        """
        Update the position.
        
        Args:
            x: X position in pixels
            y: Y position in pixels
        """
        self.x = x
        self.y = y
    
    def set_color(self, color: Tuple[float, float, float]):
        """
        Update the color.
        
        Args:
            color: RGB color tuple (0.0-1.0)
        """
        self.color = color
    
    def set_scale(self, scale: float):
        """
        Update the scale factor.
        
        Args:
            scale: Scale factor (1.0 = normal)
        """
        self.scale = scale
    
    def set_font(self, font: Font):
        """
        Set or update the font.
        
        Args:
            font: Font to use
        """
        self.font = font
    
    def show(self):
        """Make this text visible."""
        self.visible = True
    
    def hide(self):
        """Hide this text."""
        self.visible = False
    
    def toggle_visibility(self):
        """Toggle visibility."""
        self.visible = not self.visible
    
    def get_width(self) -> int:
        """
        Calculate the width of the text in pixels.
        
        Returns:
            Width in pixels, or 0 if no font is set
        """
        if not self.font:
            return 0
        return int(self.font.get_text_width(self.text) * self.scale)
    
    def __repr__(self) -> str:
        return f"Text2D(label='{self.label}', text='{self.text[:20]}...', pos=({self.x}, {self.y}), visible={self.visible})"
