"""
Model Loader Module
Loads 3D models from various file formats (.obj, .fbx).
"""

import os
import numpy as np
from typing import Optional, List, Tuple
from .model import Model
from .mesh import Mesh
from .vertex import Vertex
from .texture import Texture


class ModelLoader:
    """Handles loading 3D models from files."""
    
    @staticmethod
    def load_obj(filepath: str, texture_path: Optional[str] = None) -> Optional[Model]:
        """
        Load a model from an OBJ file.
        
        Args:
            filepath: Path to .obj file
            texture_path: Optional path to texture file
            
        Returns:
            Model instance if successful, None otherwise
        """
        try:
            import pywavefront  # type: ignore
            
            if not os.path.exists(filepath):
                print(f"ERROR: OBJ file not found: {filepath}")
                return None
            
            # Load OBJ file
            scene = pywavefront.Wavefront(filepath, collect_faces=True, create_materials=True)
            
            # Extract model name from filename
            model_name = os.path.splitext(os.path.basename(filepath))[0]
            model = Model(model_name)
            
            # Process each mesh in the OBJ file
            for mesh_name, mesh_data in scene.meshes.items():
                vertices = []
                
                # Get vertex data from the mesh
                for material in mesh_data.materials:
                    # PyWavefront vertices are in format: [x,y,z, nx,ny,nz, u,v, ...]
                    # depending on what's in the OBJ file
                    vertex_format = material.vertex_format
                    
                    for i in range(0, len(material.vertices), len(vertex_format.split('/'))):
                        # Extract position
                        pos_x = material.vertices[i] if i < len(material.vertices) else 0.0
                        pos_y = material.vertices[i+1] if i+1 < len(material.vertices) else 0.0
                        pos_z = material.vertices[i+2] if i+2 < len(material.vertices) else 0.0
                        
                        # Try to extract normals and UVs based on format
                        # Common format: "T2F_N3F_V3F" = texture(2) normal(3) vertex(3)
                        # or "N3F_V3F" = normal(3) vertex(3)
                        # or "V3F" = vertex(3)
                        
                        # Default values
                        color = (1.0, 1.0, 1.0)
                        texcoord = None
                        normal = None
                        
                        # Parse vertex format to extract data correctly
                        # For now, use simple extraction
                        if 'T2F' in vertex_format and i+7 < len(material.vertices):
                            texcoord = (material.vertices[i+6], material.vertices[i+7])
                        
                        if 'N3F' in vertex_format and i+5 < len(material.vertices):
                            normal = (material.vertices[i+3], material.vertices[i+4], material.vertices[i+5])
                        
                        vertex = Vertex(
                            position=(pos_x, pos_y, pos_z),
                            color=color,
                            texcoord=texcoord,
                            normal=normal
                        )
                        vertices.append(vertex)
                
                if vertices:
                    mesh = Mesh(vertices)
                    
                    # Load texture if provided
                    if texture_path and os.path.exists(texture_path):
                        mesh.texture = Texture(texture_path)
                    
                    model.add_mesh(mesh)
            
            print(f"[OK] Loaded OBJ model '{model_name}' with {model.mesh_count} mesh(es)")
            return model
            
        except ImportError:
            print("ERROR: PyWavefront not installed. Run: pip install PyWavefront")
            return None
        except Exception as e:
            print(f"ERROR: Failed to load OBJ file '{filepath}': {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def load_fbx(filepath: str, texture_path: Optional[str] = None) -> Optional[Model]:
        """
        Load a model from an FBX file using pyassimp.
        
        Args:
            filepath: Path to .fbx file
            texture_path: Optional path to texture file
            
        Returns:
            Model instance if successful, None otherwise
        """
        try:
            import pyassimp  # type: ignore
            
            if not os.path.exists(filepath):
                print(f"ERROR: FBX file not found: {filepath}")
                return None
            
            print(f"Loading FBX file: {filepath}")
            
            # Load FBX file with pyassimp
            scene_assimp = pyassimp.load(filepath)
            
            print(f"[DEBUG] Loaded {len(scene_assimp.meshes)} mesh(es) from FBX")
            
            # Extract model name from filename
            model_name = os.path.splitext(os.path.basename(filepath))[0]
            model = Model(model_name)
            
            # Process all meshes in the FBX file
            for assimp_mesh in scene_assimp.meshes:
                print(f"[DEBUG] Processing mesh with {len(assimp_mesh.vertices)} vertices")
                mesh = ModelLoader._convert_assimp_to_mesh(assimp_mesh, texture_path)
                if mesh:
                    print(f"[DEBUG] Added mesh with {mesh.vertex_count} vertices")
                    model.add_mesh(mesh)
            
            # Release the scene
            pyassimp.release(scene_assimp)
            
            print(f"[OK] Loaded FBX model '{model_name}' with {model.mesh_count} mesh(es)")
            return model
            
        except ImportError:
            print("ERROR: pyassimp not installed. Run: pip install pyassimp")
            return None
        except Exception as e:
            print(f"ERROR: Failed to load FBX file '{filepath}': {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def _convert_assimp_to_mesh(assimp_mesh, texture_path: Optional[str] = None) -> Optional[Mesh]:
        """
        Convert an Assimp mesh to our Mesh format.
        
        Args:
            assimp_mesh: Assimp mesh object
            texture_path: Optional path to texture file
            
        Returns:
            Mesh instance if successful, None otherwise
        """
        try:
            vertices = []
            
            # Get vertex positions
            positions = assimp_mesh.vertices
            
            # Get normals
            normals = assimp_mesh.normals if hasattr(assimp_mesh, 'normals') and assimp_mesh.normals is not None else None
            
            # Get UV coordinates (texture coordinates channel 0)
            uvs = None
            if hasattr(assimp_mesh, 'texturecoords') and assimp_mesh.texturecoords is not None:
                if len(assimp_mesh.texturecoords) > 0 and assimp_mesh.texturecoords[0] is not None:
                    uvs = assimp_mesh.texturecoords[0]
            
            # Create vertices
            for i in range(len(positions)):
                pos = tuple(positions[i])
                
                # Normal
                normal = tuple(normals[i]) if normals is not None and i < len(normals) else (0.0, 1.0, 0.0)
                
                # UV (use only U and V, ignore W if present)
                if uvs is not None and i < len(uvs):
                    uv = (uvs[i][0], uvs[i][1])
                else:
                    uv = (0.0, 0.0)
                
                vertex = Vertex(
                    position=pos,
                    color=(1.0, 1.0, 1.0),  # Default white (texture will override)
                    texcoord=uv,
                    normal=normal
                )
                vertices.append(vertex)
            
            # Get indices (faces)
            indices = None
            if hasattr(assimp_mesh, 'faces') and assimp_mesh.faces is not None:
                indices = []
                for face in assimp_mesh.faces:
                    indices.extend(face)
            
            # Load texture if provided
            texture = None
            if texture_path and os.path.exists(texture_path):
                texture = Texture(texture_path)
            
            return Mesh(vertices, indices, texture=texture)
            
        except Exception as e:
            print(f"ERROR: Failed to convert assimp mesh: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    @staticmethod
    def _convert_trimesh_to_mesh(trimesh_geometry, texture_path: Optional[str] = None) -> Optional[Mesh]:
        """
        Convert a trimesh geometry to our Mesh format.
        
        Args:
            trimesh_geometry: Trimesh geometry object
            texture_path: Optional path to texture file
            
        Returns:
            Mesh instance if successful, None otherwise
        """
        try:
            vertices = []
            
            # Get vertex positions
            positions = trimesh_geometry.vertices
            
            # Get normals (or generate if not available)
            if hasattr(trimesh_geometry, 'vertex_normals') and trimesh_geometry.vertex_normals is not None:
                normals = trimesh_geometry.vertex_normals
            else:
                normals = np.zeros_like(positions)
                normals[:, 1] = 1.0  # Default up
            
            # Get UV coordinates if available
            if hasattr(trimesh_geometry, 'visual') and hasattr(trimesh_geometry.visual, 'uv'):
                uvs = trimesh_geometry.visual.uv
            else:
                uvs = np.zeros((len(positions), 2))  # Default UVs
            
            # Create vertices
            for i in range(len(positions)):
                pos = tuple(positions[i])
                normal = tuple(normals[i]) if i < len(normals) else (0.0, 1.0, 0.0)
                uv = tuple(uvs[i]) if i < len(uvs) else (0.0, 0.0)
                
                vertex = Vertex(
                    position=pos,
                    color=(1.0, 1.0, 1.0),  # Default white
                    texcoord=uv,
                    normal=normal
                )
                vertices.append(vertex)
            
            # Get indices (faces)
            indices = None
            if hasattr(trimesh_geometry, 'faces') and trimesh_geometry.faces is not None:
                indices = trimesh_geometry.faces.flatten().tolist()
            
            # Load texture if provided
            texture = None
            if texture_path and os.path.exists(texture_path):
                texture = Texture(texture_path)
            
            return Mesh(vertices, indices, texture=texture)
            
        except Exception as e:
            print(f"ERROR: Failed to convert trimesh geometry: {e}")
            return None
    
    @staticmethod
    def load_model(filepath: str, texture_path: Optional[str] = None) -> Optional[Model]:
        """
        Load a model from file (auto-detects format).
        
        Args:
            filepath: Path to model file
            texture_path: Optional path to texture file
            
        Returns:
            Model instance if successful, None otherwise
        """
        if not os.path.exists(filepath):
            print(f"ERROR: Model file not found: {filepath}")
            return None
        
        # Detect file format
        ext = os.path.splitext(filepath)[1].lower()
        
        if ext == '.obj':
            return ModelLoader.load_obj(filepath, texture_path)
        elif ext == '.fbx':
            return ModelLoader.load_fbx(filepath, texture_path)
        else:
            print(f"ERROR: Unsupported model format: {ext}")
            print("Supported formats: .obj, .fbx")
            return None

