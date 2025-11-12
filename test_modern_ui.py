"""
Test Modern UI System
Quick test to verify OpenGL-based UI components work.
"""

import sys
from engine.src import Application
from game.scenes.modern_settings_menu import ModernSettingsMenuScene
from engine.src.ui import DefaultTheme, DarkTheme, GameCustomTheme


def test_modern_ui():
    """Test modern UI components."""
    print("=" * 70)
    print(" TESTING MODERN UI SYSTEM")
    print("=" * 70)
    print()
    
    # Create app
    app = Application(
        width=800,
        height=600,
        title="Modern UI Test",
        app_name="modern_ui_test"
    )
    
    print("\nAvailable themes:")
    print("  1. DefaultTheme (modern, clean)")
    print("  2. DarkTheme (dark mode)")
    print("  3. GameCustomTheme (blue/gold example)")
    print()
    
    # Choose theme
    theme_choice = "default"  # Change to "dark" or "custom" to test
    
    if theme_choice == "dark":
        theme = DarkTheme()
        print("[OK] Using DarkTheme")
    elif theme_choice == "custom":
        theme = GameCustomTheme()
        print("[OK] Using GameCustomTheme")
    else:
        theme = DefaultTheme()
        print("[OK] Using DefaultTheme")
    
    # Create modern settings menu
    settings_menu = ModernSettingsMenuScene(
        name="Modern Settings Test",
        app=app,
        return_scene=None,
        theme=theme
    )
    
    print("\n" + "=" * 70)
    print(" CONTROLS")
    print("=" * 70)
    print("  - Mouse: Hover and click UI elements")
    print("  - Sliders: Click and drag the circular handles")
    print("  - Checkboxes: Click to toggle")
    print("  - Dropdowns: Click to open, select option")
    print("  - ESC: Exit")
    print("=" * 70)
    print()
    
    print("[OK] Starting modern UI test...")
    print()
    
    # Run
    return app.run(settings_menu)


if __name__ == "__main__":
    sys.exit(test_modern_ui())

