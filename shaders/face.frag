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
    float color = dot(light_vector.xyz, normal_vector);
    float shadow = textureProj(depth_map, light_projection);
    fragment_color.xyz = vec3(max(color, light_vector.a)) * shadow;
    fragment_color.a = 1.0;
}
