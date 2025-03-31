import numpy as np
import matplotlib.pyplot as plt


# Init (n, list_x, list_y)
def init(n, list_x, list_y, k0, kn):
    n = int(input("Nhap n (so cap x-y  cho truoc): "))
    list_x = np.zeros(n)
    list_y = np.zeros(n)

    for i in range(n):
        list_x[i], list_y[i] = map(float, input(f"Nhap x[{i}], y[{i}]: ").split())
    
    k0 = float(input("Nhap k0: "))
    kn = float(input(f"Nhap kn (k{n-1}): "))

    return n, list_x, list_y, k0, kn

# Calculate k (1 -> n-2) by matrix
def cal_k(n, h, list_y, k0, kn):
    A = np.zeros((n - 2, n - 2))
    B = np.zeros(n - 2)

    for i in range(n - 2):
        for j in range(n - 2):
            if i == j:
                A[i][j] = 4
            elif i == j + 1 or i == j - 1:
                A[i][j] = 1
    
    for i in range(n - 2):
        B[i] = 3 * (list_y[i + 2] - list_y[i]) / h
        if (i == 0 or i == n - 3):
            B[i] = B[i] - k0 if i == 0 else B[i] - kn

    # print(A)
    # print(B)
    k = np.linalg.solve(A, B)
    k = np.insert(k, 0, k0)
    k = np.append(k, kn)
    # Làm tròn k
    for i in range(n - 1):
        k[i] = round(k[i], 3)
    return k

# Compute spline3 by return array a_ij
def spline3(n, list_x, list_y, k0, kn, h):
    k = cal_k(n, h, list_y, k0, kn)
    print(k)
    a = np.zeros((n - 1, 4))

    for i in range(n - 1):
        a[i][0] = list_y[i]
        a[i][1] = k[i]
        a[i][2] = 3 * (1 / h**2) * (list_y[i + 1] - list_y[i]) - (1 / h) * (2 * k[i] + k[i + 1])
        a[i][3] = 2 * (1 / h**3) * (list_y[i] - list_y[i + 1]) + (1 / h**2) * (k[i] + k[i + 1])
    return a
        

# # test
# x = np.array([-2.0, -1.0, 0.0, 1.0, 2.0], dtype=float)
# y = np.array([0.0, 0.0, 1.0, 0.0, 0.0], dtype=float)
# n = 5
# h = 1

# a = spline3(n, x, y, 0, 0, h)
# print(a)

# Main
if __name__ == "__main__":
    n, list_x, list_y, k0, kn = 0, [], [], 0, 0
    n, list_x, list_y, k0, kn = init(n, list_x, list_y, k0, kn)
    h = list_x[1] - list_x[0]
    a = spline3(n, list_x, list_y, k0, kn, h)
    print(f"Ket qua:\n{a}")

    # Draw graph
    ### My code
    x = np.linspace(list_x[0], list_x[-1], 1000)
    y = np.zeros(x.shape)
    for i in range(n - 1):
        idx = np.where((x >= list_x[i]) & (x <= list_x[i + 1]))
        y[idx] = a[i][0] + a[i][1] * (x[idx] - list_x[i]) + a[i][2] * (x[idx] - list_x[i])**2 + a[i][3] * (x[idx] - list_x[i])**3
    plt.plot(x, y, label='my code')
    plt.scatter(list_x, list_y, color='red')

    ### Scipy code
    from scipy.interpolate import CubicSpline
    cs = CubicSpline(list_x, list_y, bc_type='natural')
    plt.plot(x, cs(x), '--', label='CubicSpline from scipy library')
    plt.legend()
    plt.show()

    # Test
    input_x = float(input("Nhap x de tinh y: "))
    y = cs(input_x)
    print(f"y({input_x}) = {y}")
