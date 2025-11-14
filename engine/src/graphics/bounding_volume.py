"""
Bounding Volume Module
Provides bounding volume calculations for culling and collision detection.
"""

import numpy as np
from typing import Optional, Tuple, List
from .mesh import Mesh
from .vertex import Vertex


class BoundingSphere:
    """Represents a bounding sphere."""
    
    def __init__(self, center: np.ndarray, radius: float):
        """
        Initialize a bounding sphere.
        
        Args:
            center: Sphere center (vec3)
            radius: Sphere radius
        """
        self.center = np.array(center, dtype=np.float32)
        self.radius = float(radius)
    
    def transform(self, matrix: np.ndarray) -> 'BoundingSphere':
        """
        Transform sphere by a 4x4 matrix.
        
        Note: For uniform scale, radius is scaled by the scale factor.
        For non-uniform scale, this is an approximation.
        
        Args:
            matrix: 4x4 transformation matrix
            
        Returns:
            New transformed bounding sphere
        """
        # Transform center
        center_homogeneous = np.array([self.center[0], self.center[1], self.center[2], 1.0])
        transformed_center = (matrix @ center_homogeneous)[:3]
        
        # Approximate radius scaling (using average of scale factors)
        # For uniform scale, this is exact
        scale_x = np.linalg.norm(matrix[0, :3])
        scale_y = np.linalg.norm(matrix[1, :3])
        scale_z = np.linalg.norm(matrix[2, :3])
        avg_scale = (scale_x + scale_y + scale_z) / 3.0
        
        transformed_radius = self.radius * avg_scale
        
        return BoundingSphere(transformed_center, transformed_radius)


class BoundingBox:
    """Represents an Axis-Aligned Bounding Box (AABB)."""
    
    def __init__(self, min_point: np.ndarray, max_point: np.ndarray):
        """
        Initialize an AABB.
        
        Args:
            min_point: Minimum corner (vec3)
            max_point: Maximum corner (vec3)
        """
        self.min_point = np.array(min_point, dtype=np.float32)
        self.max_point = np.array(max_point, dtype=np.float32)
        self._validate()
    
    def _validate(self):
        """Ensure min_point < max_point for all axes."""
        for i in range(3):
            if self.min_point[i] > self.max_point[i]:
                # Swap if invalid
                self.min_point[i], self.max_point[i] = self.max_point[i], self.min_point[i]
    
    @property
    def center(self) -> np.ndarray:
        """Get the center of the bounding box."""
        return (self.min_point + self.max_point) / 2.0
    
    @property
    def size(self) -> np.ndarray:
        """Get the size (width, height, depth) of the bounding box."""
        return self.max_point - self.min_point
    
    @property
    def radius(self) -> float:
        """Get the radius of the bounding sphere that encloses this box."""
        size = self.size
        return np.linalg.norm(size) / 2.0
    
    def get_corners(self) -> List[np.ndarray]:
        """Get all 8 corners of the bounding box."""
        return [
            np.array([self.min_point[0], self.min_point[1], self.min_point[2]]),
            np.array([self.max_point[0], self.min_point[1], self.min_point[2]]),
            np.array([self.min_point[0], self.max_point[1], self.min_point[2]]),
            np.array([self.max_point[0], self.max_point[1], self.min_point[2]]),
            np.array([self.min_point[0], self.min_point[1], self.max_point[2]]),
            np.array([self.max_point[0], self.min_point[1], self.max_point[2]]),
            np.array([self.min_point[0], self.max_point[1], self.max_point[2]]),
            np.array([self.max_point[0], self.max_point[1], self.max_point[2]]),
        ]
    
    def transform(self, matrix: np.ndarray) -> 'BoundingBox':
        """
        Transform AABB by a 4x4 matrix.
        
        This creates an Oriented Bounding Box (OBB), then computes
        a new AABB that encloses it.
        
        Args:
            matrix: 4x4 transformation matrix
            
        Returns:
            New AABB that encloses the transformed box
        """
        corners = self.get_corners()
        
        # Transform all corners
        transformed_corners = []
        for corner in corners:
            corner_homogeneous = np.array([corner[0], corner[1], corner[2], 1.0])
            transformed = (matrix @ corner_homogeneous)[:3]
            transformed_corners.append(transformed)
        
        # Find new min/max
        transformed_corners = np.array(transformed_corners)
        new_min = np.min(transformed_corners, axis=0)
        new_max = np.max(transformed_corners, axis=0)
        
        return BoundingBox(new_min, new_max)
    
    @staticmethod
    def from_mesh(mesh: Mesh) -> 'BoundingBox':
        """
        Calculate AABB from mesh vertices.
        
        Args:
            mesh: Mesh to calculate bounds from
            
        Returns:
            BoundingBox containing all mesh vertices
        """
        if mesh.vertex_count == 0:
            # Return degenerate box at origin
            return BoundingBox(
                np.array([0.0, 0.0, 0.0]),
                np.array([0.0, 0.0, 0.0])
            )
        
        # Get all vertex positions
        positions = []
        for vertex in mesh.vertices:
            positions.append(vertex.position)
        
        positions = np.array(positions)
        
        # Find min/max
        min_point = np.min(positions, axis=0)
        max_point = np.max(positions, axis=0)
        
        return BoundingBox(min_point, max_point)
    
    @staticmethod
    def from_vertices(vertices: List[Vertex]) -> 'BoundingBox':
        """
        Calculate AABB from a list of vertices.
        
        Args:
            vertices: List of vertices
            
        Returns:
            BoundingBox containing all vertices
        """
        if len(vertices) == 0:
            return BoundingBox(
                np.array([0.0, 0.0, 0.0]),
                np.array([0.0, 0.0, 0.0])
            )
        
        positions = np.array([v.position for v in vertices])
        min_point = np.min(positions, axis=0)
        max_point = np.max(positions, axis=0)
        
        return BoundingBox(min_point, max_point)
    
    @staticmethod
    def merge(boxes: List['BoundingBox']) -> 'BoundingBox':
        """
        Create a bounding box that encloses all given boxes.
        
        Args:
            boxes: List of bounding boxes
            
        Returns:
            Merged bounding box
        """
        if len(boxes) == 0:
            return BoundingBox(
                np.array([0.0, 0.0, 0.0]),
                np.array([0.0, 0.0, 0.0])
            )
        
        min_points = np.array([box.min_point for box in boxes])
        max_points = np.array([box.max_point for box in boxes])
        
        merged_min = np.min(min_points, axis=0)
        merged_max = np.max(max_points, axis=0)
        
        return BoundingBox(merged_min, merged_max)


