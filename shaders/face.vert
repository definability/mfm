#version 300 es

in vec3 vin_position;
in vec3 vin_normal;

out vec3 vout_color;

uniform mat4 vin_light;
uniform mat4 rotation_matrix;

void main(void) {
    if (vin_light[1][3] < 1.0) {
        vout_color = vec3(dot(vec4(vin_normal, 1.0), vin_light[0]));
    } else {
        vout_color = vec3((vec4(vin_normal, 0.0) - vin_light[0]) / vin_light[1]);
    }
    gl_Position = rotation_matrix * vec4(vin_position, 1.0);
}
