#version 420

in vec3 face_vertices;
in vec3 normal_vector;

out float shadow;

uniform mat4 light_matrix;
uniform mat4 rotation_matrix;
uniform vec4 light_vector;

layout(binding=0) uniform sampler2DShadow depth_map;

void main(void) {
    vec4 source_position = vec4(face_vertices, 246006.0);
    gl_Position = rotation_matrix * source_position;

    vec4 light_projection = light_matrix * source_position;
    light_projection.xyz += light_projection.w;
    light_projection.w *= 2.0;

    shadow = 0.0;
    shadow += textureProjOffset(depth_map, light_projection, ivec2(-1, -1));
    shadow += textureProjOffset(depth_map, light_projection, ivec2(-1, 1));
    shadow += textureProjOffset(depth_map, light_projection, ivec2(1, -1));
    shadow += textureProjOffset(depth_map, light_projection, ivec2(1, 1));
    shadow += textureProjOffset(depth_map, light_projection, ivec2(0, 0));
    shadow = shadow < 3.0? shadow / 5.0 : 1.0;

    float color = max(-dot(light_vector.xyz, normal_vector), 0.0);
    shadow = color * max(shadow, light_vector.a);
}
