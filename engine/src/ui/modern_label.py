"""
Modern Label Component
Text label with customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import LabelStyle
from typing import Optional


class ModernLabel(UIElement):
    """Modern text label."""
    
    def __init__(
        self,
        x: float,
        y: float,
        text: str = "",
        anchor: Anchor = Anchor.TOP_LEFT,
        style: Optional[LabelStyle] = None,
        size: float = 1.0,
        bold: bool = False
    ):
        """
        Initialize modern label.
        
        Args:
            x, y: Position
            text: Label text
            anchor: Anchor point
            style: Label style (uses default if None)
            size: Text size multiplier
            bold: Bold text (not implemented yet)
        """
        # Approximate size based on text length
        width = len(text) * 12 * size
        height = 20 * size
        
        super().__init__(x, y, width, height, anchor)
        
        self.text = text
        self.style = style or LabelStyle()
        self.size = size
        self.bold = bold
    
    def set_text(self, text: str):
        """Update label text."""
        self.text = text
        # Update width
        self.width = len(text) * 12 * self.size
    
    def render(self, ui_renderer, text_renderer):
        """
        Render the label.
        
        Args:
            ui_renderer: ModernUIRenderer instance (not used for labels)
            text_renderer: TextRenderer for text
        """
        if not self.visible or not self.text:
            return
        
        x, y = self.get_absolute_position()
        
        # Draw background if not transparent
        if self.style.bg_color.a > 0:
            ui_renderer.draw_rect(
                x, y, self.width, self.height,
                self.style.bg_color.to_tuple()
            )
        
        # Draw text
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text_renderer.render_text(
                text_renderer.font,
                self.text,
                int(x),
                int(y + self.height),
                scale=self.size * self.style.text_size,
                color=self.style.text_color.to_rgb()
            )
        
        # Render children (pass both renderers!)
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

