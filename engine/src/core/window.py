"""
Window Management Module
Handles GLFW window creation and event handling.
"""

import glfw
from typing import Optional, Callable


class Window:
    """Manages GLFW window creation and event handling."""
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "Vulkan Window"):
        """
        Initialize the Window.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            title: Window title
        """
        self.width = width
        self.height = height
        self.title = title
        self.window = None
        self._resize_callback: Optional[Callable] = None
        self._mouse_callback: Optional[Callable] = None
        self._scroll_callback: Optional[Callable] = None
        self._mouse_button_callback: Optional[Callable] = None
        self.mouse_captured = False
        
    def init(self) -> bool:
        """
        Initialize GLFW and create the window.
        
        Returns:
            True if successful, False otherwise
        """
        if not glfw.init():
            print("ERROR: Failed to initialize GLFW")
            return False
        
        # Configure GLFW for OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)  # For macOS compatibility
        glfw.window_hint(glfw.RESIZABLE, glfw.TRUE)
        
        # Create window (initially windowed)
        self.window = glfw.create_window(self.width, self.height, self.title, None, None)
        if not self.window:
            print("ERROR: Failed to create GLFW window")
            glfw.terminate()
            return False
        
        # Store initial windowed size for fullscreen toggle
        self._windowed_width = self.width
        self._windowed_height = self.height
        self._windowed_xpos = 100
        self._windowed_ypos = 100
        self.is_fullscreen = False
        
        # Make the OpenGL context current
        glfw.make_context_current(self.window)
        
        # Enable VSync
        glfw.swap_interval(1)
        
        # Set up callbacks
        glfw.set_window_user_pointer(self.window, self)
        glfw.set_framebuffer_size_callback(self.window, Window._framebuffer_resize_callback)
        glfw.set_cursor_pos_callback(self.window, Window._mouse_callback_internal)
        glfw.set_scroll_callback(self.window, Window._scroll_callback_internal)
        glfw.set_mouse_button_callback(self.window, Window._mouse_button_callback_internal)
        
        print(f"[OK] Window created: {self.width}x{self.height}")
        return True
    
    @staticmethod
    def _framebuffer_resize_callback(window, width: int, height: int):
        """Internal callback for framebuffer resize events."""
        window_obj = glfw.get_window_user_pointer(window)
        if window_obj and window_obj._resize_callback:
            window_obj._resize_callback(width, height)
    
    @staticmethod
    def _mouse_callback_internal(window, xpos: float, ypos: float):
        """Internal callback for mouse movement."""
        window_obj = glfw.get_window_user_pointer(window)
        if window_obj and window_obj._mouse_callback:
            # Always send mouse move events (not just when captured)
            # This is needed for UI interaction (sliders, hover, etc.)
            window_obj._mouse_callback(xpos, ypos)
    
    @staticmethod
    def _scroll_callback_internal(window, xoffset: float, yoffset: float):
        """Internal callback for mouse scroll."""
        window_obj = glfw.get_window_user_pointer(window)
        if window_obj and window_obj._scroll_callback:
            window_obj._scroll_callback(xoffset, yoffset)
    
    @staticmethod
    def _mouse_button_callback_internal(window, button: int, action: int, mods: int):
        """Internal callback for mouse button events."""
        window_obj = glfw.get_window_user_pointer(window)
        if window_obj and window_obj._mouse_button_callback:
            # Get current mouse position
            xpos, ypos = glfw.get_cursor_pos(window)
            window_obj._mouse_button_callback(button, action, mods, xpos, ypos)
    
    def set_resize_callback(self, callback: Callable[[int, int], None]):
        """
        Set a callback for window resize events.
        
        Args:
            callback: Function that takes (width, height) as parameters
        """
        self._resize_callback = callback
    
    def set_mouse_callback(self, callback: Callable[[float, float], None]):
        """
        Set a callback for mouse movement.
        
        Args:
            callback: Function that takes (xpos, ypos) as parameters
        """
        self._mouse_callback = callback
    
    def set_scroll_callback(self, callback: Callable[[float, float], None]):
        """
        Set a callback for mouse scroll.
        
        Args:
            callback: Function that takes (xoffset, yoffset) as parameters
        """
        self._scroll_callback = callback
    
    def set_mouse_button_callback(self, callback: Callable[[int, int, int, float, float], None]):
        """
        Set a callback for mouse button events.
        
        Args:
            callback: Function that takes (button, action, mods, xpos, ypos) as parameters
        """
        self._mouse_button_callback = callback
    
    def capture_mouse(self, capture: bool = True):
        """
        Capture or release the mouse cursor.
        
        Args:
            capture: True to capture and hide cursor, False to release
        """
        self.mouse_captured = capture
        if capture:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_DISABLED)
        else:
            glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_NORMAL)
    
    def should_close(self) -> bool:
        """Check if the window should close."""
        return glfw.window_should_close(self.window)
    
    def poll_events(self):
        """Poll for window events."""
        glfw.poll_events()
    
    def get_key(self, key: int) -> int:
        """
        Get the state of a keyboard key.
        
        Args:
            key: GLFW key constant
            
        Returns:
            Key state (GLFW_PRESS, GLFW_RELEASE, etc.)
        """
        return glfw.get_key(self.window, key)
    
    def get_framebuffer_size(self) -> tuple[int, int]:
        """
        Get the current framebuffer size.
        
        Returns:
            Tuple of (width, height)
        """
        return glfw.get_framebuffer_size(self.window)
    
    def swap_buffers(self):
        """Swap the front and back buffers (present the rendered frame)."""
        glfw.swap_buffers(self.window)
    
    def set_fullscreen(self, fullscreen: bool):
        """
        Toggle fullscreen mode.
        
        Args:
            fullscreen: True for fullscreen, False for windowed
        """
        if not self.window:
            return
        
        if fullscreen and not self.is_fullscreen:
            # Save current windowed position and size
            self._windowed_xpos, self._windowed_ypos = glfw.get_window_pos(self.window)
            self._windowed_width, self._windowed_height = glfw.get_window_size(self.window)
            
            # Get primary monitor and its video mode
            monitor = glfw.get_primary_monitor()
            mode = glfw.get_video_mode(monitor)
            
            # Set to fullscreen
            glfw.set_window_monitor(
                self.window,
                monitor,
                0, 0,
                mode.size.width,
                mode.size.height,
                mode.refresh_rate
            )
            
            self.is_fullscreen = True
            self.width = mode.size.width
            self.height = mode.size.height
            print(f"[Window] Switched to fullscreen: {mode.size.width}x{mode.size.height}")
            
            # Force GLFW to process the monitor change
            glfw.poll_events()
            
            # Trigger framebuffer resize callback to update viewport
            print(f"[Window] Triggering resize callback: {mode.size.width}x{mode.size.height}")
            if self._resize_callback:
                self._resize_callback(mode.size.width, mode.size.height)
            
        elif not fullscreen and self.is_fullscreen:
            # Restore windowed mode
            glfw.set_window_monitor(
                self.window,
                None,
                self._windowed_xpos,
                self._windowed_ypos,
                self._windowed_width,
                self._windowed_height,
                0
            )
            
            self.is_fullscreen = False
            self.width = self._windowed_width
            self.height = self._windowed_height
            print(f"[Window] Switched to windowed: {self._windowed_width}x{self._windowed_height}")
            
            # Force GLFW to process the monitor change
            glfw.poll_events()
            
            # Trigger framebuffer resize callback to update viewport
            print(f"[Window] Triggering resize callback: {self._windowed_width}x{self._windowed_height}")
            if self._resize_callback:
                self._resize_callback(self._windowed_width, self._windowed_height)
    
    def cleanup(self):
        """Clean up window resources."""
        if self.window:
            glfw.destroy_window(self.window)
            self.window = None
        glfw.terminate()
        print("[OK] Window cleaned up")

