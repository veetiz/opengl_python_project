"""
Model Module
Represents a 3D model with mesh data.
"""

from typing import List, Optional, TYPE_CHECKING
from .mesh import Mesh
from .vertex import Vertex

if TYPE_CHECKING:
    from .texture import Texture


class Model:
    """Represents a 3D model composed of one or more meshes."""
    
    def __init__(self, name: str = "Model"):
        """
        Initialize a model.
        
        Args:
            name: Model name for identification
        """
        self.name = name
        self.meshes: List[Mesh] = []
    
    def add_mesh(self, mesh: Mesh):
        """
        Add a mesh to this model.
        
        Args:
            mesh: Mesh to add
        """
        self.meshes.append(mesh)
    
    @property
    def mesh_count(self) -> int:
        """Get the number of meshes in this model."""
        return len(self.meshes)
    
    @staticmethod
    def create_triangle(name: str = "Triangle") -> 'Model':
        """
        Create a simple triangle model.
        
        Args:
            name: Model name
            
        Returns:
            Model with a single triangle mesh
        """
        model = Model(name)
        model.add_mesh(Mesh.create_triangle())
        return model
    
    @staticmethod
    def create_quad(name: str = "Quad") -> 'Model':
        """
        Create a simple quad model.
        
        Args:
            name: Model name
            
        Returns:
            Model with a single quad mesh
        """
        model = Model(name)
        model.add_mesh(Mesh.create_quad())
        return model
    
    @staticmethod
    def create_cube(name: str = "Cube") -> 'Model':
        """
        Create a cube model.
        
        Args:
            name: Model name
            
        Returns:
            Model with cube mesh
        """
        # Define cube vertices (position + color)
        vertices = [
            # Front face (red)
            Vertex(position=(-0.5, -0.5,  0.5), color=(1.0, 0.0, 0.0)),
            Vertex(position=( 0.5, -0.5,  0.5), color=(1.0, 0.0, 0.0)),
            Vertex(position=( 0.5,  0.5,  0.5), color=(1.0, 0.0, 0.0)),
            Vertex(position=(-0.5,  0.5,  0.5), color=(1.0, 0.0, 0.0)),
            
            # Back face (green)
            Vertex(position=(-0.5, -0.5, -0.5), color=(0.0, 1.0, 0.0)),
            Vertex(position=( 0.5, -0.5, -0.5), color=(0.0, 1.0, 0.0)),
            Vertex(position=( 0.5,  0.5, -0.5), color=(0.0, 1.0, 0.0)),
            Vertex(position=(-0.5,  0.5, -0.5), color=(0.0, 1.0, 0.0)),
        ]
        
        # Define cube indices
        indices = [
            # Front face
            0, 1, 2, 2, 3, 0,
            # Back face
            5, 4, 7, 7, 6, 5,
            # Left face
            4, 0, 3, 3, 7, 4,
            # Right face
            1, 5, 6, 6, 2, 1,
            # Top face
            3, 2, 6, 6, 7, 3,
            # Bottom face
            4, 5, 1, 1, 0, 4
        ]
        
        model = Model(name)
        model.add_mesh(Mesh(vertices, indices))
        return model
    
    @staticmethod
    def create_textured_quad(name: str = "TexturedQuad", texture: Optional['Texture'] = None) -> 'Model':
        """
        Create a quad with proper UV coordinates for texturing.
        
        Args:
            name: Model name
            texture: Optional texture to apply
            
        Returns:
            Model with textured quad mesh
        """
        vertices = [
            # Position, Color, TexCoord, Normal
            Vertex(position=(-0.5, -0.5, 0.0), color=(1.0, 1.0, 1.0), texcoord=(0.0, 0.0), normal=(0.0, 0.0, 1.0)),
            Vertex(position=( 0.5, -0.5, 0.0), color=(1.0, 1.0, 1.0), texcoord=(1.0, 0.0), normal=(0.0, 0.0, 1.0)),
            Vertex(position=( 0.5,  0.5, 0.0), color=(1.0, 1.0, 1.0), texcoord=(1.0, 1.0), normal=(0.0, 0.0, 1.0)),
            Vertex(position=(-0.5,  0.5, 0.0), color=(1.0, 1.0, 1.0), texcoord=(0.0, 1.0), normal=(0.0, 0.0, 1.0)),
        ]
        indices = [0, 1, 2, 2, 3, 0]
        
        model = Model(name)
        mesh = Mesh(vertices, indices, texture=texture)
        model.add_mesh(mesh)
        return model
    
    @staticmethod
    def create_textured_cube(name: str = "TexturedCube", texture: Optional['Texture'] = None) -> 'Model':
        """
        Create a textured cube with proper UV coordinates.
        
        Args:
            name: Model name
            texture: Optional texture to apply
            
        Returns:
            Model with textured cube mesh
        """
        vertices = [
            # Front face (z = 0.5) - looking at +Z
            Vertex(position=(-0.5, -0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 0.0), normal=(0.0, 0.0, 1.0)),
            Vertex(position=( 0.5, -0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 0.0), normal=(0.0, 0.0, 1.0)),
            Vertex(position=( 0.5,  0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 1.0), normal=(0.0, 0.0, 1.0)),
            Vertex(position=(-0.5,  0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 1.0), normal=(0.0, 0.0, 1.0)),
            
            # Back face (z = -0.5) - looking at -Z (reversed winding)
            Vertex(position=( 0.5, -0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 0.0), normal=(0.0, 0.0, -1.0)),
            Vertex(position=(-0.5, -0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 0.0), normal=(0.0, 0.0, -1.0)),
            Vertex(position=(-0.5,  0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 1.0), normal=(0.0, 0.0, -1.0)),
            Vertex(position=( 0.5,  0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 1.0), normal=(0.0, 0.0, -1.0)),
            
            # Left face (x = -0.5) - looking at -X
            Vertex(position=(-0.5, -0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 0.0), normal=(-1.0, 0.0, 0.0)),
            Vertex(position=(-0.5, -0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 0.0), normal=(-1.0, 0.0, 0.0)),
            Vertex(position=(-0.5,  0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 1.0), normal=(-1.0, 0.0, 0.0)),
            Vertex(position=(-0.5,  0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 1.0), normal=(-1.0, 0.0, 0.0)),
            
            # Right face (x = 0.5) - looking at +X (reversed winding)
            Vertex(position=(0.5, -0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 0.0), normal=(1.0, 0.0, 0.0)),
            Vertex(position=(0.5, -0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 0.0), normal=(1.0, 0.0, 0.0)),
            Vertex(position=(0.5,  0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 1.0), normal=(1.0, 0.0, 0.0)),
            Vertex(position=(0.5,  0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 1.0), normal=(1.0, 0.0, 0.0)),
            
            # Top face (y = 0.5) - looking at +Y
            Vertex(position=(-0.5,  0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 0.0), normal=(0.0, 1.0, 0.0)),
            Vertex(position=( 0.5,  0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 0.0), normal=(0.0, 1.0, 0.0)),
            Vertex(position=( 0.5,  0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 1.0), normal=(0.0, 1.0, 0.0)),
            Vertex(position=(-0.5,  0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 1.0), normal=(0.0, 1.0, 0.0)),
            
            # Bottom face (y = -0.5) - looking at -Y (reversed winding)
            Vertex(position=(-0.5, -0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 0.0), normal=(0.0, -1.0, 0.0)),
            Vertex(position=( 0.5, -0.5, -0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 0.0), normal=(0.0, -1.0, 0.0)),
            Vertex(position=( 0.5, -0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(1.0, 1.0), normal=(0.0, -1.0, 0.0)),
            Vertex(position=(-0.5, -0.5,  0.5), color=(1.0, 1.0, 1.0), texcoord=(0.0, 1.0), normal=(0.0, -1.0, 0.0)),
        ]
        
        indices = [
            # Front (CCW from outside)
            0, 1, 2, 2, 3, 0,
            # Back (CCW from outside)
            4, 5, 6, 6, 7, 4,
            # Left (CCW from outside)
            8, 9, 10, 10, 11, 8,
            # Right (CCW from outside)
            12, 13, 14, 14, 15, 12,
            # Top (CCW from outside)
            16, 17, 18, 18, 19, 16,
            # Bottom (CCW from outside)
            20, 21, 22, 22, 23, 20
        ]
        
        model = Model(name)
        mesh = Mesh(vertices, indices, texture=texture)
        model.add_mesh(mesh)
        return model

