"""
Octree Spatial Partitioning Module
Implements an Octree data structure for efficient spatial queries and frustum culling.
"""

import numpy as np
from typing import List, Optional, Callable, TYPE_CHECKING
from enum import IntEnum

if TYPE_CHECKING:
    from ..scene.gameobject import GameObject
    from ..rendering.frustum import Frustum


class OctreeResult(IntEnum):
    """Result of octree query."""
    OUTSIDE = 0
    INTERSECT = 1
    INSIDE = 2


class OctreeNode:
    """Represents a node in the Octree."""
    
    def __init__(
        self,
        center: np.ndarray,
        half_size: float,
        parent: Optional['OctreeNode'] = None,
        depth: int = 0,
        max_depth: int = 8,
        max_objects: int = 10
    ):
        """
        Initialize an octree node.
        
        Args:
            center: Center point of the node's bounding box (vec3)
            half_size: Half the size of the node (creates cube from center ± half_size)
            parent: Parent node (None for root)
            depth: Current depth in the tree
            max_depth: Maximum depth before stopping subdivision
            max_objects: Maximum objects per node before subdividing
        """
        self.center = np.array(center, dtype=np.float32)
        self.half_size = float(half_size)
        self.parent = parent
        self.depth = depth
        self.max_depth = max_depth
        self.max_objects = max_objects
        
        # Calculate bounding box
        self.min_point = self.center - self.half_size
        self.max_point = self.center + self.half_size
        
        # Node data
        self.objects: List['GameObject'] = []
        self.children: List[Optional['OctreeNode']] = [None] * 8
        self.is_leaf = True
        
    def get_bounding_box(self) -> tuple[np.ndarray, np.ndarray]:
        """Get the bounding box of this node."""
        return (self.min_point.copy(), self.max_point.copy())
    
    def contains_point(self, point: np.ndarray) -> bool:
        """Check if a point is inside this node's bounds."""
        return np.all(point >= self.min_point) and np.all(point <= self.max_point)
    
    def intersects_aabb(
        self,
        min_point: np.ndarray,
        max_point: np.ndarray
    ) -> bool:
        """
        Check if an AABB intersects this node's bounds.
        
        Args:
            min_point: AABB minimum point
            max_point: AABB maximum point
            
        Returns:
            True if AABB intersects this node
        """
        # Check if AABB is completely outside
        if np.any(max_point < self.min_point) or np.any(min_point > self.max_point):
            return False
        return True
    
    def get_octant(self, point: np.ndarray) -> int:
        """
        Determine which octant a point belongs to.
        
        Returns:
            Octant index (0-7):
            0: -X, -Y, -Z (left, bottom, back)
            1: +X, -Y, -Z (right, bottom, back)
            2: -X, +Y, -Z (left, top, back)
            3: +X, +Y, -Z (right, top, back)
            4: -X, -Y, +Z (left, bottom, front)
            5: +X, -Y, +Z (right, bottom, front)
            6: -X, +Y, +Z (left, top, front)
            7: +X, +Y, +Z (right, top, front)
        """
        octant = 0
        if point[0] >= self.center[0]:
            octant |= 1  # +X
        if point[1] >= self.center[1]:
            octant |= 2  # +Y
        if point[2] >= self.center[2]:
            octant |= 4  # +Z
        return octant
    
    def subdivide(self):
        """Subdivide this node into 8 children."""
        if not self.is_leaf or self.depth >= self.max_depth:
            return
        
        child_half_size = self.half_size * 0.5
        
        # Create 8 children
        for i in range(8):
            # Calculate child center based on octant
            child_center = self.center.copy()
            if i & 1:  # +X
                child_center[0] += child_half_size
            else:  # -X
                child_center[0] -= child_half_size
            
            if i & 2:  # +Y
                child_center[1] += child_half_size
            else:  # -Y
                child_center[1] -= child_half_size
            
            if i & 4:  # +Z
                child_center[2] += child_half_size
            else:  # -Z
                child_center[2] -= child_half_size
            
            self.children[i] = OctreeNode(
                child_center,
                child_half_size,
                self,
                self.depth + 1,
                self.max_depth,
                self.max_objects
            )
        
        self.is_leaf = False
        
        # Redistribute objects to children
        objects_to_redistribute = self.objects.copy()
        self.objects.clear()
        
        for obj in objects_to_redistribute:
            self._insert_object(obj)
    
    def _insert_object(self, game_object: 'GameObject') -> bool:
        """
        Insert an object into this node or its children.
        
        Args:
            game_object: GameObject to insert
            
        Returns:
            True if inserted successfully
        """
        # Get object's bounding box
        if not game_object.model:
            return False
        
        model_matrix = game_object.get_model_matrix()
        bounds = game_object.model.get_bounding_box(model_matrix)
        
        # Check if object fits in this node
        if not self.intersects_aabb(bounds.min_point, bounds.max_point):
            return False
        
        # If this is a leaf and we have space, add it here
        if self.is_leaf:
            if len(self.objects) < self.max_objects:
                self.objects.append(game_object)
                return True
            else:
                # Need to subdivide
                self.subdivide()
        
        # Try to insert into children
        if not self.is_leaf:
            inserted = False
            for child in self.children:
                if child and child._insert_object(game_object):
                    inserted = True
                    break
            
            # If object spans multiple children, keep it in this node
            if not inserted:
                self.objects.append(game_object)
                return True
        
        return False
    
    def query_frustum(
        self,
        frustum: 'Frustum',
        result: List['GameObject']
    ):
        """
        Query all objects that intersect with the frustum.
        
        Args:
            frustum: Frustum to test against
            result: List to append results to
        """
        if not frustum.is_initialized():
            # If frustum not initialized, return all objects
            result.extend(self.objects)
            if not self.is_leaf:
                for child in self.children:
                    if child:
                        child.query_frustum(frustum, result)
            return
        
        # Test this node's bounding box against frustum
        node_result = frustum.test_aabb(self.min_point, self.max_point)
        
        if node_result == OctreeResult.OUTSIDE:
            # Entire node is outside frustum, skip it
            return
        
        # Add objects in this node
        result.extend(self.objects)
        
        # Recursively query children
        if not self.is_leaf:
            for child in self.children:
                if child:
                    child.query_frustum(frustum, result)
    
    def query_aabb(
        self,
        min_point: np.ndarray,
        max_point: np.ndarray,
        result: List['GameObject']
    ):
        """
        Query all objects that intersect with an AABB.
        
        Args:
            min_point: AABB minimum point
            max_point: AABB maximum point
            result: List to append results to
        """
        # Check if query AABB intersects this node
        if not self.intersects_aabb(min_point, max_point):
            return
        
        # Add objects in this node
        result.extend(self.objects)
        
        # Recursively query children
        if not self.is_leaf:
            for child in self.children:
                if child:
                    child.query_aabb(min_point, max_point, result)
    
    def query_sphere(
        self,
        center: np.ndarray,
        radius: float,
        result: List['GameObject']
    ):
        """
        Query all objects that intersect with a sphere.
        
        Args:
            center: Sphere center
            radius: Sphere radius
            result: List to append results to
        """
        # Simple AABB-sphere intersection test
        # Create AABB around sphere
        sphere_min = center - radius
        sphere_max = center + radius
        
        if not self.intersects_aabb(sphere_min, sphere_max):
            return
        
        # Add objects in this node
        result.extend(self.objects)
        
        # Recursively query children
        if not self.is_leaf:
            for child in self.children:
                if child:
                    child.query_sphere(center, radius, result)
    
    def clear(self):
        """Clear all objects and children from this node."""
        self.objects.clear()
        if not self.is_leaf:
            for i in range(8):
                if self.children[i]:
                    self.children[i].clear()
                    self.children[i] = None
        self.is_leaf = True
    
    def get_statistics(self) -> dict:
        """
        Get statistics about this node and its children.
        
        Returns:
            Dictionary with statistics
        """
        stats = {
            'node_count': 1,
            'leaf_count': 1 if self.is_leaf else 0,
            'object_count': len(self.objects),
            'max_depth': self.depth,
            'total_objects': len(self.objects)
        }
        
        if not self.is_leaf:
            for child in self.children:
                if child:
                    child_stats = child.get_statistics()
                    stats['node_count'] += child_stats['node_count']
                    stats['leaf_count'] += child_stats['leaf_count']
                    stats['total_objects'] += child_stats['total_objects']
                    stats['max_depth'] = max(stats['max_depth'], child_stats['max_depth'])
        
        return stats


