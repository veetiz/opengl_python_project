"""
UI Dropdown Component
OpenGL-based dropdown with smooth graphics and customizable styling.
"""

from .ui_element import UIElement, Anchor
from .ui_style import DropdownStyle
from .ui_units import UISize
from typing import List, Optional, Callable, Union


class UIDropdown(UIElement):
    """UI dropdown selector with OpenGL rendering."""
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        width: Union[float, UISize] = 150.0,
        height: Union[float, UISize] = 35.0,
        options: List[str] = None,
        selected_index: int = 0,
        anchor: Anchor = Anchor.TOP_LEFT,
        on_select: Optional[Callable[[int, str], None]] = None,
        style: Optional[DropdownStyle] = None,
        **kwargs
    ):
        """
        Initialize modern dropdown with CSS-like sizing support.
        
        Args:
            x, y: Position (supports px, %, vw, vh, rem, em, calc)
            width, height: Size (supports all units)
            options: List of options
            selected_index: Initially selected index
            anchor: Anchor point
            on_select: Selection callback (receives index and text)
            style: Dropdown style (uses default if None)
            **kwargs: Additional CSS-like parameters
        """
        # Import here to avoid circular dependency
        from .ui_units import px
        from .ui_calc import UICalc
        
        # Convert to float for UIElement
        x_val = float(x) if isinstance(x, (int, float)) else 0.0
        y_val = float(y) if isinstance(y, (int, float)) else 0.0
        width_val = float(width) if isinstance(width, (int, float)) else 150.0
        height_val = float(height) if isinstance(height, (int, float)) else 35.0
        
        # Start at layer 200 (above normal elements)
        # Will move to layer 300 when open
        super().__init__(x_val, y_val, width_val, height_val, anchor, layer=200)
        
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
        
        # Change layer when opening/closing
        if self.is_open:
            self.layer = 300  # Move to overlay layer (on top of everything!)
        else:
            self.layer = 200  # Return to normal layer
    
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
            w = self.compiled_width if hasattr(self, 'compiled_width') else self.width
            h = self.compiled_height if hasattr(self, 'compiled_height') else self.height
            dropdown_y = y + h
            for i in range(len(self.options)):
                option_y = dropdown_y + i * self.style.item_height
                if (x <= mouse_x <= x + w and 
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
        
        # Use compiled sizes
        w = self.compiled_width if hasattr(self, 'compiled_width') else self.width
        h = self.compiled_height if hasattr(self, 'compiled_height') else self.height
        
        # Draw main button
        bg_color = self.style.hover_color if self.is_hovered else self.style.bg_color
        ui_renderer.draw_rect(
            x, y, w, h,
            bg_color.to_tuple()
        )
        
        # Draw border
        ui_renderer.draw_border_rect(
            x, y, w, h,
            self.style.border_width,
            self.style.border_color.to_tuple()
        )
        
        # Draw selected text
        if text_renderer and hasattr(text_renderer, 'font') and text_renderer.font:
            text = self.get_selected_text()
            text_x = x + self.style.padding
            text_y = y + h / 2 + 8
            
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
                int(x + w - 25),
                int(text_y),
                scale=0.8,
                color=self.style.text_color.to_rgb()
            )
        
        # Draw dropdown menu if open (layer system ensures it renders on top)
        if self.is_open:
            dropdown_y = y + h
            total_height = len(self.options) * self.style.item_height
            
            # Main dropdown background (solid, covers elements below due to layer!)
            ui_renderer.draw_rect(
                x, dropdown_y,
                w, total_height,
                (0.2, 0.2, 0.2, 1.0)  # Solid dark gray
            )
            
            # Dropdown border
            ui_renderer.draw_border_rect(
                x, dropdown_y,
                w, total_height,
                2.0,
                (0.6, 0.6, 0.6, 1.0)  # Gray border
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

