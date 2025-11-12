# 🎨 Modern UI System - Complete Guide

## 📖 **OVERVIEW**

The Modern UI System provides **OpenGL-based UI components** with **customizable styling** for creating professional, game-specific user interfaces.

### **Key Features:**
- ✅ **OpenGL Rendering** - GPU-accelerated, smooth graphics
- ✅ **No ASCII Characters** - Real shapes (rectangles, circles)
- ✅ **Theme System** - Consistent styling across all components
- ✅ **Fully Customizable** - Extend themes for your game's unique look
- ✅ **Easy Integration** - Drop-in replacement for text-based UI

---

## 🏗️ **ARCHITECTURE**

### **Three-Layer Design:**

```
┌─────────────────────────────────────┐
│  Game Layer (Customization)         │
│  - Custom themes                    │
│  - Styled components                │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  Component Layer (UI Elements)      │
│  - ModernButton, ModernSlider, etc. │
│  - Event handling                   │
│  - State management                 │
└─────────────────────────────────────┘
            ↓
┌─────────────────────────────────────┐
│  Rendering Layer (OpenGL)           │
│  - ModernUIRenderer                 │
│  - Shaders, buffers                 │
│  - Primitive drawing                │
└─────────────────────────────────────┘
```

---

## 🎨 **USING MODERN COMPONENTS**

### **1. Basic Usage (Default Theme)**

```python
from engine.src.ui import (
    ModernButton, ModernSlider, ModernCheckbox,
    ModernPanel, DefaultTheme
)

# Create with default theme
theme = DefaultTheme()

button = ModernButton(
    x=100, y=100,
    width=150, height=40,
    text="Click Me",
    on_click=my_handler,
    style=theme.button
)

slider = ModernSlider(
    x=100, y=150,
    width=300, height=30,
    min_value=0.0,
    max_value=1.0,
    current_value=0.5,
    on_value_change=my_slider_handler,
    label="Volume",
    style=theme.slider
)

checkbox = ModernCheckbox(
    x=100, y=200,
    label="Enable Feature",
    checked=True,
    on_toggle=my_toggle_handler,
    style=theme.checkbox
)
```

### **2. Custom Theme**

```python
from engine.src.ui import UITheme, Color

class MyGameTheme(UITheme):
    """Custom theme for your game."""
    
    def __init__(self):
        super().__init__()
        
        # Buttons - Gold and Black
        self.button.bg_color = Color(0.8, 0.6, 0.0, 1.0)
        self.button.hover_color = Color(1.0, 0.8, 0.2, 1.0)
        self.button.text_color = Color(0.0, 0.0, 0.0, 1.0)
        self.button.border_radius = 10.0
        
        # Sliders - Blue Fill
        self.slider.track_color = Color(0.1, 0.1, 0.15, 1.0)
        self.slider.fill_color = Color(0.2, 0.4, 1.0, 1.0)
        self.slider.handle_color = Color(1.0, 1.0, 1.0, 1.0)
        self.slider.handle_radius = 15.0
        
        # Checkboxes - Green Check
        self.checkbox.check_color = Color(0.0, 1.0, 0.3, 1.0)
        
        # Panels - Semi-transparent dark
        self.panel.bg_color = Color(0.0, 0.0, 0.0, 0.85)

# Use in your scene
menu = MyMenuScene(theme=MyGameTheme())
```

### **3. Per-Component Styling**

```python
from engine.src.ui import ModernButton, ButtonStyle, Color

# Create custom style for one button
danger_style = ButtonStyle()
danger_style.bg_color = Color(0.9, 0.1, 0.1, 1.0)  # Red
danger_style.hover_color = Color(1.0, 0.3, 0.3, 1.0)
danger_style.text_color = Color(1.0, 1.0, 1.0, 1.0)  # White text

delete_button = ModernButton(
    x=300, y=400,
    width=150, height=45,
    text="DELETE",
    on_click=delete_handler,
    style=danger_style  # Custom style just for this button
)
```

---

## 📊 **COMPONENT REFERENCE**

### **ModernButton**

**Constructor:**
```python
ModernButton(
    x, y,           # Position
    width, height,  # Size
    text="Button",  # Button text
    on_click=None,  # Click callback
    style=None      # ButtonStyle (optional)
)
```

**Styling:**
```python
style.bg_color          # Background color
style.hover_color       # Hover state color
style.press_color       # Pressed state color
style.text_color        # Text color
style.border_color      # Border color
style.border_width      # Border thickness
style.border_radius     # Corner rounding (future)
style.padding           # Internal padding
style.text_size         # Text scale
```

