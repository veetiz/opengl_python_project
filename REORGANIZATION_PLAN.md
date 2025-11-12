# Project Reorganization Plan

## File Categorization

### **core/** - Core application & window management
- app.py - Main application class
- window.py - Window management (GLFW)
- input.py - Input handling (keyboard, mouse)

### **rendering/** - Rendering pipeline
- renderer.py - OpenGL renderer
- shader.py - Shader management
- shadow_map.py - Shadow mapping

### **graphics/** - Graphics resources & data
- material.py - Material system
- texture.py - Texture loading
- mesh.py - Mesh data structure
- vertex.py - Vertex definitions
- model.py - 3D model class
- model_loader.py - Model loading (OBJ, FBX)
- light.py - Lighting (Directional, Point, Spot)

### **audio/** - Audio system
- audio_manager.py - Audio engine
- audio_clip.py - Audio clip data
- audio_source.py - Audio source component
- audio_listener.py - Audio listener
- audio2d.py - 2D audio
- audio3d.py - 3D spatial audio

### **ui/** - User interface & text
- text_renderer.py - 2D text rendering
- text2d.py - 2D text component
- text3d_renderer.py - 3D text rendering
- text3d.py - 3D text component
- font.py - Font class
- font_loader.py - Font loading

### **scene/** - Scene management & entities
- scene.py - Scene container
- splash_scene.py - Splash screen scene
- entity.py - Base entity class
- gameobject.py - GameObject & Transform
- gamescript.py - Script component
- camera.py - Camera class

### **systems/** - Engine systems
- settings_manager.py - Settings management
- settings_presets.py - Quality presets
- threading_manager.py - Multithreading
- asset_loader.py - Async asset loading

### **physics/** - Physics (future)
- (Empty for now - ready for physics system)

### **utils/** - Utility functions
- (Empty for now - ready for math, helpers, etc.)

## New Structure

```
vulkan_window_project/
├── engine/
│   └── src/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── app.py
│       │   ├── window.py
│       │   └── input.py
│       ├── rendering/
│       │   ├── __init__.py
│       │   ├── renderer.py
│       │   ├── shader.py
│       │   └── shadow_map.py
│       ├── graphics/
│       │   ├── __init__.py
│       │   ├── material.py
│       │   ├── texture.py
│       │   ├── mesh.py
│       │   ├── vertex.py
│       │   ├── model.py
│       │   ├── model_loader.py
│       │   └── light.py
│       ├── audio/
│       │   ├── __init__.py
│       │   ├── audio_manager.py
│       │   ├── audio_clip.py
│       │   ├── audio_source.py
│       │   ├── audio_listener.py
│       │   ├── audio2d.py
│       │   └── audio3d.py
│       ├── ui/
│       │   ├── __init__.py
│       │   ├── text_renderer.py
│       │   ├── text2d.py
│       │   ├── text3d_renderer.py
│       │   ├── text3d.py
│       │   ├── font.py
│       │   └── font_loader.py
│       ├── scene/
│       │   ├── __init__.py
│       │   ├── scene.py
│       │   ├── splash_scene.py
│       │   ├── entity.py
│       │   ├── gameobject.py
│       │   ├── gamescript.py
│       │   └── camera.py
│       ├── systems/
│       │   ├── __init__.py
│       │   ├── settings_manager.py
│       │   ├── settings_presets.py
│       │   ├── threading_manager.py
│       │   └── asset_loader.py
│       ├── physics/
│       │   └── __init__.py
│       └── utils/
│           └── __init__.py
├── game/
├── assets/
├── config/
├── docs/
├── examples/
├── shaders/
└── main.py
```

