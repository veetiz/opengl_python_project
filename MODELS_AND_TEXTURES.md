# Model Loading and Textures Guide

This engine supports loading 3D models and textures.

## Supported Formats

### Models
- **.OBJ** - Fully supported via PyWavefront
- **.FBX** - Fully supported via pyassimp

### Textures
- **.PNG** - Recommended
- **.JPG** / **.JPEG** - Supported
- **.BMP** - Supported
- Any format supported by PIL/Pillow

## Installation

Install required dependencies:

```bash
pip install PyWavefront Pillow pyassimp
```

Note: For FBX support, pyassimp requires the Assimp library to be installed on your system.

## Usage Examples

### Loading an OBJ Model

```python
from src import ModelLoader, GameObject

# Load model from OBJ file
model = ModelLoader.load_obj("assets/models/cube.obj")

# Optional: Load with texture
model = ModelLoader.load_obj(
    "assets/models/cube.obj",
    texture_path="assets/textures/cube_texture.png"
)

# Create GameObject with loaded model
obj = GameObject(name="LoadedCube", model=model)
scene.add_game_object(obj)
```

### Loading a Texture

```python
from src import Texture, Mesh, Vertex

# Load texture
texture = Texture("assets/textures/brick.png")

# Create mesh with texture
vertices = [...]  # Your vertices with UV coordinates
mesh = Mesh(vertices, texture=texture)
```

### Creating Textured Vertices

```python
from src import Vertex

# Vertex with position, color, and UV coordinates
vertex = Vertex(
    position=(0.0, 0.0, 0.0),
    color=(1.0, 1.0, 1.0),
    texcoord=(0.0, 0.0),  # UV coordinates
    normal=(0.0, 1.0, 0.0)  # Normal vector
)
```

## Directory Structure

Recommended folder structure:

```
project/
├── assets/
│   ├── models/
│   │   ├── cube.obj
│   │   ├── sphere.obj
│   │   └── character.obj
│   └── textures/
│       ├── brick.png
│       ├── wood.png
│       └── metal.jpg
├── game/
│   └── scripts/
├── src/
└── main.py
```

## Example: Complete Textured Model

```python
# In main.py
from src import ModelLoader, GameObject, Texture

# Load model with texture
model = ModelLoader.load_obj(
    "assets/models/cube.obj",
    texture_path="assets/textures/cube_diffuse.png"
)

if model:
    # Create GameObject
    cube = GameObject(
        name="TexturedCube",
        model=model,
        position=(0.0, 0.0, 0.0),
        scale=(1.0, 1.0, 1.0)
    )
    scene.add_game_object(cube)
else:
    print("Failed to load model!")
```

## Shader Support

The default shaders support:
- ✅ Texture mapping
- ✅ Vertex colors
- ✅ Normal mapping (basic)
- ✅ Mix texture with vertex color

## Notes

- Textures are automatically bound during rendering
- If no texture is provided, vertex colors are used
- The engine creates a default white texture for untextured meshes
- UV coordinates are required for proper texture mapping
- OBJ files should include texture coordinates (vt in the file)

