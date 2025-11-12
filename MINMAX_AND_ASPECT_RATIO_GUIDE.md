# ✅ MIN/MAX SIZES & ASPECT RATIO - COMPLETE!

## 🎉 **NEW FEATURES IMPLEMENTED**

### **1. Min/Max Size Constraints**
Prevent elements from becoming too small or too large when using responsive units.

### **2. Aspect Ratio**
Automatically maintain width:height proportions for media elements.

---

## 📖 **MIN/MAX SIZES**

### **Usage:**

```python
from engine.src.ui import UIButton, px, vw

# Responsive button with constraints
button = UIButton(
    width=vw(50),        # 50% of viewport width
    min_width=px(200),   # Never smaller than 200px
    max_width=px(800)    # Never larger than 800px
)
```

### **Parameters:**

- `min_width` - Minimum width (any unit: px, %, vw, vh)
- `max_width` - Maximum width (any unit: px, %, vw, vh)
- `min_height` - Minimum height (any unit: px, %, vw, vh)
- `max_height` - Maximum height (any unit: px, %, vw, vh)

### **Examples:**

#### **Example 1: Responsive Modal with Constraints**
```python
from engine.src.ui import UIPanel, vw, vh, px

# Modal: 80% of screen, but never too small or too big
modal = UIPanel(
    x=vw(10), y=vh(10),
    width=vw(80),
    height=vh(80),
    min_width=px(400),   # Readable on small screens
    max_width=px(1200),  # Not too wide on large screens
    min_height=px(300),
    max_height=px(900)
)
```

#### **Example 2: Button that Adapts but Stays Usable**
```python
# Button: 30% of viewport, but always readable
button = UIButton(
    width=vw(30),
    min_width=px(150),  # Always wide enough for text
    max_width=px(400),  # Not too wide on large screens
    height=px(50)
)
```

#### **Example 3: Sidebar with Constraints**
```python
# Sidebar: 20% of screen, constrained
sidebar = UIPanel(
    width=vw(20),
    min_width=px(200),  # Always at least 200px
    max_width=px(350),  # Never more than 350px
    height=vh(100)
)
```

#### **Example 4: Percentage Constraints (Relative to Parent)**
```python
# Parent
container = UIPanel(width=px(800), height=px(600))

# Child: flexible but constrained relative to parent
child = UIButton(
    width=percent(80),    # 80% of parent (640px)
    min_width=percent(25),  # At least 25% (200px)
    max_width=percent(100)  # At most 100% (800px)
)
container.add_child(child)
```

---

## 📖 **ASPECT RATIO**

### **Usage:**

```python
from engine.src.ui import UIPanel, vw, px

# Video player: width set, height auto-calculated
video = UIPanel(
    width=vw(80),
    aspect_ratio=16/9  # Height = width / (16/9) = width * 9/16
)
```

### **Parameter:**

- `aspect_ratio` - Width/height ratio (float)
  - `16/9` = 1.777... (widescreen)
  - `4/3` = 1.333... (classic)
  - `1.0` = square
  - `3/4` = 0.75 (portrait)

### **How It Works:**

**Width drives height** (default behavior):
```
height = width / aspect_ratio
```

Examples:
- Width 800px, ratio 16:9 → Height = 800/(16/9) = 450px
- Width 200px, ratio 1.0 → Height = 200/1.0 = 200px (square)
- Width 300px, ratio 3/4 → Height = 300/(3/4) = 400px

### **Examples:**

#### **Example 1: 16:9 Video Player**
```python
# Responsive video player
video = UIPanel(
    width=vw(80),      # 80% of viewport width
    aspect_ratio=16/9  # Standard widescreen
)

# Window 1280x720:
#   width = 1024px (80% of 1280)
#   height = 576px (1024 / (16/9))

# Window 1920x1080:
#   width = 1536px (80% of 1920)
#   height = 864px (1536 / (16/9))
```

#### **Example 2: Square Thumbnail**
```python
# Square image thumbnail
thumbnail = UIPanel(
    width=px(200),
    aspect_ratio=1.0  # Perfect square
)
# height = 200px (same as width)
```

#### **Example 3: Portrait Image**
```python
# Portrait image (3:4 ratio)
image = UIPanel(
    width=px(300),
    aspect_ratio=3/4  # Taller than wide
)
# height = 400px (300 / (3/4) = 400)
```

#### **Example 4: Card with 4:3 Ratio**
```python
# Card component with classic ratio
card = UIPanel(
    width=percent(30),  # 30% of parent
    aspect_ratio=4/3    # Classic ratio
)
```

#### **Example 5: Ultra-wide Display**
```python
# 21:9 ultra-wide banner
banner = UIPanel(
    width=vw(100),  # Full width
    aspect_ratio=21/9
)
# Very wide, relatively short
```

---

## 🎯 **COMBINING FEATURES**

### **Aspect Ratio + Min/Max Constraints:**

```python
# Video with aspect ratio and size limits
video = UIPanel(
    width=vw(80),
    aspect_ratio=16/9,
    min_width=px(640),   # At least 640px wide
    max_width=px(1920),  # At most 1920px wide
    min_height=px(360),  # At least 360px tall
    max_height=px(1080)  # At most 1080px tall
)

# Process:
# 1. Compile width (vw(80) → pixels)
# 2. Clamp width (min/max)
# 3. Calculate height (width / aspect_ratio)
# 4. Clamp height (min/max)
```

