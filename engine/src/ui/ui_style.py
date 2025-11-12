"""
UI Style System
Defines visual appearance and theming for UI components.
"""

from typing import Tuple


class Color:
    """RGBA color representation."""
    
    def __init__(self, r: float, g: float, b: float, a: float = 1.0):
        """
        Initialize color.
        
        Args:
            r, g, b, a: Color components (0.0-1.0)
        """
        self.r = r
        self.g = g
        self.b = b
        self.a = a
    
    def to_tuple(self) -> Tuple[float, float, float, float]:
        """Get color as RGBA tuple."""
        return (self.r, self.g, self.b, self.a)
    
    def to_rgb(self) -> Tuple[float, float, float]:
        """Get color as RGB tuple (no alpha)."""
        return (self.r, self.g, self.b)


# Predefined colors
class Colors:
    """Common color definitions."""
    
    WHITE = Color(1.0, 1.0, 1.0, 1.0)
    BLACK = Color(0.0, 0.0, 0.0, 1.0)
    GRAY = Color(0.5, 0.5, 0.5, 1.0)
    DARK_GRAY = Color(0.2, 0.2, 0.2, 1.0)
    LIGHT_GRAY = Color(0.8, 0.8, 0.8, 1.0)
    
    # Primary colors
    RED = Color(1.0, 0.0, 0.0, 1.0)
    GREEN = Color(0.0, 1.0, 0.0, 1.0)
    BLUE = Color(0.0, 0.5, 1.0, 1.0)
    YELLOW = Color(1.0, 1.0, 0.0, 1.0)
    
    # UI colors
    PRIMARY = Color(0.2, 0.4, 0.8, 1.0)
    SECONDARY = Color(0.3, 0.3, 0.3, 1.0)
    SUCCESS = Color(0.0, 0.7, 0.3, 1.0)
    WARNING = Color(1.0, 0.7, 0.0, 1.0)
    DANGER = Color(0.9, 0.2, 0.2, 1.0)
    
    # Transparent
    TRANSPARENT = Color(0.0, 0.0, 0.0, 0.0)


class UIStyle:
    """Base style class."""
    
    def __init__(self):
        """Initialize base style."""
        self.padding = 10.0
        self.margin = 5.0
        self.border_width = 2.0
        self.border_radius = 0.0  # No rounding by default


class ButtonStyle(UIStyle):
    """Style for buttons."""
    
    def __init__(self):
        """Initialize button style."""
        super().__init__()
        
        # Colors
        self.bg_color = Color(0.3, 0.3, 0.3, 1.0)
        self.hover_color = Color(0.4, 0.4, 0.4, 1.0)
        self.press_color = Color(0.2, 0.2, 0.2, 1.0)
        self.text_color = Colors.WHITE
        self.border_color = Color(0.5, 0.5, 0.5, 1.0)
        
        # Sizes
        self.padding = 15.0
        self.border_width = 2.0
        self.border_radius = 5.0
        self.text_size = 1.0


class SliderStyle(UIStyle):
    """Style for sliders."""
    
    def __init__(self):
        """Initialize slider style."""
        super().__init__()
        
        # Track colors (empty/inactive part) - VERY BRIGHT for visibility
        self.track_color = Color(0.5, 0.5, 0.5, 1.0)  # Medium gray for empty part
        self.track_border_color = Color(0.7, 0.7, 0.7, 1.0)
        
        # Fill colors (active/filled part) - VERY BRIGHT for visibility
        self.fill_color = Color(0.4, 1.0, 0.5, 1.0)  # Very bright green for filled part (customizable!)
        self.fill_hover_color = Color(0.5, 1.0, 0.6, 1.0)
        
        # Handle colors
        self.handle_color = Color(0.9, 0.9, 0.9, 1.0)
        self.handle_hover_color = Colors.WHITE
        self.handle_press_color = Color(0.7, 0.7, 0.7, 1.0)
        
        # Sizes
        self.track_height = 12.0  # Taller for better visibility of colors
        self.handle_radius = 14.0  # Larger handle for easier dragging
        self.border_width = 2.0  # Thicker border for visibility
        
        # Label spacing
        self.label_spacing = 10.0  # Space between label and slider


class CheckboxStyle(UIStyle):
    """Style for checkboxes."""
    
    def __init__(self):
        """Initialize checkbox style."""
        super().__init__()
        
        # Box colors
        self.box_color = Color(0.2, 0.2, 0.2, 1.0)
        self.box_hover_color = Color(0.3, 0.3, 0.3, 1.0)
        self.box_border_color = Color(0.5, 0.5, 0.5, 1.0)
        
        # Check colors
        self.check_color = Color(0.2, 0.7, 0.3, 1.0)
        self.check_hover_color = Color(0.3, 0.8, 0.4, 1.0)
        
        # Text
        self.text_color = Colors.WHITE
        
        # Sizes
        self.box_size = 20.0
        self.border_width = 2.0
        self.border_radius = 3.0
        self.check_padding = 4.0
        self.text_size = 1.0


class PanelStyle(UIStyle):
    """Style for panels."""
    
    def __init__(self):
        """Initialize panel style."""
        super().__init__()
        
        # Colors
        self.bg_color = Color(0.1, 0.1, 0.1, 0.9)
        self.border_color = Color(0.4, 0.4, 0.4, 1.0)
        
        # Sizes
        self.padding = 20.0
        self.border_width = 2.0
        self.border_radius = 10.0


class LabelStyle(UIStyle):
    """Style for labels."""
    
    def __init__(self):
        """Initialize label style."""
        super().__init__()
        
        # Colors
        self.text_color = Colors.WHITE
        self.bg_color = Colors.TRANSPARENT
        
        # Sizes
        self.text_size = 1.0
        self.padding = 0.0


class DropdownStyle(UIStyle):
    """Style for dropdowns."""
    
    def __init__(self):
        """Initialize dropdown style."""
        super().__init__()
        
        # Colors
        self.bg_color = Color(0.3, 0.3, 0.3, 1.0)
        self.hover_color = Color(0.4, 0.4, 0.4, 1.0)
        self.selected_color = Color(0.2, 0.4, 0.8, 1.0)
        self.text_color = Colors.WHITE
        self.border_color = Color(0.5, 0.5, 0.5, 1.0)
        
        # Sizes
        self.padding = 10.0
        self.border_width = 2.0
        self.border_radius = 3.0
        self.item_height = 30.0
        self.text_size = 1.0

