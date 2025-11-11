"""
OpenGL Renderer Module
Handles OpenGL initialization and rendering operations.
"""

from OpenGL.GL import *  # type: ignore
from OpenGL.GL.shaders import compileProgram, compileShader  # type: ignore
import numpy as np
import ctypes
from typing import Optional, Dict, List
from .window import Window
from .camera import Camera
from .scene import Scene
from .mesh import Mesh
from .shadow_map import ShadowMap
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
        self.shadow_shader: Optional[int] = None
        self.shadow_shader_point: Optional[int] = None
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
        
        # Shadow maps
        self.shadow_maps: Dict[str, ShadowMap] = {}  # Maps light name to shadow map
        
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
            
            # Load and compile shadow shaders
            if not self._create_shadow_shaders():
                print("WARNING: Shadow shaders failed to compile - shadows will be disabled")
                # Continue anyway, shadows are optional
            
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
            
            # PBR texture uniforms
            self.roughness_map_loc = glGetUniformLocation(self.shader_program, "roughnessMap")
            self.use_roughness_map_loc = glGetUniformLocation(self.shader_program, "useRoughnessMap")
            self.ao_map_loc = glGetUniformLocation(self.shader_program, "aoMap")
            self.use_ao_map_loc = glGetUniformLocation(self.shader_program, "useAOMap")
            
            # Explicitly bind samplers to texture units
            glUseProgram(self.shader_program)
            
            # Main texture samplers
            texture_sampler_loc = glGetUniformLocation(self.shader_program, "textureSampler")
            if texture_sampler_loc != -1:
                glUniform1i(texture_sampler_loc, 0)  # Unit 0
            
            normal_map_sampler_loc = glGetUniformLocation(self.shader_program, "normalMap")
            if normal_map_sampler_loc != -1:
                glUniform1i(normal_map_sampler_loc, 1)  # Unit 1
            
            # Shadow map samplers
            shadow_dir_loc = glGetUniformLocation(self.shader_program, "shadowMapDirectional")
            if shadow_dir_loc != -1:
                glUniform1i(shadow_dir_loc, 2)  # Unit 2
            
            # Spot shadow maps
            for i in range(4):
                spot_loc = glGetUniformLocation(self.shader_program, f"shadowMapSpot{i}")
                if spot_loc != -1:
                    glUniform1i(spot_loc, 3 + i)  # Units 3-6
            
            # Point shadow cubemaps
            for i in range(4):
                point_loc = glGetUniformLocation(self.shader_program, f"shadowMapPoint{i}")
                if point_loc != -1:
                    glUniform1i(point_loc, 7 + i)  # Units 7-10
            
            # PBR texture maps
            roughness_map_loc = glGetUniformLocation(self.shader_program, "roughnessMap")
            if roughness_map_loc != -1:
                glUniform1i(roughness_map_loc, 11)  # Unit 11
            
            ao_map_loc = glGetUniformLocation(self.shader_program, "aoMap")
            if ao_map_loc != -1:
                glUniform1i(ao_map_loc, 12)  # Unit 12
            
            # Initialize numSpotLights to 0 (will be set properly during render)
            glUniform1i(self.num_spot_lights_loc, 0)
            
            glUseProgram(0)
            
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
            
            # Create program manually to avoid premature validation
            self.shader_program = glCreateProgram()
            glAttachShader(self.shader_program, vert_shader)
            glAttachShader(self.shader_program, frag_shader)
            glLinkProgram(self.shader_program)
            
            # Check link status
            link_status = glGetProgramiv(self.shader_program, GL_LINK_STATUS)
            if not link_status:
                info_log = glGetProgramInfoLog(self.shader_program)
                print(f"ERROR: Shader program linking failed: {info_log.decode()}")
                return False
            
            # Clean up shaders (no longer needed after linking)
            glDeleteShader(vert_shader)
            glDeleteShader(frag_shader)
            
            print("[OK] Shaders compiled and linked successfully")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to compile shaders: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_shadow_shaders(self) -> bool:
        """Compile shadow depth shaders."""
        try:
            # Directional/Spot light shadow shader
            vert_path = "shaders/shadow_depth.vert.glsl"
            frag_path = "shaders/shadow_depth.frag.glsl"
            
            if os.path.exists(vert_path) and os.path.exists(frag_path):
                with open(vert_path, 'r') as f:
                    vert_source = f.read()
                with open(frag_path, 'r') as f:
                    frag_source = f.read()
                
                vert_shader = compileShader(vert_source, GL_VERTEX_SHADER)
                frag_shader = compileShader(frag_source, GL_FRAGMENT_SHADER)
                
                self.shadow_shader = glCreateProgram()
                glAttachShader(self.shadow_shader, vert_shader)
                glAttachShader(self.shadow_shader, frag_shader)
                glLinkProgram(self.shadow_shader)
                
                if not glGetProgramiv(self.shadow_shader, GL_LINK_STATUS):
                    print(f"ERROR: Shadow shader linking failed")
                    return False
                
                glDeleteShader(vert_shader)
                glDeleteShader(frag_shader)
                print("[OK] Shadow depth shader compiled")
            
            # Point light shadow shader (requires geometry shader - skip for now)
            # We'll implement this later if needed
            
            return True
            
        except Exception as e:
            print(f"WARNING: Failed to compile shadow shaders: {e}")
            return False
    
    def _create_shadow_maps(self):
        """Create shadow maps for lights that cast shadows."""
        if not self.scene:
            return
        
        for light in self.scene.get_active_lights():
            if light.cast_shadows and light.name not in self.shadow_maps:
                light_data = light.get_light_data()
                
                if light_data['type'] == 'point':
                    # Cubemap shadow map for point lights
                    shadow_map = ShadowMap(1024, 1024, is_cubemap=True)
                else:
                    # 2D shadow map for directional/spot lights
                    shadow_map = ShadowMap(2048, 2048, is_cubemap=False)
                
                self.shadow_maps[light.name] = shadow_map
                light.shadow_map = shadow_map
                print(f"[OK] Shadow map created for light '{light.name}'")
    
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
        
        # Create shadow maps for lights that cast shadows
        self._create_shadow_maps()
    
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
            
            # Bind roughness map if available
            if mat.roughness_map and mat.roughness_map.texture_id:
                glActiveTexture(GL_TEXTURE11)  # Use texture unit 11 for roughness
                mat.roughness_map.bind(11)
                glUniform1i(self.roughness_map_loc, 11)
                glUniform1i(self.use_roughness_map_loc, 1)  # Enable roughness mapping
            else:
                glUniform1i(self.use_roughness_map_loc, 0)  # Disable roughness mapping
            
            # Bind AO map if available
            if mat.ao_map and mat.ao_map.texture_id:
                glActiveTexture(GL_TEXTURE12)  # Use texture unit 12 for AO
                mat.ao_map.bind(12)
                glUniform1i(self.ao_map_loc, 12)
                glUniform1i(self.use_ao_map_loc, 1)  # Enable AO mapping
            else:
                glUniform1i(self.use_ao_map_loc, 0)  # Disable AO mapping
        else:
            # Default material
            glUniform3fv(self.material_ambient_loc, 1, [0.2, 0.2, 0.2])
            glUniform3fv(self.material_diffuse_loc, 1, [0.8, 0.8, 0.8])
            glUniform3fv(self.material_specular_loc, 1, [1.0, 1.0, 1.0])
            glUniform1f(self.material_shininess_loc, 32.0)
            glUniform1i(self.use_normal_map_loc, 0)  # Disable normal mapping
            glUniform1i(self.use_roughness_map_loc, 0)  # Disable roughness mapping
            glUniform1i(self.use_ao_map_loc, 0)  # Disable AO mapping
    
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
    
    def _setup_shadow_mapping(self):
        """Set up shadow mapping uniforms and bind shadow textures."""
        if not self.scene:
            return
        
        # Get lights
        active_lights = self.scene.get_active_lights()
        directional_light = None
        spot_lights = []
        
        for light in active_lights:
            light_data = light.get_light_data()
            if light_data['type'] == 'directional' and not directional_light:
                directional_light = light
            elif light_data['type'] == 'spot' and len(spot_lights) < 4:
                spot_lights.append(light)
        
        # Set up directional light shadows
        if directional_light and directional_light.cast_shadows and directional_light.name in self.shadow_maps:
            shadow_map = self.shadow_maps[directional_light.name]
            shadow_map.bind_texture(2)  # Texture unit 2
            
            light_space_matrix = self._calculate_light_space_matrix(directional_light)
            lsm_loc = glGetUniformLocation(self.shader_program, "lightSpaceMatrixDirectional")
            glUniformMatrix4fv(lsm_loc, 1, GL_FALSE, light_space_matrix)
            
            use_shadows_loc = glGetUniformLocation(self.shader_program, "useShadowsDirectional")
            glUniform1i(use_shadows_loc, 1)
        else:
            use_shadows_loc = glGetUniformLocation(self.shader_program, "useShadowsDirectional")
            glUniform1i(use_shadows_loc, 0)
        
        # Set up spotlight shadows
        for i in range(4):
            if i < len(spot_lights) and spot_lights[i].cast_shadows and spot_lights[i].name in self.shadow_maps:
                shadow_map = self.shadow_maps[spot_lights[i].name]
                shadow_map.bind_texture(3 + i)  # Texture units 3-6
                
                light_space_matrix = self._calculate_light_space_matrix(spot_lights[i])
                lsm_loc = glGetUniformLocation(self.shader_program, f"lightSpaceMatrixSpot[{i}]")
                glUniformMatrix4fv(lsm_loc, 1, GL_FALSE, light_space_matrix)
                
                use_shadows_loc = glGetUniformLocation(self.shader_program, f"useShadowsSpot[{i}]")
                glUniform1i(use_shadows_loc, 1)
            else:
                use_shadows_loc = glGetUniformLocation(self.shader_program, f"useShadowsSpot[{i}]")
                glUniform1i(use_shadows_loc, 0)
        
        # Disable point light shadows for now
        for i in range(4):
            use_shadows_loc = glGetUniformLocation(self.shader_program, f"useShadowsPoint[{i}]")
            glUniform1i(use_shadows_loc, 0)
    
    def _calculate_light_space_matrix(self, light):
        """Calculate light-space matrix for shadow mapping."""
        light_data = light.get_light_data()
        light_type = light_data['type']
        
        if light_type == 'directional':
            # Orthographic projection for directional lights
            light_dir = np.array(light_data['direction'], dtype=np.float32)
            
            # Create view matrix looking from light direction
            light_pos = np.array([0.0, 0.0, 0.0], dtype=np.float32) - light_dir * 10.0
            target = np.array([0.0, 0.0, 0.0], dtype=np.float32)
            up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
            
            # Simple lookAt
            z_axis = light_dir / np.linalg.norm(light_dir)
            x_axis = np.cross(up, z_axis)
            x_axis = x_axis / np.linalg.norm(x_axis)
            y_axis = np.cross(z_axis, x_axis)
            
            view = np.identity(4, dtype=np.float32)
            view[0, :3] = x_axis
            view[1, :3] = y_axis
            view[2, :3] = z_axis
            view[:3, 3] = -np.dot(np.array([x_axis, y_axis, z_axis]), light_pos)
            
            # Orthographic projection
            near = 1.0
            far = 20.0
            size = 10.0
            proj = np.array([
                [1.0/size, 0, 0, 0],
                [0, 1.0/size, 0, 0],
                [0, 0, -2.0/(far-near), -(far+near)/(far-near)],
                [0, 0, 0, 1]
            ], dtype=np.float32)
            
            return np.dot(proj, view)
            
        elif light_type == 'spot':
            # Perspective projection for spot lights
            light_pos = np.array(light_data['position'], dtype=np.float32)
            light_dir = np.array(light_data['direction'], dtype=np.float32)
            
            # Create view matrix
            target = light_pos + light_dir
            up = np.array([0.0, 1.0, 0.0], dtype=np.float32)
            
            z_axis = light_dir / np.linalg.norm(light_dir)
            x_axis = np.cross(up, z_axis)
            if np.linalg.norm(x_axis) > 0:
                x_axis = x_axis / np.linalg.norm(x_axis)
            y_axis = np.cross(z_axis, x_axis)
            
            view = np.identity(4, dtype=np.float32)
            view[0, :3] = x_axis
            view[1, :3] = y_axis
            view[2, :3] = z_axis
            view[:3, 3] = -np.dot(np.array([x_axis, y_axis, z_axis]), light_pos)
            
            # Perspective projection
            fov = np.radians(45.0)  # 45 degree FOV
            aspect = 1.0
            near = 0.1
            far = 25.0
            
            f = 1.0 / np.tan(fov / 2.0)
            proj = np.array([
                [f/aspect, 0, 0, 0],
                [0, f, 0, 0],
                [0, 0, (far+near)/(near-far), (2*far*near)/(near-far)],
                [0, 0, -1, 0]
            ], dtype=np.float32)
            
            return np.dot(proj, view)
        
        return np.identity(4, dtype=np.float32)
    
    def _render_shadow_pass(self):
        """Render shadow maps for all lights that cast shadows."""
        if not self.shadow_shader or not self.scene:
            return
        
        # Save current viewport
        viewport = glGetIntegerv(GL_VIEWPORT)
        
        # Render shadows for each light
        for light in self.scene.get_active_lights():
            if not light.cast_shadows or light.name not in self.shadow_maps:
                continue
            
            shadow_map = self.shadow_maps[light.name]
            light_data = light.get_light_data()
            
            # Skip point lights for now (requires geometry shader)
            if light_data['type'] == 'point':
                continue
            
            # Bind shadow map framebuffer
            shadow_map.bind()
            
            # Use shadow shader
            glUseProgram(self.shadow_shader)
            
            # Calculate light space matrix
            light_space_matrix = self._calculate_light_space_matrix(light)
            
            # Set uniform
            light_space_loc = glGetUniformLocation(self.shadow_shader, "lightSpaceMatrix")
            glUniformMatrix4fv(light_space_loc, 1, GL_FALSE, light_space_matrix)
            
            # Render all objects
            for game_object in self.scene.game_objects:
                if not game_object.model or not game_object.active:
                    continue
                
                # Set model matrix
                model = game_object.transform.get_model_matrix()
                model_loc = glGetUniformLocation(self.shadow_shader, "model")
                glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
                
                # Render each mesh
                for mesh in game_object.model.meshes:
                    if mesh.vbo:
                        glBindVertexArray(self.vao)
                        glBindBuffer(GL_ARRAY_BUFFER, mesh.vbo)
                        
                        # Only need position for shadow pass
                        glEnableVertexAttribArray(0)
                        from .vertex import Vertex as VertexClass
                        stride = VertexClass.get_stride()
                        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, 
                                            ctypes.c_void_p(VertexClass.get_position_offset()))
                        
                        # Draw
                        if mesh.has_indices and mesh.ebo:
                            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, mesh.ebo)
                            glDrawElements(GL_TRIANGLES, mesh.index_count, GL_UNSIGNED_INT, None)
                        else:
                            glDrawArrays(GL_TRIANGLES, 0, mesh.vertex_count)
            
            # Unbind shadow map
            shadow_map.unbind()
        
        # Restore viewport
        glViewport(viewport[0], viewport[1], viewport[2], viewport[3])
    
    def render_frame(self):
        """Render a single frame."""
        if not self.scene:
            return
        
        try:
            # Render shadow maps first
            self._render_shadow_pass()
            
            # Clear the screen for main render
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
            
            # Set up shadow mapping
            self._setup_shadow_mapping()
            
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
        
        # Clean up shadow maps
        for shadow_map in self.shadow_maps.values():
            shadow_map.cleanup()
        self.shadow_maps.clear()
        
        # Clean up all mesh VBOs
        for vbo in self._mesh_vbos.values():
            glDeleteBuffers(1, [vbo])
        self._mesh_vbos.clear()
        
        # Clean up VAO
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            self.vao = None
        
        # Clean up shader programs
        if self.shader_program:
            glDeleteProgram(self.shader_program)
            self.shader_program = None
        
        if self.shadow_shader:
            glDeleteProgram(self.shadow_shader)
            self.shadow_shader = None
        
        if self.shadow_shader_point:
            glDeleteProgram(self.shadow_shader_point)
            self.shadow_shader_point = None
        
        print("[OK] OpenGL renderer cleaned up")
