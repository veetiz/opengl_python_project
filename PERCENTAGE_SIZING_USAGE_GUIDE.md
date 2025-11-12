# 🎨 CSS-LIKE PERCENTAGE SIZING - USAGE GUIDE

## 🚀 **QUICK START**

The percentage sizing system is **ready to use** right now! Here's how:

### **1. Import the Units:**
```python
from engine.src.ui import px, percent, vw, vh
```

### **2. Use Them Anywhere:**
```python
# Old way (still works):
button = UIButton(x=100, y=50, width=200, height=40)

# New way (responsive):
button = UIButton(
    x=vw(10),      # 10% of window width
    y=vh(10),      # 10% of window height
    width=vw(30),  # 30% of window width
    height=px(50)  # 50 pixels tall
)
```

### **3. That's It!**
The system **automatically compiles** sizes when rendering. No extra code needed!

---

## 📖 **UNIT TYPES**

### **`px(value)` - Pixels (Absolute)**
Fixed size in pixels. Never changes.

```python
button = UIButton(x=px(100), width=px(200))
# Always 100px from left, always 200px wide
```

### **`percent(value)` - Percentage of Parent**
Relative to the parent element's size.

```python
panel = UIPanel(width=px(600), height=px(400))
button = UIButton(width=percent(50), height=percent(25))
panel.add_child(button)
# Button: 300px wide (50% of 600), 100px tall (25% of 400)
```

### **`vw(value)` - Viewport Width**
Percentage of window width. Responsive!

```python
button = UIButton(width=vw(50))
# Window 1280px → 640px wide
# Window 1920px → 960px wide
# Automatically adapts!
```

### **`vh(value)` - Viewport Height**
Percentage of window height. Responsive!

```python
panel = UIPanel(height=vh(80))
# Window 720px → 576px tall
# Window 1080px → 864px tall
# Automatically adapts!
```

---

## 🎯 **COMMON PATTERNS**

### **Pattern 1: Full-Width Header**
```python
header = UIPanel(
    x=vw(0), y=vh(0),
    width=vw(100), height=px(60)
)
# Always spans full width, fixed 60px height
```

### **Pattern 2: Centered Modal**
```python
modal = UIPanel(
    x=vw(20), y=vh(20),
    width=vw(60), height=vh(60)
)
# Centered with 20% margins on all sides
# Adapts to any screen size!
```

### **Pattern 3: Sidebar + Content**
```python
# Sidebar (20% of screen)
sidebar = UIPanel(
    x=vw(0), y=vh(0),
    width=vw(20), height=vh(100)
)

# Content (80% of screen)
content = UIPanel(
    x=vw(20), y=vh(0),
    width=vw(80), height=vh(100)
)
```

### **Pattern 4: Responsive Button Grid**
```python
# 4 buttons, equal width (23% each, 2% gaps)
for i in range(4):
    btn = UIButton(
        x=percent(2 + i * 25),  # 2%, 27%, 52%, 77%
        width=percent(23),
        height=px(50)
    )
    panel.add_child(btn)
```

### **Pattern 5: Header + Content + Footer**
```python
# Header (fixed 60px)
header = UIPanel(x=vw(0), y=vh(0), width=vw(100), height=px(60))

# Content (fills remaining space)
content = UIPanel(x=vw(0), y=px(60), width=vw(100), height=vh(85))

# Footer (fixed 10% at bottom)
footer = UIPanel(x=vw(0), y=vh(90), width=vw(100), height=vh(10))
```

---

## 💡 **PRACTICAL EXAMPLES**

### **Example 1: Settings Menu (Responsive)**
```python
from engine.src.ui import UIPanel, UIButton, px, vw, vh, percent

# Main panel (80% of screen, centered)
settings_panel = UIPanel(
    x=vw(10), y=vh(10),
    width=vw(80), height=vh(80)
)

# Title (full width of panel)
title = UILabel(
    x=percent(5), y=px(20),
    width=percent(90), height=px(40),
    text="Settings"
)
settings_panel.add_child(title)

# Buttons (responsive grid)
for i, label in enumerate(["Low", "Medium", "High", "Ultra"]):
    btn = UIButton(
        x=percent(5 + i * 23),  # Distributed across panel
        y=px(80),
        width=percent(20),      # Each button 20% of panel width
        height=px(40)
    )
    settings_panel.add_child(btn)
```

### **Example 2: Game HUD**
```python
# Health bar (top-left, 20% of screen)
health_bar = UIPanel(
    x=vw(2), y=vh(2),
    width=vw(20), height=px(30)
)

# Minimap (bottom-right, 15% of screen)
minimap = UIPanel(
    x=vw(83), y=vh(75),
    width=vw(15), height=vh(23)
)

# Message box (bottom-center, 50% of screen)
message_box = UIPanel(
    x=vw(25), y=vh(85),
    width=vw(50), height=vh(13)
)
```

