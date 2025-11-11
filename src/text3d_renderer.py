"""
Text3D Renderer Module
Low-level OpenGL 3D text rendering engine.
"""

from OpenGL.GL import *  # type: ignore
from OpenGL.GL.shaders import compileProgram, compileShader  # type: ignore
import numpy as np
from typing import Optional, Tuple, List
import os
from .font import Font


class Text3DRenderer:
    """
    Low-level 3D text rendering engine that handles OpenGL setup and rendering.
    Supports billboard mode (always faces camera) and world-oriented text.
    """
    
    def __init__(self):
        """Initialize 3D text renderer."""
        self.shader_program: Optional[int] = None
        self.vao: Optional[int] = None
        self.vbo: Optional[int] = None
        self.model_loc: Optional[int] = None
        self.view_loc: Optional[int] = None
        self.projection_loc: Optional[int] = None
        self.billboard_loc: Optional[int] = None
        self.text_color_loc: Optional[int] = None
        self.text_sampler_loc: Optional[int] = None
        self.initialized = False
        
    def init(self) -> bool:
        """
        Initialize 3D text rendering system.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load 3D text shaders
            if not self._load_shaders():
                return False
            
            # Get uniform locations
            self.model_loc = glGetUniformLocation(self.shader_program, "model")
            self.view_loc = glGetUniformLocation(self.shader_program, "view")
            self.projection_loc = glGetUniformLocation(self.shader_program, "projection")
            self.billboard_loc = glGetUniformLocation(self.shader_program, "billboard")
            self.text_color_loc = glGetUniformLocation(self.shader_program, "textColor")
            self.text_sampler_loc = glGetUniformLocation(self.shader_program, "text")
            
            # Create VAO and VBO for rendering quads
            self.vao = glGenVertexArrays(1)
            self.vbo = glGenBuffers(1)
            
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            
            # Allocate memory for quad vertices (6 vertices * 4 floats)
            glBufferData(GL_ARRAY_BUFFER, 6 * 4 * 4, None, GL_DYNAMIC_DRAW)
            
            # Set up vertex attributes
            glEnableVertexAttribArray(0)
            glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 4, ctypes.c_void_p(0))
            
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
            
            self.initialized = True
            print("[OK] Text3DRenderer initialized")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to initialize Text3DRenderer: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _load_shaders(self) -> bool:
        """Load and compile 3D text shaders."""
        try:
            vert_path = "shaders/text3d.vert.glsl"
            frag_path = "shaders/text3d.frag.glsl"
            
            if not os.path.exists(vert_path):
                print(f"ERROR: 3D text vertex shader not found: {vert_path}")
                return False
            
            if not os.path.exists(frag_path):
                print(f"ERROR: 3D text fragment shader not found: {frag_path}")
                return False
            
            with open(vert_path, 'r') as f:
                vert_source = f.read()
            
            with open(frag_path, 'r') as f:
                frag_source = f.read()
            
            # Compile shaders
            vert_shader = compileShader(vert_source, GL_VERTEX_SHADER)
            frag_shader = compileShader(frag_source, GL_FRAGMENT_SHADER)
            self.shader_program = compileProgram(vert_shader, frag_shader)
            
            print("[OK] 3D text shaders compiled")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to compile 3D text shaders: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def render_text_3d(
        self,
        text: str,
        font: Font,
        position: Tuple[float, float, float],
        size: float,
        color: Tuple[float, float, float],
        view_matrix: np.ndarray,
        projection_matrix: np.ndarray,
        billboard: bool = True,
        rotation: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        scale: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    ):
        """
        Render 3D text in world space.
        
        Args:
            text: Text to render
            font: Font to use
            position: 3D world position
            size: Text size in world units
            color: RGB color (0.0-1.0)
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
            billboard: If True, text faces camera; if False, uses rotation
            rotation: Rotation in degrees (x, y, z) - only used if billboard=False
            scale: Scale factors (x, y, z)
        """
        if not self.initialized or not font:
            return
        
        # Enable blending for text transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Disable depth writing (but keep depth testing) so text doesn't occlude itself
        glDepthMask(GL_FALSE)
        
        # Use text shader
        glUseProgram(self.shader_program)
        
        # Set view and projection matrices
        glUniformMatrix4fv(self.view_loc, 1, GL_FALSE, view_matrix)
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection_matrix)
        
        # Set billboard mode
        glUniform1i(self.billboard_loc, 1 if billboard else 0)
        
        # Set text color
        glUniform3fv(self.text_color_loc, 1, color)
        
        # Activate texture unit
        glActiveTexture(GL_TEXTURE0)
        glUniform1i(self.text_sampler_loc, 0)
        
        # Bind VAO
        glBindVertexArray(self.vao)
        
        # Calculate scale factor once (normalize pixels to world units)
        # This prevents stretching as camera distance changes
        scale_factor = size / font.size
        
        # Calculate starting X position for centering
        text_width = font.get_text_width(text) * scale_factor
        x_offset = -text_width / 2.0  # Center the text
        
        # Render each character
        x = x_offset
        for char in text:
            if char not in font.glyphs:
                continue
            
            glyph = font.glyphs[char]
            
            # Calculate character quad positions (in local space)
            xpos = x + glyph.bearing_x * scale_factor
            ypos = glyph.bearing_y * scale_factor  # Positive for proper orientation
            
            w = glyph.width * scale_factor
            h = glyph.height * scale_factor
            
            # Update VBO for each character
            # Vertices arranged to fix upside-down and horizontal flip
            vertices = np.array([
                [xpos,     ypos,     0.0, 1.0],  # Bottom-left
                [xpos,     ypos - h, 0.0, 0.0],  # Top-left
                [xpos + w, ypos - h, 1.0, 0.0],  # Top-right
                
                [xpos,     ypos,     0.0, 1.0],  # Bottom-left
                [xpos + w, ypos - h, 1.0, 0.0],  # Top-right
                [xpos + w, ypos,     1.0, 1.0]   # Bottom-right
            ], dtype=np.float32)
            
            # Create model matrix with position, rotation, and scale
            model = self._create_model_matrix(position, rotation, scale)
            glUniformMatrix4fv(self.model_loc, 1, GL_FALSE, model)
            
            # Bind glyph texture
            glBindTexture(GL_TEXTURE_2D, glyph.texture_id)
            
            # Update VBO
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            
            # Render quad
            glDrawArrays(GL_TRIANGLES, 0, 6)
            
            # Advance cursor for next glyph (use normalized scale)
            x += (glyph.advance >> 6) * scale_factor  # Bitshift by 6 to get value in pixels
        
        # Unbind
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
        
        # Re-enable depth writing
        glDepthMask(GL_TRUE)
        
        # Disable blending
        glDisable(GL_BLEND)
    
    def _create_model_matrix(
        self,
        position: Tuple[float, float, float],
        rotation: Tuple[float, float, float],
        scale: Tuple[float, float, float]
    ) -> np.ndarray:
        """Create a model matrix from position, rotation, and scale."""
        # Translation matrix
        translation = np.identity(4, dtype=np.float32)
        translation[0, 3] = position[0]
        translation[1, 3] = position[1]
        translation[2, 3] = position[2]
        
        # Rotation matrices (in degrees)
        rx, ry, rz = np.radians(rotation[0]), np.radians(rotation[1]), np.radians(rotation[2])
        
        # Rotation around X
        rot_x = np.identity(4, dtype=np.float32)
        rot_x[1, 1] = np.cos(rx)
        rot_x[1, 2] = -np.sin(rx)
        rot_x[2, 1] = np.sin(rx)
        rot_x[2, 2] = np.cos(rx)
        
        # Rotation around Y
        rot_y = np.identity(4, dtype=np.float32)
        rot_y[0, 0] = np.cos(ry)
        rot_y[0, 2] = np.sin(ry)
        rot_y[2, 0] = -np.sin(ry)
        rot_y[2, 2] = np.cos(ry)
        
        # Rotation around Z
        rot_z = np.identity(4, dtype=np.float32)
        rot_z[0, 0] = np.cos(rz)
        rot_z[0, 1] = -np.sin(rz)
        rot_z[1, 0] = np.sin(rz)
        rot_z[1, 1] = np.cos(rz)
        
        # Scale matrix
        scale_matrix = np.identity(4, dtype=np.float32)
        scale_matrix[0, 0] = scale[0]
        scale_matrix[1, 1] = scale[1]
        scale_matrix[2, 2] = scale[2]
        
        # Combine: T * Rz * Ry * Rx * S
        model = translation @ rot_z @ rot_y @ rot_x @ scale_matrix
        
        return model
    
    def render_text_objects(self, text_objects: List, view_matrix: np.ndarray, projection_matrix: np.ndarray):
        """
        Render multiple Text3D objects.
        
        Args:
            text_objects: List of Text3D objects
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
        """
        for text_obj in text_objects:
            if not text_obj.visible or not text_obj.font or not text_obj.text:
                continue
            
            self.render_text_3d(
                text=text_obj.text,
                font=text_obj.font,
                position=text_obj.position,
                size=text_obj.size,
                color=text_obj.color,
                view_matrix=view_matrix,
                projection_matrix=projection_matrix,
                billboard=text_obj.billboard,
                rotation=tuple(text_obj.transform.rotation),
                scale=tuple(text_obj.transform.scale)
            )
    
    def cleanup(self):
        """Clean up OpenGL resources."""
        if self.vbo:
            glDeleteBuffers(1, [self.vbo])
            self.vbo = None
        
        if self.vao:
            glDeleteVertexArrays(1, [self.vao])
            self.vao = None
        
        if self.shader_program:
            glDeleteProgram(self.shader_program)
            self.shader_program = None
        
        self.initialized = False
        print("[OK] Text3DRenderer cleaned up")
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            if self.initialized:
                self.cleanup()
        except:
            pass  # Ignore errors during cleanup

