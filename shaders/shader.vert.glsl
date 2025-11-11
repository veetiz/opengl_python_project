#version 330 core

layout(location = 0) in vec3 inPosition;
layout(location = 1) in vec3 inColor;
layout(location = 2) in vec2 inTexCoord;
layout(location = 3) in vec3 inNormal;
layout(location = 4) in vec3 inTangent;
layout(location = 5) in vec3 inBitangent;

out vec3 fragColor;
out vec2 fragTexCoord;
out vec3 fragNormal;
out vec3 fragPos;
out mat3 TBN;
out vec4 fragPosLightSpaceDirectional;
out vec4 fragPosLightSpaceSpot[4];

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;
uniform mat4 lightSpaceMatrixDirectional;
uniform mat4 lightSpaceMatrixSpot[4];
uniform int numSpotLights;

void main() {
    vec4 worldPos = model * vec4(inPosition, 1.0);
    
    gl_Position = projection * view * worldPos;
    fragColor = inColor;
    fragTexCoord = inTexCoord;
    fragPos = vec3(worldPos);
    
    // Transform TBN vectors to world space
    mat3 normalMatrix = mat3(transpose(inverse(model)));
    vec3 T = normalize(normalMatrix * inTangent);
    vec3 B = normalize(normalMatrix * inBitangent);
    vec3 N = normalize(normalMatrix * inNormal);
    
    // Build TBN matrix for tangent space to world space transformation
    TBN = mat3(T, B, N);
    
    // Also pass the normal for non-normal-mapped rendering
    fragNormal = N;
    
    // Calculate light space positions for shadow mapping
    fragPosLightSpaceDirectional = lightSpaceMatrixDirectional * worldPos;
    
    for (int i = 0; i < numSpotLights && i < 4; i++) {
        fragPosLightSpaceSpot[i] = lightSpaceMatrixSpot[i] * worldPos;
    }
}
