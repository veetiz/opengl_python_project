# Vulkan Window Project (Python)

A basic Vulkan window application built with Python, using GLFW for window management and the Vulkan API.

## Prerequisites

- Python 3.8 or higher
- Vulkan SDK installed on your system
  - Download from: https://vulkan.lunarg.com/
- GPU with Vulkan support

## Installation

1. **Install Vulkan SDK**
   - Download and install the Vulkan SDK for your platform
   - Make sure the SDK is properly configured in your system PATH

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
vulkan_window_project/
├── src/
│   ├── __init__.py      # Package initialization
│   ├── app.py           # Application class (boot/main loop)
│   ├── window.py        # Window management (GLFW)
│   ├── renderer.py      # Vulkan renderer with full pipeline
│   ├── vertex.py        # Vertex data structure
│   ├── mesh.py          # Mesh class for geometry
│   └── shader.py        # Shader module loader
├── shaders/
│   ├── shader.vert      # Vertex shader (GLSL)
│   ├── shader.frag      # Fragment shader (GLSL)
│   ├── vert.spv         # Compiled vertex shader (generated)
│   ├── frag.spv         # Compiled fragment shader (generated)
│   └── README.md        # Shader compilation instructions
├── main.py              # Entry point - renders a triangle!
├── compile_shaders.py   # Shader compilation script
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Architecture

The project follows a modular architecture with clear separation of concerns:

- **`main.py`** - Entry point that creates the application and a triangle mesh
- **`src/app.py`** - `Application` class that coordinates window and renderer, handles main loop
- **`src/window.py`** - `Window` class for GLFW window management and events
- **`src/renderer.py`** - `VulkanRenderer` class with complete rendering pipeline
  - Swap chain management
  - Render pass and framebuffers
  - Graphics pipeline with shaders
  - Command buffer recording
  - Vertex buffer management
  - Frame rendering with synchronization
- **`src/vertex.py`** - `Vertex` class with position and color attributes
- **`src/mesh.py`** - `Mesh` class for storing geometry (vertices and indices)
- **`src/shader.py`** - Shader module loader for SPIR-V shaders

## Usage

### 1. Compile Shaders

Before running, compile the GLSL shaders to SPIR-V:

```bash
python compile_shaders.py
```

This requires the Vulkan SDK to be installed with `glslc` compiler.

### 2. Run the Application

```bash
python main.py
```

You should see a window with a colored triangle rendered using Vulkan!

**Controls:**
- Press `ESC` to close the window
- Close the window using the X button

## Features

### Core Features
- ✅ **Modular Architecture** - Clean separation of concerns (Window, Renderer, Application)
- ✅ **GLFW Window Management** - Window creation, event handling, resize callbacks
- ✅ **Full Vulkan Pipeline** - Complete rendering pipeline implementation
- ✅ **Type Hints** - Full Python type annotations for better IDE support

### Vulkan Components
- ✅ **Instance & Devices** - Vulkan instance, physical device selection, logical device
- ✅ **Surface & Swap Chain** - Window surface and swap chain management
- ✅ **Graphics Pipeline** - Shader loading, pipeline layout, and graphics pipeline
- ✅ **Render Pass** - Color attachment and subpass configuration
- ✅ **Command Buffers** - Command pool and buffer management
- ✅ **Synchronization** - Semaphores and fences for frame pacing
- ✅ **Vertex Buffers** - GPU memory allocation and vertex data upload
- ✅ **Resource Cleanup** - Proper cleanup of all Vulkan resources

### Rendering Features
- ✅ **Vertex Class** - Structured vertex data with position and color
- ✅ **Mesh System** - Mesh class for geometry with vertex/index buffers
- ✅ **Shader Support** - GLSL vertex and fragment shaders compiled to SPIR-V
- ✅ **Triangle Rendering** - Working example rendering a colored triangle
- ✅ **Multiple Meshes** - Support for rendering multiple mesh objects

## Next Steps

This project provides a complete Vulkan rendering foundation. You can extend it with:

### Geometry & Rendering
- **Index Buffers** - Implement indexed rendering for more complex meshes
- **3D Models** - Load OBJ or GLTF models
- **Multiple Shapes** - Add quad, cube, sphere mesh generators
- **Instancing** - Render multiple instances of the same mesh efficiently

### Visual Enhancements
- **Textures** - Implement texture loading and sampling
- **Depth Buffer** - Add depth testing for 3D rendering
- **Camera System** - Implement view and projection matrices
- **Lighting** - Add Phong or PBR lighting models
- **Normal Mapping** - Enhanced surface details

### Advanced Features
- **Uniform Buffers** - Dynamic transformation matrices
- **Push Constants** - Fast per-draw data updates
- **Multiple Render Passes** - Post-processing effects
- **Compute Shaders** - GPU compute capabilities
- **Dynamic Swap Chain** - Handle window resize properly

### Optimization
- **Staging Buffers** - Faster memory transfers
- **Memory Pools** - Better memory management
- **Pipeline Cache** - Faster startup times

## Troubleshooting

**"Failed to create Vulkan instance"**
- Make sure the Vulkan SDK is installed
- Verify your GPU supports Vulkan
- Check that Vulkan drivers are up to date

**"Failed to initialize GLFW"**
- Ensure GLFW is properly installed via pip
- Try reinstalling: `pip install --upgrade glfw`

**Import errors**
- Make sure all dependencies are installed: `pip install -r requirements.txt`
- Verify you're using the correct Python version

## License

MIT License - Feel free to use this as a starting point for your Vulkan projects!