**Example:**
```python
button = ModernButton(
    x=100, y=100,
    width=200, height=50,
    text="START GAME",
    on_click=start_game
)
```

---

### **ModernSlider**

**Constructor:**
```python
ModernSlider(
    x, y,                    # Position
    width, height=30,        # Size
    min_value=0.0,           # Minimum value
    max_value=1.0,           # Maximum value
    current_value=0.5,       # Starting value
    on_value_change=None,    # Value change callback
    label="",                # Optional label
    style=None               # SliderStyle (optional)
)
```

**Styling:**
```python
style.track_color          # Track background color
style.track_border_color   # Track border color
style.fill_color           # Fill color (shows value)
style.fill_hover_color     # Fill color when hovered
style.handle_color         # Handle color
style.handle_hover_color   # Handle hover color
style.handle_press_color   # Handle pressed color
style.track_height         # Track height
style.handle_radius        # Handle size
style.border_width         # Border thickness
```

**Example:**
```python
slider = ModernSlider(
    x=100, y=150,
    width=400, height=30,
    min_value=0.0,
    max_value=100.0,
    current_value=75.0,
    on_value_change=lambda v: print(f"Volume: {v}"),
    label="Master Volume"
)
```

---

### **ModernCheckbox**

**Constructor:**
```python
ModernCheckbox(
    x, y,                # Position
    label="",            # Label text
    checked=False,       # Initial state
    on_toggle=None,      # Toggle callback
    style=None           # CheckboxStyle (optional)
)
```

**Styling:**
```python
style.box_color          # Box background color
style.box_hover_color    # Box hover color
style.box_border_color   # Box border color
style.check_color        # Checkmark color
style.check_hover_color  # Checkmark hover color
style.text_color         # Label text color
style.box_size           # Box size
style.border_width       # Border thickness
style.border_radius      # Corner rounding (future)
style.check_padding      # Checkmark padding
style.text_size          # Text scale
```

**Example:**
```python
checkbox = ModernCheckbox(
    x=100, y=200,
    label="Enable Shadows",
    checked=True,
    on_toggle=lambda checked: print(f"Shadows: {checked}")
)
```

---

### **ModernPanel**

**Constructor:**
```python
ModernPanel(
    x, y,           # Position
    width, height,  # Size
    style=None      # PanelStyle (optional)
)
```

**Styling:**
```python
style.bg_color       # Background color (RGBA)
style.border_color   # Border color
style.border_width   # Border thickness
style.border_radius  # Corner rounding (future)
style.padding        # Internal padding
```

**Example:**
```python
panel = ModernPanel(
    x=100, y=100,
    width=500, height=400
)

# Add children
button = ModernButton(x=20, y=20, width=150, height=40, text="Child")
panel.add_child(button)
```

---

## 🎨 **BUILT-IN THEMES**

### **DefaultTheme (Modern & Clean)**
```python
from engine.src.ui import DefaultTheme

theme = DefaultTheme()
# Dark gray buttons with blue accents
# Blue fill on sliders
# Clean, professional appearance
```

### **DarkTheme (Dark Mode)**
```python
from engine.src.ui import DarkTheme

theme = DarkTheme()
# Very dark backgrounds
# Subtle colors
# High contrast
```

### **LightTheme (Light Mode)**
```python
from engine.src.ui import LightTheme

theme = LightTheme()
# Light gray backgrounds
# Dark text
# Bright appearance
```

### **GameCustomTheme (Example)**
```python
from engine.src.ui import GameCustomTheme

theme = GameCustomTheme()
# Blue and gold theme
# Example of custom colors
# Use as reference for your own
```

---

## 🎯 **CUSTOMIZATION GUIDE**

### **Level 1: Use Built-in Themes**
```python
# Easiest - just pick a theme
from engine.src.ui import DarkTheme

menu = SettingsMenu(theme=DarkTheme())
```

### **Level 2: Tweak Existing Theme**
```python
from engine.src.ui import DefaultTheme, Color

theme = DefaultTheme()
# Modify specific colors
theme.button.bg_color = Color(0.5, 0.0, 0.5, 1.0)  # Purple
theme.slider.fill_color = Color(1.0, 0.5, 0.0, 1.0)  # Orange

menu = SettingsMenu(theme=theme)
```

