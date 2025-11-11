# Shaders

This directory contains GLSL shaders for the Vulkan renderer.

## Compiling Shaders

Before running the application, you need to compile the GLSL shaders to SPIR-V format.

### Automatic Compilation (Recommended)

Run the Python compilation script from the project root:

```bash
python compile_shaders.py
```

This script will automatically find `glslc` from your Vulkan SDK installation and compile the shaders.

### Manual Compilation

If you have `glslc` in your PATH, you can compile manually:

```bash
cd shaders
glslc shader.vert -o vert.spv
glslc shader.frag -o frag.spv
```

Or on Windows, run the batch file:

```cmd
cd shaders
compile_shaders.bat
```

## Shader Files

- `shader.vert` - Vertex shader (transforms vertices and passes colors)
- `shader.frag` - Fragment shader (outputs interpolated colors)
- `vert.spv` - Compiled vertex shader (SPIR-V bytecode)
- `frag.spv` - Compiled fragment shader (SPIR-V bytecode)

## Requirements

- **Vulkan SDK** must be installed
- **glslc** compiler (included with Vulkan SDK)

Download Vulkan SDK from: https://vulkan.lunarg.com/

