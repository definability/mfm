#include <stdlib.h>
#include <stdint.h>
#include <math.h>

void normals(float* normal_vectors, uint16_t* triangles, float* result,
             int amount) {
    uint16_t triangle;
    int i = 0;
    int j;

    do {
        j = 0;
        do {
            triangle = triangles[3*i + j];
            if (result[triangle*3] == 0.f) {
                result[triangle*3]     = normal_vectors[3*i];
                result[triangle*3 + 1] = normal_vectors[3*i + 1];
                result[triangle*3 + 2] = normal_vectors[3*i + 2];
            }
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

