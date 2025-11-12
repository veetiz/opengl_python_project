"""
Audio2D Module
Non-positional audio source (background music, UI sounds).
"""

from typing import Optional
from .audio_source import AudioSource
from .audio_clip import AudioClip


class Audio2D(AudioSource):
    """
    2D Audio Source - non-positional audio.
    Perfect for background music, UI sounds, narration.
    Volume is constant regardless of listener position.
    """
    
    def __init__(
        self,
        name: str = "Audio2D",
        clip: Optional[AudioClip] = None,
        volume: float = 1.0,
        loop: bool = False,
        play_on_start: bool = False,
        auto_play: bool = False,
        category: str = "sfx"  # "music", "sfx", "voice"
    ):
        """
        Initialize 2D audio source.
        
        Args:
            name: Source name
            clip: Audio clip to play
            volume: Volume level (0.0-1.0)
            loop: Whether to loop the audio
            play_on_start: Play when scene starts
            auto_play: Play immediately when clip is set
            category: Audio category for mixing ("music", "sfx", "voice")
        """
        super().__init__(name, clip, volume, loop, play_on_start, auto_play)
        self.category = category
    
    def update(self, delta_time: float):
        """
        Update audio source.
        
        Args:
            delta_time: Time since last frame
        """
        super().update(delta_time)
        
        # 2D audio doesn't need positional updates
        # Volume stays constant
    
    def __repr__(self) -> str:
        clip_name = self.clip.filepath if self.clip else "None"
        status = "playing" if self.is_playing else ("paused" if self.is_paused else "stopped")
        return f"Audio2D('{self.name}', category='{self.category}', {status}, vol={self.volume:.2f})"

