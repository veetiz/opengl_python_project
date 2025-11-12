"""
Text Renderer Module
Low-level OpenGL text rendering engine.
"""

from OpenGL.GL import *  # type: ignore
from OpenGL.GL.shaders import compileProgram, compileShader  # type: ignore
import numpy as np
from typing import Optional, Tuple, List
import os
from .font import Font


class TextRenderer:
    """
    Low-level text rendering engine that handles OpenGL setup and rendering.
    This class manages shaders, buffers, and the actual drawing of text.
    """
    
    def __init__(self):
        """Initialize text renderer."""
        self.shader_program: Optional[int] = None
        self.vao: Optional[int] = None
        self.vbo: Optional[int] = None
        self.projection_loc: Optional[int] = None
        self.text_color_loc: Optional[int] = None
        self.text_sampler_loc: Optional[int] = None
        self.initialized = False
        self.screen_width = 0
        self.screen_height = 0
        
    def init(self, screen_width: int, screen_height: int) -> bool:
        """
        Initialize text rendering system.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Load text shaders
            if not self._load_shaders():
                return False
            
            # Get uniform locations
            self.projection_loc = glGetUniformLocation(self.shader_program, "projection")
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
            glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 4 * 4, None)
            
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
            
            # Mark as initialized BEFORE setting projection (so it doesn't return early)
            self.initialized = True
            
            # Set initial projection
            self.set_projection(screen_width, screen_height)
            
            print("[OK] TextRenderer initialized")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to initialize TextRenderer: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _load_shaders(self) -> bool:
        """Load and compile text shaders."""
        try:
            vert_path = "shaders/text.vert.glsl"
            frag_path = "shaders/text.frag.glsl"
            
            if not os.path.exists(vert_path):
                print(f"ERROR: Text vertex shader not found: {vert_path}")
                return False
            
            if not os.path.exists(frag_path):
                print(f"ERROR: Text fragment shader not found: {frag_path}")
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
            
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to load text shaders: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def set_projection(self, width: int, height: int):
        """
        Update orthographic projection matrix for screen coordinates.
        
        Args:
            width: Screen width in pixels
            height: Screen height in pixels
        """
        if not self.initialized or not self.shader_program:
            return
        
        if width <= 0 or height <= 0:
            print(f"[TEXT_RENDERER] ERROR: Invalid dimensions {width}x{height}")
            return
        
        self.screen_width = width
        self.screen_height = height
        
        # Create orthographic projection (0,0 at top-left)
        # Maps screen coordinates to NDC: x: [0, width] -> [-1, 1], y: [0, height] -> [1, -1]
        projection = np.array([
            [2.0/width,        0.0,              0.0,  -1.0],
            [0.0,              -2.0/height,      0.0,   1.0],
            [0.0,              0.0,             -1.0,   0.0],
            [0.0,              0.0,              0.0,   1.0]
        ], dtype=np.float32).T  # Transpose for column-major order in OpenGL
        
        glUseProgram(self.shader_program)
        glUniformMatrix4fv(self.projection_loc, 1, GL_FALSE, projection)
        glUseProgram(0)
    
    def render_text(self, font: Font, text: str, x: float, y: float, 
                   scale: float = 1.0, color: Tuple[float, float, float] = (1.0, 1.0, 1.0)):
        """
        Render text at screen position.
        
        Args:
            font: Font to use
            text: Text string to render
            x: X position (pixels, left edge)
            y: Y position (pixels, top edge)
            scale: Scale factor (1.0 = normal size)
            color: RGB color tuple (0.0-1.0)
        """
        if not self.initialized or not self.shader_program:
            return
        
        if not font or not text:
            return
        
        # Enable blending for text transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Disable depth test for 2D text
        depth_test_enabled = glIsEnabled(GL_DEPTH_TEST)
        if depth_test_enabled:
            glDisable(GL_DEPTH_TEST)
        
        # Use text shader
        glUseProgram(self.shader_program)
        glUniform3f(self.text_color_loc, color[0], color[1], color[2])
        glUniform1i(self.text_sampler_loc, 0)
        glActiveTexture(GL_TEXTURE0)
        
        glBindVertexArray(self.vao)
        
        # Render each character
        current_x = x
        chars_rendered = 0
        for char in text:
            glyph = font.get_glyph(char)
            if not glyph:
                continue
            
            # Skip rendering for empty glyphs (like space)
            if glyph.texture_id == 0:
                current_x += (glyph.advance >> 6) * scale
                continue
            
            chars_rendered += 1
            
            # Calculate glyph position and size
            # Baseline alignment: y is the baseline, glyphs align properly
            xpos = current_x + glyph.bearing_x * scale
            # bearing_y = distance from baseline to top of glyph
            # Top of glyph should be at: y - bearing_y (in screen coords, down is positive)
            ypos = y - glyph.bearing_y * scale
            
            w = glyph.width * scale
            h = glyph.height * scale
            
            # Update VBO for each character
            # Image is already flipped in font_loader, so use normal texture coords
            vertices = np.array([
                [xpos,     ypos + h,   0.0, 0.0],  # bottom-left (at baseline y)
                [xpos,     ypos,       0.0, 1.0],  # top-left
                [xpos + w, ypos,       1.0, 1.0],  # top-right
                
                [xpos,     ypos + h,   0.0, 0.0],  # bottom-left (at baseline y)
                [xpos + w, ypos,       1.0, 1.0],  # top-right
                [xpos + w, ypos + h,   1.0, 0.0]   # bottom-right (at baseline y)
            ], dtype=np.float32)
            
            # Bind glyph texture
            glBindTexture(GL_TEXTURE_2D, glyph.texture_id)
            
            # Update VBO
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferSubData(GL_ARRAY_BUFFER, 0, vertices.nbytes, vertices)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            
            # Render quad
            glDrawArrays(GL_TRIANGLES, 0, 6)
            
            # Advance cursor (bitshift by 6 to get value in pixels)
            current_x += (glyph.advance >> 6) * scale
        
        glBindVertexArray(0)
        glBindTexture(GL_TEXTURE_2D, 0)
        glUseProgram(0)
        
        # Re-enable depth test if it was enabled
        if depth_test_enabled:
            glEnable(GL_DEPTH_TEST)
        glDisable(GL_BLEND)
    
    def render_text_objects(self, text_objects: List):
        """
        Render multiple text objects.
        
        Args:
            text_objects: List of Text2D objects to render
        """
        for text_obj in text_objects:
            if not text_obj.visible:
                continue
            
            if not text_obj.font or not text_obj.text:
                continue
            
            self.render_text(
                font=text_obj.font,
                text=text_obj.text,
                x=text_obj.x,
                y=text_obj.y,
                scale=text_obj.scale,
                color=text_obj.color
            )
    
    def cleanup(self):
        """Clean up OpenGL resources."""
        try:
            if self.vbo:
                glDeleteBuffers(1, [self.vbo])
            if self.vao:
                glDeleteVertexArrays(1, [self.vao])
            if self.shader_program:
                glDeleteProgram(self.shader_program)
            
            self.initialized = False
            print("[OK] TextRenderer cleaned up")
            
        except Exception as e:
            print(f"ERROR: Failed to cleanup TextRenderer: {e}")

