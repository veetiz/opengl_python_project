"""
UI Compiler
Compiles UI sizes from CSS-like units (%, vw, vh) to absolute pixels.
"""

from typing import Optional, Union, TYPE_CHECKING
from .ui_units import UISize, UnitType

if TYPE_CHECKING:
    from .ui_component import UIComponent


class UICompiler:
    """
    Compiles UI component sizes from units to absolute pixels.
    Handles: %, vw, vh → px
    """
    
    def __init__(self, viewport_width: int, viewport_height: int):
        """
        Initialize UI compiler.
        
        Args:
            viewport_width: Viewport width in pixels (window width)
            viewport_height: Viewport height in pixels (window height)
        """
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
    
    def set_viewport(self, width: int, height: int):
        """
        Update viewport dimensions.
        
        Args:
            width: New viewport width
            height: New viewport height
        """
        self.viewport_width = width
        self.viewport_height = height
    
    def compile_size(
        self, 
        size: Union[float, UISize], 
        parent_size: Optional[float] = None,
        is_width: bool = True
    ) -> float:
        """
        Compile a size value to absolute pixels.
        
        Args:
            size: Size value (float = pixels, UISize = with units)
            parent_size: Parent's size in pixels (for % units)
            is_width: True if width, False if height (for vw/vh)
            
        Returns:
            Absolute size in pixels
            
        Examples:
            compile_size(100)                  # 100px
            compile_size(UISize(50, "%"), 200) # 100px (50% of 200)
            compile_size(UISize(80, "vw"))     # 80% of viewport width
            compile_size(UISize(100, "vh"))    # 100% of viewport height
        """
        # If it's just a number, treat as pixels
        if isinstance(size, (int, float)):
            return float(size)
        
        # If it's a UISize, compile based on unit
        if isinstance(size, UISize):
            if size.is_pixels():
                return size.value
            
            elif size.is_percent():
                if parent_size is None:
                    # No parent, use viewport
                    base = self.viewport_width if is_width else self.viewport_height
                else:
                    base = parent_size
                return (size.value / 100.0) * base
            
            elif size.is_viewport_width():
                return (size.value / 100.0) * self.viewport_width
            
            elif size.is_viewport_height():
                return (size.value / 100.0) * self.viewport_height
        
        # Fallback
        return 0.0
    
    def compile_component(self, component: 'UIComponent'):
        """
        Compile all sizes for a component and its children.
        
        Args:
            component: UIComponent to compile
        """
        # Get parent's compiled size (if available)
        parent_width = None
        parent_height = None
        
        if component.parent:
            parent_width = component.parent.compiled_width
            parent_height = component.parent.compiled_height
        
        # Compile this component's sizes
        component.compiled_x = self.compile_size(
            component.x_size if hasattr(component, 'x_size') else component.x,
            parent_width,
            is_width=True
        )
        
        component.compiled_y = self.compile_size(
            component.y_size if hasattr(component, 'y_size') else component.y,
            parent_height,
            is_width=False
        )
        
        component.compiled_width = self.compile_size(
            component.width_size if hasattr(component, 'width_size') else component.width,
            parent_width,
            is_width=True
        )
        
        component.compiled_height = self.compile_size(
            component.height_size if hasattr(component, 'height_size') else component.height,
            parent_height,
            is_width=False
        )
        
        # Compile children recursively
        if hasattr(component, 'children'):
            for child in component.children:
                self.compile_component(child)