### **Example 3: Main Menu**
```python
# Background overlay (full screen)
overlay = UIPanel(
    x=vw(0), y=vh(0),
    width=vw(100), height=vh(100)
)

# Menu panel (centered, 40% of screen)
menu = UIPanel(
    x=vw(30), y=vh(25),
    width=vw(40), height=vh(50)
)

# Menu buttons (stacked, full width of menu)
button_labels = ["New Game", "Load Game", "Settings", "Quit"]
for i, label in enumerate(button_labels):
    btn = UIButton(
        x=percent(10), y=px(60 + i * 70),
        width=percent(80), height=px(50),
        text=label
    )
    menu.add_child(btn)
```

---

## 🔧 **HOW IT WORKS**

### **Behind the Scenes:**

1. **You create UI with units:**
   ```python
   button = UIButton(x=vw(10), width=percent(50))
   ```

2. **UIManager compiles sizes automatically:**
   ```python
   ui_manager.render(text_renderer)
   # ↳ Compiles: vw(10) → 128px (if window is 1280px)
   # ↳ Compiles: percent(50) → depends on parent
   # ↳ Renders with compiled sizes
   ```

3. **Window resize updates automatically:**
   ```python
   # User resizes window to 1920x1080
   ui_manager.set_window_size(1920, 1080)
   # ↳ Next render: vw(10) → 192px (updated!)
   ```

**Zero boilerplate. Just works! ✨**

---

## 📊 **SIZE CALCULATION CHEAT SHEET**

| Unit | Relative To | Example | Window 1280x720 | Window 1920x1080 |
|------|-------------|---------|-----------------|------------------|
| `px(100)` | Nothing (absolute) | 100px | 100px | 100px |
| `percent(50)` | Parent size | 50% of parent | 50% of parent | 50% of parent |
| `vw(10)` | Viewport width | 10% of width | 128px | 192px |
| `vh(10)` | Viewport height | 10% of height | 72px | 108px |
| `vw(100)` | Viewport width | Full width | 1280px | 1920px |
| `vh(100)` | Viewport height | Full height | 720px | 1080px |

---

## ⚠️ **IMPORTANT NOTES**

### **✅ Backward Compatibility:**
Old code still works! Numbers are treated as pixels:
```python
button = UIButton(x=100, width=200)  # Still works!
# Equivalent to:
button = UIButton(x=px(100), width=px(200))
```

### **✅ Properties Work:**
You can get/set sizes normally:
```python
button.x = vw(10)  # Sets size with units
print(button.x)    # Returns compiled pixels
```

### **✅ Nested Percentages:**
Percentages cascade through children:
```python
root = UIPanel(width=vw(80))     # 80% of viewport
child = UIPanel(width=percent(50))  # 50% of root
# child = 40% of viewport (80% * 50%)
```

### **✅ Window Resize:**
Sizes automatically recompile:
```python
# Resize window → UI adapts automatically!
# No code changes needed!
```

---

## 🎮 **TRY IT NOW!**

### **1. Run the Tests:**
```bash
python test_percentage_sizing.py
```
See all unit tests pass!

### **2. Run the Visual Demo:**
```bash
python demo_percentage_ui.py
```
**Resize the window** to see the UI adapt in real-time!

### **3. Update Your Settings Menu:**
```python
# In game/scenes/settings_menu.py

# OLD (fixed pixels):
main_panel = UIPanel(x=100, y=100, width=600, height=500)

# NEW (responsive):
from engine.src.ui import vw, vh
main_panel = UIPanel(
    x=vw(10), y=vh(10),
    width=vw(80), height=vh(80)
)
# Now adapts to any resolution! 🎉
```

---

## 🌟 **BENEFITS**

### **✅ Responsive Design:**
UI adapts to any screen resolution automatically!

### **✅ Less Math:**
No more calculating pixel positions manually!

### **✅ Flexible Layouts:**
Easy to create grids, sidebars, centered modals, etc.

### **✅ CSS-Like:**
Familiar to web developers!

### **✅ Zero Overhead:**
Compilation happens once per frame, no performance impact!

---

## 📚 **COMPLETE API**

### **Units:**
```python
px(value: float) → UISize
percent(value: float) → UISize
vw(value: float) → UISize
vh(value: float) → UISize
```

### **Component:**
```python
UIComponent(
    x: Union[float, UISize] = 0,
    y: Union[float, UISize] = 0,
    width: Union[float, UISize] = 100,
    height: Union[float, UISize] = 50,
    ...
)
```

### **Compiler (usually not needed directly):**
```python
compiler = UICompiler(viewport_width, viewport_height)
compiler.compile_component(component)
compiler.set_viewport(new_width, new_height)
```

---

## 🎉 **YOU'RE READY!**

Start building responsive UIs with CSS-like sizing!

**Examples:**
- ✅ Responsive settings menu
- ✅ Flexible game HUD
- ✅ Centered modals
- ✅ Full-screen overlays
- ✅ Sidebar layouts
- ✅ Button grids

**All UI components support it:**
- UIButton
- UISlider
- UICheckbox
- UIPanel
- UILabel
- UIDropdown

**Happy coding! 🎨✨**

