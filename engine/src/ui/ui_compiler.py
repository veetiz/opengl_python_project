"""
UI Compiler
Compiles UI sizes from CSS-like units (%, vw, vh) to absolute pixels.
"""

from typing import Optional, Union, TYPE_CHECKING
from .ui_units import UISize, UnitType
from .ui_calc import UICalc

if TYPE_CHECKING:
    from .ui_component import UIComponent


class UICompiler:
    """
    Compiles UI component sizes from units to absolute pixels.
    Handles: %, vw, vh → px
    """
    
    def __init__(self, viewport_width: int, viewport_height: int, root_font_size: float = 16.0):
        """
        Initialize UI compiler.
        
        Args:
            viewport_width: Viewport width in pixels (window width)
            viewport_height: Viewport height in pixels (window height)
            root_font_size: Root font size in pixels (default: 16px, standard)
        """
        self.viewport_width = viewport_width
        self.viewport_height = viewport_height
        self.root_font_size = root_font_size
    
    def set_viewport(self, width: int, height: int):
        """
        Update viewport dimensions.
        
        Args:
            width: New viewport width
            height: New viewport height
        """
        self.viewport_width = width
        self.viewport_height = height
    
    def set_root_font_size(self, size: float):
        """
        Update root font size for rem calculations.
        
        Args:
            size: Root font size in pixels
        """
        self.root_font_size = size
    
    def compile_size(
        self, 
        size: Union[float, UISize, UICalc], 
        parent_size: Optional[float] = None,
        is_width: bool = True,
        parent_font_size: Optional[float] = None
    ) -> float:
        """
        Compile a size value to absolute pixels.
        
        Args:
            size: Size value (float = pixels, UISize = with units, UICalc = calculation)
            parent_size: Parent's size in pixels (for % units)
            is_width: True if width, False if height (for vw/vh)
            parent_font_size: Parent's font size in pixels (for em units)
            
        Returns:
            Absolute size in pixels
            
        Examples:
            compile_size(100)                  # 100px
            compile_size(UISize(50, "%"), 200) # 100px (50% of 200)
            compile_size(UISize(80, "vw"))     # 80% of viewport width
            compile_size(UISize(100, "vh"))    # 100% of viewport height
            compile_size(calc(vw(100), px(-40)))  # 100vw - 40px
            compile_size(rem(2))               # 2 * root_font_size
            compile_size(em(1.5), parent_font_size=20)  # 1.5 * 20 = 30px
        """
        # If it's just a number, treat as pixels
        if isinstance(size, (int, float)):
            return float(size)
        
        # If it's a UICalc, compile it
        if isinstance(size, UICalc):
            return self.compile_calc(size, parent_size, is_width, parent_font_size)
        
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
            
            elif size.is_rem():
                # Relative to root font size
                return size.value * self.root_font_size
            
            elif size.is_em():
                # Relative to parent font size
                if parent_font_size is None:
                    # No parent font, use root font size
                    return size.value * self.root_font_size
                else:
                    # Use parent's font size
                    return size.value * parent_font_size
        
        # Fallback
        return 0.0
    
    def compile_calc(
        self,
        calc: UICalc,
        parent_size: Optional[float] = None,
        is_width: bool = True,
        parent_font_size: Optional[float] = None
    ) -> float:
        """
        Compile a UICalc to absolute pixels.
        
        Args:
            calc: UICalc instance
            parent_size: Parent's size in pixels
            is_width: True if width, False if height
            parent_font_size: Parent's font size in pixels
            
        Returns:
            Calculated size in pixels
            
        Examples:
            calc(vw(100), px(-40))     # Full width minus 40px
            calc(percent(50), px(20))  # 50% plus 20px
            calc(vw(50), px(-100))     # Center with offset
        """
        # Compile left operand
        left_value = self.compile_size(calc.left, parent_size, is_width, parent_font_size)
        
        # Compile right operand
        right_value = self.compile_size(calc.right, parent_size, is_width, parent_font_size)
        
        # Perform operation
        if calc.operator == '+':
            return left_value + right_value
        elif calc.operator == '-':
            return left_value - right_value
        elif calc.operator == '*':
            return left_value * right_value
        elif calc.operator == '/':
            if right_value == 0:
                print(f"[UICompiler] Warning: Division by zero in calc(), returning 0")
                return 0.0
            return left_value / right_value
        else:
            print(f"[UICompiler] Warning: Unknown operator '{calc.operator}', returning 0")
            return 0.0
    
    def compile_component(self, component: 'UIComponent'):
        """
        Compile all sizes for a component and its children.
        Handles min/max constraints, aspect ratios, and font sizes (rem/em).
        
        Args:
            component: UIComponent to compile
        """
        # Get parent's compiled size (if available)
        parent_width = None
        parent_height = None
        parent_font_size = None
        
        if component.parent:
            parent_width = component.parent.compiled_width
            parent_height = component.parent.compiled_height
            parent_font_size = component.parent.compiled_font_size
        
        # Compile font size FIRST (needed for em calculations)
        if hasattr(component, 'font_size_value'):
            component.compiled_font_size = self.compile_size(
                component.font_size_value,
                parent_font_size,  # For em: relative to parent font
                is_width=True,  # Not used for font, but required
                parent_font_size=parent_font_size  # Pass explicitly
            )
        elif not hasattr(component, 'compiled_font_size'):
            # Inherit parent font size or use root
            component.compiled_font_size = parent_font_size if parent_font_size else self.root_font_size
        
        # Compile position
        component.compiled_x = self.compile_size(
            component.x_size if hasattr(component, 'x_size') else component.x,
            parent_width,
            is_width=True,
            parent_font_size=parent_font_size
        )
        
        component.compiled_y = self.compile_size(
            component.y_size if hasattr(component, 'y_size') else component.y,
            parent_height,
            is_width=False,
            parent_font_size=parent_font_size
        )
        
        # Compile base sizes
        component.compiled_width = self.compile_size(
            component.width_size if hasattr(component, 'width_size') else component.width,
            parent_width,
            is_width=True,
            parent_font_size=parent_font_size
        )
        
        component.compiled_height = self.compile_size(
            component.height_size if hasattr(component, 'height_size') else component.height,
            parent_height,
            is_width=False,
            parent_font_size=parent_font_size
        )
        
        # Compile min/max constraints (if present)
        if hasattr(component, 'min_width_size') and component.min_width_size is not None:
            component.compiled_min_width = self.compile_size(
                component.min_width_size, parent_width, is_width=True, parent_font_size=parent_font_size
            )
        
        if hasattr(component, 'max_width_size') and component.max_width_size is not None:
            component.compiled_max_width = self.compile_size(
                component.max_width_size, parent_width, is_width=True, parent_font_size=parent_font_size
            )
        
        if hasattr(component, 'min_height_size') and component.min_height_size is not None:
            component.compiled_min_height = self.compile_size(
                component.min_height_size, parent_height, is_width=False, parent_font_size=parent_font_size
            )
        
        if hasattr(component, 'max_height_size') and component.max_height_size is not None:
            component.compiled_max_height = self.compile_size(
                component.max_height_size, parent_height, is_width=False, parent_font_size=parent_font_size
            )
        
        # Apply aspect ratio (if present)
        if hasattr(component, 'aspect_ratio') and component.aspect_ratio is not None:
            if component.aspect_ratio > 0:
                # Width drives height (default behavior)
                component.compiled_height = component.compiled_width / component.aspect_ratio
        
        # Apply min/max clamping
        if hasattr(component, 'compiled_min_width') and component.compiled_min_width is not None:
            component.compiled_width = max(component.compiled_width, component.compiled_min_width)
        
        if hasattr(component, 'compiled_max_width') and component.compiled_max_width is not None:
            component.compiled_width = min(component.compiled_width, component.compiled_max_width)
        
        if hasattr(component, 'compiled_min_height') and component.compiled_min_height is not None:
            component.compiled_height = max(component.compiled_height, component.compiled_min_height)
        
        if hasattr(component, 'compiled_max_height') and component.compiled_max_height is not None:
            component.compiled_height = min(component.compiled_height, component.compiled_max_height)
        
        # Compile children recursively
        if hasattr(component, 'children'):
            for child in component.children:
                self.compile_component(child)

