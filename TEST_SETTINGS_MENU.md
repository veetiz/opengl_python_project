# 🧪 TESTING CHECKLIST - Settings Menu

## ✅ **WHAT TO TEST**

### **1. Splash Screen (3 seconds)**
- [ ] White text "OpenGL Game Engine" is **visible**
- [ ] White text "Loading..." is **visible**
- [ ] Text is centered on black background
- [ ] Automatically transitions to main scene

### **2. Main Game Scene**
- [ ] 3D wooden object is visible
- [ ] Object **stays visible** when rotating (all angles)
- [ ] Camera controls work (WASD)
- [ ] Object rotation works (Arrow keys)
- [ ] Control text visible at top: "...F1: Settings..."

### **3. Settings Menu (Press F1)**
- [ ] Press **F1** → Settings menu appears
- [ ] See three tabs: Graphics, Audio, Controls
- [ ] Graphics preset buttons visible (Low/Medium/High/Ultra)
- [ ] Sliders are interactive
- [ ] Checkboxes are clickable
- [ ] Dropdowns work

### **4. Change Settings**
- [ ] Click **"Low"** graphics preset
- [ ] Values update (shadow quality, MSAA, etc.)
- [ ] Click **"Apply"** button
- [ ] Settings save successfully (check console)

### **5. Return to Game**
- [ ] Press **F1** again → Back to game
- [ ] Or click **"Back"** button
- [ ] Settings are applied (visible changes)

### **6. Test Different Preset**
- [ ] Open settings (F1)
- [ ] Click **"Ultra"** preset
- [ ] Click **"Apply"**
- [ ] Close settings (F1)
- [ ] Visual quality changed

---

## 🎮 **CONTROLS**

### **Main Game**
- `WASD` - Move camera
- `Arrow Keys` - Rotate object
- `TAB` - Toggle mouse capture
- `C` - Switch camera
- `F1` - **Open/Close Settings Menu** ⭐
- `ESC` - Exit

### **Settings Menu**
- `Mouse` - Click UI elements
- `F1` - Close menu
- `ESC` - Exit game

---

## 🐛 **IF SOMETHING DOESN'T WORK**

### **Splash Text Not Visible**
- Check console for errors
- Verify window dimensions match splash dimensions
- Check text color vs background color

### **3D Object Disappears**
- Face culling should be **disabled**
- Check `config/game_engine_settings.json`: `"culling_enabled": false`

### **Settings Menu Not Opening**
- Press F1 key
- Check console for "Opening settings menu..." message
- Verify SettingsMenuScene was created successfully

### **Settings Not Applying**
- Click **"Apply"** button (not just "Back")
- Check console for save confirmation
- Verify `config/game_engine_settings.json` was updated

---

## ✅ **EXPECTED RESULTS**

All items should be **✅ WORKING**:
- ✅ Splash text visible
- ✅ 3D object always visible
- ✅ F1 opens settings menu
- ✅ Settings menu is interactive
- ✅ Settings apply and save
- ✅ F1 closes settings menu
- ✅ Game continues normally

---

## 🚀 **START TEST**

```bash
python main.py
```

**Happy testing!** 🎮

