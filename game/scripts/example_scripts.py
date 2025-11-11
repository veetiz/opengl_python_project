"""
Example Game Scripts
Demonstrates how to create and use GameScripts.
"""

from src import GameScript
import numpy as np


class RotateScript(GameScript):
    """Rotates a GameObject continuously."""
    
    def __init__(self, entity=None, rotation_speed=(0.0, 50.0, 0.0)):
        """
        Initialize rotation script.
        
        Args:
            entity: Entity to attach to
            rotation_speed: Rotation speed in degrees per second (pitch, yaw, roll)
        """
        super().__init__(entity)
        self.rotation_speed = np.array(rotation_speed, dtype=np.float32)
    
    def on_start(self):
        """Called when script starts."""
        print(f"[RotateScript] Attached to '{self.entity.name}' - rotation started")
    
    def on_update(self, delta_time: float):
        """Rotate the game object each frame."""
        if self.entity and hasattr(self.entity, 'rotate'):
            # Calculate rotation for this frame
            rotation = self.rotation_speed * delta_time
            self.entity.rotate(
                pitch=rotation[0],
                yaw=rotation[1],
                roll=rotation[2]
            )


class OscillateScript(GameScript):
    """Moves a GameObject up and down in a sine wave."""
    
    def __init__(self, entity=None, speed=1.0, amplitude=0.5):
        """
        Initialize oscillate script.
        
        Args:
            entity: Entity to attach to
            speed: Oscillation speed
            amplitude: Movement amplitude
        """
        super().__init__(entity)
        self.speed = speed
        self.amplitude = amplitude
        self.time = 0.0
        self.initial_y = 0.0
    
    def on_start(self):
        """Store initial position."""
        if self.entity and hasattr(self.entity, 'transform'):
            self.initial_y = self.entity.transform.position[1]
            print(f"[OscillateScript] Attached to '{self.entity.name}' - oscillation started")
    
    def on_update(self, delta_time: float):
        """Move the object up and down."""
        if self.entity and hasattr(self.entity, 'transform'):
            self.time += delta_time
            offset = np.sin(self.time * self.speed) * self.amplitude
            self.entity.transform.position[1] = self.initial_y + offset


class FPSCounterScript(GameScript):
    """Global script that prints FPS periodically."""
    
    def __init__(self, entity=None, print_interval=2.0):
        """
        Initialize FPS counter.
        
        Args:
            entity: Should be None (global script)
            print_interval: How often to print FPS (seconds)
        """
        super().__init__(entity)
        self.print_interval = print_interval
        self.frame_count = 0
        self.time_accumulator = 0.0
    
    def on_start(self):
        """Called when script starts."""
        print("[FPSCounterScript] Started (global scene script)")
    
    def on_update(self, delta_time: float):
        """Count frames and print FPS."""
        self.frame_count += 1
        self.time_accumulator += delta_time
        
        if self.time_accumulator >= self.print_interval:
            fps = self.frame_count / self.time_accumulator
            print(f"[FPS] {fps:.1f} fps ({self.frame_count} frames in {self.time_accumulator:.2f}s)")
            self.frame_count = 0
            self.time_accumulator = 0.0


class CameraOrbitScript(GameScript):
    """Orbits a camera around a target point."""
    
    def __init__(self, entity=None, orbit_speed=30.0, radius=3.0):
        """
        Initialize camera orbit script.
        
        Args:
            entity: Camera entity to orbit
            orbit_speed: Orbit speed in degrees per second
            radius: Orbit radius
        """
        super().__init__(entity)
        self.orbit_speed = orbit_speed
        self.radius = radius
        self.angle = 0.0
    
    def on_start(self):
        """Called when script starts."""
        if self.entity:
            print(f"[CameraOrbitScript] Attached to camera '{self.entity.name}'")
    
    def on_update(self, delta_time: float):
        """Orbit the camera around the origin."""
        if self.entity and hasattr(self.entity, 'position'):
            self.angle += self.orbit_speed * delta_time
            
            # Calculate new position in orbit
            angle_rad = np.radians(self.angle)
            x = np.cos(angle_rad) * self.radius
            z = np.sin(angle_rad) * self.radius
            
            self.entity.position = np.array([x, 0.0, z], dtype=np.float32)

