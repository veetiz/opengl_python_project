"""
Settings Menu Scene
Game-specific settings menu using engine UI widgets.
"""

from engine.src import Scene, SettingsManager, SettingsPresets
from engine.src.ui import (
    UIManager, UIPanel, UIButton, UILabel, UISlider, 
    UICheckbox, UIDropdown, Anchor
)


class SettingsMenuScene(Scene):
    """
    Settings menu scene with graphics, audio, and control settings.
    Uses engine UI widgets to provide interactive settings configuration.
    """
    
    def __init__(
        self,
        name: str = "Settings Menu",
        app=None,
        return_scene=None
    ):
        """
        Initialize settings menu.
        
        Args:
            name: Scene name
            app: Application instance (for settings access)
            return_scene: Scene to return to when closing menu
        """
        super().__init__(name)
        
        self.app = app
        self.return_scene = return_scene
        self.ui_manager: UIManager = None
        
        # Will be initialized when scene starts
        self._initialized = False
    
    def initialize_ui(self, window_width: int, window_height: int):
        """
        Initialize UI elements.
        Called when scene starts with window dimensions.
        
        Args:
            window_width: Window width
            window_height: Window height
        """
        if self._initialized:
            return
        
        self.ui_manager = UIManager(window_width, window_height)
        
        # Create main panel
        panel_width = 600.0
        panel_height = 500.0
        panel_x = (window_width - panel_width) / 2
        panel_y = (window_height - panel_height) / 2
        
        main_panel = UIPanel(
            x=panel_x,
            y=panel_y,
            width=panel_width,
            height=panel_height,
            bg_color=(0.1, 0.1, 0.15, 0.95),
            padding=20.0
        )
        
        # Title
        title = UILabel(
            x=0,
            y=0,
            text="SETTINGS MENU",
            size=1.5,
            bold=True,
            color=(1.0, 1.0, 0.5)
        )
        main_panel.add_child(title)
        
        # === GRAPHICS SETTINGS ===
        
        graphics_label = UILabel(
            x=0,
            y=50,
            text="GRAPHICS",
            size=1.0,
            bold=True,
            color=(0.8, 0.8, 1.0)
        )
        main_panel.add_child(graphics_label)
        
        # Quality preset dropdown
        preset_label = UILabel(
            x=0,
            y=85,
            text="Quality Preset:",
            size=0.8
        )
        main_panel.add_child(preset_label)
        
        current_preset = "high"  # Default
        preset_dropdown = UIDropdown(
            x=180,
            y=80,
            width=150,
            height=25,
            options=["low", "medium", "high", "ultra"],
            selected_index=2,  # "high"
            on_select=self._on_preset_change
        )
        main_panel.add_child(preset_dropdown)
        
        # VSync checkbox
        vsync_value = self.app.settings.get('window.vsync') if self.app else True
        vsync_checkbox = UICheckbox(
            x=0,
            y=120,
            label="VSync",
            checked=vsync_value,
            on_toggle=self._on_vsync_toggle
        )
        main_panel.add_child(vsync_checkbox)
        
        # MSAA dropdown
        msaa_label = UILabel(
            x=0,
            y=155,
            text="Anti-Aliasing (MSAA):",
            size=0.8
        )
        main_panel.add_child(msaa_label)
        
        msaa_current = self.app.settings.get('graphics.msaa_samples') if self.app else 4
        msaa_index = {0: 0, 2: 1, 4: 2, 8: 3}.get(msaa_current, 2)
        
        msaa_dropdown = UIDropdown(
            x=220,
            y=150,
            width=100,
            height=25,
            options=["Off", "2x", "4x", "8x"],
            selected_index=msaa_index,
            on_select=self._on_msaa_change
        )
        main_panel.add_child(msaa_dropdown)
        
        # Shadow quality slider
        shadow_size_label = UILabel(
            x=0,
            y=195,
            text="Shadow Quality:",
            size=0.8
        )
        main_panel.add_child(shadow_size_label)
        
        shadow_current = self.app.settings.get('graphics.shadow_map_size') if self.app else 2048
        shadow_value = {512: 0.0, 1024: 0.33, 2048: 0.66, 4096: 1.0}.get(shadow_current, 0.66)
        
        shadow_slider = UISlider(
            x=180,
            y=192,
            width=200,
            height=20,
            min_value=0.0,
            max_value=1.0,
            current_value=shadow_value,
            on_value_change=self._on_shadow_quality_change
        )
        main_panel.add_child(shadow_slider)
        
        # === AUDIO SETTINGS ===
        
        audio_label = UILabel(
            x=0,
            y=240,
            text="AUDIO",
            size=1.0,
            bold=True,
            color=(0.8, 0.8, 1.0)
        )
        main_panel.add_child(audio_label)
        
        # Master volume slider
        master_vol_label = UILabel(
            x=0,
            y=275,
            text="Master Volume:",
            size=0.8
        )
        main_panel.add_child(master_vol_label)
        
        master_vol_current = self.app.settings.get('audio.master_volume') if self.app else 0.8
        
        master_volume_slider = UISlider(
            x=180,
            y=272,
            width=200,
            height=20,
            min_value=0.0,
            max_value=1.0,
            current_value=master_vol_current,
            on_value_change=self._on_master_volume_change
        )
        main_panel.add_child(master_volume_slider)
        
        # Music volume slider
        music_vol_label = UILabel(
            x=0,
            y=310,
            text="Music Volume:",
            size=0.8
        )
        main_panel.add_child(music_vol_label)
        
        music_vol_current = self.app.settings.get('audio.music_volume') if self.app else 0.6
        
        music_volume_slider = UISlider(
            x=180,
            y=307,
            width=200,
            height=20,
            min_value=0.0,
            max_value=1.0,
            current_value=music_vol_current,
            on_value_change=self._on_music_volume_change
        )
        main_panel.add_child(music_volume_slider)
        
        # Effects volume slider
        effects_vol_label = UILabel(
            x=0,
            y=345,
            text="Effects Volume:",
            size=0.8
        )
        main_panel.add_child(effects_vol_label)
        
        effects_vol_current = self.app.settings.get('audio.effects_volume') if self.app else 0.7
        
        effects_volume_slider = UISlider(
            x=180,
            y=342,
            width=200,
            height=20,
            min_value=0.0,
            max_value=1.0,
            current_value=effects_vol_current,
            on_value_change=self._on_effects_volume_change
        )
        main_panel.add_child(effects_volume_slider)
        
        # === BUTTONS ===
        
        # Apply button
        apply_button = UIButton(
            x=50,
            y=420,
            width=120,
            height=40,
            text="APPLY",
            on_click=self._on_apply,
            bg_color=(0.2, 0.5, 0.2),
            hover_color=(0.3, 0.6, 0.3),
            text_size=0.9
        )
        main_panel.add_child(apply_button)
        
        # Reset button
        reset_button = UIButton(
            x=190,
            y=420,
            width=120,
            height=40,
            text="RESET",
            on_click=self._on_reset,
            bg_color=(0.6, 0.3, 0.2),
            hover_color=(0.7, 0.4, 0.3),
            text_size=0.9
        )
        main_panel.add_child(reset_button)
        
        # Back button
        back_button = UIButton(
            x=330,
            y=420,
            width=120,
            height=40,
            text="BACK",
            on_click=self._on_back,
            bg_color=(0.3, 0.3, 0.3),
            hover_color=(0.4, 0.4, 0.4),
            text_size=0.9
        )
        main_panel.add_child(back_button)
        
        # Add main panel to UI manager
        self.ui_manager.add_element(main_panel)
        
        self._initialized = True
        print("[SettingsMenu] UI initialized")
    
    # === Callbacks ===
    
    def _on_preset_change(self, index: int, preset: str):
        """Handle quality preset change."""
        print(f"[SettingsMenu] Quality preset changed to: {preset}")
        if self.app and self.app.settings:
            SettingsPresets.apply_graphics_preset(self.app.settings, preset)
            # Settings will be applied when user clicks Apply button
    
    def _on_vsync_toggle(self, value: bool):
        """Handle VSync toggle."""
        print(f"[SettingsMenu] VSync set to: {value}")
        if self.app and self.app.settings:
            self.app.settings.set('window.vsync', value)
    
    def _on_msaa_change(self, index: int, text: str):
        """Handle MSAA change."""
        msaa_map = {"Off": 0, "2x": 2, "4x": 4, "8x": 8}
        msaa_value = msaa_map.get(text, 4)
        print(f"[SettingsMenu] MSAA set to: {msaa_value}")
        if self.app and self.app.settings:
            self.app.settings.set('graphics.msaa_samples', msaa_value)
    
    def _on_shadow_quality_change(self, value: float):
        """Handle shadow quality change."""
        # Map 0.0-1.0 to shadow resolutions
        resolutions = {
            0.0: 512,
            0.33: 1024,
            0.66: 2048,
            1.0: 4096
        }
        
        # Find closest resolution
        shadow_size = 512
        min_diff = float('inf')
        for threshold, size in resolutions.items():
            diff = abs(value - threshold)
            if diff < min_diff:
                min_diff = diff
                shadow_size = size
        
        if self.app and self.app.settings:
            self.app.settings.set('graphics.shadow_map_size', shadow_size)
    
    def _on_master_volume_change(self, value: float):
        """Handle master volume change."""
        if self.app and self.app.settings:
            self.app.settings.set('audio.master_volume', value)
    
    def _on_music_volume_change(self, value: float):
        """Handle music volume change."""
        if self.app and self.app.settings:
            self.app.settings.set('audio.music_volume', value)
    
    def _on_effects_volume_change(self, value: float):
        """Handle effects volume change."""
        if self.app and self.app.settings:
            self.app.settings.set('audio.effects_volume', value)
    
    def _on_apply(self):
        """Handle Apply button click."""
        print("\n[SettingsMenu] Applying settings...")
        if self.app:
            # Apply to renderer
            if self.app.renderer:
                self.app.renderer.apply_settings()
            
            # Save settings
            self.app.settings.save()
            
            print("[SettingsMenu] Settings applied and saved!")
    
    def _on_reset(self):
        """Handle Reset button click."""
        print("\n[SettingsMenu] Resetting to defaults...")
        if self.app and self.app.settings:
            self.app.settings.reset_to_defaults('graphics')
            self.app.settings.reset_to_defaults('audio')
            print("[SettingsMenu] Settings reset!")
            
            # Reinitialize UI to reflect new values
            self._initialized = False
            if self.ui_manager:
                self.ui_manager.clear()
            self.initialize_ui(800, 600)  # TODO: Get actual window size
    
    def _on_back(self):
        """Handle Back button click."""
        print("[SettingsMenu] Returning to previous scene...")
        if self.app and self.return_scene:
            self.app.renderer.set_scene(self.return_scene)
    
    # === Scene Methods ===
    
    def update(self, delta_time: float):
        """Update the scene."""
        super().update(delta_time)
        
        # Update UI
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
        Render UI elements.
        Called by application after 3D rendering.
        
        Args:
            text_renderer: TextRenderer instance
        """
        if not self._initialized and self.app:
            # Initialize UI on first render (when we have window size)
            width = self.app.width if hasattr(self.app, 'width') else 800
            height = self.app.height if hasattr(self.app, 'height') else 600
            self.initialize_ui(width, height)
        
        if self.ui_manager:
            self.ui_manager.render(text_renderer)

