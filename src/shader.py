"""
Shader Module
Handles shader loading and compilation for Vulkan.
"""

import vulkan as vk
import os
from typing import Optional


class ShaderModule:
    """Manages Vulkan shader modules."""
    
    def __init__(self, device, shader_code: bytes):
        """
        Create a shader module.
        
        Args:
            device: Vulkan logical device
            shader_code: SPIR-V shader bytecode
        """
        self.device = device
        self.module = None
        
        create_info = vk.VkShaderModuleCreateInfo(
            sType=vk.VK_STRUCTURE_TYPE_SHADER_MODULE_CREATE_INFO,
            codeSize=len(shader_code),
            pCode=shader_code
        )
        
        try:
            self.module = vk.vkCreateShaderModule(device, create_info, None)
        except Exception as e:
            raise RuntimeError(f"Failed to create shader module: {e}")
    
    def cleanup(self):
        """Clean up the shader module."""
        if self.module:
            vk.vkDestroyShaderModule(self.device, self.module, None)
            self.module = None
    
    @staticmethod
    def load_from_file(device, filepath: str) -> 'ShaderModule':
        """
        Load a shader module from a SPIR-V file.
        
        Args:
            device: Vulkan logical device
            filepath: Path to SPIR-V shader file
            
        Returns:
            ShaderModule instance
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Shader file not found: {filepath}")
        
        with open(filepath, 'rb') as f:
            code = f.read()
        
        return ShaderModule(device, code)


def compile_shaders_if_needed():
    """
    Compile shaders if SPIR-V files don't exist.
    Requires glslc (from Vulkan SDK) to be in PATH.
    """
    shaders_dir = "shaders"
    vert_spirv = os.path.join(shaders_dir, "vert.spv")
    frag_spirv = os.path.join(shaders_dir, "frag.spv")
    
    vert_glsl = os.path.join(shaders_dir, "shader.vert")
    frag_glsl = os.path.join(shaders_dir, "shader.frag")
    
    needs_compile = False
    
    if not os.path.exists(vert_spirv) or not os.path.exists(frag_spirv):
        needs_compile = True
    else:
        # Check if GLSL is newer than SPIR-V
        if os.path.exists(vert_glsl) and os.path.getmtime(vert_glsl) > os.path.getmtime(vert_spirv):
            needs_compile = True
        if os.path.exists(frag_glsl) and os.path.getmtime(frag_glsl) > os.path.getmtime(frag_spirv):
            needs_compile = True
    
    if needs_compile:
        import subprocess
        print("Compiling shaders...")
        try:
            # Compile vertex shader
            result = subprocess.run(
                ["glslc", vert_glsl, "-o", vert_spirv],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"ERROR: Vertex shader compilation failed:\n{result.stderr}")
                return False
            print("[OK] Vertex shader compiled")
            
            # Compile fragment shader
            result = subprocess.run(
                ["glslc", frag_glsl, "-o", frag_spirv],
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                print(f"ERROR: Fragment shader compilation failed:\n{result.stderr}")
                return False
            print("[OK] Fragment shader compiled")
            
        except FileNotFoundError:
            print("WARNING: glslc not found. Please compile shaders manually.")
            print("Run: cd shaders && glslc shader.vert -o vert.spv && glslc shader.frag -o frag.spv")
            return False
    
    return True

