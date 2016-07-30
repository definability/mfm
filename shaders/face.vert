#version 300 es

in vec3 vin_position;
in vec3 vin_color;

out vec3 vout_color;

uniform mat4 rotation_matrix;

void main(void) {
    vout_color = vin_color;
    gl_Position = rotation_matrix * vec4(vin_position, 1.0);
}
