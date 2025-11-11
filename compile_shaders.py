"""
Shader Compilation Script
Compiles GLSL shaders to SPIR-V using glslc from Vulkan SDK.
"""

import subprocess
import os
import sys


def find_glslc():
    """Try to find glslc in common Vulkan SDK locations."""
    # Common Vulkan SDK paths
    possible_paths = [
        os.path.expandvars(r"$VULKAN_SDK\Bin\glslc.exe"),
        r"C:\VulkanSDK\1.3.275.0\Bin\glslc.exe",
        r"C:\VulkanSDK\1.3.268.0\Bin\glslc.exe",
        r"C:\VulkanSDK\1.3.261.1\Bin\glslc.exe",
    ]
    
    # Check if glslc is in PATH
    try:
        result = subprocess.run(["glslc", "--version"], capture_output=True)
        if result.returncode == 0:
            return "glslc"
    except:
        pass
    
    # Check common paths
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def compile_shader(glslc_path, input_file, output_file):
    """Compile a single shader."""
    print(f"Compiling {input_file}...")
    try:
        result = subprocess.run(
            [glslc_path, input_file, "-o", output_file],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            print(f"  ERROR: {result.stderr}")
            return False
        
        print(f"  [OK] Compiled to {output_file}")
        return True
        
    except Exception as e:
        print(f"  ERROR: {e}")
        return False


def main():
    print("=" * 60)
    print("Vulkan Shader Compiler")
    print("=" * 60)
    
    # Find glslc
    glslc = find_glslc()
    if not glslc:
        print("\nERROR: glslc not found!")
        print("\nPlease ensure Vulkan SDK is installed and either:")
        print("  1. Add Vulkan SDK Bin to your PATH, or")
        print("  2. Set VULKAN_SDK environment variable")
        print("\nDownload Vulkan SDK from: https://vulkan.lunarg.com/")
        return 1
    
    print(f"\nFound glslc: {glslc}")
    print()
    
    # Compile shaders
    shaders = [
        ("shaders/shader.vert", "shaders/vert.spv"),
        ("shaders/shader.frag", "shaders/frag.spv")
    ]
    
    success = True
    for src, dst in shaders:
        if not os.path.exists(src):
            print(f"ERROR: Source file not found: {src}")
            success = False
            continue
        
        if not compile_shader(glslc, src, dst):
            success = False
    
    print()
    if success:
        print("=" * 60)
        print("All shaders compiled successfully!")
        print("=" * 60)
        return 0
    else:
        print("=" * 60)
        print("Some shaders failed to compile!")
        print("=" * 60)
        return 1


if __name__ == "__main__":
    sys.exit(main())

