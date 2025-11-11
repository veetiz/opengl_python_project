# Quick Start Guide

Get your Vulkan triangle rendering in 3 easy steps!

## Prerequisites

1. **Python 3.8+** installed
2. **Vulkan SDK** installed from https://vulkan.lunarg.com/
3. **GPU with Vulkan support**

## Step 1: Install Dependencies

```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Install Python packages (already done if you followed setup)
pip install -r requirements.txt
```

## Step 2: Compile Shaders

```bash
python compile_shaders.py
```

This will compile `shaders/shader.vert` and `shaders/shader.frag` to SPIR-V bytecode.

**If compilation fails:**
- Make sure Vulkan SDK is installed
- Add Vulkan SDK's `Bin` directory to your PATH
- Or compile manually: 
  ```bash
  cd shaders
  glslc shader.vert -o vert.spv
  glslc shader.frag -o frag.spv
  ```

## Step 3: Run the Application

```bash
python main.py
```

## What You Should See

1. **Console output:**
   ```
   ============================================================
   Initializing Vulkan Application
   ============================================================
   [OK] Window created: 800x600
   [OK] Vulkan instance created (validation: False)
   [OK] Vulkan surface created
   [OK] Physical device selected: [Your GPU Name]
   [OK] Logical device created
   [OK] Swap chain created (X images)
   [OK] Created X image views
   [OK] Render pass created
   [OK] Graphics pipeline created
   [OK] Created X framebuffers
   [OK] Command pool created
   [OK] Allocated X command buffers
   [OK] Created synchronization objects
   [OK] Vulkan renderer initialized
   ============================================================
   Initialization complete!
   ============================================================
   
   Creating triangle mesh...
   [OK] Triangle mesh added to renderer
   
   Entering main loop...
   Controls:
     - ESC: Exit application
     - Close window: Exit application
   ```

2. **Window with a colored triangle:**
   - Top: Red
   - Bottom Right: Green
   - Bottom Left: Blue
   - Smooth color gradients between vertices
   - Black background

## Controls

- **ESC key** - Exit the application
- **X button** - Close the window and exit

## Troubleshooting

### "glslc not found"
- Install Vulkan SDK
- Add `C:\VulkanSDK\[version]\Bin` to your PATH

### "Failed to create Vulkan instance"
- Install Vulkan runtime drivers
- Update your GPU drivers

### "No suitable GPU found"
- Check if your GPU supports Vulkan
- Update GPU drivers
- Run `vulkaninfo` to verify Vulkan installation

### "File not found: shaders/vert.spv"
- Run `python compile_shaders.py` first
- Or manually compile shaders (see Step 2)

## Next Steps

Once you have the triangle rendering, try:

1. **Add more shapes:**
   ```python
   quad = Mesh.create_quad()
   app.add_mesh(quad)
   ```

2. **Create custom vertices:**
   ```python
   from src import Vertex, Mesh
   
   vertices = [
       Vertex(position=(0.0, -0.5, 0.0), color=(1.0, 1.0, 1.0)),
       Vertex(position=(0.5, 0.5, 0.0), color=(1.0, 0.0, 1.0)),
       Vertex(position=(-0.5, 0.5, 0.0), color=(0.0, 1.0, 1.0))
   ]
   my_mesh = Mesh(vertices)
   app.add_mesh(my_mesh)
   ```

3. **Enable validation layers:**
   ```python
   app = Application(
       width=800,
       height=600,
       title="My Vulkan App",
       enable_validation=True  # Enable for debugging
   )
   ```

## Performance

- **Expected FPS:** 60 (VSync limited)
- **GPU Usage:** Minimal
- **Memory:** < 10 MB
- **Startup Time:** 1-2 seconds

Enjoy your Vulkan rendering! 🎉

