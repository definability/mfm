#include <stdlib.h>
#include <stdint.h>

#include "face.h"

void calculate_face(float* mean_shape, float* principal_components,
                    float* pc_deviations, float* coefficients,
                    float* face, size_t dimensions, size_t vertices) {
    size_t i = 0, j;
    do {
        face[i] = mean_shape[i];
        j = 0;
        do {
            face[i] += principal_components[i * dimensions + j]
                       * coefficients[j] * pc_deviations[j];
        } while(++j < dimensions);
    } while(++i < vertices);
}

void calculate_row(float* principal_components, float* pc_deviations,
                   float coefficient_difference, size_t row,
                   float* face, size_t dimensions, size_t vertices) {
    size_t i = 0;
    do {
        face[i] += principal_components[i * dimensions + row]
                   * coefficient_difference * pc_deviations[row];
    } while(++i < vertices);
}
