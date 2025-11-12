"""
UI Slider Component
OpenGL-based slider with smooth graphics and customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import SliderStyle
from .ui_units import UISize
from typing import Optional, Callable, Union


class UISlider(UIElement):
    """UI slider with OpenGL rendering."""
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        width: Union[float, UISize] = 200.0,
        height: Union[float, UISize] = 30.0,
        min_value: float = 0.0,
        max_value: float = 1.0,
        current_value: float = 0.5,
        anchor: Anchor = Anchor.TOP_LEFT,
        on_value_change: Optional[Callable[[float], None]] = None,
        label: str = "",
        style: Optional[SliderStyle] = None,
        **kwargs
    ):
        """
        Initialize modern slider with CSS-like sizing support.
        
        Args:
            x, y: Position (supports px, %, vw, vh, rem, em, calc)
            width, height: Size (supports all units)
            min_value: Minimum value
            max_value: Maximum value
            current_value: Starting value
            anchor: Anchor point
            on_value_change: Value change callback
            label: Optional label
            style: Slider style (uses default if None)
            **kwargs: Additional CSS-like parameters
        """
        # Import here to avoid circular dependency
        from .ui_units import px
        from .ui_calc import UICalc
        
        # Convert to float for UIElement
        x_val = float(x) if isinstance(x, (int, float)) else 0.0
        y_val = float(y) if isinstance(y, (int, float)) else 0.0
        width_val = float(width) if isinstance(width, (int, float)) else 200.0
        height_val = float(height) if isinstance(height, (int, float)) else 30.0
        
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
        
        self.min_value = min_value
        self.max_value = max_value
        self._value = max(min_value, min(max_value, current_value))
        self.on_value_change = on_value_change
        self.label = label
        self.style = style or SliderStyle()
        
        # State
        self.is_dragging = False
    
    @property
    def value(self) -> float:
        """Get current value."""
        return self._value
    
    @value.setter
    def value(self, val: float):
        """Set value and trigger callback."""
        old_value = self._value
        self._value = max(self.min_value, min(self.max_value, val))
        
        if self._value != old_value and self.on_value_change:
            self.on_value_change(self._value)
    
    def get_value_percentage(self) -> float:
        """Get value as percentage (0.0 - 1.0)."""
        if self.max_value == self.min_value:
            return 0.0
        return (self._value - self.min_value) / (self.max_value - self.min_value)
    
    def set_value_from_position(self, mouse_x: float):
        """Set value based on mouse X position."""
        x, y = self.get_absolute_position()
        
        # Use compiled width for accurate mouse tracking
        w = self.compiled_width if hasattr(self, 'compiled_width') else self.width
        
        # Calculate percentage
        relative_x = mouse_x - x
        percentage = max(0.0, min(1.0, relative_x / w))
        
        # Set value
        new_value = self.min_value + percentage * (self.max_value - self.min_value)
        self.value = new_value
    
    def handle_mouse_move(self, mouse_x: float, mouse_y: float) -> bool:
        """Handle mouse movement."""
        result = super().handle_mouse_move(mouse_x, mouse_y)
        
        # Update value if dragging
        if self.is_dragging:
            self.set_value_from_position(mouse_x)
            return True
        
        return result
    
    def handle_mouse_click(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        """Handle mouse click."""
        if not self.visible or not self.enabled:
            return False
        
        if button == 0 and self.contains_point(mouse_x, mouse_y):
            self.is_dragging = True
            self.is_pressed = True
            self.set_value_from_position(mouse_x)
            return True
        
        return False
    
    def handle_mouse_release(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        """Handle mouse release."""
        if self.is_dragging:
            self.is_dragging = False
            self.is_pressed = False
            return True
        
        return super().handle_mouse_release(mouse_x, mouse_y, button)
    
    def render(self, ui_renderer, text_renderer):
        """
        Render the slider using OpenGL.
        
        Args:
            ui_renderer: ModernUIRenderer instance
            text_renderer: TextRenderer for text/label
        """
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        percentage = self.get_value_percentage()
        
        # Use compiled sizes
        w = self.compiled_width if hasattr(self, 'compiled_width') else self.width
        h = self.compiled_height if hasattr(self, 'compiled_height') else self.height
        
        # Add spacing after label
        label_offset = self.style.label_spacing if self.label else 0
        
        # Calculate track position (centered vertically, accounting for label)
        track_y = y + label_offset + (h - self.style.track_height) / 2
        
        # Draw track background (FULL WIDTH - gray/empty part)
        ui_renderer.draw_rect(
            x, track_y,
            w, self.style.track_height,
            self.style.track_color.to_tuple()  # Gray for empty part
        )
        
        # Draw fill (ACTIVE PART - colored based on value)
        fill_width = w * percentage
        if fill_width > 0:
            fill_color = self.style.fill_hover_color if self.is_hovered else self.style.fill_color
            ui_renderer.draw_rect(
                x, track_y,
                fill_width, self.style.track_height,
                fill_color.to_tuple()  # Colored fill (green by default)
            )
        
        # Draw track border (around full slider - use compiled width!)
        ui_renderer.draw_border_rect(
            x, track_y,
            w, self.style.track_height,
            self.style.border_width,
            self.style.track_border_color.to_tuple()
        )
        
        # Draw handle (centered on track, use compiled width)
        handle_x = x + (w * percentage)
        handle_y = track_y + self.style.track_height / 2
        
        if self.is_pressed:
            handle_color = self.style.handle_press_color
        elif self.is_hovered:
            handle_color = self.style.handle_hover_color
        else:
            handle_color = self.style.handle_color
        
        ui_renderer.draw_circle(
            handle_x, handle_y,
            self.style.handle_radius,
            handle_color.to_tuple()
        )
        
        # Draw label well above the slider (more spacing)
        if self.label and text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text_renderer.render_text(
                text_renderer.font,
                self.label,
                int(x),
                int(y - 5),  # Above the component
                scale=0.8,
                color=(1.0, 1.0, 1.0)
            )
        
        # Draw value next to the handle (not far right)
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            # Show actual shadow value if it's shadow quality
            if "Shadow" in self.label:
                # Map value to shadow resolution
                resolutions = {0.0: 512, 0.33: 1024, 0.66: 2048, 1.0: 4096}
                closest_val = min(resolutions.keys(), key=lambda k: abs(k - percentage))
                value_text = str(resolutions[closest_val])
            else:
                # Show percentage for volume sliders
                value_text = f"{int(self._value * 100)}%"
            
            # Position value text above and to the right of handle (use compiled width)
            handle_x = x + (w * percentage)
            text_renderer.render_text(
                text_renderer.font,
                value_text,
                int(handle_x - 20),
                int(track_y - 8),
                scale=0.6,
                color=(1.0, 1.0, 1.0)
            )
        
        # Render children (pass both renderers!)
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

