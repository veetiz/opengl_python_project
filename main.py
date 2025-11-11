"""
OpenGL Application
Entry point for the OpenGL application.
"""

import sys
from src import Application, Scene, GameObject, Model, Camera, GameScript, ModelLoader, Texture
from game.scripts import RotateScript, FPSCounterScript, CameraMovementScript


def main():
    """Main entry point."""
    print("=" * 70)
    print(" OpenGL Triangle Renderer - Python")
    print("=" * 70)
    print()
    
    # Create application with desired settings
    app = Application(
        width=800,
        height=600,
        title="OpenGL Triangle - Python",
        enable_validation=False  # Set to True for debugging
    )
    
    # Create scene (before initialization for aspect ratio calculation)
    print("\nCreating scene...")
    scene = Scene("Main Scene")
    
    # Create and add multiple cameras to scene
    # Camera 1: Front view (default/active) with movement controls
    front_camera = Camera(
        name="FrontCamera",
        position=(0.0, 0.0, 3.0),
        target=(0.0, 0.0, 0.0),
        up=(0.0, 1.0, 0.0),
        fov=45.0,
        aspect_ratio=800.0 / 600.0,  # Use default aspect ratio
        near=0.1,
        far=100.0
    )
    
    # Attach camera movement script to front camera
    camera_movement = CameraMovementScript(
        move_speed=2.5,
        rotate_speed=50.0,
        mouse_sensitivity=0.1
    )
    front_camera.add_script(camera_movement)
    
    scene.add_camera(front_camera)
    print(f"[OK] Camera '{front_camera.name}' added to scene (index 0) with CameraMovementScript")
    
    # Camera 2: Top-down view
    top_camera = Camera(
        name="TopCamera",
        position=(0.0, 5.0, 0.0),
        target=(0.0, 0.0, 0.0),
        up=(0.0, 0.0, -1.0),
        fov=60.0,
        aspect_ratio=800.0 / 600.0,  # Use default aspect ratio
        near=0.1,
        far=100.0
    )
    scene.add_camera(top_camera)
    print(f"[OK] Camera '{top_camera.name}' added to scene (index 1)")
    
    # Set active camera (index 0 = front camera)
    scene.set_active_camera(0)
    print(f"[OK] Active camera: {scene.active_camera_index}")
    
    # === CREATE GAME OBJECTS ===
    
    # NOTE: Don't load textures yet - OpenGL context doesn't exist until app.run()
    # Create model with texture path, load texture after init
    print("\nCreating textured quad (texture will load after OpenGL init)...")
    
    # Store texture path for later loading
    texture_path = "assets/textures/Substance_graph_basecolor.png"
    
    # Create a simple textured quad (simpler than cube for testing)
    wood_model = Model.create_textured_quad("WoodQuad", texture=None)
    
    wood_obj = GameObject(
        name="WoodQuad",
        model=wood_model,
        position=(0.0, 0.0, 0.0),
        rotation=(0.0, 0.0, 0.0),
        scale=(2.0, 2.0, 2.0)  # Make it bigger
    )
    scene.add_game_object(wood_obj)
    
    # Store texture path as custom property so we can load it after OpenGL init
    wood_obj._texture_path = texture_path
    
    # Attach a rotation script to see it from all angles
    rotate_script = RotateScript(rotation_speed=(0, 30, 0))  # Rotate around Y axis only
    wood_obj.add_script(rotate_script)
    print(f"[OK] Textured quad created with RotateScript")
    
    # Note: Texture will be loaded after OpenGL initialization
    
    # Attach a global FPS counter script to the scene (global script)
    fps_script = FPSCounterScript(print_interval=3.0)  # Print FPS every 3 seconds
    scene.add_script(fps_script)
    print(f"[OK] FPSCounterScript added to scene (global)")
    
    # Count total scripts
    entity_script_count = sum(len(entity.scripts) for entity in scene.get_all_entities())
    
    print(f"[OK] Scene created with {scene.object_count} object(s) and {scene.camera_count} camera(s)")
    print(f"[OK] Total scripts: {entity_script_count} entity scripts + {len(scene.scripts)} global scripts")
    
    print("\n" + "=" * 70)
    print(" Ready to render!")
    print("=" * 70)
    print()
    
    # Run the application with the scene
    # app.run() will call init(), then set the scene, then start the main loop
    return app.run(scene)


if __name__ == "__main__":
    sys.exit(main())
