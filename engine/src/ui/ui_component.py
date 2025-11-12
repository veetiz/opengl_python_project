"""
UI Component Base Class
Base class for all UI components with CSS-like sizing support.
"""

from typing import Optional, Union, Tuple
from .ui_units import UISize, px
from .ui_element import Anchor


class UIComponent:
    """
    Base class for all UI components.
    Supports CSS-like sizing: px, %, vw, vh
    
    This is the new base class that replaces/wraps UIElement with sizing support.
    """
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        width: Union[float, UISize] = 100.0,
        height: Union[float, UISize] = 50.0,
        anchor: Anchor = Anchor.TOP_LEFT,
        visible: bool = True,
        enabled: bool = True,
        layer: int = 0
    ):
        """
        Initialize UI component.
        
        Args:
            x: X position (float=pixels, UISize=with units)
            y: Y position (float=pixels, UISize=with units)
            width: Width (float=pixels, UISize=with units)
            height: Height (float=pixels, UISize=with units)
            anchor: Anchor point
            visible: Visibility
            enabled: Interaction enabled
            layer: Render layer (z-index)
            
        Examples:
            # Absolute pixels
            UIComponent(x=100, y=50, width=200, height=40)
            
            # Percentage of parent
            UIComponent(x=percent(10), y=percent(20), width=percent(50), height=px(40))
            
            # Viewport units
            UIComponent(x=vw(10), y=vh(10), width=vw(80), height=vh(20))
            
            # Mixed
            UIComponent(x=px(100), y=percent(50), width=vw(30), height=px(40))
        """
        # Store original sizes (with units)
        self.x_size = x if isinstance(x, UISize) else px(x)
        self.y_size = y if isinstance(y, UISize) else px(y)
        self.width_size = width if isinstance(width, UISize) else px(width)
        self.height_size = height if isinstance(height, UISize) else px(height)
        
        # Compiled sizes (absolute pixels) - set by UICompiler
        self.compiled_x = float(x) if isinstance(x, (int, float)) else 0.0
        self.compiled_y = float(y) if isinstance(y, (int, float)) else 0.0
        self.compiled_width = float(width) if isinstance(width, (int, float)) else 100.0
        self.compiled_height = float(height) if isinstance(height, (int, float)) else 50.0
        
        # Properties
        self.anchor = anchor
        self.visible = visible
        self.enabled = enabled
        self.layer = layer
        
        # State
        self.is_hovered = False
        self.is_pressed = False
        self.is_focused = False
        
        # Hierarchy
        self.parent: Optional['UIComponent'] = None
        self.children: list['UIComponent'] = []
        
        # Padding (can also use units)
        self.padding_left = 0.0
        self.padding_right = 0.0
        self.padding_top = 0.0
        self.padding_bottom = 0.0
    
    # Properties for backward compatibility
    @property
    def x(self) -> float:
        """Get compiled X position."""
        return self.compiled_x
    
    @x.setter
    def x(self, value: Union[float, UISize]):
        """Set X position."""
        self.x_size = value if isinstance(value, UISize) else px(value)
        # Will be recompiled on next render
    
    @property
    def y(self) -> float:
        """Get compiled Y position."""
        return self.compiled_y
    
    @y.setter
    def y(self, value: Union[float, UISize]):
        """Set Y position."""
        self.y_size = value if isinstance(value, UISize) else px(value)
    
    @property
    def width(self) -> float:
        """Get compiled width."""
        return self.compiled_width
    
    @width.setter
    def width(self, value: Union[float, UISize]):
        """Set width."""
        self.width_size = value if isinstance(value, UISize) else px(value)
    
    @property
    def height(self) -> float:
        """Get compiled height."""
        return self.compiled_height
    
    @height.setter
    def height(self, value: Union[float, UISize]):
        """Set height."""
        self.height_size = value if isinstance(value, UISize) else px(value)
    
    def add_child(self, child: 'UIComponent'):
        """Add a child component."""
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'UIComponent'):
        """Remove a child component."""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def get_absolute_position(self) -> Tuple[float, float]:
        """
        Get absolute screen position (compiled).
        
        Returns:
            Tuple of (x, y) in pixels
        """
        abs_x = self.compiled_x
        abs_y = self.compiled_y
        
        # Add parent offset
        if self.parent:
            parent_x, parent_y = self.parent.get_absolute_position()
            abs_x += parent_x + self.parent.padding_left
            abs_y += parent_y + self.parent.padding_top
        
        return abs_x, abs_y
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get element bounds in screen coordinates.
        
        Returns:
            Tuple of (x, y, width, height) in pixels
        """
        x, y = self.get_absolute_position()
        return (x, y, self.compiled_width, self.compiled_height)
    
    def contains_point(self, mouse_x: float, mouse_y: float) -> bool:
        """
        Check if a point is inside this component.
        
        Args:
            mouse_x: Mouse X position
            mouse_y: Mouse Y position
            
        Returns:
            True if point is inside
        """
        x, y, w, h = self.get_bounds()
        return (x <= mouse_x <= x + w) and (y <= mouse_y <= y + h)

