#version 330 core

in vec3 fragColor;
in vec2 fragTexCoord;
in vec3 fragNormal;
in vec3 fragPos;
in mat3 TBN;
in vec4 fragPosLightSpaceDirectional;
in vec4 fragPosLightSpaceSpot[4];

out vec4 outColor;

// Texture samplers - assign specific units
uniform sampler2D textureSampler;              // Unit 0
uniform sampler2D normalMap;                   // Unit 1
uniform sampler2D shadowMapDirectional;        // Unit 2
uniform sampler2D shadowMapSpot0;              // Unit 3
uniform sampler2D shadowMapSpot1;              // Unit 4
uniform sampler2D shadowMapSpot2;              // Unit 5
uniform sampler2D shadowMapSpot3;              // Unit 6
uniform samplerCube shadowMapPoint0;           // Unit 7
uniform samplerCube shadowMapPoint1;           // Unit 8
uniform samplerCube shadowMapPoint2;           // Unit 9
uniform samplerCube shadowMapPoint3;           // Unit 10
uniform sampler2D roughnessMap;                // Unit 11
uniform sampler2D aoMap;                       // Unit 12

uniform int useTexture;
uniform int useRoughnessMap;
uniform int useAOMap;

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
uniform int useNormalMap;

// Shadow mapping
uniform int useShadowsDirectional;
uniform int useShadowsPoint[4];
uniform int useShadowsSpot[4];
uniform mat4 lightSpaceMatrixDirectional;
uniform mat4 lightSpaceMatrixSpot[4];
uniform vec3 pointLightPosForShadow[4];
uniform float pointLightFarPlane[4];

// Lighting enabled/disabled
uniform int lightingEnabled;

// Shadow calculation functions
float calculateShadowDirectional(vec4 fragPosLightSpace, vec3 normal, vec3 lightDir) {
    // Perform perspective divide
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // Transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;
    
    // Get closest depth value from light's perspective
    float closestDepth = texture(shadowMapDirectional, projCoords.xy).r;
    // Get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    
    // Calculate bias to reduce shadow acne
    float bias = max(0.005 * (1.0 - dot(normal, lightDir)), 0.001);
    
    // PCF (Percentage Closer Filtering) for soft shadows
    float shadow = 0.0;
    vec2 texelSize = 1.0 / textureSize(shadowMapDirectional, 0);
    for(int x = -1; x <= 1; ++x)
    {
        for(int y = -1; y <= 1; ++y)
        {
            float pcfDepth = texture(shadowMapDirectional, projCoords.xy + vec2(x, y) * texelSize).r;
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;
        }
    }
    shadow /= 9.0;
    
    // Keep the shadow at 0.0 when outside the far_plane region of the light's frustum
    if(projCoords.z > 1.0)
        shadow = 0.0;
    
    return shadow;
}

float calculateShadowPoint(int index, vec3 fragPos) {
    // Get vector between fragment position and light position
    vec3 fragToLight = fragPos - pointLightPosForShadow[index];
    
    // Use the light to fragment vector to sample from the depth map
    float closestDepth;
    if (index == 0) closestDepth = texture(shadowMapPoint0, fragToLight).r;
    else if (index == 1) closestDepth = texture(shadowMapPoint1, fragToLight).r;
    else if (index == 2) closestDepth = texture(shadowMapPoint2, fragToLight).r;
    else closestDepth = texture(shadowMapPoint3, fragToLight).r;
    
    // It is currently in linear range between [0,1]. Re-transform back to original value
    closestDepth *= pointLightFarPlane[index];
    
    // Now get current linear depth as the length between the fragment and light position
    float currentDepth = length(fragToLight);
    
    // Test for shadows with bias
    float bias = 0.05;
    float shadow = currentDepth - bias > closestDepth ? 1.0 : 0.0;
    
    return shadow;
}

float calculateShadowSpot(int index, vec4 fragPosLightSpace, vec3 normal, vec3 lightDir) {
    // Perform perspective divide
    vec3 projCoords = fragPosLightSpace.xyz / fragPosLightSpace.w;
    // Transform to [0,1] range
    projCoords = projCoords * 0.5 + 0.5;
    
    // Get the correct shadow map based on index
    vec2 texelSize;
    if (index == 0) texelSize = 1.0 / textureSize(shadowMapSpot0, 0);
    else if (index == 1) texelSize = 1.0 / textureSize(shadowMapSpot1, 0);
    else if (index == 2) texelSize = 1.0 / textureSize(shadowMapSpot2, 0);
    else texelSize = 1.0 / textureSize(shadowMapSpot3, 0);
    
    // Calculate bias
    float bias = max(0.005 * (1.0 - dot(normal, lightDir)), 0.001);
    
    // Get depth of current fragment from light's perspective
    float currentDepth = projCoords.z;
    
    // PCF for soft shadows
    float shadow = 0.0;
    for(int x = -1; x <= 1; ++x)
    {
        for(int y = -1; y <= 1; ++y)
        {
            vec2 sampleCoord = projCoords.xy + vec2(x, y) * texelSize;
            float pcfDepth;
            if (index == 0) pcfDepth = texture(shadowMapSpot0, sampleCoord).r;
            else if (index == 1) pcfDepth = texture(shadowMapSpot1, sampleCoord).r;
            else if (index == 2) pcfDepth = texture(shadowMapSpot2, sampleCoord).r;
            else pcfDepth = texture(shadowMapSpot3, sampleCoord).r;
            
            shadow += currentDepth - bias > pcfDepth ? 1.0 : 0.0;
        }
    }
    shadow /= 9.0;
    
    if(projCoords.z > 1.0)
        shadow = 0.0;
    
    return shadow;
}

