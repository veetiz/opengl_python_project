"""
UI Calc
CSS-like calc() function for arithmetic with different units.
"""

from typing import Union
from .ui_units import UISize


class UICalc:
    """
    Represents a calculated size (CSS calc()).
    Stores an operation between two values.
    
    Examples:
        calc(vw(100), px(-40))  # 100vw - 40px
        calc(percent(50), px(20), '+')  # 50% + 20px
        calc(vw(50), px(-100))  # Center with offset
    """
    
    def __init__(
        self,
        left: Union[float, UISize, 'UICalc'],
        right: Union[float, UISize, 'UICalc'],
        operator: str = '+'
    ):
        """
        Initialize UI calculation.
        
        Args:
            left: Left operand (number, UISize, or another UICalc)
            right: Right operand (number, UISize, or another UICalc)
            operator: Operation ('+', '-', '*', '/')
        """
        self.left = left
        self.right = right
        self.operator = operator
        
        # Validate operator
        if operator not in ['+', '-', '*', '/']:
            raise ValueError(f"Invalid operator '{operator}'. Must be '+', '-', '*', or '/'")
    
    def __repr__(self):
        return f"UICalc({self.left} {self.operator} {self.right})"


# Main calc() function
def calc(
    left: Union[float, UISize, UICalc],
    right: Union[float, UISize, UICalc],
    operator: str = '+'
) -> UICalc:
    """
    Create a calculated size (CSS-like calc()).
    
    Args:
        left: Left operand
        right: Right operand
        operator: Operation ('+', '-', '*', '/')
        
    Returns:
        UICalc instance
        
    Examples:
        # Full width minus padding
        calc(vw(100), px(-40))
        
        # 50% plus offset
        calc(percent(50), px(20), '+')
        
        # Center element
        calc(vw(50), px(-100))  # 50vw - 100px (center 200px element)
        
        # Nested calc
        calc(calc(vw(100), px(-40)), px(-20))  # ((100vw - 40px) - 20px)
    """
    return UICalc(left, right, operator)


# Helper functions for common operations
def add(
    left: Union[float, UISize, UICalc],
    right: Union[float, UISize, UICalc]
) -> UICalc:
    """Add two values: left + right"""
    return UICalc(left, right, '+')


def sub(
    left: Union[float, UISize, UICalc],
    right: Union[float, UISize, UICalc]
) -> UICalc:
    """Subtract two values: left - right"""
    return UICalc(left, right, '-')


def mul(
    left: Union[float, UISize, UICalc],
    right: Union[float, UISize, UICalc]
) -> UICalc:
    """Multiply two values: left * right"""
    return UICalc(left, right, '*')


def div(
    left: Union[float, UISize, UICalc],
    right: Union[float, UISize, UICalc]
) -> UICalc:
    """Divide two values: left / right"""
    return UICalc(left, right, '/')

