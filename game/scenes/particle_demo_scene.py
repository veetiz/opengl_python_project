"""
Particle Demo Scene
Demonstrates the particle system with various effects.
"""

from engine.src import Scene, Camera, ParticleSystem, ParticlePresets
import numpy as np


class ParticleDemoScene(Scene):
    """
    Demo scene showcasing particle effects.
    """
    
    def __init__(self, name: str = "Particle Demo"):
        """Initialize particle demo scene."""
        super().__init__(name)
        
        self.particle_system = None
        self.current_effect = 0
        self.effect_names = ["fire", "smoke", "sparkles", "magic_aura", "explosion"]
        self.switch_cooldown = 0.0
    
    def init(self):
        """Initialize scene."""
        super().init()
        
        # Create camera
        camera = Camera(
            name="ParticleCamera",
            position=np.array([0.0, 2.0, 8.0], dtype=np.float32),
            target=np.array([0.0, 1.0, 0.0], dtype=np.float32),
            fov=45.0
        )
        self.add_camera(camera)
        self.set_active_camera(0)  # Use index, not name
        
        # Initialize particle system
        self.particle_system = ParticleSystem()
        if not self.particle_system.init():
            print("[ERROR] Failed to initialize particle system")
            return False
        
        # Add initial fire effect
        self._create_effect("fire")
        
        # Add text instructions
        from engine.src import Text2D
        instructions = Text2D(
            label="instructions",
            text="Press SPACE to cycle particle effects",
            x=10, y=10,
            scale=1.0,
            color=(1.0, 1.0, 1.0)
        )
        self.text2d_objects.append(instructions)
        
        effect_label = Text2D(
            label="effect_label",
            text=f"Current: {self.effect_names[self.current_effect].upper()}",
            x=10, y=40,
            scale=1.2,
            color=(0.3, 1.0, 0.5)
        )
        self.text2d_objects.append(effect_label)
        
        print(f"[ParticleDemoScene] Initialized with {self.effect_names[0]}")
        return True
    
    def _create_effect(self, effect_name: str):
        """Create a particle effect at center."""
        # Clear existing emitters
        self.particle_system.emitters.clear()
        
        # Create new effect at origin
        position = (0.0, 1.0, 0.0)
        
        if effect_name == "fire":
            emitter = ParticlePresets.create_fire(position)
        elif effect_name == "smoke":
            emitter = ParticlePresets.create_smoke(position)
        elif effect_name == "sparkles":
            emitter = ParticlePresets.create_sparkles(position)
        elif effect_name == "magic_aura":
            emitter = ParticlePresets.create_magic_aura(position)
        elif effect_name == "explosion":
            emitter = ParticlePresets.create_explosion(position)
            # Trigger one-time burst
            emitter.is_emitting = True
            for _ in range(50):
                emitter._spawn_particle()
            emitter.is_emitting = False
        else:
            emitter = ParticlePresets.create_fire(position)
        
        self.particle_system.add_emitter(effect_name, emitter)
        
        # Update text label
        if len(self.text2d_objects) > 1:
            self.text2d_objects[1].text = f"Current: {effect_name.upper()}"
    
    def update(self, delta_time: float):
        """Update scene."""
        super().update(delta_time)
        
        # Update particle system
        if self.particle_system:
            self.particle_system.update(delta_time)
        
        # Handle effect switching
        self.switch_cooldown = max(0, self.switch_cooldown - delta_time)
        
        # Space key to switch effects (using GLFW directly for now)
        import glfw
        # We'd need input handling here, but for demo purposes
        # the user can implement key binding
    
    def render_particles(self, view_matrix: np.ndarray, projection_matrix: np.ndarray):
        """
        Render particles.
        
        Args:
            view_matrix: Camera view matrix
            projection_matrix: Camera projection matrix
        """
        if self.particle_system:
            self.particle_system.render(view_matrix, projection_matrix)
    
    def switch_to_next_effect(self):
        """Switch to the next particle effect."""
        if self.switch_cooldown > 0:
            return
        
        self.current_effect = (self.current_effect + 1) % len(self.effect_names)
        effect_name = self.effect_names[self.current_effect]
        self._create_effect(effect_name)
        self.switch_cooldown = 0.5  # Cooldown to prevent rapid switching
        
        print(f"[ParticleDemoScene] Switched to: {effect_name}")
    
    def cleanup(self):
        """Clean up scene resources."""
        if self.particle_system:
            self.particle_system.cleanup()
        
        super().cleanup()

