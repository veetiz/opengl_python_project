#version 330 core

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec3 inColor;
layout(location = 2) in vec2 inTexCoord;
layout(location = 3) in vec3 inNormal;

out vec3 fragColor;
out vec2 fragTexCoord;
out vec3 fragNormal;
out vec3 fragPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main() {
    gl_Position = projection * view * model * vec4(inPosition, 1.0);
    fragColor = inColor;
    fragTexCoord = inTexCoord;
    fragNormal = mat3(transpose(inverse(model))) * inNormal;
    fragPos = vec3(model * vec4(inPosition, 1.0));
}
