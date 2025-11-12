"""
UI Panel Widget
Container panel for organizing UI elements.
"""

from .ui_element import UIElement, Anchor
from typing import Tuple


class UIPanel(UIElement):
    """Container panel for UI elements."""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        anchor: Anchor = Anchor.TOP_LEFT,
        bg_color: Tuple[float, float, float, float] = (0.1, 0.1, 0.1, 0.8),
        border_color: Tuple[float, float, float] = (0.4, 0.4, 0.4),
        border_width: float = 2.0,
        padding: float = 10.0
    ):
        """
        Initialize panel.
        
        Args:
            x, y: Position
            width, height: Size
            anchor: Anchor point
            bg_color: Background color (RGBA)
            border_color: Border color (RGB)
            border_width: Border width in pixels
            padding: Internal padding
        """
        super().__init__(x, y, width, height, anchor)
        
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        
        # Set padding
        self.padding_left = padding
        self.padding_right = padding
        self.padding_top = padding
        self.padding_bottom = padding
    
    def render(self, text_renderer):
        """Render the panel and its children."""
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        
        # Draw background
        self._draw_background(text_renderer, x, y)
        
        # Draw border
        self._draw_border(text_renderer, x, y)
        
        # Render children (they use padding automatically)
        super().render(text_renderer)
    
    def _draw_background(self, text_renderer, x, y):
        """Draw panel background."""
        # Simple background representation
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            # Draw semi-transparent background using █ characters
            bg_char = "█"
            for row in range(int(self.height / 20)):
                text_renderer.render_text(
                    text_renderer.font,
                    bg_char * int(self.width / 10),
                    int(x),
                    int(y + row * 20),
                    scale=0.5,
                    color=self.bg_color[:3]  # RGB only for text renderer
                )
    
    def _draw_border(self, text_renderer, x, y):
        """Draw panel border."""
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            # Top border
            text_renderer.render_text(
                text_renderer.font,
                "─" * int(self.width / 8),
                int(x),
                int(y),
                scale=0.5,
                color=self.border_color
            )
            
            # Bottom border
            text_renderer.render_text(
                text_renderer.font,
                "─" * int(self.width / 8),
                int(x),
                int(y + self.height - 10),
                scale=0.5,
                color=self.border_color
            )

