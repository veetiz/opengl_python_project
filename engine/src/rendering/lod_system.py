"""
Level of Detail (LOD) System Module
Manages LOD levels for models to optimize rendering performance based on distance.
"""

import numpy as np
from typing import List, Optional, Dict, TYPE_CHECKING
from enum import IntEnum

if TYPE_CHECKING:
    from ..graphics.model import Model
    from ..graphics.mesh import Mesh
    from ..scene.camera import Camera


class LODLevel(IntEnum):
    """LOD level enumeration."""
    LOD0 = 0  # Highest detail (closest)
    LOD1 = 1  # Medium detail
    LOD2 = 2  # Low detail
    LOD3 = 3  # Lowest detail (furthest)
    CULLED = -1  # Too far, culled


class LODData:
    """Stores LOD data for a model."""
    
    def __init__(self, model: 'Model'):
        """
        Initialize LOD data for a model.
        
        Args:
            model: Model to create LOD data for
        """
        self.model = model
        self.lod_levels: Dict[int, 'Model'] = {}  # Maps LOD level to Model
        self.distances: List[float] = []  # Distance thresholds for each LOD level
        self._default_lod = model  # Default to original model
        
        # Add default LOD0 (highest detail)
        self.lod_levels[LODLevel.LOD0] = model
    
    def add_lod_level(self, lod_level: int, lod_model: 'Model', distance: float):
        """
        Add a LOD level to this model.
        
        Args:
            lod_level: LOD level (0 = highest, higher = lower detail)
            lod_model: Model to use for this LOD level
            distance: Distance threshold for this LOD level
        """
        self.lod_levels[lod_level] = lod_model
        
        # Update distance thresholds
        while len(self.distances) <= lod_level:
            self.distances.append(float('inf'))
        
        self.distances[lod_level] = distance
        # Sort distances (closest first)
        self.distances.sort()
    
    def get_lod_level(self, distance: float, max_distance: float = float('inf')) -> int:
        """
        Get the appropriate LOD level for a given distance.
        
        Args:
            distance: Distance from camera
            max_distance: Maximum render distance (cull if beyond)
            
        Returns:
            LOD level (0 = highest detail, -1 = culled)
        """
        if distance > max_distance:
            return LODLevel.CULLED
        
        # Find appropriate LOD level based on distance thresholds
        for i, threshold in enumerate(self.distances):
            if distance <= threshold:
                # Return highest available LOD level <= i
                for lod in range(i, -1, -1):
                    if lod in self.lod_levels:
                        return lod
        
        # If beyond all thresholds, use lowest available LOD
        if self.lod_levels:
            return max(self.lod_levels.keys())
        
        return LODLevel.LOD0
    
    def get_model_for_lod(self, lod_level: int) -> Optional['Model']:
        """
        Get the model for a specific LOD level.
        
        Args:
            lod_level: LOD level
            
        Returns:
            Model for this LOD level, or None if not available
        """
        if lod_level == LODLevel.CULLED:
            return None
        
        # Return the requested LOD if available
        if lod_level in self.lod_levels:
            return self.lod_levels[lod_level]
        
        # Fallback to nearest available LOD
        if not self.lod_levels:
            return self._default_lod
        
        # Find nearest LOD level
        available_levels = sorted(self.lod_levels.keys())
        if lod_level < available_levels[0]:
            return self.lod_levels[available_levels[0]]
        elif lod_level > available_levels[-1]:
            return self.lod_levels[available_levels[-1]]
        else:
            # Find closest available level
            closest = min(available_levels, key=lambda x: abs(x - lod_level))
            return self.lod_levels[closest]
    
    def has_lod_levels(self) -> bool:
        """Check if this model has multiple LOD levels."""
        return len(self.lod_levels) > 1


