#version 110

in float shadow;

void main(void) {
    gl_FragColor.xyz = vec3(shadow);
    gl_FragColor.a = 1.0;
}