### **Responsive Image Gallery:**

```python
# Gallery with responsive, constrained images
for image in images:
    img = UIPanel(
        width=vw(30),       # 30% of viewport
        aspect_ratio=1.0,   # Square
        min_width=px(200),  # Readable
        max_width=px(400)   # Not too large
    )
    gallery.add_child(img)
```

---

## 📊 **COMMON ASPECT RATIOS**

| Name | Ratio | Decimal | Use Case |
|------|-------|---------|----------|
| Square | 1:1 | 1.0 | Avatars, thumbnails |
| Classic TV | 4:3 | 1.333 | Old displays, tablets |
| HD Video | 16:9 | 1.778 | Modern video, displays |
| Widescreen | 16:10 | 1.6 | Laptops, monitors |
| Ultra-wide | 21:9 | 2.333 | Cinema, gaming |
| Portrait | 3:4 | 0.75 | Phone photos, portraits |
| Tall Portrait | 9:16 | 0.563 | Vertical video, stories |
| Golden Ratio | φ:1 | 1.618 | Artistic, design |

---

## 🧪 **TEST RESULTS**

All tests passing! ✅

### **Min/Max Tests:**
- ✅ Min width clamping
- ✅ Max width clamping
- ✅ Min/max range
- ✅ Min/max height
- ✅ Viewport resize with constraints
- ✅ Percentage constraints

### **Aspect Ratio Tests:**
- ✅ 16:9 widescreen
- ✅ 1:1 square
- ✅ 3:4 portrait
- ✅ Responsive width with aspect
- ✅ Combined aspect + constraints

**Run tests:** `python test_minmax_and_aspect.py`

---

## 💡 **PRACTICAL EXAMPLES**

### **Responsive Card Component:**

```python
from engine.src.ui import UIPanel, UILabel, vw, px

# Card: responsive width, 4:3 aspect, constrained
card = UIPanel(
    x=vw(5), y=px(100),
    width=vw(25),       # 25% of viewport
    aspect_ratio=4/3,   # Classic card ratio
    min_width=px(250),  # Readable
    max_width=px(400)   # Not too large
)

# Card content (title, image, etc.)
title = UILabel(
    x=px(20), y=px(20),
    width=percent(90),
    height=px(40),
    text="Card Title"
)
card.add_child(title)
```

### **Video Player with Controls:**

```python
# Video container
video = UIPanel(
    x=vw(10), y=vh(10),
    width=vw(80),
    aspect_ratio=16/9,
    min_width=px(640),   # At least SD resolution
    max_width=px(1920)   # At most Full HD
)

# Control bar (full width of video, fixed height)
controls = UIPanel(
    x=px(0),
    y=percent(100),  # At bottom of video
    width=percent(100),  # Full width of parent
    height=px(50)
)
video.add_child(controls)
```

### **Image Gallery Grid:**

```python
# Gallery container
gallery = UIPanel(
    x=vw(5), y=vh(5),
    width=vw(90), height=vh(90)
)

# Add square images (3 per row)
for i in range(9):
    img = UIPanel(
        x=percent(2 + (i % 3) * 33),  # 3 columns
        y=px(10 + (i // 3) * 220),    # Rows
        width=percent(30),             # 30% of gallery
        aspect_ratio=1.0,              # Square
        min_width=px(150),
        max_width=px(300)
    )
    gallery.add_child(img)
```

---

## ✨ **BENEFITS**

### **Min/Max Sizes:**
- ✅ Responsive design that stays usable
- ✅ Prevent UI breaking on small/large screens
- ✅ Maintain readability
- ✅ Professional layouts

### **Aspect Ratio:**
- ✅ Consistent media dimensions
- ✅ No image distortion
- ✅ Automatic height calculation
- ✅ Perfect for video, images, cards

---

## 🎯 **WHEN TO USE**

### **Use Min/Max When:**
- ✅ UI must work on any screen size
- ✅ Text must stay readable
- ✅ Buttons must stay clickable
- ✅ Layouts shouldn't break on extreme sizes

### **Use Aspect Ratio When:**
- ✅ Displaying video content
- ✅ Showing images/photos
- ✅ Creating card layouts
- ✅ Maintaining visual proportions

---

## 📚 **API REFERENCE**

### **UIComponent Parameters:**

```python
UIComponent(
    x, y, width, height,           # Base sizes (any unit)
    min_width=None,                # Minimum width constraint
    max_width=None,                # Maximum width constraint
    min_height=None,               # Minimum height constraint
    max_height=None,               # Maximum height constraint
    aspect_ratio=None,             # Width/height ratio
    ...
)
```

### **Supported Units:**

All size parameters support:
- `px(value)` - Pixels
- `percent(value)` - Percentage of parent
- `vw(value)` - Percentage of viewport width
- `vh(value)` - Percentage of viewport height

---

## 🎊 **YOU'RE READY!**

Start using min/max constraints and aspect ratios now!

```python
from engine.src.ui import UIPanel, vw, vh, px

# Responsive, constrained, proportional UI!
modal = UIPanel(
    width=vw(80),
    min_width=px(400),
    max_width=px(1200),
    aspect_ratio=16/9
)
```

**Happy coding! 🚀✨**

