"""
FlexContainer
CSS-like flexbox container for automatic layout.
"""

from typing import List, Optional, Union
from enum import Enum
from .ui_element import UIElement, Anchor
from .ui_units import UISize, px


class FlexDirection(Enum):
    """Flex direction (main axis)."""
    ROW = "row"              # Horizontal (left to right)
    ROW_REVERSE = "row-reverse"  # Horizontal (right to left)
    COLUMN = "column"        # Vertical (top to bottom)
    COLUMN_REVERSE = "column-reverse"  # Vertical (bottom to top)


class JustifyContent(Enum):
    """Justify content (main axis alignment)."""
    FLEX_START = "flex-start"    # Start of container
    FLEX_END = "flex-end"        # End of container
    CENTER = "center"            # Center of container
    SPACE_BETWEEN = "space-between"  # Even spacing, no edges
    SPACE_AROUND = "space-around"    # Even spacing, half edges
    SPACE_EVENLY = "space-evenly"    # Even spacing, full edges


class AlignItems(Enum):
    """Align items (cross axis alignment)."""
    FLEX_START = "flex-start"  # Start of cross axis
    FLEX_END = "flex-end"      # End of cross axis
    CENTER = "center"          # Center of cross axis
    STRETCH = "stretch"        # Stretch to fill
    BASELINE = "baseline"      # Align baselines


class FlexWrap(Enum):
    """Flex wrap behavior."""
    NOWRAP = "nowrap"    # Single line
    WRAP = "wrap"        # Multi-line
    WRAP_REVERSE = "wrap-reverse"  # Multi-line (reverse)


