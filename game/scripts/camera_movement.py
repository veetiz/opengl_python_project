"""
Camera Movement Script
Handles camera movement and rotation based on input.
"""

from engine.src import GameScript
import glfw


class CameraMovementScript(GameScript):
    """Script that handles camera movement and rotation from input."""
    
    def __init__(
        self,
        entity=None,
        move_speed: float = 2.5,
        rotate_speed: float = 50.0,
        mouse_sensitivity: float = 0.1
    ):
        """
        Initialize camera movement script.
        
        Args:
            entity: Camera entity to control
            move_speed: Movement speed (units per second)
            rotate_speed: Rotation speed (degrees per second) for keyboard
            mouse_sensitivity: Mouse rotation sensitivity
        """
        super().__init__(entity)
        self.move_speed = move_speed
        self.rotate_speed = rotate_speed
        self.mouse_sensitivity = mouse_sensitivity
        
        # Reference to input system (will be set by scene)
        self.input = None
    
    def on_start(self):
        """Called when script starts."""
        if self.entity:
            print(f"[CameraMovementScript] Attached to camera '{self.entity.name}'")
    
    def on_update(self, delta_time: float):
        """Update camera based on input."""
        if not self.entity or not self.input:
            return
        
        # Get the camera
        camera = self.entity
        
        # Check if camera has required methods
        if not all(hasattr(camera, m) for m in ['move_forward', 'move_backward', 'move_left', 
                                                   'move_right', 'move_up', 'move_down', 'rotate']):
            return
        
        velocity = self.move_speed * delta_time
        
        # === KEYBOARD MOVEMENT ===
        if self.input.keyboard.is_key_pressed(glfw.KEY_W):
            camera.move_forward(velocity)
        if self.input.keyboard.is_key_pressed(glfw.KEY_S):
            camera.move_backward(velocity)
        if self.input.keyboard.is_key_pressed(glfw.KEY_A):
            camera.move_left(velocity)
        if self.input.keyboard.is_key_pressed(glfw.KEY_D):
            camera.move_right(velocity)
        if self.input.keyboard.is_key_pressed(glfw.KEY_Q):
            camera.move_down(velocity)
        if self.input.keyboard.is_key_pressed(glfw.KEY_E):
            camera.move_up(velocity)
        
        # === KEYBOARD ROTATION (Arrow Keys) ===
        rotation_delta = self.rotate_speed * delta_time
        yaw_change = 0.0
        pitch_change = 0.0
        
        if self.input.keyboard.is_key_pressed(glfw.KEY_LEFT):
            yaw_change -= rotation_delta
        if self.input.keyboard.is_key_pressed(glfw.KEY_RIGHT):
            yaw_change += rotation_delta
        if self.input.keyboard.is_key_pressed(glfw.KEY_UP):
            pitch_change += rotation_delta
        if self.input.keyboard.is_key_pressed(glfw.KEY_DOWN):
            pitch_change -= rotation_delta
        
        if yaw_change != 0.0 or pitch_change != 0.0:
            camera.rotate(yaw_change, pitch_change)
        
        # === MOUSE ROTATION (when captured) ===
        if self.input.mouse.captured:
            mouse_offset = self.input.mouse.get_offset()
            if mouse_offset[0] != 0.0 or mouse_offset[1] != 0.0:
                # Apply mouse sensitivity
                yaw = mouse_offset[0] * self.mouse_sensitivity
                pitch = mouse_offset[1] * self.mouse_sensitivity
                camera.rotate(yaw, pitch)
        
        # === MOUSE SCROLL ZOOM ===
        if self.input.scroll_offset != 0.0 and hasattr(camera, 'zoom'):
            camera.zoom(self.input.scroll_offset)

