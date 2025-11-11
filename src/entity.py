"""
Entity Module
Base class for all scene entities (cameras, game objects, etc.).
"""

from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .gamescript import GameScript


class Entity:
    """Base class for all entities in a scene."""
    
    def __init__(self, name: str = "Entity"):
        """
        Initialize an entity.
        
        Args:
            name: Entity name for identification
        """
        self.name = name
        self.active = True  # Whether this entity is active
        self.parent: Optional['Entity'] = None
        self.children: List['Entity'] = []
        self.tags: set[str] = set()  # Tags for grouping/filtering entities
        self.scripts: List['GameScript'] = []  # Scripts attached to this entity
        self._scripts_started = False
    
    def set_active(self, active: bool):
        """
        Set the active state of this entity.
        
        Args:
            active: True to activate, False to deactivate
        """
        self.active = active
    
    def add_tag(self, tag: str):
        """
        Add a tag to this entity.
        
        Args:
            tag: Tag to add
        """
        self.tags.add(tag)
    
    def remove_tag(self, tag: str):
        """
        Remove a tag from this entity.
        
        Args:
            tag: Tag to remove
        """
        self.tags.discard(tag)
    
    def has_tag(self, tag: str) -> bool:
        """
        Check if entity has a specific tag.
        
        Args:
            tag: Tag to check
            
        Returns:
            True if entity has the tag, False otherwise
        """
        return tag in self.tags
    
    def add_child(self, child: 'Entity'):
        """
        Add a child entity.
        
        Args:
            child: Child entity to add
        """
        if child not in self.children:
            self.children.append(child)
            child.parent = self
    
    def remove_child(self, child: 'Entity'):
        """
        Remove a child entity.
        
        Args:
            child: Child entity to remove
        """
        if child in self.children:
            self.children.remove(child)
            child.parent = None
    
    def get_children(self, recursive: bool = False) -> List['Entity']:
        """
        Get all children of this entity.
        
        Args:
            recursive: If True, gets all descendants
            
        Returns:
            List of child entities
        """
        if not recursive:
            return self.children.copy()
        
        # Get all descendants recursively
        all_children = []
        for child in self.children:
            all_children.append(child)
            all_children.extend(child.get_children(recursive=True))
        return all_children
    
    # === Script Management ===
    
    def add_script(self, script: 'GameScript'):
        """
        Add a script to this entity.
        
        Args:
            script: GameScript instance to attach
        """
        # Initialize the script with this entity
        script.entity = self
        self.scripts.append(script)
        
        # Call on_attach callback
        script.on_attach()
        
        # If scripts have already been started, start this new one
        if self._scripts_started:
            script.on_start()
    
    def remove_script(self, script: 'GameScript'):
        """
        Remove a script from this entity.
        
        Args:
            script: GameScript to remove
        """
        if script in self.scripts:
            script.on_detach()
            self.scripts.remove(script)
            script.entity = None
    
    def get_script(self, script_type: type) -> Optional['GameScript']:
        """
        Get the first script of a specific type.
        
        Args:
            script_type: Type of script to find
            
        Returns:
            Script instance if found, None otherwise
        """
        for script in self.scripts:
            if isinstance(script, script_type):
                return script
        return None
    
    def get_scripts(self, script_type: type = None) -> List['GameScript']:
        """
        Get all scripts, optionally filtered by type.
        
        Args:
            script_type: Optional type to filter by
            
        Returns:
            List of scripts
        """
        if script_type is None:
            return self.scripts.copy()
        return [s for s in self.scripts if isinstance(s, script_type)]
    
    def update_scripts(self, delta_time: float):
        """
        Update all active scripts attached to this entity.
        
        Args:
            delta_time: Time since last frame
        """
        # Start scripts on first update
        if not self._scripts_started:
            for script in self.scripts:
                if script.enabled:
                    script.on_start()
            self._scripts_started = True
        
        # Update enabled scripts
        for script in self.scripts:
            if script.enabled:
                script.on_update(delta_time)
    
    def __repr__(self) -> str:
        """String representation of the entity."""
        return f"{self.__class__.__name__}(name='{self.name}', active={self.active}, scripts={len(self.scripts)})"