class Octree:
    """
    Octree spatial partitioning structure for efficient spatial queries.
    
    Divides 3D space into hierarchical octants to accelerate spatial queries
    like frustum culling, collision detection, and range queries.
    """
    
    def __init__(
        self,
        center: np.ndarray,
        size: float,
        max_depth: int = 8,
        max_objects_per_node: int = 10
    ):
        """
        Initialize the Octree.
        
        Args:
            center: Center point of the root node's bounding box (vec3)
            size: Total size of the root node (creates cube from center ± size/2)
            max_depth: Maximum depth of the tree (default: 8)
            max_objects_per_node: Maximum objects per node before subdividing (default: 10)
        """
        half_size = size * 0.5
        self.root = OctreeNode(
            center,
            half_size,
            None,
            0,
            max_depth,
            max_objects_per_node
        )
        self.max_depth = max_depth
        self.max_objects_per_node = max_objects_per_node
        self._object_to_node: dict = {}  # Track which node contains each object
    
    def insert(self, game_object: 'GameObject') -> bool:
        """
        Insert a game object into the octree.
        
        Args:
            game_object: GameObject to insert
            
        Returns:
            True if inserted successfully
        """
        if game_object in self._object_to_node:
            # Object already in tree, remove it first
            self.remove(game_object)
        
        if self.root._insert_object(game_object):
            self._object_to_node[game_object] = self.root
            return True
        return False
    
    def remove(self, game_object: 'GameObject') -> bool:
        """
        Remove a game object from the octree.
        
        Args:
            game_object: GameObject to remove
            
        Returns:
            True if removed successfully
        """
        # Find and remove from the node
        # Since we track objects, we can search efficiently
        if game_object in self._object_to_node:
            node = self._object_to_node[game_object]
            if game_object in node.objects:
                node.objects.remove(game_object)
            del self._object_to_node[game_object]
            return True
        return False
    
    def clear(self):
        """Clear all objects from the octree."""
        self.root.clear()
        self._object_to_node.clear()
    
    def rebuild(self, objects: List['GameObject']):
        """
        Rebuild the octree with a new set of objects.
        
        Args:
            objects: List of GameObjects to insert
        """
        self.clear()
        for obj in objects:
            self.insert(obj)
    
    def query_frustum(
        self,
        frustum: 'Frustum'
    ) -> List['GameObject']:
        """
        Query all objects that intersect with the frustum.
        
        Args:
            frustum: Frustum to test against
            
        Returns:
            List of active GameObjects that intersect the frustum
        """
        result: List['GameObject'] = []
        self.root.query_frustum(frustum, result)
        # Remove duplicates (objects that span multiple nodes) and filter for active objects
        unique_results = list(dict.fromkeys(result))  # Preserves order while removing duplicates
        return [obj for obj in unique_results if obj.active]
    
    def query_aabb(
        self,
        min_point: np.ndarray,
        max_point: np.ndarray
    ) -> List['GameObject']:
        """
        Query all objects that intersect with an AABB.
        
        Args:
            min_point: AABB minimum point
            max_point: AABB maximum point
            
        Returns:
            List of GameObjects that intersect the AABB
        """
        result: List['GameObject'] = []
        self.root.query_aabb(min_point, max_point, result)
        # Remove duplicates
        return list(dict.fromkeys(result))
    
    def query_sphere(
        self,
        center: np.ndarray,
        radius: float
    ) -> List['GameObject']:
        """
        Query all objects that intersect with a sphere.
        
        Args:
            center: Sphere center
            radius: Sphere radius
            
        Returns:
            List of GameObjects that intersect the sphere
        """
        result: List['GameObject'] = []
        self.root.query_sphere(center, radius, result)
        # Remove duplicates
        return list(dict.fromkeys(result))
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the octree.
        
        Returns:
            Dictionary with statistics
        """
        return self.root.get_statistics()
    
    def get_bounding_box(self) -> tuple[np.ndarray, np.ndarray]:
        """Get the bounding box of the root node."""
        return self.root.get_bounding_box()

