"""
Modern UI Renderer
OpenGL-based rendering for UI components (rectangles, circles, gradients).
"""

import numpy as np
from OpenGL.GL import *
from OpenGL.GL import shaders
from typing import Tuple


class ModernUIRenderer:
    """
    Renders UI primitives using OpenGL.
    Replaces ASCII character-based rendering with proper shapes.
    """
    
    def __init__(self):
        """Initialize the modern UI renderer."""
        self.initialized = False
        self.shader_program = None
        self.vao = None
        self.vbo = None
        self.circle_vao = None  # Separate VAO for circles
        self.circle_vbo = None  # Separate VBO for circles
        self.color_loc = None
        self.position_loc = None
        self.size_loc = None
        self.projection_loc = None
        self.projection_matrix = None
        
        self.screen_width = 800
        self.screen_height = 600
    
    def init(self, width: int, height: int) -> bool:
        """
        Initialize OpenGL resources.
        
        Args:
            width: Screen width
            height: Screen height
            
        Returns:
            True if successful
        """
        try:
            # Create shader program
            self._create_shaders()
            
            # Create vertex array and buffer
            self._create_buffers()
            
            # Set projection matrix
            self.set_projection(width, height)
            
            self.initialized = True
            print("[ModernUIRenderer] Initialized successfully")
            return True
            
        except Exception as e:
            print(f"[ModernUIRenderer] ERROR: Initialization failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _create_shaders(self):
        """Create and compile shaders for UI rendering."""
        # Vertex shader - simple 2D positioning
        vertex_shader_source = """
        #version 330 core
        layout(location = 0) in vec2 aPos;
        
        uniform mat4 projection;
        uniform vec2 position;
        uniform vec2 size;
        
        void main() {
            vec2 scaledPos = aPos * size + position;
            gl_Position = projection * vec4(scaledPos, 0.0, 1.0);
        }
        """
        
        # Fragment shader - solid color
        fragment_shader_source = """
        #version 330 core
        out vec4 FragColor;
        
        uniform vec4 color;
        
        void main() {
            FragColor = color;
        }
        """
        
        # Compile shaders
        vertex_shader = shaders.compileShader(vertex_shader_source, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
        
        # Link program
        self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)
        
        # Get uniform locations
        self.projection_loc = glGetUniformLocation(self.shader_program, "projection")
        self.position_loc = glGetUniformLocation(self.shader_program, "position")
        self.size_loc = glGetUniformLocation(self.shader_program, "size")
        self.color_loc = glGetUniformLocation(self.shader_program, "color")
        
        print("[ModernUIRenderer] Shaders compiled successfully")
    
    def _create_buffers(self):
        """Create vertex array and buffer objects."""
        # Create VAO for rectangles
        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)
        
        # Create VBO for a unit rectangle (0,0 to 1,1) - STATIC
        vertices = np.array([
            # Triangle 1
            0.0, 0.0,
            1.0, 0.0,
            1.0, 1.0,
            # Triangle 2
            0.0, 0.0,
            1.0, 1.0,
            0.0, 1.0
        ], dtype=np.float32)
        
        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        
        # Set vertex attribute
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        
        glBindVertexArray(0)
        
        # Create separate VAO/VBO for circles (DYNAMIC)
        self.circle_vao = glGenVertexArrays(1)
        self.circle_vbo = glGenBuffers(1)
    
    def set_projection(self, width: int, height: int):
        """
        Set orthographic projection for screen coordinates.
        
        Args:
            width: Screen width
            height: Screen height
        """
        self.screen_width = width
        self.screen_height = height
        
        # Orthographic projection: screen coordinates to NDC
        self.projection_matrix = np.array([
            [2.0/width,  0.0,         0.0,  -1.0],
            [0.0,        -2.0/height, 0.0,   1.0],
            [0.0,        0.0,        -1.0,   0.0],
            [0.0,        0.0,         0.0,   1.0]
        ], dtype=np.float32).T  # Transpose for column-major
    
    def draw_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    ):
        """
        Draw a filled rectangle.
        
        Args:
            x, y: Top-left position
            width, height: Size
            color: RGBA color (0.0-1.0)
        """
        if not self.initialized or not self.shader_program or not self.vao:
            return
        
        # Verify shader and VAO are still valid
        if not glIsProgram(self.shader_program):
            print("[ModernUIRenderer] ERROR: Shader program invalid! Reinitializing...")
            self._create_shaders()
        
        if not glIsVertexArray(self.vao):
            print("[ModernUIRenderer] ERROR: VAO invalid! Reinitializing...")
            self._create_buffers()
        
        # Use shader
        glUseProgram(self.shader_program)
        
        # Set uniforms
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection_matrix)
        glUniform2f(self.position_loc, x, y)
        glUniform2f(self.size_loc, width, height)
        glUniform4f(self.color_loc, *color)
        
        # Draw
        glBindVertexArray(self.vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)
        
        # Unbind shader for safety
        glUseProgram(0)
    
    def draw_circle(
        self,
        x: float,
        y: float,
        radius: float,
        color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
        segments: int = 32
    ):
        """
        Draw a filled circle using triangle fan.
        
        Args:
            x, y: Center position
            radius: Circle radius
            color: RGBA color
            segments: Number of segments (higher = smoother)
        """
        if not self.initialized:
            return
        
        # Create circle vertices
        vertices = []
        vertices.extend([x, y])  # Center point
        
        for i in range(segments + 1):
            angle = 2.0 * np.pi * i / segments
            vx = x + radius * np.cos(angle)
            vy = y + radius * np.sin(angle)
            vertices.extend([vx, vy])
        
        vertices = np.array(vertices, dtype=np.float32)
        
        # Use SEPARATE VAO/VBO for circles to avoid corrupting rectangle VBO
        glBindVertexArray(self.circle_vao)
        
        # Upload to GPU (DYNAMIC buffer for circles)
        glBindBuffer(GL_ARRAY_BUFFER, self.circle_vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
        
        # Set vertex attribute for circle VAO
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        
        # Use shader with identity transform (vertices are already in screen space)
        glUseProgram(self.shader_program)
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, self.projection_matrix)
        glUniform2f(self.position_loc, 0.0, 0.0)
        glUniform2f(self.size_loc, 1.0, 1.0)
        glUniform4f(self.color_loc, *color)
        
        # Draw
        glDrawArrays(GL_TRIANGLE_FAN, 0, len(vertices) // 2)
        
        glBindVertexArray(0)
        
        # Unbind shader for safety
        glUseProgram(0)
    
    def draw_border_rect(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        border_width: float = 2.0,
        color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0)
    ):
        """
        Draw a rectangle border.
        
        Args:
            x, y: Top-left position
            width, height: Size
            border_width: Border thickness
            color: RGBA color
        """
        # Top
        self.draw_rect(x, y, width, border_width, color)
        # Bottom
        self.draw_rect(x, y + height - border_width, width, border_width, color)
        # Left
        self.draw_rect(x, y, border_width, height, color)
        # Right
        self.draw_rect(x + width - border_width, y, border_width, height, color)
    
    def cleanup(self):
        """Clean up OpenGL resources."""
        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
        if self.circle_vbo:
            glDeleteBuffers(1, [self.circle_vbo])
        if self.circle_vao:
            glDeleteVertexArrays(1, [self.circle_vao])
        if self.shader_program:
            glDeleteProgram(self.shader_program)
        
        print("[ModernUIRenderer] Cleaned up")

