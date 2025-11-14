"""
Instanced Rendering Module
Manages instanced rendering for efficient batch rendering of multiple objects with the same mesh.
"""

import numpy as np
from typing import Dict, List, Optional, TYPE_CHECKING
from collections import defaultdict
from OpenGL.GL import *  # type: ignore

if TYPE_CHECKING:
    from ..scene.gameobject import GameObject
    from ..graphics.mesh import Mesh


class InstanceBatch:
    """Represents a batch of instances to render together."""
    
    def __init__(self, mesh_id: int):
        """
        Initialize an instance batch.
        
        Args:
            mesh_id: Unique identifier for the mesh
        """
        self.mesh_id = mesh_id
        self.instances: List['GameObject'] = []
        self.instance_matrices: np.ndarray = np.array([], dtype=np.float32)
        self.instance_vbo: Optional[int] = None
        self.dirty = True  # Needs buffer update
        
    def add_instance(self, game_object: 'GameObject'):
        """Add a game object instance to this batch."""
        self.instances.append(game_object)
        self.dirty = True
    
    def remove_instance(self, game_object: 'GameObject'):
        """Remove a game object instance from this batch."""
        if game_object in self.instances:
            self.instances.remove(game_object)
            self.dirty = True
    
    def clear(self):
        """Clear all instances from this batch."""
        self.instances.clear()
        self.dirty = True
    
    def update_instance_data(self):
        """Update the instance matrix buffer with current instance transforms."""
        if not self.dirty or len(self.instances) == 0:
            return
        
        # Collect all instance matrices
        matrices = []
        for obj in self.instances:
            if obj.active:
                model_matrix = obj.get_model_matrix()
                # OpenGL expects column-major matrices, so transpose
                model_matrix_transposed = model_matrix.T
                matrices.append(model_matrix_transposed.flatten())
        
        if len(matrices) == 0:
            self.instance_matrices = np.array([], dtype=np.float32)
            return
        
        # Convert to numpy array (N instances x 16 floats)
        self.instance_matrices = np.array(matrices, dtype=np.float32)
        self.dirty = False
    
    def upload_to_gpu(self):
        """Upload instance data to GPU buffer."""
        if len(self.instance_matrices) == 0:
            return
        
        # Create or update VBO
        if self.instance_vbo is None:
            self.instance_vbo = glGenBuffers(1)
        
        glBindBuffer(GL_ARRAY_BUFFER, self.instance_vbo)
        
        # Upload data (or update if already exists)
        data_size = self.instance_matrices.nbytes
        glBufferData(GL_ARRAY_BUFFER, data_size, self.instance_matrices, GL_DYNAMIC_DRAW)
        
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def cleanup(self):
        """Clean up GPU resources."""
        if self.instance_vbo is not None:
            glDeleteBuffers(1, [self.instance_vbo])
            self.instance_vbo = None


class InstancedRenderer:
    """
    Manages instanced rendering for efficient batch rendering.
    
    Groups objects by mesh and renders them using instanced draw calls,
    reducing draw calls from O(n) to O(m) where m is the number of unique meshes.
    """
    
    def __init__(self, max_instances_per_batch: int = 10000):
        """
        Initialize the instanced renderer.
        
        Args:
            max_instances_per_batch: Maximum instances per batch (default: 10000)
        """
        self.max_instances_per_batch = max_instances_per_batch
        self.batches: Dict[int, InstanceBatch] = {}  # Maps mesh_id to InstanceBatch
        self.enabled = True
        
    def get_mesh_id(self, mesh: 'Mesh') -> int:
        """
        Get a unique identifier for a mesh.
        
        Args:
            mesh: Mesh object
            
        Returns:
            Unique mesh identifier
        """
        return id(mesh)
    
    def add_instance(self, game_object: 'GameObject', mesh: 'Mesh'):
        """
        Add a game object instance for instanced rendering.
        
        Args:
            game_object: GameObject to add
            mesh: Mesh that this object uses
        """
        if not self.enabled:
            return
        
        mesh_id = self.get_mesh_id(mesh)
        
        if mesh_id not in self.batches:
            self.batches[mesh_id] = InstanceBatch(mesh_id)
        
        self.batches[mesh_id].add_instance(game_object)
    
    def remove_instance(self, game_object: 'GameObject', mesh: 'Mesh'):
        """
        Remove a game object instance from instanced rendering.
        
        Args:
            game_object: GameObject to remove
            mesh: Mesh that this object uses
        """
        if not self.enabled:
            return
        
        mesh_id = self.get_mesh_id(mesh)
        
        if mesh_id in self.batches:
            self.batches[mesh_id].remove_instance(game_object)
            
            # Clean up empty batches
            if len(self.batches[mesh_id].instances) == 0:
                self.batches[mesh_id].cleanup()
                del self.batches[mesh_id]
    
    def clear(self):
        """Clear all instance batches."""
        for batch in self.batches.values():
            batch.cleanup()
        self.batches.clear()
    
    def prepare_batches(self, objects: List['GameObject']):
        """
        Prepare instance batches from a list of game objects.
        
        Args:
            objects: List of GameObjects to batch
        """
        if not self.enabled:
            return
        
        # Clear existing batches
        self.clear()
        
        # Group objects by mesh
        mesh_groups: Dict[int, List['GameObject']] = defaultdict(list)
        
        for obj in objects:
            if not obj.active or not obj.model:
                continue
            
            for mesh in obj.model.meshes:
                mesh_id = self.get_mesh_id(mesh)
                mesh_groups[mesh_id].append(obj)
        
        # Create batches
        for mesh_id, instances in mesh_groups.items():
            batch = InstanceBatch(mesh_id)
            batch.instances = instances
            batch.dirty = True
            self.batches[mesh_id] = batch
    
    def update_instance_data(self):
        """Update all instance data buffers."""
        if not self.enabled:
            return
        
        for batch in self.batches.values():
            batch.update_instance_data()
            batch.upload_to_gpu()
    
    def get_batches(self) -> Dict[int, InstanceBatch]:
        """
        Get all instance batches.
        
        Returns:
            Dictionary mapping mesh_id to InstanceBatch
        """
        return self.batches
    
    def get_statistics(self) -> dict:
        """
        Get statistics about instanced rendering.
        
        Returns:
            Dictionary with statistics
        """
        total_instances = sum(len(batch.instances) for batch in self.batches.values())
        total_batches = len(self.batches)
        
        return {
            'enabled': self.enabled,
            'total_batches': total_batches,
            'total_instances': total_instances,
            'avg_instances_per_batch': total_instances / total_batches if total_batches > 0 else 0
        }
    
    def cleanup(self):
        """Clean up all GPU resources."""
        self.clear()

