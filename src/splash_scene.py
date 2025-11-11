"""
Splash Scene Module
A scene for showing splash screens with centered text.
"""

from typing import Optional
from .scene import Scene
from .text2d import Text2D
from .font import Font


class SplashScene(Scene):
    """
    Splash screen scene with centered title and loading text.
    Inherits from Scene to leverage entity management.
    """
    
    def __init__(self, name: str = "Splash", title_font: Optional[Font] = None, loading_font: Optional[Font] = None):
        """
        Initialize splash scene.
        
        Args:
            name: Scene name
            title_font: Font for title text (can be set later)
            loading_font: Font for loading text (can be set later)
        """
        super().__init__(name)
        
        # Text entities
        self.title_text: Optional[Text2D] = None
        self.loading_text: Optional[Text2D] = None
        
        # Store fonts
        self.title_font = title_font
        self.loading_font = loading_font
        
        # Screen dimensions (will be updated)
        self.screen_width = 800
        self.screen_height = 600
        
        # Create text entities (positions will be updated when screen size is known)
        self._create_text_entities()
    
    def _create_text_entities(self):
        """Create the title and loading text entities."""
        # Title text (will be centered)
        self.title_text = Text2D(
            label="SplashTitle",
            text="OpenGL Game Engine",
            font=self.title_font,
            x=0,
            y=0,
            size=64,
            scale=1.0,
            color=(1.0, 1.0, 1.0),
            visible=True
        )
        
        # Loading text (below title)
        self.loading_text = Text2D(
            label="LoadingText",
            text="Loading...",
            font=self.loading_font,
            x=0,
            y=0,
            size=32,
            scale=0.8,
            color=(0.7, 0.7, 0.7),
            visible=True
        )
    
    def set_screen_size(self, width: int, height: int):
        """
        Update screen size and recalculate centered positions.
        
        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        self.screen_width = width
        self.screen_height = height
        self._update_text_positions()
    
    def _update_text_positions(self):
        """Calculate and update centered text positions."""
        if not self.title_text or not self.loading_text:
            return
        
        # Center title text
        if self.title_text.font:
            title_width = self.title_text.get_width()
            self.title_text.x = (self.screen_width - title_width) / 2
            self.title_text.y = self.screen_height / 2 - 50
        else:
            # Approximate centering if font not loaded yet
            self.title_text.x = self.screen_width / 2 - 200
            self.title_text.y = self.screen_height / 2 - 50
        
        # Center loading text (below title)
        if self.loading_text.font:
            loading_width = self.loading_text.get_width()
            self.loading_text.x = (self.screen_width - loading_width) / 2
            self.loading_text.y = self.screen_height / 2 + 20
        else:
            # Approximate centering if font not loaded yet
            self.loading_text.x = self.screen_width / 2 - 80
            self.loading_text.y = self.screen_height / 2 + 20
    
    def set_fonts(self, title_font: Font, loading_font: Optional[Font] = None):
        """
        Set fonts for the text elements.
        
        Args:
            title_font: Font for title
            loading_font: Font for loading text (uses title_font if None)
        """
        self.title_font = title_font
        self.loading_font = loading_font if loading_font else title_font
        
        if self.title_text:
            self.title_text.set_font(self.title_font)
        
        if self.loading_text:
            self.loading_text.set_font(self.loading_font)
        
        # Recalculate positions now that we have fonts
        self._update_text_positions()
    
    def set_title(self, title: str):
        """
        Update the title text.
        
        Args:
            title: New title text
        """
        if self.title_text:
            self.title_text.set_text(title)
            self._update_text_positions()  # Recenter
    
    def set_title_simple(self, title: str):
        """
        Update title without recentering (for testing).
        
        Args:
            title: New title text
        """
        if self.title_text:
            self.title_text.set_text(title)
    
    def set_loading_text(self, text: str):
        """
        Update the loading text.
        
        Args:
            text: New loading text
        """
        if self.loading_text:
            self.loading_text.set_text(text)
            self._update_text_positions()  # Recenter
    
    def get_text_entities(self) -> list:
        """
        Get all text entities in this splash scene.
        
        Returns:
            List of Text2D entities
        """
        texts = []
        if self.title_text:
            texts.append(self.title_text)
        if self.loading_text:
            texts.append(self.loading_text)
        return texts

