"""
GameScript Module
Base class for game scripts/behaviors that can be attached to entities or scenes.
"""

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .entity import Entity
    from .scene import Scene


class GameScript:
    """Base class for game scripts/behaviors."""
    
    def __init__(self, entity: Optional['Entity'] = None):
        """
        Initialize a game script.
        
        Args:
            entity: Optional entity this script is attached to.
                    None if attached globally to the scene.
        """
        self.entity = entity
        self.scene: Optional['Scene'] = None
        self.enabled = True
    
    def on_attach(self):
        """Called when the script is attached to an entity or scene."""
        pass
    
    def on_detach(self):
        """Called when the script is detached from an entity or scene."""
        pass
    
    def on_update(self, delta_time: float):
        """
        Called every frame to update the script logic.
        
        Args:
            delta_time: Time since last frame in seconds
        """
        pass
    
    def on_start(self):
        """Called once when the script first starts (before first update)."""
        pass
    
    def on_enable(self):
        """Called when the script is enabled."""
        pass
    
    def on_disable(self):
        """Called when the script is disabled."""
        pass
    
    def set_enabled(self, enabled: bool):
        """
        Enable or disable this script.
        
        Args:
            enabled: True to enable, False to disable
        """
        if self.enabled != enabled:
            self.enabled = enabled
            if enabled:
                self.on_enable()
            else:
                self.on_disable()
    
    def __repr__(self) -> str:
        """String representation of the script."""
        entity_name = self.entity.name if self.entity else "Scene"
        return f"{self.__class__.__name__}(entity='{entity_name}', enabled={self.enabled})"

