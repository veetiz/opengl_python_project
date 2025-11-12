"""
UI Label Component
Text label with customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import LabelStyle
from .ui_units import UISize
from typing import Optional, Union


class UILabel(UIElement):
    """UI text label."""
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        text: str = "",
        width: Optional[Union[float, UISize]] = None,
        height: Optional[Union[float, UISize]] = None,
        anchor: Anchor = Anchor.TOP_LEFT,
        style: Optional[LabelStyle] = None,
        size: float = 1.0,
        bold: bool = False,
        **kwargs
    ):
        """
        Initialize modern label with CSS-like sizing support.
        
        Args:
            x, y: Position (supports px, %, vw, vh, rem, em, calc)
            text: Label text
            width, height: Size (optional, auto-calculated from text if None)
            anchor: Anchor point
            style: Label style (uses default if None)
            size: Text size multiplier
            bold: Bold text (not implemented yet)
            **kwargs: Additional CSS-like parameters
        """
        # Import here to avoid circular dependency
        from .ui_units import px
        from .ui_calc import UICalc
        
        # Approximate size based on text length (if not provided)
        default_width = len(text) * 12 * size
        default_height = 20 * size
        
        # Use provided size or default
        width_val = float(width) if isinstance(width, (int, float)) else default_width if width is None else 0.0
        height_val = float(height) if isinstance(height, (int, float)) else default_height if height is None else 0.0
        
        # Convert position to float
        x_val = float(x) if isinstance(x, (int, float)) else 0.0
        y_val = float(y) if isinstance(y, (int, float)) else 0.0
        
        super().__init__(x_val, y_val, width_val, height_val, anchor)
        
        # Store CSS-like sizes
        self.x_size = x if isinstance(x, (UISize, UICalc)) else px(x)
        self.y_size = y if isinstance(y, (UISize, UICalc)) else px(y)
        self.width_size = width if isinstance(width, (UISize, UICalc)) else px(width_val) if width is not None else px(default_width)
        self.height_size = height if isinstance(height, (UISize, UICalc)) else px(height_val) if height is not None else px(default_height)
        
        # Store constraints from kwargs
        for key in ['min_width', 'max_width', 'min_height', 'max_height', 'aspect_ratio']:
            if key in kwargs:
                val = kwargs[key]
                if key == 'aspect_ratio':
                    setattr(self, key, val)
                else:
                    setattr(self, f'{key}_size', val if val is None or isinstance(val, (UISize, UICalc)) else px(val))
        
        # Compiled sizes
        self.compiled_x = x_val
        self.compiled_y = y_val
        self.compiled_width = width_val
        self.compiled_height = height_val
        
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

