# 🎨 CSS-LIKE PERCENTAGE SIZING SYSTEM

## 🎯 **WHAT'S BEING IMPLEMENTED**

A complete CSS-like sizing system with:
- ✅ **Pixels (px)** - Absolute values
- ✅ **Percentage (%)** - Relative to parent
- ✅ **Viewport Width (vw)** - Relative to window width
- ✅ **Viewport Height (vh)** - Relative to window height
- ✅ **UIComponent** - Base class with size compilation
- ✅ **UICompiler** - External size calculator

---

## 🏗️ **NEW ARCHITECTURE**

### **Class Hierarchy:**
```
UIComponent (new base class)
  ├─ Common properties (x, y, width, height)
  ├─ Size units (px, %, vw, vh)
  ├─ Compiled sizes (absolute pixels)
  └─ Uses UICompiler for calculations

UIButton extends UIComponent
UISlider extends UIComponent
UICheckbox extends UIComponent
... (all components)
```

### **Size Compilation:**
```
UICompiler (external class)
  ├─ Takes viewport size (window dimensions)
  ├─ Compiles % → pixels (relative to parent)
  ├─ Compiles vw → pixels (relative to viewport width)
  ├─ Compiles vh → pixels (relative to viewport height)
  └─ Recursively compiles children
```

---

## 📝 **USAGE EXAMPLES**

### **Example 1: Absolute Pixels (Current Behavior)**
```python
button = UIButton(
    x=100,      # 100px from left
    y=50,       # 50px from top
    width=200,  # 200px wide
    height=40   # 40px tall
)
```

### **Example 2: Percentage of Parent**
```python
panel = UIPanel(
    x=px(100), y=px(100),
    width=px(600), height=px(400)
)

# Button takes 80% of panel width
button = UIButton(
    x=percent(10),   # 10% from left = 60px (10% of 600)
    y=percent(10),   # 10% from top = 40px (10% of 400)
    width=percent(80),  # 80% of parent = 480px (80% of 600)
    height=px(40)    # 40px tall (absolute)
)
panel.add_child(button)
```

### **Example 3: Viewport Units**
```python
# Full-screen modal (80% of viewport)
modal = UIPanel(
    x=vw(10),   # 10% of window width from left
    y=vh(10),   # 10% of window height from top
    width=vw(80),  # 80% of window width
    height=vh(80)  # 80% of window height
)
# Window 1280x720:
#   x = 128px (10% of 1280)
#   y = 72px (10% of 720)
#   width = 1024px (80% of 1280)
#   height = 576px (80% of 720)
```

### **Example 4: Mixed Units**
```python
# Centered button with responsive width
button = UIButton(
    x=vw(50),      # Center horizontally (50% of viewport)
    y=px(100),     # 100px from top (absolute)
    width=vw(30),  # 30% of viewport width (responsive!)
    height=px(50)  # 50px tall (absolute)
)
```

### **Example 5: Responsive Layout**
```python
# Header (full width, fixed height)
header = UIPanel(
    x=vw(0), y=vh(0),
    width=vw(100), height=px(60)
)

# Content (full width, flexible height)
content = UIPanel(
    x=vw(0), y=px(60),
    width=vw(100), height=vh(80)  # 80% of viewport height
)

# Footer (full width, fixed height)
footer = UIPanel(
    x=vw(0), y=vh(90),
    width=vw(100), height=vh(10)
)
```

---

## 🔧 **TECHNICAL IMPLEMENTATION**

### **Step 1: Create UIComponent Base Class**
All UI components will inherit from `UIComponent` instead of `UIElement`.

### **Step 2: Size Storage**
```python
class UIComponent:
    # Original sizes (with units)
    x_size: UISize
    y_size: UISize
    width_size: UISize
    height_size: UISize
    
    # Compiled sizes (absolute pixels)
    compiled_x: float
    compiled_y: float
    compiled_width: float
    compiled_height: float
```

### **Step 3: UICompiler Compiles Sizes**
```python
compiler = UICompiler(viewport_width=1280, viewport_height=720)

# Compile component
compiler.compile_component(button)
# → button.compiled_x, compiled_y, compiled_width, compiled_height are set

# Recursively compiles children
compiler.compile_component(panel)  # Compiles panel + all children
```

### **Step 4: Components Use Compiled Sizes**
```python
def render(self, ui_renderer, text_renderer):
    # Use compiled sizes for rendering
    x, y = self.get_absolute_position()  # Uses compiled_x, compiled_y
    w, h = self.compiled_width, self.compiled_height
    
    ui_renderer.draw_rect(x, y, w, h, color)
```

---

## 📊 **SIZE CALCULATION FLOW**

```
1. Create component with units:
   button = UIButton(x=vw(10), width=percent(50), ...)

2. Component stores sizes:
   button.x_size = UISize(10, "vw")
   button.width_size = UISize(50, "%")

3. Compile before rendering:
   compiler = UICompiler(viewport_width=1280, viewport_height=720)
   compiler.compile_component(panel)  # Compiles panel + children

4. UICompiler calculates:
   button.compiled_x = (10 / 100) * 1280 = 128px
   button.compiled_width = (50 / 100) * parent_width

5. Rendering uses compiled sizes:
   ui_renderer.draw_rect(button.compiled_x, ..., button.compiled_width, ...)
```

---

## ✅ **BENEFITS**

### **Responsive Design:**
- ✅ UI scales with window size
- ✅ Percentages adapt to parent size
- ✅ Viewport units adapt to screen resolution

### **Flexible Layouts:**
- ✅ Center elements easily (x=vw(50))
- ✅ Full-width panels (width=vw(100))
- ✅ Flexible grids (width=percent(33))

### **CSS-Like:**
- ✅ Familiar to web developers
- ✅ Intuitive sizing
- ✅ Professional workflow

---

## 🎮 **EXAMPLE: RESPONSIVE SETTINGS MENU**

```python
from engine.src.ui import UIPanel, UIButton, vw, vh, percent

# Modal panel (80% of viewport, centered)
settings_panel = UIPanel(
    x=vw(10),      # 10% from left
    y=vh(10),      # 10% from top
    width=vw(80),  # 80% of viewport width
    height=vh(80)  # 80% of viewport height
)

# Buttons (responsive to panel width)
for i, label in enumerate(["Low", "Medium", "High", "Ultra"]):
    btn = UIButton(
        x=percent(i * 25),  # 0%, 25%, 50%, 75% of panel width
        y=px(80),
        width=percent(23),  # 23% of panel width (with 2% gap)
        height=px(35)
    )
    settings_panel.add_child(btn)

# Result: Buttons automatically resize when window resizes!
```

---

## 🚀 **IMPLEMENTATION STATUS**

Created files:
- ✅ `engine/src/ui/ui_units.py` - Unit types and helper functions
- ✅ `engine/src/ui/ui_compiler.py` - Size compilation logic
- ✅ `engine/src/ui/ui_component.py` - New base class

Next steps:
1. Update all UI components to extend UIComponent
2. Integrate UICompiler into rendering flow
3. Add compilation step before rendering
4. Test with responsive layouts

---

## 🎉 **COMING SOON!**

**Your UI will support:**
```python
# Full-width header
header = UIPanel(width=vw(100), height=px(60))

# Centered modal (50% of screen)
modal = UIPanel(x=vw(25), y=vh(25), width=vw(50), height=vh(50))

# Responsive grid
for i in range(3):
    col = UIPanel(x=percent(i*33), width=percent(33))  # 3 columns
```

**CSS-like responsive UI in your game engine!** 🎨✨

