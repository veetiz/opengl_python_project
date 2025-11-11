#version 330 core

layout (location = 0) in vec4 vertex; // <vec2 pos, vec2 tex>

out vec2 TexCoords;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform int billboard;  // 1 = billboard mode, 0 = world-oriented

void main()
{
    if (billboard == 1) {
        // Billboard mode - make text always face camera
        // Extract camera right and up vectors from view matrix
        vec3 cameraRight = vec3(view[0][0], view[1][0], view[2][0]);
        vec3 cameraUp = vec3(view[0][1], view[1][1], view[2][1]);
        
        // Get position and scale from model matrix
        vec3 worldPos = vec3(model[3][0], model[3][1], model[3][2]);
        vec3 scale = vec3(
            length(vec3(model[0][0], model[0][1], model[0][2])),
            length(vec3(model[1][0], model[1][1], model[1][2])),
            length(vec3(model[2][0], model[2][1], model[2][2]))
        );
        
        // Calculate billboard vertex position with scale
        vec3 vertexPos = worldPos 
            + cameraRight * vertex.x * scale.x
            + cameraUp * vertex.y * scale.y;
        
        gl_Position = projection * view * vec4(vertexPos, 1.0);
    } else {
        // World-oriented mode - render on XY plane facing +Z
        // Apply full transformation (position, rotation, scale)
        vec4 localPos = vec4(vertex.x, vertex.y, 0.0, 1.0);
        gl_Position = projection * view * model * localPos;
    }
    
    TexCoords = vertex.zw;
}

