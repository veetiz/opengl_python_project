"""
Particle System
Individual particle and particle emitter classes.
"""

import numpy as np
from typing import Optional, Tuple, Callable
import random


class Particle:
    """
    Individual particle with physics properties.
    """
    
    def __init__(
        self,
        position: np.ndarray,
        velocity: np.ndarray,
        color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
        size: float = 1.0,
        lifetime: float = 1.0,
        rotation: float = 0.0,
        rotation_speed: float = 0.0
    ):
        """
        Initialize a particle.
        
        Args:
            position: Initial position (x, y, z)
            velocity: Initial velocity (vx, vy, vz)
            color: RGBA color (0-1 range)
            size: Particle size in world units
            lifetime: How long particle lives (seconds)
            rotation: Initial rotation (radians)
            rotation_speed: Rotation speed (radians/sec)
        """
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.array(velocity, dtype=np.float32)
        self.color = np.array(color, dtype=np.float32)
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.rotation = rotation
        self.rotation_speed = rotation_speed
        self.is_alive = True
        
        # Store initial values for interpolation
        self.initial_size = size
        self.initial_color = np.array(color, dtype=np.float32)
    
    def update(self, delta_time: float, gravity: np.ndarray = None):
        """
        Update particle physics.
        
        Args:
            delta_time: Time since last frame
            gravity: Gravity vector (default: (0, -9.8, 0))
        """
        if not self.is_alive:
            return
        
        # Apply velocity
        self.position += self.velocity * delta_time
        
        # Apply gravity
        if gravity is not None:
            self.velocity += gravity * delta_time
        
        # Update rotation
        self.rotation += self.rotation_speed * delta_time
        
        # Decrease lifetime
        self.lifetime -= delta_time
        if self.lifetime <= 0:
            self.is_alive = False
    
    def get_life_percentage(self) -> float:
        """Get remaining life as percentage (1.0 = just spawned, 0.0 = dead)."""
        return self.lifetime / self.max_lifetime if self.max_lifetime > 0 else 0.0


