"""
UI Theme System
Collections of styles for consistent UI appearance.
Game developers can extend UITheme to create custom themes.
"""

from .ui_style import (
    ButtonStyle, SliderStyle, CheckboxStyle, PanelStyle,
    LabelStyle, DropdownStyle, Color, Colors
)


class UITheme:
    """
    Base UI theme class.
    Game developers extend this to create custom themes.
    """
    
    def __init__(self):
        """Initialize theme with default styles."""
        # Component styles
        self.button = ButtonStyle()
        self.slider = SliderStyle()
        self.checkbox = CheckboxStyle()
        self.panel = PanelStyle()
        self.label = LabelStyle()
        self.dropdown = DropdownStyle()
        
        # Global colors
        self.colors = {
            'primary': Colors.PRIMARY,
            'secondary': Colors.SECONDARY,
            'success': Colors.SUCCESS,
            'warning': Colors.WARNING,
            'danger': Colors.DANGER,
            'text': Colors.WHITE,
            'background': Colors.DARK_GRAY,
            'border': Colors.GRAY
        }


class DefaultTheme(UITheme):
    """Default clean, modern theme."""
    
    def __init__(self):
        """Initialize default theme."""
        super().__init__()
        
        # Modern button style
        self.button.bg_color = Color(0.25, 0.25, 0.25, 1.0)
        self.button.hover_color = Color(0.35, 0.35, 0.35, 1.0)
        self.button.press_color = Color(0.15, 0.15, 0.15, 1.0)
        self.button.border_radius = 6.0
        self.button.padding = 15.0
        
        # Modern slider style
        self.slider.track_color = Color(0.15, 0.15, 0.15, 1.0)
        self.slider.fill_color = Color(0.2, 0.5, 1.0, 1.0)
        self.slider.fill_hover_color = Color(0.3, 0.6, 1.0, 1.0)
        self.slider.handle_color = Color(0.9, 0.9, 0.9, 1.0)
        self.slider.handle_radius = 12.0
        self.slider.track_height = 8.0
        
        # Modern checkbox style
        self.checkbox.box_color = Color(0.2, 0.2, 0.2, 1.0)
        self.checkbox.check_color = Color(0.2, 0.8, 0.3, 1.0)
        self.checkbox.border_radius = 4.0


class DarkTheme(UITheme):
    """Dark theme example."""
    
    def __init__(self):
        """Initialize dark theme."""
        super().__init__()
        
        # Dark color scheme
        self.button.bg_color = Color(0.1, 0.1, 0.1, 1.0)
        self.button.hover_color = Color(0.2, 0.2, 0.2, 1.0)
        self.button.press_color = Color(0.05, 0.05, 0.05, 1.0)
        
        self.slider.track_color = Color(0.1, 0.1, 0.1, 1.0)
        self.slider.fill_color = Color(0.3, 0.3, 0.8, 1.0)
        self.slider.handle_color = Color(0.8, 0.8, 0.8, 1.0)
        
        self.panel.bg_color = Color(0.05, 0.05, 0.05, 0.95)


class LightTheme(UITheme):
    """Light theme example."""
    
    def __init__(self):
        """Initialize light theme."""
        super().__init__()
        
        # Light color scheme
        self.button.bg_color = Color(0.9, 0.9, 0.9, 1.0)
        self.button.hover_color = Color(0.95, 0.95, 0.95, 1.0)
        self.button.press_color = Color(0.8, 0.8, 0.8, 1.0)
        self.button.text_color = Colors.BLACK
        
        self.slider.track_color = Color(0.85, 0.85, 0.85, 1.0)
        self.slider.fill_color = Color(0.2, 0.4, 0.9, 1.0)
        
        self.panel.bg_color = Color(0.95, 0.95, 0.95, 0.98)
        self.panel.border_color = Color(0.6, 0.6, 0.6, 1.0)
        
        self.label.text_color = Colors.BLACK


# Example: Game-specific custom theme
class GameCustomTheme(UITheme):
    """
    Example custom theme for games.
    Game developers can create their own by extending UITheme.
    """
    
    def __init__(self):
        """Initialize custom theme."""
        super().__init__()
        
        # Custom colors - Blue and Gold theme
        self.button.bg_color = Color(0.1, 0.2, 0.5, 1.0)
        self.button.hover_color = Color(0.2, 0.3, 0.6, 1.0)
        self.button.press_color = Color(0.05, 0.1, 0.4, 1.0)
        
        self.slider.track_color = Color(0.15, 0.15, 0.2, 1.0)
        self.slider.fill_color = Color(0.8, 0.6, 0.0, 1.0)  # Gold
        self.slider.handle_color = Color(1.0, 0.9, 0.5, 1.0)  # Light gold
        
        self.checkbox.check_color = Color(1.0, 0.8, 0.0, 1.0)  # Gold checkmark
        
        self.panel.bg_color = Color(0.05, 0.05, 0.15, 0.95)
        self.panel.border_color = Color(0.3, 0.3, 0.5, 1.0)

