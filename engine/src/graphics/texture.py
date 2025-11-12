"""
Texture Module
Handles texture loading and management for OpenGL.
"""

from OpenGL.GL import *  # type: ignore
from PIL import Image
import numpy as np
from typing import Optional
import os


class Texture:
    """Represents an OpenGL texture."""
    
    def __init__(self, filepath: Optional[str] = None):
        """
        Initialize a texture.
        
        Args:
            filepath: Optional path to texture file
        """
        self.texture_id: Optional[int] = None
        self.width: int = 0
        self.height: int = 0
        self.channels: int = 0
        self.filepath = filepath
        
        if filepath:
            self.load(filepath)
    
    def load(self, filepath: str) -> bool:
        """
        Load a texture from file.
        
        Args:
            filepath: Path to image file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not os.path.exists(filepath):
                print(f"ERROR: Texture file not found: {filepath}")
                return False
            
            # Load image
            img = Image.open(filepath)
            
            # Convert to RGB/RGBA
            if img.mode == 'RGB':
                img_data = img.convert('RGB')
                gl_format = GL_RGB
                self.channels = 3
            elif img.mode == 'RGBA':
                img_data = img.convert('RGBA')
                gl_format = GL_RGBA
                self.channels = 4
            else:
                img_data = img.convert('RGB')
                gl_format = GL_RGB
                self.channels = 3
            
            # Flip image (OpenGL expects origin at bottom-left)
            img_data = img_data.transpose(Image.FLIP_TOP_BOTTOM)
            
            self.width = img.width
            self.height = img.height
            
            # Generate texture
            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            
            # Set texture parameters
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            
            # Upload texture data
            glTexImage2D(
                GL_TEXTURE_2D, 0, gl_format,
                self.width, self.height, 0,
                gl_format, GL_UNSIGNED_BYTE,
                np.array(img_data, dtype=np.uint8)
            )
            
            # Generate mipmaps
            glGenerateMipmap(GL_TEXTURE_2D)
            
            # Unbind
            glBindTexture(GL_TEXTURE_2D, 0)
            
            print(f"[OK] Texture loaded: {filepath} ({self.width}x{self.height}, {self.channels} channels)")
            return True
            
        except Exception as e:
            print(f"ERROR: Failed to load texture '{filepath}': {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def bind(self, texture_unit: int = 0):
        """
        Bind this texture to a texture unit.
        
        Args:
            texture_unit: Texture unit (0-31)
        """
        if self.texture_id:
            glActiveTexture(GL_TEXTURE0 + texture_unit)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
    
    def unbind(self):
        """Unbind this texture."""
        glBindTexture(GL_TEXTURE_2D, 0)
    
    def cleanup(self):
        """Clean up texture resources."""
        if self.texture_id:
            glDeleteTextures(1, [self.texture_id])
            self.texture_id = None
    
    @staticmethod
    def create_white_texture() -> 'Texture':
        """
        Create a simple white 1x1 texture (useful as default).
        
        Returns:
            White texture
        """
        texture = Texture()
        texture.width = 1
        texture.height = 1
        texture.channels = 3
        
        # Generate texture
        texture.texture_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture.texture_id)
        
        # White pixel
        white_pixel = np.array([255, 255, 255], dtype=np.uint8)
        
        glTexImage2D(
            GL_TEXTURE_2D, 0, GL_RGB,
            1, 1, 0,
            GL_RGB, GL_UNSIGNED_BYTE,
            white_pixel
        )
        
        glBindTexture(GL_TEXTURE_2D, 0)
        
        return texture
    
    def __repr__(self) -> str:
        """String representation."""
        return f"Texture(id={self.texture_id}, size={self.width}x{self.height})"

