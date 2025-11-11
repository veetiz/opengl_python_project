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
        try:
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
                print("ERROR: Shader program creation failed")
                return False
            
            # Get uniform locations
            self.model_loc = glGetUniformLocation(self.shader_program, "model")
            self.view_loc = glGetUniformLocation(self.shader_program, "view")
            self.projection_loc = glGetUniformLocation(self.shader_program, "projection")
            self.texture_sampler_loc = glGetUniformLocation(self.shader_program, "textureSampler")
            self.use_texture_loc = glGetUniformLocation(self.shader_program, "useTexture")
            
            # Material uniforms
            self.material_ambient_loc = glGetUniformLocation(self.shader_program, "material_ambient")
            self.material_diffuse_loc = glGetUniformLocation(self.shader_program, "material_diffuse")
            self.material_specular_loc = glGetUniformLocation(self.shader_program, "material_specular")
            self.material_shininess_loc = glGetUniformLocation(self.shader_program, "material_shininess")
            
            # Lighting uniforms
            self.lighting_enabled_loc = glGetUniformLocation(self.shader_program, "lightingEnabled")
            self.view_pos_loc = glGetUniformLocation(self.shader_program, "viewPos")
            
            # Directional light uniforms
            self.has_dir_light_loc = glGetUniformLocation(self.shader_program, "hasDirectionalLight")
            self.dir_light_direction_loc = glGetUniformLocation(self.shader_program, "dirLight_direction")
            self.dir_light_color_loc = glGetUniformLocation(self.shader_program, "dirLight_color")
            self.dir_light_intensity_loc = glGetUniformLocation(self.shader_program, "dirLight_intensity")
            
            # Point light uniforms
            self.num_point_lights_loc = glGetUniformLocation(self.shader_program, "numPointLights")
            
            # Spot light uniforms
            self.num_spot_lights_loc = glGetUniformLocation(self.shader_program, "numSpotLights")
            
            # Normal mapping uniforms
            self.normal_map_loc = glGetUniformLocation(self.shader_program, "normalMap")
            self.use_normal_map_loc = glGetUniformLocation(self.shader_program, "useNormalMap")
            
            # Create VAO
            self.vao = glGenVertexArrays(1)
            glBindVertexArray(self.vao)
            
            print("[OK] OpenGL renderer initialized")
            return True
            
        except Exception as e:
            print(f"ERROR: Renderer initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
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
            try:
                vert_shader = compileShader(vert_source, GL_VERTEX_SHADER)
                print("[DEBUG] Vertex shader compiled")
            except Exception as e:
                print(f"ERROR: Vertex shader compilation failed: {e}")
                raise
            
            try:
                frag_shader = compileShader(frag_source, GL_FRAGMENT_SHADER)
                print("[DEBUG] Fragment shader compiled")
            except Exception as e:
                print(f"ERROR: Fragment shader compilation failed: {e}")
                raise
            
            self.shader_program = compileProgram(vert_shader, frag_shader)
            
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
            
            # Bind VAO first (required for setting up vertex attributes)
            glBindVertexArray(self.vao)
            
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
            
            # Tangent attribute (location = 4)
            glEnableVertexAttribArray(4)
            glVertexAttribPointer(4, 3, GL_FLOAT, GL_FALSE, stride, 
                                ctypes.c_void_p(VertexClass.get_tangent_offset()))
            
            # Bitangent attribute (location = 5)
            glEnableVertexAttribArray(5)
            glVertexAttribPointer(5, 3, GL_FLOAT, GL_FALSE, stride, 
                                ctypes.c_void_p(VertexClass.get_bitangent_offset()))
            
            # Create EBO if mesh has indices
            if mesh.has_indices and mesh.index_data is not None:
                ebo = glGenBuffers(1)
                mesh.ebo = ebo
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
                glBufferData(GL_ELEMENT_ARRAY_BUFFER, mesh.index_data.nbytes, mesh.index_data, GL_STATIC_DRAW)
            
            # Unbind VAO
            glBindVertexArray(0)
            
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to create vertex buffer: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _set_material(self, game_object):
        """
        Set material uniforms for a game object.
        
        Args:
            game_object: GameObject with optional material
        """
        # Use object's material if available, otherwise default values
        if hasattr(game_object, 'material') and game_object.material:
            mat = game_object.material
            glUniform3fv(self.material_ambient_loc, 1, mat.ambient)
            glUniform3fv(self.material_diffuse_loc, 1, mat.diffuse)
            glUniform3fv(self.material_specular_loc, 1, mat.specular)
            glUniform1f(self.material_shininess_loc, mat.shininess)
            
            # Bind normal map if available
            if mat.normal_map and mat.normal_map.texture_id:
                glActiveTexture(GL_TEXTURE1)  # Use texture unit 1 for normal map
                mat.normal_map.bind(1)
                glUniform1i(self.normal_map_loc, 1)  # Set sampler to unit 1
                glUniform1i(self.use_normal_map_loc, 1)  # Enable normal mapping
            else:
                glUniform1i(self.use_normal_map_loc, 0)  # Disable normal mapping
        else:
            # Default material
            glUniform3fv(self.material_ambient_loc, 1, [0.2, 0.2, 0.2])
            glUniform3fv(self.material_diffuse_loc, 1, [0.8, 0.8, 0.8])
            glUniform3fv(self.material_specular_loc, 1, [1.0, 1.0, 1.0])
            glUniform1f(self.material_shininess_loc, 32.0)
            glUniform1i(self.use_normal_map_loc, 0)  # Disable normal mapping
    
    def _setup_lighting(self):
        """Set up lighting uniforms for the current scene."""
        if not self.scene:
            return
        
        # Get active lights from scene
        active_lights = self.scene.get_active_lights()
        
        # Enable lighting if we have lights
        has_lights = len(active_lights) > 0
        glUniform1i(self.lighting_enabled_loc, 1 if has_lights else 0)
        
        if not has_lights:
            return
        
        # Separate lights by type
        directional_light = None
        point_lights = []
        spot_lights = []
        
        for light in active_lights:
            light_data = light.get_light_data()
            if light_data['type'] == 'directional':
                if not directional_light:  # Use first directional light only
                    directional_light = light
            elif light_data['type'] == 'point':
                if len(point_lights) < 4:  # Maximum 4 point lights
                    point_lights.append(light)
            elif light_data['type'] == 'spot':
                if len(spot_lights) < 4:  # Maximum 4 spot lights
                    spot_lights.append(light)
        
        # Set directional light
        if directional_light:
            data = directional_light.get_light_data()
            glUniform1i(self.has_dir_light_loc, 1)
            glUniform3fv(self.dir_light_direction_loc, 1, data['direction'])
            glUniform3fv(self.dir_light_color_loc, 1, data['color'])
            glUniform1f(self.dir_light_intensity_loc, data['intensity'])
        else:
            glUniform1i(self.has_dir_light_loc, 0)
        
        # Set point lights
        glUniform1i(self.num_point_lights_loc, len(point_lights))
        for i, point_light in enumerate(point_lights):
            data = point_light.get_light_data()
            pos_loc = glGetUniformLocation(self.shader_program, f"pointLights_position[{i}]")
            color_loc = glGetUniformLocation(self.shader_program, f"pointLights_color[{i}]")
            intensity_loc = glGetUniformLocation(self.shader_program, f"pointLights_intensity[{i}]")
            constant_loc = glGetUniformLocation(self.shader_program, f"pointLights_constant[{i}]")
            linear_loc = glGetUniformLocation(self.shader_program, f"pointLights_linear[{i}]")
            quadratic_loc = glGetUniformLocation(self.shader_program, f"pointLights_quadratic[{i}]")
            
            glUniform3fv(pos_loc, 1, data['position'])
            glUniform3fv(color_loc, 1, data['color'])
            glUniform1f(intensity_loc, data['intensity'])
            glUniform1f(constant_loc, data['constant'])
            glUniform1f(linear_loc, data['linear'])
            glUniform1f(quadratic_loc, data['quadratic'])
        
        # Set spot lights
        glUniform1i(self.num_spot_lights_loc, len(spot_lights))
        for i, spot_light in enumerate(spot_lights):
            data = spot_light.get_light_data()
            pos_loc = glGetUniformLocation(self.shader_program, f"spotLights_position[{i}]")
            dir_loc = glGetUniformLocation(self.shader_program, f"spotLights_direction[{i}]")
            color_loc = glGetUniformLocation(self.shader_program, f"spotLights_color[{i}]")
            intensity_loc = glGetUniformLocation(self.shader_program, f"spotLights_intensity[{i}]")
            inner_cutoff_loc = glGetUniformLocation(self.shader_program, f"spotLights_innerCutoff[{i}]")
            outer_cutoff_loc = glGetUniformLocation(self.shader_program, f"spotLights_outerCutoff[{i}]")
            constant_loc = glGetUniformLocation(self.shader_program, f"spotLights_constant[{i}]")
            linear_loc = glGetUniformLocation(self.shader_program, f"spotLights_linear[{i}]")
            quadratic_loc = glGetUniformLocation(self.shader_program, f"spotLights_quadratic[{i}]")
            
            glUniform3fv(pos_loc, 1, data['position'])
            glUniform3fv(dir_loc, 1, data['direction'])
            glUniform3fv(color_loc, 1, data['color'])
            glUniform1f(intensity_loc, data['intensity'])
            glUniform1f(inner_cutoff_loc, data['inner_cutoff'])
            glUniform1f(outer_cutoff_loc, data['outer_cutoff'])
            glUniform1f(constant_loc, data['constant'])
            glUniform1f(linear_loc, data['linear'])
            glUniform1f(quadratic_loc, data['quadratic'])
    
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
                
                # Set view position for specular lighting
                glUniform3fv(self.view_pos_loc, 1, active_camera.position)
            
            # Set up lighting
            self._setup_lighting()
            
            # Bind VAO
            glBindVertexArray(self.vao)
            
            # Render all active game objects in the scene
            for game_object in self.scene.get_active_objects():
                if game_object.model:
                    # Set model matrix from game object transform
                    model_matrix = game_object.get_model_matrix()
                    glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model_matrix)
                    
                    # Set material properties (use object's material or default)
                    self._set_material(game_object)
                    
                    # Draw all meshes in the model
                    for mesh in game_object.model.meshes:
                        if hasattr(mesh, 'vbo') and mesh.vbo:
                            glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo)
                            
                            # Bind diffuse texture if available
                            has_texture = hasattr(mesh, 'texture') and mesh.texture and mesh.texture.texture_id
                            
                            if has_texture:
                                glActiveTexture(GL_TEXTURE0)
                                mesh.texture.bind(0)
                                glUniform1i(self.texture_sampler_loc, 0)
                                glUniform1i(self.use_texture_loc, 1)
                            else:
                                glUniform1i(self.use_texture_loc, 0)
                            
                            # Bind normal map if available (from material)
                            has_normal_map = (hasattr(game_object, 'material') and 
                                            game_object.material and 
                                            game_object.material.normal_map and 
                                            game_object.material.normal_map.texture_id)
                            
                            if has_normal_map:
                                glActiveTexture(GL_TEXTURE1)
                                game_object.material.normal_map.bind(1)
                                glUniform1i(self.normal_map_loc, 1)
                                glUniform1i(self.use_normal_map_loc, 1)
                            else:
                                glUniform1i(self.use_normal_map_loc, 0)
                            
                            # Use indexed rendering if available
                            if mesh.has_indices and hasattr(mesh, 'ebo') and mesh.ebo:
                                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.ebo)
                                glDrawElements(GL_TRIANGLES, mesh.index_count, GL_UNSIGNED_INT, None)
                            else:
                                glDrawArrays(GL_TRIANGLES, 0, mesh.vertex_count)
                            
                            # Unbind texture
                            if hasattr(mesh, 'texture') and mesh.texture:
                                mesh.texture.unbind()
            
            # NOTE: Don't swap buffers here - let Application do it after text rendering
            
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
