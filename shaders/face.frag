#version 420

precision mediump float;

in vec4 vertex_position;
in vec4 source_position;

uniform mat4 light_matrix;

layout(location = 0) out vec4 fragment_color;
uniform vec4 light_vector;
layout(binding=1) uniform sampler2D depth_map;

void main(void) {
    vec4 light_projection = light_matrix * source_position;
    vec3 normal_vector = normalize(
        cross(dFdx(vertex_position).xyz, dFdy(vertex_position).xyz));
    float color = dot(light_vector.xyz, normal_vector);
    float shadow = texture(
        depth_map,
        0.5 * light_projection.xy / light_projection.w + 0.5).r
        + 0.5 - 0.5 * (light_projection.z / light_projection.w)
        < 1.0 - 0.01 ? 1.0 : 0.0;
    fragment_color.xyz = vec3(max(color, light_vector.a)) - shadow;
    fragment_color.a = 1.0;
}
