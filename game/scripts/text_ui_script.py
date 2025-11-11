"""
Text UI Script
Renders UI text on screen using Text2D.
"""

from src import GameScript, FontLoader
import os


class TextUIScript(GameScript):
    """
    Renders UI text overlays on screen.
    """
    
    def __init__(self, font_path: str = None, font_size: int = 24):
        """
        Initialize TextUIScript.
        
        Args:
            font_path: Path to TTF font file (uses system font if None)
            font_size: Font size in pixels
        """
        super().__init__()
        self.font_path = font_path
        self.font_size = font_size
        self.font = None
        self.app = None
        
    def on_attach(self, entity_or_scene):
        """Called when script is attached."""
        super().on_attach(entity_or_scene)
        
        # Get application instance from scene
        # We'll need to pass it through somehow, for now we'll load font on_start
        print(f"[TextUIScript] Attached (will load font on start)")
    
    def on_start(self):
        """Called before first frame."""
        # Determine font path
        if self.font_path is None:
            # Use Windows default font
            self.font_path = "C:/Windows/Fonts/arial.ttf"
            if not os.path.exists(self.font_path):
                # Try alternative fonts
                for font_name in ["calibri.ttf", "segoeui.ttf", "tahoma.ttf"]:
                    alt_path = f"C:/Windows/Fonts/{font_name}"
                    if os.path.exists(alt_path):
                        self.font_path = alt_path
                        break
        
        # Load font
        print(f"[TextUIScript] Loading font: {self.font_path} (size {self.font_size})")
        self.font = FontLoader.load(self.font_path, self.font_size)
        
        if self.font:
            print(f"[TextUIScript] Font loaded successfully")
            
            # If attached to a splash scene, set the fonts immediately
            if self.scene and hasattr(self.scene, 'set_fonts'):
                print(f"[TextUIScript] Applying font to SplashScene")
                self.scene.set_fonts(self.font, self.font)
        else:
            print(f"[TextUIScript] WARNING: Failed to load font")
    
    def on_update(self, delta_time: float):
        """Called every frame."""
        # Text rendering will be handled externally by accessing this script's font
        pass
    
    def on_detach(self):
        """Called when script is detached."""
        if self.font:
            FontLoader.cleanup_font(self.font)
        print(f"[TextUIScript] Detached")

