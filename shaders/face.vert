#version 420

in vec3 face_vertices;
in vec3 normal_vector;

out float shadow;

uniform mat4 light_matrix;
uniform mat4 rotation_matrix;
uniform vec4 light_vector;

layout(binding=0) uniform sampler2DShadow depth_map;

void main(void) {
    vec4 source_position = vec4(face_vertices, 1.0);
    gl_Position = rotation_matrix * source_position;

    vec4 light_projection = light_matrix * source_position;
    light_projection.xyz += light_projection.w;
    light_projection.w *= 2.0;

    float nl_cosine = - dot(light_vector.xyz, normal_vector);
    float intensity = (nl_cosine + light_vector.a) / (1.0 + light_vector.a);
    shadow = 0.0;

    if (nl_cosine > 0.0) {
        shadow += textureProjOffset(depth_map, light_projection, ivec2(-1, -1));
        shadow += textureProjOffset(depth_map, light_projection, ivec2(-1, 1));
        shadow += textureProjOffset(depth_map, light_projection, ivec2(1, -1));
        shadow += textureProjOffset(depth_map, light_projection, ivec2(1, 1));
        shadow += textureProjOffset(depth_map, light_projection, ivec2(0, 0));
        shadow = shadow < 3.0? shadow / 5.0 : 1.0;
    }

    shadow = max(intensity, 0.0) * max(shadow, light_vector.a);
}
