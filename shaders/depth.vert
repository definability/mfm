#version 300 es

in vec3 face_vertices;

uniform mat4 light_matrix;

void main(void) {
    gl_Position = light_matrix * vec4(face_vertices, 246006.0);
}
