#version 300 es

in vec3 mean_position;

out vec4 vertex_position;

uniform mat4 rotation_matrix;
uniform float coefficients[199];
uniform sampler2D principal_components;

void main(void) {
    int c_pos = gl_VertexID;
    ivec2 texPos = ivec2(c_pos % 8192, c_pos / 8192);
    vec4 tmp = vec4(0.0);
    for (int i = 0; i < 199; i++) {
        tmp += texelFetch(principal_components, texPos, 0) * coefficients[i];
        c_pos += 53490;
        texPos = ivec2(c_pos % 8192, c_pos / 8192);
    }
    gl_Position = rotation_matrix * vec4(mean_position + vec3(tmp), 246006.0);
    vertex_position = gl_Position;
}
