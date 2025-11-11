"""
OpenGL Application
Entry point for the OpenGL application.
"""

import sys
import time
from src import (
    Application, Scene, SplashScene, GameObject, Model, Camera, GameScript, 
    ModelLoader, Texture, FontLoader, DirectionalLight, PointLight, SpotLight, Material,
    Text3D
)
from game.scripts import RotateScript, FPSCounterScript, CameraMovementScript, TextUIScript, SplashTransitionScript


def create_main_scene():
    """Create the main game scene with 3D objects."""
    print("\n" + "=" * 70)
    print("Creating main scene...")
    print("=" * 70)
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
    
    # === CREATE LIGHTS ===
    
    print("\nAdding lights to scene...")
    
    # Add a directional light (like the sun)
    sun_light = DirectionalLight(
        name="Sun",
        direction=(0.3, -0.8, -0.5),  # Coming from top-right
        color=(1.0, 0.95, 0.9),  # Slightly warm white
        intensity=0.4,  # Lower intensity for subtle lighting
        cast_shadows=True  # Enable shadows!
    )
    scene.add_light(sun_light)
    print(f"[OK] Directional light 'Sun' added with shadows")
    
    # Add a point light for additional illumination
    point_light = PointLight(
        name="LightBulb",
        position=(2.0, 2.0, 2.0),
        color=(1.0, 1.0, 1.0),
        intensity=0.3,  # Lower intensity
        constant=1.0,
        linear=0.14,    # Increased falloff
        quadratic=0.07  # Increased falloff
    )
    scene.add_light(point_light)
    print(f"[OK] Point light 'LightBulb' added")
    
    # Add a spotlight
    spot_light = SpotLight(
        name="Flashlight",
        position=(-2.0, 2.0, 3.0),
        direction=(0.5, -0.5, -1.0),
        color=(1.0, 0.9, 0.8),  # Slightly warm
        intensity=0.5,
        inner_cutoff=12.5,  # degrees
        outer_cutoff=17.5,  # degrees
        constant=1.0,
        linear=0.09,
        quadratic=0.032,
        cast_shadows=True  # Enable shadows!
    )
    scene.add_light(spot_light)
    print(f"[OK] Spot light 'Flashlight' added with shadows")
    
    # === CREATE GAME OBJECTS ===
    
    # NOTE: Don't load textures yet - OpenGL context doesn't exist until app.run()
    # Create model with texture path, load texture after init
    print("\nCreating textured quad (texture will load after OpenGL init)...")
    
    # Store texture paths for later loading
    texture_path = "assets/textures/Substance_graph_basecolor.png"
    normal_map_path = "assets/textures/Substance_graph_normal.png"
    roughness_map_path = "assets/textures/Substance_graph_roughness.png"
    ao_map_path = "assets/textures/Substance_graph_ambientocclusion.png"
    
    # Create a simple textured quad (simpler than cube for testing)
    wood_model = Model.create_textured_quad("WoodQuad", texture=None)
    
    # Create a material for the wooden quad
    wood_material = Material(
        name="Wood",
        ambient=(0.4, 0.35, 0.3),  # Higher ambient to keep scene visible
        diffuse=(0.8, 0.7, 0.6),   # Wood-like diffuse
        specular=(0.3, 0.3, 0.3),  # Low specular (wood is not very shiny)
        shininess=16.0,
        normal_map=None,  # Will be loaded after OpenGL init
        roughness_map=None,  # Will be loaded after OpenGL init
        ao_map=None  # Will be loaded after OpenGL init
    )
    
    wood_obj = GameObject(
        name="WoodQuad",
        model=wood_model,
        material=wood_material,
        position=(0.0, 0.0, 0.0),
        rotation=(0.0, 0.0, 0.0),
        scale=(2.0, 2.0, 2.0)  # Make it bigger
    )
    scene.add_game_object(wood_obj)
    
    # Store texture paths as custom properties so we can load them after OpenGL init
    wood_obj._texture_path = texture_path
    wood_obj._normal_map_path = normal_map_path
    wood_obj._roughness_map_path = roughness_map_path
    wood_obj._ao_map_path = ao_map_path
    
    # Attach a rotation script to see it from all angles
    rotate_script = RotateScript(rotation_speed=(0, 30, 0))  # Rotate around Y axis only
    wood_obj.add_script(rotate_script)
    print(f"[OK] Textured quad created with RotateScript")
    
    # Note: Texture will be loaded after OpenGL initialization
    
    # === CREATE 3D TEXT ===
    
    print("\nAdding 3D text to scene...")
    
    # Create a 3D text label floating above the wood quad
    label_3d = Text3D(
        label="WoodLabel",
        text="PBR Material with Shadows",
        font=None,  # Will be set by text_ui_script
        position=(0.0, 1.5, 0.0),  # Above the quad
        size=0.15,  # Size in world units
        color=(1.0, 1.0, 0.0),  # Yellow
        billboard=True,  # Always face camera
        visible=True
    )
    scene.add_text3d(label_3d)
    print(f"[OK] 3D text '{label_3d.label}' added at position {label_3d.position}")
    
    # Create another 3D text label (world-oriented)
    # World-oriented: stays fixed in space, same base orientation as wood quad
    world_text = Text3D(
        label="WorldText",
        text="WORLD",
        font=None,  # Will be set by text_ui_script
        position=(0.0, -1.8, 0.0),  # Below the quad
        rotation=(0.0, 0.0, 0.0),  # Same base rotation as wood quad
        size=0.12,  # Slightly larger
        scale=(1.0, 1.0, 1.0),  # Same scale as base (no flips)
        color=(0.2, 1.0, 0.2),  # Bright green
        billboard=False,  # World-oriented - stays fixed in space
        visible=True
    )
    scene.add_text3d(world_text)
    print(f"[OK] 3D text '{world_text.label}' added at position {world_text.position}")
    
    # Attach text UI script to load font (for main scene HUD and 3D text)
    text_ui_script = TextUIScript(font_size=24)
    scene.add_script(text_ui_script)
    
    # Attach a global FPS counter script
    fps_script = FPSCounterScript(print_interval=3.0)
    scene.add_script(fps_script)
    
    print(f"[OK] Main scene created with {scene.object_count} object(s), {scene.camera_count} camera(s), and {scene.text3d_count} 3D text(s)")
    
    return scene, text_ui_script


