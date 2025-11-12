"""
Simple test: CSS-like sizing in actual game window
"""

import sys
import glfw
from OpenGL.GL import *

from engine.src.core.window import Window
from engine.src.ui import (
    UIManager, UIRenderer, UIPanel, UIButton, UILabel,
    px, vw, vh, calc, DefaultTheme,
    TextRenderer, FontLoader
)


def main():
    """Test CSS sizing in actual game window."""
    window = Window(1280, 720, "CSS Sizing Test")
    
    # UI System
    ui_manager = UIManager(1280, 720)
    ui_renderer = UIRenderer()
    ui_renderer.init()
    ui_renderer.set_projection(1280, 720)
    
    text_renderer = TextRenderer()
    text_renderer.init()
    font = FontLoader.load("C:/Windows/Fonts/arial.ttf", 24)
    
    theme = DefaultTheme()
    
    # Test 1: Simple centered panel with px
    panel = UIPanel(
        x=calc(vw(50), px(-300)),
        y=calc(vh(50), px(-250)),
        width=px(600),
        height=px(500),
        style=theme.panel
    )
    ui_manager.add_element(panel)
    
    # Add a button inside
    button = UIButton(
        x=px(50),
        y=px(50),
        width=px(200),
        height=px(50),
        text="Test Button",
        style=theme.button
    )
    panel.add_child(button)
    
    # Add label
    label = UILabel(
        x=px(50),
        y=px(120),
        text="CSS Sizing Test",
        style=theme.label
    )
    panel.add_child(label)
    
    print("\n" + "="*60)
    print("CSS SIZING TEST")
    print("="*60)
    print(f"Panel x_size: {panel.x_size}")
    print(f"Panel y_size: {panel.y_size}")
    print(f"Panel initial compiled_x: {panel.compiled_x}")
    print(f"Panel initial compiled_y: {panel.compiled_y}")
    print("="*60 + "\n")
    
    frame_count = 0
    
    while not window.should_close() and frame_count < 300:  # Run for 300 frames
        glClearColor(0.1, 0.1, 0.15, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Render UI (this should compile CSS sizes)
        text_renderer.font = font
        
        if frame_count == 0:
            # First frame - check compiled positions
            print("\n[FRAME 0] Before first render:")
            print(f"  Panel compiled_x: {panel.compiled_x}")
            print(f"  Panel compiled_y: {panel.compiled_y}")
            print(f"  Panel get_absolute_position(): {panel.get_absolute_position()}")
        
        ui_manager.render(text_renderer)
        
        if frame_count == 1:
            # Second frame - after compilation
            print("\n[FRAME 1] After compilation:")
            print(f"  Panel compiled_x: {panel.compiled_x}")
            print(f"  Panel compiled_y: {panel.compiled_y}")
            print(f"  Panel get_absolute_position(): {panel.get_absolute_position()}")
            print(f"  Expected: (~340, ~110) for 1280x720")
            print()
        
        # Manual render for debugging
        for element in ui_manager.elements:
            element.render(ui_renderer, text_renderer)
        
        window.swap_buffers()
        window.poll_events()
        frame_count += 1
    
    ui_renderer.cleanup()
    window.terminate()
    return 0


if __name__ == "__main__":
    sys.exit(main())

