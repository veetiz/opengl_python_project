"""
Render Pipeline
Orchestrates all rendering stages and manages renderer components.
"""

from typing import Optional, Callable, Dict, Any
from OpenGL.GL import glDisable, glEnable, glIsEnabled, GL_CULL_FACE
import numpy as np


class RenderPipeline:
    """
    Manages and executes the rendering pipeline.
    Coordinates all renderer components in the correct order.
    """
    
    def __init__(self):
        """Initialize the render pipeline."""
        # Core renderers
        self.scene_renderer = None      # OpenGLRenderer (3D scene)
        self.text3d_renderer = None     # Text3DRenderer (3D text in world)
        self.text2d_renderer = None     # TextRenderer (2D UI text overlay)
        self.ui_renderer = None         # UIRenderer (Modern UI components)
        
        # Callbacks
        self.ui_text_callback: Optional[Callable] = None
        
        # State
        self.initialized = False
        
    def register_scene_renderer(self, renderer):
        """Register the main 3D scene renderer."""
        self.scene_renderer = renderer
        print("[RenderPipeline] Scene renderer registered")
        
    def register_text3d_renderer(self, renderer):
        """Register the 3D text renderer."""
        self.text3d_renderer = renderer
        print("[RenderPipeline] 3D text renderer registered")
        
    def register_text2d_renderer(self, renderer):
        """Register the 2D text renderer."""
        self.text2d_renderer = renderer
        print("[RenderPipeline] 2D text renderer registered")
        
    def register_ui_renderer(self, renderer):
        """Register the UI renderer."""
        self.ui_renderer = renderer
        print("[RenderPipeline] UI renderer registered")
        
    def set_ui_text_callback(self, callback: Callable):
        """Set callback for UI text setup (e.g., font loading)."""
        self.ui_text_callback = callback
        
    def init(self) -> bool:
        """Initialize the pipeline."""
        if not self.scene_renderer:
            print("[RenderPipeline] ERROR: No scene renderer registered")
            return False
        
        self.initialized = True
        print("[RenderPipeline] Initialized successfully")
        return True
    
    def render(self):
        """
        Execute the complete rendering pipeline.
        
        Rendering order:
        1. 3D Scene (geometry, shadows, lighting)
        2. 3D Text (world-space text)
        3. Particles (3D particles with billboarding)
        4. 2D UI Text (overlays)
        5. UI Elements (buttons, sliders, etc.)
        """
        if not self.initialized or not self.scene_renderer:
            return
        
        # === STAGE 1: Render 3D Scene ===
        self.scene_renderer.render_frame()
        
        # === STAGE 2: Render 3D Text (world space) ===
        self._render_3d_text()
        
        # === STAGE 3: Render Particles ===
        self._render_particles()
        
        # === STAGE 4: Render 2D Text and UI ===
        self._render_2d_ui()
    
    def _render_3d_text(self):
        """Render 3D text objects in world space."""
        if not self.text3d_renderer or not self.scene_renderer or not self.scene_renderer.scene:
            return
        
        scene = self.scene_renderer.scene
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
    
    def _render_particles(self):
        """Render particle systems."""
        if not self.scene_renderer or not self.scene_renderer.scene:
            return
        
        scene = self.scene_renderer.scene
        
        # Check if scene has a particle system
        if hasattr(scene, 'particle_system') and scene.particle_system:
            active_camera = scene.get_active_camera()
            if active_camera:
                view_matrix = active_camera.get_view_matrix()
                projection_matrix = active_camera.get_projection_matrix()
                scene.particle_system.render(view_matrix, projection_matrix)
    
    def _render_2d_ui(self):
        """Render 2D UI elements and text overlays."""
        if not self.text2d_renderer or not self.scene_renderer or not self.scene_renderer.scene:
            return
        
        scene = self.scene_renderer.scene
        
        # IMPORTANT: Call UI text callback FIRST to set fonts before rendering
        if self.ui_text_callback:
            self.ui_text_callback(self.text2d_renderer)
        
        # CRITICAL: Disable culling before UI rendering
        # 3D rendering may have enabled it, but UI should never be culled
        cull_state_before = glIsEnabled(GL_CULL_FACE)
        glDisable(GL_CULL_FACE)
        
        # Render 2D text overlay objects (if any)
        if hasattr(scene, 'text2d_objects') and len(scene.text2d_objects) > 0:
            self.text2d_renderer.render_text_objects(scene.text2d_objects)
        
        # Check if scene has a render_ui method (new UI system)
        if hasattr(scene, 'render_ui'):
            scene.render_ui(self.text2d_renderer)
        # Fallback: Check if scene has text entities (legacy SplashScene)
        elif hasattr(scene, 'get_text_entities'):
            text_entities = scene.get_text_entities()
            self.text2d_renderer.render_text_objects(text_entities)
        
        # Restore culling state if it was enabled
        if cull_state_before:
            glEnable(GL_CULL_FACE)
    
    def get_current_scene(self):
        """Get the current active scene."""
        if self.scene_renderer:
            return self.scene_renderer.scene
        return None
    
    def cleanup(self):
        """Clean up pipeline resources."""
        # Renderers clean themselves up
        self.initialized = False
        print("[RenderPipeline] Cleaned up")

