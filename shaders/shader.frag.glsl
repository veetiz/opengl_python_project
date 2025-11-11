#version 330 core

in vec3 fragColor;
in vec2 fragTexCoord;
in vec3 fragNormal;
in vec3 fragPos;

out vec4 outColor;

uniform sampler2D textureSampler;
uniform int useTexture;

// Material properties
uniform vec3 material_ambient;
uniform vec3 material_diffuse;
uniform vec3 material_specular;
uniform float material_shininess;

// Directional light
uniform int hasDirectionalLight;
uniform vec3 dirLight_direction;
uniform vec3 dirLight_color;
uniform float dirLight_intensity;

// Point lights (support up to 4)
uniform int numPointLights;
uniform vec3 pointLights_position[4];
uniform vec3 pointLights_color[4];
uniform float pointLights_intensity[4];
uniform float pointLights_constant[4];
uniform float pointLights_linear[4];
uniform float pointLights_quadratic[4];

// Spot lights (support up to 4)
uniform int numSpotLights;
uniform vec3 spotLights_position[4];
uniform vec3 spotLights_direction[4];
uniform vec3 spotLights_color[4];
uniform float spotLights_intensity[4];
uniform float spotLights_innerCutoff[4];
uniform float spotLights_outerCutoff[4];
uniform float spotLights_constant[4];
uniform float spotLights_linear[4];
uniform float spotLights_quadratic[4];

// Camera position for specular
uniform vec3 viewPos;

// Normal mapping
uniform sampler2D normalMap;
uniform int useNormalMap;

// Lighting enabled/disabled
uniform int lightingEnabled;

vec3 calculateDirectionalLight(vec3 normal, vec3 viewDir, vec3 baseColor) {
    vec3 lightDir = normalize(-dirLight_direction);
    
    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0);
    
    // Specular (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material_shininess);
    
    // Combine
    vec3 ambient = material_ambient * baseColor;
    vec3 diffuse = material_diffuse * diff * baseColor;
    vec3 specular = material_specular * spec;
    
    return (ambient + diffuse + specular) * dirLight_color * dirLight_intensity;
}

vec3 calculatePointLight(int index, vec3 normal, vec3 viewDir, vec3 baseColor) {
    vec3 lightPos = pointLights_position[index];
    vec3 lightColor = pointLights_color[index];
    float intensity = pointLights_intensity[index];
    
    vec3 lightDir = normalize(lightPos - fragPos);
    float distance = length(lightPos - fragPos);
    
    // Attenuation
    float attenuation = 1.0 / (pointLights_constant[index] + 
                               pointLights_linear[index] * distance + 
                               pointLights_quadratic[index] * distance * distance);
    
    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0);
    
    // Specular (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material_shininess);
    
    // Combine
    vec3 ambient = material_ambient * baseColor;
    vec3 diffuse = material_diffuse * diff * baseColor;
    vec3 specular = material_specular * spec;
    
    return (ambient + diffuse + specular) * lightColor * intensity * attenuation;
}

vec3 calculateSpotLight(int index, vec3 normal, vec3 viewDir, vec3 baseColor) {
    vec3 lightPos = spotLights_position[index];
    vec3 lightDir = normalize(lightPos - fragPos);
    vec3 spotDir = normalize(spotLights_direction[index]);
    
    // Calculate spotlight cone effect
    float theta = dot(lightDir, -spotDir);
    float epsilon = spotLights_innerCutoff[index] - spotLights_outerCutoff[index];
    float intensity_factor = clamp((theta - spotLights_outerCutoff[index]) / epsilon, 0.0, 1.0);
    
    // Distance attenuation
    float distance = length(lightPos - fragPos);
    float attenuation = 1.0 / (spotLights_constant[index] + 
                               spotLights_linear[index] * distance + 
                               spotLights_quadratic[index] * distance * distance);
    
    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0);
    
    // Specular (Blinn-Phong)
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), material_shininess);
    
    // Combine
    vec3 ambient = material_ambient * baseColor;
    vec3 diffuse = material_diffuse * diff * baseColor;
    vec3 specular = material_specular * spec;
    
    vec3 lightColor = spotLights_color[index];
    float intensity = spotLights_intensity[index];
    
    return (ambient + diffuse + specular) * lightColor * intensity * attenuation * intensity_factor;
}

void main() {
    // Get normal (potentially from normal map)
    vec3 norm;
    if (useNormalMap == 1) {
        // Sample normal from normal map and transform to [-1, 1] range
        norm = texture(normalMap, fragTexCoord).rgb;
        norm = normalize(norm * 2.0 - 1.0);
        // TODO: Transform to world space using TBN matrix
    } else {
        norm = normalize(fragNormal);
    }
    
    vec3 viewDir = normalize(viewPos - fragPos);
    
    // Get base color from texture or vertex color
    vec4 texColor = texture(textureSampler, fragTexCoord);
    vec3 baseColor;
    if (useTexture == 1) {
        baseColor = texColor.rgb * fragColor;
    } else {
        baseColor = fragColor;
    }
    
    // Apply lighting if enabled
    if (lightingEnabled == 1) {
        vec3 result = vec3(0.0);
        
        // Directional light
        if (hasDirectionalLight == 1) {
            result += calculateDirectionalLight(norm, viewDir, baseColor);
        }
        
        // Point lights
        for (int i = 0; i < numPointLights && i < 4; i++) {
            result += calculatePointLight(i, norm, viewDir, baseColor);
        }
        
        // Spot lights
        for (int i = 0; i < numSpotLights && i < 4; i++) {
            result += calculateSpotLight(i, norm, viewDir, baseColor);
        }
        
        // If no lights, use ambient only
        if (hasDirectionalLight == 0 && numPointLights == 0 && numSpotLights == 0) {
            result = material_ambient * baseColor;
        }
        
        outColor = vec4(result, 1.0);
    } else {
        // No lighting - just use base color
        outColor = vec4(baseColor, 1.0);
    }
}
