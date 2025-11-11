"""
Vertex Module
Defines vertex data structure for OpenGL rendering.
"""

import numpy as np
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Vertex:
    """Vertex data structure with position, color, texture coordinates, normal, tangent, and bitangent."""
    
    position: Tuple[float, float, float]
    color: Tuple[float, float, float] = (1.0, 1.0, 1.0)
    texcoord: Optional[Tuple[float, float]] = None
    normal: Optional[Tuple[float, float, float]] = None
    tangent: Optional[Tuple[float, float, float]] = None
    bitangent: Optional[Tuple[float, float, float]] = None
    
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
        
        if self.tangent:
            data.extend(self.tangent)
        else:
            data.extend([1.0, 0.0, 0.0])  # Default tangent (right)
        
        if self.bitangent:
            data.extend(self.bitangent)
        else:
            data.extend([0.0, 0.0, 1.0])  # Default bitangent (forward)
        
        return np.array(data, dtype=np.float32)
    
    @staticmethod
    def get_stride() -> int:
        """
        Get the stride (size in bytes) of a vertex.
        
        Returns:
            Vertex stride in bytes
        """
        # Position (3) + Color (3) + TexCoord (2) + Normal (3) + Tangent (3) + Bitangent (3) = 17 floats
        return 17 * 4  # 68 bytes
    
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
    
    @staticmethod
    def get_tangent_offset() -> int:
        """Get byte offset for tangent attribute."""
        return 11 * 4  # After position (3) + color (3) + texcoord (2) + normal (3)
    
    @staticmethod
    def get_bitangent_offset() -> int:
        """Get byte offset for bitangent attribute."""
        return 14 * 4  # After position (3) + color (3) + texcoord (2) + normal (3) + tangent (3)


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


def calculate_tangents(vertices: List[Vertex], indices: Optional[List[int]] = None) -> List[Vertex]:
    """
    Calculate tangent and bitangent vectors for vertices.
    Uses the method described in: http://www.opengl-tutorial.org/intermediate-tutorials/tutorial-13-normal-mapping/
    
    Args:
        vertices: List of vertices with positions, texcoords, and normals
        indices: Optional index list (if None, assumes sequential triangles)
        
    Returns:
        List of vertices with calculated tangents and bitangents
    """
    # Initialize tangent and bitangent accumulators
    tangents = [np.zeros(3, dtype=np.float32) for _ in vertices]
    bitangents = [np.zeros(3, dtype=np.float32) for _ in vertices]
    
    # Process triangles
    if indices:
        # Use indexed triangles
        for i in range(0, len(indices), 3):
            if i + 2 >= len(indices):
                break
            
            i0, i1, i2 = indices[i], indices[i + 1], indices[i + 2]
            if i0 >= len(vertices) or i1 >= len(vertices) or i2 >= len(vertices):
                continue
            
            _calculate_triangle_tangent(vertices, i0, i1, i2, tangents, bitangents)
    else:
        # Use sequential triangles
        for i in range(0, len(vertices), 3):
            if i + 2 >= len(vertices):
                break
            
            _calculate_triangle_tangent(vertices, i, i + 1, i + 2, tangents, bitangents)
    
    # Normalize and apply to vertices
    result = []
    for i, vertex in enumerate(vertices):
        # Gram-Schmidt orthogonalize tangent with respect to normal
        normal = np.array(vertex.normal if vertex.normal else [0, 1, 0], dtype=np.float32)
        tangent = tangents[i]
        
        # Orthogonalize
        tangent = tangent - normal * np.dot(normal, tangent)
        
        # Normalize
        t_len = np.linalg.norm(tangent)
        if t_len > 0:
            tangent = tangent / t_len
        
        # Normalize bitangent
        bitangent = bitangents[i]
        b_len = np.linalg.norm(bitangent)
        if b_len > 0:
            bitangent = bitangent / b_len
        
        # Create new vertex with tangent and bitangent
        new_vertex = Vertex(
            position=vertex.position,
            color=vertex.color,
            texcoord=vertex.texcoord,
            normal=vertex.normal,
            tangent=tuple(tangent),
            bitangent=tuple(bitangent)
        )
        result.append(new_vertex)
    
    return result


def _calculate_triangle_tangent(vertices: List[Vertex], i0: int, i1: int, i2: int, 
                                tangents: List[np.ndarray], bitangents: List[np.ndarray]):
    """
    Calculate tangent and bitangent for a single triangle.
    
    Args:
        vertices: List of all vertices
        i0, i1, i2: Indices of the triangle vertices
        tangents: Accumulator list for tangents
        bitangents: Accumulator list for bitangents
    """
    v0, v1, v2 = vertices[i0], vertices[i1], vertices[i2]
    
    # Positions
    pos0 = np.array(v0.position, dtype=np.float32)
    pos1 = np.array(v1.position, dtype=np.float32)
    pos2 = np.array(v2.position, dtype=np.float32)
    
    # UV coordinates
    uv0 = np.array(v0.texcoord if v0.texcoord else [0, 0], dtype=np.float32)
    uv1 = np.array(v1.texcoord if v1.texcoord else [0, 0], dtype=np.float32)
    uv2 = np.array(v2.texcoord if v2.texcoord else [0, 0], dtype=np.float32)
    
    # Edges
    delta_pos1 = pos1 - pos0
    delta_pos2 = pos2 - pos0
    delta_uv1 = uv1 - uv0
    delta_uv2 = uv2 - uv0
    
    # Calculate tangent and bitangent
    denom = delta_uv1[0] * delta_uv2[1] - delta_uv1[1] * delta_uv2[0]
    
    if abs(denom) > 1e-6:  # Avoid division by zero
        r = 1.0 / denom
        tangent = (delta_pos1 * delta_uv2[1] - delta_pos2 * delta_uv1[1]) * r
        bitangent = (delta_pos2 * delta_uv1[0] - delta_pos1 * delta_uv2[0]) * r
        
        # Accumulate for all three vertices of the triangle
        tangents[i0] += tangent
        tangents[i1] += tangent
        tangents[i2] += tangent
        
        bitangents[i0] += bitangent
        bitangents[i1] += bitangent
        bitangents[i2] += bitangent
