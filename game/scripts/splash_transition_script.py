"""
Splash Transition Script
Handles automatic transition from splash scene to main scene.
"""

from engine.src import GameScript
import time


class SplashTransitionScript(GameScript):
    """
    Automatically transitions from splash scene to main scene after a delay.
    """
    
    def __init__(self, duration: float = 3.0, main_scene=None, app=None):
        """
        Initialize splash transition script.
        
        Args:
            duration: How long to show splash in seconds
            main_scene: The main scene to transition to
            app: Application instance for scene switching
        """
        super().__init__()
        self.duration = duration
        self.main_scene = main_scene
        self.app = app
        self.start_time = None
        self.transitioned = False
    
    def on_attach(self, entity_or_scene):
        """Called when script is attached."""
        super().on_attach(entity_or_scene)
        print(f"[SplashTransitionScript] Will transition after {self.duration} seconds")
    
    def on_start(self):
        """Called before first frame."""
        self.start_time = time.time()
        print(f"[SplashTransitionScript] Splash started at {self.start_time}")
    
    def on_update(self, delta_time: float):
        """Called every frame - check if it's time to transition."""
        if self.transitioned or not self.start_time:
            return
        
        elapsed = time.time() - self.start_time
        
        if elapsed >= self.duration:
            print(f"\n[SplashTransitionScript] Transitioning to main scene...")
            if self.app and self.main_scene:
                self.app.set_scene(self.main_scene)
                # Load deferred textures for the main scene
                self.app._load_deferred_textures()
            self.transitioned = True