class FlexContainer(UIElement):
    """
    Flexbox container that automatically positions children.
    
    CSS-like flexbox for game UIs!
    
    Examples:
        # Horizontal row
        row = FlexContainer(direction="row", justify="space-between")
        row.add_child(UIButton(...))
        row.add_child(UIButton(...))
        
        # Vertical column
        column = FlexContainer(direction="column", align="center")
        column.add_child(UILabel(...))
        column.add_child(UIButton(...))
        
        # Responsive grid
        grid = FlexContainer(direction="row", wrap="wrap", gap=px(10))
        for i in range(12):
            grid.add_child(UIPanel(...))
    """
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        width: Union[float, UISize] = 100.0,
        height: Union[float, UISize] = 100.0,
        direction: Union[str, FlexDirection] = FlexDirection.ROW,
        justify: Union[str, JustifyContent] = JustifyContent.FLEX_START,
        align: Union[str, AlignItems] = AlignItems.FLEX_START,
        wrap: Union[str, FlexWrap] = FlexWrap.NOWRAP,
        gap: Union[float, UISize] = 0.0,
        anchor: Anchor = Anchor.TOP_LEFT,
        **kwargs
    ):
        """
        Initialize flex container.
        
        Args:
            x, y, width, height: Standard component properties
            direction: Flex direction ("row", "column", etc.)
            justify: Main axis alignment ("flex-start", "center", etc.)
            align: Cross axis alignment ("flex-start", "center", etc.)
            wrap: Wrap behavior ("nowrap", "wrap", "wrap-reverse")
            gap: Gap between items (any unit)
            anchor: Anchor point
            **kwargs: Additional properties
        """
        # Import here to avoid circular dependency
        from .ui_calc import UICalc
        
        # Convert to float for UIElement
        x_val = float(x) if isinstance(x, (int, float)) else 0.0
        y_val = float(y) if isinstance(y, (int, float)) else 0.0
        width_val = float(width) if isinstance(width, (int, float)) else 100.0
        height_val = float(height) if isinstance(height, (int, float)) else 100.0
        
        super().__init__(x_val, y_val, width_val, height_val, anchor)
        
        # Store CSS-like sizes
        self.x_size = x if isinstance(x, (UISize, UICalc)) else px(x)
        self.y_size = y if isinstance(y, (UISize, UICalc)) else px(y)
        self.width_size = width if isinstance(width, (UISize, UICalc)) else px(width)
        self.height_size = height if isinstance(height, (UISize, UICalc)) else px(height)
        
        # Compiled sizes
        self.compiled_x = x_val
        self.compiled_y = y_val
        self.compiled_width = width_val
        self.compiled_height = height_val
        
        # Convert string to enum if needed
        if isinstance(direction, str):
            direction = FlexDirection(direction)
        if isinstance(justify, str):
            justify = JustifyContent(justify)
        if isinstance(align, str):
            align = AlignItems(align)
        if isinstance(wrap, str):
            wrap = FlexWrap(wrap)
        
        self.direction = direction
        self.justify = justify
        self.align = align
        self.wrap = wrap
        self.gap_size = gap if isinstance(gap, UISize) else px(gap)
        
        # Compiled gap (set by compiler)
        self.compiled_gap = float(gap) if isinstance(gap, (int, float)) else 0.0
    
    def is_horizontal(self) -> bool:
        """Check if flex direction is horizontal."""
        return self.direction in [FlexDirection.ROW, FlexDirection.ROW_REVERSE]
    
    def is_vertical(self) -> bool:
        """Check if flex direction is vertical."""
        return self.direction in [FlexDirection.COLUMN, FlexDirection.COLUMN_REVERSE]
    
    def is_reversed(self) -> bool:
        """Check if flex direction is reversed."""
        return self.direction in [FlexDirection.ROW_REVERSE, FlexDirection.COLUMN_REVERSE]
    
    def layout(self):
        """
        Perform flexbox layout on children.
        Called after size compilation.
        """
        if not self.children:
            return
        
        # Get container dimensions
        container_width = self.compiled_width
        container_height = self.compiled_height
        
        # Get main and cross axis sizes
        if self.is_horizontal():
            main_size = container_width
            cross_size = container_height
        else:
            main_size = container_height
            cross_size = container_width
        
        # Calculate total size of children + gaps
        total_child_size = 0.0
        for child in self.children:
            if self.is_horizontal():
                total_child_size += child.compiled_width
            else:
                total_child_size += child.compiled_height
        
        # Add gaps
        if len(self.children) > 1:
            total_child_size += self.compiled_gap * (len(self.children) - 1)
        
        # Calculate spacing based on justify-content
        spacing = 0.0
        start_offset = 0.0
        
        if self.justify == JustifyContent.FLEX_START:
            start_offset = 0.0
            spacing = self.compiled_gap
        elif self.justify == JustifyContent.FLEX_END:
            start_offset = main_size - total_child_size
            spacing = self.compiled_gap
        elif self.justify == JustifyContent.CENTER:
            start_offset = (main_size - total_child_size) / 2
            spacing = self.compiled_gap
        elif self.justify == JustifyContent.SPACE_BETWEEN:
            start_offset = 0.0
            if len(self.children) > 1:
                spacing = (main_size - (total_child_size - self.compiled_gap * (len(self.children) - 1))) / (len(self.children) - 1)
            else:
                spacing = 0.0
        elif self.justify == JustifyContent.SPACE_AROUND:
            if len(self.children) > 0:
                total_spacing = main_size - (total_child_size - self.compiled_gap * (len(self.children) - 1))
                spacing = total_spacing / len(self.children)
                start_offset = spacing / 2
        elif self.justify == JustifyContent.SPACE_EVENLY:
            if len(self.children) > 0:
                total_spacing = main_size - (total_child_size - self.compiled_gap * (len(self.children) - 1))
                spacing = total_spacing / (len(self.children) + 1)
                start_offset = spacing
        
        # Position children
        current_pos = start_offset
        
        children_list = list(self.children)
        if self.is_reversed():
            children_list.reverse()
        
        for child in children_list:
            # Main axis position
            if self.is_horizontal():
                child.compiled_x = current_pos
                current_pos += child.compiled_width + spacing
            else:
                child.compiled_y = current_pos
                current_pos += child.compiled_height + spacing
            
            # Cross axis position (align-items)
            if self.is_horizontal():
                # Vertical alignment
                if self.align == AlignItems.FLEX_START:
                    child.compiled_y = 0.0
                elif self.align == AlignItems.FLEX_END:
                    child.compiled_y = cross_size - child.compiled_height
                elif self.align == AlignItems.CENTER:
                    child.compiled_y = (cross_size - child.compiled_height) / 2
                elif self.align == AlignItems.STRETCH:
                    child.compiled_y = 0.0
                    child.compiled_height = cross_size
            else:
                # Horizontal alignment
                if self.align == AlignItems.FLEX_START:
                    child.compiled_x = 0.0
                elif self.align == AlignItems.FLEX_END:
                    child.compiled_x = cross_size - child.compiled_width
                elif self.align == AlignItems.CENTER:
                    child.compiled_x = (cross_size - child.compiled_width) / 2
                elif self.align == AlignItems.STRETCH:
                    child.compiled_x = 0.0
                    child.compiled_width = cross_size
    
    def handle_mouse_move(self, mouse_x: float, mouse_y: float) -> bool:
        """
        Handle mouse movement (pass to children).
        
        Args:
            mouse_x: Mouse X position
            mouse_y: Mouse Y position
            
        Returns:
            True if handled
        """
        for child in self.children:
            if child.handle_mouse_move(mouse_x, mouse_y):
                return True
        return False
    
    def handle_mouse_click(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        """
        Handle mouse click (pass to children).
        
        Args:
            mouse_x, mouse_y: Mouse position
            button: Mouse button
            
        Returns:
            True if handled
        """
        for child in reversed(self.children):
            if child.handle_mouse_click(mouse_x, mouse_y, button):
                return True
        return False
    
    def handle_mouse_release(self, mouse_x: float, mouse_y: float, button: int) -> bool:
        """
        Handle mouse release (pass to children).
        
        Args:
            mouse_x, mouse_y: Mouse position
            button: Mouse button
            
        Returns:
            True if handled
        """
        for child in self.children:
            if child.handle_mouse_release(mouse_x, mouse_y, button):
                return True
        return False
    
    def update(self, delta_time: float):
        """
        Update container and children.
        
        Args:
            delta_time: Time since last frame
        """
        for child in self.children:
            child.update(delta_time)
    
    def render(self, ui_renderer, text_renderer):
        """
        Render the flex container and its children.
        
        Args:
            ui_renderer: UIRenderer instance
            text_renderer: TextRenderer instance
        """
        if not self.visible:
            return
        
        # FlexContainer itself is invisible (just a layout container)
        # Render all children
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

