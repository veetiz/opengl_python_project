"""
Mesh Module
Defines mesh data structure for storing vertex and index data.
"""

import numpy as np
from typing import List, Optional, TYPE_CHECKING
from .vertex import Vertex, vertices_to_array

if TYPE_CHECKING:
    from .texture import Texture


class Mesh:
    """Mesh class to hold vertex and index buffer data."""
    
    def __init__(self, vertices: List[Vertex], indices: Optional[List[int]] = None, texture: Optional['Texture'] = None):
        """
        Initialize a mesh.
        
        Args:
            vertices: List of Vertex objects
            indices: Optional list of indices for indexed rendering
            texture: Optional texture to apply to this mesh
        """
        self.vertices = vertices
        self.indices = indices if indices is not None else []
        self.texture = texture
        
        # Convert to numpy arrays for rendering
        self.vertex_data = vertices_to_array(vertices)
        self.index_data = np.array(indices, dtype=np.uint32) if indices else np.array([], dtype=np.uint32)
        
        # Buffer handles (will be set by renderer)
        self.vbo = None  # Vertex Buffer Object (OpenGL)
        self.ebo = None  # Element Buffer Object (OpenGL)
    
    @property
    def vertex_count(self) -> int:
        """Get the number of vertices."""
        return len(self.vertices)
    
    @property
    def index_count(self) -> int:
        """Get the number of indices."""
        return len(self.indices)
    
    @property
    def has_indices(self) -> bool:
        """Check if the mesh uses indexed rendering."""
        return len(self.indices) > 0
    
    @staticmethod
    def create_triangle() -> 'Mesh':
        """
        Create a simple colored triangle mesh.
        
        Returns:
            Triangle mesh with colored vertices
        """
        vertices = [
            Vertex(position=(0.0, -0.5, 0.0), color=(1.0, 0.0, 0.0)),   # Top - Red
            Vertex(position=(0.5, 0.5, 0.0), color=(0.0, 1.0, 0.0)),    # Bottom Right - Green
            Vertex(position=(-0.5, 0.5, 0.0), color=(0.0, 0.0, 1.0))    # Bottom Left - Blue
        ]
        return Mesh(vertices)
    
    @staticmethod
    def create_quad() -> 'Mesh':
        """
        Create a simple colored quad (rectangle) mesh with indexed rendering.
        
        Returns:
            Quad mesh with colored vertices and indices
        """
        vertices = [
            Vertex(position=(-0.5, -0.5, 0.0), color=(1.0, 0.0, 0.0)),  # Top Left - Red
            Vertex(position=(0.5, -0.5, 0.0), color=(0.0, 1.0, 0.0)),   # Top Right - Green
            Vertex(position=(0.5, 0.5, 0.0), color=(0.0, 0.0, 1.0)),    # Bottom Right - Blue
            Vertex(position=(-0.5, 0.5, 0.0), color=(1.0, 1.0, 0.0))    # Bottom Left - Yellow
        ]
        indices = [0, 1, 2, 2, 3, 0]  # Two triangles
        return Mesh(vertices, indices)
    

