#version 420

precision mediump float;

in vec4 vertex_position;
in vec4 light_projection;

layout(location = 0) out vec4 fragment_color;
uniform vec4 light_vector;
layout(binding=1) uniform sampler2DShadow depth_map;

void main(void) {
    vec3 normal_vector = normalize(
        cross(dFdx(vertex_position).xyz, dFdy(vertex_position).xyz));
    float color = max(dot(light_vector.xyz, normal_vector), 0.0);
    float shadow = 0.0;
    shadow += textureProjOffset(depth_map, light_projection, ivec2(-1, -1));
    shadow += textureProjOffset(depth_map, light_projection, ivec2(-1, 1));
    shadow += textureProjOffset(depth_map, light_projection, ivec2(1, -1));
    shadow += textureProjOffset(depth_map, light_projection, ivec2(1, 1));
    shadow += textureProjOffset(depth_map, light_projection, ivec2(0, 0));
    shadow = shadow < 3.0? shadow / 5.0 : 1.0;
    fragment_color.xyz = vec3(color * max(shadow, light_vector.a));
    fragment_color.a = 1.0;
}
