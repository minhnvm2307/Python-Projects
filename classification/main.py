import numpy as np
import matplotlib.pyplot as plt
import random

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

x = np.arange(-10, 10)

y = sigmoid(x)

w = np.array([1])
b = 0


z = w * x + b

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.plot(z, y, label='Sigmoid', color='blue')
ax.plot(x, z, label='z', color='red')
ax.set_title('Sigmoid Function')
ax.set_xlabel('Input')
ax.set_ylabel('Output')
ax.set_ylim(-0.1, 1.1) 
ax.legend()
plt.grid()
plt.show()