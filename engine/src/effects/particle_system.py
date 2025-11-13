"""
Particle System Manager
Manages multiple particle emitters and coordinates rendering.
"""

from typing import List, Optional, Dict
from .particle import ParticleEmitter
from .particle_renderer import ParticleRenderer
import numpy as np


class ParticleSystem:
    """
    Manages multiple particle emitters and rendering.
    """
    
    def __init__(self):
        """Initialize particle system."""
        self.emitters: Dict[str, ParticleEmitter] = {}
        self.renderer: Optional[ParticleRenderer] = None
        self.enabled = True
    
    def init(self) -> bool:
        """
        Initialize particle system renderer.
        
        Returns:
            True if successful
        """
        self.renderer = ParticleRenderer()
        if not self.renderer.init():
            print("[ERROR] Failed to initialize ParticleRenderer")
            return False
        
        print("[ParticleSystem] Initialized")
        return True
    
    def add_emitter(self, name: str, emitter: ParticleEmitter):
        """
        Add a named emitter to the system.
        
        Args:
            name: Unique emitter name
            emitter: ParticleEmitter instance
        """
        self.emitters[name] = emitter
        print(f"[ParticleSystem] Added emitter '{name}'")
    
    def remove_emitter(self, name: str):
        """
        Remove an emitter from the system.
        
        Args:
            name: Emitter name
        """
        if name in self.emitters:
            del self.emitters[name]
            print(f"[ParticleSystem] Removed emitter '{name}'")
    
    def get_emitter(self, name: str) -> Optional[ParticleEmitter]:
        """
        Get an emitter by name.
        
        Args:
            name: Emitter name
            
        Returns:
            ParticleEmitter or None
        """
        return self.emitters.get(name)
    
    def clear_all(self):
        """Clear all particles from all emitters."""
        for emitter in self.emitters.values():
            emitter.clear()
    
    def update(self, delta_time: float):
        """
        Update all particle emitters.
        
        Args:
            delta_time: Time since last frame (seconds)
        """
        if not self.enabled:
            return
        
        for emitter in self.emitters.values():
            emitter.update(delta_time)
    
    def render(self, view_matrix: np.ndarray, projection_matrix: np.ndarray):
        """
        Render all particles from all emitters.
        
        Args:
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
        """
        if not self.enabled or not self.renderer:
            return
        
        # Collect all active particles from all emitters
        all_particles = []
        for emitter in self.emitters.values():
            all_particles.extend(emitter.get_active_particles())
        
        if all_particles:
            self.renderer.render(all_particles, view_matrix, projection_matrix)
    
    def get_total_particle_count(self) -> int:
        """Get total number of active particles across all emitters."""
        return sum(emitter.get_particle_count() for emitter in self.emitters.values())
    
    def cleanup(self):
        """Clean up particle system resources."""
        if self.renderer:
            self.renderer.cleanup()
        
        self.emitters.clear()
        print("[ParticleSystem] Cleaned up")