### **Level 3: Create Custom Theme**
```python
from engine.src.ui import UITheme, Color

class RPGTheme(UITheme):
    def __init__(self):
        super().__init__()
        
        # Medieval/Fantasy colors
        self.button.bg_color = Color(0.4, 0.2, 0.0, 1.0)  # Brown
        self.button.hover_color = Color(0.5, 0.3, 0.1, 1.0)
        self.slider.fill_color = Color(0.8, 0.6, 0.0, 1.0)  # Gold
        
menu = SettingsMenu(theme=RPGTheme())
```

### **Level 4: Override Individual Components**
```python
from engine.src.ui import ModernButton, ButtonStyle, Color

# Create unique style for special button
boss_button_style = ButtonStyle()
boss_button_style.bg_color = Color(1.0, 0.0, 0.0, 1.0)
boss_button_style.hover_color = Color(1.0, 0.3, 0.0, 1.0)
boss_button_style.text_color = Color(1.0, 1.0, 0.0, 1.0)  # Yellow text

boss_fight_button = ModernButton(
    x=300, y=500,
    width=250, height=60,
    text="FIGHT BOSS!",
    on_click=start_boss_fight,
    style=boss_button_style  # Unique style
)
```

---

## 🛠️ **RENDERING INTEGRATION**

### **In Your Scene:**
```python
def render_ui(self, text_renderer):
    """Render UI using modern components."""
    if not self._initialized:
        self.initialize_ui(app.width, app.height)
    
    # Get UI renderer from app
    ui_renderer = self.app.ui_renderer
    
    # Load font for labels/text
    if not hasattr(self, '_font'):
        self._font = FontLoader.load("arial.ttf", 24)
    
    text_renderer.font = self._font
    
    # Render all UI elements
    for element in self.ui_manager.elements:
        if element.visible:
            # Pass BOTH renderers:
            # - ui_renderer for shapes (rectangles, circles)
            # - text_renderer for text (labels, values)
            element.render(ui_renderer, text_renderer)
    
    # Clean up
    delattr(text_renderer, 'font')
```

---

## 📚 **EXAMPLES**

### **Example 1: Simple Menu**
```python
from engine.src import Scene
from engine.src.ui import (
    UIManager, ModernPanel, ModernButton,
    ModernLabel, DefaultTheme
)

class SimpleMenu(Scene):
    def __init__(self, app):
        super().__init__("Menu")
        self.app = app
        self.theme = DefaultTheme()
        self.ui_manager = UIManager(800, 600)
        
        # Panel
        panel = ModernPanel(
            x=250, y=200,
            width=300, height=200,
            style=self.theme.panel
        )
        self.ui_manager.add_element(panel)
        
        # Title
        title = ModernLabel(
            x=80, y=20,
            text="MAIN MENU",
            size=1.5,
            style=self.theme.label
        )
        panel.add_child(title)
        
        # Buttons
        start_btn = ModernButton(
            x=75, y=80,
            width=150, height=40,
            text="START",
            on_click=self.start_game,
            style=self.theme.button
        )
        panel.add_child(start_btn)
        
        quit_btn = ModernButton(
            x=75, y=130,
            width=150, height=40,
            text="QUIT",
            on_click=self.quit_game,
            style=self.theme.button
        )
        panel.add_child(quit_btn)
    
    def start_game(self):
        print("Starting game...")
    
    def quit_game(self):
        print("Quitting...")
    
    def render_ui(self, text_renderer):
        if self.ui_manager and self.app.ui_renderer:
            # Load font
            if not hasattr(self, '_font'):
                from engine.src import FontLoader
                self._font = FontLoader.load("arial.ttf", 24)
            
            text_renderer.font = self._font
            
            # Render UI
            for elem in self.ui_manager.elements:
                elem.render(self.app.ui_renderer, text_renderer)
```

### **Example 2: Custom Themed UI**
```python
from engine.src.ui import UITheme, Color

class SciFiTheme(UITheme):
    """Sci-fi themed UI (cyan/blue)."""
    
    def __init__(self):
        super().__init__()
        
        # Futuristic cyan buttons
        self.button.bg_color = Color(0.0, 0.3, 0.4, 1.0)
        self.button.hover_color = Color(0.0, 0.5, 0.6, 1.0)
        self.button.text_color = Color(0.5, 1.0, 1.0, 1.0)
        
        # Glowing cyan sliders
        self.slider.track_color = Color(0.0, 0.1, 0.15, 1.0)
        self.slider.fill_color = Color(0.0, 0.8, 1.0, 1.0)
        self.slider.handle_color = Color(0.5, 1.0, 1.0, 1.0)
        
        # Dark background panels
        self.panel.bg_color = Color(0.0, 0.05, 0.1, 0.95)
        self.panel.border_color = Color(0.0, 0.6, 0.8, 1.0)

# Use theme
menu = MySettingsMenu(theme=SciFiTheme())
```

