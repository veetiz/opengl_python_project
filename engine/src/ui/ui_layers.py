"""
UI Layer System
Defines layer constants for proper z-ordering.
"""


class UILayers:
    """
    Standard UI layer definitions.
    Lower numbers render first (background), higher numbers render last (foreground).
    """
    
    # Background layers (0-99)
    BACKGROUND = 0
    PANEL_BACKGROUND = 10
    
    # Normal UI layers (100-199)
    PANEL = 100
    BUTTON = 100
    SLIDER = 100
    CHECKBOX = 100
    LABEL = 100
    
    # Interactive layers (200-299)
    DROPDOWN_CLOSED = 200
    TOOLTIP = 250
    
    # Overlay layers (300-399)
    DROPDOWN_OPEN = 300  # Open dropdowns on top of everything!
    MODAL_OVERLAY = 350
    
    # Top layers (400+)
    POPUP = 400
    NOTIFICATION = 450
    DEBUG_OVERLAY = 500


# Helper function to get layer for element based on state
def get_dynamic_layer(element, base_layer: int = 100) -> int:
    """
    Get dynamic layer for element based on its state.
    
    Args:
        element: UI element
        base_layer: Base layer when inactive
        
    Returns:
        Layer number
    """
    # Dropdowns move to higher layer when open
    if hasattr(element, 'is_open'):
        if element.is_open:
            return UILayers.DROPDOWN_OPEN
        else:
            return UILayers.DROPDOWN_CLOSED
    
    # Modals/popups are always on top
    if hasattr(element, 'is_modal') and element.is_modal:
        return UILayers.MODAL_OVERLAY
    
    return base_layer

