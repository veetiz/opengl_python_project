# 🧮 CALC() FUNCTION - COMPLETE GUIDE

## 🎉 **NEW FEATURE: CSS-LIKE CALC()**

Perform arithmetic with different units, just like CSS `calc()`!

---

## 📖 **BASIC USAGE**

```python
from engine.src.ui import UIPanel, calc, px, vw, vh

# Full width minus padding
panel = UIPanel(width=calc(vw(100), px(-40)))
# Window 1280px → width = 1240px (1280 - 40)

# Center an element
button = UIButton(
    x=calc(vw(50), px(-100)),  # 50% - half width
    width=px(200)
)
```

---

## 🔧 **SYNTAX**

### **Main Function:**
```python
calc(left, right, operator='+')
```

**Parameters:**
- `left` - Left operand (px, %, vw, vh, number, or another calc)
- `right` - Right operand (px, %, vw, vh, number, or another calc)
- `operator` - Operation: `'+'`, `'-'`, `'*'`, `'/'` (default: `'+'`)

### **Helper Functions:**
```python
add(left, right)  # left + right
sub(left, right)  # left - right
mul(left, right)  # left * right
div(left, right)  # left / right
```

---

## 💡 **EXAMPLES**

### **Example 1: Full Width Minus Padding**
```python
# Panel: full width with 20px padding on each side
panel = UIPanel(
    width=calc(vw(100), px(-40))  # 100vw - 40px
)

# Window 1280px: width = 1240px
# Window 1920px: width = 1880px
```

### **Example 2: Center an Element**
```python
# Center a 300px button horizontally
button = UIButton(
    x=calc(vw(50), px(-150)),  # 50% - half button width
    width=px(300)
)

# Window 1280px: x = 640 - 150 = 490px (centered!)
```

### **Example 3: 50% Plus Offset**
```python
# Start at 50% and add 100px
element = UIPanel(
    x=calc(percent(50), px(100), '+')
)

# Parent 800px: x = 400 + 100 = 500px
```

### **Example 4: Multiply for Scaling**
```python
# Base size * scale factor
panel = UIPanel(
    width=calc(px(200), 1.5, '*')  # 200 * 1.5 = 300px
)
```

### **Example 5: Divide for Columns**
```python
# Split parent width into 3 columns
column = UIPanel(
    width=calc(percent(100), 3, '/')  # 100% / 3 ≈ 33.33% each
)
```

---

## 🎯 **COMMON PATTERNS**

### **Pattern 1: Responsive Padding**
```python
# Full width minus fixed padding
container = UIPanel(
    x=px(20),                      # 20px from left
    width=calc(vw(100), px(-40))   # Full width - 40px (20px each side)
)
```

### **Pattern 2: Centered Modal**
```python
# Center a 600px modal
modal = UIPanel(
    x=calc(vw(50), px(-300)),  # Center - half width
    y=calc(vh(50), px(-200)),  # Center - half height
    width=px(600),
    height=px(400)
)
```

### **Pattern 3: Sidebar + Content**
```python
# Sidebar: 250px fixed
sidebar = UIPanel(
    x=px(0),
    width=px(250),
    height=vh(100)
)

# Content: remaining space
content = UIPanel(
    x=px(250),
    width=calc(vw(100), px(-250)),  # Full width - sidebar
    height=vh(100)
)
```

### **Pattern 4: Grid with Gaps**
```python
# 3 columns with 10px gaps
for i in range(3):
    col = UIPanel(
        x=calc(
            calc(percent(i * 33.33), px(i * 10)),  # Position + gap offset
            '+' 
        ),
        width=calc(percent(33.33), px(-10))  # 33.33% - gap
    )
```

### **Pattern 5: Responsive Font Size**
```python
# Base size + viewport scaling
title = UILabel(
    font_size=calc(px(16), vw(2), '+')  # 16px + 2vw
)

# Window 1280px: font = 16 + 25.6 = 41.6px
# Window 800px: font = 16 + 16 = 32px
```

---

## 🔄 **NESTED CALC**

### **Nested Addition/Subtraction:**
```python
# ((100vw - 40px) - 20px) = full width - 60px total
panel = UIPanel(
    width=calc(
        calc(vw(100), px(-40)),  # Inner: full width - 40px
        px(-20)                   # Outer: result - 20px
    )
)

# Window 1280px: width = (1280 - 40) - 20 = 1220px
```

### **Nested Multiplication:**
```python
# (50vw + 100px) * 1.5
panel = UIPanel(
    width=calc(
        calc(vw(50), px(100), '+'),  # Inner: 50% + 100px
        1.5,                          # Outer: result * 1.5
        '*'
    )
)

# Window 1280px: width = (640 + 100) * 1.5 = 1110px
```

### **Complex Nesting:**
```python
# ((100vw - 300px) / 2) + 20px
# = (viewport - fixed) / 2 + offset
panel = UIPanel(
    width=calc(
        calc(
            calc(vw(100), px(-300)),  # Innermost: full - fixed
            2,                         # Middle: divide by 2
            '/'
        ),
        px(20),                       # Outermost: add offset
        '+'
    )
)
```

---

## 🎨 **MIXED UNITS**

### **Viewport + Pixels:**
```python
width=calc(vw(80), px(-20))  # 80% of viewport - 20px
```

### **Percentage + Pixels:**
```python
width=calc(percent(50), px(100), '+')  # 50% of parent + 100px
```

### **Viewport + Percentage:**
```python
# Note: Both relative units
width=calc(vw(50), percent(20), '+')
# vw is relative to viewport
# % is relative to parent
```

---

