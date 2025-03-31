import numpy as np
import matplotlib.pyplot as plt

import random

# Generate 50 training data points
import numpy as np
import os

def generate_data():
    np.random.seed(42)  # For reproducibility
    
    # Generate random x values within a range (e.g., 0 to 23)
    x_train = np.sort(np.random.uniform(0, 23, 50))
    
    # Create y_train with a more scattered effect
    y_train = 2 * x_train + np.random.randn(*x_train.shape) * 5  # Larger noise factor
    
    # Ensure the directory exists before saving
    save_path = "C:\\Users\\ADMIN\\Desktop\\PythonCoding\\.cph\\gradient_descent"
    os.makedirs(save_path, exist_ok=True)
    
    file_path = os.path.join(save_path, "train_data.txt")
    
    with open(file_path, 'w') as f:
        f.write(str(x_train.shape[0]) + '\n')
        for i in range(x_train.shape[0]):
            f.write(f"{x_train[i]:.4f} {y_train[i]:.4f}\n")
    
    print(f"Data saved to {file_path}")

# Run the function to generate data
generate_data()


generate_data()
# Show the data
def show_data():
    # Load the data from the file
    f = open('C:\\Users\\ADMIN\\Desktop\\PythonCoding\\.cph/gradient_descent/train_data.txt', 'r')
    shape = int(f.readline().strip())

    x_train = np.zeros(shape)
    y_train = np.zeros(shape)

    for i in range(shape):
        line = f.readline()
        x_train[i] = float(line.split()[0])
        y_train[i] = float(line.split()[1])

    plt.scatter(x_train, y_train)
    plt.show()

show_data()

def load_data():
    x_train = np.zeros((x_shape, 1))
    y_train = np.zeros((x_shape, 1))

    # Open the file and read the data
    f = open('data.txt', 'r')

    # First line is the number of x_train
    shape = f.readlines()
    shape = int(shape[0].strip())

    # Read the data
    for i in range(shape):
        line = f.readline()
        x_train[i] = float(line.split()[0])
        y_train[i] = float(line.split()[1])
