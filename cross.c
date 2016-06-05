#include <stdlib.h>
#include <stdint.h>
#include <math.h>

void cross(float* vertices, uint16_t* triangles, float* result,
           int amount) {
    size_t u, v, w;
    int i = 0;

    do {
        u = 3 * ((size_t)triangles[3*i + 1]);
        v = 3 * ((size_t)triangles[3*i + 2]);
        w = 3 * ((size_t)triangles[3*i + 0]);

        result[3*i]     = (vertices[u+1] - vertices[w+1]) *
                          (vertices[v+2] - vertices[w+2]) -
                          (vertices[u+2] - vertices[w+2]) *
                          (vertices[v+1] - vertices[w+1]);

        result[3*i + 1] = (vertices[u+2] - vertices[w+2]) *
                          (vertices[v+0] - vertices[w+0]) -
                          (vertices[u+0] - vertices[w+0]) *
                          (vertices[v+2] - vertices[w+2]);

        result[3*i + 2] = (vertices[u+0] - vertices[w+0]) *
                          (vertices[v+1] - vertices[w+1]) -
                          (vertices[u+1] - vertices[w+1]) *
                          (vertices[v+0] - vertices[w+0]);

        i++;
    } while (i < amount);
}

void normals(float* normal_vectors, uint16_t* triangles, float* result,
             int amount) {
    uint16_t triangle;
    int i = 0;
    int j;

    do {
        j = 0;
        do {
            triangle = triangles[3*i + j];
            result[triangle*3]     += normal_vectors[3*i];
            result[triangle*3 + 1] += normal_vectors[3*i + 1];
            result[triangle*3 + 2] += normal_vectors[3*i + 2];
            j++;
        } while (j < 3);
        i++;
    } while (i < amount);
}

void normalize(float* normals, int amount) {
    float norm;
    int i = 0;

    do {
        norm = sqrt(normals[3*i]     * normals[3*i]
                  + normals[3*i + 1] * normals[3*i + 1]
                  + normals[3*i + 2] * normals[3*i + 2]);
        normals[3*i] /= norm;
        normals[3*i + 1] /= norm;
        normals[3*i + 2] /= norm;
        i++;
    } while (i < amount);
}
