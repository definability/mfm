void get_face(float* mean_shape, float* principal_components,
              float* pc_deviations, float* coefficients,
              float* face, int dimensions, int vertices) {
    int i = 0, j;
    do {
        face[i] = mean_shape[i];
        j = 0;
        do {
            face[i] += principal_components[i * dimensions + j]
                     * coefficients[j] * pc_deviations[j];
        } while(++j < dimensions);
    } while(++i < vertices);
}
