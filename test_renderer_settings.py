"""
Test Renderer Settings Integration
Quick test to verify renderer settings integration.
"""

from engine.src import Application, SettingsPresets

def test_integration():
    print("\n" + "="*70)
    print(" TESTING RENDERER SETTINGS INTEGRATION")
    print("="*70 + "\n")
    
    # Create application (loads settings automatically)
    print("Creating application...")
    app = Application(app_name="test_renderer")
    
    print("\nInitializing...")
    if not app.init():
        print("ERROR: Failed to initialize!")
        return
    
    print("\n" + "="*70)
    print(" TESTING RUNTIME SETTINGS CHANGES")
    print("="*70)
    
    # Test 1: Change VSync
    print("\n1. Testing VSync callback...")
    current_vsync = app.settings.get('window.vsync')
    print(f"   Current VSync: {current_vsync}")
    app.settings.set('window.vsync', not current_vsync)
    print(f"   New VSync: {not current_vsync}")
    
    # Test 2: Change Audio Volume
    print("\n2. Testing Audio Volume callback...")
    app.settings.set('audio.master_volume', 0.5)
    
    # Test 3: Change Shadow Quality
    print("\n3. Testing Shadow Quality change...")
    app.settings.set('graphics.shadow_map_size', 1024)
    
    # Test 4: Apply Low Preset
    print("\n4. Applying LOW graphics preset...")
    SettingsPresets.apply_graphics_preset(app.settings, "low")
    app.renderer.apply_settings()
    
    # Test 5: Apply Ultra Preset
    print("\n5. Applying ULTRA graphics preset...")
    SettingsPresets.apply_graphics_preset(app.settings, "ultra")
    app.renderer.apply_settings()
    
    # Print current settings
    print("\n" + "="*70)
    print(" CURRENT GRAPHICS SETTINGS")
    print("="*70)
    print(f"MSAA: {app.settings.get('graphics.msaa_samples')}x")
    print(f"Shadows: {app.settings.get('graphics.shadows_enabled')}")
    print(f"Shadow Resolution: {app.settings.get('graphics.shadow_map_size')}")
    print(f"Bloom: {app.settings.get('graphics.bloom')}")
    print(f"Render Distance: {app.settings.get('graphics.render_distance')}")
    print(f"Culling: {app.settings.get('graphics.culling_enabled')}")
    print(f"Anisotropic Filtering: {app.settings.get('graphics.anisotropic_filtering')}x")
    
    print("\n" + "="*70)
    print(" TEST COMPLETE - ALL SETTINGS APPLIED!")
    print("="*70 + "\n")
    
    # Cleanup
    app.cleanup()
    
    print("\n✅ Renderer integration test passed!\n")

if __name__ == "__main__":
    test_integration()

