"""
Modern Settings Menu Scene
Game-specific settings menu using modern OpenGL UI components.
"""

from engine.src import Scene, SettingsManager, SettingsPresets
from engine.src.ui import (
    UIManager, ModernPanel, ModernButton, ModernLabel, ModernSlider,
    ModernCheckbox, ModernDropdown, Anchor, DefaultTheme
)


class ModernSettingsMenuScene(Scene):
    """
    Modern settings menu with OpenGL-based UI components.
    Uses theme system for customizable appearance.
    """
    
    def __init__(
        self,
        name: str = "Settings Menu",
        app=None,
        return_scene=None,
        theme=None
    ):
        """
        Initialize modern settings menu.
        
        Args:
            name: Scene name
            app: Application instance
            return_scene: Scene to return to when closing
            theme: UITheme instance (uses DefaultTheme if None)
        """
        super().__init__(name)
        
        self.app = app
        self.return_scene = return_scene
        self.theme = theme or DefaultTheme()
        self.ui_manager: UIManager = None
        
        self._initialized = False
    
    def initialize_ui(self, window_width: int, window_height: int):
        """
        Initialize modern UI elements.
        
        Args:
            window_width: Window width
            window_height: Window height
        """
        if self._initialized:
            return
        
        print("[ModernSettingsMenu] Initializing modern UI...")
        
        self.ui_manager = UIManager(window_width, window_height)
        
        # Main panel
        panel_width = 600
        panel_height = 500
        panel_x = (window_width - panel_width) / 2
        panel_y = (window_height - panel_height) / 2
        
        main_panel = ModernPanel(
            x=panel_x,
            y=panel_y,
            width=panel_width,
            height=panel_height,
            style=self.theme.panel
        )
        self.ui_manager.add_element(main_panel)
        
        # Title
        title = ModernLabel(
            x=20,
            y=10,
            text="SETTINGS",
            size=1.5,
            bold=True,
            style=self.theme.label
        )
        main_panel.add_child(title)
        
        # === GRAPHICS SECTION ===
        
        graphics_header = ModernLabel(
            x=20,
            y=50,
            text="GRAPHICS",
            size=1.2,
            bold=True,
            style=self.theme.label
        )
        main_panel.add_child(graphics_header)
        
        # Graphics preset buttons
        presets = ["Low", "Medium", "High", "Ultra"]
        for i, preset in enumerate(presets):
            btn = ModernButton(
                x=20 + i * 135,
                y=80,
                width=125,
                height=35,
                text=preset,
                on_click=lambda p=preset.lower(): self._on_preset_click(p),
                style=self.theme.button
            )
            main_panel.add_child(btn)
        
        # Shadow Quality Slider (with more space for label)
        shadow_current = self.app.settings.get('graphics.shadow_map_size') if self.app else 2048
        shadow_value = {512: 0.0, 1024: 0.33, 2048: 0.66, 4096: 1.0}.get(shadow_current, 0.66)
        
        shadow_slider = ModernSlider(
            x=20,
            y=145,  # Lower to give space for label
            width=480,
            height=30,
            min_value=0.0,
            max_value=1.0,
            current_value=shadow_value,
            on_value_change=self._on_shadow_quality_change,
            label="Shadow Quality",
            style=self.theme.slider
        )
        main_panel.add_child(shadow_slider)
        
        # MSAA Dropdown (with label, more spacing from slider)
        msaa_label = ModernLabel(
            x=20,
            y=195,
            text="MSAA:",
            size=0.9,
            style=self.theme.label
        )
        main_panel.add_child(msaa_label)
        
        msaa_current = self.app.settings.get('graphics.msaa_samples') if self.app else 4
        msaa_options = ["Off", "2x", "4x", "8x"]
        msaa_map = {0: 0, 2: 1, 4: 2, 8: 3}
        msaa_index = msaa_map.get(msaa_current, 2)
        
        msaa_dropdown = ModernDropdown(
            x=100,
            y=190,
            width=150,
            height=30,
            options=msaa_options,
            selected_index=msaa_index,
            on_select=self._on_msaa_change,
            style=self.theme.dropdown
        )
        main_panel.add_child(msaa_dropdown)
        
        # VSync Checkbox (with more spacing)
        vsync_current = self.app.settings.get('window.vsync') if self.app else True
        vsync_checkbox = ModernCheckbox(
            x=20,
            y=240,
            label="VSync",
            checked=vsync_current,
            on_toggle=self._on_vsync_toggle,
            style=self.theme.checkbox
        )
        main_panel.add_child(vsync_checkbox)
        
        # Fullscreen Checkbox
        fullscreen_current = self.app.settings.get('window.fullscreen') if self.app else False
        fullscreen_checkbox = ModernCheckbox(
            x=200,
            y=240,
            label="Fullscreen",
            checked=fullscreen_current,
            on_toggle=self._on_fullscreen_toggle,
            style=self.theme.checkbox
        )
        main_panel.add_child(fullscreen_checkbox)
        
        # === AUDIO SECTION ===
        
        audio_header = ModernLabel(
            x=20,
            y=290,
            text="AUDIO",
            size=1.2,
            bold=True,
            style=self.theme.label
        )
        main_panel.add_child(audio_header)
        
        # Master Volume Slider
        master_vol_current = self.app.settings.get('audio.master_volume') if self.app else 0.8
        
        master_vol_slider = ModernSlider(
            x=20,
            y=335,  # More space for label
            width=480,
            height=30,
            min_value=0.0,
            max_value=1.0,
            current_value=master_vol_current,
            on_value_change=self._on_master_volume_change,
            label="Master Volume",
            style=self.theme.slider
        )
        main_panel.add_child(master_vol_slider)
        
        # Music Volume Slider
        music_vol_current = self.app.settings.get('audio.music_volume') if self.app else 0.6
        
        music_vol_slider = ModernSlider(
            x=20,
            y=390,  # Proper spacing
            width=480,
            height=30,
            min_value=0.0,
            max_value=1.0,
            current_value=music_vol_current,
            on_value_change=self._on_music_volume_change,
            label="Music Volume",
            style=self.theme.slider
        )
        main_panel.add_child(music_vol_slider)
        
        # === ACTION BUTTONS ===
        
        # Apply Button
        apply_btn = ModernButton(
            x=20,
            y=440,
            width=120,
            height=40,
            text="APPLY",
            on_click=self._on_apply,
            style=self.theme.button
        )
        main_panel.add_child(apply_btn)
        
        # Reset Button
        reset_btn = ModernButton(
            x=160,
            y=440,
            width=120,
            height=40,
            text="RESET",
            on_click=self._on_reset,
            style=self.theme.button
        )
        main_panel.add_child(reset_btn)
        
        # Back Button
        back_btn = ModernButton(
            x=300,
            y=440,
            width=120,
            height=40,
            text="BACK",
            on_click=self._on_back,
            style=self.theme.button
        )
        main_panel.add_child(back_btn)
        
        self._initialized = True
        print("[ModernSettingsMenu] Modern UI initialized")
    
    # === Callbacks ===
    
    def _on_preset_click(self, preset: str):
        """Handle graphics preset click."""
        print(f"[ModernSettingsMenu] Applying {preset} preset...")
        if self.app and self.app.settings:
            SettingsPresets.apply_graphics_preset(self.app.settings, preset)
    
    def _on_shadow_quality_change(self, value: float):
        """Handle shadow quality slider change."""
        resolutions = {
            0.0: 512,
            0.33: 1024,
            0.66: 2048,
            1.0: 4096
        }
        
        # Find closest resolution
        closest_value = min(resolutions.keys(), key=lambda k: abs(k - value))
        shadow_size = resolutions[closest_value]
        
        if self.app and self.app.settings:
            self.app.settings.set('graphics.shadow_map_size', shadow_size)
    
    def _on_msaa_change(self, index: int, text: str):
        """Handle MSAA dropdown change."""
        msaa_map = {"Off": 0, "2x": 2, "4x": 4, "8x": 8}
        msaa_value = msaa_map.get(text, 4)
        
        if self.app and self.app.settings:
            self.app.settings.set('graphics.msaa_samples', msaa_value)
    
    def _on_vsync_toggle(self, value: bool):
        """Handle VSync checkbox toggle."""
        if self.app and self.app.settings:
            self.app.settings.set('window.vsync', value)
    
    def _on_fullscreen_toggle(self, value: bool):
        """Handle fullscreen checkbox toggle."""
        if self.app and self.app.settings:
            self.app.settings.set('window.fullscreen', value)
    
    def _on_master_volume_change(self, value: float):
        """Handle master volume slider change."""
        if self.app and self.app.settings:
            self.app.settings.set('audio.master_volume', value)
    
    def _on_music_volume_change(self, value: float):
        """Handle music volume slider change."""
        if self.app and self.app.settings:
            self.app.settings.set('audio.music_volume', value)
    
    def _on_apply(self):
        """Handle Apply button click."""
        print("\n[ModernSettingsMenu] Applying settings...")
        if self.app:
            if self.app.renderer:
                self.app.renderer.apply_settings()
            
            # Force UI font reload
            if hasattr(self, '_ui_font'):
                delattr(self, '_ui_font')
            
            self.app.settings.save()
            print("[ModernSettingsMenu] Settings applied and saved!")
    
    def _on_reset(self):
        """Handle Reset button click."""
        print("\n[ModernSettingsMenu] Resetting to defaults...")
        if self.app and self.app.settings:
            self.app.settings.reset_to_defaults('graphics')
            self.app.settings.reset_to_defaults('audio')
            print("[ModernSettingsMenu] Settings reset!")
    
    def _on_back(self):
        """Handle Back button click."""
        print("[ModernSettingsMenu] Returning to game...")
        if self.app and self.return_scene:
            self.app.renderer.set_scene(self.return_scene)
    
    # === Scene Methods ===
    
    def update(self, delta_time: float):
        """Update the scene."""
        super().update(delta_time)
        
        if self.ui_manager:
            self.ui_manager.update(delta_time)
    
    def on_mouse_move(self, x: float, y: float):
        """Handle mouse movement."""
        if self.ui_manager:
            self.ui_manager.on_mouse_move(x, y)
    
    def on_mouse_click(self, x: float, y: float, button: int):
        """Handle mouse click."""
        if self.ui_manager:
            self.ui_manager.on_mouse_click(x, y, button)
    
    def on_mouse_release(self, x: float, y: float, button: int):
        """Handle mouse release."""
        if self.ui_manager:
            self.ui_manager.on_mouse_release(x, y, button)
    
    def render_ui(self, text_renderer):
        """
        Render modern UI elements.
        
        Args:
            text_renderer: TextRenderer instance
        """
        if not self._initialized and self.app:
            width = self.app.width if hasattr(self.app, 'width') else 1280
            height = self.app.height if hasattr(self.app, 'height') else 720
            self.initialize_ui(width, height)
        
        if self.ui_manager and self.app and self.app.ui_renderer:
            # Load font for text labels
            if not hasattr(self, '_ui_font'):
                from engine.src import FontLoader
                self._ui_font = FontLoader.load("C:/Windows/Fonts/arial.ttf", 24)
                print(f"[ModernSettingsMenu] UI font loaded")
            
            # Save OpenGL state before UI rendering
            from OpenGL.GL import (glIsEnabled, glEnable, glDisable, GL_BLEND, 
                                  GL_DEPTH_TEST, glBlendFunc, GL_SRC_ALPHA, 
                                  GL_ONE_MINUS_SRC_ALPHA)
            
            depth_was_enabled = glIsEnabled(GL_DEPTH_TEST)
            
            # Set up for 2D UI rendering
            glDisable(GL_DEPTH_TEST)
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Attach font to text_renderer for labels
            text_renderer.font = self._ui_font
            
            # Render all UI elements with both renderers
            # Pass 1: Render all elements except open dropdowns
            for element in self.ui_manager.elements:
                if element.visible:
                    # Check if it's a dropdown that needs to render children
                    skip_for_z_order = False
                    for child in element.children if hasattr(element, 'children') else []:
                        if hasattr(child, 'is_open') and child.is_open:
                            skip_for_z_order = True
                            break
                    
                    if not skip_for_z_order:
                        element.render(self.app.ui_renderer, text_renderer)
            
            # Pass 2: Render panels with open dropdowns (on top)
            for element in self.ui_manager.elements:
                if element.visible:
                    # Check if any child dropdown is open
                    has_open_dropdown = False
                    for child in element.children if hasattr(element, 'children') else []:
                        if hasattr(child, 'is_open') and child.is_open:
                            has_open_dropdown = True
                            break
                    
                    if has_open_dropdown:
                        # Re-render the panel and its open dropdown on top
                        element.render(self.app.ui_renderer, text_renderer)
            
            # Clean up font
            if hasattr(text_renderer, 'font'):
                delattr(text_renderer, 'font')
            
            # Restore OpenGL state
            if depth_was_enabled:
                glEnable(GL_DEPTH_TEST)

