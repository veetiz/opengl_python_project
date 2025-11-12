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


class UISize:
    """
    Represents a size value with units.
    Supports: px, %, vw, vh (CSS-like)
    """
    
    def __init__(self, value: float, unit: Union[str, UnitType] = UnitType.PIXELS):
        """
        Initialize UI size.
        
        Args:
            value: Numeric value
            unit: Unit type ("px", "%", "vw", "vh")
            
        Examples:
            UISize(100, "px")  # 100 pixels
            UISize(50, "%")    # 50% of parent
            UISize(80, "vw")   # 80% of viewport width
            UISize(100, "vh")  # 100% of viewport height
        """
        self.value = value
        
        if isinstance(unit, str):
            unit_map = {
                "px": UnitType.PIXELS,
                "%": UnitType.PERCENT,
                "vw": UnitType.VIEWPORT_WIDTH,
                "vh": UnitType.VIEWPORT_HEIGHT
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

