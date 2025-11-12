"""
Modern Button Component
OpenGL-based button with smooth graphics and customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import ButtonStyle, Colors
from typing import Optional, Callable


class ModernButton(UIElement):
    """Modern button with OpenGL rendering."""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        text: str = "Button",
        anchor: Anchor = Anchor.TOP_LEFT,
        on_click: Optional[Callable] = None,
        style: Optional[ButtonStyle] = None
    ):
        """
        Initialize modern button.
        
        Args:
            x, y: Position
            width, height: Size
            text: Button text
            anchor: Anchor point
            on_click: Click callback
            style: Button style (uses default if None)
        """
        super().__init__(x, y, width, height, anchor)
        
        self.text = text
        self.on_click = on_click
        self.style = style or ButtonStyle()
    
    def get_current_color(self):
        """Get current background color based on state."""
        if self.is_pressed:
            return self.style.press_color
        elif self.is_hovered:
            return self.style.hover_color
        else:
            return self.style.bg_color
    
    def render(self, ui_renderer, text_renderer):
        """
        Render the button using OpenGL.
        
        Args:
            ui_renderer: ModernUIRenderer instance
            text_renderer: TextRenderer for text
        """
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        color = self.get_current_color()
        
        # Draw background
        ui_renderer.draw_rect(
            x, y, self.width, self.height,
            color.to_tuple()
        )
        
        # Draw border
        ui_renderer.draw_border_rect(
            x, y, self.width, self.height,
            self.style.border_width,
            self.style.border_color.to_tuple()
        )
        
        # Draw text (centered)
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            # Rough text centering (can be improved with proper text metrics)
            text_width = len(self.text) * 10 * self.style.text_size
            text_height = 16 * self.style.text_size
            text_x = x + (self.width - text_width) / 2
            text_y = y + (self.height - text_height) / 2 + text_height
            
            text_renderer.render_text(
                text_renderer.font,
                self.text,
                int(text_x),
                int(text_y),
                scale=self.style.text_size,
                color=self.style.text_color.to_rgb()
            )
        
        # Render children (pass both renderers!)
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

