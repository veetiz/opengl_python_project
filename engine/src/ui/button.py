"""
UI Button Component
OpenGL-based button with smooth graphics and customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import ButtonStyle, Colors
from .ui_units import UISize
from typing import Optional, Callable, Union


class UIButton(UIElement):
    """UI button with OpenGL rendering."""
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        width: Union[float, UISize] = 100.0,
        height: Union[float, UISize] = 40.0,
        text: str = "Button",
        anchor: Anchor = Anchor.TOP_LEFT,
        on_click: Optional[Callable] = None,
        style: Optional[ButtonStyle] = None,
        **kwargs
    ):
        """
        Initialize modern button with CSS-like sizing support.
        
        Args:
            x, y: Position (supports px, %, vw, vh, rem, em, calc)
            width, height: Size (supports all units)
            text: Button text
            anchor: Anchor point
            on_click: Click callback
            style: Button style (uses default if None)
            **kwargs: Additional CSS-like parameters (min_width, max_width, etc.)
        """
        # Import here to avoid circular dependency
        from .ui_units import px
        from .ui_calc import UICalc
        
        # Convert to float for UIElement
        x_val = float(x) if isinstance(x, (int, float)) else 0.0
        y_val = float(y) if isinstance(y, (int, float)) else 0.0
        width_val = float(width) if isinstance(width, (int, float)) else 100.0
        height_val = float(height) if isinstance(height, (int, float)) else 40.0
        
        super().__init__(x_val, y_val, width_val, height_val, anchor)
        
        # Store CSS-like sizes
        self.x_size = x if isinstance(x, (UISize, UICalc)) else px(x)
        self.y_size = y if isinstance(y, (UISize, UICalc)) else px(y)
        self.width_size = width if isinstance(width, (UISize, UICalc)) else px(width)
        self.height_size = height if isinstance(height, (UISize, UICalc)) else px(height)
        
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
        
        # Use compiled sizes for rendering
        w = self.compiled_width if hasattr(self, 'compiled_width') else self.width
        h = self.compiled_height if hasattr(self, 'compiled_height') else self.height
        
        # Draw background
        ui_renderer.draw_rect(
            x, y, w, h,
            color.to_tuple()
        )
        
        # Draw border
        ui_renderer.draw_border_rect(
            x, y, w, h,
            self.style.border_width,
            self.style.border_color.to_tuple()
        )
        
        # Draw text (centered - use compiled sizes for accurate centering)
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            # Text centering calculation
            text_width = len(self.text) * 10 * self.style.text_size  # Restored original
            text_height = 16 * self.style.text_size
            # Center text in button
            text_x = x + (w - text_width) / 2
            text_y = y + (h - text_height) / 2 + text_height
            
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

