"""
AudioManager Module
Manages audio initialization, mixing, and global volume control.
"""

import pygame
from typing import Dict, List, Optional
from .audio_listener import AudioListener
from .audio2d import Audio2D
from .audio3d import Audio3D


class AudioManager:
    """
    Audio Manager - handles audio system initialization and mixing.
    Manages volume levels for different categories (music, sfx, voice).
    """
    
    def __init__(
        self,
        frequency: int = 44100,
        size: int = -16,
        channels: int = 2,
        buffer: int = 512,
        max_channels: int = 32
    ):
        """
        Initialize audio manager.
        
        Args:
            frequency: Audio frequency (Hz)
            size: Audio bit depth
            channels: Number of audio channels (1=mono, 2=stereo)
            buffer: Audio buffer size (smaller = lower latency, higher CPU)
            max_channels: Maximum simultaneous sounds
        """
        self.frequency = frequency
        self.size = size
        self.channels = channels
        self.buffer = buffer
        self.max_channels = max_channels
        
        self.initialized = False
        self.listener: Optional[AudioListener] = None
        
        # Volume controls per category
        self.master_volume = 1.0
        self.music_volume = 0.7
        self.sfx_volume = 1.0
        self.voice_volume = 1.0
        
        self._init_audio()
    
    def _init_audio(self) -> bool:
        """Initialize pygame mixer."""
        try:
            # Prevent pygame from creating a video window
            import os
            os.environ['SDL_VIDEODRIVER'] = 'dummy'
            
            # Initialize pygame mixer (audio only)
            pygame.mixer.init(
                frequency=self.frequency,
                size=self.size,
                channels=self.channels,
                buffer=self.buffer
            )
            
            # Set maximum number of simultaneous sounds
            pygame.mixer.set_num_channels(self.max_channels)
            
            self.initialized = True
            print(f"[AUDIO] Audio system initialized: {self.frequency}Hz, {self.channels} channels, {self.max_channels} max sounds")
            return True
            
        except Exception as e:
            print(f"[AUDIO] ERROR: Failed to initialize audio: {e}")
            return False
    
    def set_listener(self, listener: AudioListener):
        """
        Set the active audio listener.
        
        Args:
            listener: Audio listener (usually attached to camera)
        """
        self.listener = listener
        print(f"[AUDIO] Listener set: {listener}")
    
    def update_audio_sources(self, audio_sources: List, delta_time: float):
        """
        Update all audio sources (handle 3D positioning, etc.).
        
        Args:
            audio_sources: List of AudioSource objects (Audio2D and Audio3D)
            delta_time: Time since last frame
        """
        if not self.initialized:
            return
        
        # Get listener position if available
        listener_pos = None
        if self.listener:
            self.listener.update()
            listener_pos = self.listener.position
        
        # Update each audio source
        for source in audio_sources:
            if not source.active:
                continue
            
            # Update based on type
            if isinstance(source, Audio3D):
                # 3D audio - update with listener position for distance calculations
                source.update(delta_time, listener_pos)
                
                # Apply stereo panning based on position relative to listener
                if source.is_playing and source.channel and listener_pos is not None and self.listener:
                    # Get listener right vector for stereo panning
                    listener_right = self.listener.right
                    
                    # Calculate left and right channel volumes
                    left_vol, right_vol = source.calculate_volume_and_pan(listener_pos, listener_right)
                    
                    # Apply category and master volume
                    category_vol = self._get_category_volume(source.category)
                    left_vol = left_vol * category_vol * self.master_volume
                    right_vol = right_vol * category_vol * self.master_volume
                    
                    # Set stereo volumes (left, right)
                    # Note: pygame Channel.set_volume() only sets mono volume
                    # For true stereo panning, we need to use pygame.mixer.Channel.set_volume(left, right)
                    # But pygame doesn't support per-channel volume easily, so we approximate with mono
                    average_vol = (left_vol + right_vol) / 2.0
                    source.channel.set_volume(average_vol)
                    
                    # TODO: Implement true stereo panning using custom audio processing
                    # For now, we have distance-based volume working
                    
            elif isinstance(source, Audio2D):
                # 2D audio - simple update
                source.update(delta_time)
                
                # Apply category volume
                if source.is_playing and source.channel:
                    category_vol = self._get_category_volume(source.category)
                    source.channel.set_volume(source.volume * category_vol * self.master_volume)
    
    def _get_category_volume(self, category: str) -> float:
        """Get volume multiplier for a category."""
        if category == "music":
            return self.music_volume
        elif category == "voice":
            return self.voice_volume
        else:  # "sfx" or unknown
            return self.sfx_volume
    
    def set_master_volume(self, volume: float):
        """Set master volume (affects all audio)."""
        self.master_volume = max(0.0, min(1.0, volume))
    
    def set_music_volume(self, volume: float):
        """Set music volume."""
        self.music_volume = max(0.0, min(1.0, volume))
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume."""
        self.sfx_volume = max(0.0, min(1.0, volume))
    
    def set_voice_volume(self, volume: float):
        """Set voice volume."""
        self.voice_volume = max(0.0, min(1.0, volume))
    
    def pause_all(self):
        """Pause all currently playing audio."""
        pygame.mixer.pause()
    
    def unpause_all(self):
        """Resume all paused audio."""
        pygame.mixer.unpause()
    
    def stop_all(self):
        """Stop all currently playing audio."""
        pygame.mixer.stop()
    
    def cleanup(self):
        """Clean up audio system."""
        if self.initialized:
            pygame.mixer.quit()
            self.initialized = False
            print("[AUDIO] Audio system cleaned up")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except:
            pass

