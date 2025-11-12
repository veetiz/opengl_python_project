"""
AudioClip Module
Represents loaded audio data.
"""

import pygame
import os
from typing import Optional


class AudioClip:
    """
    Represents a loaded audio file (WAV, MP3, OGG).
    This is just data - doesn't inherit from Entity.
    """
    
    def __init__(self, filepath: str):
        """
        Load an audio file.
        
        Args:
            filepath: Path to audio file (WAV, MP3, OGG)
        """
        self.filepath = filepath
        self.sound: Optional[pygame.mixer.Sound] = None
        self.duration: float = 0.0
        
        self._load()
    
    def _load(self):
        """Load the audio file."""
        try:
            if not os.path.exists(self.filepath):
                print(f"[AUDIO] ERROR: Audio file not found: {self.filepath}")
                return
            
            # Load sound
            self.sound = pygame.mixer.Sound(self.filepath)
            
            # Get duration (in seconds)
            self.duration = self.sound.get_length()
            
            print(f"[AUDIO] Loaded: {os.path.basename(self.filepath)} ({self.duration:.2f}s)")
            
        except Exception as e:
            print(f"[AUDIO] ERROR: Failed to load audio file '{self.filepath}': {e}")
            self.sound = None
    
    def is_loaded(self) -> bool:
        """Check if audio is loaded successfully."""
        return self.sound is not None
    
    def get_volume(self) -> float:
        """Get the volume of this clip (0.0-1.0)."""
        if self.sound:
            return self.sound.get_volume()
        return 0.0
    
    def set_volume(self, volume: float):
        """
        Set the volume of this clip.
        
        Args:
            volume: Volume level (0.0-1.0)
        """
        if self.sound:
            self.sound.set_volume(max(0.0, min(1.0, volume)))
    
    def __repr__(self) -> str:
        status = "loaded" if self.is_loaded() else "not loaded"
        return f"AudioClip('{os.path.basename(self.filepath)}', {status}, {self.duration:.2f}s)"

