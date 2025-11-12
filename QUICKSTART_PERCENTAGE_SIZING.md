# 🚀 PERCENTAGE SIZING - 5 MINUTE QUICKSTART

## ✨ **YOUR UI NOW SUPPORTS CSS-LIKE SIZING!**

### **Step 1: Import** (1 line)
```python
from engine.src.ui import px, percent, vw, vh
```

### **Step 2: Use** (anywhere!)
```python
# Responsive button (adapts to window size)
button = UIButton(
    x=vw(10),      # 10% of window width
    y=vh(10),      # 10% of window height
    width=vw(30),  # 30% of window width
    height=px(50)  # 50 pixels tall
)
```

### **Step 3: Done!** ✅
**That's it!** Sizes compile automatically. No extra code needed!

---

## 📖 **THE 4 UNITS**

| Unit | What It Means | Example | Window 1280x720 |
|------|---------------|---------|-----------------|
| `px(100)` | 100 pixels | Always 100px | 100px |
| `percent(50)` | 50% of parent | Half of parent | Depends on parent |
| `vw(10)` | 10% of window width | 10% of 1280 | 128px |
| `vh(10)` | 10% of window height | 10% of 720 | 72px |

---

## 🎯 **5 COMMON PATTERNS**

### **1. Full-Width Header**
```python
header = UIPanel(
    x=vw(0), y=vh(0),
    width=vw(100), height=px(60)
)
```

### **2. Centered Modal**
```python
modal = UIPanel(
    x=vw(20), y=vh(20),
    width=vw(60), height=vh(60)
)
```

### **3. Responsive Buttons**
```python
for i, label in enumerate(["Low", "Medium", "High", "Ultra"]):
    btn = UIButton(
        x=percent(5 + i * 23),  # Distributed across parent
        width=percent(20),      # 20% of parent
        height=px(40)
    )
    panel.add_child(btn)
```

### **4. Sidebar + Content**
```python
sidebar = UIPanel(x=vw(0), width=vw(20), height=vh(100))
content = UIPanel(x=vw(20), width=vw(80), height=vh(100))
```

### **5. Game HUD**
```python
health = UIPanel(x=vw(2), y=vh(2), width=vw(20), height=px(30))
minimap = UIPanel(x=vw(83), y=vh(75), width=vw(15), height=vh(23))
```

---

## 🧪 **TRY IT NOW!**

### **Test It:**
```bash
python test_percentage_sizing.py
```

### **See It:**
```bash
python demo_percentage_ui.py
```
**Resize the window** to see responsive UI in action!

---

## 💡 **TIPS**

### **Mix Units Freely:**
```python
button = UIButton(
    x=vw(50),       # Viewport width
    y=px(100),      # Pixels
    width=percent(80),  # Percentage of parent
    height=px(50)   # Pixels
)
```

### **Nested Elements:**
```python
panel = UIPanel(width=vw(80))           # 80% of viewport
button = UIButton(width=percent(50))    # 50% of panel = 40% of viewport
panel.add_child(button)
```

### **Window Resize:**
UI automatically adapts! No extra code needed!

---

## 📚 **NEED MORE INFO?**

### **Quick Examples:**
→ `PERCENTAGE_SIZING_USAGE_GUIDE.md`

### **Complete Reference:**
→ `CSS_SIZING_FINAL_SUMMARY.md`

### **Technical Details:**
→ `PERCENTAGE_SIZING_COMPLETE.md`

---

## ✅ **YOU'RE READY!**

Start building responsive UIs now! 🎨✨

```python
from engine.src.ui import px, percent, vw, vh

# That's all you need to know!
button = UIButton(x=vw(10), width=vw(30))
```

**Happy coding! 🚀**

