#version 420

precision mediump float;

in vec4 vertex_position;
in float shadow;

layout(location = 0) out vec4 fragment_color;
uniform vec4 light_vector;

void main(void) {
    vec3 normal_vector = normalize(
        cross(dFdx(vertex_position).xyz, dFdy(vertex_position).xyz));
    float color = max(dot(light_vector.xyz, normal_vector), 0.0);
    fragment_color.xyz = vec3(color * max(shadow, light_vector.a));
    fragment_color.a = 1.0;
}
