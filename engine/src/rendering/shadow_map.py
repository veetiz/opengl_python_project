"""
Shadow Map Module
Manages shadow map framebuffers and depth textures.
"""

from OpenGL.GL import *
import numpy as np


class ShadowMap:
    """
    Shadow map for storing depth information from a light's perspective.
    Supports both 2D textures (directional/spot lights) and cubemaps (point lights).
    """
    
    def __init__(self, width: int = 1024, height: int = 1024, is_cubemap: bool = False):
        """
        Initialize a shadow map.
        
        Args:
            width: Shadow map width in pixels
            height: Shadow map height in pixels
            is_cubemap: Whether this is a cubemap (for point lights)
        """
        self.width = width
        self.height = height
        self.is_cubemap = is_cubemap
        
        self.fbo = None
        self.depth_texture = None
        
        self._create_framebuffer()
    
    def _create_framebuffer(self):
        """Create the framebuffer and depth texture."""
        try:
            # Create framebuffer
            self.fbo = glGenFramebuffers(1)
            glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
            
            # Create depth texture
            if self.is_cubemap:
                # Cubemap for point lights
                self.depth_texture = glGenTextures(1)
                glBindTexture(GL_TEXTURE_CUBE_MAP, self.depth_texture)
                
                for i in range(6):
                    glTexImage2D(
                        GL_TEXTURE_CUBE_MAP_POSITIVE_X + i,
                        0, GL_DEPTH_COMPONENT,
                        self.width, self.height,
                        0, GL_DEPTH_COMPONENT, GL_FLOAT, None
                    )
                
                glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
                glTexParameteri(GL_TEXTURE_CUBE_MAP, GL_TEXTURE_WRAP_R, GL_CLAMP_TO_EDGE)
                
                glFramebufferTexture(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, self.depth_texture, 0)
            else:
                # 2D texture for directional/spot lights
                self.depth_texture = glGenTextures(1)
                glBindTexture(GL_TEXTURE_2D, self.depth_texture)
                
                glTexImage2D(
                    GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT,
                    self.width, self.height,
                    0, GL_DEPTH_COMPONENT, GL_FLOAT, None
                )
                
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
                
                # Set border color to maximum depth (1.0) so areas outside shadow map aren't in shadow
                border_color = [1.0, 1.0, 1.0, 1.0]
                glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)
                
                glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, self.depth_texture, 0)
            
            # Tell OpenGL we're not using any color data
            glDrawBuffer(GL_NONE)
            glReadBuffer(GL_NONE)
            
            # Check framebuffer completeness
            if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
                print("ERROR: Shadow map framebuffer is not complete!")
                return False
            
            # Unbind framebuffer
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            
            print(f"[OK] Shadow map created: {'Cubemap' if self.is_cubemap else '2D'} {self.width}x{self.height}")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to create shadow map: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def bind(self):
        """Bind the shadow map framebuffer for rendering."""
        if self.fbo:
            glBindFramebuffer(GL_FRAMEBUFFER, self.fbo)
            glViewport(0, 0, self.width, self.height)
            glClear(GL_DEPTH_BUFFER_BIT)
    
    def unbind(self):
        """Unbind the shadow map framebuffer."""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def bind_texture(self, texture_unit: int = 0):
        """
        Bind the shadow map texture for sampling in shaders.
        
        Args:
            texture_unit: Texture unit to bind to (0-31)
        """
        if self.depth_texture:
            glActiveTexture(GL_TEXTURE0 + texture_unit)
            if self.is_cubemap:
                glBindTexture(GL_TEXTURE_CUBE_MAP, self.depth_texture)
            else:
                glBindTexture(GL_TEXTURE_2D, self.depth_texture)
    
    def cleanup(self):
        """Clean up OpenGL resources."""
        if self.depth_texture:
            glDeleteTextures(1, [self.depth_texture])
            self.depth_texture = None
        
        if self.fbo:
            glDeleteFramebuffers(1, [self.fbo])
            self.fbo = None
    
    def __del__(self):
        """Destructor to ensure cleanup."""
        try:
            self.cleanup()
        except:
            pass  # Ignore errors during cleanup

