"""
UI Label Widget
Non-interactive text label.
"""

from .ui_element import UIElement, Anchor
from typing import Tuple


class UILabel(UIElement):
    """Static text label widget."""
    
    def __init__(
        self,
        x: float,
        y: float,
        text: str = "Label",
        anchor: Anchor = Anchor.TOP_LEFT,
        color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        size: float = 1.0,
        bold: bool = False
    ):
        """
        Initialize label.
        
        Args:
            x, y: Position
            text: Label text
            anchor: Anchor point
            color: Text color (RGB)
            size: Text scale
            bold: Bold text (simulated with double-render)
        """
        # Calculate approximate size based on text
        width = len(text) * 12 * size
        height = 24 * size
        
        super().__init__(x, y, width, height, anchor, enabled=False)
        
        self.text = text
        self.color = color
        self.size = size
        self.bold = bold
    
    def set_text(self, text: str):
        """Update label text."""
        self.text = text
        # Update size
        self.width = len(text) * 12 * self.size
        self.height = 24 * self.size
    
    def render(self, text_renderer):
        """Render the label."""
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text_renderer.render_text(
                text_renderer.font,
                self.text,
                int(x),
                int(y),
                scale=self.size,
                color=self.color
            )
            
            # Simulate bold by rendering twice with slight offset
            if self.bold:
                text_renderer.render_text(
                    text_renderer.font,
                    self.text,
                    int(x + 1),
                    int(y),
                    scale=self.size,
                    color=self.color
                )
        
        # Render children
        super().render(text_renderer)

