"""
Application Module
Main application class that coordinates window and renderer.
"""

import sys
import glfw
import time
from .window import Window
from .input import Input
from ..rendering.renderer import OpenGLRenderer
from ..scene.scene import Scene
from ..ui.text_renderer import TextRenderer
from ..ui.text3d_renderer import Text3DRenderer
from ..audio.audio_manager import AudioManager
from ..audio.audio_listener import AudioListener
from ..systems.settings_manager import SettingsManager
from ..systems.threading_manager import ThreadingManager
from ..systems.asset_loader import AssetLoader


class Application:
    """Main application class that manages the window and renderer."""
    
    def __init__(
        self, 
        width: int = None,  # None = use settings
        height: int = None,  # None = use settings
        title: str = None,  # None = use settings
        enable_validation: bool = False,
        app_name: str = "game_engine"
    ):
        """
        Initialize the Application.
        
        Args:
            width: Window width (None = use settings)
            height: Window height (None = use settings)
            title: Window title (None = use settings)
            enable_validation: Enable OpenGL debug output
            app_name: Application name for settings
        """
        # Initialize settings FIRST
        self.settings = SettingsManager(app_name=app_name)
        
        # Use settings if not provided
        self.width = width or self.settings.get('window.width')
        self.height = height or self.settings.get('window.height')
        self.title = title or self.settings.get('window.title')
        self.enable_validation = enable_validation or self.settings.get('engine.debug_mode')
        
        # Initialize threading system
        num_workers = self.settings.get('performance.worker_threads')
        threading_enabled = self.settings.get('performance.multithreading')
        self.threading_manager = ThreadingManager(num_workers, threading_enabled)
        
        # Initialize asset loader
        self.asset_loader = AssetLoader(
            self.threading_manager,
            enable_cache=True
        )
        
        # Components
        self.window: Window = None
        self.renderer: OpenGLRenderer = None
        self.input: Input = None
        self.text_renderer: TextRenderer = None
        self.text3d_renderer = None
        self.audio_manager = None
        self.ui_renderer = None  # ModernUIRenderer for OpenGL-based UI
        
        # State
        self.is_running = False
        self.framebuffer_resized = False
        self._ui_text_callback = None
        
        print(f"[Application] Using settings from: {self.settings.user_file}")
        print(f"[Application] Multithreading: {threading_enabled} ({num_workers} workers)")
    
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
        
        # Apply window settings
        vsync = self.settings.get('window.vsync')
        if vsync:
            glfw.swap_interval(1)  # Enable VSync
            print("[OK] VSync enabled")
        else:
            glfw.swap_interval(0)  # Disable VSync
            print("[OK] VSync disabled")
        
        # Create input manager
        self.input = Input(self.window.window)
        
        # Set up window callbacks
        self.window.set_resize_callback(self._on_framebuffer_resize)
        self.window.set_mouse_callback(self._on_mouse_move)
        self.window.set_scroll_callback(self._on_mouse_scroll)
        self.window.set_mouse_button_callback(self._on_mouse_button)
        
        # Create and initialize renderer (pass settings)
        self.renderer = OpenGLRenderer(
            app_name=self.title,
            enable_validation=self.enable_validation,
            settings=self.settings  # Pass settings to renderer
        )
        if not self.renderer.init(self.window):
            print("ERROR: Failed to initialize renderer")
            return False
        
        # Initialize Text Renderer (2D)
        self.text_renderer = TextRenderer()
        if not self.text_renderer.init(self.width, self.height):
            print("ERROR: Failed to initialize TextRenderer")
            return False
        
        # Initialize Modern UI Renderer
        from ..ui.modern_ui_renderer import ModernUIRenderer
        self.ui_renderer = ModernUIRenderer()
        if not self.ui_renderer.init(self.width, self.height):
            print("ERROR: Failed to initialize ModernUIRenderer")
            return False
        
        # Initialize Text3D Renderer
        self.text3d_renderer = Text3DRenderer()
        if not self.text3d_renderer.init():
            print("ERROR: Failed to initialize Text3DRenderer")
            return False
        
        # Initialize Audio Manager
        self.audio_manager = AudioManager()
        if not self.audio_manager.initialized:
            print("WARNING: Failed to initialize Audio Manager - audio will be disabled")
        else:
            # Apply audio settings
            self.audio_manager.set_master_volume(self.settings.get('audio.master_volume'))
            print(f"[OK] Audio master volume set to {self.settings.get('audio.master_volume')}")
        
        # Create audio listener (will be attached to active camera)
        self.audio_listener = AudioListener()
        if self.audio_manager.initialized:
            self.audio_manager.set_listener(self.audio_listener)
        
        # Note: Textures will be loaded after scene is set in run()
        
        print("=" * 60)
        print("Initialization complete!")
        print("=" * 60)
        
        # Register settings callbacks for live updates
        self._register_settings_callbacks()
        
        return True
    
    def _register_settings_callbacks(self):
        """Register callbacks for settings changes."""
        if not self.settings:
            return
        
        # VSync callback
        def on_vsync_change(new_value, old_value):
            import glfw
            glfw.swap_interval(1 if new_value else 0)
            print(f"[Settings] VSync changed: {old_value} -> {new_value}")
        
        self.settings.register_callback('window.vsync', on_vsync_change)
        
        # Audio volume callback
        def on_volume_change(new_value, old_value):
            if self.audio_manager and self.audio_manager.initialized:
                self.audio_manager.set_master_volume(new_value)
                print(f"[Settings] Master volume changed: {old_value} -> {new_value}")
        
        self.settings.register_callback('audio.master_volume', on_volume_change)
        
        # Shadow quality callback
        def on_shadow_quality_change(new_value, old_value):
            if self.renderer:
                self.renderer.apply_settings()
                print(f"[Settings] Shadow quality changed: {old_value} -> {new_value}")
        
        self.settings.register_callback('graphics.shadow_map_size', on_shadow_quality_change)
        self.settings.register_callback('graphics.shadows_enabled', on_shadow_quality_change)
        
        print("[Application] Settings callbacks registered (live updates enabled)")
    
    def _load_deferred_textures(self):
        """Load textures for objects after OpenGL context is created."""
        if not self.renderer or not self.renderer.scene:
            return
        
        from ..graphics.texture import Texture
        print("\n[TEXTURE LOADING] Loading deferred textures...")
        
        for game_object in self.renderer.scene.game_objects:
            # Load diffuse texture
            if hasattr(game_object, '_texture_path') and game_object._texture_path:
                texture_path = game_object._texture_path
                print(f"[TEXTURE LOADING] Loading diffuse texture for '{game_object.name}': {texture_path}")
                
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
            
            # Load normal map
            if hasattr(game_object, '_normal_map_path') and game_object._normal_map_path:
                normal_map_path = game_object._normal_map_path
                print(f"[TEXTURE LOADING] Loading normal map for '{game_object.name}': {normal_map_path}")
                
                try:
                    normal_map = Texture(normal_map_path)
                    print(f"[TEXTURE LOADING] [OK] Loaded normal map: ID={normal_map.texture_id}")
                    
                    # Apply normal map to material
                    if game_object.material:
                        game_object.material.set_normal_map(normal_map)
                        print(f"[TEXTURE LOADING] Applied normal map to material")
                    
                    # Clear the deferred normal map path
                    del game_object._normal_map_path
                    
                except Exception as e:
                    print(f"[TEXTURE LOADING] [ERROR] Failed to load normal map: {e}")
            
            # Load roughness map
            if hasattr(game_object, '_roughness_map_path') and game_object._roughness_map_path:
                roughness_map_path = game_object._roughness_map_path
                print(f"[TEXTURE LOADING] Loading roughness map for '{game_object.name}': {roughness_map_path}")
                
                try:
                    roughness_map = Texture(roughness_map_path)
                    print(f"[TEXTURE LOADING] [OK] Loaded roughness map: ID={roughness_map.texture_id}")
                    
                    # Apply roughness map to material
                    if game_object.material:
                        game_object.material.set_roughness_map(roughness_map)
                        print(f"[TEXTURE LOADING] Applied roughness map to material")
                    
                    # Clear the deferred roughness map path
                    del game_object._roughness_map_path
                    
                except Exception as e:
                    print(f"[TEXTURE LOADING] [ERROR] Failed to load roughness map: {e}")
            
            # Load AO map
            if hasattr(game_object, '_ao_map_path') and game_object._ao_map_path:
                ao_map_path = game_object._ao_map_path
                print(f"[TEXTURE LOADING] Loading AO map for '{game_object.name}': {ao_map_path}")
                
                try:
                    ao_map = Texture(ao_map_path)
                    print(f"[TEXTURE LOADING] [OK] Loaded AO map: ID={ao_map.texture_id}")
                    
                    # Apply AO map to material
                    if game_object.material:
                        game_object.material.set_ao_map(ao_map)
                        print(f"[TEXTURE LOADING] Applied AO map to material")
                    
                    # Clear the deferred AO map path
                    del game_object._ao_map_path
                    
                except Exception as e:
                    print(f"[TEXTURE LOADING] [ERROR] Failed to load AO map: {e}")
        
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
        if self.ui_renderer:
            self.ui_renderer.set_projection(width, height)
    
    def _on_mouse_move(self, xpos: float, ypos: float):
        """Handle mouse movement."""
        if self.input:
            self.input.update_mouse_position(xpos, ypos)
        
        # Forward to current scene
        if self.renderer and self.renderer.scene:
            if hasattr(self.renderer.scene, 'on_mouse_move'):
                self.renderer.scene.on_mouse_move(xpos, ypos)
    
    def _on_mouse_scroll(self, xoffset: float, yoffset: float):
        """Handle mouse scroll."""
        if self.input:
            self.input.update_scroll(xoffset, yoffset)
    
    def _on_mouse_button(self, button: int, action: int, mods: int, xpos: float, ypos: float):
        """Handle mouse button events."""
        # Forward to current scene
        if self.renderer and self.renderer.scene:
            if action == glfw.PRESS:
                if hasattr(self.renderer.scene, 'on_mouse_click'):
                    self.renderer.scene.on_mouse_click(xpos, ypos, button)
            elif action == glfw.RELEASE:
                if hasattr(self.renderer.scene, 'on_mouse_release'):
                    self.renderer.scene.on_mouse_release(xpos, ypos, button)
    
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
            
            # Start audio sources that have play_on_start enabled
            if self.audio_manager and self.audio_manager.initialized:
                for audio_source in scene.audio_sources:
                    if audio_source.play_on_start:
                        audio_source.play()
                        print(f"[AUDIO] Auto-playing: {audio_source.name}")
        
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
        p_pressed = False
        
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
                
                # Toggle settings menu with P key
                p_current = self.input.keyboard.is_key_pressed(glfw.KEY_P)
                if p_current and not p_pressed:
                    if hasattr(self, '_settings_menu_scene') and hasattr(self, '_main_scene'):
                        current_scene = self.renderer.scene if self.renderer else None
                        if current_scene == self._settings_menu_scene:
                            # Return to main scene
                            print("Closing settings menu...")
                            self.renderer.set_scene(self._main_scene)
                        else:
                            # Open settings menu
                            print("Opening settings menu...")
                            # Initialize UI if not already done
                            if not self._settings_menu_scene._initialized:
                                self._settings_menu_scene.initialize_ui(self.width, self.height)
                                self._settings_menu_scene._initialized = True
                            self.renderer.set_scene(self._settings_menu_scene)
                p_pressed = p_current
                
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
                    
                    # Update audio listener to match active camera
                    active_camera = self.renderer.scene.get_active_camera()
                    if active_camera and self.audio_listener:
                        self.audio_listener.attach_to_camera(active_camera)
                    
                    # Update all audio sources
                    if self.audio_manager and self.audio_manager.initialized:
                        audio_sources = self.renderer.scene.get_active_audio_sources()
                        self.audio_manager.update_audio_sources(audio_sources, delta_time)
                
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
        
        # Render 3D text in world space
        if self.text3d_renderer and self.renderer and self.renderer.scene:
            scene = self.renderer.scene
            active_camera = scene.get_active_camera()
            
            if active_camera and len(scene.text3d_objects) > 0:
                view_matrix = active_camera.get_view_matrix()
                projection_matrix = active_camera.get_projection_matrix()
                
                active_text3d = scene.get_active_text3d()
                self.text3d_renderer.render_text_objects(
                    active_text3d,
                    view_matrix,
                    projection_matrix
                )
        
        # Render additional UI text overlays after 3D rendering
        # IMPORTANT: Call callback FIRST to set fonts before rendering!
        if self.text_renderer and hasattr(self, '_ui_text_callback') and self._ui_text_callback:
            self._ui_text_callback(self.text_renderer)
        
        # Render 2D text entities from scene (if any)
        if self.text_renderer and self.renderer and self.renderer.scene:
            scene = self.renderer.scene
            
            # Check if scene has a render_ui method (new UI system)
            if hasattr(scene, 'render_ui'):
                scene.render_ui(self.text_renderer)
            # Fallback: Check if scene has text entities (legacy SplashScene)
            elif hasattr(scene, 'get_text_entities'):
                text_entities = scene.get_text_entities()
                self.text_renderer.render_text_objects(text_entities)
        
        # Swap buffers AFTER all rendering (3D + text) is complete
        if self.window:
            self.window.swap_buffers()
    
    def cleanup(self):
        """Clean up all application resources."""
        print("\n" + "=" * 60)
        print("Cleaning up application resources")
        print("=" * 60)
        
        # Clean up asset loader (wait for pending loads)
        if hasattr(self, 'asset_loader') and self.asset_loader:
            self.asset_loader.cleanup()
        
        # Clean up threading (wait for tasks)
        if hasattr(self, 'threading_manager') and self.threading_manager:
            self.threading_manager.shutdown(wait=True)
        
        if self.renderer:
            self.renderer.cleanup()
        
        if self.text_renderer:
            self.text_renderer.cleanup()
        
        if self.text3d_renderer:
            self.text3d_renderer.cleanup()
        
        if self.ui_renderer:
            self.ui_renderer.cleanup()
        
        if self.audio_manager:
            self.audio_manager.cleanup()
        
        if self.window:
            self.window.cleanup()
        
        # Save settings on exit
        if hasattr(self, 'settings') and self.settings:
            self.settings.save()
        
        print("=" * 60)
        print("Cleanup complete - goodbye!")
        print("=" * 60)
