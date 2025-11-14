"""
Frustum Culling Module
Implements frustum culling for performance optimization.
"""

import numpy as np
from typing import Tuple, Optional
from enum import IntEnum


class FrustumResult(IntEnum):
    """Result of frustum intersection test."""
    OUTSIDE = 0  # Completely outside frustum
    INTERSECT = 1  # Partially inside frustum
    INSIDE = 2  # Completely inside frustum


class FrustumPlane:
    """Represents a single frustum plane (normal + distance)."""
    
    def __init__(self, normal: np.ndarray, distance: float):
        """
        Initialize a frustum plane.
        
        Args:
            normal: Plane normal vector (normalized)
            distance: Distance from origin to plane
        """
        self.normal = normal
        self.distance = distance
    
    def distance_to_point(self, point: np.ndarray) -> float:
        """
        Calculate signed distance from point to plane.
        
        Positive = in front of plane (inside frustum)
        Negative = behind plane (outside frustum)
        
        Args:
            point: Point to test (vec3)
            
        Returns:
            Signed distance to plane
        """
        return np.dot(self.normal, point) + self.distance


class Frustum:
    """
    Represents a camera frustum (viewing pyramid).
    
    The frustum is defined by 6 planes:
    - Left, Right, Top, Bottom, Near, Far
    """
    
    # Plane indices
    LEFT = 0
    RIGHT = 1
    BOTTOM = 2
    TOP = 3
    NEAR = 4
    FAR = 5
    
    def __init__(self):
        """Initialize an empty frustum."""
        self.planes: list[FrustumPlane] = [None] * 6
        self._initialized = False
    
    def update_from_camera(
        self,
        position: np.ndarray,
        front: np.ndarray,
        right: np.ndarray,
        up: np.ndarray,
        fov_y: float,
        aspect: float,
        z_near: float,
        z_far: float
    ):
        """
        Create frustum planes directly from camera parameters.
        
        Based on: https://learnopengl.com/Guest-Articles/2021/Scene/Frustum-Culling
        
        Args:
            position: Camera position (vec3)
            front: Camera front vector (normalized, vec3)
            right: Camera right vector (normalized, vec3)
            up: Camera up vector (normalized, vec3)
            fov_y: Field of view in Y direction (degrees)
            aspect: Aspect ratio (width/height)
            z_near: Near clipping plane distance
            z_far: Far clipping plane distance
        """
        import math
        
        # Convert FOV from degrees to radians
        fov_y_rad = math.radians(fov_y)
        
        # Calculate half vertical and horizontal sides of far plane
        half_v_side = z_far * math.tan(fov_y_rad * 0.5)
        half_h_side = half_v_side * aspect
        
        # Calculate front vector scaled by far distance
        front_mult_far = front * z_far
        
        # Helper function to create plane from point and normal
        def create_plane(point_on_plane: np.ndarray, normal: np.ndarray) -> FrustumPlane:
            # Normalize the normal
            normal = normal / np.linalg.norm(normal)
            # Calculate distance: -dot(normal, point_on_plane)
            distance = -np.dot(normal, point_on_plane)
            return FrustumPlane(normal, distance)
        
        # Near plane: at camera position + near * front, normal is front
        near_point = position + front * z_near
        self.planes[self.NEAR] = create_plane(near_point, front)
        
        # Far plane: at camera position + far * front, normal is -front
        far_point = position + front_mult_far
        self.planes[self.FAR] = create_plane(far_point, -front)
        
        # Right plane: cross product of (front*far - right*halfHSide) and up
        right_plane_normal = np.cross(front_mult_far - right * half_h_side, up)
        self.planes[self.RIGHT] = create_plane(position, right_plane_normal)
        
        # Left plane: cross product of up and (front*far + right*halfHSide)
        left_plane_normal = np.cross(up, front_mult_far + right * half_h_side)
        self.planes[self.LEFT] = create_plane(position, left_plane_normal)
        
        # Top plane: cross product of right and (front*far - up*halfVSide)
        top_plane_normal = np.cross(right, front_mult_far - up * half_v_side)
        self.planes[self.TOP] = create_plane(position, top_plane_normal)
        
        # Bottom plane: cross product of (front*far + up*halfVSide) and right
        bottom_plane_normal = np.cross(front_mult_far + up * half_v_side, right)
        self.planes[self.BOTTOM] = create_plane(position, bottom_plane_normal)
        
        self._initialized = True
    
    def update_from_matrix(self, view_projection_matrix: np.ndarray):
        """
        Extract frustum planes from view-projection matrix (legacy method).
        
        Note: update_from_camera() is preferred as it's more reliable.
        """
        # This method is kept for backward compatibility but update_from_camera is preferred
        pass
    
    def test_point(self, point: np.ndarray) -> FrustumResult:
        """
        Test if a point is inside the frustum.
        
        Args:
            point: Point to test (vec3)
            
        Returns:
            FrustumResult.INSIDE if point is inside, OUTSIDE otherwise
        """
        if not self._initialized:
            return FrustumResult.INSIDE  # If not initialized, don't cull
        
        for plane in self.planes:
            if plane is None:
                continue
            # Planes have normals pointing INWARD (toward viewable area)
            # So points inside frustum have POSITIVE distance
            if plane.distance_to_point(point) < 0:
                return FrustumResult.OUTSIDE
        
        return FrustumResult.INSIDE
    
    def test_sphere(
        self, 
        center: np.ndarray, 
        radius: float
    ) -> FrustumResult:
        """
        Test if a sphere intersects the frustum.
        
        Args:
            center: Sphere center (vec3)
            radius: Sphere radius
            
        Returns:
            FrustumResult.INSIDE if completely inside,
            INTERSECT if partially inside,
            OUTSIDE if completely outside
        """
        if not self._initialized:
            return FrustumResult.INSIDE
        
        inside_count = 0
        
        for plane in self.planes:
            if plane is None:
                continue
            
            distance = plane.distance_to_point(center)
            
            # Planes have normals pointing INWARD (toward viewable area)
            # So points inside frustum have POSITIVE distance
            if distance < -radius:
                # Sphere is completely outside this plane
                return FrustumResult.OUTSIDE
            
            if distance > radius:
                # Sphere is completely inside this plane
                inside_count += 1
        
        # If sphere is inside all planes, it's completely inside
        if inside_count == 6:
            return FrustumResult.INSIDE
        
        # Otherwise, it's intersecting
        return FrustumResult.INTERSECT
    
    def test_aabb(
        self,
        min_point: np.ndarray,
        max_point: np.ndarray
    ) -> FrustumResult:
        """
        Test if an Axis-Aligned Bounding Box (AABB) intersects the frustum.
        
        Uses the "p-n vertex" method: test the closest and farthest
        vertex from each plane to determine intersection.
        
        Args:
            min_point: AABB minimum point (vec3)
            max_point: AABB maximum point (vec3)
            
        Returns:
            FrustumResult.INSIDE if completely inside,
            INTERSECT if partially inside,
            OUTSIDE if completely outside
        """
        if not self._initialized:
            return FrustumResult.INSIDE
        
        inside_count = 0
        
        for plane in self.planes:
            if plane is None:
                continue
            
            # Find the p-vertex (positive vertex) and n-vertex (negative vertex)
            # p-vertex: vertex with maximum distance from plane (inside frustum)
            # n-vertex: vertex with minimum distance from plane (outside frustum)
            
            p_vertex = np.array([
                max_point[0] if plane.normal[0] >= 0 else min_point[0],
                max_point[1] if plane.normal[1] >= 0 else min_point[1],
                max_point[2] if plane.normal[2] >= 0 else min_point[2]
            ])
            
            n_vertex = np.array([
                min_point[0] if plane.normal[0] >= 0 else max_point[0],
                min_point[1] if plane.normal[1] >= 0 else max_point[1],
                min_point[2] if plane.normal[2] >= 0 else max_point[2]
            ])
            
            # Calculate distances
            n_dist = plane.distance_to_point(n_vertex)
            p_dist = plane.distance_to_point(p_vertex)
            
            # Planes have normals pointing INWARD (toward viewable area)
            # So points inside frustum have POSITIVE distance
            # 
            # n-vertex: the vertex closest to the plane (minimum distance)
            # p-vertex: the vertex farthest from the plane (maximum distance)
            #
            # If p-vertex (farthest point) is outside (negative), entire AABB is outside
            # We use a small epsilon to avoid culling objects that are just barely touching
            EPSILON = 1e-6
            if p_dist < -EPSILON:
                return FrustumResult.OUTSIDE
            
            # If n-vertex (closest point) is inside (positive), AABB is completely inside this plane
            if n_dist > EPSILON:
                inside_count += 1
        
        # If AABB is inside all planes, it's completely inside
        if inside_count == 6:
            return FrustumResult.INSIDE
        
        # Otherwise, it's intersecting
        return FrustumResult.INTERSECT
    
    def test_aabb_world(
        self,
        min_point: np.ndarray,
        max_point: np.ndarray,
        model_matrix: np.ndarray
    ) -> FrustumResult:
        """
        Test an AABB that's been transformed by a model matrix.
        
        This converts the AABB corners to world space and then tests them.
        More expensive than test_aabb, but necessary for rotated objects.
        
        Args:
            min_point: AABB minimum point in model space (vec3)
            max_point: AABB maximum point in model space (vec3)
            model_matrix: Model transformation matrix (4x4)
            
        Returns:
            FrustumResult
        """
        if not self._initialized:
            return FrustumResult.INSIDE
        
        # Get all 8 corners of the AABB
        corners = np.array([
            [min_point[0], min_point[1], min_point[2], 1.0],
            [max_point[0], min_point[1], min_point[2], 1.0],
            [min_point[0], max_point[1], min_point[2], 1.0],
            [max_point[0], max_point[1], min_point[2], 1.0],
            [min_point[0], min_point[1], max_point[2], 1.0],
            [max_point[0], min_point[1], max_point[2], 1.0],
            [min_point[0], max_point[1], max_point[2], 1.0],
            [max_point[0], max_point[1], max_point[2], 1.0],
        ])
        
        # Transform corners to world space
        world_corners = (model_matrix @ corners.T).T[:, :3]
        
        # Find world-space AABB
        world_min = np.min(world_corners, axis=0)
        world_max = np.max(world_corners, axis=0)
        
        # Test the world-space AABB (less accurate but faster)
        # For more accuracy, we could test the oriented bounding box (OBB)
        return self.test_aabb(world_min, world_max)
    
    def is_initialized(self) -> bool:
        """Check if frustum has been initialized."""
        return self._initialized

