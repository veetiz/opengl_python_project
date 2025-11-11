#version 330 core

in vec3 fragColor;
in vec2 fragTexCoord;
in vec3 fragNormal;
in vec3 fragPos;

out vec4 outColor;

uniform sampler2D textureSampler;
uniform int useTexture;

void main() {
    vec4 texColor = texture(textureSampler, fragTexCoord);
    vec4 vertColor = vec4(fragColor, 1.0);
    
    // Mix texture and vertex color, or use vertex color only
    if (useTexture == 1) {
        outColor = texColor * vertColor;
    } else {
        outColor = vertColor;
    }
}
