"""
UI Button Widget
Interactive button with hover and click states.
"""

from .ui_element import UIElement, Anchor
from typing import Optional, Callable, Tuple


class UIButton(UIElement):
    """Interactive button widget."""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        text: str = "Button",
        anchor: Anchor = Anchor.TOP_LEFT,
        on_click: Optional[Callable] = None,
        bg_color: Tuple[float, float, float] = (0.3, 0.3, 0.3),
        hover_color: Tuple[float, float, float] = (0.4, 0.4, 0.4),
        press_color: Tuple[float, float, float] = (0.2, 0.2, 0.2),
        text_color: Tuple[float, float, float] = (1.0, 1.0, 1.0),
        text_size: float = 1.0
    ):
        """
        Initialize button.
        
        Args:
            x, y: Position
            width, height: Size
            text: Button text
            anchor: Anchor point
            on_click: Click callback
            bg_color: Background color (RGB)
            hover_color: Hover state color
            press_color: Pressed state color
            text_color: Text color
            text_size: Text scale
        """
        super().__init__(x, y, width, height, anchor)
        
        self.text = text
        self.on_click = on_click
        
        # Colors
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.press_color = press_color
        self.text_color = text_color
        self.text_size = text_size
        
        # Border
        self.border_width = 2.0
        self.border_color = (0.5, 0.5, 0.5)
    
    def get_current_color(self) -> Tuple[float, float, float]:
        """Get current color based on state."""
        if self.is_pressed:
            return self.press_color
        elif self.is_hovered:
            return self.hover_color
        else:
            return self.bg_color
    
    def render(self, text_renderer):
        """Render the button."""
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        
        # Get current color
        color = self.get_current_color()
        
        # Draw background box (using text renderer - we'll draw rectangles with █ character)
        # This is a simple approach - in production you'd use GL primitives
        self._draw_box(text_renderer, x, y, self.width, self.height, color)
        
        # Draw text centered
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text_x = x + self.width / 2 - len(self.text) * 6 * self.text_size  # Rough centering
            text_y = y + self.height / 2 - 8 * self.text_size
            
            text_renderer.render_text(
                text_renderer.font,
                self.text,
                int(text_x),
                int(text_y),
                scale=self.text_size,
                color=self.text_color
            )
        
        # Render children
        super().render(text_renderer)
    
    def _draw_box(self, text_renderer, x, y, width, height, color):
        """Draw a colored box (simple implementation using text renderer)."""
        # In production, you'd use OpenGL to draw rectangles
        # For now, this is a placeholder that draws a border
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            # Draw border outline with text (simple visual)
            border_char = "#"
            text_renderer.render_text(
                text_renderer.font,
                border_char * int(width / 8),
                int(x),
                int(y),
                scale=0.5,
                color=self.border_color
            )

