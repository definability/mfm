void calculate_face(float* mean_shape, float* principal_components,
                    float* pc_deviations, float* coefficients,
                    float* face, size_t dimensions, size_t vertices);
void calculate_row(float* principal_components, float* pc_deviations,
                   float coefficient_difference, size_t row,
                   float* face, size_t dimensions, size_t vertices);
