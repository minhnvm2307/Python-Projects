import matrix as my_matrix
import numpy as np

# Given Ax = b, find the det(A_i)
# Example:
# inputs =
# [[ 1. -1.  2. -1.  -8.],
#  [ 2. -2.  3. -3.  -20.],
#  [ 1.  1.  1.  0.   -2],
#  [ 1. -1.  4.  3.   4.]]

# -> b = [-8, -20, -2, 4]

# A_0 =
# [[ -1.  2. -1. -8],
#  [ -2.  3. -3. -20],
#  [  1.  1.  0. -2],
#  [ -1.  4.  3.  4.]]
# det(A) = 4.00
# det(A_0) = 28.00
# -> x_0 = det(A_0) / det(A) = 7.00
def krame(matrice: np.array) -> None:
    # Get the last column of the matrix
    b = matrice[:, -1]
    # Get the matrix without the last column
    A = matrice[:, :-1]
    # Calculate the determinant of A
    det_A = my_matrix.matrix_determinant(A)
    print(f"det(A) = {det_A:.2f}")

    # For each column of A, replace it with b
    for i in range(A.shape[1]):
        A_i = A.copy()
        A_i[:, i] = b
        det_A_i = my_matrix.matrix_determinant(A_i)
        print(f"det(A_{i}) = {det_A_i:.2f}")
        print(f"x_{i} = det(A_{i}) / det(A) = {det_A_i / det_A:.2f}")

# Main function
if __name__ == "__main__":
    # Get the matrix from user
    num_of_row = int(input("Number of rows: "))
    matrix = my_matrix.matrix_init(num_of_row)
    my_matrix.matrix_print(matrix, "Matrix A")

    # Solve the system of linear equations by Krame method
    krame(matrix)