"""
UI Element Base Class
Base class for all UI elements (buttons, sliders, panels, etc.)
"""

from typing import Optional, Callable, Tuple
from enum import Enum


class Anchor(Enum):
    """Anchor points for UI elements."""
    TOP_LEFT = "top_left"
    TOP_CENTER = "top_center"
    TOP_RIGHT = "top_right"
    CENTER_LEFT = "center_left"
    CENTER = "center"
    CENTER_RIGHT = "center_right"
    BOTTOM_LEFT = "bottom_left"
    BOTTOM_CENTER = "bottom_center"
    BOTTOM_RIGHT = "bottom_right"


class UIElement:
    """
    Base class for all UI elements.
    Handles positioning, sizing, visibility, and basic events.
    """
    
    def __init__(
        self,
        x: float = 0.0,
        y: float = 0.0,
        width: float = 100.0,
        height: float = 50.0,
        anchor: Anchor = Anchor.TOP_LEFT,
        visible: bool = True,
        enabled: bool = True
    ):
        """
        Initialize UI element.
        
        Args:
            x: X position
            y: Y position
            width: Element width
            height: Element height
            anchor: Anchor point for positioning
            visible: Whether element is visible
            enabled: Whether element is enabled (can receive input)
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.anchor = anchor
        self.visible = visible
        self.enabled = enabled
        
        # State
        self.is_hovered = False
        self.is_pressed = False
        self.is_focused = False
        
        # Parent/children
        self.parent: Optional['UIElement'] = None
        self.children: list['UIElement'] = []
        
        # Callbacks
        self.on_click: Optional[Callable] = None
        self.on_hover_enter: Optional[Callable] = None
        self.on_hover_exit: Optional[Callable] = None
        self.on_focus_gain: Optional[Callable] = None
        self.on_focus_lose: Optional[Callable] = None
        
        # Padding
        self.padding_left = 0.0
        self.padding_right = 0.0
        self.padding_top = 0.0
        self.padding_bottom = 0.0
    
    def get_absolute_position(self) -> Tuple[float, float]:
        """
        Get absolute screen position accounting for parent and anchor.
        
        Returns:
            Tuple of (x, y) in screen coordinates
        """
        abs_x = self.x
        abs_y = self.y
        
        # Add parent offset
        if self.parent:
            parent_x, parent_y = self.parent.get_absolute_position()
            abs_x += parent_x + self.parent.padding_left
            abs_y += parent_y + self.parent.padding_top
        
        # Apply anchor offset
        # Note: Y is inverted in screen coordinates (0 = top)
        anchor_offset_x, anchor_offset_y = self._get_anchor_offset()
        abs_x += anchor_offset_x
        abs_y += anchor_offset_y
        
        return abs_x, abs_y
    
    def _get_anchor_offset(self) -> Tuple[float, float]:
        """Get offset based on anchor point."""
        # For now, anchors are relative to parent
        # In a real implementation, you'd anchor to screen edges
        return (0, 0)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """
        Get element bounds in screen coordinates.
        
        Returns:
            Tuple of (x, y, width, height)
        """
        x, y = self.get_absolute_position()
        return (x, y, self.width, self.height)
    
    def contains_point(self, mouse_x: float, mouse_y: float) -> bool:
        """
        Check if a point is inside this element.
        
        Args:
            mouse_x: Mouse X position
            mouse_y: Mouse Y position
            
        Returns:
            True if point is inside element bounds
        """
        x, y, w, h = self.get_bounds()
        return (x <= mouse_x <= x + w) and (y <= mouse_y <= y + h)
    
    def add_child(self, child: 'UIElement'):
        """Add a child element."""
        child.parent = self
        self.children.append(child)
    
    def remove_child(self, child: 'UIElement'):
        """Remove a child element."""
        if child in self.children:
            child.parent = None
            self.children.remove(child)
    
    def handle_mouse_move(self, mouse_x: float, mouse_y: float) -> bool:
        """
        Handle mouse movement.
        
        Args:
            mouse_x: Mouse X position
            mouse_y: Mouse Y position
            
        Returns:
            True if event was handled
        """
        if not self.visible or not self.enabled:
            return False
        
        # Check hover state
        was_hovered = self.is_hovered
        self.is_hovered = self.contains_point(mouse_x, mouse_y)
        
        # Trigger hover events
        if self.is_hovered and not was_hovered:
            if self.on_hover_enter:
                self.on_hover_enter()
        elif not self.is_hovered and was_hovered:
            if self.on_hover_exit:
                self.on_hover_exit()
        
        # Check children
        for child in self.children:
            if child.handle_mouse_move(mouse_x, mouse_y):
                return True
        
        return self.is_hovered
    
    def handle_mouse_click(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        """
        Handle mouse click.
        
        Args:
            mouse_x: Mouse X position
            mouse_y: Mouse Y position
            button: Mouse button (0=left, 1=right, 2=middle)
            
        Returns:
            True if event was handled
        """
        if not self.visible or not self.enabled:
            return False
        
        # Check children first (front to back)
        for child in reversed(self.children):
            if child.handle_mouse_click(mouse_x, mouse_y, button):
                return True
        
        # Check if clicked on this element
        if self.contains_point(mouse_x, mouse_y):
            self.is_pressed = True
            if self.on_click and button == 0:  # Left click
                self.on_click()
                return True  # Only return True if we have a click handler
            # If no click handler, we're just a container (like Panel)
            # Don't consume the event
        
        return False
    
    def handle_mouse_release(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        """
        Handle mouse release.
        
        Args:
            mouse_x: Mouse X position
            mouse_y: Mouse Y position
            button: Mouse button
            
        Returns:
            True if event was handled
        """
        if not self.visible:
            return False
        
        was_pressed = self.is_pressed
        self.is_pressed = False
        
        # Check children
        for child in reversed(self.children):
            if child.handle_mouse_release(mouse_x, mouse_y, button):
                return True
        
        return was_pressed
    
    def update(self, delta_time: float):
        """
        Update element logic.
        
        Args:
            delta_time: Time since last frame in seconds
        """
        # Update children
        for child in self.children:
            child.update(delta_time)
    
    def render(self, text_renderer):
        """
        Render the element.
        Must be overridden by subclasses.
        
        Args:
            text_renderer: TextRenderer instance for drawing
        """
        # Base class doesn't render anything
        # Subclasses override this method
        
        # Render children
        if self.visible:
            for child in self.children:
                child.render(text_renderer)
    
    def set_position(self, x: float, y: float):
        """Set element position."""
        self.x = x
        self.y = y
    
    def set_size(self, width: float, height: float):
        """Set element size."""
        self.width = width
        self.height = height
    
    def show(self):
        """Make element visible."""
        self.visible = True
    
    def hide(self):
        """Hide element."""
        self.visible = False
    
    def enable(self):
        """Enable element (can receive input)."""
        self.enabled = True
    
    def disable(self):
        """Disable element (cannot receive input)."""
        self.enabled = False

