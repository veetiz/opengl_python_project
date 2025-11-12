"""
UI Panel Component
OpenGL-based panel container with customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import PanelStyle
from .ui_units import UISize
from typing import Optional, Union


class UIPanel(UIElement):
    """UI panel container with OpenGL rendering."""
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        width: Union[float, UISize] = 100.0,
        height: Union[float, UISize] = 100.0,
        min_width: Optional[Union[float, UISize]] = None,
        max_width: Optional[Union[float, UISize]] = None,
        min_height: Optional[Union[float, UISize]] = None,
        max_height: Optional[Union[float, UISize]] = None,
        aspect_ratio: Optional[float] = None,
        anchor: Anchor = Anchor.TOP_LEFT,
        style: Optional[PanelStyle] = None,
        **kwargs
    ):
        """
        Initialize modern panel with CSS-like sizing support.
        
        Args:
            x, y: Position (supports px, %, vw, vh, rem, em, calc)
            width, height: Size (supports all units)
            min_width, max_width: Width constraints
            min_height, max_height: Height constraints
            aspect_ratio: Width/height ratio
            anchor: Anchor point
            style: Panel style (uses default if None)
            **kwargs: Additional UIElement/UIComponent parameters
        """
        # Import here to avoid circular dependency
        from .ui_units import px
        from .ui_calc import UICalc
        
        # Convert to float for UIElement (will be compiled later)
        x_val = float(x) if isinstance(x, (int, float)) else 0.0
        y_val = float(y) if isinstance(y, (int, float)) else 0.0
        width_val = float(width) if isinstance(width, (int, float)) else 100.0
        height_val = float(height) if isinstance(height, (int, float)) else 100.0
        
        super().__init__(x_val, y_val, width_val, height_val, anchor)
        
        # Store CSS-like sizes (for UICompiler)
        self.x_size = x if isinstance(x, (UISize, UICalc)) else px(x)
        self.y_size = y if isinstance(y, (UISize, UICalc)) else px(y)
        self.width_size = width if isinstance(width, (UISize, UICalc)) else px(width)
        self.height_size = height if isinstance(height, (UISize, UICalc)) else px(height)
        
        # Store constraints
        self.min_width_size = min_width if min_width is None or isinstance(min_width, (UISize, UICalc)) else px(min_width)
        self.max_width_size = max_width if max_width is None or isinstance(max_width, (UISize, UICalc)) else px(max_width)
        self.min_height_size = min_height if min_height is None or isinstance(min_height, (UISize, UICalc)) else px(min_height)
        self.max_height_size = max_height if max_height is None or isinstance(max_height, (UISize, UICalc)) else px(max_height)
        
        # Store aspect ratio
        self.aspect_ratio = aspect_ratio
        
        # Compiled sizes (will be set by UICompiler)
        self.compiled_x = x_val
        self.compiled_y = y_val
        self.compiled_width = width_val
        self.compiled_height = height_val
        self.compiled_min_width = None
        self.compiled_max_width = None
        self.compiled_min_height = None
        self.compiled_max_height = None
        
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
        
        # Use compiled sizes for rendering
        w = self.compiled_width if hasattr(self, 'compiled_width') else self.width
        h = self.compiled_height if hasattr(self, 'compiled_height') else self.height
        
        # Draw background
        ui_renderer.draw_rect(
            x, y, w, h,
            self.style.bg_color.to_tuple()
        )
        
        # Draw border
        if self.style.border_width > 0:
            ui_renderer.draw_border_rect(
                x, y, w, h,
                self.style.border_width,
                self.style.border_color.to_tuple()
            )
        
        # Render children (pass both renderers!)
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

