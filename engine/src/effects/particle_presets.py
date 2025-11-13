"""
Particle Presets
Pre-configured particle effects (fire, smoke, sparkles, etc.)
"""

from .particle import ParticleEmitter
import numpy as np


class ParticlePresets:
    """Collection of pre-configured particle effects."""
    
    @staticmethod
    def create_fire(position=(0, 0, 0)) -> ParticleEmitter:
        """
        Create a fire particle emitter.
        
        Args:
            position: Emitter position
            
        Returns:
            Configured fire emitter
        """
        emitter = ParticleEmitter(
            position=position,
            emission_rate=50.0,  # 50 particles/sec
            max_particles=200,
            particle_lifetime=1.5,
            particle_size=0.3,
            emit_velocity=(0.0, 2.0, 0.0),  # Upward
            velocity_randomness=0.8,
            color=(1.0, 0.5, 0.0, 1.0),  # Orange
            gravity=(0.0, 0.5, 0.0),  # Slight upward drift
            emitter_type="cone"
        )
        
        emitter.cone_angle = 15.0  # Narrow cone upward
        
        # Color gradient: orange → red → black (fade out)
        def fire_color(life_pct):
            if life_pct > 0.7:
                # Start: bright orange
                return (1.0, 0.6, 0.1, 1.0)
            elif life_pct > 0.3:
                # Middle: red
                t = (life_pct - 0.3) / 0.4
                return (1.0, 0.3 + t * 0.3, 0.1 * t, 1.0)
            else:
                # End: dark red, fade out
                t = life_pct / 0.3
                return (0.5 * t, 0.1 * t, 0.0, t)
        
        emitter.color_over_lifetime = fire_color
        
        # Size: grows then shrinks
        def fire_size(life_pct):
            if life_pct > 0.5:
                return 1.0 + (1.0 - life_pct)
            else:
                return life_pct * 2
        
        emitter.size_over_lifetime = fire_size
        
        return emitter
    
    @staticmethod
    def create_smoke(position=(0, 0, 0)) -> ParticleEmitter:
        """
        Create a smoke particle emitter.
        
        Args:
            position: Emitter position
            
        Returns:
            Configured smoke emitter
        """
        emitter = ParticleEmitter(
            position=position,
            emission_rate=20.0,
            max_particles=150,
            particle_lifetime=3.0,
            particle_size=0.5,
            emit_velocity=(0.0, 1.0, 0.0),
            velocity_randomness=1.0,
            color=(0.3, 0.3, 0.3, 0.6),  # Gray, semi-transparent
            gravity=(0.0, 0.2, 0.0),  # Slight upward drift
            emitter_type="cone"
        )
        
        emitter.cone_angle = 25.0
        
        # Color: dark → light gray, fade out
        def smoke_color(life_pct):
            brightness = 0.2 + life_pct * 0.3
            alpha = life_pct * 0.5
            return (brightness, brightness, brightness, alpha)
        
        emitter.color_over_lifetime = smoke_color
        
        # Size: grows over time
        def smoke_size(life_pct):
            return 0.5 + (1.0 - life_pct) * 1.5
        
        emitter.size_over_lifetime = smoke_size
        
        return emitter
    
    @staticmethod
    def create_sparkles(position=(0, 0, 0)) -> ParticleEmitter:
        """
        Create a sparkle particle emitter.
        
        Args:
            position: Emitter position
            
        Returns:
            Configured sparkle emitter
        """
        emitter = ParticleEmitter(
            position=position,
            emission_rate=30.0,
            max_particles=100,
            particle_lifetime=0.8,
            particle_size=0.15,
            emit_velocity=(0.0, 2.0, 0.0),
            velocity_randomness=1.5,
            color=(1.0, 1.0, 0.5, 1.0),  # Yellow-white
            gravity=(0.0, -2.0, 0.0),  # Falls down
            emitter_type="point"
        )
        
        # Color: bright → fade
        def sparkle_color(life_pct):
            return (1.0, 1.0, 0.8, life_pct)
        
        emitter.color_over_lifetime = sparkle_color
        
        # Size: constant then fade
        def sparkle_size(life_pct):
            return 1.0 if life_pct > 0.3 else life_pct / 0.3
        
        emitter.size_over_lifetime = sparkle_size
        
        return emitter
    
    @staticmethod
    def create_explosion(position=(0, 0, 0)) -> ParticleEmitter:
        """
        Create an explosion particle emitter (one-shot burst).
        
        Args:
            position: Explosion center
            
        Returns:
            Configured explosion emitter
        """
        emitter = ParticleEmitter(
            position=position,
            emission_rate=200.0,  # Fast burst
            max_particles=50,
            particle_lifetime=1.0,
            particle_size=0.4,
            emit_velocity=(5.0, 5.0, 5.0),
            velocity_randomness=1.0,
            color=(1.0, 0.7, 0.2, 1.0),  # Bright orange
            gravity=(0.0, -9.8, 0.0),
            emitter_type="sphere"
        )
        
        emitter.sphere_radius = 0.5
        emitter.is_emitting = False  # Don't emit continuously
        
        # Color: orange → red → black
        def explosion_color(life_pct):
            if life_pct > 0.7:
                return (1.0, 0.8, 0.3, 1.0)
            elif life_pct > 0.3:
                t = (life_pct - 0.3) / 0.4
                return (1.0, 0.4 + t * 0.4, 0.1, 1.0)
            else:
                t = life_pct / 0.3
                return (0.3, 0.1, 0.0, t)
        
        emitter.color_over_lifetime = explosion_color
        
        # Size: grows then shrinks
        def explosion_size(life_pct):
            if life_pct > 0.6:
                return (1.0 - life_pct) * 3
            else:
                return life_pct * 2
        
        emitter.size_over_lifetime = explosion_size
        
        return emitter
    
    @staticmethod
    def create_rain(position=(0, 10, 0)) -> ParticleEmitter:
        """
        Create a rain particle emitter.
        
        Args:
            position: Emitter position (should be high up)
            
        Returns:
            Configured rain emitter
        """
        emitter = ParticleEmitter(
            position=position,
            emission_rate=100.0,
            max_particles=500,
            particle_lifetime=3.0,
            particle_size=0.1,
            emit_velocity=(0.0, -10.0, 0.0),  # Fast downward
            velocity_randomness=0.2,
            color=(0.5, 0.6, 1.0, 0.6),  # Light blue, transparent
            gravity=(0.0, -2.0, 0.0),  # Additional downward force
            emitter_type="box"
        )
        
        emitter.box_size = (10.0, 0.1, 10.0)  # Wide area, thin vertical
        
        # Constant color
        emitter.color_over_lifetime = lambda life_pct: (0.5, 0.6, 1.0, 0.6)
        emitter.size_over_lifetime = lambda life_pct: 1.0
        
        return emitter
    
    @staticmethod
    def create_snow(position=(0, 10, 0)) -> ParticleEmitter:
        """
        Create a snow particle emitter.
        
        Args:
            position: Emitter position (should be high up)
            
        Returns:
            Configured snow emitter
        """
        emitter = ParticleEmitter(
            position=position,
            emission_rate=50.0,
            max_particles=300,
            particle_lifetime=5.0,
            particle_size=0.15,
            emit_velocity=(0.0, -1.0, 0.0),  # Slow downward
            velocity_randomness=0.5,
            color=(1.0, 1.0, 1.0, 0.9),  # White
            gravity=(0.0, -0.5, 0.0),  # Gentle fall
            emitter_type="box"
        )
        
        emitter.box_size = (10.0, 0.1, 10.0)
        
        # Gentle fade
        emitter.color_over_lifetime = lambda life_pct: (1.0, 1.0, 1.0, life_pct * 0.9)
        emitter.size_over_lifetime = lambda life_pct: 1.0
        
        return emitter
    
    @staticmethod
    def create_magic_aura(position=(0, 0, 0)) -> ParticleEmitter:
        """
        Create a magical aura particle emitter.
        
        Args:
            position: Center position
            
        Returns:
            Configured magic aura emitter
        """
        emitter = ParticleEmitter(
            position=position,
            emission_rate=40.0,
            max_particles=150,
            particle_lifetime=2.0,
            particle_size=0.2,
            emit_velocity=(1.0, 1.0, 1.0),
            velocity_randomness=1.0,
            color=(0.5, 0.2, 1.0, 0.8),  # Purple
            gravity=(0.0, 0.0, 0.0),  # No gravity
            emitter_type="sphere"
        )
        
        emitter.sphere_radius = 1.5
        
        # Color: purple → pink → fade
        def magic_color(life_pct):
            if life_pct > 0.5:
                return (0.5, 0.2, 1.0, 0.8)
            else:
                t = life_pct / 0.5
                return (0.8, 0.4, 1.0, t * 0.8)
        
        emitter.color_over_lifetime = magic_color
        emitter.size_over_lifetime = lambda life_pct: 0.5 + life_pct * 0.5
        
        return emitter

