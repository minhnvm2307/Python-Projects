import matrix as my_matrix
import numpy as np



def swap_rows(matrix, row_a, row_b):
    matrix[row_a, :], matrix[row_b, :] = matrix[row_b, :].copy(), matrix[row_a, :].copy()



def upper_triangle_matrix(matrix) -> np.array:
    N = matrix.shape[0]
    for i in range(1, N):
        if (matrix[i-1, i-1] == 0):
            for j in range(i, N):
                if (matrix[j, i-1] != 0):
                    swap_rows(matrix, i-1, j)
                    break
        
        for j in range(i, N):
            m = -1 * matrix[j, i-1] / matrix[i-1, i-1]
            for k in range(i-1, N+1):
                matrix[j, k] += m * matrix[i-1, k]
    return matrix


def gauss(matrix) -> np.array:
    N = matrix.shape[0]
    matrix = upper_triangle_matrix(matrix)

    # Print the upper triangle matrix
    my_matrix.matrix_print(matrix, "Matrix A (Upper triangle)")

    x = np.zeros(N)
    for i in range(N-1, -1, -1):
        s = 0
        for j in range(i+1, N):
            s += matrix[i, j] * x[j]
        x[i] = (matrix[i, N] - s) / matrix[i, i]
    return x



# Main function
if __name__ == "__main__":
    # Get the matrix from user
    num_of_row = int(input("Number of rows: "))
    matrix = my_matrix.matrix_init(num_of_row)
    # my_matrix.matrix_print(matrix, "Matrix A")

    # Solve the system of linear equations by Gauss method
    x = gauss(matrix)
    for i in range(len(x)):
        print(f"x_{i} = {x[i]:.2f}")