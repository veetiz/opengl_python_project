"""
Input Module
Handles keyboard and mouse input management.
"""

import glfw
from typing import Optional


class Keyboard:
    """Manages keyboard input state."""
    
    def __init__(self, window):
        """
        Initialize keyboard input handler.
        
        Args:
            window: GLFW window handle
        """
        self.window = window
    
    def is_key_pressed(self, key: int) -> bool:
        """
        Check if a key is currently pressed.
        
        Args:
            key: GLFW key constant (e.g., glfw.KEY_W)
            
        Returns:
            True if key is pressed, False otherwise
        """
        return glfw.get_key(self.window, key) == glfw.PRESS
    
    def is_key_released(self, key: int) -> bool:
        """Check if a key is currently released."""
        return glfw.get_key(self.window, key) == glfw.RELEASE


class Mouse:
    """Manages mouse input state and movement."""
    
    def __init__(self, window, sensitivity: float = 0.1):
        """
        Initialize mouse input handler.
        
        Args:
            window: GLFW window handle
            sensitivity: Mouse sensitivity multiplier
        """
        self.window = window
        self.sensitivity = sensitivity
        
        # Mouse state
        self.first_mouse = True
        self.last_x = 0.0
        self.last_y = 0.0
        self.offset_x = 0.0
        self.offset_y = 0.0
        
        # Capture state
        self.captured = False
    
    def capture(self, enable: bool = True):
        """
        Capture or release the mouse cursor.
        
        Args:
            enable: True to capture and hide cursor, False to release
        """
        self.captured = enable
        if enable:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
            self.first_mouse = True  # Reset on capture to avoid jump
        else:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
    
    def update_position(self, xpos: float, ypos: float):
        """
        Update mouse position and calculate offset.
        
        Args:
            xpos: Current mouse X position
            ypos: Current mouse Y position
        """
        if self.first_mouse:
            self.last_x = xpos
            self.last_y = ypos
            self.first_mouse = False
            self.offset_x = 0.0
            self.offset_y = 0.0
            return
        
        self.offset_x = (xpos - self.last_x) * self.sensitivity
        self.offset_y = (self.last_y - ypos) * self.sensitivity  # Reversed: y goes from bottom to top
        
        self.last_x = xpos
        self.last_y = ypos
    
    def get_offset(self) -> tuple[float, float]:
        """
        Get mouse movement offset since last frame.
        
        Returns:
            Tuple of (x_offset, y_offset)
        """
        return (self.offset_x, self.offset_y)
    
    def reset_offset(self):
        """Reset the movement offset."""
        self.offset_x = 0.0
        self.offset_y = 0.0


class Input:
    """Combined input manager for keyboard and mouse."""
    
    def __init__(self, window):
        """
        Initialize input manager.
        
        Args:
            window: GLFW window handle
        """
        self.keyboard = Keyboard(window)
        self.mouse = Mouse(window)
        self.scroll_offset = 0.0
    
    def update_mouse_position(self, xpos: float, ypos: float):
        """Update mouse position."""
        self.mouse.update_position(xpos, ypos)
    
    def update_scroll(self, xoffset: float, yoffset: float):
        """Update scroll offset."""
        self.scroll_offset = yoffset
    
    def reset_per_frame(self):
        """Reset per-frame input state (call at start of each frame)."""
        self.scroll_offset = 0.0
        # Don't reset mouse offset here - it's managed by the mouse movement callback

