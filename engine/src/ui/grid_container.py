"""
GridContainer
CSS-like grid container for automatic 2D layouts.
"""

from typing import List, Optional, Union
from .ui_element import UIElement, Anchor
from .ui_units import UISize, px


class GridContainer(UIElement):
    """
    Grid container that automatically positions children in a grid.
    
    CSS-like grid for game UIs!
    
    Examples:
        # 3-column grid
        grid = GridContainer(columns=3, gap=px(10))
        for i in range(9):
            grid.add_child(UIPanel(...))
        # Auto-arranges in 3x3 grid!
        
        # Fixed columns, auto rows
        grid = GridContainer(columns=4, column_gap=px(20), row_gap=px(10))
        
        # Gallery layout
        gallery = GridContainer(
            width=vw(90),
            columns=3,
            gap=px(20)
        )
    """
    
    def __init__(
        self,
        x: Union[float, UISize] = 0.0,
        y: Union[float, UISize] = 0.0,
        width: Union[float, UISize] = 100.0,
        height: Union[float, UISize] = 100.0,
        columns: int = 1,
        rows: Optional[int] = None,  # Auto-calculate if None
        gap: Union[float, UISize] = 0.0,
        column_gap: Optional[Union[float, UISize]] = None,
        row_gap: Optional[Union[float, UISize]] = None,
        anchor: Anchor = Anchor.TOP_LEFT,
        **kwargs
    ):
        """
        Initialize grid container.
        
        Args:
            x, y, width, height: Standard component properties
            columns: Number of columns (default: 1)
            rows: Number of rows (None = auto-calculate)
            gap: Gap between items (both column and row)
            column_gap: Gap between columns (overrides gap)
            row_gap: Gap between rows (overrides gap)
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
        
        self.columns = max(1, columns)
        self.rows = rows
        
        # Store gap sizes
        if column_gap is not None:
            self.column_gap_size = column_gap if isinstance(column_gap, UISize) else px(column_gap)
        else:
            self.column_gap_size = gap if isinstance(gap, UISize) else px(gap)
        
        if row_gap is not None:
            self.row_gap_size = row_gap if isinstance(row_gap, UISize) else px(row_gap)
        else:
            self.row_gap_size = gap if isinstance(gap, UISize) else px(gap)
        
        # Compiled gaps (set by compiler)
        self.compiled_column_gap = float(column_gap or gap) if isinstance(column_gap or gap, (int, float)) else 0.0
        self.compiled_row_gap = float(row_gap or gap) if isinstance(row_gap or gap, (int, float)) else 0.0
    
    def layout(self):
        """
        Perform grid layout on children.
        Called after size compilation.
        """
        if not self.children:
            return
        
        # Calculate actual rows (auto if not specified)
        if self.rows is None:
            actual_rows = (len(self.children) + self.columns - 1) // self.columns  # Ceiling division
        else:
            actual_rows = self.rows
        
        # Calculate cell dimensions
        total_column_gaps = self.compiled_column_gap * (self.columns - 1) if self.columns > 1 else 0
        total_row_gaps = self.compiled_row_gap * (actual_rows - 1) if actual_rows > 1 else 0
        
        cell_width = (self.compiled_width - total_column_gaps) / self.columns
        cell_height = (self.compiled_height - total_row_gaps) / actual_rows if actual_rows > 0 else 0
        
        # Position children in grid
        for index, child in enumerate(self.children):
            # Calculate row and column
            row = index // self.columns
            col = index % self.columns
            
            # Calculate position
            x = col * (cell_width + self.compiled_column_gap)
            y = row * (cell_height + self.compiled_row_gap)
            
            # Set child position
            child.compiled_x = x
            child.compiled_y = y
            
            # Set child size to fill cell (minus any padding)
            # You can customize this - for now, children fill their cells
            child.compiled_width = cell_width
            child.compiled_height = cell_height
    
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
        Render the grid container and its children.
        
        Args:
            ui_renderer: UIRenderer instance
            text_renderer: TextRenderer instance
        """
        if not self.visible:
            return
        
        # GridContainer itself is invisible (just a layout container)
        # Render all children
        for child in self.children:
            if child.visible:
                child.render(ui_renderer, text_renderer)