class LODSystem:
    """
    Manages LOD system for all models in the scene.
    
    Automatically selects appropriate LOD levels based on distance from camera
    to optimize rendering performance.
    """
    
    def __init__(
        self,
        default_distances: Optional[List[float]] = None,
        lod_bias: float = 0.0,
        max_render_distance: float = 1000.0
    ):
        """
        Initialize the LOD system.
        
        Args:
            default_distances: Default distance thresholds for LOD levels
                              [LOD0->LOD1, LOD1->LOD2, LOD2->LOD3, ...]
            lod_bias: LOD bias to adjust LOD selection (positive = lower detail, negative = higher detail)
            max_render_distance: Maximum distance to render objects (cull beyond this)
        """
        self.lod_data: Dict['Model', LODData] = {}  # Maps model to LOD data
        self.default_distances = default_distances or [50.0, 150.0, 300.0, 500.0]
        self.lod_bias = lod_bias
        self.max_render_distance = max_render_distance
        self.enabled = True
        
        # Statistics
        self._lod_usage: Dict[int, int] = {}  # Count of objects per LOD level
        self._frame_count = 0
    
    def register_model(self, model: 'Model', lod_data: Optional[LODData] = None):
        """
        Register a model with the LOD system.
        
        Args:
            model: Model to register
            lod_data: Optional LOD data (creates default if None)
        """
        if lod_data is None:
            lod_data = LODData(model)
        self.lod_data[model] = lod_data
    
    def unregister_model(self, model: 'Model'):
        """Unregister a model from the LOD system."""
        if model in self.lod_data:
            del self.lod_data[model]
    
    def get_lod_level(
        self,
        model: 'Model',
        camera_position: np.ndarray,
        object_position: np.ndarray,
        lod_bias: Optional[float] = None
    ) -> int:
        """
        Get the appropriate LOD level for an object.
        
        Args:
            model: Model to get LOD for
            camera_position: Camera position (vec3)
            object_position: Object position (vec3)
            lod_bias: Optional LOD bias override
            
        Returns:
            LOD level (0 = highest detail, -1 = culled)
        """
        if not self.enabled:
            return LODLevel.LOD0
        
        if model not in self.lod_data:
            return LODLevel.LOD0
        
        # Calculate distance
        distance = np.linalg.norm(object_position - camera_position)
        
        # Apply LOD bias
        bias = lod_bias if lod_bias is not None else self.lod_bias
        adjusted_distance = distance * (1.0 + bias)
        
        # Get LOD level
        lod_data = self.lod_data[model]
        lod_level = lod_data.get_lod_level(adjusted_distance, self.max_render_distance)
        
        return lod_level
    
    def get_model_for_lod(self, model: 'Model', lod_level: int) -> Optional['Model']:
        """
        Get the model to render for a specific LOD level.
        
        Args:
            model: Original model
            lod_level: LOD level
            
        Returns:
            Model to render, or None if culled
        """
        if not self.enabled or model not in self.lod_data:
            return model
        
        lod_data = self.lod_data[model]
        return lod_data.get_model_for_lod(lod_level)
    
    def set_lod_bias(self, bias: float):
        """
        Set the LOD bias.
        
        Args:
            bias: LOD bias (positive = lower detail, negative = higher detail)
        """
        self.lod_bias = bias
    
    def set_max_render_distance(self, distance: float):
        """
        Set the maximum render distance.
        
        Args:
            distance: Maximum distance to render objects
        """
        self.max_render_distance = distance
    
    def get_statistics(self) -> dict:
        """
        Get LOD system statistics.
        
        Returns:
            Dictionary with statistics
        """
        total_objects = sum(self._lod_usage.values())
        
        stats = {
            'enabled': self.enabled,
            'registered_models': len(self.lod_data),
            'total_objects': total_objects,
            'lod_usage': dict(self._lod_usage),
            'lod_bias': self.lod_bias,
            'max_render_distance': self.max_render_distance
        }
        
        return stats
    
    def reset_statistics(self):
        """Reset LOD usage statistics."""
        self._lod_usage.clear()
    
    def record_lod_usage(self, lod_level: int):
        """Record LOD level usage for statistics."""
        if lod_level not in self._lod_usage:
            self._lod_usage[lod_level] = 0
        self._lod_usage[lod_level] += 1

