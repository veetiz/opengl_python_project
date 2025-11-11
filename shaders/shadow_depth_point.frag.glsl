#version 330 core

in vec4 FragPos;

uniform vec3 lightPos;
uniform float farPlane;

void main()
{
    // Calculate distance between fragment and light source
    float lightDistance = length(FragPos.xyz - lightPos);
    
    // Map to [0,1] range by dividing by far_plane
    lightDistance = lightDistance / farPlane;
    
    // Write this as the modified depth
    gl_FragDepth = lightDistance;
}

