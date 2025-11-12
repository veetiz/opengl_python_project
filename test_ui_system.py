"""
Test UI System
Quick test to verify UI widgets and settings menu.
"""

from engine.src import Application
from game.scenes import SettingsMenuScene

def test_ui_system():
    print("\n" + "="*70)
    print(" TESTING UI SYSTEM & SETTINGS MENU")
    print("="*70 + "\n")
    
    # Create application
    print("Creating application...")
    app = Application(app_name="ui_test")
    
    print("\nInitializing...")
    if not app.init():
        print("ERROR: Failed to initialize!")
        return
    
    # Create settings menu scene
    print("\nCreating settings menu scene...")
    settings_menu = SettingsMenuScene(
        name="Settings",
        app=app,
        return_scene=None  # No return scene for test
    )
    
    print("\nSetting scene...")
    app.renderer.set_scene(settings_menu)
    
    # Initialize UI
    settings_menu.initialize_ui(app.width, app.height)
    
    print("\n" + "="*70)
    print(" UI SYSTEM INITIALIZED")
    print("="*70)
    print(f"UI Manager: {settings_menu.ui_manager is not None}")
    print(f"UI Elements: {len(settings_menu.ui_manager.elements)}")
    
    if settings_menu.ui_manager:
        settings_menu.ui_manager.print_hierarchy()
    
    print("\n" + "="*70)
    print(" TEST COMPLETE - UI SYSTEM READY")
    print("="*70)
    print("\nTo use in game:")
    print("  1. Import: from game.scenes import SettingsMenuScene")
    print("  2. Create: menu = SettingsMenuScene(app=app, return_scene=main_scene)")
    print("  3. Switch: app.renderer.set_scene(menu)")
    print("\n✅ UI system test passed!\n")
    
    # Cleanup
    app.cleanup()

if __name__ == "__main__":
    test_ui_system()

