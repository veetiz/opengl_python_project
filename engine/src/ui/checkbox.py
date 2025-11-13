"""
UI Checkbox Component
OpenGL-based checkbox with smooth graphics and customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import CheckboxStyle
from .ui_units import UISize
from typing import Optional, Callable, Union


class UICheckbox(UIElement):
    """UI checkbox with OpenGL rendering."""
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        label: str = "",
        checked: bool = False,
        anchor: Anchor = Anchor.TOP_LEFT,
        on_toggle: Optional[Callable[[bool], None]] = None,
        style: Optional[CheckboxStyle] = None,
        **kwargs
    ):
        """
        Initialize modern checkbox with CSS-like sizing support.
        
        Args:
            x, y: Position (supports px, %, vw, vh, rem, em, calc)
            label: Label text
            checked: Initial checked state
            anchor: Anchor point
            on_toggle: Toggle callback
            style: Checkbox style (uses default if None)
            **kwargs: Additional CSS-like parameters
        """
        # Import here to avoid circular dependency
        from .ui_units import px
        from .ui_calc import UICalc
        
        self.style = style or CheckboxStyle()
        
        # Width includes box + spacing + label
        width = self.style.box_size + 10 + len(label) * 12
        height = self.style.box_size
        
        # Convert to float for UIElement
        x_val = float(x) if isinstance(x, (int, float)) else 0.0
        y_val = float(y) if isinstance(y, (int, float)) else 0.0
        
        super().__init__(x_val, y_val, width, height, anchor)
        
        # Store CSS-like sizes
        self.x_size = x if isinstance(x, (UISize, UICalc)) else px(x)
        self.y_size = y if isinstance(y, (UISize, UICalc)) else px(y)
        
        # Compiled sizes
        self.compiled_x = x_val
        self.compiled_y = y_val
        
        self.label = label
        self._checked = checked
        self.on_toggle = on_toggle
        
        # Override click handler
        self.on_click = self._handle_toggle
    
    @property
    def checked(self) -> bool:
        """Get checked state."""
        return self._checked
    
    @checked.setter
    def checked(self, value: bool):
        """Set checked state and trigger callback."""
        if self._checked != value:
            self._checked = value
            if self.on_toggle:
                self.on_toggle(value)
    
    def _handle_toggle(self):
        """Handle click to toggle."""
        self.checked = not self._checked
    
    def toggle(self):
        """Toggle the checkbox."""
        self.checked = not self._checked
    
    def render(self, ui_renderer, text_renderer):
        """
        Render the checkbox using OpenGL.
        
        Args:
            ui_renderer: ModernUIRenderer instance
            text_renderer: TextRenderer for label
        """
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        box_size = self.style.box_size
        
        # Draw checkbox box
        box_color = self.style.box_hover_color if self.is_hovered else self.style.box_color
        ui_renderer.draw_rect(
            x, y, box_size, box_size,
            box_color.to_tuple()
        )
        
        # Draw border
        ui_renderer.draw_border_rect(
            x, y, box_size, box_size,
            self.style.border_width,
            self.style.box_border_color.to_tuple()
        )
        
        # Draw checkmark if checked
        if self._checked:
            padding = self.style.check_padding
            check_color = self.style.check_hover_color if self.is_hovered else self.style.check_color
            
            # Draw checkmark as smaller filled rectangle
            ui_renderer.draw_rect(
                x + padding,
                y + padding,
                box_size - padding * 2,
                box_size - padding * 2,
                check_color.to_tuple()
            )
        
        # Draw label (scaled positioning)
        if self.label and text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            label_offset_x = 10 * self.style.text_size  # Scale horizontal spacing
            label_offset_y = 8 * self.style.text_size   # Scale vertical offset
            label_x = x + box_size + label_offset_x
            label_y = y + box_size / 2 + label_offset_y
            
            text_renderer.render_text(
                text_renderer.font,
                self.label,
                int(label_x),
                int(label_y),
                scale=self.style.text_size,
                color=self.style.text_color.to_rgb()
            )
        
        # Render children (pass both renderers!)
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

