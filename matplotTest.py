import numpy
import matplotlib.pyplot as plt
plt.style.use('ggplot')

def f(i):
    return i**2 - 8*i + 1

x_train = numpy.array([], dtype=float)
y_train = numpy.array([], dtype=float)

# init the graph y = 2*x
a, b = input("Type bounder [a, b] of the graph: ").split()
a = float(a)
b = float(b)
for i in numpy.arange(a, b, 0.1):
    x_train = numpy.append(x_train, i)
    y_train = numpy.append(y_train, f(i))

# Data point
plt.scatter(x_train, y_train, marker=".", c="r")
# Plot title
plt.title("My function")
# vertical axis
plt.xlabel("number of year")
# horizontial axix
plt.ylabel("How i love LKL")

# Show the graph
plt.show()