## 📊 **OPERATOR PRECEDENCE**

**calc() evaluates left-to-right, no precedence!**

Use nested calc() for complex expressions:

```python
# WRONG (if you want precedence):
calc(vw(100), px(-40), calc(px(10), 2, '*'))  # ❌ Won't work

# RIGHT (use nesting):
calc(vw(100), calc(px(10), 2, '*'), '-')  # ✅ 100vw - (10px * 2)
```

**Breakdown:**
1. Inner calc: `px(10) * 2 = 20px`
2. Outer calc: `100vw - 20px`

---

## ⚠️ **EDGE CASES**

### **Division by Zero:**
```python
width=calc(px(100), 0, '/')
# → Returns 0px with warning
# [UICompiler] Warning: Division by zero in calc(), returning 0
```

### **Negative Results:**
```python
width=calc(px(50), px(100), '-')
# → Returns -50px (may cause layout issues!)
```

### **Very Large Numbers:**
```python
width=calc(vw(100), 1000, '*')
# → May return extremely large values
```

---

## 🧪 **TEST RESULTS**

All 13 tests passing! ✅

- ✅ Basic addition
- ✅ Basic subtraction
- ✅ Mixed units (vw + px, % + px)
- ✅ Percentage with parent
- ✅ Multiplication
- ✅ Division
- ✅ Helper functions (add, sub, mul, div)
- ✅ Nested calc
- ✅ Complex nested calc
- ✅ Element centering
- ✅ Full width minus padding
- ✅ Viewport resize with calc
- ✅ Division by zero handling

**Run tests:** `python test_calc_function.py`

---

## 🚀 **PRACTICAL EXAMPLES**

### **Responsive Card Grid:**
```python
from engine.src.ui import UIPanel, calc, vw, px, percent

# Container with padding
container = UIPanel(
    x=px(20),
    width=calc(vw(100), px(-40)),  # Full width - 40px padding
    height=vh(100)
)

# 3 cards with gaps
gap = 20  # px between cards
for i in range(3):
    card = UIPanel(
        x=calc(
            percent(i * 33.33),  # Position
            px(i * gap),         # Add gap offset
            '+'
        ),
        width=calc(
            percent(33.33),   # Base width
            px(-gap),         # Minus gap
            '-'
        ),
        height=px(300)
    )
    container.add_child(card)

# Result: 3 evenly-spaced cards with 20px gaps
```

### **Sticky Header + Scrollable Content:**
```python
# Header: fixed at top
header = UIPanel(
    x=px(0), y=px(0),
    width=vw(100),
    height=px(60)
)

# Content: fills remaining space
content = UIPanel(
    x=px(0),
    y=px(60),
    width=vw(100),
    height=calc(vh(100), px(-60))  # Full height - header
)
```

### **Dynamic Button Bar:**
```python
# Button bar: 5 buttons, equal width
button_count = 5
gap = 10

for i in range(button_count):
    btn = UIButton(
        x=calc(
            calc(percent(i * 20), px(i * gap), '+'),  # Position with gap
            '+',
        ),
        width=calc(percent(20), px(-gap))  # 20% minus gap
    )
```

---

## 💡 **TIPS & TRICKS**

### **1. Centering Elements:**
```python
# Horizontal center: 50% - half width
x=calc(vw(50), px(-element_width / 2))

# Vertical center: 50% - half height
y=calc(vh(50), px(-element_height / 2))
```

### **2. Responsive Padding:**
```python
# Fluid padding that scales with viewport
padding_x = calc(vw(5), px(10), '+')  # 5vw + 10px min
```

### **3. Golden Ratio Layouts:**
```python
# Primary: 61.8%
primary = UIPanel(width=percent(61.8))

# Secondary: 38.2% (minus gap)
secondary = UIPanel(width=calc(percent(38.2), px(-10)))
```

### **4. Responsive Scaling:**
```python
# Base size with viewport scaling
size = calc(px(base_size), vw(scale_factor), '+')
```

---

## 🎓 **WHEN TO USE CALC**

### **✅ Use Calc When:**
- Mixing fixed and responsive units
- Centering elements precisely
- Creating grids with gaps
- Subtracting padding from full width
- Scaling with offsets

### **❌ Don't Need Calc When:**
- Simple px values (`px(100)` not `calc(px(100))`)
- Simple percentages (`percent(50)` not `calc(percent(50))`)
- Simple viewport units (`vw(100)` not `calc(vw(100))`)

---

## 📚 **API REFERENCE**

### **Functions:**

```python
# Main function
calc(left, right, operator='+') → UICalc

# Helpers
add(left, right) → UICalc  # left + right
sub(left, right) → UICalc  # left - right
mul(left, right) → UICalc  # left * right
div(left, right) → UICalc  # left / right
```

### **Supported Operands:**

- `px(value)` - Pixels
- `percent(value)` - Percentage
- `vw(value)` - Viewport width
- `vh(value)` - Viewport height
- `float/int` - Direct numbers
- `UICalc` - Nested calculations

### **Supported Operators:**

- `'+'` - Addition
- `'-'` - Subtraction
- `'*'` - Multiplication
- `'/'` - Division

---

## 🎊 **YOU'RE READY!**

Start using calc() for powerful, flexible layouts!

```python
from engine.src.ui import calc, px, vw, vh, percent

# Full width minus padding
panel = UIPanel(width=calc(vw(100), px(-40)))

# Centered element
button = UIButton(x=calc(vw(50), px(-150)))

# Responsive with offset
element = UIPanel(width=calc(percent(80), px(20), '+'))
```

**Happy calculating! 🧮✨**