---

## 🔧 **API REFERENCE**

### **ModernUIRenderer**

#### **Methods:**
```python
draw_rect(x, y, width, height, color)
# Draw filled rectangle
# color: (r, g, b, a) tuple (0.0-1.0)

draw_circle(x, y, radius, color, segments=32)
# Draw filled circle
# x, y: Center position
# segments: Higher = smoother

draw_border_rect(x, y, width, height, border_width, color)
# Draw rectangle border (4 thin rectangles)

set_projection(width, height)
# Update projection matrix for screen size

cleanup()
# Release OpenGL resources
```

---

### **Color Class**

```python
# Create color
color = Color(r, g, b, a)  # 0.0 - 1.0 for each

# Predefined colors
from engine.src.ui import Colors

Colors.WHITE
Colors.BLACK
Colors.GRAY, DARK_GRAY, LIGHT_GRAY
Colors.RED, GREEN, BLUE, YELLOW
Colors.PRIMARY, SECONDARY
Colors.SUCCESS, WARNING, DANGER

# Convert
color.to_tuple()  # (r, g, b, a)
color.to_rgb()    # (r, g, b)
```

---

## 🎯 **MIGRATION GUIDE**

### **From Old Text-Based UI:**

**Old:**
```python
from engine.src.ui import UIButton, UISlider

button = UIButton(...)  # ASCII-based
slider = UISlider(...)  # ASCII-based
```

**New:**
```python
from engine.src.ui import ModernButton, ModernSlider

button = ModernButton(...)  # OpenGL-based
slider = ModernSlider(...)  # OpenGL-based
```

**Changes Needed:**
1. Import modern components instead of old ones
2. Pass `ui_renderer` to `render()` method
3. Optionally add `style` parameter for customization

---

## 🎨 **THEME EXAMPLES**

### **Fantasy/RPG Theme:**
```python
class FantasyTheme(UITheme):
    def __init__(self):
        super().__init__()
        self.button.bg_color = Color(0.4, 0.2, 0.0, 1.0)  # Brown wood
        self.slider.fill_color = Color(0.8, 0.6, 0.0, 1.0)  # Gold
        self.panel.bg_color = Color(0.15, 0.1, 0.05, 0.9)  # Dark wood
```

### **Neon/Cyberpunk Theme:**
```python
class CyberpunkTheme(UITheme):
    def __init__(self):
        super().__init__()
        self.button.bg_color = Color(0.8, 0.0, 0.8, 1.0)  # Magenta
        self.slider.fill_color = Color(0.0, 1.0, 1.0, 1.0)  # Cyan
        self.panel.bg_color = Color(0.05, 0.0, 0.1, 0.95)  # Purple-black
```

### **Military/Tactical Theme:**
```python
class TacticalTheme(UITheme):
    def __init__(self):
        super().__init__()
        self.button.bg_color = Color(0.2, 0.3, 0.2, 1.0)  # Olive
        self.slider.fill_color = Color(0.4, 0.6, 0.2, 1.0)  # Green
        self.panel.bg_color = Color(0.1, 0.15, 0.1, 0.95)  # Dark green
```

---

## ✅ **ADVANTAGES**

### **Compared to Text-Based UI:**

| Feature | Text-Based | Modern OpenGL |
|---------|-----------|---------------|
| Visual Quality | ⭐⭐ ASCII chars | ⭐⭐⭐⭐⭐ Smooth shapes |
| Customization | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Full control |
| Performance | ⭐⭐⭐ Text rendering | ⭐⭐⭐⭐ GPU primitives |
| Font Dependency | ⭐ Needs glyphs | ⭐⭐⭐⭐⭐ Shapes independent |
| Scalability | ⭐⭐ Limited | ⭐⭐⭐⭐⭐ Any resolution |
| Styling | ⭐ Color only | ⭐⭐⭐⭐⭐ Full theming |

---

## 🎉 **CONCLUSION**

**You now have:**
- ✅ Professional OpenGL-based UI
- ✅ Fully customizable styling
- ✅ Theme system for consistency
- ✅ Easy game-specific customization
- ✅ Smooth, modern appearance
- ✅ No ASCII character limitations

**Create beautiful, unique UIs for your games!** 🚀✨🎮

