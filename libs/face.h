void get_face(float* mean_shape, float* principal_components,
              float* pc_deviations, float* coefficients,
              float* face, int dimensions, int vertices);

void get_row(float* principal_components, float* pc_deviations,
             float coefficient_difference, int row,
             float* face, int dimensions, int vertices);