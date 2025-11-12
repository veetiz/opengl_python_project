"""
AudioSource Module
Base class for audio sources (2D and 3D audio).
"""

import pygame
import numpy as np
from typing import Optional, Tuple, TYPE_CHECKING
from ..scene.entity import Entity
from .audio_clip import AudioClip

if TYPE_CHECKING:
    from ..scene.gameobject import Transform


class AudioSource(Entity):
    """
    Base audio source class - inherits from Entity.
    Can play, pause, stop audio clips.
    """
    
    def __init__(
        self,
        name: str = "AudioSource",
        clip: Optional[AudioClip] = None,
        volume: float = 1.0,
        loop: bool = False,
        play_on_start: bool = False,
        auto_play: bool = False
    ):
        """
        Initialize audio source.
        
        Args:
            name: Source name
            clip: Audio clip to play
            volume: Volume level (0.0-1.0)
            loop: Whether to loop the audio
            play_on_start: Play when scene starts
            auto_play: Play immediately when clip is set
        """
        super().__init__(name=name)
        
        self.clip = clip
        self.volume = max(0.0, min(1.0, volume))
        self.loop = loop
        self.play_on_start = play_on_start
        self.auto_play = auto_play
        
        self.is_playing = False
        self.is_paused = False
        self.channel: Optional[pygame.mixer.Channel] = None
    
    def set_clip(self, clip: AudioClip):
        """
        Set the audio clip.
        
        Args:
            clip: Audio clip to play
        """
        # Stop current playback
        if self.is_playing:
            self.stop()
        
        self.clip = clip
        
        if self.auto_play and clip and clip.is_loaded():
            self.play()
    
    def play(self):
        """Play the audio clip."""
        if not self.clip or not self.clip.is_loaded() or not self.active:
            return
        
        # Stop current playback
        if self.is_playing:
            self.stop()
        
        # Play sound
        loops = -1 if self.loop else 0
        self.channel = self.clip.sound.play(loops=loops)
        
        if self.channel:
            self.channel.set_volume(self.volume)
            self.is_playing = True
            self.is_paused = False
    
    def pause(self):
        """Pause the audio."""
        if self.is_playing and not self.is_paused and self.channel:
            self.channel.pause()
            self.is_paused = True
    
    def unpause(self):
        """Resume paused audio."""
        if self.is_paused and self.channel:
            self.channel.unpause()
            self.is_paused = False
    
    def stop(self):
        """Stop the audio."""
        if self.channel:
            self.channel.stop()
            self.is_playing = False
            self.is_paused = False
            self.channel = None
    
    def set_volume(self, volume: float):
        """
        Set volume.
        
        Args:
            volume: Volume level (0.0-1.0)
        """
        self.volume = max(0.0, min(1.0, volume))
        if self.channel:
            self.channel.set_volume(self.volume)
    
    def set_loop(self, loop: bool):
        """
        Set looping.
        
        Args:
            loop: Whether to loop
        """
        self.loop = loop
        # If currently playing, need to restart to apply loop change
        if self.is_playing:
            self.play()
    
    def update(self, delta_time: float):
        """
        Update audio source (check if still playing, etc.).
        
        Args:
            delta_time: Time since last frame
        """
        # Check if channel has finished playing
        if self.is_playing and self.channel and not self.channel.get_busy():
            self.is_playing = False
            self.channel = None
    
    def __repr__(self) -> str:
        clip_name = os.path.basename(self.clip.filepath) if self.clip else "None"
        status = "playing" if self.is_playing else ("paused" if self.is_paused else "stopped")
        return f"AudioSource(name='{self.name}', clip='{clip_name}', {status}, vol={self.volume:.2f})"

