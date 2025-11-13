"""
Settings Menu Scene
Game-specific settings menu using OpenGL UI components.
"""

from engine.src import Scene, SettingsManager, SettingsPresets
from engine.src.ui import (
    UIManager, UIPanel, UIButton, UILabel, UISlider,
    UICheckbox, UIDropdown, Anchor, DefaultTheme,
    FlexContainer, px, vw, vh, percent, calc, add, sub, mul, div
)


class SettingsMenuScene(Scene):
    """
    Settings menu with OpenGL-based UI components.
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
        self._debug_buttons_once = False
        self._ui_scale_factor = 1.0  # Dynamic scale based on window size
    
    def initialize_ui(self, window_width: int, window_height: int):
        """
        Initialize modern UI elements.
        
        Args:
            window_width: Window width
            window_height: Window height
        """
        if self._initialized:
            return
        
        print("[SettingsMenu] Initializing modern UI with CSS-like sizing...")
        
        # Calculate UI scale factor based on window size (reference: 1280x720)
        self._ui_scale_factor = min(window_width / 1280.0, window_height / 720.0)
        print(f"[SettingsMenu] UI scale factor: {self._ui_scale_factor:.2f}")
        
        # Create scaled theme for this resolution
        scaled_theme = DefaultTheme()
        
        # Scale button theme (ALL properties)
        scaled_theme.button.text_size = 1.0 * self._ui_scale_factor
        scaled_theme.button.padding = 15.0 * self._ui_scale_factor
        scaled_theme.button.border_width = 2.0 * self._ui_scale_factor
        scaled_theme.button.border_radius = 5.0 * self._ui_scale_factor
        
        # Scale label theme (ALL properties)
        scaled_theme.label.text_size = 1.0 * self._ui_scale_factor
        scaled_theme.label.padding = 0.0  # Labels don't use padding
        
        # Scale slider theme (ALL properties)
        scaled_theme.slider.text_size = 1.0 * self._ui_scale_factor
        scaled_theme.slider.track_height = 8.0 * self._ui_scale_factor
        scaled_theme.slider.handle_radius = 12.0 * self._ui_scale_factor
        scaled_theme.slider.border_width = 2.0 * self._ui_scale_factor
        scaled_theme.slider.label_spacing = 10.0 * self._ui_scale_factor
        
        # Scale dropdown theme (ALL properties)
        scaled_theme.dropdown.text_size = 1.0 * self._ui_scale_factor
        scaled_theme.dropdown.padding = 10.0 * self._ui_scale_factor
        scaled_theme.dropdown.border_width = 2.0 * self._ui_scale_factor
        scaled_theme.dropdown.border_radius = 3.0 * self._ui_scale_factor
        scaled_theme.dropdown.item_height = 30.0 * self._ui_scale_factor
        
        # Scale checkbox theme (ALL properties)
        scaled_theme.checkbox.text_size = 1.0 * self._ui_scale_factor
        scaled_theme.checkbox.box_size = 20.0 * self._ui_scale_factor
        scaled_theme.checkbox.border_width = 2.0 * self._ui_scale_factor
        scaled_theme.checkbox.border_radius = 3.0 * self._ui_scale_factor
        scaled_theme.checkbox.check_padding = 4.0 * self._ui_scale_factor
        
        # Scale panel theme (ALL properties)
        scaled_theme.panel.padding = 20.0 * self._ui_scale_factor
        scaled_theme.panel.border_width = 2.0 * self._ui_scale_factor
        scaled_theme.panel.border_radius = 10.0 * self._ui_scale_factor
        
        self.theme = scaled_theme
        
        self.ui_manager = UIManager(window_width, window_height)
        
        # Main panel (responsive, centered, constrained)
        # Uses vw/vh for responsiveness, calc for centering, min/max for constraints
        main_panel = UIPanel(
            x=calc(vw(50), vw(-27.5)),  # Center: 50% - half of 55% = 50% - 27.5%
            y=calc(vh(50), vh(-42.5)),  # Center: 50% - half of 85% = 50% - 42.5%
            width=vw(55),      # 55% of viewport width
            height=vh(85),     # 85% of viewport height
            min_width=px(600),  # Minimum size
            max_width=px(1200), # Maximum size
            style=self.theme.panel
        )
        self.ui_manager.add_element(main_panel)
        
        # Title (responsive positioning, fixed size multiplier)
        title = UILabel(
            x=percent(3),      # ~20px from ~640px panel
            y=percent(1.5),    # Top of panel
            text="SETTINGS",
            size=2.0,  # Reduced from 2.5 - more balanced with sections
            bold=True,
            style=self.theme.label
        )
        main_panel.add_child(title)
        
        # === GRAPHICS SECTION ===
        
        graphics_header = UILabel(
            x=percent(3),      # ~20px
            y=percent(7),      # Increased spacing from title
            text="GRAPHICS",
            size=1.5,  # Reduced from 1.8 - smaller section header
            bold=True,
            style=self.theme.label
        )
        main_panel.add_child(graphics_header)
        
        # Graphics preset buttons (safe sizing to prevent overflow)
        presets = ["Low", "Medium", "High", "Ultra"]
        button_width = percent(20)     # Safe width
        button_spacing = percent(2)    # Spacing
        start_x = percent(3)           # Left padding
        
        for i, preset in enumerate(presets):
            # Calculate position: start + (width + spacing) * index
            # Total: 3% + 4×(20% + 2%) - 2% = 89% (leaves 11% right margin)
            btn_x = calc(start_x, mul(add(button_width, button_spacing), px(i)))
            btn = UIButton(
                x=btn_x,
                y=percent(13),      # More space from GRAPHICS header
                width=button_width,
                height=percent(7.4), # ~45px
                text=preset,
                on_click=lambda p=preset.lower(): self._on_preset_click(p),
                style=self.theme.button
            )
            main_panel.add_child(btn)
        
        # Shadow Quality Slider (responsive width)
        shadow_current = self.app.settings.get('graphics.shadow_map_size') if self.app else 2048
        shadow_value = {512: 0.0, 1024: 0.33, 2048: 0.66, 4096: 1.0}.get(shadow_current, 0.66)
        
        shadow_slider = UISlider(
            x=percent(3),       # Left padding
            y=percent(23),      # Increased spacing from buttons
            width=percent(91),  # Safe width, no overflow (3% + 91% + 6% = 100%)
            height=percent(5.7),  # ~35px
            min_value=0.0,
            max_value=1.0,
            current_value=shadow_value,
            on_value_change=self._on_shadow_quality_change,
            label="Shadow Quality",
            style=self.theme.slider
        )
        main_panel.add_child(shadow_slider)
        
        # MSAA Dropdown (with label, using FlexContainer)
        # MSAA (simple positioning - FlexContainer has bugs)
        msaa_current = self.app.settings.get('graphics.msaa_samples') if self.app else 4
        msaa_options = ["Off", "2x", "4x", "8x"]
        msaa_map = {0: 0, 2: 1, 4: 2, 8: 3}
        msaa_index = msaa_map.get(msaa_current, 2)
        
        # MSAA dropdown and label (vertically centered)
        msaa_y_pos = percent(32)    # Spacing from shadow slider
        msaa_height = percent(5.7)  # ~35px - dropdown height
        
        msaa_dropdown = UIDropdown(
            x=percent(18.75),   # ~120px
            y=msaa_y_pos,       # Dropdown position
            width=percent(23.44), # ~150px
            height=msaa_height,
            options=msaa_options,
            selected_index=msaa_index,
            on_select=self._on_msaa_change,
            style=self.theme.dropdown
        )
        main_panel.add_child(msaa_dropdown)
        
        # Label vertically centered with dropdown text
        # Dropdown text is centered at: dropdown.y + dropdown.height/2
        # We need to offset label to match that vertical center
        msaa_label = UILabel(
            x=percent(3),       # ~20px
            y=calc(msaa_y_pos, mul(msaa_height, px(0.3))),  # Offset to center with dropdown text
            text="MSAA:",
            size=1.0,           # Standard size for inline labels
            style=self.theme.label
        )
        main_panel.add_child(msaa_label)
        
        # Checkboxes (not using FlexContainer - using simple positioning)
        # VSync Checkbox
        vsync_current = self.app.settings.get('window.vsync') if self.app else True
        vsync_checkbox = UICheckbox(
            x=percent(3),       # ~20px
            y=percent(40),      # Spacing from MSAA
            label="VSync",
            checked=vsync_current,
            on_toggle=self._on_vsync_toggle,
            style=self.theme.checkbox
        )
        main_panel.add_child(vsync_checkbox)
        
        # Fullscreen Checkbox
        fullscreen_current = self.app.settings.get('window.fullscreen') if self.app else False
        fullscreen_checkbox = UICheckbox(
            x=percent(39),      # ~250px
            y=percent(40),      # Same Y as VSync
            label="Fullscreen",
            checked=fullscreen_current,
            on_toggle=self._on_fullscreen_toggle,
            style=self.theme.checkbox
        )
        main_panel.add_child(fullscreen_checkbox)
        
        # === AUDIO SECTION ===
        
        audio_header = UILabel(
            x=percent(3),       # ~20px
            y=percent(48),      # Spacing from checkboxes
            text="AUDIO",
            size=1.5,  # Reduced from 1.8 - smaller section header
            bold=True,
            style=self.theme.label
        )
        main_panel.add_child(audio_header)
        
        # Master Volume Slider
        master_vol_current = self.app.settings.get('audio.master_volume') if self.app else 0.8
        
        master_vol_slider = UISlider(
            x=percent(3),       # Left padding
            y=percent(58),      # Increased from 55% - more gap from AUDIO header
            width=percent(91),  # Safe width, no overflow
            height=percent(5.7),  # ~35px
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
        
        music_vol_slider = UISlider(
            x=percent(3),       # Left padding
            y=percent(67),      # Increased from 64% - consistent spacing
            width=percent(91),  # Safe width, no overflow
            height=percent(5.7),  # ~35px
            min_value=0.0,
            max_value=1.0,
            current_value=music_vol_current,
            on_value_change=self._on_music_volume_change,
            label="Music Volume",
            style=self.theme.slider
        )
        main_panel.add_child(music_vol_slider)
        
        # === ACTION BUTTONS ===
        
        # Action buttons (safe sizing, no overflow)
        action_button_width = percent(20)  # Safe width
        action_spacing = percent(3.5)      # Space between buttons
        
        # Apply Button
        apply_btn = UIButton(
            x=percent(3),       # Left padding
            y=percent(77),      # Increased from 74% - more gap from Music Volume
            width=action_button_width,
            height=percent(8.2),  # ~50px
            text="APPLY",
            on_click=self._on_apply,
            style=self.theme.button
        )
        main_panel.add_child(apply_btn)
        
        # Reset Button (start after Apply + spacing)
        # 3 + 20 + 3.5 = 26.5
        reset_btn = UIButton(
            x=percent(26.5),
            y=percent(77),      # Same Y as Apply
            width=action_button_width,
            height=percent(8.2),
            text="RESET",
            on_click=self._on_reset,
            style=self.theme.button
        )
        main_panel.add_child(reset_btn)
        
        # Back Button (start after Reset + spacing)
        # 26.5 + 20 + 3.5 = 50
        back_btn = UIButton(
            x=percent(50),
            y=percent(77),      # Same Y as Apply/Reset
            width=action_button_width,
            height=percent(8.2),
            text="BACK",
            on_click=self._on_back,
            style=self.theme.button
        )
        main_panel.add_child(back_btn)
        
        self._initialized = True
        print("[SettingsMenu] Modern UI initialized with CSS-like sizing")
    
    # === Callbacks ===
    
    def _on_preset_click(self, preset: str):
        """Handle graphics preset click."""
        print(f"[SettingsMenu] Applying {preset} preset...")
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
        print("\n[SettingsMenu] Applying settings...")
        if self.app:
            if self.app.renderer:
                self.app.renderer.apply_settings()
            
            # Force UI font reload
            if hasattr(self, '_ui_font'):
                delattr(self, '_ui_font')
            
            self.app.settings.save()
            print("[SettingsMenu] Settings applied and saved!")
    
    def _on_reset(self):
        """Handle Reset button click."""
        print("\n[SettingsMenu] Resetting to defaults...")
        if self.app and self.app.settings:
            self.app.settings.reset_to_defaults('graphics')
            self.app.settings.reset_to_defaults('audio')
            print("[SettingsMenu] Settings reset!")
    
    def _on_back(self):
        """Handle Back button click."""
        print("[SettingsMenu] Returning to game...")
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
    
    def on_resize(self, width: int, height: int):
        """
        Handle window resize events.
        Updates UI manager viewport for CSS-like sizing (vw/vh units).
        Also recalculates UI scale factor and reinitializes UI.
        
        Args:
            width: New window width
            height: New window height
        """
        if self.ui_manager:
            # Clear old UI elements before reinitializing
            self.ui_manager.clear()
            self._initialized = False
            
            # Reinitialize with new dimensions and scale factor
            self.initialize_ui(width, height)
            print(f"[SettingsMenu] UI reinitialized for {width}x{height}")
    
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
                print(f"[SettingsMenu] UI font loaded")
            
            # Save OpenGL state before UI rendering
            from OpenGL.GL import (glIsEnabled, glEnable, glDisable, GL_BLEND, 
                                  GL_DEPTH_TEST, GL_CULL_FACE, glBlendFunc, 
                                  GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            depth_was_enabled = glIsEnabled(GL_DEPTH_TEST)
            cull_was_enabled = glIsEnabled(GL_CULL_FACE)
            
            # Set up for 2D UI rendering
            glDisable(GL_DEPTH_TEST)
            glDisable(GL_CULL_FACE)  # CRITICAL: UI should never be culled
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Attach font to text_renderer for labels
            text_renderer.font = self._ui_font
            
            # COMPILE CSS-LIKE SIZES FIRST! (Critical for CSS units to work!)
            for element in self.ui_manager.elements:
                self.ui_manager._compile_element_recursive(element)
            
            # Render all UI elements in layer order
            # Collect all renderable elements (including children recursively)
            all_elements = []
            
            def collect_elements(elem):
                """Recursively collect all elements for layer-based rendering."""
                all_elements.append(elem)
                if hasattr(elem, 'children'):
                    for child in elem.children:
                        collect_elements(child)
            
            # Collect all elements from panels
            for element in self.ui_manager.elements:
                collect_elements(element)
            
            # Sort by layer (lower layers first, higher layers on top)
            sorted_elements = sorted(all_elements, key=lambda e: e.layer if hasattr(e, 'layer') else 0)
            
            # Render in layer order (each element rendered independently)
            for element in sorted_elements:
                if element.visible:
                    # Don't render if parent is invisible
                    parent = element.parent if hasattr(element, 'parent') else None
                    if parent and not parent.visible:
                        continue
                    
                    element.render(self.app.ui_renderer, text_renderer)
            
            # Clean up font
            if hasattr(text_renderer, 'font'):
                delattr(text_renderer, 'font')
            
            # Restore OpenGL state
            if depth_was_enabled:
                glEnable(GL_DEPTH_TEST)
            if cull_was_enabled:
                glEnable(GL_CULL_FACE)

