"""
Scene Module
Manages game objects, cameras, and scene hierarchy.
"""

from typing import List, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .gameobject import GameObject
    from .camera import Camera
    from .entity import Entity
    from .gamescript import GameScript
    from .light import Light


class Scene:
    """Represents a game scene containing game objects and cameras (all are entities)."""
    
    def __init__(self, name: str = "Scene"):
        """
        Initialize a scene.
        
        Args:
            name: Scene name
        """
        self.name = name
        self.game_objects: List['GameObject'] = []
        self.cameras: List['Camera'] = []
        self.lights: List['Light'] = []
        self.text3d_objects: List = []  # 3D text entities
        self.audio_sources: List = []  # Audio sources (Audio2D and Audio3D)
        self.active_camera_index: int = 0
        self._entities: List['Entity'] = []  # All entities (unified list)
        self.scripts: List['GameScript'] = []  # Global scripts attached to the scene
        self._scripts_started = False
    
    def add_game_object(self, game_object: 'GameObject'):
        """
        Add a game object to the scene.
        
        Args:
            game_object: GameObject to add
        """
        self.game_objects.append(game_object)
        self._entities.append(game_object)
    
    def remove_game_object(self, game_object: 'GameObject'):
        """
        Remove a game object from the scene.
        
        Args:
            game_object: GameObject to remove
        """
        if game_object in self.game_objects:
            self.game_objects.remove(game_object)
        if game_object in self._entities:
            self._entities.remove(game_object)
    
    def get_active_objects(self) -> List['GameObject']:
        """
        Get all active game objects in the scene.
        
        Returns:
            List of active GameObjects
        """
        return [obj for obj in self.game_objects if obj.active]
    
    def find_by_name(self, name: str) -> Optional['GameObject']:
        """
        Find a game object by name.
        
        Args:
            name: Name to search for
            
        Returns:
            GameObject if found, None otherwise
        """
        for obj in self.game_objects:
            if obj.name == name:
                return obj
        return None
    
    def clear(self):
        """Remove all game objects from the scene."""
        self.game_objects.clear()
    
    @property
    def object_count(self) -> int:
        """Get the total number of objects in the scene."""
        return len(self.game_objects)
    
    # === Camera Management ===
    
    def add_camera(self, camera: 'Camera'):
        """
        Add a camera to the scene.
        
        Args:
            camera: Camera to add
        """
        self.cameras.append(camera)
        self._entities.append(camera)
        # If this is the first camera, set it as active
        if len(self.cameras) == 1:
            self.active_camera_index = 0
    
    def remove_camera(self, camera: 'Camera'):
        """
        Remove a camera from the scene.
        
        Args:
            camera: Camera to remove
        """
        if camera in self.cameras:
            index = self.cameras.index(camera)
            self.cameras.remove(camera)
            
            # Adjust active camera index if needed
            if self.active_camera_index >= len(self.cameras):
                self.active_camera_index = max(0, len(self.cameras) - 1)
        
        if camera in self._entities:
            self._entities.remove(camera)
    
    def set_active_camera(self, index: int):
        """
        Set the active camera by index.
        
        Args:
            index: Camera index to set as active
        """
        if 0 <= index < len(self.cameras):
            self.active_camera_index = index
    
    def get_active_camera(self) -> Optional['Camera']:
        """
        Get the currently active camera.
        
        Returns:
            Active camera if exists, None otherwise
        """
        if 0 <= self.active_camera_index < len(self.cameras):
            return self.cameras[self.active_camera_index]
        return None
    
    @property
    def camera_count(self) -> int:
        """Get the total number of cameras in the scene."""
        return len(self.cameras)
    
    # === Light Management ===
    
    def add_light(self, light: 'Light'):
        """
        Add a light to the scene.
        
        Args:
            light: Light to add
        """
        self.lights.append(light)
        self._entities.append(light)
    
    def remove_light(self, light: 'Light'):
        """
        Remove a light from the scene.
        
        Args:
            light: Light to remove
        """
        if light in self.lights:
            self.lights.remove(light)
            if light in self._entities:
                self._entities.remove(light)
    
    def get_active_lights(self) -> List['Light']:
        """
        Get all active lights in the scene.
        
        Returns:
            List of active lights
        """
        return [light for light in self.lights if light.active]
    
    @property
    def light_count(self) -> int:
        """Get the total number of lights in the scene."""
        return len(self.lights)
    
    # === Text3D Management ===
    
    def add_text3d(self, text3d):
        """
        Add a 3D text object to the scene.
        
        Args:
            text3d: Text3D object to add
        """
        self.text3d_objects.append(text3d)
        self._entities.append(text3d)
    
    def remove_text3d(self, text3d):
        """
        Remove a 3D text object from the scene.
        
        Args:
            text3d: Text3D object to remove
        """
        if text3d in self.text3d_objects:
            self.text3d_objects.remove(text3d)
            if text3d in self._entities:
                self._entities.remove(text3d)
    
    def get_active_text3d(self) -> List:
        """
        Get all active 3D text objects in the scene.
        
        Returns:
            List of active Text3D objects
        """
        return [text for text in self.text3d_objects if text.active]
    
    @property
    def text3d_count(self) -> int:
        """Get the total number of 3D text objects in the scene."""
        return len(self.text3d_objects)
    
    # === Audio Source Management ===
    
    def add_audio_source(self, audio_source):
        """
        Add an audio source to the scene.
        
        Args:
            audio_source: AudioSource (Audio2D or Audio3D)
        """
        self.audio_sources.append(audio_source)
        self._entities.append(audio_source)
    
    def remove_audio_source(self, audio_source):
        """
        Remove an audio source from the scene.
        
        Args:
            audio_source: AudioSource to remove
        """
        if audio_source in self.audio_sources:
            # Stop playback before removing
            if hasattr(audio_source, 'stop'):
                audio_source.stop()
            self.audio_sources.remove(audio_source)
            if audio_source in self._entities:
                self._entities.remove(audio_source)
    
    def get_active_audio_sources(self) -> List:
        """
        Get all active audio sources in the scene.
        
        Returns:
            List of active audio sources
        """
        return [source for source in self.audio_sources if source.active]
    
    @property
    def audio_source_count(self) -> int:
        """Get the total number of audio sources in the scene."""
        return len(self.audio_sources)
    
    # === Entity Management (Generic) ===
    
    def get_all_entities(self) -> List['Entity']:
        """
        Get all entities in the scene (game objects + cameras).
        
        Returns:
            List of all entities
        """
        return self._entities.copy()
    
    def get_active_entities(self) -> List['Entity']:
        """
        Get all active entities in the scene.
        
        Returns:
            List of active entities
        """
        return [entity for entity in self._entities if entity.active]
    
    def find_entity_by_name(self, name: str) -> Optional['Entity']:
        """
        Find any entity by name (searches game objects and cameras).
        
        Args:
            name: Name to search for
            
        Returns:
            Entity if found, None otherwise
        """
        for entity in self._entities:
            if entity.name == name:
                return entity
        return None
    
    def find_entities_by_tag(self, tag: str) -> List['Entity']:
        """
        Find all entities with a specific tag.
        
        Args:
            tag: Tag to search for
            
        Returns:
            List of entities with the tag
        """
        return [entity for entity in self._entities if entity.has_tag(tag)]
    
    @property
    def entity_count(self) -> int:
        """Get the total number of entities in the scene."""
        return len(self._entities)
    
    # === Script Management (Global) ===
    
    def add_script(self, script: 'GameScript'):
        """
        Add a global script to the scene.
        
        Args:
            script: GameScript to attach globally (no specific entity)
        """
        # Initialize script without an entity (global to scene)
        script.entity = None
        script.scene = self
        self.scripts.append(script)
        
        # Call on_attach callback with scene reference
        script.on_attach(self)
        
        # If scripts have already been started, start this new one
        if self._scripts_started:
            script.on_start()
    
    def remove_script(self, script: 'GameScript'):
        """
        Remove a global script from the scene.
        
        Args:
            script: GameScript to remove
        """
        if script in self.scripts:
            script.on_detach()
            self.scripts.remove(script)
            script.scene = None
    
    def get_script(self, script_type: type) -> Optional['GameScript']:
        """
        Get the first global script of a specific type.
        
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
        Get all global scripts, optionally filtered by type.
        
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
        Update all scripts in the scene (global + entity scripts).
        
        Args:
            delta_time: Time since last frame
        """
        # Start global scripts on first update
        if not self._scripts_started:
            for script in self.scripts:
                if script.enabled:
                    script.on_start()
            self._scripts_started = True
        
        # Update global scripts
        for script in self.scripts:
            if script.enabled:
                script.on_update(delta_time)
        
        # Update all entity scripts
        for entity in self._entities:
            if entity.active:
                entity.update_scripts(delta_time)

