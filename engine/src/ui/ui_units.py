"""
UI Units System
CSS-like units for UI sizing (px, %, vw, vh).
"""

from typing import Union, Tuple
from enum import Enum


class UnitType(Enum):
    """Unit types for UI sizing."""
    PIXELS = "px"           # Absolute pixels
    PERCENT = "%"           # Percentage of parent
    VIEWPORT_WIDTH = "vw"   # Percentage of viewport width
    VIEWPORT_HEIGHT = "vh"  # Percentage of viewport height
    REM = "rem"             # Relative to root font size
    EM = "em"               # Relative to parent font size


class UISize:
    """
    Represents a size value with units.
    Supports: px, %, vw, vh, rem, em (CSS-like)
    """
    
    def __init__(self, value: float, unit: Union[str, UnitType] = UnitType.PIXELS):
        """
        Initialize UI size.
        
        Args:
            value: Numeric value
            unit: Unit type ("px", "%", "vw", "vh", "rem", "em")
            
        Examples:
            UISize(100, "px")   # 100 pixels
            UISize(50, "%")     # 50% of parent
            UISize(80, "vw")    # 80% of viewport width
            UISize(100, "vh")   # 100% of viewport height
            UISize(2, "rem")    # 2x root font size
            UISize(1.5, "em")   # 1.5x parent font size
        """
        self.value = value
        
        if isinstance(unit, str):
            unit_map = {
                "px": UnitType.PIXELS,
                "%": UnitType.PERCENT,
                "vw": UnitType.VIEWPORT_WIDTH,
                "vh": UnitType.VIEWPORT_HEIGHT,
                "rem": UnitType.REM,
                "em": UnitType.EM
            }
            self.unit = unit_map.get(unit, UnitType.PIXELS)
        else:
            self.unit = unit
    
    def is_pixels(self) -> bool:
        """Check if this is a pixel value."""
        return self.unit == UnitType.PIXELS
    
    def is_percent(self) -> bool:
        """Check if this is a percentage value."""
        return self.unit == UnitType.PERCENT
    
    def is_viewport_width(self) -> bool:
        """Check if this is a viewport width value."""
        return self.unit == UnitType.VIEWPORT_WIDTH
    
    def is_viewport_height(self) -> bool:
        """Check if this is a viewport height value."""
        return self.unit == UnitType.VIEWPORT_HEIGHT
    
    def is_rem(self) -> bool:
        """Check if this is a rem value (root em)."""
        return self.unit == UnitType.REM
    
    def is_em(self) -> bool:
        """Check if this is an em value (relative to parent font)."""
        return self.unit == UnitType.EM
    
    def __repr__(self):
        return f"UISize({self.value}{self.unit.value})"


# Helper functions for creating sizes
def px(value: float) -> UISize:
    """Create pixel size."""
    return UISize(value, UnitType.PIXELS)

def percent(value: float) -> UISize:
    """Create percentage size."""
    return UISize(value, UnitType.PERCENT)

def vw(value: float) -> UISize:
    """Create viewport width size."""
    return UISize(value, UnitType.VIEWPORT_WIDTH)

def vh(value: float) -> UISize:
    """Create viewport height size."""
    return UISize(value, UnitType.VIEWPORT_HEIGHT)

def rem(value: float) -> UISize:
    """Create rem size (relative to root font size)."""
    return UISize(value, UnitType.REM)

def em(value: float) -> UISize:
    """Create em size (relative to parent font size)."""
    return UISize(value, UnitType.EM)