class ParticleEmitter:
    """
    Emits and manages a collection of particles.
    """
    
    def __init__(
        self,
        position: Tuple[float, float, float] = (0.0, 0.0, 0.0),
        emission_rate: float = 10.0,  # Particles per second
        max_particles: int = 1000,
        particle_lifetime: float = 2.0,
        particle_size: float = 0.5,
        emit_velocity: Tuple[float, float, float] = (0.0, 1.0, 0.0),
        velocity_randomness: float = 0.5,
        color: Tuple[float, float, float, float] = (1.0, 1.0, 1.0, 1.0),
        gravity: Optional[Tuple[float, float, float]] = (0.0, -9.8, 0.0),
        emitter_type: str = "point"  # point, cone, sphere, box
    ):
        """
        Initialize particle emitter.
        
        Args:
            position: Emitter world position
            emission_rate: Particles spawned per second
            max_particles: Maximum number of active particles
            particle_lifetime: How long each particle lives (seconds)
            particle_size: Size of each particle
            emit_velocity: Base emission velocity vector
            velocity_randomness: Random variation in velocity (0-1)
            color: Base particle color RGBA
            gravity: Gravity vector (None to disable)
            emitter_type: Emission shape (point, cone, sphere, box)
        """
        self.position = np.array(position, dtype=np.float32)
        self.emission_rate = emission_rate
        self.max_particles = max_particles
        self.particle_lifetime = particle_lifetime
        self.particle_size = particle_size
        self.emit_velocity = np.array(emit_velocity, dtype=np.float32)
        self.velocity_randomness = velocity_randomness
        self.color = color
        self.gravity = np.array(gravity, dtype=np.float32) if gravity else None
        self.emitter_type = emitter_type
        
        # Particles
        self.particles: list[Particle] = []
        
        # Emission control
        self.is_emitting = True
        self.emission_timer = 0.0
        
        # Color and size over lifetime (gradients)
        self.color_over_lifetime: Optional[Callable[[float], Tuple[float, float, float, float]]] = None
        self.size_over_lifetime: Optional[Callable[[float], float]] = None
        
        # Emitter parameters
        self.cone_angle = 30.0  # For cone emitter (degrees)
        self.sphere_radius = 1.0  # For sphere emitter
        self.box_size = (1.0, 1.0, 1.0)  # For box emitter
    
    def set_position(self, position: Tuple[float, float, float]):
        """Update emitter position."""
        self.position = np.array(position, dtype=np.float32)
    
    def start(self):
        """Start emitting particles."""
        self.is_emitting = True
    
    def stop(self):
        """Stop emitting particles."""
        self.is_emitting = False
    
    def clear(self):
        """Clear all particles."""
        self.particles.clear()
    
    def _spawn_particle(self):
        """Spawn a single particle based on emitter type."""
        # Generate spawn position
        if self.emitter_type == "point":
            spawn_pos = self.position.copy()
        
        elif self.emitter_type == "sphere":
            # Random point on sphere surface
            theta = random.uniform(0, 2 * np.pi)
            phi = random.uniform(0, np.pi)
            r = self.sphere_radius
            offset = np.array([
                r * np.sin(phi) * np.cos(theta),
                r * np.sin(phi) * np.sin(theta),
                r * np.cos(phi)
            ], dtype=np.float32)
            spawn_pos = self.position + offset
        
        elif self.emitter_type == "box":
            # Random point in box
            offset = np.array([
                random.uniform(-self.box_size[0]/2, self.box_size[0]/2),
                random.uniform(-self.box_size[1]/2, self.box_size[1]/2),
                random.uniform(-self.box_size[2]/2, self.box_size[2]/2)
            ], dtype=np.float32)
            spawn_pos = self.position + offset
        
        elif self.emitter_type == "cone":
            # Random direction in cone
            angle_rad = np.radians(self.cone_angle)
            theta = random.uniform(0, 2 * np.pi)
            phi = random.uniform(0, angle_rad)
            
            # Base direction (up)
            direction = np.array([
                np.sin(phi) * np.cos(theta),
                np.cos(phi),
                np.sin(phi) * np.sin(theta)
            ], dtype=np.float32)
            
            spawn_pos = self.position.copy()
            velocity_dir = direction
        else:
            spawn_pos = self.position.copy()
            velocity_dir = None
        
        # Generate velocity
        if self.emitter_type == "cone":
            base_vel = self.emit_velocity
        else:
            velocity_dir = self.emit_velocity / (np.linalg.norm(self.emit_velocity) + 0.001)
        
        # Add randomness to velocity
        random_vel = np.array([
            random.uniform(-1, 1),
            random.uniform(-1, 1),
            random.uniform(-1, 1)
        ], dtype=np.float32)
        random_vel = random_vel / (np.linalg.norm(random_vel) + 0.001)
        
        if self.emitter_type == "cone":
            velocity = velocity_dir * np.linalg.norm(self.emit_velocity)
        else:
            velocity = self.emit_velocity + random_vel * self.velocity_randomness
        
        # Create particle
        particle = Particle(
            position=spawn_pos,
            velocity=velocity,
            color=self.color,
            size=self.particle_size,
            lifetime=self.particle_lifetime,
            rotation=random.uniform(0, 2 * np.pi),
            rotation_speed=random.uniform(-2, 2)
        )
        
        self.particles.append(particle)
    
    def update(self, delta_time: float):
        """
        Update all particles and emit new ones.
        
        Args:
            delta_time: Time since last frame (seconds)
        """
        # Update existing particles
        for particle in self.particles[:]:  # Copy list for safe removal
            particle.update(delta_time, self.gravity)
            
            # Apply color over lifetime if defined
            if self.color_over_lifetime:
                life_pct = particle.get_life_percentage()
                particle.color = np.array(self.color_over_lifetime(life_pct), dtype=np.float32)
            
            # Apply size over lifetime if defined
            if self.size_over_lifetime:
                life_pct = particle.get_life_percentage()
                particle.size = self.size_over_lifetime(life_pct) * particle.initial_size
            
            # Remove dead particles
            if not particle.is_alive:
                self.particles.remove(particle)
        
        # Emit new particles
        if self.is_emitting and len(self.particles) < self.max_particles:
            self.emission_timer += delta_time
            particles_to_spawn = int(self.emission_timer * self.emission_rate)
            
            for _ in range(particles_to_spawn):
                if len(self.particles) < self.max_particles:
                    self._spawn_particle()
            
            self.emission_timer -= particles_to_spawn / self.emission_rate
    
    def get_active_particles(self) -> list[Particle]:
        """Get list of active particles."""
        return [p for p in self.particles if p.is_alive]
    
    def get_particle_count(self) -> int:
        """Get number of active particles."""
        return len(self.get_active_particles())

