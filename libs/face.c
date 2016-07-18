#include <stdlib.h>
#include <stdint.h>

#include "face.h"

void calculate_face(float* mean_shape, float* principal_components,
                    float* pc_deviations, float* coefficients, float* face,
                    size_t coefficients_count, size_t dimensions,
                    size_t vertices) {
    size_t j;
    while (vertices --> 0) {
        face[vertices] = mean_shape[vertices];
        j = coefficients_count;
        while (j --> 0) {
            face[vertices] += principal_components[vertices * dimensions + j]
                              * coefficients[j] * pc_deviations[j];
        }
    }
}

void calculate_row(float* principal_components, float* pc_deviations,
                   float coefficient_difference, size_t row,
                   float* face, size_t dimensions, size_t vertices) {
    while (vertices --> 0) {
        face[vertices] += principal_components[vertices * dimensions + row]
                          * coefficient_difference * pc_deviations[row];
    }
}
