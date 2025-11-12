"""
UI Panel Component
OpenGL-based panel container with customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import PanelStyle
from typing import Optional


class UIPanel(UIElement):
    """UI panel container with OpenGL rendering."""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        anchor: Anchor = Anchor.TOP_LEFT,
        style: Optional[PanelStyle] = None
    ):
        """
        Initialize modern panel.
        
        Args:
            x, y: Position
            width, height: Size
            anchor: Anchor point
            style: Panel style (uses default if None)
        """
        super().__init__(x, y, width, height, anchor)
        
        self.style = style or PanelStyle()
        
        # Set padding from style
        self.padding_left = self.style.padding
        self.padding_right = self.style.padding
        self.padding_top = self.style.padding
        self.padding_bottom = self.style.padding
    
    def render(self, ui_renderer, text_renderer):
        """
        Render the panel using OpenGL.
        
        Args:
            ui_renderer: ModernUIRenderer instance
            text_renderer: TextRenderer for text
        """
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        
        # Draw background
        ui_renderer.draw_rect(
            x, y, self.width, self.height,
            self.style.bg_color.to_tuple()
        )
        
        # Draw border
        if self.style.border_width > 0:
            ui_renderer.draw_border_rect(
                x, y, self.width, self.height,
                self.style.border_width,
                self.style.border_color.to_tuple()
            )
        
        # Render children (pass both renderers!)
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

