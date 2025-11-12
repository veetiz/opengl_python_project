"""
UI Slider Widget
Draggable slider for adjusting numeric values.
"""

from .ui_element import UIElement, Anchor
from typing import Optional, Callable, Tuple


class UISlider(UIElement):
    """Draggable slider widget for numeric values."""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float = 20.0,
        min_value: float = 0.0,
        max_value: float = 1.0,
        current_value: float = 0.5,
        anchor: Anchor = Anchor.TOP_LEFT,
        on_value_change: Optional[Callable[[float], None]] = None,
        label: str = "",
        track_color: Tuple[float, float, float] = (0.2, 0.2, 0.2),
        fill_color: Tuple[float, float, float] = (0.4, 0.6, 0.8),
        handle_color: Tuple[float, float, float] = (0.8, 0.8, 0.8),
        text_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ):
        """
        Initialize slider.
        
        Args:
            x, y: Position
            width, height: Size
            min_value: Minimum value
            max_value: Maximum value
            current_value: Starting value
            anchor: Anchor point
            on_value_change: Callback when value changes
            label: Optional label text
            track_color: Track background color
            fill_color: Fill color
            handle_color: Handle color
            text_color: Text color
        """
        super().__init__(x, y, width, height, anchor)
        
        self.min_value = min_value
        self.max_value = max_value
        self._value = max(min_value, min(max_value, current_value))
        self.on_value_change = on_value_change
        
        self.label = label
        self.track_color = track_color
        self.fill_color = fill_color
        self.handle_color = handle_color
        self.text_color = text_color
        
        # Handle state
        self.is_dragging = False
        self.handle_width = 12.0
    
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
        
        # Calculate percentage
        relative_x = mouse_x - x
        percentage = max(0.0, min(1.0, relative_x / self.width))
        
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
    
    def render(self, text_renderer):
        """Render the slider."""
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        
        # Draw label if provided
        if self.label and text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text_renderer.render_text(
                text_renderer.font,
                self.label,
                int(x),
                int(y - 20),
                scale=0.7,
                color=self.text_color
            )
        
        # Draw track (background)
        self._draw_track(text_renderer, x, y)
        
        # Draw fill (value indicator)
        self._draw_fill(text_renderer, x, y)
        
        # Draw handle
        self._draw_handle(text_renderer, x, y)
        
        # Draw value text
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            value_text = f"{self._value:.2f}"
            text_renderer.render_text(
                text_renderer.font,
                value_text,
                int(x + self.width + 10),
                int(y + 2),
                scale=0.6,
                color=self.text_color
            )
        
        # Render children
        super().render(text_renderer)
    
    def _draw_track(self, text_renderer, x, y):
        """Draw slider track."""
        # Simple representation with text
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            track = "─" * int(self.width / 8)
            text_renderer.render_text(
                text_renderer.font,
                track,
                int(x),
                int(y + self.height / 2),
                scale=0.5,
                color=self.track_color
            )
    
    def _draw_fill(self, text_renderer, x, y):
        """Draw slider fill (shows current value)."""
        percentage = self.get_value_percentage()
        fill_width = self.width * percentage
        
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            fill = "━" * int(fill_width / 8)
            text_renderer.render_text(
                text_renderer.font,
                fill,
                int(x),
                int(y + self.height / 2),
                scale=0.5,
                color=self.fill_color
            )
    
    def _draw_handle(self, text_renderer, x, y):
        """Draw slider handle."""
        percentage = self.get_value_percentage()
        handle_x = x + (self.width - self.handle_width) * percentage
        
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text_renderer.render_text(
                text_renderer.font,
                "●",
                int(handle_x),
                int(y + self.height / 2 - 8),
                scale=1.0,
                color=self.handle_color
            )

