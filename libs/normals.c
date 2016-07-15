#include <stdlib.h>
#include <stdint.h>
#include <math.h>
#include <assert.h>

#include "normals.h"

#define COMPONENTS_COUNT 3

#define X_OFFSET 0
#define Y_OFFSET 1
#define Z_OFFSET 2

void cross(float* vertices, uint16_t* triangles, float* result, size_t amount) {
    size_t u, v, w;
    size_t triangle;
    float ux, uy, uz;
    float vx, vy, vz;
    float wx, wy, wz;

    while (amount --> 0) {
        triangle = COMPONENTS_COUNT*amount;

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
    }
}

void normals(float* normal_vectors, uint16_t* triangles, float* result,
             size_t amount) {
    uint16_t vertex;
    float normal_x, normal_y, normal_z;
    size_t j;

    while (amount --> 0) {
        normal_x = normal_vectors[amount*COMPONENTS_COUNT + X_OFFSET];
        normal_y = normal_vectors[amount*COMPONENTS_COUNT + Y_OFFSET];
        normal_z = normal_vectors[amount*COMPONENTS_COUNT + Z_OFFSET];

        j = COMPONENTS_COUNT;
        while (j --> 0) {
            vertex = triangles[amount*COMPONENTS_COUNT + j];
            result[vertex*COMPONENTS_COUNT + X_OFFSET] += normal_x;
            result[vertex*COMPONENTS_COUNT + Y_OFFSET] += normal_y;
            result[vertex*COMPONENTS_COUNT + Z_OFFSET] += normal_z;
        }
    }
}

void normalize(float* normals, size_t amount) {
    float norm;
    size_t normal_x, normal_y, normal_z;

    while (amount --> 0) {
        normal_x = amount*COMPONENTS_COUNT + X_OFFSET;
        normal_y = amount*COMPONENTS_COUNT + Y_OFFSET;
        normal_z = amount*COMPONENTS_COUNT + Z_OFFSET;

        norm = sqrt(  normals[normal_x] * normals[normal_x]
                    + normals[normal_y] * normals[normal_y]
                    + normals[normal_z] * normals[normal_z]);
        normals[normal_x] /= norm;
        normals[normal_y] /= norm;
        normals[normal_z] /= norm;
    }
}

void get_normals(float* vertices, uint16_t* triangles, float* normal_map,
                 size_t vertices_count, size_t triangles_count) {
    float* normal_vectors = (float*)malloc(
        COMPONENTS_COUNT * sizeof(float) * triangles_count);
    assert(normal_vectors);
    cross(vertices, triangles, normal_vectors, triangles_count);
    normals(normal_vectors, triangles, normal_map, triangles_count);
    normalize(normal_map, vertices_count);
    free(normal_vectors);
}
