"""
Modern Dropdown Component
OpenGL-based dropdown with smooth graphics and customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import DropdownStyle
from typing import List, Optional, Callable


class ModernDropdown(UIElement):
    """Modern dropdown selector with OpenGL rendering."""
    
    def __init__(
        self,
        x: float,
        y: float,
        width: float,
        height: float = 35.0,
        options: List[str] = None,
        selected_index: int = 0,
        anchor: Anchor = Anchor.TOP_LEFT,
        on_select: Optional[Callable[[int, str], None]] = None,
        style: Optional[DropdownStyle] = None
    ):
        """
        Initialize modern dropdown.
        
        Args:
            x, y: Position
            width, height: Size
            options: List of options
            selected_index: Initially selected index
            anchor: Anchor point
            on_select: Selection callback (receives index and text)
            style: Dropdown style (uses default if None)
        """
        super().__init__(x, y, width, height, anchor)
        
        self.options = options or ["Option 1", "Option 2"]
        self.selected_index = max(0, min(len(self.options) - 1, selected_index))
        self.on_select = on_select
        self.style = style or DropdownStyle()
        
        # State
        self.is_open = False
        self.hovered_option = -1
        
        # Override click handler
        self.on_click = self._handle_toggle
    
    def get_selected_text(self) -> str:
        """Get currently selected option text."""
        if 0 <= self.selected_index < len(self.options):
            return self.options[self.selected_index]
        return ""
    
    def _handle_toggle(self):
        """Toggle dropdown open/closed."""
        self.is_open = not self.is_open
    
    def select(self, index: int):
        """
        Select an option by index.
        
        Args:
            index: Option index
        """
        if 0 <= index < len(self.options):
            old_index = self.selected_index
            self.selected_index = index
            
            if old_index != index and self.on_select:
                self.on_select(index, self.options[index])
    
    def handle_mouse_move(self, mouse_x: float, mouse_y: float) -> bool:
        """Handle mouse movement."""
        result = super().handle_mouse_move(mouse_x, mouse_y)
        
        if self.is_open:
            # Check which option is hovered
            x, y = self.get_absolute_position()
            dropdown_y = y + self.height
            
            self.hovered_option = -1
            for i in range(len(self.options)):
                option_y = dropdown_y + i * self.style.item_height
                if (x <= mouse_x <= x + self.width and 
                    option_y <= mouse_y <= option_y + self.style.item_height):
                    self.hovered_option = i
                    return True
        
        return result
    
    def handle_mouse_click(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        """Handle mouse click."""
        if not self.visible or not self.enabled:
            return False
        
        x, y = self.get_absolute_position()
        
        # Check if clicked on main dropdown button
        if self.contains_point(mouse_x, mouse_y):
            self._handle_toggle()
            return True
        
        # Check if clicked on an option (when open)
        if self.is_open:
            dropdown_y = y + self.height
            for i in range(len(self.options)):
                option_y = dropdown_y + i * self.style.item_height
                if (x <= mouse_x <= x + self.width and 
                    option_y <= mouse_y <= option_y + self.style.item_height):
                    self.select(i)
                    self.is_open = False
                    return True
        
        # Click outside closes dropdown
        if self.is_open:
            self.is_open = False
        
        return False
    
    def render(self, ui_renderer, text_renderer):
        """
        Render the dropdown using OpenGL.
        
        Args:
            ui_renderer: ModernUIRenderer instance
            text_renderer: TextRenderer for text
        """
        if not self.visible:
            return
        
        x, y = self.get_absolute_position()
        
        # Draw main button
        bg_color = self.style.hover_color if self.is_hovered else self.style.bg_color
        ui_renderer.draw_rect(
            x, y, self.width, self.height,
            bg_color.to_tuple()
        )
        
        # Draw border
        ui_renderer.draw_border_rect(
            x, y, self.width, self.height,
            self.style.border_width,
            self.style.border_color.to_tuple()
        )
        
        # Draw selected text
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text = self.get_selected_text()
            text_x = x + self.style.padding
            text_y = y + self.height / 2 + 8
            
            text_renderer.render_text(
                text_renderer.font,
                text,
                int(text_x),
                int(text_y),
                scale=self.style.text_size,
                color=self.style.text_color.to_rgb()
            )
            
            # Draw arrow indicator
            arrow = "▼" if self.is_open else "▶"
            text_renderer.render_text(
                text_renderer.font,
                "v" if self.is_open else ">",  # ASCII fallback
                int(x + self.width - 25),
                int(text_y),
                scale=0.8,
                color=self.style.text_color.to_rgb()
            )
        
        # Draw dropdown menu if open (render on top with solid background)
        if self.is_open:
            dropdown_y = y + self.height
            
            # Draw full dropdown background first (covers elements below)
            total_height = len(self.options) * self.style.item_height
            ui_renderer.draw_rect(
                x, dropdown_y,
                self.width, total_height,
                (0.15, 0.15, 0.15, 1.0)  # Solid dark background
            )
            
            # Draw dropdown border
            ui_renderer.draw_border_rect(
                x, dropdown_y,
                self.width, total_height,
                2.0,
                self.style.border_color.to_tuple()
            )
            
            # Draw each option
            for i, option in enumerate(self.options):
                option_y = dropdown_y + i * self.style.item_height
                
                # Determine color for highlight
                if i == self.selected_index:
                    # Draw selection highlight
                    ui_renderer.draw_rect(
                        x + 2, option_y + 1,
                        self.width - 4, self.style.item_height - 2,
                        self.style.selected_color.to_tuple()
                    )
                elif i == self.hovered_option:
                    # Draw hover highlight
                    ui_renderer.draw_rect(
                        x + 2, option_y + 1,
                        self.width - 4, self.style.item_height - 2,
                        self.style.hover_color.to_tuple()
                    )
                
                # Draw option text
                if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
                    opt_text_x = x + self.style.padding
                    opt_text_y = option_y + self.style.item_height / 2 + 8
                    
                    text_renderer.render_text(
                        text_renderer.font,
                        option,
                        int(opt_text_x),
                        int(opt_text_y),
                        scale=self.style.text_size,
                        color=self.style.text_color.to_rgb()
                    )
        
        # Render children (pass both renderers!)
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

