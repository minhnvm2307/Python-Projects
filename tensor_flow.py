import numpy as np

a = np.array([1, 2, 3])
ex = np.exp(a)
print(ex)
    
s = ex/np.sum(ex)

for i in range(len(s)):
    print(ex[i] / np.sum(ex))
print(s)