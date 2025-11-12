"""
UI Manager
Manages all UI elements, handles input routing, and coordinates rendering.
"""

from typing import List, Optional, Tuple
from .ui_element import UIElement
from .ui_compiler import UICompiler


class UIManager:
    """
    Manages UI elements and handles input routing.
    Central coordinator for the UI system.
    """
    
    def __init__(self, window_width: int, window_height: int):
        """
        Initialize UI manager.
        
        Args:
            window_width: Window width in pixels
            window_height: Window height in pixels
        """
        self.window_width = window_width
        self.window_height = window_height
        
        # Root UI elements (top-level panels, buttons, etc.)
        self.elements: List[UIElement] = []
        
        # Focused element
        self.focused_element: Optional[UIElement] = None
        
        # Mouse state
        self.mouse_x = 0.0
        self.mouse_y = 0.0
        self.mouse_pressed = False
        
        # CSS-like size compiler (%, vw, vh → px)
        self.compiler = UICompiler(window_width, window_height)
        
        print("[UIManager] Initialized with CSS-like sizing support")
    
    def add_element(self, element: UIElement):
        """
        Add a root UI element.
        
        Args:
            element: UI element to add
        """
        if element not in self.elements:
            self.elements.append(element)
    
    def remove_element(self, element: UIElement):
        """
        Remove a root UI element.
        
        Args:
            element: UI element to remove
        """
        if element in self.elements:
            self.elements.remove(element)
    
    def clear(self):
        """Remove all UI elements."""
        self.elements.clear()
        self.focused_element = None
    
    def on_mouse_move(self, x: float, y: float):
        """
        Handle mouse movement.
        
        Args:
            x: Mouse X position
            y: Mouse Y position
        """
        self.mouse_x = x
        self.mouse_y = y
        
        # Update hover state for all elements
        for element in self.elements:
            element.handle_mouse_move(x, y)
    
    def on_mouse_click(self, x: float, y: float, button: int) -> bool:
        """
        Handle mouse click.
        
        Args:
            x: Mouse X position
            y: Mouse Y position
            button: Mouse button (0=left, 1=right, 2=middle)
            
        Returns:
            True if event was handled
        """
        self.mouse_pressed = True
        
        # Process elements in reverse order (front to back)
        for element in reversed(self.elements):
            if element.handle_mouse_click(x, y, button):
                # Element consumed the click
                return True
        
        return False
    
    def on_mouse_release(self, x: float, y: float, button: int):
        """
        Handle mouse release.
        
        Args:
            x: Mouse X position
            y: Mouse Y position
            button: Mouse button
        """
        self.mouse_pressed = False
        
        # Process elements
        for element in reversed(self.elements):
            if element.handle_mouse_release(x, y, button):
                break
    
    def update(self, delta_time: float):
        """
        Update all UI elements.
        
        Args:
            delta_time: Time since last frame in seconds
        """
        for element in self.elements:
            element.update(delta_time)
    
    def render(self, text_renderer, ui_renderer=None):
        """
        Render all UI elements in layer order (back to front).
        Compiles CSS-like sizes (%, vw, vh) before rendering.
        
        Args:
            text_renderer: TextRenderer instance for drawing
            ui_renderer: UIRenderer instance for OpenGL components (optional, for backward compat)
        """
        # Compile sizes for all elements (%, vw, vh → px)
        for element in self.elements:
            self._compile_element_recursive(element)
        
        # Sort elements by layer (lower layers first, higher layers on top)
        sorted_elements = sorted(self.elements, key=lambda e: e.layer)
        
        # Render in layer order
        for element in sorted_elements:
            if element.visible:
                # Check if element needs both renderers (modern UI)
                if ui_renderer is not None:
                    element.render(ui_renderer, text_renderer)
                else:
                    element.render(text_renderer)
    
    def _compile_element_recursive(self, element):
        """
        Recursively compile an element and its children.
        
        Args:
            element: Element to compile
        """
        # Check if element supports CSS-like sizing
        if hasattr(element, 'x_size') and hasattr(element, 'compiled_x'):
            self.compiler.compile_component(element)
        
        # Compile children
        if hasattr(element, 'children'):
            for child in element.children:
                self._compile_element_recursive(child)
    
    def set_window_size(self, width: int, height: int):
        """
        Update window size (for anchor calculations and CSS-like sizing).
        
        Args:
            width: New window width
            height: New window height
        """
        self.window_width = width
        self.window_height = height
        
        # Update compiler viewport
        self.compiler.set_viewport(width, height)
    
    def get_element_at(self, x: float, y: float) -> Optional[UIElement]:
        """
        Get the topmost UI element at a position.
        
        Args:
            x: X position
            y: Y position
            
        Returns:
            UIElement or None
        """
        for element in reversed(self.elements):
            if element.visible and element.contains_point(x, y):
                return element
        return None
    
    def print_hierarchy(self, element: Optional[UIElement] = None, indent: int = 0):
        """
        Print UI element hierarchy (for debugging).
        
        Args:
            element: Element to print (None = print all)
            indent: Indentation level
        """
        if element is None:
            print("\nUI Hierarchy:")
            for elem in self.elements:
                self.print_hierarchy(elem, 0)
        else:
            prefix = "  " * indent
            print(f"{prefix}- {element.__class__.__name__} ({element.x}, {element.y}, {element.width}x{element.height})")
            for child in element.children:
                self.print_hierarchy(child, indent + 1)

