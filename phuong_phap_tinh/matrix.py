import numpy as np

# Inputs:
# - Number of rows: 3
# - Elements of row 0: 1 2 3
# - Elements of row 1: 4 5 6
# - Elements of row 2: 7 8 9

# Output:
# [[1, 2, 3],
#  [4, 5, 6],
#  [7, 8, 9]]
# String is the input format: "1 2 3 4 5 6 7 8 9"
# Split the string by space
def matrix_init(num_of_row: int) -> np.array:
    # Init empty matrix
    matrix = []

    # For each row input -> append to matrix
    for i in range(num_of_row):
        matrix_row = input(f"Elements of row {i}: ").split(' ')
        matrix_row = np.array(matrix_row, dtype=float)
        matrix.append(matrix_row)

    # Convert matrix to numpy array
    matrix = np.array(matrix)
    
    return matrix
        

# Print matrix function
def matrix_print(matrix: np.array, name: str) -> None:
    print(f"{name}:\n{matrix}")


# Calculate and print determinant of matrix
def matrix_determinant(matrix: np.array) -> float:
    det = np.linalg.det(matrix)
    return det

def generate_test_case(n):
    A = np.random.rand(n, n) * 10 
    x_true = np.random.rand(n) * 10  
    b = np.dot(A, x_true)  
    augmented_matrix = np.hstack((A, b.reshape(-1, 1))) 

    f = open("test_case.txt", "w")
    f.write(str(n) + "\n")
    for i in range(n):
        for j in range(n + 1):
            f.write(str(augmented_matrix[i][j]))
            if j != n:
                f.write(" ")
        f.write("\n")
    f.close()
    return augmented_matrix

print(generate_test_case(10))