def create_splash_scene(app, main_scene):
    """Create the splash screen scene."""
    print("\n" + "=" * 70)
    print("Creating splash scene...")
    print("=" * 70)
    
    splash = SplashScene(name="Splash")
    splash.set_title("OpenGL Game Engine")
    splash.set_loading_text("Loading...")
    
    # Add transition script to automatically switch to main scene
    transition_script = SplashTransitionScript(
        duration=3.0,  # Show splash for 3 seconds
        main_scene=main_scene,
        app=app
    )
    splash.add_script(transition_script)
    
    # Add font loading script for splash text
    font_script = TextUIScript(font_size=48)
    splash.add_script(font_script)
    
    print(f"[OK] Splash scene created")
    
    return splash, font_script


def main():
    """Main entry point."""
    print("=" * 70)
    print(" OpenGL Game Engine - Python")
    print("=" * 70)
    print()
    
    # Create application with desired settings
    app = Application(
        width=800,
        height=600,
        title="OpenGL Game Engine",
        enable_validation=False  # Set to True for debugging
    )
    
    # Create main scene first (so it's ready for transition)
    main_scene, main_text_script = create_main_scene()
    
    # Create splash scene with reference to main scene for transition
    splash_scene, splash_font_script = create_splash_scene(app, main_scene)
    
    # Set up UI text callback
    def render_ui_callback(text_renderer):
        """Render UI text based on current scene."""
        current_scene = app.renderer.scene if app.renderer else None
        
        # Splash scene rendering
        if current_scene == splash_scene and splash_font_script.font:
            # Apply fonts to splash text entities if not already set
            if not splash_scene.title_text.font:
                splash_scene.set_fonts(splash_font_script.font, splash_font_script.font)
        
        # Main scene rendering
        elif current_scene == main_scene and main_text_script.font:
            # Render control instructions
            text_renderer.render_text(
                main_text_script.font,
                "WASD: Move | Arrows: Rotate | TAB: Mouse | C: Camera | ESC: Exit",
                10, 10,
                scale=0.7,
                color=(0.8, 0.8, 0.8)
            )
    
    app.set_ui_text_callback(render_ui_callback)
    
    print("\n" + "=" * 70)
    print(" Ready to start!")
    print("=" * 70)
    print()
    
    # Run the application starting with splash scene
    # Transition script will automatically switch to main scene after 2 seconds
    return app.run(splash_scene)


if __name__ == "__main__":
    sys.exit(main())
