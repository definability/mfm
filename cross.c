#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <assert.h>

#define COMPONENTS_COUNT 3

#define X_OFFSET 0
#define Y_OFFSET 1
#define Z_OFFSET 2

void cross(float* vertices, uint16_t* triangles, float* result, int amount) {
    size_t u, v, w;
    size_t triangle;
    float ux, uy, uz;
    float vx, vy, vz;
    float wx, wy, wz;
    int i = 0;

    do {
        triangle = COMPONENTS_COUNT*i;

        u = COMPONENTS_COUNT * ((size_t)triangles[triangle + 0]);
        v = COMPONENTS_COUNT * ((size_t)triangles[triangle + 1]);
        w = COMPONENTS_COUNT * ((size_t)triangles[triangle + 2]);

        wx = vertices[w + X_OFFSET];
        wy = vertices[w + Y_OFFSET];
        wz = vertices[w + Z_OFFSET];

        ux = vertices[u + X_OFFSET] - wx;
        uy = vertices[u + Y_OFFSET] - wy;
        uz = vertices[u + Z_OFFSET] - wz;

        vx = vertices[v + X_OFFSET] - wx;
        vy = vertices[v + Y_OFFSET] - wy;
        vz = vertices[v + Z_OFFSET] - wz;

        result[triangle + X_OFFSET] = uy*vz - uz*vy;
        result[triangle + Y_OFFSET] = uz*vx - ux*vz;
        result[triangle + Z_OFFSET] = ux*vy - uy*vx;
    } while (++i < amount);
}

void normals(float* normal_vectors, uint16_t* triangles, float* result,
             int amount) {
    uint16_t vertex;
    float normal_x, normal_y, normal_z;
    int i = 0;
    int j;

    do {
        j = 0;
        normal_x = normal_vectors[i*COMPONENTS_COUNT + X_OFFSET];
        normal_y = normal_vectors[i*COMPONENTS_COUNT + Y_OFFSET];
        normal_z = normal_vectors[i*COMPONENTS_COUNT + Z_OFFSET];
        do {
            vertex = triangles[i*COMPONENTS_COUNT + j];
            result[vertex*COMPONENTS_COUNT + X_OFFSET] += normal_x;
            result[vertex*COMPONENTS_COUNT + Y_OFFSET] += normal_y;
            result[vertex*COMPONENTS_COUNT + Z_OFFSET] += normal_z;
        } while (++j < COMPONENTS_COUNT);
    } while (++i < amount);
}

void normalize(float* normals, int amount) {
    float norm;
    int i = 0;
    size_t normal_x, normal_y, normal_z;

    do {
        normal_x = i*COMPONENTS_COUNT + X_OFFSET;
        normal_y = i*COMPONENTS_COUNT + Y_OFFSET;
        normal_z = i*COMPONENTS_COUNT + Z_OFFSET;

        norm = sqrt(normals[normal_x] * normals[normal_x]
                  + normals[normal_y] * normals[normal_y]
                  + normals[normal_z] * normals[normal_z]);
        normals[normal_x] /= norm;
        normals[normal_y] /= norm;
        normals[normal_z] /= norm;
    } while (++i < amount);
}

void get_normals(float* vertices, uint16_t* triangles, float* normal_map,
                 int vertices_count, int triangles_count) {
    float* normal_vectors = (float*)malloc(COMPONENTS_COUNT *
                            sizeof(float) * triangles_count);
    assert(normal_vectors);
    cross(vertices, triangles, normal_vectors, triangles_count);
    normals(normal_vectors, triangles, normal_map, triangles_count);
    normalize(normal_map, vertices_count);
    free(normal_vectors);
}
