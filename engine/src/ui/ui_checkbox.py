"""
UI Checkbox Widget
Toggle checkbox for boolean values.
"""

from .ui_element import UIElement, Anchor
from typing import Optional, Callable, Tuple


class UICheckbox(UIElement):
    """Toggle checkbox widget."""
    
    def __init__(
        self,
        x: float,
        y: float,
        label: str = "",
        checked: bool = False,
        anchor: Anchor = Anchor.TOP_LEFT,
        on_toggle: Optional[Callable[[bool], None]] = None,
        box_size: float = 20.0,
        box_color: Tuple[float, float, float] = (0.3, 0.3, 0.3),
        check_color: Tuple[float, float, float] = (0.4, 0.8, 0.4),
        text_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ):
        """
        Initialize checkbox.
        
        Args:
            x, y: Position
            label: Label text
            checked: Initial checked state
            anchor: Anchor point
            on_toggle: Callback when toggled (receives new state)
            box_size: Size of checkbox box
            box_color: Box color
            check_color: Checkmark color
            text_color: Label text color
        """
        width = box_size + 10 + len(label) * 12
        super().__init__(x, y, width, box_size, anchor)
        
        self.label = label
        self._checked = checked
        self.on_toggle = on_toggle
        
        self.box_size = box_size
        self.box_color = box_color
        self.check_color = check_color
        self.text_color = text_color
        
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
    
    def render(self, text_renderer):
        """Render the checkbox."""
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        
        # Draw box
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            box_char = "☐" if not self._checked else "☑"
            text_renderer.render_text(
                text_renderer.font,
                box_char,
                int(x),
                int(y),
                scale=1.2,
                color=self.check_color if self._checked else self.box_color
            )
            
            # Draw label
            if self.label:
                text_renderer.render_text(
                    text_renderer.font,
                    self.label,
                    int(x + self.box_size + 10),
                    int(y + 3),
                    scale=0.8,
                    color=self.text_color
                )
        
        # Render children
        super().render(text_renderer)

