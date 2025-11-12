"""
Visual Demo: CSS-like Percentage Sizing
Shows responsive UI that adapts to window size.
"""

import sys
import glfw
from OpenGL.GL import *

from engine.src.window import Window
from engine.src.ui import (
    UIManager, UIRenderer, UIPanel, UIButton, UILabel,
    px, percent, vw, vh, DefaultTheme
)


class ResponsiveUIDemo:
    """Demonstrates responsive UI with percentage sizing."""
    
    def __init__(self):
        # Create window
        self.window = Window(1280, 720, "Percentage Sizing Demo - Resize Window!")
        self.window.set_mouse_button_callback(self._on_mouse_button)
        self.window.set_framebuffer_resize_callback(self._on_resize)
        
        # UI System
        self.ui_manager = UIManager(1280, 720)
        self.ui_renderer = UIRenderer()
        self.ui_renderer.init()
        self.ui_renderer.set_projection(1280, 720)
        
        # Build responsive UI
        self._build_ui()
        
        print("\n" + "="*60)
        print("🎨 RESPONSIVE UI DEMO")
        print("="*60)
        print("Try resizing the window - UI will adapt automatically!")
        print("="*60 + "\n")
    
    def _build_ui(self):
        """Build responsive UI layout."""
        theme = DefaultTheme()
        
        # === HEADER (Full-width, fixed height) ===
        header = UIPanel(
            x=vw(0), y=vh(0),
            width=vw(100), height=px(60)
        )
        header.theme = theme
        
        header_label = UILabel(
            x=px(20), y=px(15),
            width=px(500), height=px(30),
            text="Responsive UI Demo - Resize Window!",
            font_size=24
        )
        header_label.theme = theme
        header.add_child(header_label)
        
        self.ui_manager.add_element(header)
        
        # === MAIN CONTENT (Centered, 80% of viewport) ===
        main_panel = UIPanel(
            x=vw(10), y=vh(15),
            width=vw(80), height=vh(70)
        )
        main_panel.theme = theme
        
        # Title
        title = UILabel(
            x=percent(5), y=px(20),
            width=percent(90), height=px(40),
            text="CSS-like Sizing System",
            font_size=28
        )
        title.theme = theme
        main_panel.add_child(title)
        
        # Description
        desc = UILabel(
            x=percent(5), y=px(70),
            width=percent(90), height=px(30),
            text="All elements use vw/vh/% units and resize with window!",
            font_size=18
        )
        desc.theme = theme
        main_panel.add_child(desc)
        
        # === BUTTONS (25% width each, responsive) ===
        button_labels = ["px", "%", "vw", "vh"]
        button_colors = [
            "Uses absolute pixels",
            "Relative to parent",
            "Relative to viewport width",
            "Relative to viewport height"
        ]
        
        for i, (label, color) in enumerate(zip(button_labels, button_colors)):
            btn = UIButton(
                x=percent(5 + i * 23),  # 5%, 28%, 51%, 74%
                y=px(130),
                width=percent(20),  # 20% of panel width
                height=px(50),
                text=label
            )
            btn.theme = theme
            btn.on_click = lambda l=label, c=color: self._on_button_click(l, c)
            main_panel.add_child(btn)
            
            # Description label
            desc_label = UILabel(
                x=percent(5 + i * 23),
                y=px(190),
                width=percent(20),
                height=px(40),
                text=color,
                font_size=12
            )
            desc_label.theme = theme
            main_panel.add_child(desc_label)
        
        # === STATUS PANEL (Bottom, full width) ===
        status_panel = UIPanel(
            x=percent(5), y=vh(60),
            width=percent(90), height=px(100)
        )
        status_panel.theme = theme
        
        self.status_label = UILabel(
            x=px(20), y=px(20),
            width=percent(90), height=px(60),
            text="Click buttons to see unit info\nWindow: 1280x720",
            font_size=16
        )
        self.status_label.theme = theme
        status_panel.add_child(self.status_label)
        
        main_panel.add_child(status_panel)
        
        self.ui_manager.add_element(main_panel)
    
    def _on_button_click(self, unit: str, description: str):
        """Handle button click."""
        w, h = self.window.get_size()
        
        examples = {
            "px": f"px(100) = 100 pixels (always)\nAbsolute size, never changes",
            "%": f"percent(50) = 50% of parent\nIf parent is 400px wide, this = 200px",
            "vw": f"vw(50) = 50% of viewport width\nCurrent window: {w}px → {w*0.5:.0f}px",
            "vh": f"vh(50) = 50% of viewport height\nCurrent window: {h}px → {h*0.5:.0f}px"
        }
        
        self.status_label.text = f"{unit}: {description}\n\n{examples[unit]}"
        print(f"[{unit}] {description}")
    
    def _on_mouse_button(self, window, button, action, mods):
        """Handle mouse button events."""
        if action == glfw.PRESS:
            x, y = self.window.get_cursor_pos()
            w, h = self.window.get_size()
            self.ui_manager.on_mouse_click(x, h - y, button)
    
    def _on_resize(self, window, width, height):
        """Handle window resize."""
        glViewport(0, 0, width, height)
        self.ui_renderer.set_projection(width, height)
        self.ui_manager.set_window_size(width, height)
        
        # Update status label
        if hasattr(self, 'status_label'):
            current_text = self.status_label.text
            # Update window size info
            lines = current_text.split('\n')
            if len(lines) > 1:
                lines[1] = f"Window: {width}x{height}"
                self.status_label.text = '\n'.join(lines)
        
        print(f"Window resized: {width}x{height} (UI auto-adapting)")
    
    def run(self):
        """Run the demo."""
        while not self.window.should_close():
            # Clear
            glClearColor(0.1, 0.1, 0.15, 1.0)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            # Disable depth test for UI
            glDisable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Render UI (will auto-compile CSS-like sizes)
            from engine.src.ui import TextRenderer, FontLoader
            text_renderer = TextRenderer()
            text_renderer.init()
            
            # Render all UI with both renderers
            for element in self.ui_manager.elements:
                self._render_element(element, self.ui_renderer, text_renderer)
            
            # Swap buffers
            self.window.swap_buffers()
            self.window.poll_events()
        
        # Cleanup
        self.ui_renderer.cleanup()
        self.window.terminate()
    
    def _render_element(self, element, ui_renderer, text_renderer):
        """Render an element (recursive)."""
        # Compile sizes before rendering
        self.ui_manager._compile_element_recursive(element)
        
        # Render element
        if hasattr(element, 'render'):
            if hasattr(element, 'theme'):
                element.render(ui_renderer, text_renderer)
            else:
                element.render(text_renderer)
        
        # Render children
        if hasattr(element, 'children'):
            for child in element.children:
                self._render_element(child, ui_renderer, text_renderer)


def main():
    """Run the demo."""
    try:
        demo = ResponsiveUIDemo()
        demo.run()
        return 0
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())

