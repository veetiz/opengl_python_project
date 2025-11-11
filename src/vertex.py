"""
Vertex Module
Defines vertex data structure for OpenGL rendering.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Vertex:
    """Vertex data structure with position, color, and optional texture coordinates."""
    
    position: Tuple[float, float, float]
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    texcoord: Optional[Tuple[float, float]] = None
    normal: Optional[Tuple[float, float, float]] = None
    
    def to_array(self) -> np.ndarray:
        """
        Convert vertex to numpy array.
        
        Returns:
            Numpy array of vertex data
        """
        data = [*self.position, *self.color]
        
        if self.texcoord:
            data.extend(self.texcoord)
        else:
            data.extend([0.0, 0.0])  # Default UV
        
        if self.normal:
            data.extend(self.normal)
        else:
            data.extend([0.0, 1.0, 0.0])  # Default normal (up)
        
        return np.array(data, dtype=np.float32)
    
    @staticmethod
    def get_stride() -> int:
        """
        Get the stride (size in bytes) of a vertex.
        
        Returns:
            Vertex stride in bytes
        """
        # Position (3) + Color (3) + TexCoord (2) + Normal (3) = 11 floats
        return 11 * 4  # 44 bytes
    
    @staticmethod
    def get_position_offset() -> int:
        """Get byte offset for position attribute."""
        return 0
    
    @staticmethod
    def get_color_offset() -> int:
        """Get byte offset for color attribute."""
        return 3 * 4  # After position (3 floats)
    
    @staticmethod
    def get_texcoord_offset() -> int:
        """Get byte offset for texture coordinate attribute."""
        return 6 * 4  # After position (3) + color (3)
    
    @staticmethod
    def get_normal_offset() -> int:
        """Get byte offset for normal attribute."""
        return 8 * 4  # After position (3) + color (3) + texcoord (2)


def vertices_to_array(vertices: List[Vertex]) -> np.ndarray:
    """
    Convert a list of vertices to a single numpy array.
    
    Args:
        vertices: List of Vertex objects
        
    Returns:
        Flat numpy array of all vertex data
    """
    if not vertices:
        return np.array([], dtype=np.float32)
    
    return np.concatenate([v.to_array() for v in vertices])
