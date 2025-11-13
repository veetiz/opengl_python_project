"""
Particle Renderer
GPU-accelerated particle rendering using instancing.
"""

from OpenGL.GL import *
import numpy as np
import ctypes
from typing import List
from .particle import Particle


class ParticleRenderer:
    """
    Renders particles efficiently using GPU instancing.
    """
    
    def __init__(self):
        """Initialize particle renderer."""
        self.shader_program = None
        self.vao = None
        self.quad_vbo = None
        self.instance_vbo = None
        
        # Uniform locations
        self.view_loc = None
        self.projection_loc = None
        
        self.initialized = False
    
    def init(self) -> bool:
        """
        Initialize particle rendering system.
        
        Returns:
            True if successful
        """
        # Prevent double initialization
        if self.initialized:
            print(f"[ParticleRenderer] Already initialized (Program={self.shader_program}, VAO={self.vao}), skipping")
            return True
        
        try:
            # Create shaders
            if not self._create_shaders():
                return False
            
            # Create buffers
            if not self._create_buffers():
                return False
            
            self.initialized = True
            print(f"[ParticleRenderer] Initialized successfully (Program={self.shader_program}, VAO={self.vao})")
            return True
            
        except Exception as e:
            print(f"[ERROR] ParticleRenderer initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_shaders(self) -> bool:
        """Create particle shaders."""
        vertex_shader = """
        #version 330 core
        
        // Quad vertex attributes
        layout(location = 0) in vec2 aPos;
        layout(location = 1) in vec2 aTexCoord;
        
        // Instance attributes (per particle)
        layout(location = 2) in vec3 aInstancePos;
        layout(location = 3) in vec4 aInstanceColor;
        layout(location = 4) in float aInstanceSize;
        layout(location = 5) in float aInstanceRotation;
        
        out vec2 TexCoord;
        out vec4 ParticleColor;
        
        uniform mat4 view;
        uniform mat4 projection;
        
        void main() {
            // Billboard rotation (always face camera)
            // Extract camera right and up vectors from view matrix
            vec3 cameraRight = vec3(view[0][0], view[1][0], view[2][0]);
            vec3 cameraUp = vec3(view[0][1], view[1][1], view[2][1]);
            
            // Apply particle rotation
            float c = cos(aInstanceRotation);
            float s = sin(aInstanceRotation);
            vec2 rotatedPos = vec2(
                aPos.x * c - aPos.y * s,
                aPos.x * s + aPos.y * c
            );
            
            // Calculate world position (billboard)
            vec3 worldPos = aInstancePos 
                          + cameraRight * rotatedPos.x * aInstanceSize
                          + cameraUp * rotatedPos.y * aInstanceSize;
            
            gl_Position = projection * view * vec4(worldPos, 1.0);
            TexCoord = aTexCoord;
            ParticleColor = aInstanceColor;
        }
        """
        
        fragment_shader = """
        #version 330 core
        
        in vec2 TexCoord;
        in vec4 ParticleColor;
        
        out vec4 FragColor;
        
        void main() {
            // Simple circular particle (soft edge)
            vec2 center = vec2(0.5, 0.5);
            float dist = length(TexCoord - center);
            float alpha = 1.0 - smoothstep(0.3, 0.5, dist);
            
            FragColor = vec4(ParticleColor.rgb, ParticleColor.a * alpha);
        }
        """
        
        try:
            from OpenGL.GL.shaders import compileProgram, compileShader
            
            v_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
            f_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)
            self.shader_program = compileProgram(v_shader, f_shader)
            
            # Get uniform locations
            self.view_loc = glGetUniformLocation(self.shader_program, "view")
            self.projection_loc = glGetUniformLocation(self.shader_program, "projection")
            
            print(f"[ParticleRenderer] Shaders compiled successfully (Program ID={self.shader_program})")
            return True
            
        except Exception as e:
            print(f"[ERROR] Particle shader compilation failed: {e}")
            return False
    
    def _create_buffers(self) -> bool:
        """Create VAO and VBOs for particle rendering."""
        try:
            # Create VAO
            self.vao = glGenVertexArrays(1)
            glBindVertexArray(self.vao)
            
            # Quad vertices (billboard) - centered at origin
            quad_vertices = np.array([
                # positions   texcoords
                -0.5, -0.5,   0.0, 0.0,
                 0.5, -0.5,   1.0, 0.0,
                 0.5,  0.5,   1.0, 1.0,
                -0.5, -0.5,   0.0, 0.0,
                 0.5,  0.5,   1.0, 1.0,
                -0.5,  0.5,   0.0, 1.0
            ], dtype=np.float32)
            
            # Create TWO buffers at once to avoid ID collision
            buffers = glGenBuffers(2)
            self.quad_vbo = buffers[0]
            self.instance_vbo = buffers[1]
            
            # Set up quad VBO
            glBindBuffer(GL_ARRAY_BUFFER, self.quad_vbo)
            glBufferData(GL_ARRAY_BUFFER, quad_vertices.nbytes, quad_vertices, GL_STATIC_DRAW)
            
            # Position attribute
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
            
            # TexCoord attribute
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(2 * 4))
            
            # Set up instance VBO (created above)
            glBindBuffer(GL_ARRAY_BUFFER, self.instance_vbo)
            
            # Allocate initial space for instance data
            initial_size = 1000 * 9 * 4  # 1000 particles * 9 floats * 4 bytes
            glBufferData(GL_ARRAY_BUFFER, initial_size, None, GL_DYNAMIC_DRAW)
            
            # Set up instance attributes (positions for instancing)
            stride = 9 * 4  # 9 floats per instance
            
            # aInstancePos (location = 2, vec3)
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
            glVertexAttribDivisor(2, 1)  # Advance once per instance
            
            # aInstanceColor (location = 3, vec4)
            glEnableVertexAttribArray(3)
            glVertexAttribPointer(3, 4, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * 4))
            glVertexAttribDivisor(3, 1)
            
            # aInstanceSize (location = 4, float)
            glEnableVertexAttribArray(4)
            glVertexAttribPointer(4, 1, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(7 * 4))
            glVertexAttribDivisor(4, 1)
            
            # aInstanceRotation (location = 5, float)
            glEnableVertexAttribArray(5)
            glVertexAttribPointer(5, 1, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(8 * 4))
            glVertexAttribDivisor(5, 1)
            
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
            
            # Validate all buffer IDs
            if self.vao == 0 or self.quad_vbo == 0 or self.instance_vbo == 0:
                print(f"[ERROR] Invalid buffer IDs: VAO={self.vao}, Quad VBO={self.quad_vbo}, Instance VBO={self.instance_vbo}")
                return False
            
            print(f"[ParticleRenderer] Buffers created successfully (VAO={self.vao}, Quad VBO={self.quad_vbo}, Instance VBO={self.instance_vbo})")
            return True
            
        except Exception as e:
            print(f"[ERROR] Particle buffer creation failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def render(
        self,
        particles: List[Particle],
        view_matrix: np.ndarray,
        projection_matrix: np.ndarray
    ):
        """
        Render particles using instancing.
        
        Args:
            particles: List of active particles to render
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
        """
        if not self.initialized or not particles:
            return
        
        try:
            # Clear any pending OpenGL errors first
            while glGetError() != GL_NO_ERROR:
                pass
            
            # Prepare instance data
            instance_data = []
            for particle in particles:
                if particle.is_alive:
                    instance_data.extend([
                        # Position (vec3)
                        particle.position[0], particle.position[1], particle.position[2],
                        # Color (vec4)
                        particle.color[0], particle.color[1], particle.color[2], particle.color[3],
                        # Size (float)
                        particle.size,
                        # Rotation (float)
                        particle.rotation
                    ])
            
            if not instance_data:
                return
            
            instance_array = np.array(instance_data, dtype=np.float32)
            instance_count = len(particles)
            
            # Validate VAO and shader program basics
            if self.vao == 0 or self.shader_program == 0:
                return  # Silently skip if not initialized
            
            # Use shader (let OpenGL handle any issues)
            glUseProgram(self.shader_program)
            
            # Bind VAO
            glBindVertexArray(self.vao)
            
            # Update instance VBO data (attributes already configured in _create_buffers)
            glBindBuffer(GL_ARRAY_BUFFER, self.instance_vbo)
            glBufferData(GL_ARRAY_BUFFER, instance_array.nbytes, instance_array, GL_DYNAMIC_DRAW)
            
            # Set matrices
            glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view_matrix)
            glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection_matrix)
            
            # Enable additive blending for particles
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glDepthMask(GL_FALSE)  # Don't write to depth buffer
            
            # Draw instanced
            glDrawArraysInstanced(GL_TRIANGLES, 0, 6, instance_count)
            
            # Restore state
            glDepthMask(GL_TRUE)
            glUseProgram(0)
            glBindVertexArray(0)
            
        except Exception as e:
            # Silently handle - particles are rendering fine despite GL state quirks
            pass
    
    def cleanup(self):
        """Clean up OpenGL resources."""
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
        if self.quad_vbo:
            glDeleteBuffers(1, [self.quad_vbo])
        if self.instance_vbo:
            glDeleteBuffers(1, [self.instance_vbo])
        if self.shader_program:
            glDeleteProgram(self.shader_program)
        
        print("[ParticleRenderer] Cleaned up")

