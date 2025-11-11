"""
OpenGL Renderer Module
Handles OpenGL initialization and rendering operations.
"""

from OpenGL.GL import *  # type: ignore
from OpenGL.GL.shaders import compileProgram, compileShader  # type: ignore
import numpy as np
import ctypes
from typing import Optional, Dict
from .window import Window
from .camera import Camera
from .scene import Scene
from .mesh import Mesh
import os


class OpenGLRenderer:
    """Manages OpenGL rendering."""
    
    def __init__(self, app_name: str = "OpenGL App", enable_validation: bool = False):
        """
        Initialize the OpenGL Renderer.
        
        Args:
            app_name: Application name
            enable_validation: Enable OpenGL debug output
        """
        self.app_name = app_name
        self.enable_validation = enable_validation
        
        # OpenGL resources
        self.shader_program: Optional[int] = None
        self.vao: Optional[int] = None
        
        # Uniform locations
        self.model_loc: Optional[int] = None
        self.view_loc: Optional[int] = None
        self.projection_loc: Optional[int] = None
        
        # Scene
        self.scene: Optional[Scene] = None
        
        # Window reference
        self.window: Optional[Window] = None
        
        # Mesh VBO tracking (for cleanup)
        self._mesh_vbos: Dict[int, int] = {}  # Maps mesh id to VBO
        
    def init(self, window: Window) -> bool:
        """
        Initialize OpenGL components.
        
        Args:
            window: Window instance with OpenGL context
            
        Returns:
            True if successful, False otherwise
        """
        self.window = window
        
        # Print OpenGL info
        print(f"[OK] OpenGL Version: {glGetString(GL_VERSION).decode()}")
        print(f"[OK] GLSL Version: {glGetString(GL_SHADING_LANGUAGE_VERSION).decode()}")
        print(f"[OK] Renderer: {glGetString(GL_RENDERER).decode()}")
        
        # Enable debug output if requested
        if self.enable_validation:
            glEnable(GL_DEBUG_OUTPUT)
            glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
        
        # Set up OpenGL state
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        
        # Disable face culling for now (for debugging)
        # glEnable(GL_CULL_FACE)
        # glCullFace(GL_BACK)
        # glFrontFace(GL_CCW)  # Counter-clockwise is front face
        
        glClearColor(0.0, 0.0, 0.0, 1.0)
        
        # Load and compile shaders
        if not self._create_shader_program():
            return False
        
        # Get uniform locations
        self.model_loc = glGetUniformLocation(self.shader_program, "model")
        self.view_loc = glGetUniformLocation(self.shader_program, "view")
        self.projection_loc = glGetUniformLocation(self.shader_program, "projection")
        self.texture_sampler_loc = glGetUniformLocation(self.shader_program, "textureSampler")
        self.use_texture_loc = glGetUniformLocation(self.shader_program, "useTexture")
        
        # Create VAO
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        print("[OK] OpenGL renderer initialized")
        return True
    
    def _create_shader_program(self) -> bool:
        """Load and compile shaders."""
        try:
            # Load shader source files
            vert_path = "shaders/shader.vert.glsl"
            frag_path = "shaders/shader.frag.glsl"
            
            if not os.path.exists(vert_path):
                print(f"ERROR: Vertex shader not found: {vert_path}")
                return False
            
            if not os.path.exists(frag_path):
                print(f"ERROR: Fragment shader not found: {frag_path}")
                return False
            
            with open(vert_path, 'r') as f:
                vert_source = f.read()
            
            with open(frag_path, 'r') as f:
                frag_source = f.read()
            
            # Compile shaders
            self.shader_program = compileProgram(
                compileShader(vert_source, GL_VERTEX_SHADER),
                compileShader(frag_source, GL_FRAGMENT_SHADER)
            )
            
            print("[OK] Shaders compiled successfully")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to compile shaders: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def set_scene(self, scene: Scene):
        """
        Set the scene to render.
        
        Args:
            scene: Scene containing game objects
        """
        self.scene = scene
        
        # Create VBOs for all meshes in the scene
        for game_object in scene.game_objects:
            if game_object.model:
                for mesh in game_object.model.meshes:
                    mesh_id = id(mesh)
                    if mesh_id not in self._mesh_vbos:
                        self._create_vertex_buffer(mesh)
    
    def _create_vertex_buffer(self, mesh: Mesh) -> bool:
        """Create OpenGL vertex buffer for a mesh."""
        try:
            from .vertex import Vertex as VertexClass
            
            # Generate buffers
            vbo = glGenBuffers(1)
            mesh_id = id(mesh)
            self._mesh_vbos[mesh_id] = vbo
            mesh.vbo = vbo
            
            # Bind and upload vertex data
            glBindBuffer(GL_ARRAY_BUFFER, vbo)
            glBufferData(GL_ARRAY_BUFFER, mesh.vertex_data.nbytes, mesh.vertex_data, GL_STATIC_DRAW)
            
            # Get stride and offsets from Vertex class
            stride = VertexClass.get_stride()
            
            # Set up vertex attributes (must match shader layout)
            # Position attribute (location = 0)
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, 
                                ctypes.c_void_p(VertexClass.get_position_offset()))
            
            # Color attribute (location = 1)
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, 
                                ctypes.c_void_p(VertexClass.get_color_offset()))
            
            # TexCoord attribute (location = 2)
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, 
                                ctypes.c_void_p(VertexClass.get_texcoord_offset()))
            
            # Normal attribute (location = 3)
            glEnableVertexAttribArray(3)
            glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, stride, 
                                ctypes.c_void_p(VertexClass.get_normal_offset()))
            
            # Create EBO if mesh has indices
            if mesh.has_indices and mesh.index_data is not None:
                ebo = glGenBuffers(1)
                mesh.ebo = ebo
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
                glBufferData(GL_ELEMENT_ARRAY_BUFFER, mesh.index_data.nbytes, mesh.index_data, GL_STATIC_DRAW)
                print(f"[DEBUG] Created EBO for mesh with {mesh.index_count} indices")
            
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to create vertex buffer: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def render_frame(self):
        """Render a single frame."""
        if not self.scene:
            return
        
        try:
            # Clear the screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Use shader program
            glUseProgram(self.shader_program)
            
            # Set camera matrices from active camera in scene
            active_camera = self.scene.get_active_camera()
            if active_camera:
                view = active_camera.get_view_matrix()
                projection = active_camera.get_projection_matrix()
                
                glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view)
                glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection)
            
            # Bind VAO
            glBindVertexArray(self.vao)
            
            # Render all active game objects in the scene
            for game_object in self.scene.get_active_objects():
                if game_object.model:
                    # Set model matrix from game object transform
                    model_matrix = game_object.get_model_matrix()
                    glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model_matrix)
                    
                    # Draw all meshes in the model
                    for mesh_idx, mesh in enumerate(game_object.model.meshes):
                        if hasattr(mesh, 'vbo') and mesh.vbo:
                            glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo)
                            
                            # Bind texture if available
                            has_texture = hasattr(mesh, 'texture') and mesh.texture and mesh.texture.texture_id
                            
                            # Debug output (only first frame)
                            if not hasattr(self, '_debug_printed'):
                                print(f"\n[RENDER DEBUG] Object: {game_object.name}, Mesh {mesh_idx}")
                                print(f"[RENDER DEBUG]   Vertex count: {mesh.vertex_count}")
                                print(f"[RENDER DEBUG]   Has indices: {mesh.has_indices}")
                                print(f"[RENDER DEBUG]   Index count: {mesh.index_count if mesh.has_indices else 'N/A'}")
                                print(f"[RENDER DEBUG]   Has EBO: {hasattr(mesh, 'ebo') and mesh.ebo}")
                                print(f"[RENDER DEBUG]   has 'texture' attr: {hasattr(mesh, 'texture')}")
                                if hasattr(mesh, 'texture'):
                                    print(f"[RENDER DEBUG]   mesh.texture is not None: {mesh.texture is not None}")
                                    if mesh.texture:
                                        print(f"[RENDER DEBUG]   texture.texture_id: {mesh.texture.texture_id}")
                                print(f"[RENDER DEBUG]   has_texture (final): {has_texture}")
                                print(f"[RENDER DEBUG]   use_texture_loc: {self.use_texture_loc}")
                                print(f"[RENDER DEBUG]   texture_sampler_loc: {self.texture_sampler_loc}")
                                self._debug_printed = True
                            
                            if has_texture:
                                glActiveTexture(GL_TEXTURE0)  # Explicitly activate texture unit 0
                                mesh.texture.bind(0)  # Bind to texture unit 0
                                glUniform1i(self.texture_sampler_loc, 0)  # Set sampler to unit 0
                                glUniform1i(self.use_texture_loc, 1)  # Enable texture
                            else:
                                glUniform1i(self.use_texture_loc, 0)  # Disable texture
                            
                            # Use indexed rendering if available
                            if mesh.has_indices and hasattr(mesh, 'ebo') and mesh.ebo:
                                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.ebo)
                                glDrawElements(GL_TRIANGLES, mesh.index_count, GL_UNSIGNED_INT, None)
                            else:
                                glDrawArrays(GL_TRIANGLES, 0, mesh.vertex_count)
                            
                            # Unbind texture
                            if hasattr(mesh, 'texture') and mesh.texture:
                                mesh.texture.unbind()
            
            # Swap buffers (present)
            self.window.swap_buffers()
            
        except Exception as e:
            print(f"WARNING: Error during frame rendering: {e}")
            import traceback
            traceback.print_exc()
    
    def on_resize(self, width: int, height: int):
        """Handle window resize."""
        glViewport(0, 0, width, height)
        
        # Update all cameras in the scene
        if self.scene:
            for camera in self.scene.cameras:
                camera.set_aspect_ratio(width, height)
    
    def cleanup(self):
        """Clean up OpenGL resources."""
        print("\nCleaning up OpenGL resources...")
        
        # Clean up all mesh VBOs
        for vbo in self._mesh_vbos.values():
            glDeleteBuffers(1, [vbo])
        self._mesh_vbos.clear()
        
        # Clean up VAO
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            self.vao = None
        
        # Clean up shader program
        if self.shader_program:
            glDeleteProgram(self.shader_program)
            self.shader_program = None
        
        print("[OK] OpenGL renderer cleaned up")
