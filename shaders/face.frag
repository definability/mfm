#version 300 es

precision mediump float;

in vec3 vout_color;
out vec4 fout_color;

void main(void) {
    fout_color = vec4(vout_color, 1.0);
}
