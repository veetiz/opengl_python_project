"""
Application Module
Main application class that coordinates window and renderer.
"""

import sys
import glfw
import time
from .window import Window
from .renderer import OpenGLRenderer
from .scene import Scene
from .input import Input
from .text_renderer import TextRenderer


class Application:
    """Main application class that manages the window and renderer."""
    
    def __init__(
        self, 
        width: int = 800, 
        height: int = 600,
        title: str = "OpenGL Application",
        enable_validation: bool = False
    ):
        """
        Initialize the Application.
        
        Args:
            width: Window width in pixels
            height: Window height in pixels
            title: Window title
            enable_validation: Enable OpenGL debug output
        """
        self.width = width
        self.height = height
        self.title = title
        self.enable_validation = enable_validation
        
        # Components
        self.window: Window = None
        self.renderer: OpenGLRenderer = None
        self.input: Input = None
        self.text_renderer: TextRenderer = None
        
        # State
        self.is_running = False
        self.framebuffer_resized = False
        self._ui_text_callback = None
    
    def init(self) -> bool:
        """
        Initialize all application components.
        
        Returns:
            True if successful, False otherwise
        """
        print("=" * 60)
        print("Initializing OpenGL Application")
        print("=" * 60)
        
        # Create and initialize window
        self.window = Window(self.width, self.height, self.title)
        if not self.window.init():
            print("ERROR: Failed to initialize window")
            return False
        
        # Create input manager
        self.input = Input(self.window.window)
        
        # Set up window callbacks
        self.window.set_resize_callback(self._on_framebuffer_resize)
        self.window.set_mouse_callback(self._on_mouse_move)
        self.window.set_scroll_callback(self._on_mouse_scroll)
        
        # Create and initialize renderer
        self.renderer = OpenGLRenderer(
            app_name=self.title,
            enable_validation=self.enable_validation
        )
        if not self.renderer.init(self.window):
            print("ERROR: Failed to initialize renderer")
            return False
        
        # Initialize Text Renderer
        self.text_renderer = TextRenderer()
        if not self.text_renderer.init(self.width, self.height):
            print("ERROR: Failed to initialize TextRenderer")
            return False
        
        # Note: Textures will be loaded after scene is set in run()
        
        print("=" * 60)
        print("Initialization complete!")
        print("=" * 60)
        return True
    
    def _load_deferred_textures(self):
        """Load textures for objects after OpenGL context is created."""
        if not self.renderer or not self.renderer.scene:
            return
        
        from src import Texture
        print("\n[TEXTURE LOADING] Loading deferred textures...")
        
        for game_object in self.renderer.scene.game_objects:
            if hasattr(game_object, '_texture_path') and game_object._texture_path:
                texture_path = game_object._texture_path
                print(f"[TEXTURE LOADING] Loading texture for '{game_object.name}': {texture_path}")
                
                try:
                    texture = Texture(texture_path)
                    print(f"[TEXTURE LOADING] [OK] Loaded: ID={texture.texture_id}, Size={texture.width}x{texture.height}")
                    
                    # Apply texture to all meshes in the object's model
                    if game_object.model:
                        for mesh in game_object.model.meshes:
                            mesh.texture = texture
                        print(f"[TEXTURE LOADING] Applied texture to {len(game_object.model.meshes)} mesh(es)")
                    
                    # Clear the deferred texture path
                    del game_object._texture_path
                    
                except Exception as e:
                    print(f"[TEXTURE LOADING] [ERROR] Failed to load texture: {e}")
        
        print("[TEXTURE LOADING] Texture loading complete\n")
    
    def set_scene(self, scene: Scene):
        """
        Set the scene to be rendered.
        
        Args:
            scene: Scene containing game objects
        """
        if self.renderer:
            self.renderer.set_scene(scene)
        
        # Update screen size for splash scenes
        if hasattr(scene, 'set_screen_size'):
            scene.set_screen_size(self.width, self.height)
    
    def set_ui_text_callback(self, callback):
        """
        Set a callback function for rendering UI text.
        
        The callback should accept a TextRenderer instance as parameter.
        Example: lambda text_renderer: text_renderer.render_text(font, "Hello", 10, 10)
        
        Args:
            callback: Function that takes TextRenderer as parameter
        """
        self._ui_text_callback = callback
    
    def _on_framebuffer_resize(self, width: int, height: int):
        """Handle framebuffer resize events."""
        self.framebuffer_resized = True
        self.width = width
        self.height = height
        if self.renderer:
            self.renderer.on_resize(width, height)
        if self.text_renderer:
            self.text_renderer.set_projection(width, height)
    
    def _on_mouse_move(self, xpos: float, ypos: float):
        """Handle mouse movement."""
        if self.input:
            self.input.update_mouse_position(xpos, ypos)
    
    def _on_mouse_scroll(self, xoffset: float, yoffset: float):
        """Handle mouse scroll."""
        if self.input:
            self.input.update_scroll(xoffset, yoffset)
    
    def run(self, scene: Scene = None) -> int:
        """
        Run the main application loop.
        
        Args:
            scene: Optional scene to set before running
        
        Returns:
            Exit code (0 for success, 1 for error)
        """
        if not self.init():
            self.cleanup()
            return 1
        
        # Set the scene if provided
        if scene:
            self.set_scene(scene)
        
        # Now that scene is set AND OpenGL context exists, load textures
        self._load_deferred_textures()
        
        # Start all scripts before main loop so fonts are loaded
        if scene:
            print("\n[APP] Starting scene scripts before main loop...")
            scene.update_scripts(0.0)  # Call with delta_time=0 to trigger on_start
        
        self.is_running = True
        self._main_loop()
        self.cleanup()
        
        return 0
    
    def _main_loop(self):
        """Main application loop."""
        print("\nEntering main loop...")
        print("Controls:")
        print("  - WASD: Move camera (forward/back/left/right)")
        print("  - Q/E: Move camera (down/up)")
        print("  - Arrow Keys: Rotate camera")
        print("  - TAB: Toggle mouse capture for rotation")
        print("  - Mouse Scroll: Zoom in/out")
        print("  - C: Switch to next camera")
        print("  - ESC: Exit application")
        print("-" * 60)
        
        frame_count = 0
        last_time = time.time()
        tab_pressed = False
        c_pressed = False
        
        try:
            while self.is_running and not self.window.should_close():
                # Calculate delta time
                current_time = time.time()
                delta_time = current_time - last_time
                last_time = current_time
                
                # Reset per-frame input
                self.input.reset_per_frame()
                
                # Poll events
                self.window.poll_events()
                
                # === INPUT HANDLING ===
                
                # Check for ESC key
                if self.input.keyboard.is_key_pressed(glfw.KEY_ESCAPE):
                    print("\nESC pressed - exiting...")
                    self.is_running = False
                    break
                
                # Toggle mouse capture with TAB
                tab_current = self.input.keyboard.is_key_pressed(glfw.KEY_TAB)
                if tab_current and not tab_pressed:
                    self.input.mouse.captured = not self.input.mouse.captured
                    self.window.capture_mouse(self.input.mouse.captured)
                    status = "enabled" if self.input.mouse.captured else "disabled"
                    print(f"Mouse look {status}")
                tab_pressed = tab_current
                
                # Switch camera with C key
                c_current = self.input.keyboard.is_key_pressed(glfw.KEY_C)
                if c_current and not c_pressed:
                    if self.renderer and self.renderer.scene:
                        scene = self.renderer.scene
                        if scene.camera_count > 1:
                            # Switch to next camera
                            next_index = (scene.active_camera_index + 1) % scene.camera_count
                            scene.set_active_camera(next_index)
                            active_cam = scene.get_active_camera()
                            cam_name = active_cam.name if active_cam else "Unknown"
                            print(f"Switched to camera {next_index}: '{cam_name}'")
                c_pressed = c_current
                
                # === UPDATE SCRIPTS ===
                # Pass input reference to all scripts and update them
                if self.renderer and self.renderer.scene:
                    # Set input reference for all entity scripts
                    for entity in self.renderer.scene.get_all_entities():
                        for script in entity.scripts:
                            if hasattr(script, 'input'):
                                script.input = self.input
                    
                    # Set input reference for global scripts
                    for script in self.renderer.scene.scripts:
                        if hasattr(script, 'input'):
                            script.input = self.input
                    
                    # Update all scripts (handles camera movement via CameraMovementScript)
                    self.renderer.scene.update_scripts(delta_time)
                
                # Render frame
                self._render_frame()
                
                frame_count += 1
                
                # Debug: print progress and FPS
                if frame_count % 120 == 0:
                    fps = 1.0 / delta_time if delta_time > 0 else 0
                    print(f"[INFO] Frames: {frame_count}, FPS: {fps:.1f}")
                    
        except Exception as e:
            import traceback
            print(f"\n[ERROR] Exception in main loop: {e}")
            traceback.print_exc()
        
        print(f"\nMain loop exited after {frame_count} frames")
    
    def _render_frame(self):
        """Render a single frame."""
        # Render 3D scene
        self.renderer.render_frame()
        
        # Render text entities from scene (if any)
        if self.text_renderer and self.renderer and self.renderer.scene:
            scene = self.renderer.scene
            # Check if scene has text entities (like SplashScene)
            if hasattr(scene, 'get_text_entities'):
                text_entities = scene.get_text_entities()
                self.text_renderer.render_text_objects(text_entities)
        
        # Render additional UI text overlays after 3D rendering
        if self.text_renderer and hasattr(self, '_ui_text_callback') and self._ui_text_callback:
            self._ui_text_callback(self.text_renderer)
        
        # Swap buffers AFTER all rendering (3D + text) is complete
        if self.window:
            self.window.swap_buffers()
    
    def cleanup(self):
        """Clean up all application resources."""
        print("\n" + "=" * 60)
        print("Cleaning up application resources")
        print("=" * 60)
        
        if self.renderer:
            self.renderer.cleanup()
        
        if self.text_renderer:
            self.text_renderer.cleanup()
        
        if self.window:
            self.window.cleanup()
        
        print("=" * 60)
        print("Cleanup complete - goodbye!")
        print("=" * 60)
