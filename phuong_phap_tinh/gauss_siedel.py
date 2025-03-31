import matrix as my_matrix
import numpy as np

# jacobi iterative method
def gauss_siedel(matrix: np.array, x_0: np.array, tol: float):
    k = 1
    N = matrix.shape[0]

    while (k <= N):
        for i in range(N):
            s = 0
            for j in range(N):
                if (i != j):
                    s += matrix[i, j] * x_0[j] + matrix[i, N]
            x_0[i] = (matrix[i, N] - s) / matrix[i, i]

        # Check the tolerance
        if (np.linalg.norm(x_0 - matrix[:, N]) < tol):
            break

        # else, update k
        k += 1

    return x_0

# Main function
if __name__ == "__main__":
    # Test the Gauss-Siedel method
    f = open("test_case.txt", "r")
    num_of_row = int(f.readline())
    augmented_matrix = np.zeros((num_of_row, num_of_row + 1))
    for i in range(num_of_row):
        augmented_matrix[i] = np.array(f.readline().split(), dtype=float)

    # Get the initial guess
    x_0 = np.zeros(num_of_row)

    # Get the tolerance
    tol = float(input("Tolerance: "))

    # Solve the system of linear equations by Gauss-Siedel method
    x = gauss_siedel(augmented_matrix, x_0, tol)
    for i in range(len(x)):
        print(f"x_{i} = {x[i]:.2f}")