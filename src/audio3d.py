"""
Audio3D Module
Positional audio source with distance-based attenuation.
"""

import numpy as np
from typing import Optional, Tuple
from .audio_source import AudioSource
from .audio_clip import AudioClip
from .gameobject import Transform


class Audio3D(AudioSource):
    """
    3D Audio Source - positional audio with distance-based volume.
    Perfect for environmental sounds, character voices, effects in world.
    """
    
    def __init__(
        self,
        name: str = "Audio3D",
        clip: Optional[AudioClip] = None,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        volume: float = 1.0,
        loop: bool = False,
        play_on_start: bool = False,
        auto_play: bool = False,
        min_distance: float = 1.0,  # Full volume within this distance
        max_distance: float = 50.0,  # No volume beyond this distance
        rolloff_factor: float = 1.0,  # How quickly volume decreases
        category: str = "sfx"
    ):
        """
        Initialize 3D audio source.
        
        Args:
            name: Source name
            clip: Audio clip to play
            position: Position in 3D world space
            volume: Base volume level (0.0-1.0)
            loop: Whether to loop the audio
            play_on_start: Play when scene starts
            auto_play: Play immediately when clip is set
            min_distance: Distance where volume is maximum
            max_distance: Distance where volume reaches zero
            rolloff_factor: How quickly sound attenuates (1.0 = linear, 2.0 = faster)
            category: Audio category for mixing
        """
        super().__init__(name, clip, volume, loop, play_on_start, auto_play)
        
        # Transform for 3D positioning
        self.transform = Transform(position=position)
        
        # 3D audio properties
        self.min_distance = min_distance
        self.max_distance = max_distance
        self.rolloff_factor = rolloff_factor
        self.category = category
        
        # Calculated values
        self._calculated_volume = volume
        self._distance_to_listener = 0.0
    
    @property
    def position(self) -> Tuple[float, float, float]:
        """Get position (shortcut to transform)."""
        return tuple(self.transform.position)
    
    @position.setter
    def position(self, value: Tuple[float, float, float]):
        """Set position (shortcut to transform)."""
        self.transform.set_position(*value)
    
    def calculate_volume_and_pan(self, listener_position: np.ndarray, listener_right: np.ndarray) -> Tuple[float, float]:
        """
        Calculate volume and stereo panning based on distance and direction to listener.
        
        Args:
            listener_position: Position of the audio listener (camera)
            listener_right: Right vector of the listener (for stereo panning)
            
        Returns:
            Tuple of (left_volume, right_volume) for stereo positioning
        """
        # Calculate direction from listener to sound source
        to_source = self.transform.position - listener_position
        distance = np.linalg.norm(to_source)
        self._distance_to_listener = distance
        
        # Calculate distance attenuation
        if distance <= self.min_distance:
            # Full volume within min distance
            attenuation = 1.0
        elif distance >= self.max_distance:
            # Silent beyond max distance
            attenuation = 0.0
        else:
            # Linear rolloff between min and max distance
            normalized_distance = (distance - self.min_distance) / (self.max_distance - self.min_distance)
            attenuation = 1.0 - pow(normalized_distance, self.rolloff_factor)
            attenuation = max(0.0, min(1.0, attenuation))
        
        # Calculate base volume
        base_volume = self.volume * attenuation
        self._calculated_volume = base_volume
        
        # Calculate stereo panning
        if distance > 0.01:  # Avoid division by zero
            # Normalize direction
            direction_normalized = to_source / distance
            
            # Project onto listener's right vector to get left/right position
            # Dot product: -1 = left, 0 = center, +1 = right
            pan = np.dot(direction_normalized, listener_right)
            
            # Convert pan to stereo volumes
            # Pan of -1 (left): left=1.0, right=0.5
            # Pan of  0 (center): left=1.0, right=1.0
            # Pan of +1 (right): left=0.5, right=1.0
            
            # Use a smoother panning curve
            if pan < 0:  # Sound is to the left
                left_volume = base_volume
                right_volume = base_volume * (1.0 + pan * 0.5)  # Reduce right by up to 50%
            else:  # Sound is to the right
                left_volume = base_volume * (1.0 - pan * 0.5)  # Reduce left by up to 50%
                right_volume = base_volume
        else:
            # Source is at listener position - equal on both channels
            left_volume = base_volume
            right_volume = base_volume
        
        return left_volume, right_volume
    
    def calculate_volume(self, listener_position: np.ndarray) -> float:
        """
        Calculate volume based on distance to listener (for backward compatibility).
        
        Args:
            listener_position: Position of the audio listener
            
        Returns:
            Calculated volume (0.0-1.0)
        """
        # Calculate distance
        distance = np.linalg.norm(self.transform.position - listener_position)
        self._distance_to_listener = distance
        
        # Calculate attenuation
        if distance <= self.min_distance:
            attenuation = 1.0
        elif distance >= self.max_distance:
            attenuation = 0.0
        else:
            normalized_distance = (distance - self.min_distance) / (self.max_distance - self.min_distance)
            attenuation = 1.0 - pow(normalized_distance, self.rolloff_factor)
            attenuation = max(0.0, min(1.0, attenuation))
        
        self._calculated_volume = self.volume * attenuation
        return self._calculated_volume
    
    def update(self, delta_time: float, listener_position: Optional[np.ndarray] = None):
        """
        Update audio source with 3D positioning.
        
        Args:
            delta_time: Time since last frame
            listener_position: Position of the audio listener
        """
        super().update(delta_time)
        
        # Update volume based on distance
        if listener_position is not None and self.is_playing and self.channel:
            calculated_volume = self.calculate_volume(listener_position)
            self.channel.set_volume(calculated_volume)
    
    def set_min_distance(self, distance: float):
        """Set minimum distance (full volume range)."""
        self.min_distance = max(0.0, distance)
    
    def set_max_distance(self, distance: float):
        """Set maximum distance (silent range)."""
        self.max_distance = max(self.min_distance, distance)
    
    def set_rolloff_factor(self, factor: float):
        """Set rolloff factor (1.0 = linear, >1.0 = faster falloff)."""
        self.rolloff_factor = max(0.1, factor)
    
    def __repr__(self) -> str:
        clip_name = self.clip.filepath if self.clip else "None"
        status = "playing" if self.is_playing else ("paused" if self.is_paused else "stopped")
        return f"Audio3D('{self.name}', pos={self.position}, {status}, vol={self.volume:.2f}, calc_vol={self._calculated_volume:.2f}, dist={self._distance_to_listener:.1f})"

