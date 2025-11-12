"""
UI Dropdown Widget
Dropdown menu for selecting from multiple options.
"""

from .ui_element import UIElement, Anchor
from typing import List, Optional, Callable, Tuple


class UIDropdown(UIElement):
    """Dropdown menu widget."""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float = 30.0,
        options: List[str] = None,
        selected_index: int = 0,
        anchor: Anchor = Anchor.TOP_LEFT,
        on_select: Optional[Callable[[int, str], None]] = None,
        bg_color: Tuple[float, float, float] = (0.25, 0.25, 0.25),
        hover_color: Tuple[float, float, float] = (0.35, 0.35, 0.35),
        text_color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ):
        """
        Initialize dropdown.
        
        Args:
            x, y: Position
            width, height: Size
            options: List of option strings
            selected_index: Initially selected option index
            anchor: Anchor point
            on_select: Callback when option selected (index, text)
            bg_color: Background color
            hover_color: Hover color
            text_color: Text color
        """
        super().__init__(x, y, width, height, anchor)
        
        self.options = options or ["Option 1", "Option 2", "Option 3"]
        self._selected_index = max(0, min(selected_index, len(self.options) - 1))
        self.on_select = on_select
        
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.text_color = text_color
        
        # Dropdown state
        self.is_open = False
        self.hovered_option = -1
        
        # Override click handler
        self.on_click = self._handle_click
    
    @property
    def selected_index(self) -> int:
        """Get selected option index."""
        return self._selected_index
    
    @property
    def selected_text(self) -> str:
        """Get selected option text."""
        return self.options[self._selected_index]
    
    def select(self, index: int):
        """
        Select an option by index.
        
        Args:
            index: Option index to select
        """
        if 0 <= index < len(self.options):
            old_index = self._selected_index
            self._selected_index = index
            
            if old_index != index and self.on_select:
                self.on_select(index, self.options[index])
    
    def _handle_click(self):
        """Handle click to toggle dropdown."""
        self.is_open = not self.is_open
    
    def handle_mouse_click(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        """Handle mouse click."""
        if not self.visible or not self.enabled:
            return False
        
        x, y = self.get_absolute_position()
        
        # Check if clicking on an option (if dropdown is open)
        if self.is_open and button == 0:
            for i, option in enumerate(self.options):
                option_y = y + self.height + i * self.height
                if (x <= mouse_x <= x + self.width) and (option_y <= mouse_y <= option_y + self.height):
                    self.select(i)
                    self.is_open = False
                    return True
        
        # Check if clicking on main dropdown
        if self.contains_point(mouse_x, mouse_y) and button == 0:
            self._handle_click()
            return True
        
        # Close dropdown if clicking outside
        if self.is_open and not self.contains_point(mouse_x, mouse_y):
            self.is_open = False
        
        return False
    
    def handle_mouse_move(self, mouse_x: float, mouse_y: float) -> bool:
        """Handle mouse movement."""
        result = super().handle_mouse_move(mouse_x, mouse_y)
        
        # Update hovered option if dropdown is open
        if self.is_open:
            x, y = self.get_absolute_position()
            self.hovered_option = -1
            
            for i in range(len(self.options)):
                option_y = y + self.height + i * self.height
                if (x <= mouse_x <= x + self.width) and (option_y <= mouse_y <= option_y + self.height):
                    self.hovered_option = i
                    break
        
        return result
    
    def render(self, text_renderer):
        """Render the dropdown."""
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        
        # Draw main dropdown box
        color = self.hover_color if self.is_hovered else self.bg_color
        self._draw_box(text_renderer, x, y, self.width, self.height, color)
        
        # Draw selected text
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text_renderer.render_text(
                text_renderer.font,
                self.selected_text,
                int(x + 10),
                int(y + 5),
                scale=0.7,
                color=self.text_color
            )
            
            # Draw dropdown arrow
            arrow = "▼" if not self.is_open else "▲"
            text_renderer.render_text(
                text_renderer.font,
                arrow,
                int(x + self.width - 25),
                int(y + 5),
                scale=0.7,
                color=self.text_color
            )
        
        # Draw options if open
        if self.is_open:
            self._draw_options(text_renderer, x, y)
        
        # Render children
        super().render(text_renderer)
    
    def _draw_box(self, text_renderer, x, y, width, height, color):
        """Draw a box."""
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            # Draw border
            text_renderer.render_text(
                text_renderer.font,
                "[" + " " * int(width / 10) + "]",
                int(x),
                int(y + 5),
                scale=0.7,
                color=(0.5, 0.5, 0.5)
            )
    
    def _draw_options(self, text_renderer, x, y):
        """Draw dropdown options."""
        if not text_renderer or not hasattr(text_renderer, 'font') or not text_renderer.font:
            return
        
        for i, option in enumerate(self.options):
            option_y = y + self.height + i * self.height
            
            # Determine color
            if i == self.hovered_option:
                option_color = self.hover_color
            elif i == self._selected_index:
                option_color = (0.4, 0.6, 0.8)  # Highlight selected
            else:
                option_color = self.bg_color
            
            # Draw option background
            self._draw_box(text_renderer, x, option_y, self.width, self.height, option_color)
            
            # Draw option text
            text_renderer.render_text(
                text_renderer.font,
                option,
                int(x + 10),
                int(option_y + 5),
                scale=0.7,
                color=self.text_color
            )

