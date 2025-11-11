@echo off
echo Compiling shaders...

glslc shader.vert -o vert.spv
if %errorlevel% neq 0 (
    echo ERROR: Failed to compile vertex shader
    exit /b 1
)
echo [OK] Vertex shader compiled

glslc shader.frag -o frag.spv
if %errorlevel% neq 0 (
    echo ERROR: Failed to compile fragment shader
    exit /b 1
)
echo [OK] Fragment shader compiled

echo.
echo All shaders compiled successfully!