vec3 calculateDirectionalLight(vec3 normal, vec3 viewDir, vec3 baseColor, float shadow, float roughness, float ao) {
    vec3 lightDir = normalize(-dirLight_direction);
    
    // Diffuse
    float diff = max(dot(normal, lightDir), 0.0);
    
    // Specular (Blinn-Phong) - roughness affects shininess
    // Higher roughness = lower shininess = larger, dimmer highlights
    float shininess = material_shininess * (1.0 - roughness * 0.9); // Reduce shininess by up to 90%
    shininess = max(shininess, 1.0); // Minimum shininess of 1
    
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), shininess);
    
    // Roughness also affects specular intensity
    float specularIntensity = 1.0 - roughness * 0.7;
    
    // Combine
    vec3 ambient = material_ambient * baseColor * ao; // AO affects ambient
    vec3 diffuse = material_diffuse * diff * baseColor;
    vec3 specular = material_specular * spec * specularIntensity;
    
    // Apply shadow (ambient is not affected by shadows)
    return (ambient + (1.0 - shadow) * (diffuse + specular)) * dirLight_color * dirLight_intensity;
}

vec3 calculatePointLight(int index, vec3 normal, vec3 viewDir, vec3 baseColor, float shadow, float roughness, float ao) {
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
    
    // Specular (Blinn-Phong) - roughness affects shininess
    float shininess = material_shininess * (1.0 - roughness * 0.9);
    shininess = max(shininess, 1.0);
    
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), shininess);
    
    float specularIntensity = 1.0 - roughness * 0.7;
    
    // Combine
    vec3 ambient = material_ambient * baseColor * ao;
    vec3 diffuse = material_diffuse * diff * baseColor;
    vec3 specular = material_specular * spec * specularIntensity;
    
    // Apply shadow (ambient is not affected by shadows)
    return (ambient + (1.0 - shadow) * (diffuse + specular)) * lightColor * intensity * attenuation;
}

vec3 calculateSpotLight(int index, vec3 normal, vec3 viewDir, vec3 baseColor, float shadow, float roughness, float ao) {
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
    
    // Specular (Blinn-Phong) - roughness affects shininess
    float shininess = material_shininess * (1.0 - roughness * 0.9);
    shininess = max(shininess, 1.0);
    
    vec3 halfwayDir = normalize(lightDir + viewDir);
    float spec = pow(max(dot(normal, halfwayDir), 0.0), shininess);
    
    float specularIntensity = 1.0 - roughness * 0.7;
    
    // Combine
    vec3 ambient = material_ambient * baseColor * ao;
    vec3 diffuse = material_diffuse * diff * baseColor;
    vec3 specular = material_specular * spec * specularIntensity;
    
    vec3 lightColor = spotLights_color[index];
    float intensity = spotLights_intensity[index];
    
    // Apply shadow (ambient is not affected by shadows)
    return (ambient + (1.0 - shadow) * (diffuse + specular)) * lightColor * intensity * attenuation * intensity_factor;
}

void main() {
    // Get normal (potentially from normal map)
    vec3 norm;
    if (useNormalMap == 1) {
        // Sample normal from normal map and transform to [-1, 1] range
        norm = texture(normalMap, fragTexCoord).rgb;
        norm = normalize(norm * 2.0 - 1.0);
        // Transform from tangent space to world space using TBN matrix
        norm = normalize(TBN * norm);
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
    
    // Sample roughness (if available)
    float roughness = 0.5; // Default medium roughness
    if (useRoughnessMap == 1) {
        roughness = texture(roughnessMap, fragTexCoord).r; // Use red channel
    }
    
    // Sample ambient occlusion (if available)
    float ao = 1.0; // Default no occlusion
    if (useAOMap == 1) {
        ao = texture(aoMap, fragTexCoord).r; // Use red channel
    }
    
    // Apply lighting if enabled
    if (lightingEnabled == 1) {
        vec3 result = vec3(0.0);
        
        // Directional light
        if (hasDirectionalLight == 1) {
            float shadow = 0.0;
            if (useShadowsDirectional == 1) {
                vec3 lightDir = normalize(-dirLight_direction);
                shadow = calculateShadowDirectional(fragPosLightSpaceDirectional, norm, lightDir);
            }
            result += calculateDirectionalLight(norm, viewDir, baseColor, shadow, roughness, ao);
        }
        
        // Point lights
        for (int i = 0; i < numPointLights && i < 4; i++) {
            float shadow = 0.0;
            if (useShadowsPoint[i] == 1) {
                shadow = calculateShadowPoint(i, fragPos);
            }
            result += calculatePointLight(i, norm, viewDir, baseColor, shadow, roughness, ao);
        }
        
        // Spot lights
        for (int i = 0; i < numSpotLights && i < 4; i++) {
            float shadow = 0.0;
            if (useShadowsSpot[i] == 1) {
                vec3 lightDir = normalize(spotLights_position[i] - fragPos);
                shadow = calculateShadowSpot(i, fragPosLightSpaceSpot[i], norm, lightDir);
            }
            result += calculateSpotLight(i, norm, viewDir, baseColor, shadow, roughness, ao);
        }
        
        // If no lights, use ambient only (with AO)
        if (hasDirectionalLight == 0 && numPointLights == 0 && numSpotLights == 0) {
            result = material_ambient * baseColor * ao;
        }
        
        outColor = vec4(result, 1.0);
    } else {
        // No lighting - just use base color (still apply AO for depth)
        outColor = vec4(baseColor * ao, 1.0);
    }
}
